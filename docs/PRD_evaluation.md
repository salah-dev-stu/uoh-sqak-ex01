# Per-Mechanism PRD — Evaluation & Sensitivity Analysis

| Field | Value |
|---|---|
| Mechanism | Test-set metrics + OAT sensitivity sweep + reconstruction sampling |
| Owner modules | `src/sinusoid_extractor/services/evaluation_service.py`, `metrics.py`, `plotting.py`, `sweep_service.py` |
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` §3.4–3.5 (FR-EVL, FR-SEN), `PLAN.md`, `TODO.md` Phases 8–9 |

---

## 1. Theoretical Background

### 1.1 Metrics
We report four standard regression metrics on the test set:

- **MSE** — primary loss; comparable across architectures since loss surface is identical.
$$
\text{MSE} = \frac{1}{N \cdot 10}\sum_{n=1}^{N}\sum_{i=1}^{10}(\hat{y}^{(n)}_i - y^{(n)}_i)^2
$$
- **MAE** — robust to outliers, complementary to MSE.
- **R²** — coefficient of determination, normalized goodness-of-fit. Negative R² flags worse-than-mean predictions.
$$
R^2 = 1 - \frac{\sum (\hat{y}-y)^2}{\sum (y - \bar{y})^2}
$$
- **SNR (dB)** — signal-to-noise ratio; physical interpretation:
$$
\text{SNR} = 10\log_{10}\frac{\sum y^2}{\sum (\hat{y}-y)^2}
$$

### 1.2 Stratified evaluation
The test set contains tuples drawn from all 4 target frequencies. We **stratify** metrics per `target_freq_index` (0..3 ↔ 20, 60, 100, 200 Hz) so we can read off per-frequency strengths/weaknesses — central to testing H1 and H2.

### 1.3 Baseline: predict zero
The trivial constant predictor $\hat{y} = \mathbf{0}$ achieves $\text{MSE}_{\text{baseline}} = \mathbb{E}[y^2]$. Any architecture that doesn't beat this is failing.

### 1.4 Sensitivity Analysis (OAT)
**One-At-a-Time** sensitivity: vary each hyperparameter $\theta_j$ over a grid while holding all others at their defaults. Plot $\text{MSE}(θ_j)$ per architecture. OAT misses interactions but is interpretable, fast, and matches the lecturer's recommendation in RULES.md §19.

Sweep grid (PLAN.md §5.1):
- `hidden_size ∈ {64, 128, 256}`
- `num_layers ∈ {1, 2, 3}`
- `dropout ∈ {0.0, 0.2, 0.4}`
- `learning_rate ∈ {1e-4, 1e-3, 1e-2}`

For each (architecture, hyperparam, value) combination → one full train+evaluate run. Total: $4 \cdot 3 \cdot 3 = 36$ runs. With 3 seeds: 108 runs (time permitting).

### 1.5 Hypothesis testing
For each of H1 (RNN > LSTM at 100/200 Hz, multi-cycle) and H2 (LSTM > RNN at 20/60 Hz, sub-cycle):
- Compute paired test (Wilcoxon signed-rank) across per-cell test losses for the architecture pair, paired by (freq, alpha, seed).
- Report the median paired difference and a 95% CI via bootstrap.
- Report effect size (Cohen's $d$ approximation).
- Conclude: confirmed / disconfirmed / inconclusive at α=0.05.

---

## 2. Inputs

### 2.1 `EvaluationService.evaluate`
| Param | Type | Notes |
|---|---|---|
| `run_handle` | `RunHandle` | Pointer to a completed training run |
| `test_loader` | `DataLoader` | Test split |

### 2.2 `SweepService.run_oat_sweep`
| Param | Type | Notes |
|---|---|---|
| `architectures` | list[str] | default from config |
| `seeds` | list[int] | default from config |
| `hyperparams_to_sweep` | dict | from config.oat_sweep |

---

## 3. Outputs

### 3.1 `EvalReport` (dataclass)
| Field | Type | Meaning |
|---|---|---|
| `test_mse` | float | Overall |
| `test_mae` | float | |
| `test_r2` | float | |
| `test_snr_db` | float | |
| `baseline_mse` | float | predict-zero |
| `per_freq_mse` | dict[int, float] | stratified |
| `per_freq_r2` | dict[int, float] | stratified |
| `n_test` | int | |
| `reconstruction_sample` | list[(np.ndarray, np.ndarray)] | 5 (pred, target) pairs |

Persisted as `results/<run_id>/eval_report.json` (numpy arrays sub-saved to `reconstructions.npz`).

### 3.2 `results/sensitivity.csv`
Aggregated columns:
| Column | Type |
|---|---|
| `run_id` | str |
| `architecture` | str |
| `swept_hyperparam` | str |
| `swept_value` | float\|int |
| `seed` | int |
| `test_mse` | float |
| `test_r2` | float |
| `wall_clock_s` | float |
| `epochs_run` | int |

### 3.3 `results/experiment_matrix.csv`
| Column | Type |
|---|---|
| `run_id`, `architecture`, `target_freq_hz`, `noise_alpha`, `seed`, `test_mse`, `test_mae`, `test_r2`, `test_snr_db`, `wall_clock_s`, `epochs_run` |

### 3.4 `results/hypothesis_test.json`
| Field | Type |
|---|---|
| `H1.test` | "wilcoxon" |
| `H1.p_value` | float |
| `H1.median_diff` | float |
| `H1.ci_95` | [float, float] |
| `H1.verdict` | "confirmed" \| "disconfirmed" \| "inconclusive" |
| `H2.*` | same fields |
| `H3.*` | FC vs recurrent, same fields |

### 3.5 Plots → `results/figs/`
| File | Content |
|---|---|
| `loss_curves.png` | Train+val per arch per noise level |
| `mse_heatmap_alpha{α}.png` | Heatmap MSE × (arch, freq) |
| `oat_hidden_size.png` | OAT plot |
| `oat_num_layers.png` | OAT plot |
| `oat_dropout.png` | OAT plot |
| `oat_learning_rate.png` | OAT plot |
| `reconstruction_<arch>_freq{f}.png` | pred vs target windows |

---

## 4. Setup (Building Block contracts)

```
EvaluationService
  Input:  run_handle (RunHandle), test_loader (DataLoader)
  Output: EvalReport
  Setup:  config, device, hooks

SweepService
  Input:  config (full)
  Output: list[RunHandle], aggregated CSVs
  Setup:  training_service, eval_service, paths
```

---

## 5. Performance Metrics (of the evaluation pipeline itself)

| Metric | Target |
|---|---|
| EvalService.evaluate runtime per run | < 5 s (CPU, n_test=1000) |
| Sweep total wall-clock (full matrix + OAT, 3 seeds) | < 6 h on CPU |
| CSV row count = expected sweep cells | exact match |
| All persisted JSONs are valid (parse round-trip) | 100% |
| Plot generation total | < 60 s |

---

## 6. Constraints

- **Hard**: metrics computed on the held-out test set only — never train or val.
- **Hard**: stratification by target frequency is required (else H1/H2 cannot be tested).
- **Hard**: each file ≤ 150 LoC.
- **Hard**: hypothesis tests use **paired** comparison (same data conditions across architectures).
- **Soft**: 3 seeds per cell when time permits; 1 seed per cell minimum.
- **Soft**: bootstrap CI uses 1000 resamples (sufficient for 95% intervals).

---

## 7. Alternatives Considered

| Option | Chosen? | Reason |
|---|---|---|
| Wilcoxon signed-rank for hypothesis test | Yes | Non-parametric; robust to outliers; appropriate for paired ML metrics |
| Paired t-test | No | Assumes normality of differences; weaker on small N |
| Bonferroni correction across H1/H2/H3 | Yes (informal) | Three independent hypotheses; report adjusted p-values |
| Cohen's d for effect size | Yes | Standard, interpretable |
| Sobol indices instead of OAT | No | More informative but expensive; out of scope |
| Sensitivity via partial derivatives (auto-grad) | No | Architecturally interesting but doesn't match the lecturer's "OAT" recommendation |
| Heatmap colormap = `viridis` | Yes | Colorblind-friendly, perceptually uniform |
| Heatmap colormap = `RdBu` | No | Diverging not appropriate (MSE is non-negative) |
| Loss curves on log scale | Yes | Spans 2+ decades; log scale clarifies dynamics |

---

## 8. Success Criteria & Test Scenarios

### 8.1 Success criteria
1. `EvaluationService.evaluate(run, test_loader)` returns `EvalReport` with all fields populated and `test_mse > 0`.
2. Predict-zero baseline computed and reported in every EvalReport.
3. `SweepService.run_oat_sweep()` produces `results/sensitivity.csv` with the expected number of rows.
4. `SweepService.run_experiment_matrix()` produces `results/experiment_matrix.csv` with one row per (arch, freq, alpha, seed).
5. Hypothesis test outputs `verdict ∈ {"confirmed", "disconfirmed", "inconclusive"}` with supporting numerical evidence.
6. All plot files written to `results/figs/` and openable in any viewer.
7. Notebook §5–§7 reads the CSVs and produces all required plots without external state.

### 8.2 Test scenarios
Per TODO Phase 8 (MET-001..020, EV-001..025, PLT-001..015, REC-001..010) and Phase 9 (SW-001..050).

### 8.3 Failure modes
| Failure | Response |
|---|---|
| Test loader empty | `ValueError("test split empty")` |
| Run handle pointing at non-existent dir | `FileNotFoundError` |
| All predictions identical (model collapsed) | report `R² ≤ 0`, log warning, do not crash |
| Sweep interrupted mid-run | resume from CSV (idempotent) |
| Hypothesis test on N < 5 paired samples | report `verdict = "inconclusive"`, log warning |
| Plotting backend missing | fallback to `Agg`, log warning |
