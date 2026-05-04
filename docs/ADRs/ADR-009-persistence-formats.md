# ADR-009 — `.npz` / `.json` / `.csv` persistence layout

**Status**: Accepted (2026-05-04)

## Context
Need to persist (a) raw signal arrays, (b) per-run metadata + loss histories, (c) aggregated sweep results.

## Decision
- `.npz` (compressed) for numpy arrays (raw signals, reconstructions).
- `.json` for per-run metadata (`loss_history.json`, `eval_report.json`, `hypothesis_test.json`).
- `.csv` for tabular sweep aggregates (`experiment_matrix.csv`, `sensitivity.csv`).

## Consequences
- Notebook can `pd.read_csv()` directly into a DataFrame.
- `np.load()` for raw signals; no custom parsers.
- All three formats are git-friendly diffable (csv) or compact (npz).

## Alternatives considered
- **HDF5**: overkill for this scale; needs `h5py`.
- **Parquet**: better for big tables, but adds `pyarrow` dep.
- **Pickle**: rejected — version-fragile; safer to stick with stdlib formats.
