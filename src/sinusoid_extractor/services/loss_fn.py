"""Lecturer's loss formula: ``L = sum_{i=1..10} (yhat_i - y_i)^2``.

Sums squared error across the 10-sample window axis, then means over batch
so that gradients are well-scaled regardless of batch size. Equivalent to
``F.mse_loss(reduction='sum') / batch_size``.
"""

from __future__ import annotations

import torch
from torch import nn


class WindowSumMSE(nn.Module):
    """Per-element squared error, summed over the last axis, mean over batch."""

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        if prediction.shape != target.shape:
            raise ValueError(
                f"shape mismatch: prediction {tuple(prediction.shape)} "
                f"vs target {tuple(target.shape)}"
            )
        squared = (prediction - target) ** 2
        per_example = squared.sum(dim=-1)
        return per_example.mean()
