"""Tests for ``shared.queue_manager``."""

import pytest

from sinusoid_extractor.shared.queue_manager import BackpressureError, WaveQueue


def test_enqueue_dequeue_fifo_order() -> None:
    q = WaveQueue(max_size=3)
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert q.dequeue() == "c"


def test_dequeue_empty_returns_none() -> None:
    q = WaveQueue(max_size=1)
    assert q.dequeue() is None


def test_full_raises_backpressure() -> None:
    q = WaveQueue(max_size=2)
    q.enqueue(1)
    q.enqueue(2)
    with pytest.raises(BackpressureError):
        q.enqueue(3)


def test_size_and_is_full() -> None:
    q = WaveQueue(max_size=2)
    assert q.size() == 0
    assert not q.is_full()
    q.enqueue(1)
    q.enqueue(2)
    assert q.size() == 2
    assert q.is_full()


def test_invalid_max_size() -> None:
    with pytest.raises(ValueError):
        WaveQueue(max_size=0)
    with pytest.raises(ValueError):
        WaveQueue(max_size=-1)


def test_max_size_property() -> None:
    assert WaveQueue(max_size=5).max_size == 5
