"""Structured logger configured from JSON (FR-CFG-3).

Honours the dict-config under ``config/logging_config.json`` when present;
otherwise falls back to a plain console handler at INFO. The ``SINUSOID_LOG_LEVEL``
environment variable always wins.
"""

from __future__ import annotations

import contextlib
import json
import logging
import logging.config
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOGGING_CONFIG = REPO_ROOT / "config" / "logging_config.json"


def configure_logging(path: Path | str | None = None) -> None:
    """Apply the dict-config at ``path`` (or the default location)."""
    p = Path(path) if path else DEFAULT_LOGGING_CONFIG
    if p.exists():
        with p.open(encoding="utf-8") as fh:
            try:
                cfg = json.load(fh)
            except json.JSONDecodeError:
                _basic()
                return
        logging.config.dictConfig(cfg)
    else:
        _basic()
    _apply_env_override()


def get_logger(name: str) -> logging.Logger:
    """Return a logger and lazily configure logging on first use."""
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name)


def _basic() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )


def _apply_env_override() -> None:
    level = os.environ.get("SINUSOID_LOG_LEVEL")
    if not level:
        return
    with contextlib.suppress(AttributeError):
        logging.getLogger().setLevel(getattr(logging, level.upper()))
