"""Fully Connected baseline extractor (FR-MOD-2 / PRD_fc_model).

Flat 14-dim input → ReLU MLP → 10-dim linear output. Acts as the baseline
that any recurrent model should beat to justify its added complexity.
"""

from __future__ import annotations

import torch
from torch import nn

from sinusoid_extractor.constants import INPUT_DIM_FC, OUTPUT_DIM, Architecture
from sinusoid_extractor.models.base_extractor import BaseExtractor
from sinusoid_extractor.models.registry import register


@register(Architecture.FC.value)
class FCExtractor(BaseExtractor):
    """ReLU MLP. Output is linear (no activation) since targets are real-valued."""

    def __init__(
        self,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
        input_dim: int = INPUT_DIM_FC,
        output_dim: int = OUTPUT_DIM,
    ) -> None:
        super().__init__()
        if hidden_size <= 0:
            raise ValueError(f"hidden_size must be > 0, got {hidden_size}")
        if num_layers not in (1, 2, 3):
            raise ValueError(f"num_layers must be 1, 2, or 3, got {num_layers}")
        if not 0.0 <= dropout < 1.0:
            raise ValueError(f"dropout must be in [0, 1), got {dropout}")

        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.output_dim = output_dim

        layers: list[nn.Module] = []
        in_dim = input_dim
        for _ in range(num_layers):
            layers.append(nn.Linear(in_dim, hidden_size))
            layers.append(nn.ReLU())
            if dropout > 0.0:
                layers.append(nn.Dropout(dropout))
            in_dim = hidden_size
        layers.append(nn.Linear(in_dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass — see PRD_fc_model §1 for the equation."""
        return self.net(x)

    def architecture_name(self) -> str:
        return Architecture.FC.value
