"""Regenerate the two visual artefacts that were thin in the first pass.

1. results/figs/loss_curves.png — 2x2 grid, one panel per noise level,
   train+val per architecture (6 lines each panel, log-y).

2. results/figs/reconstructions.png — 2x2 grid, one panel per target
   frequency (1/3/5/7 Hz), each panel overlaying noisy input + clean
   target + FC/RNN/LSTM predictions on a representative test window.

Reads the artefacts under results/runs/ and the seed=42 base-matrix runs
recorded in results/experiment_matrix.csv. No re-training.

Usage:
    uv run python scripts/regenerate_plots.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch

from sinusoid_extractor.constants import FIXED_FREQUENCIES_HZ, Architecture
from sinusoid_extractor.models.registry import ModelRegistry
from sinusoid_extractor.sdk.sdk import SinusoidExtractorSDK
from sinusoid_extractor.services.metrics import mse
from sinusoid_extractor.services.torch_dataset import SinusoidWindowDataset

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FIGS = RESULTS / "figs"
ARCHES = ("fc", "rnn", "lstm")
ARCH_COLOR = {"fc": "#1f77b4", "rnn": "#ff7f0e", "lstm": "#2ca02c"}
SEED = 42
ALPHAS = (0.01, 0.05, 0.10, 0.20)
ALPHA_RECON = 0.05


def find_run(arch: str, alpha: float, seed: int) -> Path:
    df = pd.read_csv(RESULTS / "experiment_matrix.csv")
    sub = df[(df.architecture == arch) & (df.seed == seed) & (np.isclose(df.alpha, alpha))]
    if sub.empty:
        raise SystemExit(f"no run for {arch} alpha={alpha} seed={seed}")
    return RESULTS / "runs" / str(sub.iloc[0]["run_id"])


def render_loss_curves() -> Path:
    sns.set_theme(style="whitegrid", palette="colorblind")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=False)
    for ax, alpha in zip(axes.flat, ALPHAS, strict=True):
        for arch in ARCHES:
            run_dir = find_run(arch, alpha, SEED)
            d = json.loads((run_dir / "loss_history.json").read_text())
            color = ARCH_COLOR[arch]
            epochs = list(range(1, len(d["train_loss_per_epoch"]) + 1))
            ax.plot(epochs, d["train_loss_per_epoch"],
                    color=color, lw=1.5, label=f"{arch.upper()} train")
            ax.plot(epochs, d["val_loss_per_epoch"],
                    color=color, lw=1.5, ls="--", label=f"{arch.upper()} val")
        ax.set_yscale("log")
        ax.set_title(f"alpha = {alpha:g}")
        ax.set_xlabel("epoch")
        ax.set_ylabel("loss (log)")
        ax.grid(True, which="both", alpha=0.3)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=6, loc="upper center", bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("Train + validation loss per architecture, per noise level (seed=42)",
                 y=1.06)
    fig.tight_layout()
    out = FIGS / "loss_curves.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def render_reconstructions() -> Path:
    sdk = SinusoidExtractorSDK(config_path=REPO / "config" / "setup.json",
                                results_dir=RESULTS)
    bundle = sdk.generate_dataset(alpha=ALPHA_RECON, seed=SEED)
    test = bundle.test
    class_ids = np.argmax(test.C, axis=1)
    selected: dict[int, int] = {}
    for k, freq in enumerate(FIXED_FREQUENCIES_HZ):
        idxs = np.where(class_ids == k)[0]
        if not idxs.size:
            continue
        # pick the example with the highest target peak-to-peak — phase will be informative
        ranges = test.y[idxs].max(axis=1) - test.y[idxs].min(axis=1)
        selected[freq] = int(idxs[int(ranges.argmax())])

    preds: dict[str, np.ndarray] = {}
    for arch in ARCHES:
        run_dir = find_run(arch, ALPHA_RECON, SEED)
        history = json.loads((run_dir / "loss_history.json").read_text())
        model = ModelRegistry.build(arch, **history["model_cfg"])
        model.load_state_dict(torch.load(run_dir / "best_model.pt", weights_only=True))
        model.eval()
        ds = SinusoidWindowDataset(test, Architecture(arch))
        with torch.no_grad():
            full = torch.stack([ds[i][0] for i in range(len(ds))])
            preds[arch] = model(full).cpu().numpy()

    sns.set_theme(style="whitegrid", palette="colorblind")
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    sample_idx = np.arange(test.x.shape[1])
    for ax, freq in zip(axes.flat, FIXED_FREQUENCIES_HZ, strict=True):
        i = selected[freq]
        ax.plot(sample_idx, test.x[i], "k:", lw=1.0, alpha=0.7, label="noisy input (Σ)")
        ax.plot(sample_idx, test.y[i], "k", lw=2.5, label="clean target")
        notes = []
        for arch in ARCHES:
            yp = preds[arch][i]
            ax.plot(sample_idx, yp, color=ARCH_COLOR[arch], lw=1.6, label=f"{arch.upper()} pred")
            notes.append(f"{arch.upper()}={mse(yp, test.y[i]):.3f}")
        ax.set_title(f"Target = {freq} Hz")
        ax.set_xlabel("sample index (0–9)")
        ax.set_ylabel("amplitude")
        ax.text(0.02, 0.05, "MSE: " + "  ".join(notes),
                transform=ax.transAxes, fontsize=8,
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="0.8"))
        ax.grid(True, alpha=0.3)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    axes[0, 1].legend(handles, labels, loc="upper right", fontsize=8)
    fig.suptitle("Reconstruction examples per target frequency "
                 "(test set, alpha=0.05, seed=42)", y=1.02)
    fig.tight_layout()
    out = FIGS / "reconstructions.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> int:
    FIGS.mkdir(parents=True, exist_ok=True)
    print(f"  loss_curves    -> {render_loss_curves()}")
    print(f"  reconstructions-> {render_reconstructions()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
