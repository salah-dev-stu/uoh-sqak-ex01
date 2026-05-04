# ADR-006 — JSON for configuration

**Status**: Accepted (2026-05-04)

## Context
Need a config format. Lecturer expects JSON (rubric examples are in JSON). Stdlib parses JSON natively, no extra dependency.

## Decision
JSON for `setup.json`, `rate_limits.json`, `logging_config.json`. Comment fields prefixed with `_` and stripped at load time.

## Consequences
- Zero deps for parsing.
- Auditable (the grading agent can `cat` the file).
- No comments in JSON; we use `_comment` keys as a convention.

## Alternatives considered
- **YAML**: would need PyYAML; supports comments, but adds a dep.
- **TOML**: native to Python 3.11+ via `tomllib`, but less familiar to ML community.
