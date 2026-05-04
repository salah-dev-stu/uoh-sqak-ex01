"""Tests for ``services.early_stopping``."""

import pytest

from sinusoid_extractor.services.early_stopping import EarlyStopping


def test_triggers_after_patience() -> None:
    es = EarlyStopping(patience=2, mode="min")
    assert not es.step(1.0, epoch=0)
    assert not es.step(1.5, epoch=1)
    assert not es.step(1.5, epoch=2)
    assert es.step(1.5, epoch=3)


def test_improvement_resets_counter() -> None:
    es = EarlyStopping(patience=2, mode="min")
    es.step(1.0, epoch=0)
    es.step(1.5, epoch=1)
    es.step(0.5, epoch=2)  # improvement → reset
    assert not es.step(0.6, epoch=3)
    assert not es.step(0.7, epoch=4)


def test_max_mode() -> None:
    es = EarlyStopping(patience=1, mode="max")
    es.step(0.1, epoch=0)
    es.step(0.5, epoch=1)
    assert not es.step(0.4, epoch=2)
    assert es.step(0.4, epoch=3)


def test_min_delta_ignores_small_improvement() -> None:
    es = EarlyStopping(patience=1, mode="min", min_delta=0.5)
    es.step(1.0, epoch=0)
    es.step(0.9, epoch=1)  # not enough delta
    assert es.step(0.95, epoch=2)


def test_invalid_args() -> None:
    with pytest.raises(ValueError):
        EarlyStopping(patience=-1)
    with pytest.raises(ValueError):
        EarlyStopping(mode="bad")
    with pytest.raises(ValueError):
        EarlyStopping(min_delta=-0.1)


def test_best_payload_updated_on_improvement() -> None:
    es = EarlyStopping(patience=5, mode="min")
    es.step(1.0, payload={"epoch": 0}, epoch=0)
    es.step(0.5, payload={"epoch": 1}, epoch=1)
    assert es.best_payload == {"epoch": 1}
    assert es.best_epoch == 1
    assert es.best == 0.5
