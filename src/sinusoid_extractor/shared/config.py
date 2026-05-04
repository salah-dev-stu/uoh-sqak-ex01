"""Configuration loader (FR-CFG-* / PRD §3.7).

Reads ``config/setup.json`` and validates the version against the
running code's ``__version__``. Returns plain dict for now (typed
dataclass tree can come later if needed); access is through dotted keys.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from sinusoid_extractor.shared.persistence import load_json
from sinusoid_extractor.shared.version import __version__, is_compatible

_log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "setup.json"


class ConfigError(Exception):
    """Raised when a config file is missing, malformed, or fails validation."""


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load and validate the project config; return a plain ``dict``."""
    p = Path(path) if path else DEFAULT_CONFIG_PATH
    if not p.exists():
        raise ConfigError(f"config file not found: {p}")
    try:
        cfg = load_json(p)
    except Exception as exc:
        raise ConfigError(f"failed to parse {p}: {exc}") from exc

    cfg = _strip_comments(cfg)
    _validate(cfg)
    _check_version(cfg)
    return cfg


def get(cfg: dict[str, Any], dotted: str, default: Any = None) -> Any:
    """Dotted-key access — ``get(cfg, 'training.learning_rate', 1e-3)``."""
    cur: Any = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def env_overrides() -> dict[str, str]:
    """Collect ``SINUSOID_*`` env vars (non-empty values only)."""
    return {k: v for k, v in os.environ.items() if k.startswith("SINUSOID_") and v}


def _strip_comments(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: _strip_comments(v) for k, v in d.items() if not k.startswith("_")}
    if isinstance(d, list):
        return [_strip_comments(v) for v in d]
    return d


def _validate(cfg: dict[str, Any]) -> None:
    required = ("version", "dataset", "training", "models", "experiment", "oat_sweep", "paths")
    for key in required:
        if key not in cfg:
            raise ConfigError(f"missing required top-level key: {key!r}")
    freqs = cfg["dataset"].get("frequencies_hz")
    if not (isinstance(freqs, list) and len(freqs) == 4 and all(f > 0 for f in freqs)):
        raise ConfigError(f"dataset.frequencies_hz must be 4 positive values, got {freqs!r}")
    lr = cfg["training"].get("learning_rate")
    if not (isinstance(lr, (int, float)) and lr > 0):
        raise ConfigError(f"training.learning_rate must be > 0, got {lr!r}")
    archs = cfg["experiment"].get("architectures")
    valid = {"fc", "rnn", "lstm"}
    if not (isinstance(archs, list) and set(archs) <= valid):
        raise ConfigError(f"experiment.architectures must be subset of {valid}, got {archs!r}")


def _check_version(cfg: dict[str, Any]) -> None:
    cfg_v = cfg.get("version")
    if not isinstance(cfg_v, str):
        raise ConfigError(f"config 'version' must be a string, got {cfg_v!r}")
    if not is_compatible(__version__, cfg_v):
        _log.warning(
            "version mismatch: code=%s, config=%s — proceeding with caution",
            __version__,
            cfg_v,
        )
