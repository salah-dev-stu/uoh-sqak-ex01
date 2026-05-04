"""Tests for ``services.noise_model``."""

import math

import numpy as np
import pytest

from sinusoid_extractor.constants import NoiseDistribution
from sinusoid_extractor.services.noise_model import NoiseModel


def test_random_phase_in_range(rng) -> None:
    n = NoiseModel(rng)
    phases = [n.random_phase() for _ in range(2000)]
    assert all(0.0 <= p < 2.0 * math.pi for p in phases)
    assert max(phases) > 5.0
    assert min(phases) < 1.0


def test_apply_amplitude_noise_alpha_zero_is_identity(rng) -> None:
    pure = np.ones(50, dtype=np.float32)
    out = NoiseModel(rng).apply_amplitude_noise(pure, alpha=0.0)
    assert np.allclose(out, pure)


def test_apply_amplitude_noise_uniform_is_bounded(rng) -> None:
    pure = np.ones(2000, dtype=np.float32)
    out = NoiseModel(rng).apply_amplitude_noise(pure, alpha=0.10, distribution=NoiseDistribution.UNIFORM)
    assert np.all(out >= 0.9 - 1e-5)
    assert np.all(out <= 1.1 + 1e-5)


def test_apply_amplitude_noise_gaussian(rng) -> None:
    pure = np.ones(2000, dtype=np.float32)
    out = NoiseModel(rng).apply_amplitude_noise(pure, alpha=0.10, distribution=NoiseDistribution.GAUSSIAN)
    assert out.shape == pure.shape
    assert abs(float(np.mean(out)) - 1.0) < 0.05


def test_invalid_alpha_raises(rng) -> None:
    with pytest.raises(ValueError):
        NoiseModel(rng).apply_amplitude_noise(np.zeros(3), alpha=-0.1)


def test_invalid_rng_raises() -> None:
    with pytest.raises(TypeError):
        NoiseModel(rng="not-a-rng")  # type: ignore[arg-type]


def test_alpha_above_one_warns_but_returns(rng, caplog) -> None:
    out = NoiseModel(rng).apply_amplitude_noise(np.ones(10), alpha=1.5)
    assert out.shape == (10,)
