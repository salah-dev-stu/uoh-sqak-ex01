"""Tests for ``services.loss_fn``."""

import pytest
import torch

from sinusoid_extractor.services.loss_fn import WindowSumMSE


def test_zero_loss_for_identical() -> None:
    loss = WindowSumMSE()
    pred = torch.zeros(2, 10)
    assert float(loss(pred, pred.clone())) == 0.0


def test_quadratic_in_error() -> None:
    loss = WindowSumMSE()
    pred = torch.zeros(1, 10)
    target = torch.ones(1, 10)
    base = float(loss(pred, target))
    bigger = float(loss(pred, target * 2))
    assert pytest.approx(bigger / base, rel=1e-5) == 4.0


def test_shape_mismatch_raises() -> None:
    loss = WindowSumMSE()
    with pytest.raises(ValueError):
        loss(torch.zeros(2, 10), torch.zeros(2, 5))


def test_sum_over_window_axis() -> None:
    loss = WindowSumMSE()
    pred = torch.zeros(1, 10)
    target = torch.full((1, 10), 1.0)
    # 10 squared errors of 1 each summed = 10, mean over batch=1 → 10
    assert float(loss(pred, target)) == 10.0


def test_differentiable() -> None:
    loss = WindowSumMSE()
    pred = torch.zeros(1, 10, requires_grad=True)
    target = torch.ones(1, 10)
    loss(pred, target).backward()
    assert pred.grad is not None
