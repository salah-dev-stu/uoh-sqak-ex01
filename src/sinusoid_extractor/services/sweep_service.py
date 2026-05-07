"""Sweep service — runs the experiment matrix and the OAT sweep."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from sinusoid_extractor.services.dataset_service import DatasetService
from sinusoid_extractor.services.evaluation_service import EvaluationService
from sinusoid_extractor.services.training_service import RunHandle, TrainingService
from sinusoid_extractor.shared.persistence import append_csv_row

_log = logging.getLogger(__name__)


class SweepService:
    """Orchestrates the full experiment matrix and OAT sweep.

    Building Block (RULES.md §16):
        Input  : limit (int | None) — cap rows for smoke runs
        Output : list[RunHandle]. Side-effects: appends rows to
                 results/experiment_matrix.csv and results/sensitivity.csv;
                 also writes per-run loss + eval JSONs via the inner services.
        Setup  : config (full setup.json dict), results_dir (Path),
                 training (TrainingService), evaluation (EvaluationService)
    """

    def __init__(
        self,
        config: dict[str, Any],
        results_dir: Path,
        training: TrainingService,
        evaluation: EvaluationService,
    ) -> None:
        self.config = config
        self.results_dir = Path(results_dir)
        self.training = training
        self.evaluation = evaluation
        self.dataset_service = DatasetService(config["dataset"])

    def run_experiment_matrix(self, limit: int | None = None) -> list[RunHandle]:
        """For every (arch × alpha × seed): train and evaluate one run."""
        archs = self.config["experiment"]["architectures"]
        seeds = self.config["experiment"]["seeds"]
        alphas = self.config["dataset"]["noise_levels_alpha"]
        handles: list[RunHandle] = []
        for alpha in alphas:
            for seed in seeds:
                _, bundle = self.dataset_service.generate(alpha=float(alpha), seed=int(seed))
                for arch in archs:
                    handle = self._train_and_eval(arch, bundle, alpha, seed)
                    handles.append(handle)
                    if limit and len(handles) >= limit:
                        return handles
        return handles

    def run_oat_sweep(self, limit: int | None = None) -> list[RunHandle]:
        """Sweep one hyperparam at a time per architecture, fixed alpha + seed."""
        archs = self.config["experiment"]["architectures"]
        seed = int(self.config["experiment"]["seeds"][0])
        alpha = float(self.config["dataset"]["noise_levels_alpha"][0])
        _, bundle = self.dataset_service.generate(alpha=alpha, seed=seed)
        handles: list[RunHandle] = []
        for arch in archs:
            for hp_name, values in self.config["oat_sweep"].items():
                for value in values:
                    override = self._build_oat_override(hp_name, value)
                    handle, result = self.training.train(
                        arch=arch, bundle=bundle, hyperparams_override=override, seed=seed
                    )
                    report = self.evaluation.evaluate(handle, bundle)
                    append_csv_row(
                        self.results_dir / "sensitivity.csv",
                        {
                            "run_id": handle.run_id,
                            "architecture": arch,
                            "swept_hyperparam": hp_name,
                            "swept_value": value,
                            "seed": seed,
                            "alpha": alpha,
                            "test_mse": report.test_mse,
                            "test_r2": report.test_r2,
                            "epochs_run": result.epochs_run,
                            "wall_clock_s": result.wall_clock_seconds,
                        },
                    )
                    handles.append(handle)
                    if limit and len(handles) >= limit:
                        return handles
        return handles

    def _train_and_eval(self, arch: str, bundle, alpha: float, seed: int) -> RunHandle:
        handle, result = self.training.train(arch=arch, bundle=bundle, seed=seed)
        report = self.evaluation.evaluate(handle, bundle)
        per_freq_cols = {
            f"per_freq_mse_{int(f)}hz": report.per_freq_mse.get(int(f), float("nan"))
            for f in self.dataset_service.frequencies_hz
        }
        append_csv_row(
            self.results_dir / "experiment_matrix.csv",
            {
                "run_id": handle.run_id,
                "architecture": arch,
                "alpha": alpha,
                "seed": seed,
                "test_mse": report.test_mse,
                "test_mae": report.test_mae,
                "test_r2": report.test_r2,
                "test_snr_db": report.test_snr_db,
                "baseline_mse": report.baseline_mse,
                "epochs_run": result.epochs_run,
                "wall_clock_s": result.wall_clock_seconds,
                **per_freq_cols,
            },
        )
        return handle

    @staticmethod
    def _build_oat_override(hp_name: str, value: Any) -> dict[str, Any]:
        if hp_name == "learning_rate":
            return {"training": {"learning_rate": value}}
        return {"model": {hp_name: value}}
