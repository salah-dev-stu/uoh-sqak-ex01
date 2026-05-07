# Per-Mechanism PRD — LSTM Model

| Field | Value |
|---|---|
| Mechanism | Long Short-Term Memory extractor |
| Owner module | `src/sinusoid_extractor/models/lstm_model.py` |
| Registry name | `"lstm"` |
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` §3.2 (FR-MOD-4), `PLAN.md` ADR-003, `TODO.md` Phase 6d, `materials/lstm-book.pdf` |

---

## 1. Theoretical Background

The LSTM extends the vanilla RNN with a cell state $c_t$ and four gates that govern information flow. At each timestep $t \in \{1, \ldots, 10\}$:

$$
\begin{align}
f_t &= \sigma\bigl(W_f \cdot [h_{t-1}, \tilde{x}_t] + b_f\bigr) & \text{forget gate} \\
i_t &= \sigma\bigl(W_i \cdot [h_{t-1}, \tilde{x}_t] + b_i\bigr) & \text{input gate} \\
\tilde{c}_t &= \tanh\bigl(W_c \cdot [h_{t-1}, \tilde{x}_t] + b_c\bigr) & \text{candidate cell} \\
c_t &= f_t \odot c_{t-1} + i_t \odot \tilde{c}_t & \text{cell update} \\
o_t &= \sigma\bigl(W_o \cdot [h_{t-1}, \tilde{x}_t] + b_o\bigr) & \text{output gate} \\
h_t &= o_t \odot \tanh(c_t) & \text{hidden update}
\end{align}
$$

with $\tilde{x}_t = [x_t, C]$ (the same C-concat strategy as RNN — ADR-003) and $h_0 = c_0 = \mathbf{0}$. We project the final hidden state $h_{10}$ via `nn.Linear(H, 10)` to the prediction $\hat{y}$.

We use `torch.nn.LSTM(input_size=5, hidden_size=H, num_layers=L, batch_first=True, dropout=p)` per the LSTM book's recommendation.

### 1.1 The cell state's role
The cell state $c_t$ is a **parallel highway** that bypasses the tanh nonlinearity in the recurrence — gradients can flow through $c_t$ across many steps without vanishing. This is *the* fundamental difference from vanilla RNN.

### 1.2 The lecturer's hypothesis (H2)
**LSTM excels at low frequencies (20, 60 Hz — sub-cycle within the 10-sample window)** because most of the periodicity falls *across* the window edge; the model has to integrate to recover phase, and the cell state is exactly designed for that integration.

**Cycle counts** at $F_s = 1000$ Hz, 10-sample window: 20 Hz → 0.2 cycle, 60 Hz → 0.6 cycle, 100 Hz → 1.0 cycle, 200 Hz → 2.0 cycle. The first two are the sub-cycle "low" regime where H2 applies; the last two are multi-cycle "high" where H1 applies. We test and report honestly.

### 1.3 Parameter count
For 1-layer LSTM with input=5, hidden=H:
$$
P_{\text{cell}} = 4 \cdot H \cdot (5 + H + 1) = 4H(H + 6)
$$
plus output linear $H \cdot 10 + 10$. For $H = 128$: $P = 4 \cdot 128 \cdot 134 + 1\,290 = 68\,608 + 1\,290 = 69\,898$.

LSTM has roughly **4×** the cell parameters of a vanilla RNN at the same hidden size — a known trade-off.

### 1.4 Hyperparameters from the LSTM book (page 18)
| Knob | Suggested |
|---|---|
| Hidden size | 128 or 256 |
| Layers | 1–3 |
| Dropout | 0.2–0.5 between layers |
| Learning rate | 1e-3 to 1e-2 |
| Optimizer | Adam or RMSprop |

We use these recommendations as the OAT sweep base (PLAN.md §5.1).

---

## 2. Inputs

### 2.1 Constructor (`__init__`)
| Param | Type | Default | Range |
|---|---|---|---|
| `input_dim_per_step` | int | `5` | == 5 |
| `output_dim` | int | `10` | == 10 |
| `hidden_size` | int | `128` | > 0 |
| `num_layers` | int | `1` | 1, 2, or 3 |
| `dropout` | float | `0.2` | [0.0, 1.0); only active between layers |

### 2.2 Forward (`forward(x)`)
| Tensor | Shape | Dtype |
|---|---|---|
| `x` | `(batch_size, 10, 5)` | `float32` |

---

## 3. Outputs

| Tensor | Shape | Dtype |
|---|---|---|
| `y_hat` | `(batch_size, 10)` | `float32` |

---

## 4. Setup (Building Block contract)

```
LSTMExtractor
  Input:  x of shape (B, 10, 5), float32
  Output: y_hat of shape (B, 10), float32
  Setup:  hidden_size, num_layers (1..3), dropout (0..1; between layers)
```

Inherited:
- `ParamCountMixin.count_parameters()` → int
- `SaveLoadMixin.save(path)` / `.load(path)`
- `BaseExtractor.architecture_name() -> "lstm"`

Registered via `@register("lstm")`.

---

## 5. Performance Metrics

| Metric | Target | Notes |
|---|---|---|
| Forward latency | < 3 ms / sample (CPU, batch=64) | LSTM 4-gate overhead |
| Train wall-clock per epoch | < 30 s on CPU at default | ADR-008 |
| Param count (H=128, L=1) | ~69 898 | Documented in §1.3 |
| H2 verdict | Quantitative paired test result + CI | Reported in notebook §7 |

---

## 6. Constraints

- **Hard**: file ≤ 150 LoC (RULES.md §8).
- **Hard**: 4-gate structure preserved (use stock `nn.LSTM`, do not hand-roll).
- **Hard**: input dim per step **must** equal 5; output dim **must** equal 10.
- **Soft**: hidden_size ≤ 256, num_layers ≤ 3.
- **Soft**: dropout > 0 only meaningful when num_layers > 1.

---

## 7. Alternatives Considered

| Option | Chosen? | Reason |
|---|---|---|
| `nn.LSTM` | Yes | Production-grade, well-optimized cuDNN/MKL kernels |
| Hand-rolled LSTMCell | No | Unnecessary; harder to test; slower on CPU |
| Bidirectional LSTM | No | Out of scope (IDEA.md says standard LSTM) |
| Peephole connections | No | Not in `nn.LSTM` standard; out of scope |
| C as init hidden state | No (ADR-003) | Symmetric with RNN choice |
| Layer normalization | No | Adds complexity beyond rubric scope |
| Output via mean pooling | No | Last-step convention |
| GRU | No | Out of scope; available as registry stub for extension demo |
| Stateful between batches | No | Tuples are i.i.d.; statefulness would be incorrect |

---

## 8. Success Criteria & Test Scenarios

### 8.1 Success criteria
1. `LSTMExtractor(...).forward(x)` returns `(B, 10)` for any `B ≥ 1`, `x` of shape `(B, 10, 5)`.
2. `count_parameters()` matches §1.3.
3. Save/load round-trip is bitwise identical.
4. Training 1 epoch on a memorizable subset reduces train loss.
5. Hidden state and cell state initialize to zeros each forward call.
6. With dropout=0 + same seed, two forward passes are bitwise identical.
7. LSTM has more parameters than RNN at the same hidden size (sanity test).

### 8.2 Test scenarios
Per TODO Phase 6d (LSTM-001..045): shape tests, param count, save/load, dropout active in train mode, gradient flow, registry integration, smoke training, comparison with RNN parameter count.

### 8.3 Failure modes
- `num_layers ∉ {1, 2, 3}` → `ValueError`
- `hidden_size ≤ 0` → `ValueError`
- `dropout ∉ [0, 1)` → `ValueError`
- Input shape != `(B, 10, 5)` → upstream `RuntimeError`
- NaN gradient → caught by training loop
