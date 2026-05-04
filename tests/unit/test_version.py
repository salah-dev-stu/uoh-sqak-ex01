"""Tests for ``shared.version``."""

import pytest

from sinusoid_extractor.shared import version
from sinusoid_extractor.shared.version import bump, is_compatible, parse


def test_version_constant_is_major_1() -> None:
    """Project versioning starts at 1.00 and bumps by +0.01 per change.

    Compatibility check (RULES.md §15) is by MAJOR — assert MAJOR == 1.
    """
    major, _ = parse(version.__version__)
    assert major == 1


def test_parse_valid() -> None:
    assert parse("1.00") == (1, 0)
    assert parse("2.05") == (2, 5)


def test_parse_rejects_non_str() -> None:
    with pytest.raises(TypeError):
        parse(1.0)  # type: ignore[arg-type]


def test_parse_rejects_malformed() -> None:
    with pytest.raises(ValueError):
        parse("1")
    with pytest.raises(ValueError):
        parse("1.2.3")


def test_parse_rejects_non_integer_components() -> None:
    with pytest.raises(ValueError):
        parse("1.x")


def test_bump_minor() -> None:
    assert bump("1.00") == "1.01"
    assert bump("1.05") == "1.06"


def test_bump_overflow_to_next_major() -> None:
    assert bump("1.99") == "2.00"


def test_is_compatible_same_major() -> None:
    assert is_compatible("1.00", "1.05")
    assert not is_compatible("1.00", "2.00")
