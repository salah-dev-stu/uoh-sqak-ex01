"""Tests for ``shared.logger``."""

import json
import logging
from pathlib import Path

from sinusoid_extractor.shared.logger import configure_logging, get_logger


def test_get_logger_returns_logger() -> None:
    log = get_logger("sinusoid_extractor.test")
    assert isinstance(log, logging.Logger)


def test_configure_logging_with_missing_file_uses_basic(tmp_path: Path) -> None:
    configure_logging(tmp_path / "missing.json")
    assert logging.getLogger().handlers


def test_configure_logging_with_malformed_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json")
    configure_logging(p)
    assert logging.getLogger().handlers


def test_env_override_sets_level(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SINUSOID_LOG_LEVEL", "WARNING")
    p = tmp_path / "x.json"
    p.write_text(json.dumps({
        "version": 1,
        "formatters": {"f": {"format": "%(message)s"}},
        "handlers": {"h": {"class": "logging.StreamHandler", "formatter": "f"}},
        "root": {"level": "DEBUG", "handlers": ["h"]},
        "disable_existing_loggers": False,
    }))
    configure_logging(p)
    assert logging.getLogger().level == logging.WARNING


def test_env_override_invalid_level_is_silent(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SINUSOID_LOG_LEVEL", "BOGUS")
    configure_logging(tmp_path / "missing.json")
