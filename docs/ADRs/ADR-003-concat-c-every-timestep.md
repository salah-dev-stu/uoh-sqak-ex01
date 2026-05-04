# ADR-003 — Concatenate one-hot C at every recurrent timestep

**Status**: Accepted (2026-05-04)

## Context
The 4-dim selector $C$ tells the network which sine to extract. `IDEA.md` lists three options:
1. Use $C$ to initialise the hidden state.
2. Use $C$ as input only at $t=0$.
3. Concatenate $C$ to the input at every timestep.

## Decision
Option 3 — concatenate $C$ at every timestep. Per-timestep input dim = 1 (sample) + 4 (one-hot) = 5.

## Consequences
- Robust: even if the network "drifts," the conditioning signal is always present.
- Symmetric: RNN and LSTM see identical conditioning, so any architectural difference traces to the *cell*, not the conditioning strategy.
- Slightly larger input tensor (negligible memory overhead).

## Alternatives considered
- **Init hidden**: harder to test, hidden-state semantics blur.
- **t=0 only**: vanilla RNNs notoriously "forget" early conditioning over 10 steps.
