"""Tests for ``models.lstm_model``."""

import pytest
import torch

from sinusoid_extractor.constants import (
    CONTEXT_WINDOW,
    INPUT_DIM_RECURRENT_PER_STEP,
    OUTPUT_DIM,
)
from sinusoid_extractor.models.lstm_model import LSTMExtractor
from sinusoid_extractor.models.rnn_model import RNNExtractor


def test_forward_shape() -> None:
    m = LSTMExtractor(hidden_size=8, num_layers=1, dropout=0.0)
    out = m(torch.randn(3, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP))
    assert out.shape == (3, OUTPUT_DIM)


def test_invalid_layers_raises() -> None:
    with pytest.raises(ValueError):
        LSTMExtractor(num_layers=4)


def test_invalid_hidden_raises() -> None:
    with pytest.raises(ValueError):
        LSTMExtractor(hidden_size=0)


def test_invalid_dropout_raises() -> None:
    with pytest.raises(ValueError):
        LSTMExtractor(dropout=1.0)


def test_two_layer_with_dropout_constructs() -> None:
    m = LSTMExtractor(hidden_size=8, num_layers=2, dropout=0.4)
    out = m(torch.randn(2, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP))
    assert out.shape == (2, OUTPUT_DIM)


def test_lstm_has_more_params_than_rnn_at_same_hidden() -> None:
    rnn = RNNExtractor(hidden_size=64, num_layers=1, dropout=0.0)
    lstm = LSTMExtractor(hidden_size=64, num_layers=1, dropout=0.0)
    assert lstm.count_parameters() > rnn.count_parameters() * 3


def test_architecture_name() -> None:
    assert LSTMExtractor().architecture_name() == "lstm"


def test_gradient_flows() -> None:
    m = LSTMExtractor(hidden_size=4, num_layers=1, dropout=0.0)
    x = torch.randn(2, CONTEXT_WINDOW, INPUT_DIM_RECURRENT_PER_STEP)
    y = torch.randn(2, OUTPUT_DIM)
    ((m(x) - y) ** 2).sum().backward()
    assert all(p.grad is not None for p in m.parameters())
