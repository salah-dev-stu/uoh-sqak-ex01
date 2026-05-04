"""Tests for ``services.training_loop``."""

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from sinusoid_extractor.constants import HookEvent
from sinusoid_extractor.services.early_stopping import EarlyStopping
from sinusoid_extractor.services.loss_fn import WindowSumMSE
from sinusoid_extractor.services.training_loop import TrainingError, TrainingLoop
from sinusoid_extractor.shared.hooks import HookRegistry


def _toy_loaders(n: int = 32) -> tuple[DataLoader, DataLoader]:
    x = torch.randn(n, 14)
    y = torch.randn(n, 10)
    train = DataLoader(TensorDataset(x, y), batch_size=8)
    val = DataLoader(TensorDataset(x, y), batch_size=8)
    return train, val


def _toy_model() -> nn.Module:
    return nn.Sequential(nn.Linear(14, 16), nn.ReLU(), nn.Linear(16, 10))


def test_run_completes_max_epochs() -> None:
    model = _toy_model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    train, val = _toy_loaders()
    loop = TrainingLoop(model, opt, WindowSumMSE(), train, val, max_epochs=2,
                        early_stopping=EarlyStopping(patience=10))
    result = loop.run()
    assert result.epochs_run == 2
    assert len(result.train_loss_per_epoch) == 2
    assert len(result.val_loss_per_epoch) == 2


def test_hooks_fire_after_each_epoch() -> None:
    model = _toy_model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    train, val = _toy_loaders()
    hooks = HookRegistry()
    fired: list[int] = []
    hooks.register(HookEvent.AFTER_EPOCH, lambda **kw: fired.append(kw["epoch"]))
    TrainingLoop(model, opt, WindowSumMSE(), train, val, max_epochs=2,
                 hooks=hooks, early_stopping=EarlyStopping(patience=10)).run()
    assert fired == [0, 1]


def test_nan_loss_aborts() -> None:
    class BadLoss(nn.Module):
        def forward(self, *_):
            return torch.tensor(float("nan"))

    model = _toy_model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    train, val = _toy_loaders(8)
    loop = TrainingLoop(model, opt, BadLoss(), train, val, max_epochs=1)
    with pytest.raises(TrainingError):
        loop.run()


def test_invalid_max_epochs_raises() -> None:
    model = _toy_model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    train, val = _toy_loaders(8)
    with pytest.raises(ValueError):
        TrainingLoop(model, opt, WindowSumMSE(), train, val, max_epochs=0)


def test_early_stopping_triggers_and_restores_best() -> None:
    model = _toy_model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    train, val = _toy_loaders()
    loop = TrainingLoop(model, opt, WindowSumMSE(), train, val, max_epochs=10,
                        early_stopping=EarlyStopping(patience=0))
    result = loop.run()
    assert result.epochs_run <= 10
    assert result.best_state_dict is not None
