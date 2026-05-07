"""DatasetService — composes signal generator + noise + windower + splitter."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

from sinusoid_extractor.constants import CONTEXT_WINDOW, FIXED_FREQUENCIES_HZ
from sinusoid_extractor.services.data_bundle import DataBundle, Split
from sinusoid_extractor.services.noise_model import NoiseModel
from sinusoid_extractor.services.signal_generator import SignalGenerator
from sinusoid_extractor.services.splitter import Splitter
from sinusoid_extractor.services.windower import Windower
from sinusoid_extractor.shared.persistence import save_npz

_log = logging.getLogger(__name__)


class DatasetService:
    """Orchestrates the dataset pipeline.

    Building Block (RULES.md §16):
        Input  : alpha (float in [0, 1]), seed (int)
        Output : (raw_signals: dict[str, ndarray] of 9 arrays, DataBundle)
        Setup  : DatasetConfig dict (frequencies_hz, amplitude, sampling_rate_hz,
                 duration_seconds, context_window, n_train, n_val, n_test)
    """

    def __init__(self, dataset_cfg: dict[str, Any]) -> None:
        self.cfg = dataset_cfg
        self.frequencies_hz: tuple[int, ...] = tuple(
            dataset_cfg.get("frequencies_hz", FIXED_FREQUENCIES_HZ)
        )
        self.window_size = int(dataset_cfg.get("context_window", CONTEXT_WINDOW))

    def build_raw_signals(self, alpha: float, seed: int) -> dict[str, np.ndarray]:
        """Generate the 4 pure + 4 noisy + 1 combined arrays."""
        rng = np.random.default_rng(seed)
        gen = SignalGenerator(
            amplitude=float(self.cfg.get("amplitude", 1.0)),
            sampling_rate_hz=int(self.cfg.get("sampling_rate_hz", 1000)),
            duration_seconds=float(self.cfg.get("duration_seconds", 10.0)),
        )
        noise = NoiseModel(rng)
        out: dict[str, np.ndarray] = {}
        noisy_stack: list[np.ndarray] = []
        for f in self.frequencies_hz:
            phase = noise.random_phase()
            pure = gen.pure(f, phase=0.0)
            noisy = noise.apply_amplitude_noise(gen.pure(f, phase=phase), alpha)
            out[f"pure_{f}hz"] = pure
            out[f"noisy_{f}hz"] = noisy
            noisy_stack.append(noisy)
        out["combined_sigma"] = np.sum(np.stack(noisy_stack, axis=0), axis=0).astype(np.float32)
        return out

    def build_tuples(
        self, raw: dict[str, np.ndarray], n_train: int, n_val: int, n_test: int, seed: int
    ) -> DataBundle:
        """Sample disjoint windows and assemble (C, x, y) splits."""
        rng = np.random.default_rng(seed + 1)
        windower = Windower(self.window_size, rng)
        splitter = Splitter(rng, frequencies_hz=self.frequencies_hz)
        n_total = int(raw["combined_sigma"].shape[0])
        train_s, val_s, test_s = windower.disjoint_starts(n_total, n_train, n_val, n_test)
        pure_by_freq = {f: raw[f"pure_{f}hz"] for f in self.frequencies_hz}
        combined = raw["combined_sigma"]
        return DataBundle(
            train=self._make_split(splitter, combined, pure_by_freq, train_s),
            val=self._make_split(splitter, combined, pure_by_freq, val_s),
            test=self._make_split(splitter, combined, pure_by_freq, test_s),
            alpha=float(self.cfg.get("_alpha_for_seed", 0.0)),
            seed=int(seed),
        )

    def _make_split(
        self,
        splitter: Splitter,
        combined: np.ndarray,
        pure_by_freq: dict[int, np.ndarray],
        starts: np.ndarray,
    ) -> Split:
        oh = splitter.assign_one_hot(starts.shape[0])
        c, x, y = splitter.build_tuples(combined, pure_by_freq, starts, oh, self.window_size)
        return Split(C=c, x=x, y=y)

    def generate(self, alpha: float, seed: int) -> tuple[dict[str, np.ndarray], DataBundle]:
        """End-to-end: raw signals + (train/val/test) tuples for ``alpha``/``seed``."""
        self.cfg["_alpha_for_seed"] = alpha
        raw = self.build_raw_signals(alpha=alpha, seed=seed)
        bundle = self.build_tuples(
            raw,
            n_train=int(self.cfg.get("n_train", 5000)),
            n_val=int(self.cfg.get("n_val", 1000)),
            n_test=int(self.cfg.get("n_test", 1000)),
            seed=seed,
        )
        _log.info(
            "generated dataset alpha=%.3f seed=%d sizes=%s", alpha, seed, bundle.summary()
        )
        return raw, bundle

    @staticmethod
    def persist(raw: dict[str, np.ndarray], path: Path | str, **metadata: Any) -> Path:
        """Save raw arrays + scalar metadata to a single npz."""
        meta = {f"meta_{k}": np.array(v) for k, v in metadata.items()}
        return save_npz(path, **raw, **meta)
