# TODO — Sinusoid Extractor (HW1)

| Field | Value |
|---|---|
| Document version | 1.00 |
| Total tasks | 1002 |
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
- [ ] SETUP-011: Create `pyproject.toml` with `[project]`, `[tool.uv]`, `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report]`
- [ ] SETUP-012: Set Python version to `>=3.10` in `pyproject.toml`
- [ ] SETUP-013: Set ruff line-length 100, target-version py310, select `E,F,W,I,N,UP,B,C4,SIM`, ignore `E501`
- [ ] SETUP-014: Set `fail_under = 85` in coverage config
- [ ] SETUP-015: Set `omit = ["src/**/main.py", "*/tests/*"]` in coverage
- [ ] SETUP-016: Run `uv sync` and verify lock file is created
- [ ] SETUP-017: `uv add torch numpy matplotlib seaborn jupyter pydantic python-dotenv`
- [ ] SETUP-018: `uv add --dev pytest pytest-cov ruff ipykernel`
- [ ] SETUP-019: Verify `uv.lock` exists and is tracked
- [ ] SETUP-020: Create `src/sinusoid_extractor/__init__.py` with `__version__ = "1.00"` and `__all__`
- [ ] SETUP-021: Create `src/sinusoid_extractor/sdk/__init__.py`
- [ ] SETUP-022: Create `src/sinusoid_extractor/services/__init__.py`
- [ ] SETUP-023: Create `src/sinusoid_extractor/models/__init__.py`
- [ ] SETUP-024: Create `src/sinusoid_extractor/shared/__init__.py`
- [ ] SETUP-025: Create `tests/conftest.py` with shared seed fixture
- [ ] SETUP-026: Create `tests/unit/__init__.py`
- [ ] SETUP-027: Create `tests/integration/__init__.py`
- [ ] SETUP-028: Mirror src/ tree under `tests/unit/` (sdk/, services/, models/, shared/)
- [ ] SETUP-029: Create `config/` directory
- [ ] SETUP-030: Create `data/raw/` and `data/processed/` directories with `.gitkeep`
- [ ] SETUP-031: Create `results/` directory with `.gitkeep`
- [ ] SETUP-032: Create `notebooks/` directory with `.gitkeep`
- [ ] SETUP-033: Create `assets/` directory for diagrams/screenshots
- [ ] SETUP-034: Create `scripts/` directory for utility scripts
- [ ] SETUP-035: Create `logs/` directory with `.gitkeep` (logs git-ignored)
- [ ] SETUP-036: Run `uv run ruff check` baseline and confirm passes on empty src
- [ ] SETUP-037: Run `uv run pytest` baseline and confirm "no tests collected"
- [ ] SETUP-038: Add `scripts/check_file_lines.py` enforcing ≤150 LoC per .py
- [ ] SETUP-039: Add `Makefile` (or `justfile`) with `lint`, `test`, `check`, `notebook` targets
- [ ] SETUP-040: Verify `gh auth status` succeeds (user has gh installed)
- [ ] SETUP-041: Pre-create the GitHub repo skeleton plan (defer actual creation to push step)
- [ ] SETUP-042: Verify Python 3.10+ available via `uv python pin 3.11` (or 3.12)
- [ ] SETUP-043: Add `.python-version` file to pin interpreter
- [ ] SETUP-044: Confirm `torch` imports under uv: `uv run python -c "import torch; print(torch.__version__)"`
- [ ] SETUP-045: Confirm CPU device for training (no GPU on macOS arm64 by default)
- [ ] SETUP-046: Add `docs/ADRs/` directory (referenced by PLAN.md §4)
- [ ] SETUP-047: Write ADR-001 through ADR-010 stub files referencing PLAN.md summaries
- [ ] SETUP-048: Add `docs/diagrams/` directory for any image exports
- [ ] SETUP-049: Add `docs/SUBMISSION_CHECKLIST.md` skeleton
- [ ] SETUP-050: Initial commit of scaffolding (already done as part of PRD commit)

## Phase 1 — Configuration System (P0) [40 tasks]

- [ ] CFG-001: Write `config/setup.json` v1.00 per PLAN.md §5.1 schema
- [ ] CFG-002: Write `config/rate_limits.json` v1.00 per PLAN.md §5.2 (HW1 stub)
- [ ] CFG-003: Write `config/logging_config.json` v1.00 (Python logging dict-config)
- [ ] CFG-004: Create `src/sinusoid_extractor/shared/config.py` (loader)
- [ ] CFG-005: Implement `Config.load(path: Path) -> dict` using stdlib `json`
- [ ] CFG-006: Implement `Config.validate(raw: dict) -> Config` with schema check
- [ ] CFG-007: Add typed dataclasses for sub-sections (DatasetConfig, TrainingConfig, ModelConfigs, ExperimentConfig, OatConfig, PathsConfig)
- [ ] CFG-008: Implement `Config.get(key: str, default: Any) -> Any` for dotted access
- [ ] CFG-009: Add `Config.from_env() -> dict` for `os.environ.get(...)` overrides
- [ ] CFG-010: Add error class `ConfigError(Exception)` for invalid configs
- [ ] CFG-011: Add `Config.check_versions(code_v: str, cfg_v: str) -> None` (warns on mismatch)
- [ ] CFG-012: Unit test: load valid setup.json → returns dataclass tree
- [ ] CFG-013: Unit test: load missing required key → raises ConfigError
- [ ] CFG-014: Unit test: load malformed JSON → raises ConfigError
- [ ] CFG-015: Unit test: env override applies for SINUSOID_SEED
- [ ] CFG-016: Unit test: version mismatch logs warning, does not raise
- [ ] CFG-017: Unit test: defaults are returned for missing optional keys
- [ ] CFG-018: Unit test: dataset config validates frequencies_hz length == 4
- [ ] CFG-019: Unit test: training config validates lr > 0
- [ ] CFG-020: Unit test: model configs validate hidden_size > 0
- [ ] CFG-021: Unit test: oat sweep config has the four required keys
- [ ] CFG-022: Unit test: paths config creates dirs lazily
- [ ] CFG-023: Add `Config.dump(path: Path) -> None` for round-trip
- [ ] CFG-024: Unit test: dump → load round-trip preserves structure
- [ ] CFG-025: Add `_comment` field tolerance (loader ignores keys starting with `_`)
- [ ] CFG-026: Unit test: comment fields ignored
- [ ] CFG-027: Add fixture `tests/conftest.py::sample_config` returning a dict
- [ ] CFG-028: Add fixture `tests/conftest.py::config_path` returning tmp file
- [ ] CFG-029: Document config schema in PRD (already done — verify)
- [ ] CFG-030: Add CLI flag `--config PATH` to override default `config/setup.json`
- [ ] CFG-031: Implement noise-level type coercion (allow ints in JSON)
- [ ] CFG-032: Implement seed-list type coercion
- [ ] CFG-033: Validate experiment.architectures ⊆ {"fc","rnn","lstm"}
- [ ] CFG-034: Unit test for the coercions
- [ ] CFG-035: Unit test for arch whitelist
- [ ] CFG-036: Add `Config.print_summary() -> str` for log header
- [ ] CFG-037: Unit test print_summary returns non-empty
- [ ] CFG-038: Add YAML notice — explicitly say "JSON only, see ADR-006"
- [ ] CFG-039: Add type hints + full docstrings throughout config.py
- [ ] CFG-040: Run ruff on shared/config.py → 0 errors

## Phase 2 — Versioning & Shared Utilities (P0) [30 tasks]

- [ ] VER-001: Create `src/sinusoid_extractor/shared/version.py` with `__version__ = "1.00"`
- [ ] VER-002: Add `Version.bump(field: str = "patch") -> str` (patch = +0.01)
- [ ] VER-003: Add `Version.parse(s: str) -> tuple[int,int]`
- [ ] VER-004: Unit test: bump 1.00 → 1.01
- [ ] VER-005: Unit test: bump 1.99 → 2.00 (overflow handling)
- [ ] VER-006: Unit test: parse rejects non-MAJOR.MINOR strings
- [ ] VER-007: Wire `__version__` into `src/sinusoid_extractor/__init__.py`
- [ ] VER-008: Wire version check into SDK constructor
- [ ] LOG-001: Create `src/sinusoid_extractor/shared/logger.py`
- [ ] LOG-002: Implement `get_logger(name: str) -> logging.Logger` from `config/logging_config.json`
- [ ] LOG-003: Add structured key=value formatter
- [ ] LOG-004: Unit test: logger respects level from config
- [ ] LOG-005: Unit test: logger writes to file when configured
- [ ] LOG-006: Add log line for each SDK method entry/exit
- [ ] PERS-001: Create `src/sinusoid_extractor/shared/persistence.py`
- [ ] PERS-002: Implement `save_npz(path, **arrays) -> None`
- [ ] PERS-003: Implement `load_npz(path) -> dict[str, np.ndarray]`
- [ ] PERS-004: Implement `save_json(path, payload: dict) -> None`
- [ ] PERS-005: Implement `load_json(path) -> dict`
- [ ] PERS-006: Implement `save_csv_row(path, row: dict, header_if_new=True)`
- [ ] PERS-007: Unit test save/load npz round-trip
- [ ] PERS-008: Unit test save/load json round-trip
- [ ] PERS-009: Unit test save_csv_row appends rows
- [ ] PERS-010: Add `ensure_dir(path) -> Path` helper
- [ ] PERS-011: Unit test ensure_dir creates nested
- [ ] HOOK-001: Create `src/sinusoid_extractor/shared/hooks.py`
- [ ] HOOK-002: Implement `HookRegistry` class with `register(event, fn)` and `fire(event, **ctx)`
- [ ] HOOK-003: Define event Enum: BEFORE_TRAIN, AFTER_EPOCH, AFTER_TRAIN, BEFORE_EVAL, AFTER_EVAL
- [ ] HOOK-004: Unit test: registered hooks fire in registration order
- [ ] HOOK-005: Unit test: unknown event raises KeyError

## Phase 3 — API Gatekeeper & Wave Queue (Stubs) (P1) [30 tasks]

- [ ] GATE-001: Create `src/sinusoid_extractor/shared/gatekeeper.py`
- [ ] GATE-002: Define `Gatekeeper` ABC with `call(service: str, payload: dict) -> dict`
- [ ] GATE-003: Implement `NoopGatekeeper(Gatekeeper)` returning `{"status": "noop"}`
- [ ] GATE-004: Load rate limits from `config/rate_limits.json` at init
- [ ] GATE-005: Implement `_check_rate(service: str)` placeholder enforcing the JSON limits
- [ ] GATE-006: Add structured logging on every call attempt
- [ ] GATE-007: Unit test: noop gatekeeper returns noop status
- [ ] GATE-008: Unit test: rate limits loaded from config (mocked json)
- [ ] GATE-009: Unit test: undefined service falls back to `default` limits
- [ ] GATE-010: Unit test: missing rate_limits.json raises ConfigError
- [ ] GATE-011: Unit test: zero requests_per_minute is rejected at init
- [ ] GATE-012: Document gatekeeper purpose in PLAN.md (done) — verify
- [ ] QUE-001: Create `src/sinusoid_extractor/shared/queue_manager.py`
- [ ] QUE-002: Implement `WaveQueue` (FIFO) using `collections.deque`
- [ ] QUE-003: Implement `enqueue(item)` and `dequeue() -> Optional[item]`
- [ ] QUE-004: Implement `size() -> int` and `is_full() -> bool`
- [ ] QUE-005: Implement `BackpressureError` raised when full
- [ ] QUE-006: Add `max_size` from config
- [ ] QUE-007: Unit test: enqueue/dequeue FIFO order
- [ ] QUE-008: Unit test: full queue raises BackpressureError on enqueue
- [ ] QUE-009: Unit test: empty dequeue returns None
- [ ] QUE-010: Unit test: size tracking correct
- [ ] QUE-011: Unit test: wave queue thread-safe (using threading.Lock)
- [ ] GATE-013: Unit test: gatekeeper integration with WaveQueue (smoke)
- [ ] GATE-014: Add ADR-011 stub: "Gatekeeper noop in HW1; full impl in HW2+"
- [ ] GATE-015: Unit test rate-limit JSON keys validated
- [ ] GATE-016: Unit test: retries config respected (mocked clock)
- [ ] GATE-017: Verify gatekeeper imported by SDK (smoke)
- [ ] GATE-018: Unit test: gatekeeper has no hardcoded limits in code
- [ ] GATE-019: Lint clean
- [ ] GATE-020: Coverage ≥ 85% for gatekeeper module

## Phase 4 — Constants & Enums (P0) [20 tasks]

- [ ] CONST-001: Create `src/sinusoid_extractor/constants.py`
- [ ] CONST-002: Define `FIXED_FREQUENCIES_HZ: tuple[int, ...] = (1, 3, 5, 7)`
- [ ] CONST-003: Define `INPUT_DIM = 14` (4 one-hot + 10 window)
- [ ] CONST-004: Define `OUTPUT_DIM = 10`
- [ ] CONST-005: Define `CONTEXT_WINDOW = 10`
- [ ] CONST-006: Define `class Architecture(StrEnum)`: FC, RNN, LSTM
- [ ] CONST-007: Define `class Optimizer(StrEnum)`: ADAM, RMSPROP
- [ ] CONST-008: Define `class HookEvent(StrEnum)`: BEFORE_TRAIN, AFTER_EPOCH, AFTER_TRAIN, BEFORE_EVAL, AFTER_EVAL
- [ ] CONST-009: Define `class NoiseDistribution(StrEnum)`: UNIFORM, GAUSSIAN
- [ ] CONST-010: Define `DEFAULT_SEED = 42`
- [ ] CONST-011: Document each constant with a one-line docstring at module top
- [ ] CONST-012: Unit test: FIXED_FREQUENCIES_HZ has length 4
- [ ] CONST-013: Unit test: INPUT_DIM == 14
- [ ] CONST-014: Unit test: OUTPUT_DIM == 10
- [ ] CONST-015: Unit test: Architecture members cover all three models
- [ ] CONST-016: Unit test: Optimizer members include ADAM
- [ ] CONST-017: Unit test: HookEvent has the five expected events
- [ ] CONST-018: Unit test: NoiseDistribution has UNIFORM
- [ ] CONST-019: Lint clean
- [ ] CONST-020: Verify no hardcoded values use literals where constants exist (grep)

## Phase 5 — Dataset Service (P0) [120 tasks]

### 5a — SignalGenerator [25]
- [ ] SIG-001: Create `services/signal_generator.py`
- [ ] SIG-002: Define `SignalGenerator` class with `__init__(amplitude, sampling_rate_hz, duration_seconds)`
- [ ] SIG-003: Validate amplitude > 0
- [ ] SIG-004: Validate sampling_rate_hz > 0
- [ ] SIG-005: Validate duration_seconds > 0
- [ ] SIG-006: Implement `_time_axis() -> np.ndarray` returning `t = np.arange(N)/Fs`
- [ ] SIG-007: Implement `pure(frequency_hz, phase=0.0) -> np.ndarray`
- [ ] SIG-008: Implement `pure_all(frequencies) -> dict[freq, ndarray]`
- [ ] SIG-009: Unit test: pure(1Hz) length == Fs * T
- [ ] SIG-010: Unit test: pure(0Hz) is constant
- [ ] SIG-011: Unit test: pure has zero mean over integer cycles
- [ ] SIG-012: Unit test: pure phase shift offsets sample 0
- [ ] SIG-013: Unit test: pure_all returns 4 arrays for 4 frequencies
- [ ] SIG-014: Property test: pure peak ≈ amplitude
- [ ] SIG-015: Property test: amplitude scales linearly
- [ ] SIG-016: Add type hints + docstrings
- [ ] SIG-017: Building Block doc comment: Input/Output/Setup
- [ ] SIG-018: Lint clean for signal_generator.py
- [ ] SIG-019: Coverage ≥ 90% for signal_generator
- [ ] SIG-020: Property test: increasing freq increases zero-crossings
- [ ] SIG-021: Reject non-finite frequency
- [ ] SIG-022: Unit test: invalid amplitude raises ValueError
- [ ] SIG-023: Unit test: invalid Fs raises ValueError
- [ ] SIG-024: Unit test: invalid duration raises ValueError
- [ ] SIG-025: Verify file ≤ 150 LoC

### 5b — NoiseModel [25]
- [ ] NOI-001: Create `services/noise_model.py`
- [ ] NOI-002: Define `NoiseModel` class with `__init__(rng: np.random.Generator)`
- [ ] NOI-003: Implement `apply(pure: np.ndarray, alpha: float, distribution: NoiseDistribution = UNIFORM) -> np.ndarray`
- [ ] NOI-004: Per-sample amplitude noise: `pure * (1 + uniform(-alpha, +alpha))`
- [ ] NOI-005: Per-sample phase noise via `pure(t + dphi/(2*pi*f))`? — instead implement phase noise at the *generator* level: rebuild the sine with random phase per realization
- [ ] NOI-006: Refactor: `apply_amplitude_noise(pure, alpha, distribution)` and `random_phase() -> float in [0, 2*pi]`
- [ ] NOI-007: Unit test: apply_amplitude_noise returns same shape
- [ ] NOI-008: Unit test: amplitude noise mean ≈ 0 over many samples
- [ ] NOI-009: Unit test: amplitude noise bounded by ±alpha
- [ ] NOI-010: Unit test: random_phase in [0, 2*pi]
- [ ] NOI-011: Unit test: random_phase covers full range over 1000 draws
- [ ] NOI-012: Unit test: alpha=0 returns identity (no noise)
- [ ] NOI-013: Unit test: distribution=GAUSSIAN uses normal(0, alpha)
- [ ] NOI-014: Unit test: invalid distribution raises ValueError
- [ ] NOI-015: Unit test: invalid alpha < 0 raises ValueError
- [ ] NOI-016: Unit test: alpha > 1 logs warning (not standard)
- [ ] NOI-017: Building Block doc comment
- [ ] NOI-018: Lint clean
- [ ] NOI-019: Coverage ≥ 90%
- [ ] NOI-020: Property test: noise reproducible with same seed
- [ ] NOI-021: Property test: different seeds produce different noise
- [ ] NOI-022: Verify file ≤ 150 LoC
- [ ] NOI-023: Unit test: rng injection allows deterministic test
- [ ] NOI-024: Document choice of uniform per ADR-002
- [ ] NOI-025: Confirm phase noise = uniform(0, 2π) per IDEA.md

### 5c — Windower [20]
- [ ] WIN-001: Create `services/windower.py`
- [ ] WIN-002: Define `Windower(window_size: int, rng: np.random.Generator)`
- [ ] WIN-003: Implement `random_starts(n_total: int, n_windows: int) -> np.ndarray`
- [ ] WIN-004: Implement `disjoint_starts(n_total: int, n_train, n_val, n_test) -> tuple[ndarray, ndarray, ndarray]`
- [ ] WIN-005: Implement `extract(signal, starts) -> np.ndarray of shape (len(starts), window_size)`
- [ ] WIN-006: Unit test: extract shape (n, 10)
- [ ] WIN-007: Unit test: starts within [0, n_total - window_size]
- [ ] WIN-008: Unit test: disjoint_starts returns disjoint sets
- [ ] WIN-009: Unit test: window_size > n_total raises ValueError
- [ ] WIN-010: Unit test: zero starts returns empty array (n=0)
- [ ] WIN-011: Property test: window content matches signal at offset
- [ ] WIN-012: Property test: window_size = 1 returns single samples
- [ ] WIN-013: Building Block doc comment
- [ ] WIN-014: Lint clean
- [ ] WIN-015: Coverage ≥ 90%
- [ ] WIN-016: Verify file ≤ 150 LoC
- [ ] WIN-017: Unit test: rng deterministic
- [ ] WIN-018: Unit test: extract handles 2D signal (broadcast)
- [ ] WIN-019: Unit test: extract preserves dtype
- [ ] WIN-020: Document partitioning strategy in PRD_dataset.md

### 5d — Splitter [20]
- [ ] SPL-001: Create `services/splitter.py`
- [ ] SPL-002: Define `Splitter` class
- [ ] SPL-003: Implement `assign_one_hot(n_examples: int, n_classes: int = 4, rng) -> np.ndarray (n,4)`
- [ ] SPL-004: Implement `select_target(pure_signals: dict, one_hot: np.ndarray) -> ndarray`
- [ ] SPL-005: Implement `build_tuples(combined, pure_dict, starts, one_hots) -> (C, x, y)`
- [ ] SPL-006: Unit test: one_hot rows sum to 1
- [ ] SPL-007: Unit test: one_hot uniform distribution over classes
- [ ] SPL-008: Unit test: select_target picks correct sine
- [ ] SPL-009: Unit test: build_tuples shapes correct
- [ ] SPL-010: Unit test: build_tuples y matches pure at given starts
- [ ] SPL-011: Unit test: build_tuples x = window from combined
- [ ] SPL-012: Property test: y matches pure for the selected class
- [ ] SPL-013: Property test: x sourced from combined, not pure
- [ ] SPL-014: Building Block doc comment
- [ ] SPL-015: Lint clean
- [ ] SPL-016: Coverage ≥ 90%
- [ ] SPL-017: Verify file ≤ 150 LoC
- [ ] SPL-018: Unit test: select_target with 2D one_hot
- [ ] SPL-019: Unit test: build_tuples with empty starts returns empty arrays
- [ ] SPL-020: Document split strategy in PRD_dataset.md

### 5e — DatasetService Orchestrator [15]
- [ ] DAT-001: Create `services/dataset_service.py`
- [ ] DAT-002: Define `DatasetService(config: DatasetConfig)`
- [ ] DAT-003: Compose SignalGenerator, NoiseModel, Windower, Splitter
- [ ] DAT-004: Implement `build_raw_signals(alpha, seed) -> dict (4 pure, 4 noisy, 1 combined)`
- [ ] DAT-005: Implement `build_tuples(raw, n_train, n_val, n_test, seed) -> DataBundle`
- [ ] DAT-006: Implement `persist(raw, path)` and `load_raw(path) -> dict`
- [ ] DAT-007: Implement `generate(alpha, seed) -> DatasetHandle` end-to-end
- [ ] DAT-008: Unit test: generate returns 9 raw vectors of length 10000
- [ ] DAT-009: Unit test: generate returns 5000 train tuples
- [ ] DAT-010: Unit test: persisted npz loadable
- [ ] DAT-011: Integration test: alpha=0 gives noiseless combined signal
- [ ] DAT-012: Integration test: alpha=0.1 statistics match expectations
- [ ] DAT-013: Lint clean
- [ ] DAT-014: Coverage ≥ 90%
- [ ] DAT-015: Verify file ≤ 150 LoC

### 5f — DataBundle / Dataset (PyTorch) [15]
- [ ] DBP-001: Create `services/data_bundle.py` with TypedDict / dataclass
- [ ] DBP-002: Create `services/torch_dataset.py` with `SinusoidWindowDataset(torch.utils.data.Dataset)`
- [ ] DBP-003: Implement `__len__` and `__getitem__` returning (input_vec, target_vec)
- [ ] DBP-004: Concatenate one-hot + window into 14-dim tensor for FC
- [ ] DBP-005: For RNN/LSTM: build (10, 5) sequence (sample + 4-dim one-hot per timestep)
- [ ] DBP-006: Add `arch_view: Architecture` parameter to switch input shaping
- [ ] DBP-007: Unit test: len == n_examples
- [ ] DBP-008: Unit test: FC view returns (14,) tensor
- [ ] DBP-009: Unit test: RNN view returns (10, 5) tensor
- [ ] DBP-010: Unit test: LSTM view same as RNN view
- [ ] DBP-011: Unit test: targets shape (10,)
- [ ] DBP-012: Unit test: dtype float32
- [ ] DBP-013: Lint clean
- [ ] DBP-014: Coverage ≥ 90%
- [ ] DBP-015: Verify file ≤ 150 LoC

## Phase 6 — Models (P0) [150 tasks]

### 6a — BaseExtractor + Mixins + Registry [35]
- [ ] BASE-001: Create `models/base_extractor.py`
- [ ] BASE-002: Define `BaseExtractor(nn.Module, ParamCountMixin, SaveLoadMixin, ABC)`
- [ ] BASE-003: Add `INPUT_DIM = 14`, `OUTPUT_DIM = 10` class vars
- [ ] BASE-004: Define `forward(batch)` as abstract
- [ ] BASE-005: Define `architecture_name() -> str` as abstract
- [ ] BASE-006: Add `to_device(device)` shared helper
- [ ] BASE-007: Unit test: BaseExtractor cannot be instantiated directly
- [ ] BASE-008: Unit test: subclass without forward fails
- [ ] MIX-001: Create `models/mixins.py`
- [ ] MIX-002: Define `ParamCountMixin.count_parameters() -> int`
- [ ] MIX-003: Define `SaveLoadMixin.save(path)` and `load(path)`
- [ ] MIX-004: Unit test: count_parameters returns correct count for nn.Linear
- [ ] MIX-005: Unit test: save/load round-trip preserves weights
- [ ] MIX-006: Unit test: load on wrong arch raises clear error
- [ ] MIX-007: Mixins are self-testable in isolation (per RULES.md §6)
- [ ] MIX-008: Lint clean
- [ ] MIX-009: Coverage ≥ 90%
- [ ] MIX-010: Verify file ≤ 150 LoC
- [ ] REG-001: Create `models/registry.py`
- [ ] REG-002: Implement `ModelRegistry` with `_registry: dict[str, type[BaseExtractor]]`
- [ ] REG-003: Implement `register(name)` decorator
- [ ] REG-004: Implement `build(name, config) -> BaseExtractor`
- [ ] REG-005: Implement `available() -> list[str]`
- [ ] REG-006: Unit test: register adds entry
- [ ] REG-007: Unit test: duplicate registration raises
- [ ] REG-008: Unit test: build with unknown name raises ValueError
- [ ] REG-009: Unit test: available lists all registered
- [ ] REG-010: Document plugin pattern in PLAN.md (done)
- [ ] REG-011: Lint clean
- [ ] REG-012: Coverage ≥ 90%
- [ ] REG-013: Verify file ≤ 150 LoC
- [ ] REG-014: Auto-register fc/rnn/lstm via `models/__init__.py` imports
- [ ] REG-015: Unit test: importing models package registers all three
- [ ] REG-016: Property: registry survives module reimport
- [ ] REG-017: Add type alias `ModelFactory = Callable[[ModelConfig], BaseExtractor]`

### 6b — FC Model [30]
- [ ] FC-001: Create `models/fc_model.py`
- [ ] FC-002: Define `FCExtractor(BaseExtractor)`
- [ ] FC-003: `__init__(input_dim, output_dim, hidden_size, num_layers, dropout)`
- [ ] FC-004: Build `nn.Sequential` with Linear → ReLU → Dropout layers
- [ ] FC-005: Final layer linear (no activation)
- [ ] FC-006: Implement `forward(x: Tensor[B, 14]) -> Tensor[B, 10]`
- [ ] FC-007: Register as `@register("fc")`
- [ ] FC-008: Unit test: forward produces (B, 10)
- [ ] FC-009: Unit test: forward differentiable (loss.backward works)
- [ ] FC-010: Unit test: 2 hidden layers count parameters correctly
- [ ] FC-011: Unit test: 3 hidden layers
- [ ] FC-012: Unit test: dropout=0 deterministic in eval mode
- [ ] FC-013: Unit test: hidden_size=128 expected param count
- [ ] FC-014: Unit test: hidden_size=256 expected param count
- [ ] FC-015: Unit test: invalid num_layers raises
- [ ] FC-016: Unit test: invalid hidden_size raises
- [ ] FC-017: Unit test: dropout in [0, 1) only
- [ ] FC-018: Unit test: gradient flows through all layers
- [ ] FC-019: Unit test: save/load round-trip
- [ ] FC-020: Unit test: forward with batch=1 works
- [ ] FC-021: Unit test: forward with batch=64 works
- [ ] FC-022: Unit test: cpu/cpu round trip
- [ ] FC-023: Building Block doc comment
- [ ] FC-024: Lint clean
- [ ] FC-025: Coverage ≥ 90%
- [ ] FC-026: Verify file ≤ 150 LoC
- [ ] FC-027: Add architecture_name() returns "fc"
- [ ] FC-028: Unit test: registry.build("fc", cfg) returns FCExtractor
- [ ] FC-029: Verify input_dim/output_dim wired from class vars
- [ ] FC-030: Smoke test: train 1 epoch on tiny dataset, loss decreases

### 6c — RNN Model [40]
- [ ] RNN-001: Create `models/rnn_model.py`
- [ ] RNN-002: Define `RNNExtractor(BaseExtractor)`
- [ ] RNN-003: `__init__(input_dim_per_step, output_dim, hidden_size, num_layers, dropout)`
- [ ] RNN-004: Use `nn.RNN(input_size=5, hidden_size, num_layers, nonlinearity='tanh', batch_first=True, dropout)`
- [ ] RNN-005: Final `nn.Linear(hidden_size, 10)` mapping last hidden to output
- [ ] RNN-006: Implement `forward(x: Tensor[B, 10, 5]) -> Tensor[B, 10]`
- [ ] RNN-007: Take last timestep output: `out[:, -1, :]` then linear to 10
- [ ] RNN-008: Register as `@register("rnn")`
- [ ] RNN-009: Unit test: forward produces (B, 10)
- [ ] RNN-010: Unit test: parameter count matches `4*(in+hid+1)*hid` formula
- [ ] RNN-011: Unit test: tanh nonlinearity used (introspect _flat_weights or check forward)
- [ ] RNN-012: Unit test: 1-layer config works
- [ ] RNN-013: Unit test: 2-layer config works (dropout active between layers)
- [ ] RNN-014: Unit test: 3-layer config works
- [ ] RNN-015: Unit test: hidden_size=128 OK
- [ ] RNN-016: Unit test: hidden_size=256 OK
- [ ] RNN-017: Unit test: gradient flows
- [ ] RNN-018: Unit test: save/load preserves weights
- [ ] RNN-019: Unit test: input shape mismatch raises
- [ ] RNN-020: Unit test: batch=1 works
- [ ] RNN-021: Unit test: batch=64 works
- [ ] RNN-022: Unit test: dropout=0 deterministic
- [ ] RNN-023: Unit test: forward with detached input works
- [ ] RNN-024: Unit test: invalid layers raises
- [ ] RNN-025: Unit test: invalid hidden raises
- [ ] RNN-026: Unit test: dropout in [0,1)
- [ ] RNN-027: Unit test: registry build returns RNNExtractor
- [ ] RNN-028: Unit test: architecture_name() == "rnn"
- [ ] RNN-029: Smoke test: train 1 epoch on tiny dataset
- [ ] RNN-030: Verify nonlinearity = tanh per RNN book + IDEA
- [ ] RNN-031: Building Block doc comment
- [ ] RNN-032: LaTeX equation in docstring: $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
- [ ] RNN-033: Lint clean
- [ ] RNN-034: Coverage ≥ 90%
- [ ] RNN-035: Verify file ≤ 150 LoC
- [ ] RNN-036: Document C-concat strategy at every timestep (ADR-003)
- [ ] RNN-037: Confirm input_size = 5 = 1 sample + 4 one-hot
- [ ] RNN-038: Verify dropout only applied between layers (not after last)
- [ ] RNN-039: Unit test: hidden init to zeros
- [ ] RNN-040: Unit test: forward with even batch sizes works

### 6d — LSTM Model [45]
- [ ] LSTM-001: Create `models/lstm_model.py`
- [ ] LSTM-002: Define `LSTMExtractor(BaseExtractor)`
- [ ] LSTM-003: `__init__(input_dim_per_step, output_dim, hidden_size, num_layers, dropout)`
- [ ] LSTM-004: Use `nn.LSTM(input_size=5, hidden_size, num_layers, batch_first=True, dropout)`
- [ ] LSTM-005: Final `nn.Linear(hidden_size, 10)` mapping last hidden to output
- [ ] LSTM-006: Implement `forward(x: Tensor[B, 10, 5]) -> Tensor[B, 10]`
- [ ] LSTM-007: Take last timestep: `out[:, -1, :]` → linear
- [ ] LSTM-008: Register as `@register("lstm")`
- [ ] LSTM-009: Unit test: forward produces (B, 10)
- [ ] LSTM-010: Unit test: parameter count matches LSTM formula 4*(in+hid+1)*hid per layer
- [ ] LSTM-011: Unit test: 1-layer config works
- [ ] LSTM-012: Unit test: 2-layer config works
- [ ] LSTM-013: Unit test: 3-layer config works
- [ ] LSTM-014: Unit test: hidden_size=128 OK
- [ ] LSTM-015: Unit test: hidden_size=256 OK
- [ ] LSTM-016: Unit test: dropout=0.2 active in train, off in eval
- [ ] LSTM-017: Unit test: gradient flows
- [ ] LSTM-018: Unit test: save/load round-trip
- [ ] LSTM-019: Unit test: input shape mismatch raises
- [ ] LSTM-020: Unit test: batch=1
- [ ] LSTM-021: Unit test: batch=64
- [ ] LSTM-022: Unit test: invalid layers raises
- [ ] LSTM-023: Unit test: invalid hidden raises
- [ ] LSTM-024: Unit test: dropout in [0,1)
- [ ] LSTM-025: Unit test: registry build returns LSTMExtractor
- [ ] LSTM-026: Unit test: architecture_name() == "lstm"
- [ ] LSTM-027: Smoke test: train 1 epoch on tiny dataset
- [ ] LSTM-028: Verify 4-gate structure documented in docstring
- [ ] LSTM-029: LaTeX equations in docstring: forget/input/candidate/output/cell/hidden
- [ ] LSTM-030: Building Block doc comment
- [ ] LSTM-031: Lint clean
- [ ] LSTM-032: Coverage ≥ 90%
- [ ] LSTM-033: Verify file ≤ 150 LoC
- [ ] LSTM-034: Document C-concat strategy at every timestep (ADR-003)
- [ ] LSTM-035: Confirm input_size = 5 = 1 sample + 4 one-hot
- [ ] LSTM-036: Verify dropout only between layers
- [ ] LSTM-037: Unit test: hidden + cell init to zeros
- [ ] LSTM-038: Unit test: forget gate present (introspect)
- [ ] LSTM-039: Unit test: even batch sizes work
- [ ] LSTM-040: Compare param count: LSTM ≈ 4× RNN at same hidden
- [ ] LSTM-041: Property test: LSTM has more params than RNN at same config
- [ ] LSTM-042: Property test: dropout=0 + same seed → deterministic forward
- [ ] LSTM-043: Verify default config matches PLAN.md
- [ ] LSTM-044: Add reference to LSTM book pages 18 (hyperparam recommendations)
- [ ] LSTM-045: Sanity check: LSTM handles 0-noise data with low loss

## Phase 7 — Training Service (P0) [100 tasks]

### 7a — Loss Function [10]
- [ ] LOSS-001: Create `services/loss_fn.py`
- [ ] LOSS-002: Implement `WindowSumMSE(nn.Module)` summing per-sample MSE across the 10 outputs
- [ ] LOSS-003: Use `reduction='sum'` over window axis, mean over batch
- [ ] LOSS-004: Unit test: shape compatibility (B, 10) vs (B, 10)
- [ ] LOSS-005: Unit test: identical pred/target → 0 loss
- [ ] LOSS-006: Unit test: doubled error → 4× loss (quadratic)
- [ ] LOSS-007: Unit test: differentiable
- [ ] LOSS-008: Match lecturer formula: Total Loss = L_1 + ... + L_10
- [ ] LOSS-009: Lint clean
- [ ] LOSS-010: Verify file ≤ 150 LoC

### 7b — Early Stopping [15]
- [ ] ES-001: Create `services/early_stopping.py`
- [ ] ES-002: Define `EarlyStopping(patience: int, mode: str = 'min', min_delta: float = 0.0)`
- [ ] ES-003: Implement `step(value) -> bool` returning True when stopping
- [ ] ES-004: Track best value + epochs_without_improvement
- [ ] ES-005: Unit test: triggers after patience epochs without improvement
- [ ] ES-006: Unit test: improvement resets counter
- [ ] ES-007: Unit test: min_delta respected (small noise ignored)
- [ ] ES-008: Unit test: mode='max' reverses comparison
- [ ] ES-009: Unit test: state retrievable
- [ ] ES-010: Unit test: invalid patience raises
- [ ] ES-011: Unit test: invalid mode raises
- [ ] ES-012: Unit test: deepcopy of best_state_dict on improvement
- [ ] ES-013: Building Block doc comment
- [ ] ES-014: Lint clean
- [ ] ES-015: Coverage ≥ 90%

### 7c — Optimizer Wrapper [10]
- [ ] OPT-001: Create `services/optimizer_factory.py`
- [ ] OPT-002: Define `build_optimizer(name: str, params, lr) -> Optimizer`
- [ ] OPT-003: Support 'adam' and 'rmsprop'
- [ ] OPT-004: Unit test: adam returned for 'adam'
- [ ] OPT-005: Unit test: rmsprop returned for 'rmsprop'
- [ ] OPT-006: Unit test: invalid name raises
- [ ] OPT-007: Unit test: lr applied
- [ ] OPT-008: Lint clean
- [ ] OPT-009: Coverage 100%
- [ ] OPT-010: Verify file ≤ 150 LoC

### 7d — TrainingLoop [30]
- [ ] LOOP-001: Create `services/training_loop.py`
- [ ] LOOP-002: Define `TrainingLoop(model, optimizer, loss_fn, train_loader, val_loader, max_epochs, hooks, early_stopping)`
- [ ] LOOP-003: Implement `run() -> TrainingResult`
- [ ] LOOP-004: Per-epoch: train, then validate
- [ ] LOOP-005: Track loss_history (train + val per epoch)
- [ ] LOOP-006: Track wall_clock_seconds
- [ ] LOOP-007: Fire `BEFORE_TRAIN`, `AFTER_EPOCH`, `AFTER_TRAIN` hooks
- [ ] LOOP-008: Restore best weights on early stop
- [ ] LOOP-009: Detect NaN loss → abort with TrainingError
- [ ] LOOP-010: Set model to train()/eval() at appropriate times
- [ ] LOOP-011: Move batches to device
- [ ] LOOP-012: Unit test: 1 epoch decreases loss on memorizable data
- [ ] LOOP-013: Unit test: hooks fired with expected events
- [ ] LOOP-014: Unit test: early stop triggers
- [ ] LOOP-015: Unit test: NaN loss aborts cleanly
- [ ] LOOP-016: Unit test: max_epochs respected
- [ ] LOOP-017: Unit test: best weights restored on stop
- [ ] LOOP-018: Unit test: loss_history length matches epochs run
- [ ] LOOP-019: Unit test: optimizer.step called per batch
- [ ] LOOP-020: Unit test: optimizer.zero_grad called per batch
- [ ] LOOP-021: Unit test: param count tracked
- [ ] LOOP-022: Unit test: device='cpu' works
- [ ] LOOP-023: Unit test: deterministic with fixed seed
- [ ] LOOP-024: Building Block doc comment
- [ ] LOOP-025: Lint clean
- [ ] LOOP-026: Coverage ≥ 90%
- [ ] LOOP-027: Verify file ≤ 150 LoC
- [ ] LOOP-028: Define `TrainingResult` dataclass with all metrics
- [ ] LOOP-029: Define `TrainingError(Exception)`
- [ ] LOOP-030: Document hook lifecycle in docstring

### 7e — TrainingService Orchestrator [20]
- [ ] TSV-001: Create `services/training_service.py`
- [ ] TSV-002: Define `TrainingService(config, gatekeeper)`
- [ ] TSV-003: Implement `train(arch, dataset, hyperparams, seed) -> RunHandle`
- [ ] TSV-004: Build model via registry
- [ ] TSV-005: Build optimizer via factory
- [ ] TSV-006: Build train/val DataLoaders with num_workers
- [ ] TSV-007: Construct TrainingLoop
- [ ] TSV-008: Persist results to `results/<run_id>/`
- [ ] TSV-009: Generate run_id with timestamp + arch + freq + alpha + seed
- [ ] TSV-010: Save loss_history.json
- [ ] TSV-011: Save best_model.pt
- [ ] TSV-012: Unit test: train returns RunHandle with valid run_id
- [ ] TSV-013: Unit test: results dir created
- [ ] TSV-014: Unit test: loss_history persisted
- [ ] TSV-015: Unit test: model checkpoint persisted
- [ ] TSV-016: Integration test: train fc 2 epochs end-to-end
- [ ] TSV-017: Integration test: train rnn 2 epochs end-to-end
- [ ] TSV-018: Integration test: train lstm 2 epochs end-to-end
- [ ] TSV-019: Lint clean
- [ ] TSV-020: Verify file ≤ 150 LoC

### 7f — Training utilities [15]
- [ ] TUT-001: Add `set_global_seed(seed)` in shared
- [ ] TUT-002: Unit test: set_global_seed makes torch deterministic
- [ ] TUT-003: Unit test: set_global_seed makes numpy deterministic
- [ ] TUT-004: Unit test: set_global_seed makes random deterministic
- [ ] TUT-005: Add `count_parameters(model)` in mixins (covered)
- [ ] TUT-006: Add `format_run_id(arch, freq, alpha, seed) -> str`
- [ ] TUT-007: Unit test: run_id contains all 4 components
- [ ] TUT-008: Unit test: run_id has timestamp
- [ ] TUT-009: Add `select_device() -> str` (cpu fallback)
- [ ] TUT-010: Unit test: select_device returns 'cpu' when no GPU
- [ ] TUT-011: Add `wall_clock_timer()` context manager
- [ ] TUT-012: Unit test: timer measures > 0
- [ ] TUT-013: Lint clean
- [ ] TUT-014: Coverage ≥ 90%
- [ ] TUT-015: Verify each file ≤ 150 LoC

## Phase 8 — Evaluation Service (P0) [70 tasks]

### 8a — Metrics [20]
- [ ] MET-001: Create `services/metrics.py`
- [ ] MET-002: Implement `mse(pred, target) -> float`
- [ ] MET-003: Implement `mae(pred, target) -> float`
- [ ] MET-004: Implement `r2_score(pred, target) -> float`
- [ ] MET-005: Implement `snr_db(pred, target) -> float`
- [ ] MET-006: Unit test: mse 0 for identical
- [ ] MET-007: Unit test: mse non-negative
- [ ] MET-008: Unit test: mae 0 for identical
- [ ] MET-009: Unit test: r2 == 1 for perfect prediction
- [ ] MET-010: Unit test: r2 < 0 possible for bad prediction
- [ ] MET-011: Unit test: snr higher for better predictions
- [ ] MET-012: Unit test: handle empty arrays gracefully
- [ ] MET-013: Unit test: support np and torch input
- [ ] MET-014: Unit test: dtype-agnostic
- [ ] MET-015: Building Block doc comment
- [ ] MET-016: Lint clean
- [ ] MET-017: Coverage ≥ 95%
- [ ] MET-018: Verify file ≤ 150 LoC
- [ ] MET-019: Add `predict_zero_baseline(target) -> float` for comparison
- [ ] MET-020: Unit test baseline returns mean(target^2)

### 8b — EvaluationService [25]
- [ ] EV-001: Create `services/evaluation_service.py`
- [ ] EV-002: Define `EvaluationService(config)`
- [ ] EV-003: Implement `evaluate(run_handle, test_loader) -> EvalReport`
- [ ] EV-004: Compute test_mse, test_mae, test_r2
- [ ] EV-005: Compute baseline (predict zero) for comparison
- [ ] EV-006: Sample 5 reconstructions for plotting
- [ ] EV-007: Persist `eval_report.json` next to `loss_history.json`
- [ ] EV-008: Unit test: report contains required fields
- [ ] EV-009: Unit test: identical pred/target → near-zero metrics
- [ ] EV-010: Unit test: persisted report parseable
- [ ] EV-011: Unit test: baseline computed
- [ ] EV-012: Unit test: reconstruction sample shape
- [ ] EV-013: Building Block doc comment
- [ ] EV-014: Lint clean
- [ ] EV-015: Coverage ≥ 90%
- [ ] EV-016: Verify file ≤ 150 LoC
- [ ] EV-017: Define `EvalReport` dataclass
- [ ] EV-018: Fire BEFORE_EVAL / AFTER_EVAL hooks
- [ ] EV-019: Unit test: hooks fire
- [ ] EV-020: Integration test: train+evaluate fc on tiny dataset
- [ ] EV-021: Integration test: train+evaluate rnn on tiny dataset
- [ ] EV-022: Integration test: train+evaluate lstm on tiny dataset
- [ ] EV-023: Stratify metrics by target_freq (4 frequencies)
- [ ] EV-024: Unit test: stratification works
- [ ] EV-025: Aggregate per-(arch,freq,alpha) into one row of sensitivity.csv

### 8c — Plotting helpers [15]
- [ ] PLT-001: Create `services/plotting.py`
- [ ] PLT-002: Implement `plot_loss_curves(history, ax)`
- [ ] PLT-003: Implement `plot_reconstruction(pred, target, ax)`
- [ ] PLT-004: Implement `plot_mse_heatmap(df, x, y, value, ax)`
- [ ] PLT-005: Implement `plot_oat_sensitivity(df, hyperparam, ax)`
- [ ] PLT-006: Implement `plot_signal_timeseries(signal, fs, ax, label)`
- [ ] PLT-007: Implement `plot_fft_spectrum(signal, fs, ax)`
- [ ] PLT-008: Use seaborn `colorblind` palette
- [ ] PLT-009: Add titles, axis labels, legends to all plots
- [ ] PLT-010: Unit test: each plot returns Axes object
- [ ] PLT-011: Unit test: plots produce non-empty figure
- [ ] PLT-012: Smoke test: render to /tmp file
- [ ] PLT-013: Lint clean
- [ ] PLT-014: Verify file ≤ 150 LoC
- [ ] PLT-015: Coverage ≥ 80% (plotting is hard to test deeply)

### 8d — Reconstruction sampling [10]
- [ ] REC-001: Implement `sample_reconstructions(model, loader, n=5) -> list[(pred, target)]`
- [ ] REC-002: Cycle through frequencies for diverse examples
- [ ] REC-003: Save as npz under `results/<run_id>/reconstructions.npz`
- [ ] REC-004: Unit test: returns n examples
- [ ] REC-005: Unit test: pred shape == target shape
- [ ] REC-006: Unit test: persistence round-trips
- [ ] REC-007: Lint clean
- [ ] REC-008: Coverage ≥ 90%
- [ ] REC-009: Verify file ≤ 150 LoC
- [ ] REC-010: Building Block doc comment

## Phase 9 — Sweep Service (P1) [50 tasks]

- [ ] SW-001: Create `services/sweep_service.py`
- [ ] SW-002: Define `SweepService(config, training_service, eval_service)`
- [ ] SW-003: Implement `run_experiment_matrix() -> list[RunHandle]` for arch × freq × alpha × seed
- [ ] SW-004: Implement `run_oat_sweep() -> list[RunHandle]` for hyperparams
- [ ] SW-005: Aggregate results into `results/sensitivity.csv`
- [ ] SW-006: Aggregate results into `results/experiment_matrix.csv`
- [ ] SW-007: Per-run logging (start/end + params)
- [ ] SW-008: Skip already-completed runs (idempotency)
- [ ] SW-009: Unit test: matrix size = 3 archs × 4 freqs × 4 alphas × 3 seeds = 144 runs
- [ ] SW-010: Unit test: idempotency skips done runs
- [ ] SW-011: Unit test: oat sweep generates 4 hyperparams × 3 values × 3 archs = 36 runs/seed
- [ ] SW-012: Unit test: csv aggregation includes all rows
- [ ] SW-013: Unit test: csv has correct columns
- [ ] SW-014: Integration test: tiny matrix (1 arch × 1 freq × 1 alpha × 1 seed) runs
- [ ] SW-015: Integration test: tiny oat (fc, hidden=[64]) runs
- [ ] SW-016: Building Block doc comment
- [ ] SW-017: Lint clean
- [ ] SW-018: Coverage ≥ 85%
- [ ] SW-019: Verify file ≤ 150 LoC
- [ ] SW-020: Add `--dry-run` mode that lists planned runs without executing
- [ ] SW-021: Unit test: dry-run lists expected count
- [ ] SW-022: Implement `_grid_size_estimate() -> int`
- [ ] SW-023: Unit test: estimate matches actual
- [ ] SW-024: Document scaling tradeoffs in PRD_evaluation.md
- [ ] SW-025: Add `--limit N` flag to truncate long sweeps for debugging
- [ ] SW-026: Unit test: limit truncates
- [ ] SW-027: Add per-run timeout config
- [ ] SW-028: Unit test: timeout raises TrainingError
- [ ] SW-029: Add resume from CSV if interrupted
- [ ] SW-030: Unit test: resume picks up where left off
- [ ] SW-031: Add total wall-clock report at end
- [ ] SW-032: Unit test: total wall-clock reported
- [ ] SW-033: Add per-arch wall-clock stratification
- [ ] SW-034: Unit test: stratification works
- [ ] SW-035: Add memory monitoring placeholder (psutil optional)
- [ ] SW-036: Unit test: memory not enforced (just logged)
- [ ] SW-037: Add CLI subcommand `run-matrix` and `run-oat`
- [ ] SW-038: Unit test: CLI dispatches correctly
- [ ] SW-039: Add `--config-override` JSON flag
- [ ] SW-040: Unit test: override applied
- [ ] SW-041: Save manifest with all run_ids
- [ ] SW-042: Unit test: manifest contains expected run_ids
- [ ] SW-043: Add SHA-256 of config to manifest
- [ ] SW-044: Unit test: SHA reproducible
- [ ] SW-045: Add results pruning utility (`scripts/prune_results.py`)
- [ ] SW-046: Unit test: prune dry-run lists candidates
- [ ] SW-047: Document the matrix in PRD_evaluation.md
- [ ] SW-048: Add `--seed-only N` for fast smoke runs
- [ ] SW-049: Unit test: seed-only filter works
- [ ] SW-050: Verify all sweep files ≤ 150 LoC

## Phase 10 — SDK (P0) [40 tasks]

- [ ] SDK-001: Create `sdk/sdk.py`
- [ ] SDK-002: Define `SinusoidExtractorSDK` class
- [ ] SDK-003: `__init__(config_path: Path | None = None)`
- [ ] SDK-004: Load config + version check at init
- [ ] SDK-005: Instantiate gatekeeper, dataset_service, training_service, eval_service, sweep_service
- [ ] SDK-006: Implement `generate_dataset(alpha, seed) -> DatasetHandle`
- [ ] SDK-007: Implement `train_model(arch, dataset, hyperparams, seed) -> RunHandle`
- [ ] SDK-008: Implement `evaluate(run, dataset) -> EvalReport`
- [ ] SDK-009: Implement `run_experiment_matrix() -> list[RunHandle]`
- [ ] SDK-010: Implement `run_oat_sweep() -> list[RunHandle]`
- [ ] SDK-011: Implement `get_version() -> str`
- [ ] SDK-012: Implement `get_config() -> dict`
- [ ] SDK-013: Add structured logging on every method
- [ ] SDK-014: Unit test: SDK init reads config
- [ ] SDK-015: Unit test: SDK init missing config raises
- [ ] SDK-016: Unit test: generate_dataset returns handle
- [ ] SDK-017: Unit test: train_model returns RunHandle
- [ ] SDK-018: Unit test: evaluate returns EvalReport
- [ ] SDK-019: Unit test: run_experiment_matrix returns list
- [ ] SDK-020: Unit test: run_oat_sweep returns list
- [ ] SDK-021: Unit test: get_version returns "1.00"
- [ ] SDK-022: Unit test: get_config returns dict
- [ ] SDK-023: Integration test: end-to-end via SDK only
- [ ] SDK-024: Building Block doc comment
- [ ] SDK-025: Lint clean
- [ ] SDK-026: Coverage ≥ 90%
- [ ] SDK-027: Verify file ≤ 150 LoC
- [ ] SDK-028: Document each method in docstring (input/output/setup)
- [ ] SDK-029: Add `__all__ = ["SinusoidExtractorSDK"]` in `sdk/__init__.py`
- [ ] SDK-030: Verify external import works: `from sinusoid_extractor.sdk import SinusoidExtractorSDK`
- [ ] SDK-031: Verify SDK has no business logic (just dispatches)
- [ ] SDK-032: Audit: no service called outside SDK in tests/ or notebooks/
- [ ] SDK-033: Add SDK constructor parameter for `gatekeeper` injection (DI)
- [ ] SDK-034: Unit test: custom gatekeeper accepted
- [ ] SDK-035: Add `health_check() -> dict` for self-diagnostic
- [ ] SDK-036: Unit test: health_check returns OK
- [ ] SDK-037: Add `list_completed_runs() -> list[RunHandle]`
- [ ] SDK-038: Unit test: list_completed_runs reads results/
- [ ] SDK-039: Add `clear_results()` (defensive — requires explicit confirmation)
- [ ] SDK-040: Unit test: clear_results requires confirm=True

## Phase 11 — CLI (P0) [30 tasks]

- [ ] CLI-001: Create `src/sinusoid_extractor/main.py`
- [ ] CLI-002: Build argparse with subcommands: generate-data, train, evaluate, run-matrix, run-oat, version
- [ ] CLI-003: Add `--config PATH` global flag
- [ ] CLI-004: Add `--log-level LEVEL` global flag
- [ ] CLI-005: Implement `cmd_generate_data(args)` calling SDK
- [ ] CLI-006: Implement `cmd_train(args)`
- [ ] CLI-007: Implement `cmd_evaluate(args)`
- [ ] CLI-008: Implement `cmd_run_matrix(args)`
- [ ] CLI-009: Implement `cmd_run_oat(args)`
- [ ] CLI-010: Implement `cmd_version(args)` printing version
- [ ] CLI-011: Argparse: validate arch in {fc, rnn, lstm}
- [ ] CLI-012: Argparse: validate alpha in [0, 1]
- [ ] CLI-013: Argparse: validate seed integer
- [ ] CLI-014: Implement `main()` entry point
- [ ] CLI-015: Add `if __name__ == "__main__": main()` guard
- [ ] CLI-016: Unit test: each cmd_* function callable in isolation
- [ ] CLI-017: Unit test: argparse rejects bad arch
- [ ] CLI-018: Unit test: argparse rejects negative alpha
- [ ] CLI-019: Unit test: --version prints version and exits 0
- [ ] CLI-020: Unit test: --help works
- [ ] CLI-021: Smoke: `uv run python -m sinusoid_extractor.main version` returns 0
- [ ] CLI-022: Smoke: `uv run python -m sinusoid_extractor.main generate-data --alpha 0.05` runs
- [ ] CLI-023: Building Block doc comment
- [ ] CLI-024: Lint clean
- [ ] CLI-025: Verify file ≤ 150 LoC
- [ ] CLI-026: Confirm CLI is THIN (no business logic, just dispatch)
- [ ] CLI-027: Add `--quiet` flag to suppress logs
- [ ] CLI-028: Unit test: --quiet reduces stdout
- [ ] CLI-029: Add exit codes (0 success, 1 error, 2 bad args)
- [ ] CLI-030: Unit test: exit codes correct

## Phase 12 — Logging (P1) [20 tasks]

- [ ] LOGI-001: Finalize `config/logging_config.json` with file + console handlers
- [ ] LOGI-002: Console handler at INFO; file handler at DEBUG
- [ ] LOGI-003: Rotating file handler (10MB × 5)
- [ ] LOGI-004: Per-module loggers via `__name__`
- [ ] LOGI-005: Sensitive value redaction filter (placeholder for future)
- [ ] LOGI-006: Unit test: logging config loads
- [ ] LOGI-007: Unit test: log line written to file
- [ ] LOGI-008: Unit test: rotation triggers at threshold (mocked)
- [ ] LOGI-009: Unit test: redaction filter (placeholder)
- [ ] LOGI-010: Verify no logs created during pytest (use caplog)
- [ ] LOGI-011: Add `disable_logging` context manager for tests
- [ ] LOGI-012: Unit test: disable_logging silences logger
- [ ] LOGI-013: Add structured kv format
- [ ] LOGI-014: Unit test: kv format produces expected string
- [ ] LOGI-015: Add CLI flag `--log-level` overriding config
- [ ] LOGI-016: Unit test: CLI override works
- [ ] LOGI-017: Add log rotation test
- [ ] LOGI-018: Add log to `logs/sinusoid_extractor.log`
- [ ] LOGI-019: Verify logs/ git-ignored
- [ ] LOGI-020: Lint clean

## Phase 13 — Tests Augmentation & Fixtures (P0) [80 tasks]

- [ ] FIX-001: `tests/conftest.py::sample_config` (dict)
- [ ] FIX-002: `tests/conftest.py::tmp_config_path` (Path)
- [ ] FIX-003: `tests/conftest.py::tiny_dataset` (200 train / 50 val / 50 test)
- [ ] FIX-004: `tests/conftest.py::seed_rng` (np.random.Generator)
- [ ] FIX-005: `tests/conftest.py::sdk` (instantiated SDK with tmp config)
- [ ] FIX-006: `tests/conftest.py::cpu_device` (torch device)
- [ ] FIX-007: Auto-set seed=42 for every test (autouse)
- [ ] FIX-008: Skip GPU-only tests (no GPU on CI)
- [ ] FIX-009: Mark slow tests with `@pytest.mark.slow`
- [ ] FIX-010: Add `--run-slow` pytest flag
- [ ] EDGE-001: Test alpha=0 (no noise) → combined == sum of pure
- [ ] EDGE-002: Test alpha=1 (full noise) → combined still bounded
- [ ] EDGE-003: Test single-frequency dataset (other 3 zero) optional
- [ ] EDGE-004: Test window_size = signal length (one window)
- [ ] EDGE-005: Test n_train = 0 (degenerate empty bundle) returns clean error
- [ ] EDGE-006: Test num_layers = 1 (no dropout active)
- [ ] EDGE-007: Test hidden_size = 1 (degenerate model)
- [ ] EDGE-008: Test max_epochs = 1
- [ ] EDGE-009: Test early stop with patience=0 → stops first non-improvement
- [ ] EDGE-010: Test early stop with patience > epochs → never stops
- [ ] EDGE-011: Test loss_fn with all-zero target
- [ ] EDGE-012: Test loss_fn with NaN input → raises
- [ ] EDGE-013: Test save with read-only path → raises
- [ ] EDGE-014: Test load missing file → raises
- [ ] EDGE-015: Test config without version → warning logged
- [ ] EDGE-016: Test malformed JSON → raises
- [ ] EDGE-017: Test SDK without config → uses default
- [ ] EDGE-018: Test invalid arch in CLI → argparse error
- [ ] EDGE-019: Test alpha < 0 → ValueError
- [ ] EDGE-020: Test alpha > 1 → warning, accepted
- [ ] PROP-001: Property: dataset reproducibility under same seed
- [ ] PROP-002: Property: noise mean ≈ 0 across many samples
- [ ] PROP-003: Property: window content matches signal at offset
- [ ] PROP-004: Property: model forward is shape-stable across batch sizes
- [ ] PROP-005: Property: param count > 0 for all models
- [ ] PROP-006: Property: training loss decreases monotonically (smoothed) on memorizable data
- [ ] PROP-007: Property: registry returns same instance type for same name
- [ ] PROP-008: Property: csv aggregation has no duplicate run_ids
- [ ] INT-001: Integration: SDK end-to-end fc on tiny dataset
- [ ] INT-002: Integration: SDK end-to-end rnn on tiny dataset
- [ ] INT-003: Integration: SDK end-to-end lstm on tiny dataset
- [ ] INT-004: Integration: matrix sweep with limit=2 finishes
- [ ] INT-005: Integration: oat sweep with limit=2 finishes
- [ ] INT-006: Integration: results dir created with expected files
- [ ] INT-007: Integration: csv aggregation produced
- [ ] INT-008: Integration: notebook execution smoke (jupyter nbconvert --execute)
- [ ] INT-009: Integration: gatekeeper called from sdk (smoke, no-op)
- [ ] INT-010: Integration: hooks fired during sdk.train_model
- [ ] COV-001: Run `uv run pytest --cov` and confirm ≥ 85%
- [ ] COV-002: Identify lowest-coverage module and add tests
- [ ] COV-003: Aim for 90% on dataset_service
- [ ] COV-004: Aim for 90% on training_loop
- [ ] COV-005: Aim for 85% on plotting (hard to deeply test)
- [ ] LIN-001: `uv run ruff check src/ tests/` returns 0
- [ ] LIN-002: Auto-fix safe: `uv run ruff check --fix`
- [ ] LIN-003: Re-run lint to confirm clean
- [ ] LIN-004: Add `pre-commit` hint in README (optional)
- [ ] LIN-005: Verify no F401 (unused imports)
- [ ] LIN-006: Verify no E (PEP8) errors
- [ ] LIN-007: Verify no B (bugbear) flags
- [ ] LIN-008: Verify no C4 (comprehension) flags
- [ ] LIN-009: Verify no SIM (simplify) suggestions outstanding
- [ ] LIN-010: Verify naming conventions (N) clean
- [ ] FILE-001: Run `scripts/check_file_lines.py` → 0 errors
- [ ] FILE-002: Identify any file > 150 LoC and split
- [ ] FILE-003: Re-run check after splits
- [ ] SEC-001: Grep for `api_key|secret|password|token` → empty
- [ ] SEC-002: Verify `.env` not in `git ls-files`
- [ ] SEC-003: Verify `.env-example` is committed
- [ ] SEC-004: Verify `.gitignore` includes secrets
- [ ] SEC-005: Run `git secrets --scan` if available (skip if not)
- [ ] SEC-006: Confirm no hardcoded API keys
- [ ] SEC-007: Confirm no hardcoded URLs
- [ ] SEC-008: Confirm no hardcoded paths (use config.paths)
- [ ] SEC-009: Confirm config files versioned (1.00)
- [ ] SEC-010: Confirm code __version__ matches config version

## Phase 14 — Run Experiments (P0) [40 tasks]

- [ ] EXP-001: Pre-flight: confirm `uv sync` clean
- [ ] EXP-002: Pre-flight: confirm `uv run pytest` green
- [ ] EXP-003: Pre-flight: confirm `uv run ruff check` clean
- [ ] EXP-004: Generate the 4 datasets (alpha ∈ {0.01, 0.05, 0.10, 0.20})
- [ ] EXP-005: Persist all 4 datasets to `data/raw/`
- [ ] EXP-006: Verify dataset reproducibility (re-run, compare hashes)
- [ ] EXP-007: Run base matrix: 3 archs × 4 alphas (use 1 seed first to time)
- [ ] EXP-008: Estimate full matrix wall-clock from timing
- [ ] EXP-009: If full matrix > 6 h, reduce seeds to 2 or use parallelism
- [ ] EXP-010: Run base matrix: 3 archs × 4 alphas × 3 seeds = 36 runs
- [ ] EXP-011: Aggregate base matrix results to `results/experiment_matrix.csv`
- [ ] EXP-012: Run OAT sweep: 4 hyperparams × 3 values × 3 archs (with default seeds)
- [ ] EXP-013: Aggregate OAT results to `results/sensitivity.csv`
- [ ] EXP-014: Verify all runs produced loss_history.json
- [ ] EXP-015: Verify all runs produced eval_report.json
- [ ] EXP-016: Spot-check: best loss < worst loss (sanity)
- [ ] EXP-017: Spot-check: alpha=0.01 better than alpha=0.20 (intuition)
- [ ] EXP-018: Save final manifest of all run_ids
- [ ] EXP-019: Persist a `results/RUN_REPORT.md` summary
- [ ] EXP-020: Compute mean ± std per cell across seeds
- [ ] EXP-021: Compute paired test (RNN vs LSTM at high freq)
- [ ] EXP-022: Compute paired test (LSTM vs RNN at low freq)
- [ ] EXP-023: Compute FC vs recurrent paired test
- [ ] EXP-024: Save statistical results to `results/hypothesis_test.json`
- [ ] EXP-025: Save best hyperparams per arch to `results/best_hparams.json`
- [ ] EXP-026: If hypothesis disconfirmed, document explanation
- [ ] EXP-027: Render reconstructions for best runs to `results/figs/`
- [ ] EXP-028: Render loss-curve montage to `results/figs/loss_curves.png`
- [ ] EXP-029: Render heatmap to `results/figs/mse_heatmap.png`
- [ ] EXP-030: Render OAT line plots to `results/figs/oat_*.png`
- [ ] EXP-031: Verify reproducibility: re-run one cell, compare results within tolerance
- [ ] EXP-032: Document any non-deterministic divergence
- [ ] EXP-033: Backup `results/` to a tarball before notebook authoring
- [ ] EXP-034: Confirm CSV files have headers + correct row count
- [ ] EXP-035: Confirm no NaNs in CSV results
- [ ] EXP-036: Audit run wall-clocks (slowest run, fastest run)
- [ ] EXP-037: If LSTM > 30s/epoch, reduce hidden or batch
- [ ] EXP-038: Re-run problematic cells if needed
- [ ] EXP-039: Final commit of `results/` artifacts (CSVs and figs only — npz git-ignored)
- [ ] EXP-040: Tag this commit `v1.00-experiments`

## Phase 15 — Notebook (P0) [60 tasks]

### 15a — Setup Section [10]
- [ ] NB-001: Create `notebooks/analysis.ipynb`
- [ ] NB-002: Title cell: "Sinusoid Extraction with FC, RNN, and LSTM — Analysis"
- [ ] NB-003: Author + date + course cell
- [ ] NB-004: Imports cell (numpy, pandas, matplotlib, seaborn, sdk)
- [ ] NB-005: Set seed cell + reproducibility note
- [ ] NB-006: Load config cell
- [ ] NB-007: Load results from `results/` cell
- [ ] NB-008: Sanity-check loaded data shapes
- [ ] NB-009: Display config summary (table)
- [ ] NB-010: Section divider markdown

### 15b — Dataset Visualization [10]
- [ ] NB-011: Markdown intro to dataset
- [ ] NB-012: Load and plot pure sine 1 Hz
- [ ] NB-013: Load and plot pure sine 3 Hz
- [ ] NB-014: Load and plot pure sine 5 Hz
- [ ] NB-015: Load and plot pure sine 7 Hz
- [ ] NB-016: Plot noisy versions (4 panel grid)
- [ ] NB-017: Plot Σ combined signal
- [ ] NB-018: FFT spectrum of Σ (frequency axis 0–50 Hz)
- [ ] NB-019: Annotate the 4 expected peaks (1, 3, 5, 7 Hz)
- [ ] NB-020: Markdown commentary on visibility of peaks

### 15c — Architectures + LaTeX [12]
- [ ] NB-021: FC architecture markdown with equations
- [ ] NB-022: FC LaTeX: $y = W_2 \cdot \text{ReLU}(W_1 x + b_1) + b_2$
- [ ] NB-023: RNN architecture markdown
- [ ] NB-024: RNN LaTeX: $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
- [ ] NB-025: LSTM architecture markdown
- [ ] NB-026: LSTM LaTeX: forget gate $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
- [ ] NB-027: LSTM input gate
- [ ] NB-028: LSTM candidate cell
- [ ] NB-029: LSTM cell update
- [ ] NB-030: LSTM output gate
- [ ] NB-031: Display per-arch parameter counts table
- [ ] NB-032: Display per-arch wall-clock training time table

### 15d — Training [8]
- [ ] NB-033: Training loss curves grid (3 archs × 4 noise levels)
- [ ] NB-034: Validation loss overlay
- [ ] NB-035: Highlight early-stopping epoch with vertical line
- [ ] NB-036: Markdown observations on convergence speed
- [ ] NB-037: Markdown observations on overfitting (train ↓ val ↑)
- [ ] NB-038: Per-arch best-epoch comparison table
- [ ] NB-039: Per-arch parameter count vs final loss scatter
- [ ] NB-040: Discussion of training dynamics

### 15e — Evaluation [10]
- [ ] NB-041: Heatmap MSE × (arch, target_freq) for alpha=0.05
- [ ] NB-042: Heatmap for alpha=0.10
- [ ] NB-043: Heatmap for alpha=0.20
- [ ] NB-044: Reconstruction plots: pred vs true for FC at 3 Hz
- [ ] NB-045: Reconstruction plots: pred vs true for RNN at 7 Hz
- [ ] NB-046: Reconstruction plots: pred vs true for LSTM at 1 Hz
- [ ] NB-047: Bar plot: best test MSE per arch
- [ ] NB-048: Test MSE vs noise level line plot
- [ ] NB-049: R² score table
- [ ] NB-050: Discussion of where each arch shines/struggles

### 15f — Sensitivity Analysis OAT [5]
- [ ] NB-051: Hidden size OAT plot (3 arches overlaid)
- [ ] NB-052: # layers OAT plot
- [ ] NB-053: Dropout OAT plot
- [ ] NB-054: Learning rate OAT plot (log scale x)
- [ ] NB-055: Discussion of which hyperparam matters most per arch

### 15g — Hypothesis Test [3]
- [ ] NB-056: H1 verdict: paired test results, effect size, CI
- [ ] NB-057: H2 verdict: paired test results, effect size, CI
- [ ] NB-058: H3 verdict + summary table

### 15h — Conclusion [2]
- [ ] NB-059: Reflective conclusion: what worked, what surprised, what next
- [ ] NB-060: Acknowledgment of AI assistance per syllabus

## Phase 16 — README (P0) [30 tasks]

- [ ] RDM-001: Create `README.md` with project title + 1-line tagline
- [ ] RDM-002: Add badge row (python version, license, ruff, pytest)
- [ ] RDM-003: Add Table of Contents
- [ ] RDM-004: Section: Overview
- [ ] RDM-005: Section: The Hypothesis (H1, H2, H3)
- [ ] RDM-006: Section: Architecture (small diagram or ASCII)
- [ ] RDM-007: Section: Installation (uv + clone + uv sync)
- [ ] RDM-008: Section: Quick Start (single command produces results)
- [ ] RDM-009: Section: Configuration (all keys explained)
- [ ] RDM-010: Section: Usage / CLI subcommands
- [ ] RDM-011: Section: Examples (3 worked examples)
- [ ] RDM-012: Section: Project Structure (tree)
- [ ] RDM-013: Section: Running Tests (uv run pytest --cov)
- [ ] RDM-014: Section: Linting (uv run ruff check)
- [ ] RDM-015: Section: Notebook (how to open and run analysis.ipynb)
- [ ] RDM-016: Section: Extending the project (adding a new model via registry)
- [ ] RDM-017: Section: Troubleshooting / common issues
- [ ] RDM-018: Section: Contribution Guidelines
- [ ] RDM-019: Section: License (MIT)
- [ ] RDM-020: Section: Credits / third-party
- [ ] RDM-021: Section: AI assistance acknowledgment (per syllabus)
- [ ] RDM-022: Section: Citation (BibTeX-ish)
- [ ] RDM-023: Reference PRD/PLAN/TODO docs
- [ ] RDM-024: Reference per-mechanism PRDs
- [ ] RDM-025: Reference PROMPTS.md
- [ ] RDM-026: Add screenshots/plots from results/figs/
- [ ] RDM-027: Add link to GitHub repo
- [ ] RDM-028: Add author / contact
- [ ] RDM-029: Add ISO/IEC 25010 brief mention
- [ ] RDM-030: Final read-through, fix typos

## Phase 17 — Documentation Polish (P1) [25 tasks]

- [ ] DOC-001: Write `docs/PROMPTS.md` with full prompt log + meta-reflections
- [ ] DOC-002: Write `docs/SUBMISSION_CHECKLIST.md` with all rubric items
- [ ] DOC-003: Verify all per-mechanism PRDs are present (dataset, fc, rnn, lstm, training, evaluation)
- [ ] DOC-004: Update PRD timeline if shifted
- [ ] DOC-005: Update PLAN risks/mitigations from real experience
- [ ] DOC-006: Mark TODO items [x] as completed throughout (continuous)
- [ ] DOC-007: Add `docs/diagrams/c4_context.md` (mermaid or ASCII)
- [ ] DOC-008: Add `docs/diagrams/c4_container.md`
- [ ] DOC-009: Add `docs/diagrams/c4_component.md`
- [ ] DOC-010: Add `docs/diagrams/uml_dataset_class.md`
- [ ] DOC-011: Add `docs/diagrams/uml_model_hierarchy.md`
- [ ] DOC-012: Add `docs/diagrams/sequence_train.md`
- [ ] DOC-013: Final ADR audit — all 10 present and meaningful
- [ ] DOC-014: Verify per-mechanism PRDs each have I/O contract + alternatives + success criteria
- [ ] DOC-015: Verify ISO/IEC 25010 paragraph in PLAN.md (done)
- [ ] DOC-016: Add CHANGELOG.md (1.00 entry)
- [ ] DOC-017: Add LICENSE (MIT)
- [ ] DOC-018: Verify all docs cross-link correctly
- [ ] DOC-019: Verify no broken markdown links
- [ ] DOC-020: Spell-check all docs
- [ ] DOC-021: Resolve all `<!-- TBD -->` markers (or document why deferred)
- [ ] DOC-022: Update version stamps if any doc bumped
- [ ] DOC-023: Audit: PRD requirements ↔ TODO tasks (Verify Pass)
- [ ] DOC-024: Add missing TODO items found in audit
- [ ] DOC-025: Sign-off comment at top of each doc

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

- All 1002 tasks above are `[x]`.
- `uv run ruff check src/ tests/` returns 0.
- `uv run pytest --cov` reports ≥ 85%.
- `scripts/check_file_lines.py` reports 0 violations.
- `git log --oneline | wc -l` ≥ 50 commits.
- GitHub repo public, shared with `rmisegal@gmail.com`, tagged `v1.00`.
- Notebook executes end-to-end with no errors.
- Submission PDF uploaded to Moodle by 2026-05-07 23:59.
- All TBDs in PRD/PLAN resolved.
