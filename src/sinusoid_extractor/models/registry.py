"""Model registry / factory (ADR-005, RULES.md §18.5).

Adds a new model by writing a new file under ``models/`` decorated with
``@register("name")``. Lookup goes through :class:`ModelRegistry`; no edits
needed to existing files.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class _Registry:
    """Singleton-ish dispatch table keyed by string architecture name."""

    def __init__(self) -> None:
        self._map: dict[str, type] = {}

    def register(self, name: str) -> Callable[[type[T]], type[T]]:
        """Decorator: bind ``cls`` to ``name``."""
        if not isinstance(name, str) or not name:
            raise ValueError(f"registry name must be a non-empty str, got {name!r}")

        def _decorator(cls: type[T]) -> type[T]:
            if name in self._map:
                raise ValueError(f"architecture {name!r} already registered")
            self._map[name] = cls
            return cls

        return _decorator

    def build(self, name: str, **kwargs: Any) -> Any:
        """Instantiate the class registered under ``name`` with ``kwargs``."""
        try:
            cls = self._map[name]
        except KeyError as exc:
            raise ValueError(
                f"unknown architecture {name!r}; available: {self.available()}"
            ) from exc
        return cls(**kwargs)

    def available(self) -> list[str]:
        """Sorted list of all currently-registered names."""
        return sorted(self._map)

    def clear(self) -> None:
        """Reset the registry (test convenience; never call in production)."""
        self._map.clear()


ModelRegistry = _Registry()
"""Process-wide model registry. Import & call ``ModelRegistry.register('foo')``."""


def register(name: str) -> Callable[[type[T]], type[T]]:
    """Convenience alias for ``ModelRegistry.register(name)``."""
    return ModelRegistry.register(name)
