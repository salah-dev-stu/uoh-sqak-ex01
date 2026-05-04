"""Tests for ``services.optimizer_factory``."""

import pytest
import torch

from sinusoid_extractor.constants import Optimizer
from sinusoid_extractor.services.optimizer_factory import build_optimizer


def _params() -> list[torch.Tensor]:
    return [torch.randn(2, 2, requires_grad=True)]


def test_adam() -> None:
    opt = build_optimizer("adam", _params(), learning_rate=0.001)
    assert isinstance(opt, torch.optim.Adam)


def test_rmsprop() -> None:
    opt = build_optimizer(Optimizer.RMSPROP, _params(), learning_rate=0.001)
    assert isinstance(opt, torch.optim.RMSprop)


def test_invalid_name_raises() -> None:
    with pytest.raises(ValueError):
        build_optimizer("sgd", _params(), learning_rate=0.001)


def test_invalid_lr_raises() -> None:
    with pytest.raises(ValueError):
        build_optimizer("adam", _params(), learning_rate=-1.0)


def test_lr_applied() -> None:
    opt = build_optimizer("adam", _params(), learning_rate=0.005)
    for g in opt.param_groups:
        assert g["lr"] == 0.005
