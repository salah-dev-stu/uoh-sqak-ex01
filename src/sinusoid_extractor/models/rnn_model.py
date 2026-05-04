"""Vanilla RNN extractor (FR-MOD-3 / PRD_rnn_model).

10-step sequence with per-timestep input ``[sample, one_hot]`` (ADR-003).
Hidden update: ``h_t = tanh(W_h h_{t-1} + W_x x_t + b)``.
"""

from __future__ import annotations

import torch
from torch import nn

from sinusoid_extractor.constants import (
    INPUT_DIM_RECURRENT_PER_STEP,
    OUTPUT_DIM,
    Architecture,
)
from sinusoid_extractor.models.base_extractor import BaseExtractor
from sinusoid_extractor.models.registry import register


@register(Architecture.RNN.value)
class RNNExtractor(BaseExtractor):
    """``torch.nn.RNN`` with tanh, last hidden state → ``Linear`` to 10 outputs."""

    def __init__(
        self,
        hidden_size: int = 128,
        num_layers: int = 1,
        dropout: float = 0.0,
        input_dim_per_step: int = INPUT_DIM_RECURRENT_PER_STEP,
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

        self.rnn = nn.RNN(
            input_size=input_dim_per_step,
            hidden_size=hidden_size,
            num_layers=num_layers,
            nonlinearity="tanh",
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.head = nn.Linear(hidden_size, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """``x`` shape ``(B, 10, 5)`` → ``(B, 10)``."""
        out, _ = self.rnn(x)
        last = out[:, -1, :]
        return self.head(last)

    def architecture_name(self) -> str:
        return Architecture.RNN.value
