"""Tests for ``models.mixins``."""

from pathlib import Path

import torch
from torch import nn

from sinusoid_extractor.models.mixins import ParamCountMixin, SaveLoadMixin


class _Tiny(nn.Module, ParamCountMixin, SaveLoadMixin):
    def __init__(self) -> None:
        super().__init__()
        self.fc = nn.Linear(3, 2)


def test_count_parameters() -> None:
    m = _Tiny()
    # 3*2 weight + 2 bias = 8
    assert m.count_parameters() == 8


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    a = _Tiny()
    b = _Tiny()
    a.save(tmp_path / "w.pt")
    b.load(tmp_path / "w.pt")
    for pa, pb in zip(a.parameters(), b.parameters(), strict=False):
        assert torch.allclose(pa, pb)
