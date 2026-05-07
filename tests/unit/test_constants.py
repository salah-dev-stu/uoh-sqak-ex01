"""Sanity tests for project constants."""

from sinusoid_extractor.constants import (
    CONTEXT_WINDOW,
    FIXED_FREQUENCIES_HZ,
    INPUT_DIM_FC,
    INPUT_DIM_RECURRENT_PER_STEP,
    ONE_HOT_DIM,
    OUTPUT_DIM,
    Architecture,
    HookEvent,
    NoiseDistribution,
    Optimizer,
)


def test_fixed_frequencies_have_4_distinct_positive_values() -> None:
    """Frequencies are 4 distinct positive integers.

    Concrete values are tunable via config (current default: 20/60/100/200 Hz,
    chosen to span sub-cycle and multi-cycle regimes within the 10-sample
    window at Fs=1000 Hz).
    """
    assert len(FIXED_FREQUENCIES_HZ) == 4
    assert all(f > 0 for f in FIXED_FREQUENCIES_HZ)
    assert len(set(FIXED_FREQUENCIES_HZ)) == 4


def test_one_hot_and_window() -> None:
    assert ONE_HOT_DIM == 4
    assert CONTEXT_WINDOW == 10
    assert OUTPUT_DIM == 10


def test_input_dims() -> None:
    assert INPUT_DIM_FC == ONE_HOT_DIM + CONTEXT_WINDOW == 14
    assert INPUT_DIM_RECURRENT_PER_STEP == 1 + ONE_HOT_DIM == 5


def test_architecture_members_cover_three() -> None:
    assert {a.value for a in Architecture} == {"fc", "rnn", "lstm"}


def test_optimizer_members() -> None:
    assert "adam" in {o.value for o in Optimizer}
    assert "rmsprop" in {o.value for o in Optimizer}


def test_hook_events() -> None:
    expected = {"before_train", "after_epoch", "after_train", "before_eval", "after_eval"}
    assert {e.value for e in HookEvent} == expected


def test_noise_distributions() -> None:
    assert {n.value for n in NoiseDistribution} == {"uniform", "gaussian"}
