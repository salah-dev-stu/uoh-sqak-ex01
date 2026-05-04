"""Random-start window extraction over 1-D signals (per PRD_dataset)."""

from __future__ import annotations

import numpy as np


class Windower:
    """Pulls fixed-length windows from a 1-D signal at random start offsets."""

    def __init__(self, window_size: int, rng: np.random.Generator) -> None:
        if window_size < 1:
            raise ValueError(f"window_size must be >= 1, got {window_size}")
        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be a numpy.random.Generator")
        self.window_size = int(window_size)
        self._rng = rng

    def random_starts(self, n_total: int, n_windows: int) -> np.ndarray:
        """Draw ``n_windows`` start indices uniformly within valid range."""
        max_start = n_total - self.window_size
        if max_start < 0:
            raise ValueError(
                f"window_size {self.window_size} > n_total {n_total}"
            )
        if n_windows == 0:
            return np.empty(0, dtype=np.int64)
        return self._rng.integers(0, max_start + 1, size=n_windows, dtype=np.int64)

    def disjoint_starts(
        self,
        n_total: int,
        n_train: int,
        n_val: int,
        n_test: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return ``(train, val, test)`` start arrays drawn without replacement."""
        max_start = n_total - self.window_size
        total = n_train + n_val + n_test
        if total > max_start + 1:
            raise ValueError(
                f"requested {total} windows but only {max_start + 1} starts available"
            )
        all_starts = self._rng.choice(max_start + 1, size=total, replace=False)
        return (
            np.sort(all_starts[:n_train]),
            np.sort(all_starts[n_train : n_train + n_val]),
            np.sort(all_starts[n_train + n_val :]),
        )

    def extract(self, signal: np.ndarray, starts: np.ndarray) -> np.ndarray:
        """Return ``(len(starts), window_size)`` slice array."""
        if signal.ndim != 1:
            raise ValueError(f"signal must be 1-D, got shape {signal.shape}")
        if starts.size == 0:
            return np.empty((0, self.window_size), dtype=signal.dtype)
        idx = starts[:, None] + np.arange(self.window_size, dtype=np.int64)[None, :]
        return signal[idx]
