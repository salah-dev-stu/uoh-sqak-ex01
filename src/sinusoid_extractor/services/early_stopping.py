"""Early-stopping helper: stop after ``patience`` epochs without improvement."""

from __future__ import annotations

import math
from copy import deepcopy
from typing import Any


class EarlyStopping:
    """Tracks best monitored value and signals when to stop."""

    def __init__(self, patience: int = 10, mode: str = "min", min_delta: float = 0.0) -> None:
        if patience < 0:
            raise ValueError(f"patience must be >= 0, got {patience}")
        if mode not in ("min", "max"):
            raise ValueError(f"mode must be 'min' or 'max', got {mode!r}")
        if min_delta < 0:
            raise ValueError(f"min_delta must be >= 0, got {min_delta}")
        self.patience = int(patience)
        self.mode = mode
        self.min_delta = float(min_delta)
        self._best: float = math.inf if mode == "min" else -math.inf
        self._epochs_no_improve = 0
        self._best_payload: dict[str, Any] | None = None
        self._best_epoch: int = -1

    def step(self, value: float, payload: dict[str, Any] | None = None, epoch: int = -1) -> bool:
        """Return ``True`` when training should stop."""
        improved = self._is_improvement(value)
        if improved:
            self._best = float(value)
            self._epochs_no_improve = 0
            self._best_payload = deepcopy(payload) if payload is not None else None
            self._best_epoch = int(epoch)
        else:
            self._epochs_no_improve += 1
        return self._epochs_no_improve > self.patience

    def _is_improvement(self, value: float) -> bool:
        if self.mode == "min":
            return value < self._best - self.min_delta
        return value > self._best + self.min_delta

    @property
    def best(self) -> float:
        """Best value observed so far."""
        return self._best

    @property
    def best_epoch(self) -> int:
        """Epoch index at which the best value was observed."""
        return self._best_epoch

    @property
    def best_payload(self) -> dict[str, Any] | None:
        """Snapshot stored at the best epoch (typically ``state_dict``)."""
        return self._best_payload
