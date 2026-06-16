# Architecture

This project follows a **medallion-style data architecture** (raw → processed → features → reports), inspired by production ML/analytics pipelines.

```
                ┌─────────────┐
                │  01_raw     │   Immutable source data
                └──────┬──────┘
                       │  clean()
                ┌──────▼──────┐
                │ 02_processed│   Deduplicated, imputed
                └──────┬──────┘
                       │  engineer_features()
                ┌──────▼──────┐
                │ 03_features │   CLV, RFM, engagement, tiers
                └──────┬──────┘
                       │  statistics.py / visualisation
                ┌──────▼──────┐
                │   reports/  │   Static PNGs + interactive HTML
                └─────────────┘
```

## Module Responsibilities

| Module | Responsibility |
|--------|-----------------|
| `src/ingestion/pipeline.py` | Load raw CSV, clean (impute/dedupe), engineer derived features |
| `src/analysis/statistics.py` | Descriptive stats, hypothesis tests, correlation, segment profiling, K-Means |
| `src/visualisation/theme.py` | Single source of truth for colour palette / styling (matplotlib + plotly) |
| `src/utils/reporting.py` | KPI computation and markdown findings generation |

## Design Principles

1. **Single source of truth for theme** — every chart (static or interactive) pulls from `theme.py`, so a palette change propagates everywhere.
2. **Idempotent pipeline** — re-running `pipeline.py` always reproduces the same processed/feature datasets from the immutable raw file.
3. **Testable core logic** — cleaning, feature engineering, and statistics are pure functions covered by `tests/`, decoupled from notebook/plotting code.
4. **Two-tier reporting** — static PNG dashboards for quick scanning/sharing, plus a single self-contained interactive HTML report for deep exploration.

## Data Flow Summary

| Stage | Input | Output | Script |
|-------|-------|--------|--------|
| Ingest | `data/01_raw/*.csv` | cleaned DataFrame | `pipeline.load_raw`, `pipeline.clean` |
| Engineer | cleaned DataFrame | `data/03_features/*.csv` | `pipeline.engineer_features` |
| Analyse | features DataFrame | CSVs in `data/02_processed/` | `statistics.py` functions |
| Visualise | features DataFrame | PNGs in `reports/figures/` | inline matplotlib/seaborn scripts |
| Report | features DataFrame + figures | `reports/html/interactive_report.html` | Plotly chart generation + HTML assembly |
