"""High-level training service used by the SDK."""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader

from sinusoid_extractor.constants import Architecture
from sinusoid_extractor.models.registry import ModelRegistry
from sinusoid_extractor.services.data_bundle import DataBundle
from sinusoid_extractor.services.early_stopping import EarlyStopping
from sinusoid_extractor.services.loss_fn import WindowSumMSE
from sinusoid_extractor.services.optimizer_factory import build_optimizer
from sinusoid_extractor.services.torch_dataset import SinusoidWindowDataset
from sinusoid_extractor.services.training_loop import TrainingLoop, TrainingResult
from sinusoid_extractor.shared.persistence import ensure_dir, save_json

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunHandle:
    """Pointer to a completed training run on disk."""

    run_id: str
    run_dir: Path
    architecture: str
    seed: int


class TrainingService:
    """Builds model + optimizer + loaders and runs a :class:`TrainingLoop`.

    Building Block (RULES.md §16):
        Input  : arch (str | Architecture), bundle (DataBundle),
                 hyperparams_override (dict | None), seed (int | None)
        Output : (RunHandle, TrainingResult). Side-effects: persists
                 best_model.pt + loss_history.json under results/runs/<run_id>/.
        Setup  : config (full setup.json dict), results_dir (Path)
    """

    def __init__(self, config: dict[str, Any], results_dir: Path) -> None:
        self.config = config
        self.results_dir = Path(results_dir)

    def train(
        self,
        arch: str | Architecture,
        bundle: DataBundle,
        hyperparams_override: dict[str, Any] | None = None,
        seed: int | None = None,
    ) -> tuple[RunHandle, TrainingResult]:
        """Train one model on ``bundle``; persist artifacts; return handle + result."""
        arch_value = arch.value if isinstance(arch, Architecture) else str(arch)
        seed_value = int(seed if seed is not None else self.config["dataset"].get("seed", 42))
        self._set_global_seed(seed_value)

        model_cfg = self._merge_model_cfg(arch_value, hyperparams_override)
        training_cfg = self._merge_training_cfg(hyperparams_override)
        model = ModelRegistry.build(arch_value, **model_cfg)
        optimizer = build_optimizer(
            training_cfg["optimizer"], model.parameters(), training_cfg["learning_rate"]
        )
        loss_fn = WindowSumMSE()
        train_loader, val_loader = self._build_loaders(bundle, arch_value, training_cfg)
        early = EarlyStopping(patience=int(training_cfg["early_stopping_patience"]))
        loop = TrainingLoop(
            model=model,
            optimizer=optimizer,
            loss_fn=loss_fn,
            train_loader=train_loader,
            val_loader=val_loader,
            max_epochs=int(training_cfg["max_epochs"]),
            early_stopping=early,
            device="cpu",
        )
        result = loop.run()

        run_id = self._make_run_id(arch_value, bundle.alpha, seed_value)
        run_dir = ensure_dir(self.results_dir / "runs" / run_id)
        torch.save(model.state_dict(), run_dir / "best_model.pt")
        save_json(run_dir / "loss_history.json", self._build_loss_payload(
            run_id=run_id, arch=arch_value, bundle=bundle, model=model, model_cfg=model_cfg,
            training_cfg=training_cfg, result=result, seed=seed_value,
        ))
        return RunHandle(run_id, run_dir, arch_value, seed_value), result

    def _build_loaders(
        self, bundle: DataBundle, arch: str, training_cfg: dict[str, Any]
    ) -> tuple[DataLoader, DataLoader]:
        train_ds = SinusoidWindowDataset(bundle.train, arch)
        val_ds = SinusoidWindowDataset(bundle.val, arch)
        bs = int(training_cfg["batch_size"])
        nw = int(training_cfg.get("num_workers", 0))
        return (
            DataLoader(train_ds, batch_size=bs, shuffle=True, num_workers=nw),
            DataLoader(val_ds, batch_size=bs, shuffle=False, num_workers=nw),
        )

    def _merge_model_cfg(self, arch: str, override: dict[str, Any] | None) -> dict[str, Any]:
        base = dict(self.config["models"].get(arch, {}))
        if override and "model" in override:
            base.update(override["model"])
        return base

    def _merge_training_cfg(self, override: dict[str, Any] | None) -> dict[str, Any]:
        base = dict(self.config["training"])
        if override and "training" in override:
            base.update(override["training"])
        return base

    @staticmethod
    def _set_global_seed(seed: int) -> None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

    @staticmethod
    def _make_run_id(arch: str, alpha: float, seed: int) -> str:
        ts = time.strftime("%Y%m%dT%H%M%S")
        return f"{arch}_alpha{alpha:.3f}_seed{seed}_{ts}"

    @staticmethod
    def _build_loss_payload(**kw: Any) -> dict[str, Any]:
        result: TrainingResult = kw["result"]
        bundle: DataBundle = kw["bundle"]
        return {
            "run_id": kw["run_id"],
            "architecture": kw["arch"],
            "seed": kw["seed"],
            "alpha": bundle.alpha,
            "model_cfg": kw["model_cfg"],
            "training_cfg": kw["training_cfg"],
            "param_count": sum(p.numel() for p in kw["model"].parameters()),
            "epochs_run": result.epochs_run,
            "wall_clock_seconds": result.wall_clock_seconds,
            "best_val_loss": result.best_val_loss,
            "best_epoch": result.best_epoch,
            "train_loss_per_epoch": result.train_loss_per_epoch,
            "val_loss_per_epoch": result.val_loss_per_epoch,
        }
