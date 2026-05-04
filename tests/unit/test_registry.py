"""Tests for ``models.registry``."""

import pytest

import sinusoid_extractor.models  # noqa: F401 — triggers registration
from sinusoid_extractor.models.registry import ModelRegistry


def test_three_archs_registered() -> None:
    available = ModelRegistry.available()
    assert {"fc", "rnn", "lstm"} <= set(available)


def test_build_unknown_raises() -> None:
    with pytest.raises(ValueError):
        ModelRegistry.build("transformer")


def test_register_duplicate_raises() -> None:
    with pytest.raises(ValueError):
        ModelRegistry.register("fc")(lambda: None)  # type: ignore[arg-type]


def test_register_invalid_name_raises() -> None:
    with pytest.raises(ValueError):
        ModelRegistry.register("")  # type: ignore[arg-type]
