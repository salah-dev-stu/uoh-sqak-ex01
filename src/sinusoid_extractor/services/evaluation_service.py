"""Evaluation service — test-set metrics, per-frequency stratification, baseline."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader

from sinusoid_extractor.constants import FIXED_FREQUENCIES_HZ, Architecture, HookEvent
from sinusoid_extractor.models.registry import ModelRegistry
from sinusoid_extractor.services.data_bundle import DataBundle
from sinusoid_extractor.services.metrics import (
    mae,
    mse,
    predict_zero_baseline,
    r2_score,
    snr_db,
)
from sinusoid_extractor.services.torch_dataset import SinusoidWindowDataset
from sinusoid_extractor.services.training_service import RunHandle
from sinusoid_extractor.shared.hooks import HookRegistry
from sinusoid_extractor.shared.persistence import save_json

_log = logging.getLogger(__name__)


@dataclass
class EvalReport:
    """Aggregated test metrics + per-frequency breakdown."""

    run_id: str
    test_mse: float
    test_mae: float
    test_r2: float
    test_snr_db: float
    baseline_mse: float
    n_test: int
    per_freq_mse: dict[int, float] = field(default_factory=dict)
    per_freq_r2: dict[int, float] = field(default_factory=dict)


class EvaluationService:
    """Loads a trained checkpoint and computes metrics on the test split."""

    def __init__(self, config: dict[str, Any], hooks: HookRegistry | None = None) -> None:
        self.config = config
        self.hooks = hooks or HookRegistry()

    def evaluate(self, run: RunHandle, bundle: DataBundle) -> EvalReport:
        """Run the model on the test split and produce an :class:`EvalReport`."""
        self.hooks.fire(HookEvent.BEFORE_EVAL, run_id=run.run_id)
        model_cfg = self._read_training_model_cfg(run)
        model = ModelRegistry.build(run.architecture, **model_cfg)
        model.load_state_dict(torch.load(run.run_dir / "best_model.pt", weights_only=True))
        model.eval()

        loader = DataLoader(
            SinusoidWindowDataset(bundle.test, run.architecture),
            batch_size=int(self.config["training"]["batch_size"]),
        )
        preds, targets = self._collect(model, loader)

        report = EvalReport(
            run_id=run.run_id,
            test_mse=mse(preds, targets),
            test_mae=mae(preds, targets),
            test_r2=r2_score(preds, targets),
            test_snr_db=snr_db(preds, targets),
            baseline_mse=predict_zero_baseline(targets),
            n_test=int(targets.shape[0]),
            per_freq_mse=self._stratify(preds, targets, bundle.test.C, mse),
            per_freq_r2=self._stratify(preds, targets, bundle.test.C, r2_score),
        )
        save_json(run.run_dir / "eval_report.json", asdict(report))
        self.hooks.fire(HookEvent.AFTER_EVAL, run_id=run.run_id, report=report)
        return report

    @staticmethod
    def _collect(model, loader: DataLoader) -> tuple[np.ndarray, np.ndarray]:
        preds, targets = [], []
        with torch.no_grad():
            for inputs, target in loader:
                preds.append(model(inputs).cpu().numpy())
                targets.append(target.cpu().numpy())
        return np.concatenate(preds, axis=0), np.concatenate(targets, axis=0)

    @staticmethod
    def _stratify(preds: np.ndarray, targets: np.ndarray, one_hot: np.ndarray, fn) -> dict[int, float]:
        out: dict[int, float] = {}
        class_ids = np.argmax(one_hot, axis=1)
        for i, freq in enumerate(FIXED_FREQUENCIES_HZ):
            mask = class_ids == i
            if not mask.any():
                continue
            out[int(freq)] = float(fn(preds[mask], targets[mask]))
        return out

    @staticmethod
    def supported_archs() -> list[str]:
        """Helper used by tests to discover registered architectures."""
        return [a.value for a in Architecture]

    def _read_training_model_cfg(self, run: RunHandle) -> dict[str, Any]:
        """Read the exact model_cfg used at training time (handles OAT overrides)."""
        history_path = run.run_dir / "loss_history.json"
        if history_path.exists():
            from sinusoid_extractor.shared.persistence import load_json

            payload = load_json(history_path)
            persisted = payload.get("model_cfg")
            if isinstance(persisted, dict) and persisted:
                return dict(persisted)
        return dict(self.config["models"].get(run.architecture, {}))
