"""Tests for ``shared.hooks``."""

import pytest

from sinusoid_extractor.constants import HookEvent
from sinusoid_extractor.shared.hooks import HookRegistry


def test_register_and_fire_in_order() -> None:
    reg = HookRegistry()
    log: list[str] = []
    reg.register(HookEvent.AFTER_EPOCH, lambda **_: log.append("a"))
    reg.register("after_epoch", lambda **_: log.append("b"))
    reg.fire(HookEvent.AFTER_EPOCH)
    assert log == ["a", "b"]


def test_fire_swallows_exceptions() -> None:
    reg = HookRegistry()
    reg.register(HookEvent.BEFORE_TRAIN, lambda **_: (_ for _ in ()).throw(RuntimeError("boom")))
    reg.fire(HookEvent.BEFORE_TRAIN)


def test_unknown_event_string_raises() -> None:
    reg = HookRegistry()
    with pytest.raises(KeyError):
        reg.register("not_an_event", lambda **_: None)


def test_unknown_event_type_raises() -> None:
    reg = HookRegistry()
    with pytest.raises(TypeError):
        reg.register(123, lambda **_: None)  # type: ignore[arg-type]


def test_count_and_clear() -> None:
    reg = HookRegistry()
    reg.register(HookEvent.AFTER_TRAIN, lambda **_: None)
    assert reg.count(HookEvent.AFTER_TRAIN) == 1
    reg.clear()
    assert reg.count(HookEvent.AFTER_TRAIN) == 0


def test_fire_passes_kwargs() -> None:
    reg = HookRegistry()
    captured: dict = {}
    reg.register(HookEvent.AFTER_EPOCH, lambda **kw: captured.update(kw))
    reg.fire(HookEvent.AFTER_EPOCH, epoch=3, train_loss=0.1)
    assert captured == {"epoch": 3, "train_loss": 0.1}
