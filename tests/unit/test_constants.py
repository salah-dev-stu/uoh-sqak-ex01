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


def test_fixed_frequencies_match_lecturer_spec() -> None:
    assert FIXED_FREQUENCIES_HZ == (1, 3, 5, 7)


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
