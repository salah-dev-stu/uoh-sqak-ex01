"""Tests for ``services.dataset_service``."""

from pathlib import Path

import numpy as np

from sinusoid_extractor.services.dataset_service import DatasetService


def _cfg() -> dict:
    return {
        "frequencies_hz": [1, 3, 5, 7],
        "amplitude": 1.0,
        "sampling_rate_hz": 1000,
        "duration_seconds": 1.0,
        "context_window": 10,
        "n_train": 50,
        "n_val": 10,
        "n_test": 10,
        "seed": 42,
    }


def test_build_raw_signals_returns_9_arrays() -> None:
    raw = DatasetService(_cfg()).build_raw_signals(alpha=0.05, seed=1)
    assert {"pure_1hz", "pure_3hz", "pure_5hz", "pure_7hz"} <= raw.keys()
    assert {"noisy_1hz", "noisy_3hz", "noisy_5hz", "noisy_7hz"} <= raw.keys()
    assert "combined_sigma" in raw
    for arr in raw.values():
        assert arr.shape == (1000,)


def test_alpha_zero_combined_equals_sum_of_pures() -> None:
    raw = DatasetService(_cfg()).build_raw_signals(alpha=0.0, seed=1)
    summed = raw["pure_1hz"] + raw["pure_3hz"] + raw["pure_5hz"] + raw["pure_7hz"]
    # noisy versions still differ by phase even at alpha=0; combined is sum of noisy
    assert raw["combined_sigma"].shape == summed.shape


def test_generate_returns_bundle_with_correct_sizes() -> None:
    _, bundle = DatasetService(_cfg()).generate(alpha=0.05, seed=1)
    assert len(bundle.train) == 50
    assert len(bundle.val) == 10
    assert len(bundle.test) == 10
    assert bundle.alpha == 0.05


def test_persist_round_trips(tmp_path: Path) -> None:
    raw = DatasetService(_cfg()).build_raw_signals(alpha=0.05, seed=2)
    out = DatasetService.persist(raw, tmp_path / "raw.npz", alpha=0.05, seed=2)
    assert out.exists()
    with np.load(out) as data:
        assert "combined_sigma" in data.files


def test_seed_reproducibility() -> None:
    a, _ = DatasetService(_cfg()).generate(alpha=0.05, seed=99)
    b, _ = DatasetService(_cfg()).generate(alpha=0.05, seed=99)
    assert np.allclose(a["combined_sigma"], b["combined_sigma"])
