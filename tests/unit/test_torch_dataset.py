"""Tests for ``services.torch_dataset``."""

import numpy as np
import torch

from sinusoid_extractor.constants import (
    CONTEXT_WINDOW,
    INPUT_DIM_FC,
    INPUT_DIM_RECURRENT_PER_STEP,
    Architecture,
)
from sinusoid_extractor.services.data_bundle import Split
from sinusoid_extractor.services.torch_dataset import SinusoidWindowDataset


def _split(n: int) -> Split:
    rng = np.random.default_rng(0)
    return Split(
        C=rng.random((n, 4)).astype(np.float32),
        x=rng.random((n, 10)).astype(np.float32),
        y=rng.random((n, 10)).astype(np.float32),
    )


def test_len() -> None:
    ds = SinusoidWindowDataset(_split(7), Architecture.FC)
    assert len(ds) == 7


def test_fc_view_returns_flat_14() -> None:
    ds = SinusoidWindowDataset(_split(3), Architecture.FC)
    inp, _ = ds[0]
    assert inp.shape == (INPUT_DIM_FC,)


def test_rnn_view_returns_seq() -> None:
    ds = SinusoidWindowDataset(_split(3), Architecture.RNN)
    inp, _ = ds[0]
    assert inp.shape == (CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP)


def test_lstm_view_same_as_rnn() -> None:
    ds = SinusoidWindowDataset(_split(2), Architecture.LSTM)
    inp, _ = ds[0]
    assert inp.shape == (CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP)


def test_target_shape_and_dtype() -> None:
    ds = SinusoidWindowDataset(_split(2), "fc")
    _, tgt = ds[0]
    assert tgt.shape == (10,)
    assert tgt.dtype == torch.float32
