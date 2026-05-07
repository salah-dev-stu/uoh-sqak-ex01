"""Tests for ``services.splitter``."""

import numpy as np
import pytest

from sinusoid_extractor.services.splitter import Splitter


def test_assign_one_hot_shape_and_sum(rng) -> None:
    s = Splitter(rng)
    oh = s.assign_one_hot(20)
    assert oh.shape == (20, 4)
    assert (oh.sum(axis=1) == 1.0).all()


def test_assign_one_hot_zero_examples(rng) -> None:
    assert Splitter(rng).assign_one_hot(0).shape == (0, 4)


def test_assign_one_hot_negative_raises(rng) -> None:
    with pytest.raises(ValueError):
        Splitter(rng).assign_one_hot(-1)


def test_build_tuples_shapes(rng) -> None:
    s = Splitter(rng, frequencies_hz=(1, 3, 5, 7))
    combined = np.arange(100, dtype=np.float32)
    pure = {1: combined.copy(), 3: combined * 2, 5: combined * 3, 7: combined * 4}
    starts = np.array([0, 10, 50], dtype=np.int64)
    oh = s.assign_one_hot(3)
    c, x, y = s.build_tuples(combined, pure, starts, oh, window_size=5)
    assert c.shape == (3, 4)
    assert x.shape == (3, 5)
    assert y.shape == (3, 5)


def test_build_tuples_y_matches_pure_for_class(rng) -> None:
    s = Splitter(rng, frequencies_hz=(1, 3, 5, 7))
    combined = np.arange(20, dtype=np.float32)
    pure = {1: combined + 10, 3: combined + 20, 5: combined + 30, 7: combined + 40}
    starts = np.array([0], dtype=np.int64)
    oh = np.array([[0, 0, 1, 0]], dtype=np.float32)  # class index 2 → freq 5 Hz
    _, _, y = s.build_tuples(combined, pure, starts, oh, window_size=3)
    assert (y[0] == np.array([30, 31, 32], dtype=np.float32)).all()


def test_invalid_frequencies_length_raises(rng) -> None:
    with pytest.raises(ValueError):
        Splitter(rng, frequencies_hz=(1, 3, 5))


def test_default_frequencies_match_constant(rng) -> None:
    from sinusoid_extractor.constants import FIXED_FREQUENCIES_HZ
    s = Splitter(rng)
    # Internal attribute is private but we verify the contract via behaviour:
    pure = {f: np.arange(20, dtype=np.float32) for f in FIXED_FREQUENCIES_HZ}
    oh = np.eye(4, dtype=np.float32)[[0]]
    _, _, y = s.build_tuples(np.zeros(20, dtype=np.float32), pure,
                             np.array([0]), oh, window_size=3)
    assert y.shape == (1, 3)


def test_build_tuples_empty(rng) -> None:
    s = Splitter(rng)
    starts = np.empty(0, dtype=np.int64)
    oh = np.empty((0, 4), dtype=np.float32)
    c, x, y = s.build_tuples(np.zeros(10, dtype=np.float32), {1: np.zeros(10, dtype=np.float32)}, starts, oh, 5)
    assert c.shape == (0, 4) and x.shape == (0, 5) and y.shape == (0, 5)


def test_invalid_rng_raises() -> None:
    with pytest.raises(TypeError):
        Splitter(rng="bad")  # type: ignore[arg-type]


def test_one_hot_starts_length_mismatch(rng) -> None:
    s = Splitter(rng)
    pure = {1: np.zeros(10, dtype=np.float32), 3: np.zeros(10, dtype=np.float32),
            5: np.zeros(10, dtype=np.float32), 7: np.zeros(10, dtype=np.float32)}
    with pytest.raises(ValueError):
        s.build_tuples(np.zeros(10, dtype=np.float32), pure,
                       starts=np.array([0, 1]), one_hot=np.zeros((1, 4)), window_size=3)
