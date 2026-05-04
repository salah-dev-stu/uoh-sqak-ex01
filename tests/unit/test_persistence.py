"""Tests for ``shared.persistence``."""

from pathlib import Path

import numpy as np
import pytest

from sinusoid_extractor.shared.persistence import (
    append_csv_row,
    ensure_dir,
    load_json,
    load_npz,
    save_json,
    save_npz,
)


def test_ensure_dir_creates_nested(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "c"
    out = ensure_dir(target)
    assert out.is_dir()


def test_save_and_load_npz_round_trip(tmp_path: Path) -> None:
    a = np.arange(10, dtype=np.float32)
    b = np.linspace(0, 1, 5, dtype=np.float32)
    save_npz(tmp_path / "x.npz", a=a, b=b)
    loaded = load_npz(tmp_path / "x.npz")
    assert np.allclose(loaded["a"], a)
    assert np.allclose(loaded["b"], b)


def test_save_and_load_json_round_trip(tmp_path: Path) -> None:
    payload = {"a": 1, "b": [1, 2, 3], "c": {"d": "e"}}
    save_json(tmp_path / "x.json", payload)
    assert load_json(tmp_path / "x.json") == payload


def test_save_json_serialises_numpy(tmp_path: Path) -> None:
    payload = {"arr": np.array([1, 2, 3]), "scalar": np.float32(1.5)}
    save_json(tmp_path / "x.json", payload)
    loaded = load_json(tmp_path / "x.json")
    assert loaded["arr"] == [1, 2, 3]
    assert loaded["scalar"] == pytest.approx(1.5)


def test_save_json_rejects_unserialisable(tmp_path: Path) -> None:
    with pytest.raises(TypeError):
        save_json(tmp_path / "x.json", {"o": object()})


def test_append_csv_row_writes_header_then_rows(tmp_path: Path) -> None:
    p = tmp_path / "x.csv"
    append_csv_row(p, {"a": 1, "b": 2})
    append_csv_row(p, {"a": 3, "b": 4})
    text = p.read_text()
    assert text.splitlines()[0] == "a,b"
    assert "1,2" in text
    assert "3,4" in text
