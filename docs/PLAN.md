# Architecture & Technical Plan — Sinusoid Extractor (HW1)

| Field | Value |
|---|---|
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` (root), `TODO.md`, `PRD_dataset.md`, `PRD_fc_model.md`, `PRD_rnn_model.md`, `PRD_lstm_model.md`, `PRD_training_loop.md`, `PRD_evaluation.md` |

---

## 1. Architectural North Star

Layered, SDK-fronted, plugin-friendly. Strictly per RULES.md §5:

```
+--------------------------------------------------------+
| External Consumers (CLI, Jupyter notebook, future GUI) |
+----------------------------+---------------------------+
                             v
+----------------------------+---------------------------+
|              SDK  (sinusoid_extractor.sdk)             |   <- single entry point
|              SinusoidExtractorSDK                      |
+----------------------------+---------------------------+
                             v
+--------------+--------------+--------------+----------+
|  Services    |  Models      |  Shared      |  Const   |
|  - dataset   |  - fc_model  |  - config    |  consts  |
|  - training  |  - rnn_model |  - version   |  enums   |
|  - eval      |  - lstm_model|  - logger    |          |
|  - sweep     |  - registry  |  - gatekeep  |          |
+--------------+--------------+--------------+----------+
                             v
+----------------------------+---------------------------+
|   Infrastructure (filesystem I/O via stdlib + numpy)   |
|   - npz read/write   - json read/write   - results dir |
+----------------------------+---------------------------+
```

External consumers **never** import services or models directly; everything flows through `SinusoidExtractorSDK`. The CLI (`main.py`) is a thin argparse wrapper that calls SDK methods.

---

## 2. C4 Model

### 2.1 Level 1 — System Context

```
        +------------------+
        |   Salah Qadah    |  <-- Submitter (Human)
        |  (researcher)    |
        +--------+---------+
                 |
                 | runs experiments / reads notebook
                 v
       +-------------------+        reads
       |  Sinusoid         | <----------------+
       |  Extractor        |                  |
       |  System           |  writes results  |
       +-------------------+ -----------------+
                 |
                 | depends on (read-only)
                 v
        +------------------+
        |  PyTorch + NumPy |
        |  scientific      |
        |  Python stack    |
        +------------------+

       (No external API; no DB; no cloud service.)
```

### 2.2 Level 2 — Container Diagram

```
   +------------------------------+      +-------------------------------+
   |  CLI Container               |      |  Jupyter Notebook Container   |
   |  python -m sinusoid_extractor|      |  notebooks/analysis.ipynb     |
   |  (argparse + SDK calls)      |      |  (LaTeX + plots + verdicts)   |
   +-------------+----------------+      +---------------+---------------+
                 |                                       |
                 | calls SDK                             | calls SDK
                 v                                       v
   +-----------------------------------------------------------------+
   |   SDK Container  ( src/sinusoid_extractor/sdk/sdk.py )          |
   |   class SinusoidExtractorSDK                                    |
   |     .generate_dataset(...)                                      |
   |     .train_model(arch, hyperparams, dataset_id) -> Run          |
   |     .evaluate(run_id) -> EvalReport                             |
   |     .run_experiment_matrix(...)                                 |
   |     .run_oat_sweep(...)                                         |
   +-----+--------+--------+----------+----------+--------+----------+
         |        |        |          |          |        |
         v        v        v          v          v        v
      Dataset Training Evaluation  Model      Config  Gatekeeper
      Service  Service  Service    Registry   Loader  (no-op stub)
         |        |        |          |          |        |
         |        |        |          |          |        |
         v        v        v          v          v        v
   +-------------------------------------------------------+
   |              Filesystem (data/, results/, config/)    |
   +-------------------------------------------------------+
```

### 2.3 Level 3 — Component Diagram (services)

```
                       SDK
                        |
   +--------------+-----+-----+--------------+----------------+
   |              |           |              |                |
   v              v           v              v                v
DatasetService  TrainingService  EvalService  SweepService  ModelRegistry
   |              |           |              |                |
   |              |           |              |                |
 SignalGen   TrainingLoop  Metrics      OATPlanner       FC/RNN/LSTM
 NoiseModel  Optimizer     Reconstruct  ConfigGrid       (factories)
 Windower    EarlyStop                                   |
 Splitter    LossFn                                      Mixin: ParamCount
 Persister   Hooks                                       Mixin: SaveLoad
```

### 2.4 Level 4 — Code Diagram (selected)

For the dataset service:
```
DatasetService
  __init__(config: DatasetConfig)
  build() -> RawSignals                # 9 vectors
  build_tuples(split: str) -> Tuples   # (C, x, y) batches
  persist(path: Path) -> None
  load(path: Path) -> RawSignals
```

For the model registry:
```
ModelRegistry
  _registry: dict[str, type[BaseExtractor]]
  register(name: str) -> Decorator
  build(name: str, config: ModelConfig) -> BaseExtractor
```

---

## 3. Module / File Layout (mirrors PRD §3.6)

```
src/sinusoid_extractor/
  __init__.py            # __version__, __all__
  constants.py           # PHYSICAL_CONSTANTS, ENUMS, FIXED_FREQUENCIES
  main.py                # CLI entry point (argparse → SDK)
  sdk/
    __init__.py
    sdk.py               # SinusoidExtractorSDK
  services/
    __init__.py
    dataset_service.py
    signal_generator.py
    noise_model.py
    windower.py
    splitter.py
    training_service.py
    training_loop.py
    early_stopping.py
    evaluation_service.py
    metrics.py
    sweep_service.py
  models/
    __init__.py
    base_extractor.py    # ABC + Mixins
    registry.py
    fc_model.py
    rnn_model.py
    lstm_model.py
  shared/
    __init__.py
    config.py            # config loader + schema
    version.py           # __version__ = "1.00"
    logger.py            # structured logging from JSON config
    gatekeeper.py        # API gatekeeper stub (no-op)
    queue_manager.py     # FIFO wave queue stub
    persistence.py       # npz/json/csv I/O helpers
    hooks.py             # lifecycle hook registry

tests/
  unit/
    sdk/test_sdk.py
    services/test_dataset_service.py
    services/test_signal_generator.py
    services/test_noise_model.py
    services/test_windower.py
    services/test_splitter.py
    services/test_training_loop.py
    services/test_early_stopping.py
    services/test_evaluation_service.py
    services/test_metrics.py
    models/test_fc_model.py
    models/test_rnn_model.py
    models/test_lstm_model.py
    models/test_registry.py
    shared/test_config.py
    shared/test_version.py
    shared/test_gatekeeper.py
    shared/test_queue_manager.py
    shared/test_persistence.py
    shared/test_hooks.py
  integration/
    test_end_to_end.py
    test_oat_sweep.py
  conftest.py
```

Every file ≤ 150 LoC (ex. blanks/comments). Long classes are split: data types → `*_types.py`; pure helpers → `*_helpers.py`; orchestration stays in the main file.

---

## 4. Architecture Decision Records (ADRs)

ADRs are stored under `docs/ADRs/`. Summary table:

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | PyTorch over TensorFlow | Accepted |
| ADR-002 | Uniform amplitude noise (vs Gaussian) | Accepted |
| ADR-003 | Concatenate one-hot C at every RNN/LSTM timestep (vs init hidden state) | Accepted |
| ADR-004 | Adam over RMSprop as default optimizer | Accepted |
| ADR-005 | Model registry / factory pattern for plugin extensibility | Accepted |
| ADR-006 | JSON config (vs YAML / TOML) for portability and stdlib parsing | Accepted |
| ADR-007 | Per-architecture seed sweep ≥ 3 seeds for hypothesis testing | Accepted |
| ADR-008 | Wall-clock training budget capped at 30 s/epoch (CPU) | Accepted |
| ADR-009 | `.npz` for raw signals, `.json` for hyperparams + losses, `.csv` for sweeps | Accepted |
| ADR-010 | Lifecycle hooks (`before_train`, `after_epoch`, etc.) for plugin attachment | Accepted |

### ADR-001 — PyTorch over TensorFlow
**Context.** The lecturer's RNN book uses PyTorch idiom (`torch.nn.RNN`); the LSTM book references both, but with PyTorch first. The course community uses PyTorch.
**Decision.** PyTorch.
**Consequences.** Free `torch.nn.RNN` and `torch.nn.LSTM` cells; Adam optimizer first-class; `DataLoader` for parallel data loading. No keras-style symbolic API.

### ADR-002 — Uniform amplitude noise
**Context.** IDEA.md §"Noise" gives free choice between uniform and Gaussian for amplitude noise (it explicitly *requires* uniform [0, 2π] for phase). Uniform is simpler to bound (±α%) and easier to interpret.
**Decision.** Amplitude noise = Uniform(−α·A, +α·A).
**Consequences.** Bounded perturbations (no fat tails); reproducible α-sweep semantics; easier to plot α vs MSE without tail surprises.

### ADR-003 — Concatenate one-hot C at every RNN/LSTM timestep
**Context.** IDEA.md §"How to prepend C" lists three options: as initial hidden state, as input at t=0, or concatenated at every timestep.
**Decision.** Concatenate at every timestep. So RNN/LSTM input dim = 4 + 1 = 5 per timestep (the one-hot plus the current sample from the window).
**Consequences.** Identical conditioning signal at every step (RNN can't "forget" which sine to extract); symmetric with LSTM's behavior; clean parameter accounting.

### ADR-004 — Adam over RMSprop
**Context.** Both are listed in IDEA.md. Adam is the de-facto default in modern DL.
**Decision.** Adam, lr=1e-3.
**Consequences.** Faster convergence on most regression problems; less sensitive to lr tuning; well-tested against RNN/LSTM training quirks.

### ADR-005 — Model registry / factory
**Context.** Rubric §18.5 requires a plugin architecture. We need to dispatch from string name (config) to model class without touching existing code when adding a new arch.
**Decision.** A `ModelRegistry` singleton with a `@register("name")` decorator. New models add themselves at import time.
**Consequences.** Adding a Transformer = `@register("transformer") class TransformerExtractor(...)` in a new file; no edits to existing files.

### ADR-006 — JSON config
**Context.** Lecturer expects JSON (rubric examples show JSON). Stdlib parses JSON natively, no extra dep.
**Decision.** JSON for `setup.json`, `rate_limits.json`, `logging_config.json`.
**Consequences.** No comments in config (stdlib limitation); we use a `_comment` field convention where helpful.

### ADR-007 — ≥3 seeds per data point in OAT
**Context.** Hypothesis testing requires variance estimates. One run per point cannot deliver effect size + CI.
**Decision.** Each base experiment cell (arch × noise × freq) runs ≥3 seeds; OAT points run ≥3 seeds where time allows, otherwise 1 with a note.
**Consequences.** Statistical claims become defensible; runtime budget grows ~3×; mitigated by parallel `DataLoader` and small models.

### ADR-008 — 30 s/epoch CPU budget
**Context.** No GPU. With ~5000 training tuples and batch=64, ~80 batches/epoch.
**Decision.** Cap epoch wall-clock at 30 s; if exceeded, log warning and reduce batch to 32 / hidden to 128.
**Consequences.** Total experiment matrix bounded ≈ (12 base + 36 OAT) × 80 epochs × 30 s ≈ 32 h — reduced by early stopping (median 30–40 epochs) and small model size to a realistic ~6 h.

### ADR-009 — Persistence formats
**Decision.** `.npz` for arrays, `.json` for metadata/losses, `.csv` for tabular sweep results.
**Consequences.** Notebook can `pandas.read_csv()` directly; `numpy.load()` for arrays; `json.load()` for metadata.

### ADR-010 — Lifecycle hooks
**Decision.** `TrainingLoop` exposes `register_hook(event: str, fn: Callable)`. Events: `before_train`, `after_epoch`, `after_train`, `before_evaluate`, `after_evaluate`.
**Consequences.** Plugins can log custom metrics or save extra artifacts without modifying core. Tested via a no-op test plugin in `tests/`.

---

## 5. Data Schemas

### 5.1 Config schema (`config/setup.json`)

```json
{
  "version": "1.00",
  "_comment": "Project-wide config. Bump version on any change.",
  "dataset": {
    "frequencies_hz": [1, 3, 5, 7],
    "amplitude": 1.0,
    "sampling_rate_hz": 1000,
    "duration_seconds": 10,
    "context_window": 10,
    "n_train": 5000,
    "n_val": 1000,
    "n_test": 1000,
    "seed": 42,
    "noise_levels_alpha": [0.01, 0.05, 0.10, 0.20]
  },
  "training": {
    "optimizer": "adam",
    "learning_rate": 0.001,
    "batch_size": 64,
    "max_epochs": 80,
    "early_stopping_patience": 10,
    "num_workers": 2
  },
  "models": {
    "fc":   { "hidden_size": 128, "num_layers": 2, "dropout": 0.2 },
    "rnn":  { "hidden_size": 128, "num_layers": 1, "dropout": 0.0 },
    "lstm": { "hidden_size": 128, "num_layers": 1, "dropout": 0.2 }
  },
  "experiment": {
    "seeds": [42, 123, 7],
    "architectures": ["fc", "rnn", "lstm"],
    "target_frequency_indices": [0, 1, 2, 3]
  },
  "oat_sweep": {
    "hidden_size": [64, 128, 256],
    "num_layers": [1, 2, 3],
    "dropout": [0.0, 0.2, 0.4],
    "learning_rate": [0.0001, 0.001, 0.01]
  },
  "paths": {
    "data_dir": "data/",
    "results_dir": "results/",
    "logs_dir": "logs/"
  }
}
```

### 5.2 Rate-limits schema (`config/rate_limits.json`)
HW1 has no external APIs but the structure is mandatory:
```json
{
  "version": "1.00",
  "_comment": "No external APIs in HW1. Structure preserved per RULES.md §7.",
  "services": {
    "default": {
      "requests_per_minute": 30,
      "requests_per_hour": 500,
      "concurrent_max": 5,
      "retry_after_seconds": 30,
      "max_retries": 3
    }
  }
}
```

### 5.3 Run-result schema (`results/<run_id>/loss_history.json`)
```json
{
  "run_id": "fc_freq3_alpha10_seed42_2026-05-06T12:34",
  "config_version": "1.00",
  "code_version": "1.00",
  "architecture": "fc",
  "target_frequency_hz": 3,
  "noise_alpha": 0.10,
  "seed": 42,
  "hyperparams": { "hidden_size": 128, "num_layers": 2, "dropout": 0.2, "lr": 0.001, "batch_size": 64 },
  "param_count": 8714,
  "epochs_run": 47,
  "wall_clock_seconds": 312.4,
  "train_loss_per_epoch": [/* ... */],
  "val_loss_per_epoch": [/* ... */],
  "test_loss": 0.0143
}
```

### 5.4 Sensitivity sweep aggregate (`results/sensitivity.csv`)
| run_id | architecture | hyperparam_swept | swept_value | seed | test_loss | epochs_run | wall_clock_s |
|---|---|---|---|---|---|---|---|

---

## 6. Public Interfaces (Contracts)

### 6.1 `SinusoidExtractorSDK`

```python
class SinusoidExtractorSDK:
    def __init__(self, config_path: Path | None = None) -> None: ...

    # Dataset
    def generate_dataset(self, alpha: float, seed: int | None = None) -> DatasetHandle: ...
    def load_dataset(self, handle: DatasetHandle) -> DataBundle: ...

    # Training
    def train_model(
        self, arch: str, dataset: DataBundle, hyperparams: dict | None = None, seed: int | None = None
    ) -> RunHandle: ...

    # Evaluation
    def evaluate(self, run: RunHandle, dataset: DataBundle) -> EvalReport: ...

    # Experiments
    def run_experiment_matrix(self) -> list[RunHandle]: ...
    def run_oat_sweep(self) -> list[RunHandle]: ...

    # Plumbing
    def get_version(self) -> str: ...
    def get_config(self) -> dict: ...
```

### 6.2 `BaseExtractor` (abstract)

```python
class BaseExtractor(nn.Module, ParamCountMixin, SaveLoadMixin):
    INPUT_DIM: ClassVar[int] = 14
    OUTPUT_DIM: ClassVar[int] = 10
    def forward(self, batch: BatchInput) -> torch.Tensor: ...
```

`ParamCountMixin.count_parameters() -> int` and `SaveLoadMixin.save(path) / load(path)` are shared across all three model classes.

---

## 7. ISO/IEC 25010 Quality Attributes — Full Treatment

Per RULES.md §18.6:

1. **Functional Suitability**
   - *Completeness*: every FR-* in PRD has at least one acceptance test in `tests/`.
   - *Correctness*: dataset-generation properties are property-tested (window selection, one-hot validity, noise bounds); model forward shapes are unit-tested.
   - *Appropriateness*: SDK methods map 1:1 to user-stories US-1 through US-5.

2. **Performance Efficiency**
   - *Time behavior*: ADR-008 caps epoch at 30 s on CPU; benchmark in `tests/integration/test_end_to_end.py` asserts 1-epoch FC under 5 s.
   - *Resource utilization*: model parameter counts kept under 250 K; total RAM under 500 MB at default config.
   - *Capacity*: dataset of 7 000 tuples × 14-dim input fits comfortably in memory.

3. **Compatibility**
   - *Co-existence*: pure-Python deps; `uv` lock isolates from system Python.
   - *Interoperability*: outputs are NumPy/CSV/JSON, readable by any tool.

4. **Usability**
   - *Learnability*: README walkthrough + worked notebook.
   - *Operability*: single CLI command does end-to-end; flags use sensible defaults from config.
   - *User error protection*: argparse validation + config schema check at startup; bad config exits with explicit error.
   - *Accessibility*: plot color palette uses the seaborn `colorblind` palette; high-contrast for projector/print.

5. **Reliability**
   - *Maturity*: tests cover happy path + edge cases (empty windows, alpha=0, alpha=1).
   - *Availability*: stateless (no daemon); always-on by definition.
   - *Fault tolerance*: training loop catches NaN loss and aborts the run with a clear error rather than silently producing garbage.
   - *Recoverability*: each run is atomic — partial results are not persisted; final write only after success.

6. **Security**
   - *Confidentiality*: no secrets, no PII.
   - *Integrity*: configs versioned + checksum-printed at run start.
   - *Authenticity*: not applicable (no auth).
   - *Accountability*: every run logs to `results/<run_id>/run.log` with timestamps.

7. **Maintainability**
   - *Modularity*: 4 layers (SDK / services / models / shared) with strict directional imports.
   - *Reusability*: mixins for parameter counting and save/load are shared by all model classes.
   - *Analyzability*: structured logging, full docstrings, type hints throughout.
   - *Modifiability*: model registry + lifecycle hooks support plugins without core edits.
   - *Testability*: dependency injection in services; mocks used for I/O in unit tests.

8. **Portability**
   - *Adaptability*: only `torch` and stdlib; no platform-specific code.
   - *Installability*: `uv sync` is the entire install procedure.
   - *Replaceability*: any of FC/RNN/LSTM can be swapped via the registry; backend (PyTorch) is hidden behind `BaseExtractor`.

---

## 8. Parallel Processing Strategy (RULES.md §18.7)

| Where | Mechanism | Rationale |
|---|---|---|
| Data loading | `torch.utils.data.DataLoader(num_workers=N)` | I/O-bound (NumPy → tensor); multiprocessing under the hood. |
| Experiment matrix | Sequential per-run, parallel-over-seed within a single run is **not** used (CPU-bound, single core saturates). | Avoid over-subscription; keep result attribution clean. |
| Sweep orchestration | Sequential | Determinism; reproducible result CSV. |

Thread safety: no shared mutable state across runs; each `RunHandle` writes to its own directory.

---

## 9. Extension Architecture (RULES.md §18.5)

- **Plugins**: `ModelRegistry` accepts new `BaseExtractor` subclasses via `@register("name")` at import time. Drop a `transformer_model.py` in `src/sinusoid_extractor/models/` and add to `__init__.py` to enable.
- **Lifecycle hooks**: `TrainingLoop.register_hook(event, fn)` — events `before_train`, `after_epoch`, `after_train`, `before_evaluate`, `after_evaluate`. Plugins attach without modifying core.
- **API-first**: every service exposes a tight interface (`generate`, `train`, `evaluate`); the SDK is the single integration surface.

---

## 10. Building-Blocks Design (RULES.md §18.8)

Each significant component declares Input / Output / Setup. Examples:

```
DatasetService
  Input:  alpha (float in [0,1]), seed (int), n_train/n_val/n_test (int)
  Output: DataBundle (train/val/test tensors of (C, x, y))
  Setup:  frequencies_hz, amplitude, sampling_rate_hz, duration_seconds, context_window
```

```
TrainingLoop
  Input:  model (BaseExtractor), train_loader, val_loader, hooks (list)
  Output: TrainingResult (loss_history, best_state_dict, epochs_run, wall_clock_s)
  Setup:  optimizer, learning_rate, max_epochs, early_stopping_patience
```

```
EvaluationService
  Input:  trained_model (BaseExtractor), test_loader, target_frequency_hz, alpha
  Output: EvalReport (test_mse, residuals, predictions_sample)
  Setup:  device, batch_size
```

Every block is independently testable via dependency injection.

---

## 11. Verification Strategy

1. **Unit tests** — every public function/class. Run by `uv run pytest tests/unit/`.
2. **Integration tests** — end-to-end at tiny scale (200 train / 50 val / 50 test, 3 epochs). Asserts SDK pipeline runs and produces expected artifacts.
3. **Lint** — `uv run ruff check src/ tests/` returns 0.
4. **Coverage** — `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=85`.
5. **File-size check** — `uv run python scripts/check_file_lines.py` exits 0 only if every `.py` ≤ 150 LoC (excluding blanks/comments).
6. **Secret scan** — `git grep -nE '(api_key|secret|password|token)\s*=\s*["\047]'` returns empty.
7. **Notebook smoke test** — `uv run jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb` returns 0.

CI (if added later): a single `make ci` target chains all 7.

---

## 12. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Training too slow on CPU | Medium | High | Small model sizes (≤ 256 hidden), batch=64, early stopping |
| Tests flaky due to RNG | Low | Medium | Seed every test; use deterministic ops |
| 150-LoC limit tightens unexpectedly | Medium | Medium | Plan splits up front; helper modules per service |
| Hypothesis disconfirmed (RNN ≯ LSTM at high freq) | Medium | Low | Lecturer values *analysis*, not the result; report honestly |
| `uv` install fails on macOS arm64 | Low | High | Test `uv sync` first thing on day 1 |
| GitHub repo creation needs auth | Medium | Low | `gh auth login` before push; user already has gh installed |
| Notebook LaTeX render fails | Low | Medium | Use MathJax (browser) instead of MikTeX for portability |
| 800-task TODO seems excessive | Low | Low | Lecturer slide says 300–800; we target 800+ with sub-task granularity |

---

## 13. Approval

This Plan is the **second deliverable** in the Vibe Coding Lifecycle. Approving it commits to:
- the SDK + services + models + shared layering,
- the 10 ADRs,
- the config schema in §5,
- the verification strategy in §11.

Next document: `docs/TODO.md` (≥800 tasks).
