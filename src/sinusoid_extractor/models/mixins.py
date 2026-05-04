"""Mixins shared across model classes (RULES.md §6 — DRY via mixin pattern).

Each mixin handles exactly one concern and is self-testable in isolation:
- :class:`ParamCountMixin` — counts trainable parameters
- :class:`SaveLoadMixin` — persists / restores the underlying ``state_dict``
"""

from __future__ import annotations

from pathlib import Path

import torch
from torch import nn


class ParamCountMixin:
    """Adds :meth:`count_parameters` to any ``nn.Module``."""

    def count_parameters(self: nn.Module) -> int:  # type: ignore[misc]
        """Return the count of trainable parameters in the module."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class SaveLoadMixin:
    """Adds :meth:`save` / :meth:`load` for ``state_dict`` persistence."""

    def save(self: nn.Module, path: Path | str) -> Path:  # type: ignore[misc]
        """Write ``state_dict`` to ``path`` (parent dir created if missing)."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), p)
        return p

    def load(self: nn.Module, path: Path | str) -> None:  # type: ignore[misc]
        """Replace this module's weights with those at ``path``."""
        state = torch.load(Path(path), map_location="cpu", weights_only=True)
        self.load_state_dict(state)
