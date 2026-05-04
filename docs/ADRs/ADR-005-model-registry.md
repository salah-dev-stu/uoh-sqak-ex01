# ADR-005 — Model registry / factory pattern

**Status**: Accepted (2026-05-04)

## Context
RULES.md §18.5 requires a plugin architecture: "ability to add new functionality WITHOUT changing core code." The trainer needs to dispatch architecture name (string) → model class.

## Decision
A `_Registry` class exposing `@register("name")` decorator and `build(name, **kwargs)` factory. New models add themselves at import time.

## Consequences
- Adding a Transformer = create one new file `models/transformer_model.py` decorated with `@register("transformer")`. No edits to existing files.
- Registry is process-wide (singleton-like). Tests can `clear()` for isolation.
- `available()` lists registered names; CLI uses this to validate `--arch`.

## Alternatives considered
- **`if/elif` ladder in trainer**: violates plugins-architecture requirement; couples trainer to all archs.
- **Subclass discovery via `__subclasses__`**: works but harder to document; explicit decorator is clearer.
