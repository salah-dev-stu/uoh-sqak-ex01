# ADR-010 — Lifecycle hooks via `HookRegistry`

**Status**: Accepted (2026-05-04)

## Context
RULES.md §18.5 requires "lifecycle hooks: clear connection points (e.g. `before_train`, `after_evaluate`) — middleware-style." Plugins must attach without modifying core code.

## Decision
A `HookRegistry` class with `register(event, fn)` and `fire(event, **ctx)`. Events are named via the `HookEvent` enum: `BEFORE_TRAIN`, `AFTER_EPOCH`, `AFTER_TRAIN`, `BEFORE_EVAL`, `AFTER_EVAL`. Hook exceptions are caught and logged (best-effort).

## Consequences
- `TrainingLoop` and `EvaluationService` fire events at clean lifecycle points.
- Plugins (e.g. a TensorBoard logger) can attach without editing core files.
- Tested via a no-op listener per event.

## Alternatives considered
- **Direct subclassing of `TrainingLoop`**: tighter coupling; harder to combine multiple plugins.
- **`signals` (blinker) library**: extra dep; our stdlib implementation is < 50 LoC.
