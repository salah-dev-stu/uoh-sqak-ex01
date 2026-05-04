"""FIFO wave queue with bounded capacity and backpressure (RULES.md §5).

HW1 has no remote service, so the queue is exercised only by tests and the
gatekeeper stub. The structure exists to satisfy the rubric's architectural
checklist and to be ready for future API integrations.
"""

from __future__ import annotations

import threading
from collections import deque
from typing import Any


class BackpressureError(RuntimeError):
    """Raised when an enqueue is attempted while the queue is at capacity."""


class WaveQueue:
    """Thread-safe bounded FIFO queue."""

    def __init__(self, max_size: int) -> None:
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError(f"max_size must be a positive int, got {max_size!r}")
        self._max_size = max_size
        self._items: deque[Any] = deque()
        self._lock = threading.Lock()

    def enqueue(self, item: Any) -> None:
        """Append an item to the back of the queue."""
        with self._lock:
            if len(self._items) >= self._max_size:
                raise BackpressureError(
                    f"queue at capacity ({self._max_size}); cannot enqueue"
                )
            self._items.append(item)

    def dequeue(self) -> Any | None:
        """Pop and return the front item, or None when empty."""
        with self._lock:
            if not self._items:
                return None
            return self._items.popleft()

    def size(self) -> int:
        """Current queue depth."""
        with self._lock:
            return len(self._items)

    def is_full(self) -> bool:
        """Whether the queue has reached ``max_size``."""
        with self._lock:
            return len(self._items) >= self._max_size

    @property
    def max_size(self) -> int:
        """Configured capacity."""
        return self._max_size
