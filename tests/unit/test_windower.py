"""Tests for ``services.windower``."""

import numpy as np
import pytest

from sinusoid_extractor.services.windower import Windower


def test_random_starts_in_range(rng) -> None:
    w = Windower(window_size=10, rng=rng)
    starts = w.random_starts(n_total=100, n_windows=50)
    assert starts.shape == (50,)
    assert (starts >= 0).all() and (starts <= 90).all()


def test_disjoint_starts_no_overlap(rng) -> None:
    w = Windower(window_size=5, rng=rng)
    a, b, c = w.disjoint_starts(n_total=100, n_train=10, n_val=5, n_test=5)
    assert len(set(a.tolist()) | set(b.tolist()) | set(c.tolist())) == 20


def test_disjoint_starts_too_many_raises(rng) -> None:
    w = Windower(window_size=10, rng=rng)
    with pytest.raises(ValueError):
        w.disjoint_starts(n_total=20, n_train=5, n_val=5, n_test=5)


def test_window_too_large_raises(rng) -> None:
    w = Windower(window_size=200, rng=rng)
    with pytest.raises(ValueError):
        w.random_starts(n_total=100, n_windows=1)


def test_extract_shape(rng) -> None:
    w = Windower(window_size=5, rng=rng)
    sig = np.arange(100, dtype=np.float32)
    starts = np.array([0, 10, 95], dtype=np.int64)
    out = w.extract(sig, starts)
    assert out.shape == (3, 5)
    assert (out[0] == np.arange(5)).all()
    assert (out[1] == np.arange(10, 15)).all()


def test_extract_empty_starts(rng) -> None:
    w = Windower(window_size=5, rng=rng)
    out = w.extract(np.arange(10, dtype=np.float32), np.empty(0, dtype=np.int64))
    assert out.shape == (0, 5)


def test_extract_2d_signal_raises(rng) -> None:
    w = Windower(window_size=5, rng=rng)
    with pytest.raises(ValueError):
        w.extract(np.zeros((2, 10), dtype=np.float32), np.array([0]))


def test_invalid_window_size_raises(rng) -> None:
    with pytest.raises(ValueError):
        Windower(window_size=0, rng=rng)


def test_invalid_rng_raises() -> None:
    with pytest.raises(TypeError):
        Windower(window_size=10, rng="not-a-generator")  # type: ignore[arg-type]


def test_random_starts_zero_windows(rng) -> None:
    w = Windower(window_size=10, rng=rng)
    assert w.random_starts(n_total=100, n_windows=0).shape == (0,)
