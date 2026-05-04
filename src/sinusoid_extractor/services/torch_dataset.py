"""``torch.utils.data.Dataset`` adapter — supplies FC or recurrent input shape.

For FC: returns a flat ``(14,)`` tensor (one-hot ⊕ window).
For RNN/LSTM: returns ``(10, 5)`` (per-timestep one-hot ⊕ sample).
"""

from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset

from sinusoid_extractor.constants import (
    CONTEXT_WINDOW,
    INPUT_DIM_FC,
    ONE_HOT_DIM,
    Architecture,
)
from sinusoid_extractor.services.data_bundle import Split


class SinusoidWindowDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    """Tensor-yielding wrapper over a :class:`Split`."""

    def __init__(self, split: Split, arch: Architecture | str) -> None:
        self._split = split
        self._arch = Architecture(arch) if not isinstance(arch, Architecture) else arch
        self._cached_input = self._build_input_tensor()
        self._cached_target = torch.from_numpy(split.y).float()

    def __len__(self) -> int:
        return len(self._split)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self._cached_input[idx], self._cached_target[idx]

    def _build_input_tensor(self) -> torch.Tensor:
        c = self._split.C.astype(np.float32)
        x = self._split.x.astype(np.float32)
        if self._arch == Architecture.FC:
            flat = np.concatenate([c, x], axis=1)
            assert flat.shape[1] == INPUT_DIM_FC, flat.shape
            return torch.from_numpy(flat)

        # RNN / LSTM: (n, 10, 5) — broadcast one-hot across timesteps
        n = x.shape[0]
        c_repeated = np.broadcast_to(c[:, None, :], (n, CONTEXT_WINDOW, ONE_HOT_DIM))
        x_step = x[:, :, None]
        seq = np.concatenate([x_step, c_repeated], axis=2)
        return torch.from_numpy(seq.astype(np.float32))
