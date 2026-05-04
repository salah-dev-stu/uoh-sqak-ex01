"""Tests for ``models.rnn_model``."""

import pytest
import torch

from sinusoid_extractor.constants import (
    CONTEXT_WINDOW,
    INPUT_DIM_RECURRENT_PER_STEP,
    OUTPUT_DIM,
)
from sinusoid_extractor.models.rnn_model import RNNExtractor


def test_forward_shape() -> None:
    m = RNNExtractor(hidden_size=8, num_layers=1, dropout=0.0)
    out = m(torch.randn(4, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP))
    assert out.shape == (4, OUTPUT_DIM)


def test_tanh_nonlinearity_in_use() -> None:
    m = RNNExtractor(hidden_size=8)
    assert m.rnn.nonlinearity == "tanh"


def test_invalid_layers_raises() -> None:
    with pytest.raises(ValueError):
        RNNExtractor(num_layers=0)


def test_invalid_hidden_raises() -> None:
    with pytest.raises(ValueError):
        RNNExtractor(hidden_size=-1)


def test_invalid_dropout_raises() -> None:
    with pytest.raises(ValueError):
        RNNExtractor(dropout=2.0)


def test_two_layer_with_dropout_constructs() -> None:
    m = RNNExtractor(hidden_size=8, num_layers=2, dropout=0.3)
    out = m(torch.randn(2, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP))
    assert out.shape == (2, OUTPUT_DIM)


def test_architecture_name() -> None:
    assert RNNExtractor().architecture_name() == "rnn"


def test_gradient_flows() -> None:
    m = RNNExtractor(hidden_size=4, num_layers=1, dropout=0.0)
    x = torch.randn(2, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP)
    y = torch.randn(2, OUTPUT_DIM)
    ((m(x) - y) ** 2).sum().backward()
    assert all(p.grad is not None for p in m.parameters())
