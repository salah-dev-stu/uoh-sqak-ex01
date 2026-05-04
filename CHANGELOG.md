# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simple `MAJOR.MINOR` versioning scheme starting
at `1.00` and incrementing by `+0.01` per change (RULES.md §15).

## [1.00] — 2026-05-04

### Added
- Initial release: HW1 deliverable for course 203.3763 (University of Haifa).
- `SinusoidExtractorSDK` exposing dataset generation, training, evaluation,
  experiment matrix, and OAT sensitivity sweep.
- Three model classes (FC, RNN, LSTM) with `BaseExtractor` ABC, mixins, and
  plugin-friendly model registry (`@register("name")`).
- Strict file-size discipline (every `.py` ≤ 150 logical lines).
- 173 unit + integration tests, 95% statement coverage.
- Lifecycle hooks (`before_train`, `after_epoch`, `after_train`,
  `before_eval`, `after_eval`).
- API gatekeeper stub + FIFO wave queue (no external APIs in HW1, but
  structure preserved per the rubric).
- Comprehensive `docs/` tree: `PRD.md`, `PLAN.md`, `TODO.md` (1042 tasks),
  six per-mechanism PRDs, `PROMPTS.md`, `SUBMISSION_CHECKLIST.md`.
- Jupyter notebook `notebooks/analysis.ipynb` with LaTeX equations,
  per-architecture training curves, MSE heatmaps, OAT sensitivity plots,
  and Wilcoxon signed-rank hypothesis tests.
