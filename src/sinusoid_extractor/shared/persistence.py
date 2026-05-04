"""Filesystem I/O helpers — npz / json / csv.

All path-touching code is concentrated here so tests can mock once and the
rest of the codebase stays oblivious to the filesystem layout.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


def ensure_dir(path: Path | str) -> Path:
    """Create the directory if missing; return it as a Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_npz(path: Path | str, **arrays: np.ndarray) -> Path:
    """Save named numpy arrays to a compressed .npz at ``path``."""
    p = Path(path)
    ensure_dir(p.parent)
    np.savez_compressed(p, **arrays)
    return p


def load_npz(path: Path | str) -> dict[str, np.ndarray]:
    """Load a .npz produced by :func:`save_npz` into a dict."""
    p = Path(path)
    with np.load(p, allow_pickle=False) as data:
        return {k: data[k] for k in data.files}


def save_json(path: Path | str, payload: dict[str, Any]) -> Path:
    """Write ``payload`` as pretty-printed JSON to ``path``."""
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False, default=_json_default)
    return p


def load_json(path: Path | str) -> dict[str, Any]:
    """Load a JSON document into a Python dict."""
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def append_csv_row(path: Path | str, row: dict[str, Any]) -> Path:
    """Append a row to a CSV, writing a header when the file is new."""
    p = Path(path)
    ensure_dir(p.parent)
    is_new = not p.exists() or p.stat().st_size == 0
    with p.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
        if is_new:
            writer.writeheader()
        writer.writerow(row)
    return p


def _json_default(obj: Any) -> Any:
    """Best-effort serialiser for numpy scalars and arrays."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serialisable")
