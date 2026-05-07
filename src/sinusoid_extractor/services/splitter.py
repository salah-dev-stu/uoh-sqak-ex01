"""Build (C, x, y) training tuples from raw signals + window starts."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from sinusoid_extractor.constants import FIXED_FREQUENCIES_HZ, ONE_HOT_DIM


class Splitter:
    """Assigns one-hot selectors and emits matching tuples.

    Building Block (RULES.md §16):
        Input  : combined (1-D ndarray), pure_by_freq (dict[int, ndarray]),
                 starts (int64 ndarray), one_hot (n,4 float32), window_size (int)
        Output : (C, x, y) tuple of float32 arrays
                 shapes (n, 4), (n, window_size), (n, window_size)
        Setup  : rng (numpy.random.Generator),
                 frequencies_hz (4-tuple, default = FIXED_FREQUENCIES_HZ)
    """

    def __init__(
        self,
        rng: np.random.Generator,
        frequencies_hz: Sequence[int] = FIXED_FREQUENCIES_HZ,
    ) -> None:
        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be a numpy.random.Generator")
        if len(tuple(frequencies_hz)) != ONE_HOT_DIM:
            raise ValueError(
                f"frequencies_hz must have length {ONE_HOT_DIM}, got {len(tuple(frequencies_hz))}"
            )
        self._rng = rng
        self._frequencies_hz: tuple[int, ...] = tuple(int(f) for f in frequencies_hz)

    def assign_one_hot(self, n_examples: int, n_classes: int = ONE_HOT_DIM) -> np.ndarray:
        """Return ``(n, n_classes)`` one-hot matrix with class ids drawn uniformly."""
        if n_examples < 0:
            raise ValueError(f"n_examples must be >= 0, got {n_examples}")
        if n_examples == 0:
            return np.empty((0, n_classes), dtype=np.float32)
        ids = self._rng.integers(0, n_classes, size=n_examples, dtype=np.int64)
        oh = np.zeros((n_examples, n_classes), dtype=np.float32)
        oh[np.arange(n_examples), ids] = 1.0
        return oh

    def build_tuples(
        self,
        combined: np.ndarray,
        pure_by_freq: dict[int, np.ndarray],
        starts: np.ndarray,
        one_hot: np.ndarray,
        window_size: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return ``(C, x, y)`` arrays of shapes ``(n,4) (n,W) (n,W)``."""
        n = starts.shape[0]
        if one_hot.shape[0] != n:
            raise ValueError(
                f"starts and one_hot length mismatch: {n} vs {one_hot.shape[0]}"
            )
        if n == 0:
            empty = np.empty((0, window_size), dtype=np.float32)
            return one_hot, empty, empty

        x = self._extract_windows(combined, starts, window_size)
        y = np.empty_like(x)
        class_ids = np.argmax(one_hot, axis=1)
        for i, class_id in enumerate(class_ids):
            freq = self._frequencies_hz[int(class_id)]
            pure = pure_by_freq[int(freq)]
            y[i] = pure[starts[i] : starts[i] + window_size]
        return one_hot.astype(np.float32), x.astype(np.float32), y.astype(np.float32)

    @staticmethod
    def _extract_windows(signal: np.ndarray, starts: np.ndarray, w: int) -> np.ndarray:
        idx = starts[:, None] + np.arange(w, dtype=np.int64)[None, :]
        return signal[idx]
