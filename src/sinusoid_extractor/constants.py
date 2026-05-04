"""Project-wide constants and Enums.

Per RULES.md §11, code may carry mathematical/physical constants and Enum
values inline. Anything tunable (sweep ranges, defaults) must live in
``config/setup.json`` instead — never here.
"""

from __future__ import annotations

from enum import Enum

FIXED_FREQUENCIES_HZ: tuple[int, ...] = (1, 3, 5, 7)
"""The 4 fixed source frequencies (lecturer requirement; do NOT randomize)."""

CONTEXT_WINDOW: int = 10
"""Length (in samples) of the input window — lecturer requirement."""

ONE_HOT_DIM: int = 4
"""Dimensionality of the selector vector C (one per source)."""

INPUT_DIM_FC: int = ONE_HOT_DIM + CONTEXT_WINDOW
"""FC input dim = one-hot (4) + window (10) = 14."""

INPUT_DIM_RECURRENT_PER_STEP: int = 1 + ONE_HOT_DIM
"""RNN/LSTM per-timestep input dim = sample (1) + one-hot (4) = 5 (ADR-003)."""

OUTPUT_DIM: int = CONTEXT_WINDOW
"""Output dim = the predicted clean window of the selected sine."""

DEFAULT_SEED: int = 42
"""Default seed used when none is supplied. Override via config or CLI."""

LINE_LENGTH_LIMIT: int = 150
"""LoC ceiling per Python file (RULES.md §8)."""


class Architecture(str, Enum):
    """Registered model architectures (registry name = enum value)."""

    FC = "fc"
    RNN = "rnn"
    LSTM = "lstm"


class Optimizer(str, Enum):
    """Supported optimizers (training_service / optimizer_factory)."""

    ADAM = "adam"
    RMSPROP = "rmsprop"


class HookEvent(str, Enum):
    """Lifecycle hook events fired by TrainingLoop / EvaluationService."""

    BEFORE_TRAIN = "before_train"
    AFTER_EPOCH = "after_epoch"
    AFTER_TRAIN = "after_train"
    BEFORE_EVAL = "before_eval"
    AFTER_EVAL = "after_eval"


class NoiseDistribution(str, Enum):
    """Distribution choice for amplitude noise (ADR-002 = UNIFORM)."""

    UNIFORM = "uniform"
    GAUSSIAN = "gaussian"
