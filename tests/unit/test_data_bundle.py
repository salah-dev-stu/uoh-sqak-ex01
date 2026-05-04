"""Tests for ``services.data_bundle``."""

import numpy as np

from sinusoid_extractor.services.data_bundle import DataBundle, Split


def _split(n: int) -> Split:
    return Split(
        C=np.zeros((n, 4), dtype=np.float32),
        x=np.zeros((n, 10), dtype=np.float32),
        y=np.zeros((n, 10), dtype=np.float32),
    )


def test_split_len() -> None:
    assert len(_split(7)) == 7


def test_bundle_summary() -> None:
    b = DataBundle(train=_split(10), val=_split(5), test=_split(3), alpha=0.1, seed=42)
    s = b.summary()
    assert s == {"n_train": 10, "n_val": 5, "n_test": 3, "alpha": 0.1, "seed": 42}
