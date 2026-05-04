"""Plotting helpers — matplotlib + seaborn, colorblind palette, PNG-safe."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

PALETTE = "colorblind"


def _new_axes(figsize=(7, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def plot_signal(t: np.ndarray, signal: np.ndarray, title: str, save_to: Path | None = None):
    """Time-domain plot. Returns the ``Axes``."""
    fig, ax = _new_axes()
    ax.plot(t, signal, linewidth=1.0)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("amplitude")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
    return ax


def plot_fft(signal: np.ndarray, fs: int, title: str, save_to: Path | None = None):
    """Single-sided FFT magnitude up to Nyquist."""
    fig, ax = _new_axes()
    n = signal.shape[0]
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.abs(np.fft.rfft(signal)) / n * 2.0
    ax.plot(freqs, spectrum, linewidth=1.0)
    ax.set_xlim(0, 50)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("magnitude")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
    return ax


def plot_loss_curves(train: list[float], val: list[float], title: str, save_to: Path | None = None):
    """Train + validation loss curves on log y-axis."""
    fig, ax = _new_axes()
    ax.plot(range(1, len(train) + 1), train, label="train")
    ax.plot(range(1, len(val) + 1), val, label="val")
    ax.set_yscale("log")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss (log)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3, which="both")
    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
    return ax


def plot_reconstruction(pred: np.ndarray, target: np.ndarray, title: str, save_to: Path | None = None):
    """Two overlaid lines: prediction vs ground truth."""
    fig, ax = _new_axes()
    idx = np.arange(target.shape[0])
    ax.plot(idx, target, label="target", linewidth=1.5)
    ax.plot(idx, pred, label="prediction", linewidth=1.5, linestyle="--")
    ax.set_xlabel("sample")
    ax.set_ylabel("amplitude")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
    return ax


def plot_heatmap(matrix: np.ndarray, x_labels, y_labels, title: str, save_to: Path | None = None):
    """Generic 2-D heatmap (e.g. MSE × (arch, freq))."""
    fig, ax = _new_axes(figsize=(6, 4))
    im = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels)
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    ax.set_title(title)
    fig.colorbar(im, ax=ax)
    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
    return ax
