# Per-Mechanism PRD — Fully Connected (FC) Model

| Field | Value |
|---|---|
| Mechanism | Fully Connected baseline extractor |
| Owner module | `src/sinusoid_extractor/models/fc_model.py` |
| Registry name | `"fc"` |
| Document version | 1.00 |
| Last updated | 2026-05-04 |
| Companion docs | `PRD.md` §3.2 (FR-MOD-2), `PLAN.md`, `TODO.md` Phase 6b |

---

## 1. Theoretical Background

The Fully Connected (FC) network is the **baseline** in our triple. It has **no temporal structure**: it sees the input as a flat 14-dim vector (4-dim one-hot $C$ + 10-sample window $x$ from $\Sigma$) and emits a 10-dim prediction $\hat{y}$.

Forward equation for a 2-hidden-layer instantiation:
$$
\begin{align}
h_1 &= \mathrm{Dropout}(\mathrm{ReLU}(W_1\,[\,C,\,x\,] + b_1)) \\
h_2 &= \mathrm{Dropout}(\mathrm{ReLU}(W_2\,h_1 + b_2)) \\
\hat{y} &= W_3\,h_2 + b_3
\end{align}
$$

with $W_1 \in \mathbb{R}^{H \times 14}$, $W_2 \in \mathbb{R}^{H \times H}$, $W_3 \in \mathbb{R}^{10 \times H}$.

### 1.1 Role
The FC's role is to set a **floor**: any architecture that fails to beat FC on a given (frequency, noise) cell suggests that the recurrent inductive bias is *not* helping there. Conversely, when RNN or LSTM beats FC by a wide margin, that gap quantifies the value of the temporal mechanism.

### 1.2 Why ReLU + Dropout
- ReLU is the canonical hidden-layer activation in FC regression heads (cheap, gradient-friendly, well-studied).
- Dropout (0.2 default) regularizes against the small training set (5 000 tuples).
- Output is **linear** (no activation): the targets are bounded sinusoidal values in roughly $[-1.05, +1.05]$; bounding the output (tanh/sigmoid) would be a step toward "classification-think" and constrain learning.

### 1.3 Parameter count
For $H = 128$, 2 hidden layers:
$$
P = (14 \cdot 128 + 128) + (128 \cdot 128 + 128) + (128 \cdot 10 + 10) = 1\,920 + 16\,512 + 1\,290 = 19\,722
$$
For $H = 256$, 2 hidden: $P = 75\,786$.

---

## 2. Inputs

### 2.1 Constructor (`__init__`)
| Param | Type | Default | Range |
|---|---|---|---|
| `input_dim` | int | `14` | == 14 (fixed by problem) |
| `output_dim` | int | `10` | == 10 |
| `hidden_size` | int | `128` | > 0 |
| `num_layers` | int | `2` | 1, 2, or 3 |
| `dropout` | float | `0.2` | [0.0, 1.0) |

### 2.2 Forward (`forward(x)`)
| Tensor | Shape | Dtype |
|---|---|---|
| `x` | `(batch_size, 14)` | `float32` |

The 14-dim input is the concatenation `[one_hot (4); window (10)]`.

---

## 3. Outputs

| Tensor | Shape | Dtype |
|---|---|---|
| `y_hat` | `(batch_size, 10)` | `float32` |

The 10-dim output is the predicted clean window of the *selected* sine (selected by the one-hot in the input).

---

## 4. Setup (Building Block contract)

```
FCExtractor
  Input:  x of shape (B, 14), float32
  Output: y_hat of shape (B, 10), float32
  Setup:  hidden_size, num_layers (1..3), dropout (0..1)
```

Inherited:
- `ParamCountMixin.count_parameters()` → int
- `SaveLoadMixin.save(path)` / `.load(path)`
- `BaseExtractor.architecture_name() -> "fc"`

Registered via `@register("fc")` in `models/registry.py`.

---

## 5. Performance Metrics

| Metric | Target | Notes |
|---|---|---|
| Forward latency | < 0.5 ms / sample (CPU, batch=64) | Trivially fast |
| Param count (H=128, L=2) | ~19 722 | Documented in §1.3 |
| Train MSE on α=0.01, freq=60 Hz | converges to < 0.05 in ≤ 30 epochs | Floor benchmark |
| Test MSE on α=0.05 (mean over freqs) | < 0.20 | Acceptance for "non-trivial baseline" |

---

## 6. Constraints

- **Hard**: input dim **must** equal 14; output dim **must** equal 10.
- **Hard**: file ≤ 150 LoC (RULES.md §8).
- **Soft**: hidden_size ≤ 256, num_layers ≤ 3 (per IDEA.md guidance).
- **Soft**: dropout in {0.0, 0.2, 0.4} for OAT (PLAN.md §5.1).

---

## 7. Alternatives Considered

| Option | Chosen? | Reason |
|---|---|---|
| Hidden = ReLU | Yes | Standard, proven, cheap |
| Hidden = Tanh | No | RNN already uses tanh; using same here would muddy the comparison. |
| Hidden = GELU | No | Marginal benefit on small models; complicates baseline. |
| Output = tanh | No | Would clip target range and slow learning. |
| Output = sigmoid scaled | No | Same. |
| Skip connections (ResNet-FC) | No | Adds complexity beyond rubric scope. |
| BatchNorm | No | Tiny model; not needed. |
| LayerNorm | No | Same. |
| Weight init = Kaiming | Yes (PyTorch default for Linear w/ ReLU) | Default is fine. |

---

## 8. Success Criteria & Test Scenarios

### 8.1 Success criteria
1. `FCExtractor(...).forward(x)` returns `(B, 10)` for any `B ≥ 1`.
2. `count_parameters()` matches the formula in §1.3 within 0 (no off-by-one).
3. Training 1 epoch on a memorizable subset (200 tuples) reduces train loss by at least 50%.
4. `save → load → forward` round-trip is bitwise identical.
5. With dropout=0 and identical seed, two forward passes are bitwise identical.

### 8.2 Test scenarios
- Unit: shape, gradient flow, param count, dropout determinism — TODO FC-008..030.
- Smoke: 1-epoch training on tiny dataset — FC-030.
- Integration: registry build returns `FCExtractor` — FC-028.

### 8.3 Failure modes
- `num_layers ∉ {1, 2, 3}` → `ValueError`
- `hidden_size ≤ 0` → `ValueError`
- `dropout < 0` or `≥ 1` → `ValueError`
- Input dim != 14 → upstream `ShapeError` from `nn.Linear`
