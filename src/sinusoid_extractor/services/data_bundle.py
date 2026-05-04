"""DataBundle dataclass: a single (train, val, test) triple of (C, x, y)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Split:
    """A single dataset split: aligned (C, x, y) arrays."""

    C: np.ndarray
    x: np.ndarray
    y: np.ndarray

    def __len__(self) -> int:
        return int(self.C.shape[0])


@dataclass(frozen=True)
class DataBundle:
    """The three splits + the alpha / seed used to build them."""

    train: Split
    val: Split
    test: Split
    alpha: float
    seed: int

    def summary(self) -> dict[str, int | float]:
        """A small dict useful for logging the bundle's identity."""
        return {
            "n_train": len(self.train),
            "n_val": len(self.val),
            "n_test": len(self.test),
            "alpha": float(self.alpha),
            "seed": int(self.seed),
        }
