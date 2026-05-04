# ADR-008 — Cap epoch wall-clock at 30 s on CPU

**Status**: Accepted (2026-05-04)

## Context
No GPU available. Must keep total experiment matrix under ~6 h to fit the 3-day deadline with margin.

## Decision
Soft target: epoch wall-clock ≤ 30 s on CPU at default config (hidden=128, batch=64, n_train=5000). If exceeded, log a warning and document.

## Consequences
- Default config sized so FC ~ 5 s, RNN ~ 20 s, LSTM ~ 30 s per epoch.
- Early stopping (patience 10) typically halves epochs run vs max_epochs=80.
- Empirical timing (one LSTM run): 24 s end-to-end → ~50 s/epoch was an upper bound; actual is fine.

## Alternatives considered
- **GPU on Colab**: out of project scope; the rubric expects local execution.
- **Bigger budget (60 s/epoch)**: would push total runtime past comfortable margin.
