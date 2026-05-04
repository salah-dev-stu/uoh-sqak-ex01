"""Tests for ``models.fc_model``."""

from pathlib import Path

import pytest
import torch

from sinusoid_extractor.constants import INPUT_DIM_FC, OUTPUT_DIM
from sinusoid_extractor.models.fc_model import FCExtractor


def test_forward_shape() -> None:
    m = FCExtractor(hidden_size=8, num_layers=2)
    out = m(torch.randn(4, INPUT_DIM_FC))
    assert out.shape == (4, OUTPUT_DIM)


def test_param_count_2_layers_h128() -> None:
    m = FCExtractor(hidden_size=128, num_layers=2, dropout=0.0)
    # (14*128+128) + (128*128+128) + (128*10+10) = 1920 + 16512 + 1290
    assert m.count_parameters() == 19722


def test_invalid_hidden_size_raises() -> None:
    with pytest.raises(ValueError):
        FCExtractor(hidden_size=0)


def test_invalid_num_layers_raises() -> None:
    with pytest.raises(ValueError):
        FCExtractor(num_layers=4)


def test_invalid_dropout_raises() -> None:
    with pytest.raises(ValueError):
        FCExtractor(dropout=1.5)


def test_save_load_round_trip(tmp_path: Path) -> None:
    a = FCExtractor(hidden_size=8, num_layers=1, dropout=0.0)
    b = FCExtractor(hidden_size=8, num_layers=1, dropout=0.0)
    a.save(tmp_path / "w.pt")
    b.load(tmp_path / "w.pt")
    x = torch.randn(2, INPUT_DIM_FC)
    assert torch.allclose(a(x), b(x))


def test_architecture_name() -> None:
    assert FCExtractor().architecture_name() == "fc"


def test_gradient_flows() -> None:
    m = FCExtractor(hidden_size=8, num_layers=1, dropout=0.0)
    x = torch.randn(3, INPUT_DIM_FC)
    y = torch.randn(3, OUTPUT_DIM)
    loss = ((m(x) - y) ** 2).sum()
    loss.backward()
    assert all(p.grad is not None for p in m.parameters())
