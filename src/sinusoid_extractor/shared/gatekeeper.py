"""API gatekeeper (RULES.md §7).

HW1 has no external HTTP services, so the production class is a no-op stub
that still loads and validates ``config/rate_limits.json``. The slot exists
so future homework can drop a real client in without touching downstream
services.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from sinusoid_extractor.shared.persistence import load_json

_log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RATE_LIMITS_PATH = REPO_ROOT / "config" / "rate_limits.json"


class GatekeeperError(RuntimeError):
    """Raised when the gatekeeper cannot satisfy a request."""


class Gatekeeper:
    """Centralised pass-through for any external API call (currently noop)."""

    def __init__(self, rate_limits_path: Path | str | None = None) -> None:
        path = Path(rate_limits_path) if rate_limits_path else DEFAULT_RATE_LIMITS_PATH
        if not path.exists():
            raise GatekeeperError(f"rate_limits config missing: {path}")
        self._cfg = load_json(path)
        self._validate()

    def call(self, service: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Pretend to call ``service``; return a noop response. Logged."""
        limits = self._limits_for(service)
        _log.debug(
            "gatekeeper noop call service=%s limits=%s payload_keys=%s",
            service,
            limits,
            list((payload or {}).keys()),
        )
        return {"status": "noop", "service": service}

    def _limits_for(self, service: str) -> dict[str, Any]:
        services = self._cfg.get("services", {})
        if service in services:
            return services[service]
        if "default" in services:
            return services["default"]
        raise GatekeeperError(f"no limits defined for {service!r} and no default")

    def _validate(self) -> None:
        if "version" not in self._cfg:
            raise GatekeeperError("rate_limits.json missing 'version'")
        services = self._cfg.get("services")
        if not isinstance(services, dict) or "default" not in services:
            raise GatekeeperError("rate_limits.json must define services.default")
        for name, lim in services.items():
            for key in ("requests_per_minute", "requests_per_hour", "concurrent_max"):
                if key not in lim:
                    raise GatekeeperError(f"service {name!r} missing {key!r}")
                if lim[key] <= 0:
                    raise GatekeeperError(f"service {name!r}.{key} must be > 0")
