# ADR-002 — Uniform amplitude noise

**Status**: Accepted (2026-05-04)

## Context
`IDEA.md` gives free choice between uniform and Gaussian for amplitude noise (it explicitly *requires* uniform [0, 2π] for phase). Uniform is bounded; Gaussian has tails.

## Decision
Amplitude noise = `Uniform(-α·A, +α·A)` per sample.

## Consequences
- Bounded perturbations; no fat tails surprising the model.
- Easy α-sweep semantics: at α=0.10 every sample is within ±10% of the carrier.
- Simpler reproducibility analysis than Gaussian.

## Alternatives considered
- **Gaussian(0, α)**: rejected as the *default* but kept available via `NoiseDistribution.GAUSSIAN` for OAT extension.
- **Salt-and-pepper**: rejected — non-physical for this signal model.
