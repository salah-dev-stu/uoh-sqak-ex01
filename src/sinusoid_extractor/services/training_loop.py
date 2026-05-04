"""Training loop with hooks, early stopping, NaN guard, gradient clipping."""

from __future__ import annotations

import logging
import math
import time
from copy import deepcopy
from dataclasses import dataclass, field

import torch
from torch import nn
from torch.utils.data import DataLoader

from sinusoid_extractor.constants import HookEvent
from sinusoid_extractor.services.early_stopping import EarlyStopping
from sinusoid_extractor.shared.hooks import HookRegistry

_log = logging.getLogger(__name__)
GRAD_CLIP_NORM = 1.0


class TrainingError(RuntimeError):
    """Raised on NaN loss or other irrecoverable training failures."""


@dataclass
class TrainingResult:
    """All artifacts a TrainingLoop produces."""

    train_loss_per_epoch: list[float] = field(default_factory=list)
    val_loss_per_epoch: list[float] = field(default_factory=list)
    epochs_run: int = 0
    wall_clock_seconds: float = 0.0
    best_val_loss: float = math.inf
    best_epoch: int = -1
    best_state_dict: dict | None = None


class TrainingLoop:
    """Trains a model end-to-end and returns a :class:`TrainingResult`."""

    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        loss_fn: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        max_epochs: int = 80,
        early_stopping: EarlyStopping | None = None,
        hooks: HookRegistry | None = None,
        device: str = "cpu",
    ) -> None:
        if max_epochs <= 0:
            raise ValueError(f"max_epochs must be > 0, got {max_epochs}")
        self.model = model.to(device)
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.max_epochs = max_epochs
        self.early_stopping = early_stopping or EarlyStopping(patience=10)
        self.hooks = hooks or HookRegistry()
        self.device = device

    def run(self) -> TrainingResult:
        """Execute the train/val loop and emit a :class:`TrainingResult`."""
        result = TrainingResult()
        start = time.perf_counter()
        self.hooks.fire(HookEvent.BEFORE_TRAIN, model=self.model)

        for epoch in range(self.max_epochs):
            train_loss = self._train_one_epoch()
            val_loss = self._evaluate(self.val_loader)
            result.train_loss_per_epoch.append(train_loss)
            result.val_loss_per_epoch.append(val_loss)
            result.epochs_run = epoch + 1
            self.hooks.fire(
                HookEvent.AFTER_EPOCH,
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_loss,
            )
            should_stop = self.early_stopping.step(
                val_loss, payload=deepcopy(self.model.state_dict()), epoch=epoch
            )
            if should_stop:
                _log.info("early stopping at epoch %d (best epoch %d)", epoch, self.early_stopping.best_epoch)
                break

        result.wall_clock_seconds = time.perf_counter() - start
        result.best_val_loss = float(self.early_stopping.best)
        result.best_epoch = int(self.early_stopping.best_epoch)
        result.best_state_dict = self.early_stopping.best_payload
        if result.best_state_dict is not None:
            self.model.load_state_dict(result.best_state_dict)
        self.hooks.fire(HookEvent.AFTER_TRAIN, result=result)
        return result

    def _train_one_epoch(self) -> float:
        self.model.train()
        total = 0.0
        n_batches = 0
        for inputs, targets in self.train_loader:
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)
            self.optimizer.zero_grad()
            preds = self.model(inputs)
            loss = self.loss_fn(preds, targets)
            if not torch.isfinite(loss):
                raise TrainingError(f"non-finite training loss: {loss.item()!r}")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), GRAD_CLIP_NORM)
            self.optimizer.step()
            total += float(loss.item())
            n_batches += 1
        return total / max(n_batches, 1)

    def _evaluate(self, loader: DataLoader) -> float:
        self.model.eval()
        total = 0.0
        n_batches = 0
        with torch.no_grad():
            for inputs, targets in loader:
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                preds = self.model(inputs)
                total += float(self.loss_fn(preds, targets).item())
                n_batches += 1
        return total / max(n_batches, 1)
