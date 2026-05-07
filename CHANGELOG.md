# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simple `MAJOR.MINOR` versioning scheme starting
at `1.00` and incrementing by `+0.01` per change (RULES.md §15).

## [1.05] — 2026-05-04 (README screenshot embedding pass)

### Added
- README now embeds **all 7 plots** from `results/figs/` and the **3 terminal
  screenshots** in `assets/`:
  - `assets/test_run.png` + `assets/hard_gates.png` in §Testing
  - `assets/training_demo.png` after §Quick start
  - `results/figs/dataset_components.png` in §Overview (problem visualisation)
  - `results/figs/mse_heatmaps.png`, `mse_per_arch_bar.png` extending §Results
  - `results/figs/reconstructions.png` in new §Reconstruction examples
  - `results/figs/loss_curves.png` in new §Training dynamics
  - `results/figs/oat_sensitivity.png` in new §Sensitivity analysis (OAT)
- New top-level README sections: **§Reconstruction examples**, **§Training
  dynamics**, **§Sensitivity analysis (OAT)** — each with embedded plot +
  caption explaining what to look at.

### Changed
- README §Table of contents extended from 16 to 19 sections.

## [1.04] — 2026-05-04 (visual coverage pass)

### Added
- `scripts/regenerate_plots.py` — re-renders `loss_curves.png` (2×2
  multi-noise grid, train+val per arch) and `reconstructions.png` (4 target
  frequencies, 5 traces each: noisy input + clean target + per-arch
  predictions, with per-window MSE annotations) from existing artefacts.
- Notebook §4 "Observations" markdown cell: 3 bullet observations on
  train/val tracking, noise-level floor, and LSTM late-epoch descent.
- Notebook §5.1 "Reconstruction examples" markdown subsection embedding
  the new reconstructions plot with mechanistic commentary linking it
  back to §7.5.

### Changed
- Notebook §4 loss-curves cell rewritten as 2×2 grid (one panel per α),
  6 lines per panel (FC/RNN/LSTM × train/val), shared legend at top.
- `results/figs/loss_curves.png` regenerated from the multi-noise grid.

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
