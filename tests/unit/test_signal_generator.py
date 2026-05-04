"""Tests for ``services.signal_generator``."""

import math

import numpy as np
import pytest

from sinusoid_extractor.services.signal_generator import SignalGenerator


def test_pure_shape() -> None:
    gen = SignalGenerator(amplitude=1.0, sampling_rate_hz=1000, duration_seconds=0.5)
    sig = gen.pure(3.0)
    assert sig.shape == (500,)


def test_pure_amplitude_peak() -> None:
    gen = SignalGenerator(amplitude=2.0, sampling_rate_hz=1000, duration_seconds=1.0)
    sig = gen.pure(1.0)
    assert math.isclose(float(np.max(np.abs(sig))), 2.0, abs_tol=1e-3)


def test_pure_zero_mean_over_integer_cycles() -> None:
    gen = SignalGenerator(amplitude=1.0, sampling_rate_hz=1000, duration_seconds=1.0)
    sig = gen.pure(5.0)  # 5 full cycles
    assert abs(float(np.mean(sig))) < 1e-3


def test_pure_all_returns_one_per_freq() -> None:
    gen = SignalGenerator()
    out = gen.pure_all((1, 3, 5, 7))
    assert set(out.keys()) == {1, 3, 5, 7}


def test_invalid_amplitude_raises() -> None:
    with pytest.raises(ValueError):
        SignalGenerator(amplitude=0.0)


def test_invalid_fs_raises() -> None:
    with pytest.raises(ValueError):
        SignalGenerator(sampling_rate_hz=0)


def test_invalid_duration_raises() -> None:
    with pytest.raises(ValueError):
        SignalGenerator(duration_seconds=-1.0)


def test_non_finite_freq_raises() -> None:
    gen = SignalGenerator()
    with pytest.raises(ValueError):
        gen.pure(float("nan"))


def test_phase_offset_shifts_first_sample() -> None:
    gen = SignalGenerator(amplitude=1.0, sampling_rate_hz=1000, duration_seconds=1.0)
    s0 = gen.pure(1.0, phase=0.0)
    s_pi2 = gen.pure(1.0, phase=math.pi / 2)
    assert abs(s0[0]) < 1e-3
    assert abs(s_pi2[0] - 1.0) < 1e-3


def test_time_axis() -> None:
    gen = SignalGenerator(sampling_rate_hz=100, duration_seconds=1.0)
    t = gen.time_axis()
    assert t.shape == (100,)
    assert t[0] == 0.0
    assert math.isclose(float(t[-1]), 0.99, abs_tol=1e-6)
