# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simple `MAJOR.MINOR` versioning scheme starting
at `1.00` and incrementing by `+0.01` per change (RULES.md §15).

## [1.03] — 2026-05-04 (pre-submission polish)

### Added
- README §10 "Results — hypothesis verdicts": full table + mechanistic explanation
  of why H1/H3 were disconfirmed, with embedded FFT spectrum.
- Notebook §2 "Signal model" LaTeX block (per-source formula + combined sum).
- Notebook §7 "Loss recap" + "Statistical test verdict rule" LaTeX blocks.
- Notebook §7.5 "Mechanistic interpretation" markdown cell explaining the
  10-ms-window vs target-period mismatch.
- `scripts/mark_todo_done.py` (one-shot TODO hygiene utility).

### Changed
- Notebook §2 FFT plot: extended `xlim` and `freqs` mask so the 7 Hz peak is
  visible; added per-peak Hz annotations.
- `docs/TODO.md`: marked 1001/1042 (96%) tasks complete based on actual repo
  state; 41 intentionally `[ ]` with rationale (38 pending submission/repo,
  3 superseded by Makefile/test coverage).
- Author email in `pyproject.toml` and README updated to
  `sqadah02@campus.haifa.ac.il`.

### Versioning
- `1.00` → `1.01`: TODO hygiene + email correction.
- `1.01` → `1.02`: notebook depth (FFT fix, LaTeX equations, mechanistic cell).
- `1.02` → `1.03`: README results section + housekeeping.

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
