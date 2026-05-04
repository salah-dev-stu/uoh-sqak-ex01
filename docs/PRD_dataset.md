# Per-Mechanism PRD — Dataset Generation

| Field | Value |
|---|---|
| Mechanism | Dataset generation (synthetic 4-sine + noise) |
| Owner module | `src/sinusoid_extractor/services/dataset_service.py` (+ helpers) |
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` §3.1, `PLAN.md` §3, `TODO.md` Phase 5 |

---

## 1. Theoretical Background

### 1.1 The forward model
We model a noisy time-domain signal as the sum of K = 4 narrowband sinusoidal sources, each independently corrupted by **amplitude noise** and **phase noise**:

$$
S_k(t) = A_k \cdot \sin(2\pi F_k t + \varphi_k) \cdot (1 + \eta_k(t))
$$

with
$$
\eta_k(t) \sim \mathcal{U}(-\alpha,\, +\alpha), \qquad \varphi_k \sim \mathcal{U}(0,\, 2\pi)
$$

The phase $\varphi_k$ is drawn **once per realization** (the lecturer's "let the phase go wild" — a per-realization random offset over the **full** $[0, 2\pi]$ interval, *not* a small jitter).

The amplitude noise $\eta_k(t)$ is drawn **per-sample** as a uniform multiplicative perturbation bounded by ±α (relative to the carrier). This is ADR-002's choice over Gaussian, justified below.

The combined observed signal is:
$$
\Sigma(t) = \sum_{k=1}^{4} S_k(t)
$$

The clean (target) per-source signal is:
$$
S_k^{\text{pure}}(t) = A_k \cdot \sin(2\pi F_k t)
$$
(amplitude noise off, phase $\equiv 0$ by convention so all sources are aligned in the target space). The phase ambiguity in the noisy realization makes the inverse problem non-trivial: the network must learn that $\Sigma$'s decomposition depends on the **fixed frequencies**, not the (random) phases.

### 1.2 Why this dataset
- **Controlled difficulty.** $\alpha$ knob smoothly interpolates from "trivial" (α=0) to "hard" (α=0.20+).
- **Frequency-stratified evaluation.** Each $F_k$ is a separate evaluation cell, exposing per-frequency strengths/weaknesses of FC, RNN, LSTM.
- **Fair comparison.** Identical $(C, x, y)$ tuples are reused across architectures (only the input *shaping* differs).

### 1.3 Sampling
- Sampling rate $F_s = 1000$ Hz
- Duration $T = 10$ s
- Samples per signal $N = F_s \cdot T = 10\,000$

Per Nyquist, frequencies up to 500 Hz are representable; our 1/3/5/7 Hz are well below the limit, with thousands of samples per cycle ensuring smooth waveforms.

---

## 2. Inputs

### 2.1 Configuration
Loaded from `config/setup.json` § `dataset`:
| Key | Type | Default | Range |
|---|---|---|---|
| `frequencies_hz` | list[int] | `[1, 3, 5, 7]` | length 4, all > 0, distinct |
| `amplitude` | float | `1.0` | > 0 |
| `sampling_rate_hz` | int | `1000` | > 0 |
| `duration_seconds` | float | `10` | > 0 |
| `context_window` | int | `10` | ≥ 1, ≤ N |
| `n_train` | int | `5000` | ≥ 1 |
| `n_val` | int | `1000` | ≥ 1 |
| `n_test` | int | `1000` | ≥ 1 |
| `seed` | int | `42` | any int |
| `noise_levels_alpha` | list[float] | `[0.01, 0.05, 0.10, 0.20]` | each in [0, 1] |

### 2.2 Runtime arguments
- `alpha: float in [0, 1]` — current noise level for this dataset realization.
- `seed: int | None` — overrides config seed if provided.

---

## 3. Outputs

### 3.1 Raw signals
Persisted to `data/raw/dataset_alpha{α:.2f}_seed{seed}.npz`:
| Key | Shape | Dtype | Meaning |
|---|---|---|---|
| `pure_1hz` | (10000,) | float32 | clean 1 Hz sine |
| `pure_3hz` | (10000,) | float32 | clean 3 Hz sine |
| `pure_5hz` | (10000,) | float32 | clean 5 Hz sine |
| `pure_7hz` | (10000,) | float32 | clean 7 Hz sine |
| `noisy_1hz` | (10000,) | float32 | 1 Hz with amp+phase noise |
| `noisy_3hz` | (10000,) | float32 | 3 Hz with amp+phase noise |
| `noisy_5hz` | (10000,) | float32 | 5 Hz with amp+phase noise |
| `noisy_7hz` | (10000,) | float32 | 7 Hz with amp+phase noise |
| `combined_sigma` | (10000,) | float32 | sum of 4 noisy sines |

Plus metadata in the same `.npz`:
- `alpha`, `seed`, `frequencies_hz`, `amplitude`, `sampling_rate_hz`, `duration_seconds`, `code_version`, `config_version`.

### 3.2 Training tuples (DataBundle)
| Field | Shape | Dtype | Meaning |
|---|---|---|---|
| `train.C` | (n_train, 4) | float32 | one-hot selector |
| `train.x` | (n_train, 10) | float32 | window from Σ |
| `train.y` | (n_train, 10) | float32 | matching window from selected pure |
| `val.{C,x,y}` | (n_val, ...) | — | identical schema |
| `test.{C,x,y}` | (n_test, ...) | — | identical schema |

Window starts are **disjoint** across {train, val, test} to prevent leakage.

---

## 4. Setup (Building Block contract)

```
DatasetService
  Input:  alpha (float[0,1]), seed (int)
  Output: (raw_signals: dict, data_bundle: DataBundle)
  Setup:  frequencies_hz, amplitude, sampling_rate_hz, duration_seconds,
          context_window, n_train, n_val, n_test, noise_distribution
```

Composes:
- `SignalGenerator` (Setup: amplitude, fs, duration; Input: freq, phase; Output: 1-D array)
- `NoiseModel` (Setup: rng, distribution; Input: pure signal, alpha; Output: noisy signal)
- `Windower` (Setup: window_size, rng; Input: signal length, n_windows; Output: starts + extracted windows)
- `Splitter` (Setup: rng; Input: signals, starts, one-hots; Output: (C, x, y) tuples)

---

## 5. Performance Metrics

| Metric | Target |
|---|---|
| Wall-clock to generate one dataset (α fixed, seed fixed) | < 5 s on CPU |
| Memory peak | < 100 MB |
| Determinism | Same seed → bitwise identical raw arrays |
| Disk footprint per dataset npz | < 1 MB (float32, 90 KB per array × 9 ≈ 800 KB) |

---

## 6. Constraints

- **Hard**: noise applied per-signal *before* summation (lecturer's explicit instruction). Post-sum noise is forbidden.
- **Hard**: phase noise $\sim \mathcal{U}(0, 2\pi)$, full range, drawn once per realization (not per sample).
- **Hard**: same fixed frequencies $\{1, 3, 5, 7\}$ Hz across all experiments (fair comparison).
- **Hard**: identical dataset (same seed) used across the 3 architectures.
- **Soft**: $\alpha \le 0.20$ recommended; values above produce nearly-destroyed signals (we test up to 0.20).

---

## 7. Alternatives Considered

| Option | Chosen? | Reason |
|---|---|---|
| Gaussian amplitude noise | No (ADR-002) | Uniform is bounded (no fat tails), easier α-sweep semantics. |
| Phase as small jitter | No | Lecturer was explicit: "let the phase go wild" → full $[0, 2\pi]$. |
| Random frequencies per realization | No | Breaks fair-comparison invariant; lecturer fixed the 4 freqs. |
| Post-sum noise (one shared $\eta$) | No | Lecturer was explicit: per-signal, before summation. |
| Window size != 10 | No | Lecturer specified 10. |
| Sliding non-random windows | No (rejected) | Random starts give i.i.d. tuples and reduce leakage between adjacent windows. |
| Same window starts across train/val/test | No | Leakage; we use disjoint starts (Windower.disjoint_starts). |

---

## 8. Success Criteria & Test Scenarios

### 8.1 Success criteria
1. Calling `DatasetService.generate(alpha, seed)` produces 9 raw vectors of length 10 000 and a DataBundle of 5 000+1 000+1 000 tuples in < 5 s on CPU.
2. Same seed → bitwise identical raw vectors and tuples.
3. The FFT spectrum of $\Sigma$ at α=0.05 shows clearly identifiable peaks at 1, 3, 5, 7 Hz (≥ 3 dB above the noise floor in each adjacent bin).
4. With α=0, $\Sigma = \sum_{k} S_k^{\text{pure}}$ exactly (within float32 tolerance).
5. With α > 0, sample mean of `noisy_k - pure_k` is bounded by α·A in absolute value.

### 8.2 Test scenarios
- **Unit**: every helper (SignalGenerator, NoiseModel, Windower, Splitter) tested in isolation per Phase 5 of TODO.
- **Property**: dataset reproducibility (PROP-001), noise statistics (PROP-002), window content (PROP-003).
- **Edge**: α=0 (EDGE-001), α=1 (EDGE-002), n_train=0 (EDGE-005), single-frequency dataset (EDGE-003).
- **Integration**: DatasetService.generate end-to-end (DAT-008..012).
- **Smoke**: `uv run python -m sinusoid_extractor.main generate-data --alpha 0.05` produces a file in `data/raw/`.

### 8.3 Failure modes & responses
| Failure | Response |
|---|---|
| α < 0 | `ValueError("alpha must be in [0, 1]")` |
| α > 1 | warning logged, dataset still generated |
| seed not int | `TypeError` |
| n_train + n_val + n_test > n_windows possible | `ValueError("not enough disjoint windows")` |
| Output dir write fails | `IOError` propagated with clear message |
