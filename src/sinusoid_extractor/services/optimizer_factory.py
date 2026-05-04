"""Build a torch ``Optimizer`` from a string name."""

from __future__ import annotations

from collections.abc import Iterable

import torch

from sinusoid_extractor.constants import Optimizer


def build_optimizer(
    name: str | Optimizer,
    parameters: Iterable[torch.Tensor],
    learning_rate: float,
) -> torch.optim.Optimizer:
    """Return an Adam or RMSprop instance bound to ``parameters``."""
    if learning_rate <= 0:
        raise ValueError(f"learning_rate must be > 0, got {learning_rate}")
    key = name.value if isinstance(name, Optimizer) else str(name).lower()
    if key == Optimizer.ADAM.value:
        return torch.optim.Adam(parameters, lr=learning_rate)
    if key == Optimizer.RMSPROP.value:
        return torch.optim.RMSprop(parameters, lr=learning_rate)
    valid = [o.value for o in Optimizer]
    raise ValueError(f"unknown optimizer {name!r}; valid: {valid}")
