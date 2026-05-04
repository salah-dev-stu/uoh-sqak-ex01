"""Pure sinusoid generator (per PRD_dataset §1).

Produces ``y(t) = A * sin(2*pi*f*t + phi)`` sampled at ``Fs`` over ``T``.
Knows nothing about noise or training tuples — just the carrier waves.
"""

from __future__ import annotations

import math

import numpy as np


class SignalGenerator:
    """Stateless, deterministic generator of clean sinusoids."""

    def __init__(
        self,
        amplitude: float = 1.0,
        sampling_rate_hz: int = 1000,
        duration_seconds: float = 10.0,
    ) -> None:
        if amplitude <= 0:
            raise ValueError(f"amplitude must be > 0, got {amplitude}")
        if sampling_rate_hz <= 0:
            raise ValueError(f"sampling_rate_hz must be > 0, got {sampling_rate_hz}")
        if duration_seconds <= 0:
            raise ValueError(f"duration_seconds must be > 0, got {duration_seconds}")
        self.amplitude = float(amplitude)
        self.sampling_rate_hz = int(sampling_rate_hz)
        self.duration_seconds = float(duration_seconds)
        self.n_samples = int(round(self.sampling_rate_hz * self.duration_seconds))

    def time_axis(self) -> np.ndarray:
        """Return ``t = arange(N) / Fs`` of length ``N``."""
        return np.arange(self.n_samples, dtype=np.float64) / float(self.sampling_rate_hz)

    def pure(self, frequency_hz: float, phase: float = 0.0) -> np.ndarray:
        """Generate one clean sine of length ``N`` as float32."""
        if not math.isfinite(frequency_hz):
            raise ValueError(f"frequency_hz must be finite, got {frequency_hz}")
        t = self.time_axis()
        wave = self.amplitude * np.sin(2.0 * math.pi * float(frequency_hz) * t + float(phase))
        return wave.astype(np.float32)

    def pure_all(self, frequencies_hz: tuple[int, ...]) -> dict[int, np.ndarray]:
        """Generate one clean sine per requested frequency."""
        return {int(f): self.pure(float(f)) for f in frequencies_hz}
