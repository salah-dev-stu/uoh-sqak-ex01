# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simple `MAJOR.MINOR` versioning scheme starting
at `1.00` and incrementing by `+0.01` per change (RULES.md §15).

## [1.10] — 2026-05-07 (submission packaging — final)

### Added
- `uoh-sqak-ex01.docx` (intermediate; produced by
  `scripts/fill_submission_pdf.py`) and **`uoh-sqak-ex01.pdf`** (the final
  submission cover sheet uploaded to Moodle).
- `.gitignore` excludes worker / orchestration context (`CLAUDE.md`,
  `RULES.md`, `IDEA.md`) from the public repo.

### Final metadata (locked at submission)
- Group code: `uoh-sqak` (Salah Qadah + Andalus Kalash).
- Self-grade recommendation: **90**.
- Student 1: Salah Qadah / סלאח קדח (ID 323039974).
- Student 2: Andalus Kalash / אנדלוס כלש (ID 211435797).
- GitHub: <https://github.com/salah-dev-stu/uoh-sqak-ex01> (public).
- Late: no (submitted before deadline 2026-05-07 23:59).

### Changed
- `scripts/fill_submission_pdf.py` updated with locked values.
- History scrubbed of `IDEA.md` via `git filter-repo --path IDEA.md
  --invert-paths` so the public repo carries no orchestration context.

## [1.09] — 2026-05-07 (asset refresh)

### Changed
- Re-rendered `assets/training_demo.png` so it reflects the v1.06+ rerun:
  shows `VERIFY freqs from SDK: (20, 60, 100, 200)` header, current
  matrix/OAT timings (9.0 min / 9.2 min, was 5.9 / 7.1), and run-directory
  timestamps from the post-redesign run (`20260507T...`, was `20260504T...`).
  No code or docs changed.

## [1.08] — 2026-05-07 (consistency sweep)

### Changed
- Replaced all stale 1/3/5/7 Hz references in upstream docs and notebook
  setup with 20/60/100/200 Hz so every doc tells the same story:
  - `docs/PRD.md` H1/H2 statements + KPI verdict labels.
  - `docs/PRD_dataset.md` Nyquist note + raw-signal table (`pure_*hz`,
    `noisy_*hz` keys).
  - `docs/PRD_evaluation.md` stratification comment + H1/H2 split.
  - `docs/PRD_fc_model.md` floor benchmark frequency reference.
  - `docs/PRD_lstm_model.md` H2 phrasing + cycle-count caveat.
  - `docs/PRD_rnn_model.md` rewritten H1 paragraph: now correctly explains
    the multi-cycle regime (1.0 / 2.0 cycles per window at 100 / 200 Hz)
    and notes that the empirical verdict still disconfirmed H1 — *meaningfully*
    this time, not because of sub-cycle inputs.
  - `docs/TODO.md` 9 task labels (NB-012..015, NB-019, NB-044..046, SIG-009).
  - `README.md` reconstructions caption.
  - `scripts/regenerate_plots.py` docstring reference.
  - `tests/unit/test_splitter.py:42` test fixture freqs (1/3/5/7 → 20/60/100/200)
    so the comment "class index 2 → freq 100 Hz" is accurate; assertion logic
    unchanged (still uses +10/+20/+30/+40 offsets).
  - `notebooks/analysis.ipynb` cell 0 (title + H1/H2) and cell 16 (§5.1
    reconstruction commentary) — fresh interpretations using the new
    cycle-count framing.

### Preserved (intentional historical pointers)
- `CHANGELOG.md` entries for 1.05 / 1.06 / 1.07 — historical record.
- README.md §10 paragraph "the original 1/3/5/7 Hz draft" — explains why
  the redesign matters.
- Notebook §7.5 / §8 mentions of "1/3/5/7 Hz design" — explain the flip.
- `tests/unit/test_dataset_service.py` — uses `_cfg()` fixture with 1/3/5/7
  freqs; assertions test that DatasetService works *for whatever freqs it's
  given*, which is a desirable property to keep tested.

## [1.07] — 2026-05-07 (frequency redesign + full re-experiment)

### Changed
- **Frequencies switched 1/3/5/7 → 20/60/100/200 Hz** (`config/setup.json`,
  `constants.FIXED_FREQUENCIES_HZ`, `IDEA.md`, `docs/PRD.md`,
  `docs/PRD_dataset.md`, README, notebook). Rationale (PRD §3.1, IDEA): the
  10-sample window @ Fs=1000 Hz now covers 0.2 / 0.6 / 1.0 / 2.0 cycles —
  spans sub-cycle and multi-cycle regimes so the recurrence-vs-FC question
  is fairly testable. Previous design placed every target at ≤0.07 cycles
  per window, structurally precluding any recurrence advantage.
- **`Splitter` decoupled** from the `FIXED_FREQUENCIES_HZ` constant — now
  takes `frequencies_hz` as a constructor parameter; `DatasetService`
  passes its own configured value. Two stale tests were caught and tightened
  in the same pass.
- **`SweepService` per-frequency CSV columns are now dynamic**, derived from
  `dataset_service.frequencies_hz`. Was hardcoded to `per_freq_mse_1hz/3hz/5hz/7hz`,
  which silently produced all-NaN columns under the new freqs.
- Notebook §2 dataset visualisation: time-axis shrunk to 100 ms (was 1 s) to
  keep all 4 frequency panels readable; FFT plot's `xlim` now scales with
  `max(FIXED_FREQUENCIES_HZ)`.
- Notebook §7 hypothesis-test cell rewritten to split LOW (20, 60 Hz) and
  HIGH (100, 200 Hz) frequency lists and to dump them in the JSON payload
  for downstream auditing.
- Notebook §7.5 "Mechanistic interpretation" rewritten with the new verdicts
  and concrete per-pair MSE numbers; explains why LSTM still wins at high
  freq even though H1 predicted RNN would.
- Notebook §8 "Conclusion & Reflection" rewritten — now covers what worked,
  what surprised, what's next, plus an honest assessment.
- README §10 verdict table + mechanism paragraph rewritten with the new
  numbers and the "FC is worst, not best" headline.

### Re-ran
- 36 base-matrix runs (~8.4 min CPU) + 36 OAT runs (~9.2 min CPU).
- All 7 plots in `results/figs/`.
- `results/hypothesis_test.json` now records the new verdicts.

### Verdicts (Wilcoxon signed-rank, paired)
- H1 disconfirmed (RNN > LSTM at high freq, p = 1.2e-07).
- H2 confirmed (LSTM < RNN at low freq, p = 2.4e-07).
- H3 confirmed for both arches (FC > RNN p = 3.9e-13; FC > LSTM p = 7.1e-15).

## [1.06] — 2026-05-07 (frequency-redesign spec change)

### Added
- New section in `IDEA.md` and `docs/PRD.md`: "Frequency selection rationale"
  explaining the cycle-fraction reasoning behind 20/60/100/200 Hz.

### Changed
- `config/setup.json` `dataset.frequencies_hz`: `[1, 3, 5, 7]` → `[20, 60, 100, 200]`.
- `constants.FIXED_FREQUENCIES_HZ` updated to match.
- `Splitter` decoupled from the constant; takes `frequencies_hz` via constructor.
- 2 stale tests fixed (`test_splitter`, `test_constants`).

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
