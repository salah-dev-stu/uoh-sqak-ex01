# Per-Mechanism PRD — Training Loop

| Field | Value |
|---|---|
| Mechanism | Per-architecture training loop with early stopping |
| Owner modules | `src/sinusoid_extractor/services/training_loop.py`, `training_service.py`, `early_stopping.py`, `loss_fn.py`, `optimizer_factory.py` |
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` §3.3 (FR-TRN-1..6), `PLAN.md`, `TODO.md` Phase 7 |

---

## 1. Theoretical Background

### 1.1 Loss
Per the lecturer's explicit instruction:
$$
\mathcal{L}(\hat{y}, y) = \sum_{i=1}^{10} (\hat{y}_i - y_i)^2
$$
i.e. **summed** (not averaged) MSE over the 10-sample output window. Across a mini-batch of size $B$, we mean over the batch dimension:
$$
\mathcal{L}_{\text{batch}} = \frac{1}{B}\sum_{b=1}^{B}\sum_{i=1}^{10}(\hat{y}^{(b)}_i - y^{(b)}_i)^2
$$

### 1.2 Optimizer
Adam (default, $\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$) per ADR-004. RMSprop available as alternative.

### 1.3 Early stopping
Monitor validation loss; if it does not improve by `min_delta = 0.0` for `patience = 10` consecutive epochs, stop training and restore the best weights.

### 1.4 Lifecycle hooks
The training loop fires events on which user-supplied callables (plugins) can attach:
- `BEFORE_TRAIN(ctx)` — once before the first epoch
- `AFTER_EPOCH(ctx)` — at the end of every epoch (with epoch index, train_loss, val_loss)
- `AFTER_TRAIN(ctx)` — once after stopping
- `BEFORE_EVAL(ctx)` — before evaluation
- `AFTER_EVAL(ctx)` — after evaluation

Hooks satisfy the "lifecycle hooks" requirement of RULES.md §18.5.

---

## 2. Inputs

### 2.1 `TrainingLoop` constructor
| Param | Type | Notes |
|---|---|---|
| `model` | `BaseExtractor` | Built via registry |
| `optimizer` | `torch.optim.Optimizer` | Built via factory |
| `loss_fn` | `nn.Module` | `WindowSumMSE` |
| `train_loader` | `DataLoader` | Built from DataBundle |
| `val_loader` | `DataLoader` | |
| `max_epochs` | int | default 80 |
| `early_stopping` | `EarlyStopping` | optional |
| `hooks` | `HookRegistry` | optional |
| `device` | `str` | default `"cpu"` |

### 2.2 `TrainingService.train` SDK-facing
| Param | Type | Notes |
|---|---|---|
| `arch` | str | `"fc"`, `"rnn"`, or `"lstm"` |
| `dataset` | `DataBundle` | from `DatasetService.generate(...)` |
| `hyperparams` | dict \| None | overrides config defaults |
| `seed` | int \| None | for reproducibility |

---

## 3. Outputs

### 3.1 `TrainingResult` (dataclass)
| Field | Type | Notes |
|---|---|---|
| `loss_history.train` | list[float] | per-epoch |
| `loss_history.val` | list[float] | per-epoch |
| `epochs_run` | int | actual (≤ max_epochs) |
| `wall_clock_seconds` | float | total |
| `best_val_loss` | float | min over epochs |
| `best_state_dict` | dict | model weights at best epoch |

### 3.2 Persisted artifacts
Under `results/<run_id>/`:
- `loss_history.json` — full schema in PLAN.md §5.3
- `best_model.pt` — `state_dict` of best weights
- `run.log` — structured log of every epoch

---

## 4. Setup (Building Block contract)

```
TrainingLoop
  Input:  model, train_loader, val_loader, hooks (optional)
  Output: TrainingResult
  Setup:  optimizer, loss_fn, max_epochs, early_stopping, device

TrainingService
  Input:  arch (str), dataset (DataBundle), hyperparams (dict|None), seed (int|None)
  Output: RunHandle
  Setup:  config, gatekeeper, registry, paths
```

---

## 5. Performance Metrics

| Metric | Target |
|---|---|
| FC epoch wall-clock | ≤ 5 s (CPU, default config) |
| RNN epoch wall-clock | ≤ 20 s |
| LSTM epoch wall-clock | ≤ 30 s |
| Memory peak per training run | ≤ 500 MB |
| `train(arch=..., epochs=2)` integration test runtime | ≤ 90 s |

---

## 6. Constraints

- **Hard**: loss = sum across window axis (not mean). Per lecturer's formula.
- **Hard**: NaN loss → abort run with `TrainingError`. No silent garbage.
- **Hard**: file ≤ 150 LoC each (training_loop.py, training_service.py separately).
- **Hard**: `DataLoader(num_workers=N)` per RULES.md §18.7.
- **Hard**: deterministic with fixed seed (PyTorch + NumPy + Python `random` all seeded).
- **Soft**: early stopping patience ≥ 5 (default 10).

---

## 7. Alternatives Considered

| Option | Chosen? | Reason |
|---|---|---|
| Loss = sum | Yes | Lecturer's formula |
| Loss = mean | No | Diverges from lecturer's spec |
| Adam | Yes (ADR-004) | Modern default |
| RMSprop | Available | Alternative for OAT |
| SGD with momentum | No | Adam is robust here; SGD needs careful tuning |
| ReduceLROnPlateau | No | Out of scope; early stopping suffices |
| Cosine LR schedule | No | Same |
| Mixed precision (AMP) | No | CPU-only; no benefit |
| Gradient clipping (RNN/LSTM) | Yes (default 1.0 norm clip) | Prevents rare gradient spikes |
| Restore best weights on early stop | Yes | Standard practice |
| Train→val split inside loop | No | DataBundle is pre-split |

---

## 8. Success Criteria & Test Scenarios

### 8.1 Success criteria
1. `TrainingService.train(arch="fc", dataset=tiny, max_epochs=2)` returns `RunHandle` in < 30 s.
2. `loss_history.train` is monotone-decreasing on average over the first 5 epochs of a memorizable subset.
3. NaN loss raises `TrainingError` with the offending epoch index.
4. Early stopping triggers at the right epoch on a synthetic loss schedule (val_loss flat after epoch K, patience P → stop at K+P).
5. Hooks fire in the correct order with the expected context payload.
6. Best weights are restored on stop (forward output identical to best-epoch output).
7. `loss_history.json` and `best_model.pt` are persisted under `results/<run_id>/`.
8. Two runs with the same seed produce identical loss histories (within float tolerance).

### 8.2 Test scenarios
Per TODO Phase 7 (LOSS-001..010, ES-001..015, OPT-001..010, LOOP-001..030, TSV-001..020): unit and integration tests for every component plus end-to-end SDK runs.

### 8.3 Failure modes
| Failure | Response |
|---|---|
| NaN loss | `TrainingError` raised; run aborted; no artifacts written |
| OOM (tiny here) | `MemoryError` propagated; partial state cleaned |
| Optimizer name unknown | `ValueError` from factory |
| Hook callable raises | logged, run continues (hooks are best-effort) |
| Dataset empty | `ValueError` at DataLoader construction |
| max_epochs ≤ 0 | `ValueError` |
| Patience < 0 | `ValueError` |
