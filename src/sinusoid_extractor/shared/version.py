"""Project version (RULES.md §15).

Starts at 1.00 and bumps by +0.01 per change. Configs carry their own
"version" key validated against `__version__` at SDK init.
"""

from __future__ import annotations

__version__ = "1.11"


def parse(version: str) -> tuple[int, int]:
    """Parse a 'MAJOR.MINOR' string into a (major, minor) integer pair.

    Raises ValueError on malformed input. Padded minor (e.g. '1.05') is fine.
    """
    if not isinstance(version, str):
        raise TypeError(f"version must be a string, got {type(version).__name__}")
    parts = version.split(".")
    if len(parts) != 2:
        raise ValueError(f"version must be MAJOR.MINOR, got '{version}'")
    try:
        major = int(parts[0])
        minor = int(parts[1])
    except ValueError as exc:
        raise ValueError(f"version components must be integers, got '{version}'") from exc
    if major < 0 or minor < 0 or minor > 99:
        raise ValueError(f"invalid version components in '{version}'")
    return major, minor


def bump(version: str) -> str:
    """Increment the minor component by 1 (rolling over at 100 → next major)."""
    major, minor = parse(version)
    minor += 1
    if minor >= 100:
        major += 1
        minor = 0
    return f"{major}.{minor:02d}"


def is_compatible(code_version: str, config_version: str) -> bool:
    """Compatibility = same MAJOR (config and code may differ on minor)."""
    return parse(code_version)[0] == parse(config_version)[0]
