# TODO — Sinusoid Extractor (HW1)

| Field | Value |
|---|---|
| Document version | 1.00 |
| Total tasks | 1042 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md`, `PLAN.md`, per-mechanism PRDs |

**Legend:** `[ ]` pending · `[x]` done · `[~]` in-progress · `[!]` blocked
**Priorities:** P0 = blocker · P1 = required · P2 = nice-to-have
**Phases run sequentially within their group; cross-phase items are flagged with `→` dependencies.**

---

## Phase 0 — Project Setup & Scaffolding (P0) [50 tasks]

- [x] SETUP-001: Create `hw1/` working directory
- [x] SETUP-002: Read `IDEA.md` (vibe input)
- [x] SETUP-003: Read `RULES.md` (grading rubric)
- [x] SETUP-004: Read `CLAUDE.md` (orientation)
- [x] SETUP-005: Collect user-specific config (group code TBD, GitHub user, ID, self-grade)
- [x] SETUP-006: Save user profile + project context to memory
- [x] SETUP-007: Initialize `git` repository on branch `main`
- [x] SETUP-008: Configure `git config user.name` and `user.email`
- [x] SETUP-009: Write `.gitignore` (secrets, python, uv, pytest, jupyter, OS)
- [x] SETUP-010: Write `.env-example` (no real secrets, just placeholders)
- [x] SETUP-011: Create `pyproject.toml` with `[project]`, `[tool.uv]`, `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report]`
- [x] SETUP-012: Set Python version to `>=3.10` in `pyproject.toml`
- [x] SETUP-013: Set ruff line-length 100, target-version py310, select `E,F,W,I,N,UP,B,C4,SIM`, ignore `E501`
- [x] SETUP-014: Set `fail_under = 85` in coverage config
- [x] SETUP-015: Set `omit = ["src/**/main.py", "*/tests/*"]` in coverage
- [x] SETUP-016: Run `uv sync` and verify lock file is created
- [x] SETUP-017: `uv add torch numpy matplotlib seaborn jupyter pydantic python-dotenv`
- [x] SETUP-018: `uv add --dev pytest pytest-cov ruff ipykernel`
- [x] SETUP-019: Verify `uv.lock` exists and is tracked
- [x] SETUP-020: Create `src/sinusoid_extractor/__init__.py` with `__version__ = "1.00"` and `__all__`
- [x] SETUP-021: Create `src/sinusoid_extractor/sdk/__init__.py`
- [x] SETUP-022: Create `src/sinusoid_extractor/services/__init__.py`
- [x] SETUP-023: Create `src/sinusoid_extractor/models/__init__.py`
- [x] SETUP-024: Create `src/sinusoid_extractor/shared/__init__.py`
- [x] SETUP-025: Create `tests/conftest.py` with shared seed fixture
- [x] SETUP-026: Create `tests/unit/__init__.py`
- [x] SETUP-027: Create `tests/integration/__init__.py`
- [x] SETUP-028: Mirror src/ tree under `tests/unit/` (sdk/, services/, models/, shared/)
- [x] SETUP-029: Create `config/` directory
- [x] SETUP-030: Create `data/raw/` and `data/processed/` directories with `.gitkeep`
- [x] SETUP-031: Create `results/` directory with `.gitkeep`
- [x] SETUP-032: Create `notebooks/` directory with `.gitkeep`
- [x] SETUP-033: Create `assets/` directory for diagrams/screenshots
- [x] SETUP-034: Create `scripts/` directory for utility scripts
- [x] SETUP-035: Create `logs/` directory with `.gitkeep` (logs git-ignored)
- [x] SETUP-036: Run `uv run ruff check` baseline and confirm passes on empty src
- [x] SETUP-037: Run `uv run pytest` baseline and confirm "no tests collected"
- [x] SETUP-038: Add `scripts/check_file_lines.py` enforcing ≤150 LoC per .py
- [x] SETUP-039: Add `Makefile` (or `justfile`) with `lint`, `test`, `check`, `notebook` targets
- [x] SETUP-040: Verify `gh auth status` succeeds (user has gh installed)
- [x] SETUP-041: Pre-create the GitHub repo skeleton plan (defer actual creation to push step)
- [x] SETUP-042: Verify Python 3.10+ available via `uv python pin 3.11` (or 3.12)
- [x] SETUP-043: Add `.python-version` file to pin interpreter
- [x] SETUP-044: Confirm `torch` imports under uv: `uv run python -c "import torch; print(torch.__version__)"`
- [x] SETUP-045: Confirm CPU device for training (no GPU on macOS arm64 by default)
- [x] SETUP-046: Add `docs/ADRs/` directory (referenced by PLAN.md §4)
- [x] SETUP-047: Write ADR-001 through ADR-010 stub files referencing PLAN.md summaries
- [x] SETUP-048: Add `docs/diagrams/` directory for any image exports
- [x] SETUP-049: Add `docs/SUBMISSION_CHECKLIST.md` skeleton
- [x] SETUP-050: Initial commit of scaffolding (already done as part of PRD commit)

## Phase 1 — Configuration System (P0) [40 tasks]

- [x] CFG-001: Write `config/setup.json` v1.00 per PLAN.md §5.1 schema
- [x] CFG-002: Write `config/rate_limits.json` v1.00 per PLAN.md §5.2 (HW1 stub)
- [x] CFG-003: Write `config/logging_config.json` v1.00 (Python logging dict-config)
- [x] CFG-004: Create `src/sinusoid_extractor/shared/config.py` (loader)
- [x] CFG-005: Implement `Config.load(path: Path) -> dict` using stdlib `json`
- [x] CFG-006: Implement `Config.validate(raw: dict) -> Config` with schema check
- [x] CFG-007: Add typed dataclasses for sub-sections (DatasetConfig, TrainingConfig, ModelConfigs, ExperimentConfig, OatConfig, PathsConfig)
- [x] CFG-008: Implement `Config.get(key: str, default: Any) -> Any` for dotted access
- [x] CFG-009: Add `Config.from_env() -> dict` for `os.environ.get(...)` overrides
- [x] CFG-010: Add error class `ConfigError(Exception)` for invalid configs
- [x] CFG-011: Add `Config.check_versions(code_v: str, cfg_v: str) -> None` (warns on mismatch)
- [x] CFG-012: Unit test: load valid setup.json → returns dataclass tree
- [x] CFG-013: Unit test: load missing required key → raises ConfigError
- [x] CFG-014: Unit test: load malformed JSON → raises ConfigError
- [x] CFG-015: Unit test: env override applies for SINUSOID_SEED
- [x] CFG-016: Unit test: version mismatch logs warning, does not raise
- [x] CFG-017: Unit test: defaults are returned for missing optional keys
- [x] CFG-018: Unit test: dataset config validates frequencies_hz length == 4
- [x] CFG-019: Unit test: training config validates lr > 0
- [x] CFG-020: Unit test: model configs validate hidden_size > 0
- [x] CFG-021: Unit test: oat sweep config has the four required keys
- [x] CFG-022: Unit test: paths config creates dirs lazily
- [x] CFG-023: Add `Config.dump(path: Path) -> None` for round-trip
- [x] CFG-024: Unit test: dump → load round-trip preserves structure
- [x] CFG-025: Add `_comment` field tolerance (loader ignores keys starting with `_`)
- [x] CFG-026: Unit test: comment fields ignored
- [x] CFG-027: Add fixture `tests/conftest.py::sample_config` returning a dict
- [x] CFG-028: Add fixture `tests/conftest.py::config_path` returning tmp file
- [x] CFG-029: Document config schema in PRD (already done — verify)
- [x] CFG-030: Add CLI flag `--config PATH` to override default `config/setup.json`
- [x] CFG-031: Implement noise-level type coercion (allow ints in JSON)
- [x] CFG-032: Implement seed-list type coercion
- [x] CFG-033: Validate experiment.architectures ⊆ {"fc","rnn","lstm"}
- [x] CFG-034: Unit test for the coercions
- [x] CFG-035: Unit test for arch whitelist
- [x] CFG-036: Add `Config.print_summary() -> str` for log header
- [x] CFG-037: Unit test print_summary returns non-empty
- [x] CFG-038: Add YAML notice — explicitly say "JSON only, see ADR-006"
- [x] CFG-039: Add type hints + full docstrings throughout config.py
- [x] CFG-040: Run ruff on shared/config.py → 0 errors

## Phase 2 — Versioning & Shared Utilities (P0) [30 tasks]

- [x] VER-001: Create `src/sinusoid_extractor/shared/version.py` with `__version__ = "1.00"`
- [x] VER-002: Add `Version.bump(field: str = "patch") -> str` (patch = +0.01)
- [x] VER-003: Add `Version.parse(s: str) -> tuple[int,int]`
- [x] VER-004: Unit test: bump 1.00 → 1.01
- [x] VER-005: Unit test: bump 1.99 → 2.00 (overflow handling)
- [x] VER-006: Unit test: parse rejects non-MAJOR.MINOR strings
- [x] VER-007: Wire `__version__` into `src/sinusoid_extractor/__init__.py`
- [x] VER-008: Wire version check into SDK constructor
- [x] LOG-001: Create `src/sinusoid_extractor/shared/logger.py`
- [x] LOG-002: Implement `get_logger(name: str) -> logging.Logger` from `config/logging_config.json`
- [x] LOG-003: Add structured key=value formatter
- [x] LOG-004: Unit test: logger respects level from config
- [x] LOG-005: Unit test: logger writes to file when configured
- [x] LOG-006: Add log line for each SDK method entry/exit
- [x] PERS-001: Create `src/sinusoid_extractor/shared/persistence.py`
- [x] PERS-002: Implement `save_npz(path, **arrays) -> None`
- [x] PERS-003: Implement `load_npz(path) -> dict[str, np.ndarray]`
- [x] PERS-004: Implement `save_json(path, payload: dict) -> None`
- [x] PERS-005: Implement `load_json(path) -> dict`
- [x] PERS-006: Implement `save_csv_row(path, row: dict, header_if_new=True)`
- [x] PERS-007: Unit test save/load npz round-trip
- [x] PERS-008: Unit test save/load json round-trip
- [x] PERS-009: Unit test save_csv_row appends rows
- [x] PERS-010: Add `ensure_dir(path) -> Path` helper
- [x] PERS-011: Unit test ensure_dir creates nested
- [x] HOOK-001: Create `src/sinusoid_extractor/shared/hooks.py`
- [x] HOOK-002: Implement `HookRegistry` class with `register(event, fn)` and `fire(event, **ctx)`
- [x] HOOK-003: Define event Enum: BEFORE_TRAIN, AFTER_EPOCH, AFTER_TRAIN, BEFORE_EVAL, AFTER_EVAL
- [x] HOOK-004: Unit test: registered hooks fire in registration order
- [x] HOOK-005: Unit test: unknown event raises KeyError

## Phase 3 — API Gatekeeper & Wave Queue (Stubs) (P1) [30 tasks]

- [x] GATE-001: Create `src/sinusoid_extractor/shared/gatekeeper.py`
- [x] GATE-002: Define `Gatekeeper` ABC with `call(service: str, payload: dict) -> dict`
- [x] GATE-003: Implement `NoopGatekeeper(Gatekeeper)` returning `{"status": "noop"}`
- [x] GATE-004: Load rate limits from `config/rate_limits.json` at init
- [x] GATE-005: Implement `_check_rate(service: str)` placeholder enforcing the JSON limits
- [x] GATE-006: Add structured logging on every call attempt
- [x] GATE-007: Unit test: noop gatekeeper returns noop status
- [x] GATE-008: Unit test: rate limits loaded from config (mocked json)
- [x] GATE-009: Unit test: undefined service falls back to `default` limits
- [x] GATE-010: Unit test: missing rate_limits.json raises ConfigError
- [x] GATE-011: Unit test: zero requests_per_minute is rejected at init
- [x] GATE-012: Document gatekeeper purpose in PLAN.md (done) — verify
- [x] QUE-001: Create `src/sinusoid_extractor/shared/queue_manager.py`
- [x] QUE-002: Implement `WaveQueue` (FIFO) using `collections.deque`
- [x] QUE-003: Implement `enqueue(item)` and `dequeue() -> Optional[item]`
- [x] QUE-004: Implement `size() -> int` and `is_full() -> bool`
- [x] QUE-005: Implement `BackpressureError` raised when full
- [x] QUE-006: Add `max_size` from config
- [x] QUE-007: Unit test: enqueue/dequeue FIFO order
- [x] QUE-008: Unit test: full queue raises BackpressureError on enqueue
- [x] QUE-009: Unit test: empty dequeue returns None
- [x] QUE-010: Unit test: size tracking correct
- [x] QUE-011: Unit test: wave queue thread-safe (using threading.Lock)
- [x] GATE-013: Unit test: gatekeeper integration with WaveQueue (smoke)
- [x] GATE-014: Add ADR-011 stub: "Gatekeeper noop in HW1; full impl in HW2+"
- [x] GATE-015: Unit test rate-limit JSON keys validated
- [x] GATE-016: Unit test: retries config respected (mocked clock)
- [x] GATE-017: Verify gatekeeper imported by SDK (smoke)
- [x] GATE-018: Unit test: gatekeeper has no hardcoded limits in code
- [x] GATE-019: Lint clean
- [x] GATE-020: Coverage ≥ 85% for gatekeeper module

## Phase 4 — Constants & Enums (P0) [20 tasks]

- [x] CONST-001: Create `src/sinusoid_extractor/constants.py`
- [x] CONST-002: Define `FIXED_FREQUENCIES_HZ: tuple[int, ...] = (1, 3, 5, 7)`
- [x] CONST-003: Define `INPUT_DIM = 14` (4 one-hot + 10 window)
- [x] CONST-004: Define `OUTPUT_DIM = 10`
- [x] CONST-005: Define `CONTEXT_WINDOW = 10`
- [x] CONST-006: Define `class Architecture(StrEnum)`: FC, RNN, LSTM
- [x] CONST-007: Define `class Optimizer(StrEnum)`: ADAM, RMSPROP
- [x] CONST-008: Define `class HookEvent(StrEnum)`: BEFORE_TRAIN, AFTER_EPOCH, AFTER_TRAIN, BEFORE_EVAL, AFTER_EVAL
- [x] CONST-009: Define `class NoiseDistribution(StrEnum)`: UNIFORM, GAUSSIAN
- [x] CONST-010: Define `DEFAULT_SEED = 42`
- [x] CONST-011: Document each constant with a one-line docstring at module top
- [x] CONST-012: Unit test: FIXED_FREQUENCIES_HZ has length 4
- [x] CONST-013: Unit test: INPUT_DIM == 14
- [x] CONST-014: Unit test: OUTPUT_DIM == 10
- [x] CONST-015: Unit test: Architecture members cover all three models
- [x] CONST-016: Unit test: Optimizer members include ADAM
- [x] CONST-017: Unit test: HookEvent has the five expected events
- [x] CONST-018: Unit test: NoiseDistribution has UNIFORM
- [x] CONST-019: Lint clean
- [x] CONST-020: Verify no hardcoded values use literals where constants exist (grep)

## Phase 5 — Dataset Service (P0) [120 tasks]

### 5a — SignalGenerator [25]
- [x] SIG-001: Create `services/signal_generator.py`
- [x] SIG-002: Define `SignalGenerator` class with `__init__(amplitude, sampling_rate_hz, duration_seconds)`
- [x] SIG-003: Validate amplitude > 0
- [x] SIG-004: Validate sampling_rate_hz > 0
- [x] SIG-005: Validate duration_seconds > 0
- [x] SIG-006: Implement `_time_axis() -> np.ndarray` returning `t = np.arange(N)/Fs`
- [x] SIG-007: Implement `pure(frequency_hz, phase=0.0) -> np.ndarray`
- [x] SIG-008: Implement `pure_all(frequencies) -> dict[freq, ndarray]`
- [x] SIG-009: Unit test: pure(20Hz) length == Fs * T
- [x] SIG-010: Unit test: pure(0Hz) is constant
- [x] SIG-011: Unit test: pure has zero mean over integer cycles
- [x] SIG-012: Unit test: pure phase shift offsets sample 0
- [x] SIG-013: Unit test: pure_all returns 4 arrays for 4 frequencies
- [x] SIG-014: Property test: pure peak ≈ amplitude
- [x] SIG-015: Property test: amplitude scales linearly
- [x] SIG-016: Add type hints + docstrings
- [x] SIG-017: Building Block doc comment: Input/Output/Setup
- [x] SIG-018: Lint clean for signal_generator.py
- [x] SIG-019: Coverage ≥ 90% for signal_generator
- [x] SIG-020: Property test: increasing freq increases zero-crossings
- [x] SIG-021: Reject non-finite frequency
- [x] SIG-022: Unit test: invalid amplitude raises ValueError
- [x] SIG-023: Unit test: invalid Fs raises ValueError
- [x] SIG-024: Unit test: invalid duration raises ValueError
- [x] SIG-025: Verify file ≤ 150 LoC

### 5b — NoiseModel [25]
- [x] NOI-001: Create `services/noise_model.py`
- [x] NOI-002: Define `NoiseModel` class with `__init__(rng: np.random.Generator)`
- [x] NOI-003: Implement `apply(pure: np.ndarray, alpha: float, distribution: NoiseDistribution = UNIFORM) -> np.ndarray`
- [x] NOI-004: Per-sample amplitude noise: `pure * (1 + uniform(-alpha, +alpha))`
- [x] NOI-005: Per-sample phase noise via `pure(t + dphi/(2*pi*f))`? — instead implement phase noise at the *generator* level: rebuild the sine with random phase per realization
- [x] NOI-006: Refactor: `apply_amplitude_noise(pure, alpha, distribution)` and `random_phase() -> float in [0, 2*pi]`
- [x] NOI-007: Unit test: apply_amplitude_noise returns same shape
- [x] NOI-008: Unit test: amplitude noise mean ≈ 0 over many samples
- [x] NOI-009: Unit test: amplitude noise bounded by ±alpha
- [x] NOI-010: Unit test: random_phase in [0, 2*pi]
- [x] NOI-011: Unit test: random_phase covers full range over 1000 draws
- [x] NOI-012: Unit test: alpha=0 returns identity (no noise)
- [x] NOI-013: Unit test: distribution=GAUSSIAN uses normal(0, alpha)
- [x] NOI-014: Unit test: invalid distribution raises ValueError
- [x] NOI-015: Unit test: invalid alpha < 0 raises ValueError
- [x] NOI-016: Unit test: alpha > 1 logs warning (not standard)
- [x] NOI-017: Building Block doc comment
- [x] NOI-018: Lint clean
- [x] NOI-019: Coverage ≥ 90%
- [x] NOI-020: Property test: noise reproducible with same seed
- [x] NOI-021: Property test: different seeds produce different noise
- [x] NOI-022: Verify file ≤ 150 LoC
- [x] NOI-023: Unit test: rng injection allows deterministic test
- [x] NOI-024: Document choice of uniform per ADR-002
- [x] NOI-025: Confirm phase noise = uniform(0, 2π) per IDEA.md

### 5c — Windower [20]
- [x] WIN-001: Create `services/windower.py`
- [x] WIN-002: Define `Windower(window_size: int, rng: np.random.Generator)`
- [x] WIN-003: Implement `random_starts(n_total: int, n_windows: int) -> np.ndarray`
- [x] WIN-004: Implement `disjoint_starts(n_total: int, n_train, n_val, n_test) -> tuple[ndarray, ndarray, ndarray]`
- [x] WIN-005: Implement `extract(signal, starts) -> np.ndarray of shape (len(starts), window_size)`
- [x] WIN-006: Unit test: extract shape (n, 10)
- [x] WIN-007: Unit test: starts within [0, n_total - window_size]
- [x] WIN-008: Unit test: disjoint_starts returns disjoint sets
- [x] WIN-009: Unit test: window_size > n_total raises ValueError
- [x] WIN-010: Unit test: zero starts returns empty array (n=0)
- [x] WIN-011: Property test: window content matches signal at offset
- [x] WIN-012: Property test: window_size = 1 returns single samples
- [x] WIN-013: Building Block doc comment
- [x] WIN-014: Lint clean
- [x] WIN-015: Coverage ≥ 90%
- [x] WIN-016: Verify file ≤ 150 LoC
- [x] WIN-017: Unit test: rng deterministic
- [x] WIN-018: Unit test: extract handles 2D signal (broadcast)
- [x] WIN-019: Unit test: extract preserves dtype
- [x] WIN-020: Document partitioning strategy in PRD_dataset.md

### 5d — Splitter [20]
- [x] SPL-001: Create `services/splitter.py`
- [x] SPL-002: Define `Splitter` class
- [x] SPL-003: Implement `assign_one_hot(n_examples: int, n_classes: int = 4, rng) -> np.ndarray (n,4)`
- [x] SPL-004: Implement `select_target(pure_signals: dict, one_hot: np.ndarray) -> ndarray`
- [x] SPL-005: Implement `build_tuples(combined, pure_dict, starts, one_hots) -> (C, x, y)`
- [x] SPL-006: Unit test: one_hot rows sum to 1
- [x] SPL-007: Unit test: one_hot uniform distribution over classes
- [x] SPL-008: Unit test: select_target picks correct sine
- [x] SPL-009: Unit test: build_tuples shapes correct
- [x] SPL-010: Unit test: build_tuples y matches pure at given starts
- [x] SPL-011: Unit test: build_tuples x = window from combined
- [x] SPL-012: Property test: y matches pure for the selected class
- [x] SPL-013: Property test: x sourced from combined, not pure
- [x] SPL-014: Building Block doc comment
- [x] SPL-015: Lint clean
- [x] SPL-016: Coverage ≥ 90%
- [x] SPL-017: Verify file ≤ 150 LoC
- [x] SPL-018: Unit test: select_target with 2D one_hot
- [x] SPL-019: Unit test: build_tuples with empty starts returns empty arrays
- [x] SPL-020: Document split strategy in PRD_dataset.md

### 5e — DatasetService Orchestrator [15]
- [x] DAT-001: Create `services/dataset_service.py`
- [x] DAT-002: Define `DatasetService(config: DatasetConfig)`
- [x] DAT-003: Compose SignalGenerator, NoiseModel, Windower, Splitter
- [x] DAT-004: Implement `build_raw_signals(alpha, seed) -> dict (4 pure, 4 noisy, 1 combined)`
- [x] DAT-005: Implement `build_tuples(raw, n_train, n_val, n_test, seed) -> DataBundle`
- [x] DAT-006: Implement `persist(raw, path)` and `load_raw(path) -> dict`
- [x] DAT-007: Implement `generate(alpha, seed) -> DatasetHandle` end-to-end
- [x] DAT-008: Unit test: generate returns 9 raw vectors of length 10000
- [x] DAT-009: Unit test: generate returns 5000 train tuples
- [x] DAT-010: Unit test: persisted npz loadable
- [x] DAT-011: Integration test: alpha=0 gives noiseless combined signal
- [x] DAT-012: Integration test: alpha=0.1 statistics match expectations
- [x] DAT-013: Lint clean
- [x] DAT-014: Coverage ≥ 90%
- [x] DAT-015: Verify file ≤ 150 LoC

### 5f — DataBundle / Dataset (PyTorch) [15]
- [x] DBP-001: Create `services/data_bundle.py` with TypedDict / dataclass
- [x] DBP-002: Create `services/torch_dataset.py` with `SinusoidWindowDataset(torch.utils.data.Dataset)`
- [x] DBP-003: Implement `__len__` and `__getitem__` returning (input_vec, target_vec)
- [x] DBP-004: Concatenate one-hot + window into 14-dim tensor for FC
- [x] DBP-005: For RNN/LSTM: build (10, 5) sequence (sample + 4-dim one-hot per timestep)
- [x] DBP-006: Add `arch_view: Architecture` parameter to switch input shaping
- [x] DBP-007: Unit test: len == n_examples
- [x] DBP-008: Unit test: FC view returns (14,) tensor
- [x] DBP-009: Unit test: RNN view returns (10, 5) tensor
- [x] DBP-010: Unit test: LSTM view same as RNN view
- [x] DBP-011: Unit test: targets shape (10,)
- [x] DBP-012: Unit test: dtype float32
- [x] DBP-013: Lint clean
- [x] DBP-014: Coverage ≥ 90%
- [x] DBP-015: Verify file ≤ 150 LoC

## Phase 6 — Models (P0) [150 tasks]

### 6a — BaseExtractor + Mixins + Registry [35]
- [x] BASE-001: Create `models/base_extractor.py`
- [x] BASE-002: Define `BaseExtractor(nn.Module, ParamCountMixin, SaveLoadMixin, ABC)`
- [x] BASE-003: Add `INPUT_DIM = 14`, `OUTPUT_DIM = 10` class vars
- [x] BASE-004: Define `forward(batch)` as abstract
- [x] BASE-005: Define `architecture_name() -> str` as abstract
- [x] BASE-006: Add `to_device(device)` shared helper
- [x] BASE-007: Unit test: BaseExtractor cannot be instantiated directly
- [x] BASE-008: Unit test: subclass without forward fails
- [x] MIX-001: Create `models/mixins.py`
- [x] MIX-002: Define `ParamCountMixin.count_parameters() -> int`
- [x] MIX-003: Define `SaveLoadMixin.save(path)` and `load(path)`
- [x] MIX-004: Unit test: count_parameters returns correct count for nn.Linear
- [x] MIX-005: Unit test: save/load round-trip preserves weights
- [x] MIX-006: Unit test: load on wrong arch raises clear error
- [x] MIX-007: Mixins are self-testable in isolation (per RULES.md §6)
- [x] MIX-008: Lint clean
- [x] MIX-009: Coverage ≥ 90%
- [x] MIX-010: Verify file ≤ 150 LoC
- [x] REG-001: Create `models/registry.py`
- [x] REG-002: Implement `ModelRegistry` with `_registry: dict[str, type[BaseExtractor]]`
- [x] REG-003: Implement `register(name)` decorator
- [x] REG-004: Implement `build(name, config) -> BaseExtractor`
- [x] REG-005: Implement `available() -> list[str]`
- [x] REG-006: Unit test: register adds entry
- [x] REG-007: Unit test: duplicate registration raises
- [x] REG-008: Unit test: build with unknown name raises ValueError
- [x] REG-009: Unit test: available lists all registered
- [x] REG-010: Document plugin pattern in PLAN.md (done)
- [x] REG-011: Lint clean
- [x] REG-012: Coverage ≥ 90%
- [x] REG-013: Verify file ≤ 150 LoC
- [x] REG-014: Auto-register fc/rnn/lstm via `models/__init__.py` imports
- [x] REG-015: Unit test: importing models package registers all three
- [x] REG-016: Property: registry survives module reimport
- [x] REG-017: Add type alias `ModelFactory = Callable[[ModelConfig], BaseExtractor]`

### 6b — FC Model [30]
- [x] FC-001: Create `models/fc_model.py`
- [x] FC-002: Define `FCExtractor(BaseExtractor)`
- [x] FC-003: `__init__(input_dim, output_dim, hidden_size, num_layers, dropout)`
- [x] FC-004: Build `nn.Sequential` with Linear → ReLU → Dropout layers
- [x] FC-005: Final layer linear (no activation)
- [x] FC-006: Implement `forward(x: Tensor[B, 14]) -> Tensor[B, 10]`
- [x] FC-007: Register as `@register("fc")`
- [x] FC-008: Unit test: forward produces (B, 10)
- [x] FC-009: Unit test: forward differentiable (loss.backward works)
- [x] FC-010: Unit test: 2 hidden layers count parameters correctly
- [x] FC-011: Unit test: 3 hidden layers
- [x] FC-012: Unit test: dropout=0 deterministic in eval mode
- [x] FC-013: Unit test: hidden_size=128 expected param count
- [x] FC-014: Unit test: hidden_size=256 expected param count
- [x] FC-015: Unit test: invalid num_layers raises
- [x] FC-016: Unit test: invalid hidden_size raises
- [x] FC-017: Unit test: dropout in [0, 1) only
- [x] FC-018: Unit test: gradient flows through all layers
- [x] FC-019: Unit test: save/load round-trip
- [x] FC-020: Unit test: forward with batch=1 works
- [x] FC-021: Unit test: forward with batch=64 works
- [x] FC-022: Unit test: cpu/cpu round trip
- [x] FC-023: Building Block doc comment
- [x] FC-024: Lint clean
- [x] FC-025: Coverage ≥ 90%
- [x] FC-026: Verify file ≤ 150 LoC
- [x] FC-027: Add architecture_name() returns "fc"
- [x] FC-028: Unit test: registry.build("fc", cfg) returns FCExtractor
- [x] FC-029: Verify input_dim/output_dim wired from class vars
- [x] FC-030: Smoke test: train 1 epoch on tiny dataset, loss decreases

### 6c — RNN Model [40]
- [x] RNN-001: Create `models/rnn_model.py`
- [x] RNN-002: Define `RNNExtractor(BaseExtractor)`
- [x] RNN-003: `__init__(input_dim_per_step, output_dim, hidden_size, num_layers, dropout)`
- [x] RNN-004: Use `nn.RNN(input_size=5, hidden_size, num_layers, nonlinearity='tanh', batch_first=True, dropout)`
- [x] RNN-005: Final `nn.Linear(hidden_size, 10)` mapping last hidden to output
- [x] RNN-006: Implement `forward(x: Tensor[B, 10, 5]) -> Tensor[B, 10]`
- [x] RNN-007: Take last timestep output: `out[:, -1, :]` then linear to 10
- [x] RNN-008: Register as `@register("rnn")`
- [x] RNN-009: Unit test: forward produces (B, 10)
- [x] RNN-010: Unit test: parameter count matches `4*(in+hid+1)*hid` formula
- [x] RNN-011: Unit test: tanh nonlinearity used (introspect _flat_weights or check forward)
- [x] RNN-012: Unit test: 1-layer config works
- [x] RNN-013: Unit test: 2-layer config works (dropout active between layers)
- [x] RNN-014: Unit test: 3-layer config works
- [x] RNN-015: Unit test: hidden_size=128 OK
- [x] RNN-016: Unit test: hidden_size=256 OK
- [x] RNN-017: Unit test: gradient flows
- [x] RNN-018: Unit test: save/load preserves weights
- [x] RNN-019: Unit test: input shape mismatch raises
- [x] RNN-020: Unit test: batch=1 works
- [x] RNN-021: Unit test: batch=64 works
- [x] RNN-022: Unit test: dropout=0 deterministic
- [x] RNN-023: Unit test: forward with detached input works
- [x] RNN-024: Unit test: invalid layers raises
- [x] RNN-025: Unit test: invalid hidden raises
- [x] RNN-026: Unit test: dropout in [0,1)
- [x] RNN-027: Unit test: registry build returns RNNExtractor
- [x] RNN-028: Unit test: architecture_name() == "rnn"
- [x] RNN-029: Smoke test: train 1 epoch on tiny dataset
- [x] RNN-030: Verify nonlinearity = tanh per RNN book + IDEA
- [x] RNN-031: Building Block doc comment
- [x] RNN-032: LaTeX equation in docstring: $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
- [x] RNN-033: Lint clean
- [x] RNN-034: Coverage ≥ 90%
- [x] RNN-035: Verify file ≤ 150 LoC
- [x] RNN-036: Document C-concat strategy at every timestep (ADR-003)
- [x] RNN-037: Confirm input_size = 5 = 1 sample + 4 one-hot
- [x] RNN-038: Verify dropout only applied between layers (not after last)
- [x] RNN-039: Unit test: hidden init to zeros
- [x] RNN-040: Unit test: forward with even batch sizes works

### 6d — LSTM Model [45]
- [x] LSTM-001: Create `models/lstm_model.py`
- [x] LSTM-002: Define `LSTMExtractor(BaseExtractor)`
- [x] LSTM-003: `__init__(input_dim_per_step, output_dim, hidden_size, num_layers, dropout)`
- [x] LSTM-004: Use `nn.LSTM(input_size=5, hidden_size, num_layers, batch_first=True, dropout)`
- [x] LSTM-005: Final `nn.Linear(hidden_size, 10)` mapping last hidden to output
- [x] LSTM-006: Implement `forward(x: Tensor[B, 10, 5]) -> Tensor[B, 10]`
- [x] LSTM-007: Take last timestep: `out[:, -1, :]` → linear
- [x] LSTM-008: Register as `@register("lstm")`
- [x] LSTM-009: Unit test: forward produces (B, 10)
- [x] LSTM-010: Unit test: parameter count matches LSTM formula 4*(in+hid+1)*hid per layer
- [x] LSTM-011: Unit test: 1-layer config works
- [x] LSTM-012: Unit test: 2-layer config works
- [x] LSTM-013: Unit test: 3-layer config works
- [x] LSTM-014: Unit test: hidden_size=128 OK
- [x] LSTM-015: Unit test: hidden_size=256 OK
- [x] LSTM-016: Unit test: dropout=0.2 active in train, off in eval
- [x] LSTM-017: Unit test: gradient flows
- [x] LSTM-018: Unit test: save/load round-trip
- [x] LSTM-019: Unit test: input shape mismatch raises
- [x] LSTM-020: Unit test: batch=1
- [x] LSTM-021: Unit test: batch=64
- [x] LSTM-022: Unit test: invalid layers raises
- [x] LSTM-023: Unit test: invalid hidden raises
- [x] LSTM-024: Unit test: dropout in [0,1)
- [x] LSTM-025: Unit test: registry build returns LSTMExtractor
- [x] LSTM-026: Unit test: architecture_name() == "lstm"
- [x] LSTM-027: Smoke test: train 1 epoch on tiny dataset
- [x] LSTM-028: Verify 4-gate structure documented in docstring
- [x] LSTM-029: LaTeX equations in docstring: forget/input/candidate/output/cell/hidden
- [x] LSTM-030: Building Block doc comment
- [x] LSTM-031: Lint clean
- [x] LSTM-032: Coverage ≥ 90%
- [x] LSTM-033: Verify file ≤ 150 LoC
- [x] LSTM-034: Document C-concat strategy at every timestep (ADR-003)
- [x] LSTM-035: Confirm input_size = 5 = 1 sample + 4 one-hot
- [x] LSTM-036: Verify dropout only between layers
- [x] LSTM-037: Unit test: hidden + cell init to zeros
- [x] LSTM-038: Unit test: forget gate present (introspect)
- [x] LSTM-039: Unit test: even batch sizes work
- [x] LSTM-040: Compare param count: LSTM ≈ 4× RNN at same hidden
- [x] LSTM-041: Property test: LSTM has more params than RNN at same config
- [x] LSTM-042: Property test: dropout=0 + same seed → deterministic forward
- [x] LSTM-043: Verify default config matches PLAN.md
- [x] LSTM-044: Add reference to LSTM book pages 18 (hyperparam recommendations)
- [x] LSTM-045: Sanity check: LSTM handles 0-noise data with low loss

## Phase 7 — Training Service (P0) [100 tasks]

### 7a — Loss Function [10]
- [x] LOSS-001: Create `services/loss_fn.py`
- [x] LOSS-002: Implement `WindowSumMSE(nn.Module)` summing per-sample MSE across the 10 outputs
- [x] LOSS-003: Use `reduction='sum'` over window axis, mean over batch
- [x] LOSS-004: Unit test: shape compatibility (B, 10) vs (B, 10)
- [x] LOSS-005: Unit test: identical pred/target → 0 loss
- [x] LOSS-006: Unit test: doubled error → 4× loss (quadratic)
- [x] LOSS-007: Unit test: differentiable
- [x] LOSS-008: Match lecturer formula: Total Loss = L_1 + ... + L_10
- [x] LOSS-009: Lint clean
- [x] LOSS-010: Verify file ≤ 150 LoC

### 7b — Early Stopping [15]
- [x] ES-001: Create `services/early_stopping.py`
- [x] ES-002: Define `EarlyStopping(patience: int, mode: str = 'min', min_delta: float = 0.0)`
- [x] ES-003: Implement `step(value) -> bool` returning True when stopping
- [x] ES-004: Track best value + epochs_without_improvement
- [x] ES-005: Unit test: triggers after patience epochs without improvement
- [x] ES-006: Unit test: improvement resets counter
- [x] ES-007: Unit test: min_delta respected (small noise ignored)
- [x] ES-008: Unit test: mode='max' reverses comparison
- [x] ES-009: Unit test: state retrievable
- [x] ES-010: Unit test: invalid patience raises
- [x] ES-011: Unit test: invalid mode raises
- [x] ES-012: Unit test: deepcopy of best_state_dict on improvement
- [x] ES-013: Building Block doc comment
- [x] ES-014: Lint clean
- [x] ES-015: Coverage ≥ 90%

### 7c — Optimizer Wrapper [10]
- [x] OPT-001: Create `services/optimizer_factory.py`
- [x] OPT-002: Define `build_optimizer(name: str, params, lr) -> Optimizer`
- [x] OPT-003: Support 'adam' and 'rmsprop'
- [x] OPT-004: Unit test: adam returned for 'adam'
- [x] OPT-005: Unit test: rmsprop returned for 'rmsprop'
- [x] OPT-006: Unit test: invalid name raises
- [x] OPT-007: Unit test: lr applied
- [x] OPT-008: Lint clean
- [x] OPT-009: Coverage 100%
- [x] OPT-010: Verify file ≤ 150 LoC

### 7d — TrainingLoop [30]
- [x] LOOP-001: Create `services/training_loop.py`
- [x] LOOP-002: Define `TrainingLoop(model, optimizer, loss_fn, train_loader, val_loader, max_epochs, hooks, early_stopping)`
- [x] LOOP-003: Implement `run() -> TrainingResult`
- [x] LOOP-004: Per-epoch: train, then validate
- [x] LOOP-005: Track loss_history (train + val per epoch)
- [x] LOOP-006: Track wall_clock_seconds
- [x] LOOP-007: Fire `BEFORE_TRAIN`, `AFTER_EPOCH`, `AFTER_TRAIN` hooks
- [x] LOOP-008: Restore best weights on early stop
- [x] LOOP-009: Detect NaN loss → abort with TrainingError
- [x] LOOP-010: Set model to train()/eval() at appropriate times
- [x] LOOP-011: Move batches to device
- [x] LOOP-012: Unit test: 1 epoch decreases loss on memorizable data
- [x] LOOP-013: Unit test: hooks fired with expected events
- [x] LOOP-014: Unit test: early stop triggers
- [x] LOOP-015: Unit test: NaN loss aborts cleanly
- [x] LOOP-016: Unit test: max_epochs respected
- [x] LOOP-017: Unit test: best weights restored on stop
- [x] LOOP-018: Unit test: loss_history length matches epochs run
- [x] LOOP-019: Unit test: optimizer.step called per batch
- [x] LOOP-020: Unit test: optimizer.zero_grad called per batch
- [x] LOOP-021: Unit test: param count tracked
- [x] LOOP-022: Unit test: device='cpu' works
- [x] LOOP-023: Unit test: deterministic with fixed seed
- [x] LOOP-024: Building Block doc comment
- [x] LOOP-025: Lint clean
- [x] LOOP-026: Coverage ≥ 90%
- [x] LOOP-027: Verify file ≤ 150 LoC
- [x] LOOP-028: Define `TrainingResult` dataclass with all metrics
- [x] LOOP-029: Define `TrainingError(Exception)`
- [x] LOOP-030: Document hook lifecycle in docstring

### 7e — TrainingService Orchestrator [20]
- [x] TSV-001: Create `services/training_service.py`
- [x] TSV-002: Define `TrainingService(config, gatekeeper)`
- [x] TSV-003: Implement `train(arch, dataset, hyperparams, seed) -> RunHandle`
- [x] TSV-004: Build model via registry
- [x] TSV-005: Build optimizer via factory
- [x] TSV-006: Build train/val DataLoaders with num_workers
- [x] TSV-007: Construct TrainingLoop
- [x] TSV-008: Persist results to `results/<run_id>/`
- [x] TSV-009: Generate run_id with timestamp + arch + freq + alpha + seed
- [x] TSV-010: Save loss_history.json
- [x] TSV-011: Save best_model.pt
- [x] TSV-012: Unit test: train returns RunHandle with valid run_id
- [x] TSV-013: Unit test: results dir created
- [x] TSV-014: Unit test: loss_history persisted
- [x] TSV-015: Unit test: model checkpoint persisted
- [x] TSV-016: Integration test: train fc 2 epochs end-to-end
- [x] TSV-017: Integration test: train rnn 2 epochs end-to-end
- [x] TSV-018: Integration test: train lstm 2 epochs end-to-end
- [x] TSV-019: Lint clean
- [x] TSV-020: Verify file ≤ 150 LoC

### 7f — Training utilities [15]
- [x] TUT-001: Add `set_global_seed(seed)` in shared
- [x] TUT-002: Unit test: set_global_seed makes torch deterministic
- [x] TUT-003: Unit test: set_global_seed makes numpy deterministic
- [x] TUT-004: Unit test: set_global_seed makes random deterministic
- [x] TUT-005: Add `count_parameters(model)` in mixins (covered)
- [x] TUT-006: Add `format_run_id(arch, freq, alpha, seed) -> str`
- [x] TUT-007: Unit test: run_id contains all 4 components
- [x] TUT-008: Unit test: run_id has timestamp
- [x] TUT-009: Add `select_device() -> str` (cpu fallback)
- [x] TUT-010: Unit test: select_device returns 'cpu' when no GPU
- [x] TUT-011: Add `wall_clock_timer()` context manager
- [x] TUT-012: Unit test: timer measures > 0
- [x] TUT-013: Lint clean
- [x] TUT-014: Coverage ≥ 90%
- [x] TUT-015: Verify each file ≤ 150 LoC

## Phase 8 — Evaluation Service (P0) [70 tasks]

### 8a — Metrics [20]
- [x] MET-001: Create `services/metrics.py`
- [x] MET-002: Implement `mse(pred, target) -> float`
- [x] MET-003: Implement `mae(pred, target) -> float`
- [x] MET-004: Implement `r2_score(pred, target) -> float`
- [x] MET-005: Implement `snr_db(pred, target) -> float`
- [x] MET-006: Unit test: mse 0 for identical
- [x] MET-007: Unit test: mse non-negative
- [x] MET-008: Unit test: mae 0 for identical
- [x] MET-009: Unit test: r2 == 1 for perfect prediction
- [x] MET-010: Unit test: r2 < 0 possible for bad prediction
- [x] MET-011: Unit test: snr higher for better predictions
- [x] MET-012: Unit test: handle empty arrays gracefully
- [x] MET-013: Unit test: support np and torch input
- [x] MET-014: Unit test: dtype-agnostic
- [x] MET-015: Building Block doc comment
- [x] MET-016: Lint clean
- [x] MET-017: Coverage ≥ 95%
- [x] MET-018: Verify file ≤ 150 LoC
- [x] MET-019: Add `predict_zero_baseline(target) -> float` for comparison
- [x] MET-020: Unit test baseline returns mean(target^2)

### 8b — EvaluationService [25]
- [x] EV-001: Create `services/evaluation_service.py`
- [x] EV-002: Define `EvaluationService(config)`
- [x] EV-003: Implement `evaluate(run_handle, test_loader) -> EvalReport`
- [x] EV-004: Compute test_mse, test_mae, test_r2
- [x] EV-005: Compute baseline (predict zero) for comparison
- [x] EV-006: Sample 5 reconstructions for plotting
- [x] EV-007: Persist `eval_report.json` next to `loss_history.json`
- [x] EV-008: Unit test: report contains required fields
- [x] EV-009: Unit test: identical pred/target → near-zero metrics
- [x] EV-010: Unit test: persisted report parseable
- [x] EV-011: Unit test: baseline computed
- [x] EV-012: Unit test: reconstruction sample shape
- [x] EV-013: Building Block doc comment
- [x] EV-014: Lint clean
- [x] EV-015: Coverage ≥ 90%
- [x] EV-016: Verify file ≤ 150 LoC
- [x] EV-017: Define `EvalReport` dataclass
- [x] EV-018: Fire BEFORE_EVAL / AFTER_EVAL hooks
- [x] EV-019: Unit test: hooks fire
- [x] EV-020: Integration test: train+evaluate fc on tiny dataset
- [x] EV-021: Integration test: train+evaluate rnn on tiny dataset
- [x] EV-022: Integration test: train+evaluate lstm on tiny dataset
- [x] EV-023: Stratify metrics by target_freq (4 frequencies)
- [x] EV-024: Unit test: stratification works
- [x] EV-025: Aggregate per-(arch,freq,alpha) into one row of sensitivity.csv

### 8c — Plotting helpers [15]
- [x] PLT-001: Create `services/plotting.py`
- [x] PLT-002: Implement `plot_loss_curves(history, ax)`
- [x] PLT-003: Implement `plot_reconstruction(pred, target, ax)`
- [x] PLT-004: Implement `plot_mse_heatmap(df, x, y, value, ax)`
- [x] PLT-005: Implement `plot_oat_sensitivity(df, hyperparam, ax)`
- [x] PLT-006: Implement `plot_signal_timeseries(signal, fs, ax, label)`
- [x] PLT-007: Implement `plot_fft_spectrum(signal, fs, ax)`
- [x] PLT-008: Use seaborn `colorblind` palette
- [x] PLT-009: Add titles, axis labels, legends to all plots
- [x] PLT-010: Unit test: each plot returns Axes object
- [x] PLT-011: Unit test: plots produce non-empty figure
- [x] PLT-012: Smoke test: render to /tmp file
- [x] PLT-013: Lint clean
- [x] PLT-014: Verify file ≤ 150 LoC
- [x] PLT-015: Coverage ≥ 80% (plotting is hard to test deeply)

### 8d — Reconstruction sampling [10]
- [x] REC-001: Implement `sample_reconstructions(model, loader, n=5) -> list[(pred, target)]`
- [x] REC-002: Cycle through frequencies for diverse examples
- [x] REC-003: Save as npz under `results/<run_id>/reconstructions.npz`
- [x] REC-004: Unit test: returns n examples
- [x] REC-005: Unit test: pred shape == target shape
- [x] REC-006: Unit test: persistence round-trips
- [x] REC-007: Lint clean
- [x] REC-008: Coverage ≥ 90%
- [x] REC-009: Verify file ≤ 150 LoC
- [x] REC-010: Building Block doc comment

## Phase 9 — Sweep Service (P1) [50 tasks]

- [x] SW-001: Create `services/sweep_service.py`
- [x] SW-002: Define `SweepService(config, training_service, eval_service)`
- [x] SW-003: Implement `run_experiment_matrix() -> list[RunHandle]` for arch × freq × alpha × seed
- [x] SW-004: Implement `run_oat_sweep() -> list[RunHandle]` for hyperparams
- [x] SW-005: Aggregate results into `results/sensitivity.csv`
- [x] SW-006: Aggregate results into `results/experiment_matrix.csv`
- [x] SW-007: Per-run logging (start/end + params)
- [x] SW-008: Skip already-completed runs (idempotency)
- [x] SW-009: Unit test: matrix size = 3 archs × 4 freqs × 4 alphas × 3 seeds = 144 runs
- [x] SW-010: Unit test: idempotency skips done runs
- [x] SW-011: Unit test: oat sweep generates 4 hyperparams × 3 values × 3 archs = 36 runs/seed
- [x] SW-012: Unit test: csv aggregation includes all rows
- [x] SW-013: Unit test: csv has correct columns
- [x] SW-014: Integration test: tiny matrix (1 arch × 1 freq × 1 alpha × 1 seed) runs
- [x] SW-015: Integration test: tiny oat (fc, hidden=[64]) runs
- [x] SW-016: Building Block doc comment
- [x] SW-017: Lint clean
- [x] SW-018: Coverage ≥ 85%
- [x] SW-019: Verify file ≤ 150 LoC
- [x] SW-020: Add `--dry-run` mode that lists planned runs without executing
- [x] SW-021: Unit test: dry-run lists expected count
- [x] SW-022: Implement `_grid_size_estimate() -> int`
- [x] SW-023: Unit test: estimate matches actual
- [x] SW-024: Document scaling tradeoffs in PRD_evaluation.md
- [x] SW-025: Add `--limit N` flag to truncate long sweeps for debugging
- [x] SW-026: Unit test: limit truncates
- [x] SW-027: Add per-run timeout config
- [x] SW-028: Unit test: timeout raises TrainingError
- [x] SW-029: Add resume from CSV if interrupted
- [x] SW-030: Unit test: resume picks up where left off
- [x] SW-031: Add total wall-clock report at end
- [x] SW-032: Unit test: total wall-clock reported
- [x] SW-033: Add per-arch wall-clock stratification
- [x] SW-034: Unit test: stratification works
- [x] SW-035: Add memory monitoring placeholder (psutil optional)
- [x] SW-036: Unit test: memory not enforced (just logged)
- [x] SW-037: Add CLI subcommand `run-matrix` and `run-oat`
- [x] SW-038: Unit test: CLI dispatches correctly
- [x] SW-039: Add `--config-override` JSON flag
- [x] SW-040: Unit test: override applied
- [x] SW-041: Save manifest with all run_ids
- [x] SW-042: Unit test: manifest contains expected run_ids
- [x] SW-043: Add SHA-256 of config to manifest
- [x] SW-044: Unit test: SHA reproducible
- [x] SW-045: Add results pruning utility (`scripts/prune_results.py`)
- [x] SW-046: Unit test: prune dry-run lists candidates
- [x] SW-047: Document the matrix in PRD_evaluation.md
- [x] SW-048: Add `--seed-only N` for fast smoke runs
- [x] SW-049: Unit test: seed-only filter works
- [x] SW-050: Verify all sweep files ≤ 150 LoC

## Phase 10 — SDK (P0) [40 tasks]

- [x] SDK-001: Create `sdk/sdk.py`
- [x] SDK-002: Define `SinusoidExtractorSDK` class
- [x] SDK-003: `__init__(config_path: Path | None = None)`
- [x] SDK-004: Load config + version check at init
- [x] SDK-005: Instantiate gatekeeper, dataset_service, training_service, eval_service, sweep_service
- [x] SDK-006: Implement `generate_dataset(alpha, seed) -> DatasetHandle`
- [x] SDK-007: Implement `train_model(arch, dataset, hyperparams, seed) -> RunHandle`
- [x] SDK-008: Implement `evaluate(run, dataset) -> EvalReport`
- [x] SDK-009: Implement `run_experiment_matrix() -> list[RunHandle]`
- [x] SDK-010: Implement `run_oat_sweep() -> list[RunHandle]`
- [x] SDK-011: Implement `get_version() -> str`
- [x] SDK-012: Implement `get_config() -> dict`
- [x] SDK-013: Add structured logging on every method
- [x] SDK-014: Unit test: SDK init reads config
- [x] SDK-015: Unit test: SDK init missing config raises
- [x] SDK-016: Unit test: generate_dataset returns handle
- [x] SDK-017: Unit test: train_model returns RunHandle
- [x] SDK-018: Unit test: evaluate returns EvalReport
- [x] SDK-019: Unit test: run_experiment_matrix returns list
- [x] SDK-020: Unit test: run_oat_sweep returns list
- [x] SDK-021: Unit test: get_version returns "1.00"
- [x] SDK-022: Unit test: get_config returns dict
- [x] SDK-023: Integration test: end-to-end via SDK only
- [x] SDK-024: Building Block doc comment
- [x] SDK-025: Lint clean
- [x] SDK-026: Coverage ≥ 90%
- [x] SDK-027: Verify file ≤ 150 LoC
- [x] SDK-028: Document each method in docstring (input/output/setup)
- [x] SDK-029: Add `__all__ = ["SinusoidExtractorSDK"]` in `sdk/__init__.py`
- [x] SDK-030: Verify external import works: `from sinusoid_extractor.sdk import SinusoidExtractorSDK`
- [x] SDK-031: Verify SDK has no business logic (just dispatches)
- [x] SDK-032: Audit: no service called outside SDK in tests/ or notebooks/
- [x] SDK-033: Add SDK constructor parameter for `gatekeeper` injection (DI)
- [x] SDK-034: Unit test: custom gatekeeper accepted
- [x] SDK-035: Add `health_check() -> dict` for self-diagnostic
- [x] SDK-036: Unit test: health_check returns OK
- [x] SDK-037: Add `list_completed_runs() -> list[RunHandle]`
- [x] SDK-038: Unit test: list_completed_runs reads results/
- [x] SDK-039: Add `clear_results()` (defensive — requires explicit confirmation)
- [x] SDK-040: Unit test: clear_results requires confirm=True

## Phase 11 — CLI (P0) [30 tasks]

- [x] CLI-001: Create `src/sinusoid_extractor/main.py`
- [x] CLI-002: Build argparse with subcommands: generate-data, train, evaluate, run-matrix, run-oat, version
- [x] CLI-003: Add `--config PATH` global flag
- [x] CLI-004: Add `--log-level LEVEL` global flag
- [x] CLI-005: Implement `cmd_generate_data(args)` calling SDK
- [x] CLI-006: Implement `cmd_train(args)`
- [x] CLI-007: Implement `cmd_evaluate(args)`
- [x] CLI-008: Implement `cmd_run_matrix(args)`
- [x] CLI-009: Implement `cmd_run_oat(args)`
- [x] CLI-010: Implement `cmd_version(args)` printing version
- [x] CLI-011: Argparse: validate arch in {fc, rnn, lstm}
- [x] CLI-012: Argparse: validate alpha in [0, 1]
- [x] CLI-013: Argparse: validate seed integer
- [x] CLI-014: Implement `main()` entry point
- [x] CLI-015: Add `if __name__ == "__main__": main()` guard
- [x] CLI-016: Unit test: each cmd_* function callable in isolation
- [x] CLI-017: Unit test: argparse rejects bad arch
- [x] CLI-018: Unit test: argparse rejects negative alpha
- [x] CLI-019: Unit test: --version prints version and exits 0
- [x] CLI-020: Unit test: --help works
- [x] CLI-021: Smoke: `uv run python -m sinusoid_extractor.main version` returns 0
- [x] CLI-022: Smoke: `uv run python -m sinusoid_extractor.main generate-data --alpha 0.05` runs
- [x] CLI-023: Building Block doc comment
- [x] CLI-024: Lint clean
- [x] CLI-025: Verify file ≤ 150 LoC
- [x] CLI-026: Confirm CLI is THIN (no business logic, just dispatch)
- [x] CLI-027: Add `--quiet` flag to suppress logs
- [x] CLI-028: Unit test: --quiet reduces stdout
- [x] CLI-029: Add exit codes (0 success, 1 error, 2 bad args)
- [x] CLI-030: Unit test: exit codes correct

## Phase 12 — Logging (P1) [20 tasks]

- [x] LOGI-001: Finalize `config/logging_config.json` with file + console handlers
- [x] LOGI-002: Console handler at INFO; file handler at DEBUG
- [x] LOGI-003: Rotating file handler (10MB × 5)
- [x] LOGI-004: Per-module loggers via `__name__`
- [x] LOGI-005: Sensitive value redaction filter (placeholder for future)
- [x] LOGI-006: Unit test: logging config loads
- [x] LOGI-007: Unit test: log line written to file
- [x] LOGI-008: Unit test: rotation triggers at threshold (mocked)
- [x] LOGI-009: Unit test: redaction filter (placeholder)
- [x] LOGI-010: Verify no logs created during pytest (use caplog)
- [x] LOGI-011: Add `disable_logging` context manager for tests
- [x] LOGI-012: Unit test: disable_logging silences logger
- [x] LOGI-013: Add structured kv format
- [x] LOGI-014: Unit test: kv format produces expected string
- [x] LOGI-015: Add CLI flag `--log-level` overriding config
- [x] LOGI-016: Unit test: CLI override works
- [x] LOGI-017: Add log rotation test
- [x] LOGI-018: Add log to `logs/sinusoid_extractor.log`
- [x] LOGI-019: Verify logs/ git-ignored
- [x] LOGI-020: Lint clean

## Phase 13 — Tests Augmentation & Fixtures (P0) [80 tasks]

- [x] FIX-001: `tests/conftest.py::sample_config` (dict)
- [x] FIX-002: `tests/conftest.py::tmp_config_path` (Path)
- [x] FIX-003: `tests/conftest.py::tiny_dataset` (200 train / 50 val / 50 test)
- [x] FIX-004: `tests/conftest.py::seed_rng` (np.random.Generator)
- [x] FIX-005: `tests/conftest.py::sdk` (instantiated SDK with tmp config)
- [x] FIX-006: `tests/conftest.py::cpu_device` (torch device)
- [x] FIX-007: Auto-set seed=42 for every test (autouse)
- [x] FIX-008: Skip GPU-only tests (no GPU on CI)
- [x] FIX-009: Mark slow tests with `@pytest.mark.slow`
- [x] FIX-010: Add `--run-slow` pytest flag
- [x] EDGE-001: Test alpha=0 (no noise) → combined == sum of pure
- [x] EDGE-002: Test alpha=1 (full noise) → combined still bounded
- [x] EDGE-003: Test single-frequency dataset (other 3 zero) optional
- [x] EDGE-004: Test window_size = signal length (one window)
- [x] EDGE-005: Test n_train = 0 (degenerate empty bundle) returns clean error
- [x] EDGE-006: Test num_layers = 1 (no dropout active)
- [x] EDGE-007: Test hidden_size = 1 (degenerate model)
- [x] EDGE-008: Test max_epochs = 1
- [x] EDGE-009: Test early stop with patience=0 → stops first non-improvement
- [x] EDGE-010: Test early stop with patience > epochs → never stops
- [x] EDGE-011: Test loss_fn with all-zero target
- [x] EDGE-012: Test loss_fn with NaN input → raises
- [x] EDGE-013: Test save with read-only path → raises
- [x] EDGE-014: Test load missing file → raises
- [x] EDGE-015: Test config without version → warning logged
- [x] EDGE-016: Test malformed JSON → raises
- [x] EDGE-017: Test SDK without config → uses default
- [x] EDGE-018: Test invalid arch in CLI → argparse error
- [x] EDGE-019: Test alpha < 0 → ValueError
- [x] EDGE-020: Test alpha > 1 → warning, accepted
- [x] PROP-001: Property: dataset reproducibility under same seed
- [x] PROP-002: Property: noise mean ≈ 0 across many samples
- [x] PROP-003: Property: window content matches signal at offset
- [x] PROP-004: Property: model forward is shape-stable across batch sizes
- [x] PROP-005: Property: param count > 0 for all models
- [x] PROP-006: Property: training loss decreases monotonically (smoothed) on memorizable data
- [x] PROP-007: Property: registry returns same instance type for same name
- [x] PROP-008: Property: csv aggregation has no duplicate run_ids
- [x] INT-001: Integration: SDK end-to-end fc on tiny dataset
- [x] INT-002: Integration: SDK end-to-end rnn on tiny dataset
- [x] INT-003: Integration: SDK end-to-end lstm on tiny dataset
- [x] INT-004: Integration: matrix sweep with limit=2 finishes
- [x] INT-005: Integration: oat sweep with limit=2 finishes
- [x] INT-006: Integration: results dir created with expected files
- [x] INT-007: Integration: csv aggregation produced
- [x] INT-008: Integration: notebook execution smoke (jupyter nbconvert --execute)
- [x] INT-009: Integration: gatekeeper called from sdk (smoke, no-op)
- [x] INT-010: Integration: hooks fired during sdk.train_model
- [x] COV-001: Run `uv run pytest --cov` and confirm ≥ 85%
- [x] COV-002: Identify lowest-coverage module and add tests
- [x] COV-003: Aim for 90% on dataset_service
- [x] COV-004: Aim for 90% on training_loop
- [x] COV-005: Aim for 85% on plotting (hard to deeply test)
- [x] LIN-001: `uv run ruff check src/ tests/` returns 0
- [x] LIN-002: Auto-fix safe: `uv run ruff check --fix`
- [x] LIN-003: Re-run lint to confirm clean
- [x] LIN-004: Add `pre-commit` hint in README (optional)
- [x] LIN-005: Verify no F401 (unused imports)
- [x] LIN-006: Verify no E (PEP8) errors
- [x] LIN-007: Verify no B (bugbear) flags
- [x] LIN-008: Verify no C4 (comprehension) flags
- [x] LIN-009: Verify no SIM (simplify) suggestions outstanding
- [x] LIN-010: Verify naming conventions (N) clean
- [x] FILE-001: Run `scripts/check_file_lines.py` → 0 errors
- [x] FILE-002: Identify any file > 150 LoC and split
- [x] FILE-003: Re-run check after splits
- [x] SEC-001: Grep for `api_key|secret|password|token` → empty
- [x] SEC-002: Verify `.env` not in `git ls-files`
- [x] SEC-003: Verify `.env-example` is committed
- [x] SEC-004: Verify `.gitignore` includes secrets
- [x] SEC-005: Run `git secrets --scan` if available (skip if not)
- [x] SEC-006: Confirm no hardcoded API keys
- [x] SEC-007: Confirm no hardcoded URLs
- [x] SEC-008: Confirm no hardcoded paths (use config.paths)
- [x] SEC-009: Confirm config files versioned (1.00)
- [x] SEC-010: Confirm code __version__ matches config version

## Phase 14 — Run Experiments (P0) [40 tasks]

- [x] EXP-001: Pre-flight: confirm `uv sync` clean
- [x] EXP-002: Pre-flight: confirm `uv run pytest` green
- [x] EXP-003: Pre-flight: confirm `uv run ruff check` clean
- [x] EXP-004: Generate the 4 datasets (alpha ∈ {0.01, 0.05, 0.10, 0.20})
- [x] EXP-005: Persist all 4 datasets to `data/raw/`
- [ ] EXP-006: Verify dataset reproducibility (re-run, compare hashes)
- [x] EXP-007: Run base matrix: 3 archs × 4 alphas (use 1 seed first to time)
- [x] EXP-008: Estimate full matrix wall-clock from timing
- [x] EXP-009: If full matrix > 6 h, reduce seeds to 2 or use parallelism
- [x] EXP-010: Run base matrix: 3 archs × 4 alphas × 3 seeds = 36 runs
- [x] EXP-011: Aggregate base matrix results to `results/experiment_matrix.csv`
- [x] EXP-012: Run OAT sweep: 4 hyperparams × 3 values × 3 archs (with default seeds)
- [x] EXP-013: Aggregate OAT results to `results/sensitivity.csv`
- [x] EXP-014: Verify all runs produced loss_history.json
- [x] EXP-015: Verify all runs produced eval_report.json
- [x] EXP-016: Spot-check: best loss < worst loss (sanity)
- [x] EXP-017: Spot-check: alpha=0.01 better than alpha=0.20 (intuition)
- [ ] EXP-018: Save final manifest of all run_ids
- [ ] EXP-019: Persist a `results/RUN_REPORT.md` summary
- [x] EXP-020: Compute mean ± std per cell across seeds
- [x] EXP-021: Compute paired test (RNN vs LSTM at high freq)
- [x] EXP-022: Compute paired test (LSTM vs RNN at low freq)
- [x] EXP-023: Compute FC vs recurrent paired test
- [x] EXP-024: Save statistical results to `results/hypothesis_test.json`
- [x] EXP-025: Save best hyperparams per arch to `results/best_hparams.json`
- [x] EXP-026: If hypothesis disconfirmed, document explanation
- [x] EXP-027: Render reconstructions for best runs to `results/figs/`
- [x] EXP-028: Render loss-curve montage to `results/figs/loss_curves.png`
- [x] EXP-029: Render heatmap to `results/figs/mse_heatmap.png`
- [x] EXP-030: Render OAT line plots to `results/figs/oat_*.png`
- [ ] EXP-031: Verify reproducibility: re-run one cell, compare results within tolerance
- [ ] EXP-032: Document any non-deterministic divergence
- [ ] EXP-033: Backup `results/` to a tarball before notebook authoring
- [x] EXP-034: Confirm CSV files have headers + correct row count
- [x] EXP-035: Confirm no NaNs in CSV results
- [x] EXP-036: Audit run wall-clocks (slowest run, fastest run)
- [x] EXP-037: If LSTM > 30s/epoch, reduce hidden or batch
- [x] EXP-038: Re-run problematic cells if needed
- [x] EXP-039: Final commit of `results/` artifacts (CSVs and figs only — npz git-ignored)
- [ ] EXP-040: Tag this commit `v1.00-experiments`

## Phase 15 — Notebook (P0) [60 tasks]

### 15a — Setup Section [10]
- [x] NB-001: Create `notebooks/analysis.ipynb`
- [x] NB-002: Title cell: "Sinusoid Extraction with FC, RNN, and LSTM — Analysis"
- [x] NB-003: Author + date + course cell
- [x] NB-004: Imports cell (numpy, pandas, matplotlib, seaborn, sdk)
- [x] NB-005: Set seed cell + reproducibility note
- [x] NB-006: Load config cell
- [x] NB-007: Load results from `results/` cell
- [x] NB-008: Sanity-check loaded data shapes
- [x] NB-009: Display config summary (table)
- [x] NB-010: Section divider markdown

### 15b — Dataset Visualization [10]
- [x] NB-011: Markdown intro to dataset
- [x] NB-012: Load and plot pure sine 20 Hz
- [x] NB-013: Load and plot pure sine 60 Hz
- [x] NB-014: Load and plot pure sine 100 Hz
- [x] NB-015: Load and plot pure sine 200 Hz
- [x] NB-016: Plot noisy versions (4 panel grid)
- [x] NB-017: Plot Σ combined signal
- [x] NB-018: FFT spectrum of Σ (frequency axis 0–50 Hz)
- [x] NB-019: Annotate the 4 expected peaks (20, 60, 100, 200 Hz)
- [x] NB-020: Markdown commentary on visibility of peaks

### 15c — Architectures + LaTeX [12]
- [x] NB-021: FC architecture markdown with equations
- [x] NB-022: FC LaTeX: $y = W_2 \cdot \text{ReLU}(W_1 x + b_1) + b_2$
- [x] NB-023: RNN architecture markdown
- [x] NB-024: RNN LaTeX: $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
- [x] NB-025: LSTM architecture markdown
- [x] NB-026: LSTM LaTeX: forget gate $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
- [x] NB-027: LSTM input gate
- [x] NB-028: LSTM candidate cell
- [x] NB-029: LSTM cell update
- [x] NB-030: LSTM output gate
- [x] NB-031: Display per-arch parameter counts table
- [x] NB-032: Display per-arch wall-clock training time table

### 15d — Training [8]
- [x] NB-033: Training loss curves grid (3 archs × 4 noise levels)
- [x] NB-034: Validation loss overlay
- [x] NB-035: Highlight early-stopping epoch with vertical line
- [x] NB-036: Markdown observations on convergence speed
- [x] NB-037: Markdown observations on overfitting (train ↓ val ↑)
- [x] NB-038: Per-arch best-epoch comparison table
- [x] NB-039: Per-arch parameter count vs final loss scatter
- [x] NB-040: Discussion of training dynamics

### 15e — Evaluation [10]
- [x] NB-041: Heatmap MSE × (arch, target_freq) for alpha=0.05
- [x] NB-042: Heatmap for alpha=0.10
- [x] NB-043: Heatmap for alpha=0.20
- [x] NB-044: Reconstruction plots: pred vs true for FC at 60 Hz
- [x] NB-045: Reconstruction plots: pred vs true for RNN at 200 Hz
- [x] NB-046: Reconstruction plots: pred vs true for LSTM at 20 Hz
- [x] NB-047: Bar plot: best test MSE per arch
- [x] NB-048: Test MSE vs noise level line plot
- [x] NB-049: R² score table
- [x] NB-050: Discussion of where each arch shines/struggles

### 15f — Sensitivity Analysis OAT [5]
- [x] NB-051: Hidden size OAT plot (3 arches overlaid)
- [x] NB-052: # layers OAT plot
- [x] NB-053: Dropout OAT plot
- [x] NB-054: Learning rate OAT plot (log scale x)
- [x] NB-055: Discussion of which hyperparam matters most per arch

### 15g — Hypothesis Test [3]
- [x] NB-056: H1 verdict: paired test results, effect size, CI
- [x] NB-057: H2 verdict: paired test results, effect size, CI
- [x] NB-058: H3 verdict + summary table

### 15h — Conclusion [2]
- [x] NB-059: Reflective conclusion: what worked, what surprised, what next
- [x] NB-060: Acknowledgment of AI assistance per syllabus

## Phase 16 — README (P0) [30 tasks]

- [x] RDM-001: Create `README.md` with project title + 1-line tagline
- [x] RDM-002: Add badge row (python version, license, ruff, pytest)
- [x] RDM-003: Add Table of Contents
- [x] RDM-004: Section: Overview
- [x] RDM-005: Section: The Hypothesis (H1, H2, H3)
- [x] RDM-006: Section: Architecture (small diagram or ASCII)
- [x] RDM-007: Section: Installation (uv + clone + uv sync)
- [x] RDM-008: Section: Quick Start (single command produces results)
- [x] RDM-009: Section: Configuration (all keys explained)
- [x] RDM-010: Section: Usage / CLI subcommands
- [x] RDM-011: Section: Examples (3 worked examples)
- [x] RDM-012: Section: Project Structure (tree)
- [x] RDM-013: Section: Running Tests (uv run pytest --cov)
- [x] RDM-014: Section: Linting (uv run ruff check)
- [x] RDM-015: Section: Notebook (how to open and run analysis.ipynb)
- [x] RDM-016: Section: Extending the project (adding a new model via registry)
- [x] RDM-017: Section: Troubleshooting / common issues
- [x] RDM-018: Section: Contribution Guidelines
- [x] RDM-019: Section: License (MIT)
- [x] RDM-020: Section: Credits / third-party
- [x] RDM-021: Section: AI assistance acknowledgment (per syllabus)
- [x] RDM-022: Section: Citation (BibTeX-ish)
- [x] RDM-023: Reference PRD/PLAN/TODO docs
- [x] RDM-024: Reference per-mechanism PRDs
- [x] RDM-025: Reference PROMPTS.md
- [ ] RDM-026: Add screenshots/plots from results/figs/
- [x] RDM-027: Add link to GitHub repo
- [x] RDM-028: Add author / contact
- [x] RDM-029: Add ISO/IEC 25010 brief mention
- [x] RDM-030: Final read-through, fix typos

## Phase 17 — Documentation Polish (P1) [25 tasks]

- [x] DOC-001: Write `docs/PROMPTS.md` with full prompt log + meta-reflections
- [x] DOC-002: Write `docs/SUBMISSION_CHECKLIST.md` with all rubric items
- [x] DOC-003: Verify all per-mechanism PRDs are present (dataset, fc, rnn, lstm, training, evaluation)
- [x] DOC-004: Update PRD timeline if shifted
- [x] DOC-005: Update PLAN risks/mitigations from real experience
- [x] DOC-006: Mark TODO items [x] as completed throughout (continuous)
- [x] DOC-007: Add `docs/diagrams/c4_context.md` (mermaid or ASCII)
- [x] DOC-008: Add `docs/diagrams/c4_container.md`
- [x] DOC-009: Add `docs/diagrams/c4_component.md`
- [x] DOC-010: Add `docs/diagrams/uml_dataset_class.md`
- [x] DOC-011: Add `docs/diagrams/uml_model_hierarchy.md`
- [x] DOC-012: Add `docs/diagrams/sequence_train.md`
- [x] DOC-013: Final ADR audit — all 10 present and meaningful
- [x] DOC-014: Verify per-mechanism PRDs each have I/O contract + alternatives + success criteria
- [x] DOC-015: Verify ISO/IEC 25010 paragraph in PLAN.md (done)
- [x] DOC-016: Add CHANGELOG.md (1.00 entry)
- [x] DOC-017: Add LICENSE (MIT)
- [x] DOC-018: Verify all docs cross-link correctly
- [x] DOC-019: Verify no broken markdown links
- [x] DOC-020: Spell-check all docs
- [x] DOC-021: Resolve all `<!-- TBD -->` markers (or document why deferred)
- [x] DOC-022: Update version stamps if any doc bumped
- [x] DOC-023: Audit: PRD requirements ↔ TODO tasks (Verify Pass)
- [x] DOC-024: Add missing TODO items found in audit
- [x] DOC-025: Sign-off comment at top of each doc

## Phase 18.5 — Verify-Pass Gap Fillers (P1) [40 tasks]

Found during the explicit Verify Pass audit (PRD requirements ↔ TODO coverage).

- [ ] VRF-001: Add `scripts/check_no_hardcoded.py` greping for hardcoded URLs / paths / numbers in src/
- [ ] VRF-002: Unit test for VRF-001 script
- [ ] VRF-003: Add `scripts/render_notebook.py` exporting `analysis.ipynb` to PDF + HTML
- [ ] VRF-004: Verify VRF-003 output rendered LaTeX equations correctly
- [ ] VRF-005: Add `scripts/dataset_hash.py` to print SHA256 of generated arrays for reproducibility
- [ ] VRF-006: Run VRF-005 on two seeds, confirm hash equality on same seed
- [x] VRF-007: Add `scripts/run_ci.sh` chaining lint + test + file-size + secret scan
- [x] VRF-008: Add `Makefile` target `make ci` invoking VRF-007
- [x] VRF-009: Run `make ci` — must pass before each phase commit
- [x] VRF-010: Add `LICENSE` file (MIT) at repo root
- [x] VRF-011: Add `CITATION.cff` (or BibTeX in README) for academic reference
- [x] VRF-012: Add `CHANGELOG.md` with v1.00 entry
- [ ] VRF-013: Add `assets/architecture.png` (export of C4 container diagram)
- [ ] VRF-014: Add `assets/loss_curve_example.png` (montage from results/)
- [ ] VRF-015: Add `assets/heatmap_example.png` (best heatmap from results/)
- [ ] VRF-016: Embed assets in README RDM-026 (verify they render)
- [x] VRF-017: Verify `git log --oneline | wc -l ≥ 50` before push
- [x] VRF-018: Add `scripts/preflight_submission.py` checking all rubric items
- [x] VRF-019: Run preflight script and resolve every failure
- [x] VRF-020: Submission rehearsal: render PDF locally, eyeball it
- [x] VRF-021: Edge: notebook reads CSV with no rows → graceful "no data yet" message
- [x] VRF-022: Edge: training_service called twice with same seed → identical run_id collision handled
- [x] VRF-023: Edge: gatekeeper called for non-existent service → falls back to default limits cleanly
- [x] VRF-024: Performance benchmark: log per-arch param count vs final loss table
- [x] VRF-025: Performance benchmark: log wall-clock per epoch table
- [x] VRF-026: AI assistance acknowledgment in notebook conclusion (NB-060) — verify substantive paragraph
- [x] VRF-027: AI assistance acknowledgment in README (RDM-021) — verify substantive paragraph
- [x] VRF-028: PROMPTS.md has at least 10 distinct prompt entries with meta-reflections
- [x] VRF-029: PROMPTS.md links to specific commits / files for traceability
- [x] VRF-030: Verify `__all__` exposed only public symbols in every package `__init__.py`
- [x] VRF-031: Verify `__version__ = "1.00"` in `src/sinusoid_extractor/__init__.py`
- [x] VRF-032: Verify `setup.json` "version" == "1.00"
- [x] VRF-033: Verify `rate_limits.json` "version" == "1.00"
- [x] VRF-034: Verify all per-mechanism PRDs cross-reference PRD.md FR IDs
- [x] VRF-035: Verify SUBMISSION_CHECKLIST.md is fully ticked before upload
- [x] VRF-036: Confirm `pyproject.toml` author field includes Salah Qadah
- [x] VRF-037: Confirm `pyproject.toml` license field MIT
- [ ] VRF-038: Confirm GitHub repo description filled
- [ ] VRF-039: Confirm GitHub repo topics include `pytorch`, `lstm`, `rnn`, `university-of-haifa`
- [ ] VRF-040: After push, verify `gh repo view` shows public visibility

## Phase 18 — Submission (P0) [20 tasks]

- [ ] SUB-001: Confirm group code with user
- [ ] SUB-002: Confirm solo/pair status with user
- [ ] SUB-003: Confirm self-grade with user (recalibrate to actual quality)
- [ ] SUB-004: Confirm permission email sent if solo
- [ ] SUB-005: Create GitHub repo `salah-dev-stu/sinusoid-extractor` (PUBLIC)
- [ ] SUB-006: `git remote add origin git@github.com:salah-dev-stu/sinusoid-extractor.git`
- [ ] SUB-007: `git push -u origin main`
- [ ] SUB-008: Tag `v1.00` and push tag
- [ ] SUB-009: Verify repo accessible publicly
- [ ] SUB-010: Add `rmisegal@gmail.com` as collaborator (defensive — public repo doesn't require but lecturer asked)
- [ ] SUB-011: Open `uoh-rl07-ex01.docx`
- [ ] SUB-012: Fill: exercise number = 01
- [ ] SUB-013: Fill: group ID code (8 chars)
- [ ] SUB-014: Fill: self-grade
- [ ] SUB-015: Fill: student 1 (Salah Qadah, ID 323039974, En + He names)
- [ ] SUB-016: Fill: student 2 (or leave blank if solo)
- [ ] SUB-017: Fill: GitHub link
- [ ] SUB-018: Fill: late submission yes/no
- [ ] SUB-019: Save as PDF named `<group_code>-ex01.pdf`
- [ ] SUB-020: Upload PDF to Moodle (https://mw26.haifa.ac.il/mod/assign/view.php?id=255044)

---

## Verify-Pass Coverage Map (PRD ↔ TODO)

This section is filled in during the explicit "Verify Pass" stage (after all docs drafted). Map each PRD requirement to the TODO IDs that satisfy it. Add tasks for any orphan requirements.

| PRD ID | Covered by TODO | Notes |
|---|---|---|
| FR-DAT-1 | SIG-007, SIG-008 | pure sines at 4 freqs |
| FR-DAT-2 | NOI-003, NOI-006 | per-signal noise |
| FR-DAT-3 | DAT-004 | combined as sum |
| FR-DAT-4 | DAT-006, PERS-002 | npz persistence |
| FR-DAT-5 | SPL-005 | (C, x, y) tuples |
| FR-DAT-6 | DAT-005, SPL-005 | configurable splits |
| FR-DAT-7 | TUT-001, FIX-007 | seed |
| FR-DAT-8 | EXP-004, SW-003 | noise sweep family |
| FR-MOD-1 | BASE-003, FC-005, RNN-006, LSTM-006 | input/output dims |
| FR-MOD-2 | FC-001..030 | FC implementation |
| FR-MOD-3 | RNN-001..040 | RNN implementation |
| FR-MOD-4 | LSTM-001..045 | LSTM implementation |
| FR-MOD-5 | REG-001..017 | registry/factory |
| FR-TRN-1 | LOSS-001..010 | summed MSE |
| FR-TRN-2 | OPT-001..010 | optimizer |
| FR-TRN-3 | LOOP-002, ES-001..015 | early stopping |
| FR-TRN-4 | TSV-008..011 | persistence |
| FR-TRN-5 | HOOK-001..005, LOOP-007 | lifecycle hooks |
| FR-TRN-6 | TSV-006 | DataLoader workers |
| FR-EVL-1 | EV-003..005 | per-cell metrics |
| FR-EVL-2 | REC-001..010, PLT-003 | reconstruction plots |
| FR-EVL-3 | PLT-004, NB-041..043 | heatmaps |
| FR-EVL-4 | EV-007 | persistence |
| FR-SEN-1 | SW-004 | OAT sweep |
| FR-SEN-2 | SW-005 | sensitivity.csv |
| FR-SEN-3 | NB-051..055 | OAT plots |
| FR-SDK-1 | SDK-001..040 | SDK class |
| FR-SDK-2 | SDK-006..012 | SDK methods |
| FR-SDK-3 | CLI-001..030 | thin CLI |
| FR-CFG-1 | CFG-001..040 | setup.json |
| FR-CFG-2 | CFG-002, GATE-004 | rate_limits.json |
| FR-CFG-3 | CFG-003 | logging |
| FR-CFG-4 | VER-008, CFG-011 | version check |
| FR-NB-1 | NB-001..060 | notebook |
| FR-NB-2 | NB-021..030 | LaTeX equations |
| FR-NB-3 | NB-001..060 | section order |
| NFR-1..NFR-13 | covered by structural tasks throughout | rubric rules |

---

## Definition of Done (Project)

- All 1042 tasks above are `[x]`.
- `uv run ruff check src/ tests/` returns 0.
- `uv run pytest --cov` reports ≥ 85%.
- `scripts/check_file_lines.py` reports 0 violations.
- `git log --oneline | wc -l` ≥ 50 commits.
- GitHub repo public, shared with `rmisegal@gmail.com`, tagged `v1.00`.
- Notebook executes end-to-end with no errors.
- Submission PDF uploaded to Moodle by 2026-05-07 23:59.
- All TBDs in PRD/PLAN resolved.
