"""Abstract base class for all extractor models.

All FC / RNN / LSTM extractors share:
- the same I/O contract (input dim, output dim) — see :mod:`constants`
- the :class:`ParamCountMixin` and :class:`SaveLoadMixin` behaviour
- a stable ``architecture_name()`` for run-id construction
"""

from __future__ import annotations

from abc import abstractmethod

import torch
from torch import nn

from sinusoid_extractor.constants import OUTPUT_DIM
from sinusoid_extractor.models.mixins import ParamCountMixin, SaveLoadMixin


class BaseExtractor(nn.Module, ParamCountMixin, SaveLoadMixin):
    """Abstract extractor: every concrete model subclasses this."""

    output_dim: int = OUTPUT_DIM

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Map an input batch to a (B, OUTPUT_DIM) prediction."""

    @abstractmethod
    def architecture_name(self) -> str:
        """Stable identifier used in run_ids and logs."""

    def to_device(self, device: str | torch.device) -> BaseExtractor:
        """Move parameters and buffers to ``device`` and return self."""
        self.to(device)
        return self
