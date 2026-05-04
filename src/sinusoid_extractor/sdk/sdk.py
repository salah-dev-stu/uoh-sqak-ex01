"""Public SDK — the single entry point for all business logic.

External consumers (CLI, notebook, future GUI/REST) should import this class
and call its methods. Importing ``services.*`` directly bypasses the SDK
contract and is discouraged outside tests.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from sinusoid_extractor.constants import Architecture
from sinusoid_extractor.services.data_bundle import DataBundle
from sinusoid_extractor.services.dataset_service import DatasetService
from sinusoid_extractor.services.evaluation_service import EvalReport, EvaluationService
from sinusoid_extractor.services.sweep_service import SweepService
from sinusoid_extractor.services.training_service import RunHandle, TrainingService
from sinusoid_extractor.shared.config import load_config
from sinusoid_extractor.shared.gatekeeper import Gatekeeper
from sinusoid_extractor.shared.hooks import HookRegistry
from sinusoid_extractor.shared.persistence import ensure_dir, save_npz
from sinusoid_extractor.shared.version import __version__

_log = logging.getLogger(__name__)


class SinusoidExtractorSDK:
    """One-stop SDK for dataset generation, training, evaluation, sweeps.

    Building Block (RULES.md §16):
        Input  : (per method) alpha, seed, arch, bundle, run, etc.
                 — see method signatures.
        Output : (per method) DataBundle | RunHandle | EvalReport |
                 list[RunHandle] | dict.
        Setup  : config_path (Path | None), results_dir (Path | None),
                 gatekeeper (Gatekeeper | None — for DI in tests)
    """

    def __init__(
        self,
        config_path: Path | str | None = None,
        results_dir: Path | str | None = None,
        gatekeeper: Gatekeeper | None = None,
    ) -> None:
        self.config = load_config(config_path)
        self.results_dir = ensure_dir(
            Path(results_dir or self.config["paths"]["results_dir"])
        )
        self.data_dir = ensure_dir(Path(self.config["paths"]["data_dir"]))
        self.gatekeeper = gatekeeper or Gatekeeper()
        self.hooks = HookRegistry()
        self.dataset_service = DatasetService(self.config["dataset"])
        self.training_service = TrainingService(self.config, self.results_dir)
        self.evaluation_service = EvaluationService(self.config, self.hooks)
        self.sweep_service = SweepService(
            self.config, self.results_dir, self.training_service, self.evaluation_service
        )

    def get_version(self) -> str:
        return __version__

    def get_config(self) -> dict[str, Any]:
        return self.config

    def generate_dataset(self, alpha: float, seed: int | None = None) -> DataBundle:
        """Build the (raw signals, DataBundle) pair and persist raw to disk."""
        seed_value = int(seed if seed is not None else self.config["dataset"]["seed"])
        raw, bundle = self.dataset_service.generate(alpha=alpha, seed=seed_value)
        out = self.data_dir / "raw" / f"dataset_alpha{alpha:.3f}_seed{seed_value}.npz"
        save_npz(out, **raw)
        _log.info("persisted raw dataset to %s", out)
        return bundle

    def train_model(
        self,
        arch: str | Architecture,
        bundle: DataBundle,
        hyperparams: dict[str, Any] | None = None,
        seed: int | None = None,
    ) -> RunHandle:
        handle, _ = self.training_service.train(arch, bundle, hyperparams, seed)
        return handle

    def evaluate(self, run: RunHandle, bundle: DataBundle) -> EvalReport:
        return self.evaluation_service.evaluate(run, bundle)

    def run_experiment_matrix(self, limit: int | None = None) -> list[RunHandle]:
        return self.sweep_service.run_experiment_matrix(limit=limit)

    def run_oat_sweep(self, limit: int | None = None) -> list[RunHandle]:
        return self.sweep_service.run_oat_sweep(limit=limit)

    def health_check(self) -> dict[str, Any]:
        """Quick self-diagnostic: registry + gatekeeper + paths."""
        from sinusoid_extractor.models.registry import ModelRegistry

        return {
            "version": __version__,
            "config_version": self.config.get("version"),
            "registered_architectures": ModelRegistry.available(),
            "gatekeeper": self.gatekeeper.call("default"),
            "results_dir": str(self.results_dir),
            "data_dir": str(self.data_dir),
        }
