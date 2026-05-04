"""Tests for ``shared.gatekeeper``."""

import json

import pytest

from sinusoid_extractor.shared.gatekeeper import Gatekeeper, GatekeeperError


def test_call_returns_noop(rate_limits_path) -> None:
    g = Gatekeeper(rate_limits_path)
    out = g.call("default", payload={"a": 1})
    assert out == {"status": "noop", "service": "default"}


def test_unknown_service_falls_back_to_default(rate_limits_path) -> None:
    g = Gatekeeper(rate_limits_path)
    assert g.call("ghost") == {"status": "noop", "service": "ghost"}


def test_missing_file_raises(tmp_path) -> None:
    with pytest.raises(GatekeeperError):
        Gatekeeper(tmp_path / "nope.json")


def test_missing_version_raises(tmp_path) -> None:
    p = tmp_path / "rl.json"
    p.write_text(json.dumps({"services": {"default": {"requests_per_minute": 1, "requests_per_hour": 1, "concurrent_max": 1}}}))
    with pytest.raises(GatekeeperError):
        Gatekeeper(p)


def test_missing_default_raises(tmp_path) -> None:
    p = tmp_path / "rl.json"
    p.write_text(json.dumps({"version": "1.00", "services": {"foo": {"requests_per_minute": 1, "requests_per_hour": 1, "concurrent_max": 1}}}))
    with pytest.raises(GatekeeperError):
        Gatekeeper(p)


def test_zero_limit_rejected(tmp_path) -> None:
    p = tmp_path / "rl.json"
    p.write_text(json.dumps({"version": "1.00", "services": {"default": {"requests_per_minute": 0, "requests_per_hour": 1, "concurrent_max": 1}}}))
    with pytest.raises(GatekeeperError):
        Gatekeeper(p)


def test_no_default_for_named_service(tmp_path) -> None:
    p = tmp_path / "rl.json"
    p.write_text(json.dumps({"version": "1.00", "services": {"default": {"requests_per_minute": 1, "requests_per_hour": 1, "concurrent_max": 1}}}))
    g = Gatekeeper(p)
    # Should still succeed via default fallback
    assert g.call("anything")["status"] == "noop"
