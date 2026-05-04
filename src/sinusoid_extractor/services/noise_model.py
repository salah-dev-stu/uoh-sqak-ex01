"""Per-signal amplitude + phase noise (per PRD_dataset §1, ADR-002).

Amplitude noise = uniform multiplicative perturbation in ``[-alpha, +alpha]``
per sample. Phase noise = single uniform draw in ``[0, 2*pi]`` per realisation
(the lecturer's "let the phase go wild").
"""

from __future__ import annotations

import logging
import math

import numpy as np

from sinusoid_extractor.constants import NoiseDistribution

_log = logging.getLogger(__name__)


class NoiseModel:
    """Random noise application — amplitude per-sample, phase per-realisation.

    Building Block (RULES.md §16):
        Input  : pure (1-D ndarray), alpha (float in [0, 1]),
                 distribution (NoiseDistribution, default UNIFORM)
        Output : noisy 1-D float32 ndarray, same shape as input
        Setup  : rng (numpy.random.Generator, injected for determinism)
    """

    def __init__(self, rng: np.random.Generator) -> None:
        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be a numpy.random.Generator")
        self._rng = rng

    def random_phase(self) -> float:
        """Draw a single phase from ``Uniform(0, 2*pi)``."""
        return float(self._rng.uniform(0.0, 2.0 * math.pi))

    def apply_amplitude_noise(
        self,
        pure: np.ndarray,
        alpha: float,
        distribution: NoiseDistribution = NoiseDistribution.UNIFORM,
    ) -> np.ndarray:
        """Multiplicative noise: ``pure * (1 + eta)`` per sample."""
        if alpha < 0:
            raise ValueError(f"alpha must be >= 0, got {alpha}")
        if alpha > 1:
            _log.warning("alpha=%s is unusually large; signal heavily perturbed", alpha)
        if alpha == 0:
            return pure.astype(np.float32, copy=True)

        n = pure.shape[0]
        if distribution == NoiseDistribution.UNIFORM:
            eta = self._rng.uniform(-alpha, alpha, size=n)
        elif distribution == NoiseDistribution.GAUSSIAN:
            eta = self._rng.normal(0.0, alpha, size=n)
        else:
            raise ValueError(f"unknown distribution {distribution!r}")
        return (pure.astype(np.float64) * (1.0 + eta)).astype(np.float32)
