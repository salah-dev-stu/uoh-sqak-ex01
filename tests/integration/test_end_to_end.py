"""End-to-end SDK integration tests at tiny scale (≤90 s on CPU)."""

from __future__ import annotations

import pytest

from sinusoid_extractor.constants import Architecture
from sinusoid_extractor.sdk.sdk import SinusoidExtractorSDK


@pytest.fixture
def sdk(tiny_config_path, rate_limits_path, monkeypatch, tmp_path) -> SinusoidExtractorSDK:
    from sinusoid_extractor.shared import gatekeeper as gk

    monkeypatch.setattr(gk, "DEFAULT_RATE_LIMITS_PATH", rate_limits_path)
    return SinusoidExtractorSDK(config_path=tiny_config_path, results_dir=tmp_path / "results")


def test_health_check(sdk: SinusoidExtractorSDK) -> None:
    from sinusoid_extractor.shared.version import __version__
    h = sdk.health_check()
    assert h["version"] == __version__
    assert {"fc", "rnn", "lstm"} <= set(h["registered_architectures"])


def test_generate_dataset(sdk: SinusoidExtractorSDK) -> None:
    bundle = sdk.generate_dataset(alpha=0.05, seed=42)
    assert len(bundle.train) > 0
    assert len(bundle.val) > 0
    assert len(bundle.test) > 0


@pytest.mark.parametrize("arch", [Architecture.FC.value, Architecture.RNN.value, Architecture.LSTM.value])
def test_train_evaluate_per_arch(sdk: SinusoidExtractorSDK, arch: str) -> None:
    bundle = sdk.generate_dataset(alpha=0.05, seed=42)
    handle = sdk.train_model(arch, bundle, seed=42)
    report = sdk.evaluate(handle, bundle)
    assert handle.run_id
    assert report.test_mse > 0
    assert report.n_test == len(bundle.test)
    assert report.baseline_mse > 0


def test_run_oat_sweep_smoke(sdk: SinusoidExtractorSDK) -> None:
    handles = sdk.run_oat_sweep(limit=2)
    assert len(handles) <= 2
