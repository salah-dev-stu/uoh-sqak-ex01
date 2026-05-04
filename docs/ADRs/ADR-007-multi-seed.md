# ADR-007 — At least 3 seeds per data point

**Status**: Accepted (2026-05-04)

## Context
Hypothesis testing needs variance estimates. A single run per cell cannot deliver effect size + confidence interval.

## Decision
Each base experiment cell (arch × alpha) runs ≥ 3 seeds (default `seeds: [42, 123, 7]`). OAT runs use 1 seed each (time budget).

## Consequences
- Statistical claims about H1 / H2 / H3 become defensible (Wilcoxon paired test).
- Total runtime ~3× a single-seed matrix, mitigated by small models + early stopping.
- Reproducibility: every run is deterministic given (arch, alpha, seed).

## Alternatives considered
- **5+ seeds**: better stats, but ~5× runtime; not affordable in a 3-day budget on CPU.
- **1 seed**: cheapest but cannot quote effect size; lecturer expects rigor.
