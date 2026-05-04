# Product Requirements Document — Sinusoid Extractor (HW1)

| Field | Value |
|---|---|
| Project name | `sinusoid-extractor` |
| Course | 203.3763 — Orchestration of AI Agents (תשפ"ו, semester ב), University of Haifa |
| Lecturer | Dr. Yoram Reuven Segal — `rmisegal@gmail.com` |
| Submitter | Salah Qadah / סלאח קדח (ID 323039974) |
| Group code | <!-- TBD: confirm before submission, placeholder `uoh-sk01` --> |
| Solo / pair | <!-- TBD: confirm before submission. If solo, lecturer permission must be obtained via email --> |
| GitHub | `https://github.com/salah-dev-stu/sinusoid-extractor` (public; shared with `rmisegal@gmail.com`) |
| Self-grade target | <!-- TBD: re-calibrate at submission, placeholder 92 --> |
| Deadline | 2026-05-07 23:59 (late penalty −5 pts / 24 h) |
| Document version | 1.00 |
| Last updated | 2026-05-04 |

---

## 1. Project Overview & Context

### 1.1 The user problem
Given a noisy time-domain signal that is the **sum of multiple pure sinusoids** at known fixed frequencies, can a small neural network learn to **extract one chosen pure sinusoid** from the mixture? This is a regression problem with a strong physical structure (the underlying components are deterministic; the corruption is per-component noise on amplitude and phase).

The task mirrors a recurring real-world need: source separation in audio, vibration analysis in mechanical systems, narrowband signal isolation in communications. We strip the problem down to a controlled synthetic setting so that we can compare three neural architectures on **identical** data and isolate the architectural effect.

### 1.2 Context
The course "Orchestration of AI Agents" covers the full lifecycle of building production-grade ML/AI systems with AI assistants. HW1 is the **introductory deep-learning assignment**: it forces hands-on familiarity with the canonical sequence-modelling triple (FC baseline, vanilla RNN, LSTM) under strict engineering discipline (SDK architecture, ≤150 LoC per file, ≥85% coverage, ruff-clean, `uv`-only, continuous git history).

### 1.3 Target audience
- **Primary**: Dr. Yoram Segal and his automated grading agent.
- **Secondary**: future students of the course (the README and notebook serve as a worked reference example).
- **Tertiary**: the submitter's own future self — the project is structured to be a portfolio piece.

### 1.4 Market / prior art
PyTorch's own examples include `torch.nn.RNN` and `torch.nn.LSTM` toy regression demos. The lecturer's own demo, the "Sinusoid Explorer" web app at `https://manus.im/app/dxz7lOSiBBgU5Rtl6oJlmm`, demonstrates the visual UX inspiration (per-sine sliders, FFT spectrum tab). This project does not duplicate the web-app UI; it focuses on the **comparative ML analysis** the lecturer's hypothesis demands.

---

## 2. Goals & Success Metrics

### 2.1 Primary goal
Empirically test the lecturer's hypothesis:
- **H1**: RNN extracts **high-frequency** sines (5 Hz, 7 Hz) better than LSTM, because its short effective context matches the rapid oscillation.
- **H2**: LSTM extracts **low-frequency** sines (1 Hz, 3 Hz) better than RNN, because its cell state preserves long-range structure.
- **H3**: FC sits as a baseline below both, lacking any temporal mechanism.

### 2.2 Secondary goals
- Demonstrate sensitivity of each architecture to noise level α and to standard hyperparameters (hidden size, # layers, dropout, learning rate).
- Produce a publishable-quality Jupyter notebook with LaTeX equations and OAT (One-At-a-Time) sensitivity analysis.
- Ship a clean, testable, configurable codebase that exemplifies the lecturer's engineering rubric.

### 2.3 Success metrics (KPIs)
| KPI | Target | Measured by |
|---|---|---|
| H1 verdict | Statistically defensible answer (with effect size and confidence interval) on whether RNN > LSTM at 5/7 Hz | Notebook §7 |
| H2 verdict | Same, for LSTM > RNN at 1/3 Hz | Notebook §7 |
| H3 verdict | Same, for FC vs. recurrent pair across all frequencies | Notebook §7 |
| Reconstruction MSE | Best architecture must beat the "predict zero" baseline by ≥ 10× MSE on at least one (target_freq, noise) configuration | Eval script |
| Coverage | ≥ 85% statement coverage globally | `uv run pytest --cov` |
| Lint cleanliness | `uv run ruff check` returns 0 errors | ruff |
| File-size compliance | 100% of `*.py` under 150 lines (excluding blanks/comments) | `scripts/check_file_lines.py` |
| Continuous commit cadence | ≥ 1 commit per major TODO milestone (target ≥ 50 commits) | `git log` |

### 2.4 Acceptance criteria
- All three networks train to completion on the agreed hyperparameter sweep within the timeline.
- Notebook contains every section enumerated in §6 below.
- Submission PDF (`<group_code>-ex01.pdf`) is generated from `uoh-rl07-ex01.docx` with all fields filled.
- GitHub repo is public, shared with `rmisegal@gmail.com`, and contains the full project + `uv.lock`.
- A submission checklist (in `docs/SUBMISSION_CHECKLIST.md`) is fully ticked before upload to Moodle.

---

## 3. Functional Requirements

### 3.1 Dataset generation (FR-DAT)
- **FR-DAT-1**: Generate 4 pure sine signals at fixed frequencies F ∈ {1, 3, 5, 7} Hz, sampled at Fs = 1000 Hz over T = 10 s (N = 10 000 samples per signal).
- **FR-DAT-2**: For each signal, also generate a noisy version with (i) amplitude noise of ±α% around amplitude A, distribution = uniform (documented choice; Gaussian considered, see ADR-002 in PLAN.md), and (ii) phase noise drawn from Uniform(0, 2π) — **the full range, not a small jitter**.
- **FR-DAT-3**: Compute the combined noisy signal `Σ` as the **sum of the 4 noisy sines** (noise applied per-signal *before* summation — never post-sum).
- **FR-DAT-4**: Persist 4 pure + 4 noisy + 1 combined = **9 vectors of 10 000 samples** to `data/raw/` in NumPy `.npz` format with metadata.
- **FR-DAT-5**: From these vectors, produce training tuples `(C, x, y)`:
  - `C ∈ {0,1}^4` is a one-hot selecting the target sine
  - `x ∈ ℝ^10` is a 10-sample window from `Σ` (random start position)
  - `y ∈ ℝ^10` is the same window from the *pure* version of the sine selected by `C`
- **FR-DAT-6**: Default split: 5 000 train / 1 000 val / 1 000 test tuples (configurable via `config/setup.json`). All splits drawn from the same underlying 9 vectors but with disjoint window-start indices to prevent leakage.
- **FR-DAT-7**: Random seed is fixed (default 42, configurable) for full reproducibility.
- **FR-DAT-8**: A separate "noise sweep" dataset family exists for α ∈ {1%, 5%, 10%, 20%} (configurable) so that all 3 architectures train on **the same 4 noise variants**.

### 3.2 Model architectures (FR-MOD)
- **FR-MOD-1**: All three networks share the same input/output contract: input dim = 4 (one-hot) + 10 (window) = **14**; output dim = **10**.
- **FR-MOD-2**: **FC** — input → Linear → ReLU → Dropout → Linear → ReLU → Dropout → Linear (output). 2–3 hidden layers, hidden size 128 or 256 (configurable). Linear activation on output.
- **FR-MOD-3**: **RNN** — vanilla `torch.nn.RNN` with `tanh` nonlinearity. Process the 10-sample window as a sequence of 10 timesteps. The one-hot `C` is concatenated to the input at every timestep (chosen for symmetry with LSTM; alternatives in ADR-003). 1–3 layers, hidden 128 or 256. Final hidden state → Linear → 10-sample output.
- **FR-MOD-4**: **LSTM** — `torch.nn.LSTM` with the standard 4 gates (forget, input, candidate, output). Same C-concatenation strategy as RNN. 1–3 layers, hidden 128 or 256, dropout 0.2–0.5 between layers. Final hidden state → Linear → 10-sample output.
- **FR-MOD-5**: A **model registry / factory** dispatches name → class so a new architecture (Transformer, GRU) could be added by registration alone — no edits to existing files. Satisfies "Plugins Architecture" from the rubric (RULES.md §18.5).

### 3.3 Training loop (FR-TRN)
- **FR-TRN-1**: Loss = Mean Squared Error summed across the 10-sample output window (per the lecturer's `Total Loss = L_1 + … + L_10` instruction).
- **FR-TRN-2**: Optimizer = Adam (default) or RMSprop (configurable), with configurable learning rate (default 1e-3).
- **FR-TRN-3**: Batch size default 64 (configurable), epochs default 80 with **early stopping** on validation loss (patience configurable, default 10).
- **FR-TRN-4**: Train, validation, and test losses are recorded per-epoch and persisted to `results/<run_id>/loss_history.json` along with wall-clock time and parameter count.
- **FR-TRN-5**: Lifecycle hooks (`before_train`, `after_epoch`, `after_train`, `before_evaluate`, `after_evaluate`) are exposed by the trainer so plugins can attach without modifying core code (rubric §18.5).
- **FR-TRN-6**: PyTorch `DataLoader(num_workers=N)` is used for parallel data loading; `N` is a config parameter (default 2). Satisfies parallel-processing requirement (RULES.md §18.7).

### 3.4 Evaluation (FR-EVL)
- **FR-EVL-1**: Compute test MSE for each (architecture × target_freq × noise_level) combination, plus per-test-tuple residuals.
- **FR-EVL-2**: Generate reconstruction plots: predicted vs. ground-truth windows for representative test examples.
- **FR-EVL-3**: Generate a heatmap of MSE over (architecture, target_freq) at each noise level.
- **FR-EVL-4**: Persist all eval artifacts to `results/<run_id>/`.

### 3.5 Sensitivity analysis (FR-SEN)
- **FR-SEN-1**: One-At-a-Time (OAT) sweep over: hidden size {64, 128, 256}, # layers {1, 2, 3}, dropout {0.0, 0.2, 0.4}, learning rate {1e-4, 1e-3, 1e-2}, while holding all other knobs at their defaults.
- **FR-SEN-2**: Each OAT point is a full train+evaluate run; all results are aggregated into a single `results/sensitivity.csv`.
- **FR-SEN-3**: Notebook §6 visualizes OAT effects per architecture as line plots with error bars (std over ≥ 3 seeds per point, time permitting).

### 3.6 Public SDK (FR-SDK)
- **FR-SDK-1**: All business logic is exposed via a single `SinusoidExtractorSDK` class (RULES.md §1, §5). External consumers (CLI, notebook, future GUI/REST) call **only** SDK methods, never internal services directly.
- **FR-SDK-2**: SDK methods at minimum: `generate_dataset(...)`, `train_model(arch, hyperparams, dataset)`, `evaluate(model, dataset)`, `run_oat_sweep(...)`, `load_config(path)`.
- **FR-SDK-3**: A thin CLI (`sinusoid_extractor.main`) is the only `__main__` entry point; it parses args and delegates to SDK calls.

### 3.7 Configuration (FR-CFG)
- **FR-CFG-1**: All tunable values live in `config/setup.json` (versioned, starts at `1.00`).
- **FR-CFG-2**: Rate-limit slot exists at `config/rate_limits.json` (versioned, starts at `1.00`); it is unused by HW1 (no external APIs) but the structure is mandatory per RULES.md §7.
- **FR-CFG-3**: Logging config in `config/logging_config.json`.
- **FR-CFG-4**: At startup, code version (`src/sinusoid_extractor/shared/version.py`) is checked against config version for compatibility (warn-on-mismatch).

### 3.8 Notebook (FR-NB)
- **FR-NB-1**: `notebooks/analysis.ipynb` exists and runs end-to-end on the artifacts in `results/`.
- **FR-NB-2**: All math expressed in LaTeX via `$ ... $` and `\begin{align} ... \end{align}`.
- **FR-NB-3**: Sections (mandatory order): Setup → Dataset visualization → Model architectures → Training → Evaluation → Sensitivity analysis → Hypothesis test → Conclusion.

---

## 4. Non-Functional Requirements

### 4.1 Hard rules from the grading rubric (RULES.md, Table 5)
| # | Rule | Threshold | Enforcement |
|---|---|---|---|
| NFR-1 | SDK architecture | All business logic via SDK layer | Code review |
| NFR-2 | OOP / no duplication | Anything used 2+ times extracted (base class / mixin / Template Method) | Code review |
| NFR-3 | API Gatekeeper | Centralized class for any external API (no-op for HW1, structure must exist) | Code review |
| NFR-4 | Rate limits in JSON, not code | `config/rate_limits.json` versioned | Config test |
| NFR-5 | Wave queue / FIFO backpressure | Stub structure exists | Integration test |
| NFR-6 | Versioning | Code & config start at `1.00`, +0.01 per change | Version module |
| NFR-7 | TDD | RED → GREEN → REFACTOR; tests written with code | Process |
| NFR-8 | File size | ≤ 150 LoC/file (no blanks/comments counted) | `scripts/check_file_lines.py` |
| NFR-9 | Linter | `uv run ruff check` → 0 errors | ruff |
| NFR-10 | Coverage | `uv run pytest --cov` ≥ 85% (`fail_under = 85`) | pytest |
| NFR-11 | No hardcoded values | All tunables via config / constants / Enum | Code review |
| NFR-12 | No secrets in code | `.env-example` + `os.environ.get(...)`; `.env` git-ignored | Auto scan |
| NFR-13 | `uv` only | No pip / venv / virtualenv / `python -m`; everything via `uv run`/`uv sync`/`uv add`/`uv lock` | Auto |

### 4.2 Quality (ISO/IEC 25010, summary — full treatment in PLAN.md)
1. **Functional Suitability** — every functional requirement above is acceptance-tested.
2. **Performance Efficiency** — `DataLoader` with `num_workers`; FC ≤ 5 s / epoch on CPU, RNN/LSTM ≤ 30 s / epoch on CPU at default hyperparams.
3. **Compatibility** — pure Python 3.10+; runs on macOS, Linux, WSL.
4. **Usability** — single CLI entry point, README with worked examples, notebook is self-contained.
5. **Reliability** — fixed seeds, deterministic ops where possible, graceful CLI errors.
6. **Security** — no secrets, no remote calls; `.gitignore` shields env/keys.
7. **Maintainability** — SDK + services + models split; ≤ 150 LoC files; coverage ≥ 85%; ruff-clean.
8. **Portability** — `uv`-managed deps, `uv.lock` tracked; no platform-specific code.

### 4.3 Engineering process
- **Continuous git commits** — at least one meaningful commit per major TODO milestone, target ≥ 50 commits across the project life. One single end-of-project push is heavily penalized (RULES.md §16).
- **Prompt log** — every prompt used to drive code generation is recorded in `docs/PROMPTS.md` with context / goal / strategy notes (RULES.md §17).
- **Per-mechanism PRDs** — each significant component (dataset, FC, RNN, LSTM, training loop, evaluation) has its own `PRD_<name>.md` under `docs/`.
- **TODO scale** — `docs/TODO.md` will contain ≥ 800 tasks (lecturer slide says 300–800; we target the high end for the 92+ quality bar).

---

## 5. User Stories & Use Cases

### 5.1 Primary user stories
- **US-1** — *As the grading agent*, I run `uv sync && uv run pytest --cov && uv run ruff check` and observe coverage ≥ 85%, 0 ruff errors, all tests green.
- **US-2** — *As Dr. Segal*, I open `notebooks/analysis.ipynb` and read a self-contained narrative answering H1/H2/H3 with plots, equations, and a reflective conclusion.
- **US-3** — *As Dr. Segal*, I clone the repo and run `uv run python -m sinusoid_extractor.main run-experiment --config config/setup.json` and the full pipeline (data → train → eval → save) executes end-to-end.
- **US-4** — *As a future student*, I read `README.md` and can install, configure, run, and extend the project without consulting external docs.
- **US-5** — *As a future maintainer*, I add a Transformer model by writing one new file under `src/sinusoid_extractor/models/` and registering it — no edits to existing files.

### 5.2 Use cases
- **UC-1**: Generate the dataset once, persist to `data/`, reuse across all training runs.
- **UC-2**: Train the three architectures across 4 noise levels (12 runs) and persist all loss curves + final test MSE.
- **UC-3**: Run the OAT sweep (4 hyperparams × 3 values × 3 architectures = 36 additional runs) and aggregate to `results/sensitivity.csv`.
- **UC-4**: Render the notebook end-to-end from `results/`, export to PDF/HTML for inclusion in submission artifacts.

---

## 6. Notebook Specification (Jupyter)

The notebook is **half the grade** (lecturer). Sections (in order):

1. **Setup** — imports, seed, configuration loaded from `config/setup.json` (no duplicate values).
2. **Dataset visualization**
   - Time-domain plots of each pure sine
   - Time-domain plots of each noisy sine
   - The combined Σ signal
   - **FFT spectrum of Σ** confirming the 4 frequency peaks are recoverable
3. **Model architectures** — narrative + diagrams + LaTeX equations:
   - FC: $y = W_2 \cdot \text{ReLU}(W_1 x + b_1) + b_2$
   - RNN: $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
   - LSTM: standard 4-gate equations (forget / input / candidate / output / cell update / hidden update)
4. **Training** — loss curves (train + val) per architecture per noise level; wall-clock time and parameter count.
5. **Evaluation** — heatmap MSE × (arch, target_freq) per noise level; reconstruction plots.
6. **Sensitivity Analysis (OAT)** — line plots per hyperparameter per architecture.
7. **Hypothesis test** — quantitative answers to H1/H2/H3 with effect sizes and confidence intervals (paired tests across seeds where possible).
8. **Conclusion** — what worked, what surprised, what to try next. Reflective tone (lecturer values analysis over success).

---

## 7. Constraints

| Type | Constraint |
|---|---|
| Time | Hard deadline 2026-05-07 23:59 (3 days from project start). |
| Hardware | macOS laptop, CPU-only training (no GPU assumed). |
| Framework | PyTorch (per IDEA.md). No TensorFlow / JAX / Keras. |
| Package manager | `uv` exclusively. No `pip`, `venv`, `virtualenv`, `python -m`. |
| Lint | `ruff` rules `E,F,W,I,N,UP,B,C4,SIM`, ignore `E501`, line-length 100, target `py310`. |
| File size | ≤ 150 LoC per `*.py` file (no whitespace games). |
| Test coverage | ≥ 85%, `fail_under = 85` in `pyproject.toml`. |
| Repo visibility | **Public** GitHub repo (lecturer slide), shared with `rmisegal@gmail.com`. |
| Disk | Generated `data/` may be git-ignored if large; small NPZ artifacts are tracked for reproducibility. |
| AI policy | Per syllabus, Gen-AI use must be reported. Prompt log at `docs/PROMPTS.md` and acknowledgment paragraph in `README.md`. |

---

## 8. Dependencies

### 8.1 Runtime (Python, via `uv add`)
- `python>=3.10`
- `torch` — neural networks
- `numpy` — array ops
- `matplotlib`, `seaborn` — plots
- `jupyter` — notebook
- `pydantic` (or `dataclasses`) — config schema validation
- `python-dotenv` — env var loading

### 8.2 Dev (via `uv add --dev`)
- `pytest`, `pytest-cov`
- `ruff`
- `ipykernel`

### 8.3 External
- `git` + GitHub (public repo, shared with `rmisegal@gmail.com`)
- LaTeX renderer for the notebook (MikTeX / TeX Live / browser MathJax — MathJax suffices)
- Moodle (submission portal)

---

## 9. Out of Scope

- Real audio data; this is a synthetic-only exercise.
- GPU-specific code paths or distributed training.
- Production REST API (the SDK is API-shaped but no HTTP server is built).
- A web UI (the lecturer's "Sinusoid Explorer" demo is inspiration, not a deliverable).
- Hyperparameter optimization beyond OAT (no Bayesian search, no grid search).
- Models beyond the required three (Transformer / GRU stubs may be present in the registry as extensibility examples but are not trained).

---

## 10. Timeline & Milestones

| Day | Date | Milestone | Definition of Done |
|---|---|---|---|
| 0 | 2026-05-04 | PRD + PLAN + TODO + per-mechanism PRDs | All four `docs/` files written, user-approved, committed |
| 1 | 2026-05-05 AM | Repo scaffolding + first green tests | `uv sync`, ruff 0, pytest green on stub tests, first 5–10 commits |
| 1 | 2026-05-05 PM | Dataset service + tests | FR-DAT-1..8 satisfied, dataset persisted, tests pass |
| 1 | 2026-05-05 EOD | All 3 model classes + tests | FR-MOD-1..5 satisfied, registry working |
| 2 | 2026-05-06 AM | Training service + evaluation service + tests | FR-TRN-1..6, FR-EVL-1..4 satisfied |
| 2 | 2026-05-06 PM | First full experiment matrix run | 12 base runs + 36 OAT runs in `results/` |
| 2 | 2026-05-06 EOD | Notebook draft | All 8 sections present with at least placeholder content |
| 3 | 2026-05-07 AM | Notebook polish + README + submission PDF | Full LaTeX equations, hypothesis verdicts, reflective conclusion; README at user-manual depth |
| 3 | 2026-05-07 PM | Submission | PDF uploaded to Moodle, repo public + shared, all TBDs resolved |

Late penalty −5 pts / 24 h. We have **zero buffer** — any blocker must be surfaced immediately.

---

## 11. Approval

This PRD is the **first deliverable** in the Vibe Coding Lifecycle.

By approving this document, the user commits to:
- the technical decisions in §3 (dataset spec, model architectures, training loop),
- the success metrics in §2.3 and acceptance criteria in §2.4,
- the timeline in §10,
- proceeding to draft `docs/PLAN.md` next.

Open items requiring user action **before submission** (TBDs):
- [ ] Confirm group code (placeholder `uoh-sk01`)
- [ ] Confirm solo / pair status; if solo, send permission email to `rmisegal@gmail.com`
- [ ] Confirm self-grade (placeholder `92`)
