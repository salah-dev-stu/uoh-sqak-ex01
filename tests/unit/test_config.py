"""Tests for ``shared.config``."""

import json
from pathlib import Path

import pytest

from sinusoid_extractor.shared.config import ConfigError, env_overrides, get, load_config


def test_load_returns_dict(tiny_config_path) -> None:
    cfg = load_config(tiny_config_path)
    assert cfg["version"] == "1.00"
    assert cfg["dataset"]["frequencies_hz"] == [1, 3, 5, 7]


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        load_config(tmp_path / "nope.json")


def test_malformed_json_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json")
    with pytest.raises(ConfigError):
        load_config(p)


def test_missing_required_key_raises(tmp_path: Path) -> None:
    p = tmp_path / "x.json"
    p.write_text(json.dumps({"version": "1.00", "dataset": {"frequencies_hz": [1, 3, 5, 7]}}))
    with pytest.raises(ConfigError):
        load_config(p)


def test_invalid_frequencies_raises(tmp_path: Path, tiny_config_dict) -> None:
    cfg = dict(tiny_config_dict)
    cfg["dataset"] = dict(cfg["dataset"], frequencies_hz=[1, 2, 3])
    p = tmp_path / "x.json"
    p.write_text(json.dumps(cfg))
    with pytest.raises(ConfigError):
        load_config(p)


def test_get_dotted_key(tiny_config_path) -> None:
    cfg = load_config(tiny_config_path)
    assert get(cfg, "training.learning_rate") == 0.001
    assert get(cfg, "missing.path", default=99) == 99


def test_strip_comments(tmp_path: Path, tiny_config_dict) -> None:
    cfg = dict(tiny_config_dict, _comment="hello", dataset={**tiny_config_dict["dataset"], "_note": "x"})
    p = tmp_path / "x.json"
    p.write_text(json.dumps(cfg))
    loaded = load_config(p)
    assert "_comment" not in loaded
    assert "_note" not in loaded["dataset"]


def test_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("SINUSOID_TEST", "1")
    monkeypatch.setenv("OTHER_VAR", "x")
    overrides = env_overrides()
    assert overrides["SINUSOID_TEST"] == "1"
    assert "OTHER_VAR" not in overrides


def test_invalid_lr_raises(tmp_path: Path, tiny_config_dict) -> None:
    cfg = dict(tiny_config_dict)
    cfg["training"] = dict(cfg["training"], learning_rate=-1.0)
    p = tmp_path / "x.json"
    p.write_text(json.dumps(cfg))
    with pytest.raises(ConfigError):
        load_config(p)


def test_invalid_arch_raises(tmp_path: Path, tiny_config_dict) -> None:
    cfg = dict(tiny_config_dict)
    cfg["experiment"] = dict(cfg["experiment"], architectures=["transformer"])
    p = tmp_path / "x.json"
    p.write_text(json.dumps(cfg))
    with pytest.raises(ConfigError):
        load_config(p)
