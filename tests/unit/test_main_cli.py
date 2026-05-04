"""Tests for ``main`` CLI."""

import pytest

from sinusoid_extractor.main import build_parser, main


def test_version_command(capsys) -> None:
    from sinusoid_extractor.shared.version import __version__
    rc = main(["version"])
    out = capsys.readouterr().out.strip()
    assert rc == 0
    assert out == __version__


def test_parser_rejects_bad_arch() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["train", "--arch", "transformer", "--alpha", "0.1"])


def test_parser_accepts_known_subcommands() -> None:
    parser = build_parser()
    parser.parse_args(["generate-data", "--alpha", "0.05"])
    parser.parse_args(["run-matrix"])
    parser.parse_args(["run-oat"])
