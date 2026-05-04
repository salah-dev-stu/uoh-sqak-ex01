# ADR-004 — Adam as default optimizer

**Status**: Accepted (2026-05-04)

## Context
`IDEA.md` lists Adam and RMSprop as acceptable optimizers. Adam is the de-facto modern default for small regression nets.

## Decision
Adam ($\\beta_1=0.9$, $\\beta_2=0.999$, $\\epsilon=10^{-8}$), lr=1e-3 by default.

## Consequences
- Faster convergence on most regression problems.
- Less sensitive to lr choice.
- Well-tested against RNN/LSTM training quirks.
- RMSprop available via `Optimizer.RMSPROP` and exposed in OAT (training cfg override).

## Alternatives considered
- **SGD with momentum**: needs careful lr tuning; slower for tiny models.
- **AdamW**: weight-decay variant; not needed at this model scale.
