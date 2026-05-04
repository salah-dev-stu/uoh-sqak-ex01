"""Lifecycle hook registry (RULES.md §18.5).

Plugins attach callables to events fired by the training loop / evaluation
service without modifying the core. Hooks are best-effort: an exception in a
hook is logged but does not abort the run.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from sinusoid_extractor.constants import HookEvent

_log = logging.getLogger(__name__)

HookFn = Callable[..., None]


class HookRegistry:
    """Lookup of event-name → ordered list of registered callables."""

    def __init__(self) -> None:
        self._hooks: dict[str, list[HookFn]] = defaultdict(list)

    def register(self, event: HookEvent | str, fn: HookFn) -> None:
        """Attach ``fn`` to ``event``. Fires in registration order."""
        key = self._coerce(event)
        self._hooks[key].append(fn)

    def fire(self, event: HookEvent | str, /, **ctx: Any) -> None:
        """Fire ``event`` with keyword context; swallow & log fn exceptions."""
        key = self._coerce(event)
        for fn in self._hooks.get(key, ()):
            try:
                fn(**ctx)
            except Exception as exc:  # noqa: BLE001 — best-effort hooks
                _log.warning("hook %s failed: %s", fn.__name__, exc)

    def count(self, event: HookEvent | str) -> int:
        """Return how many hooks are registered for ``event``."""
        return len(self._hooks.get(self._coerce(event), ()))

    def clear(self) -> None:
        """Remove all registered hooks (test convenience)."""
        self._hooks.clear()

    @staticmethod
    def _coerce(event: HookEvent | str) -> str:
        if isinstance(event, HookEvent):
            return event.value
        if not isinstance(event, str):
            raise TypeError(f"event must be HookEvent or str, got {type(event).__name__}")
        valid = {e.value for e in HookEvent}
        if event not in valid:
            raise KeyError(f"unknown event {event!r}; valid: {sorted(valid)}")
        return event
