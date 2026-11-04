# Before Saturday: reproduce a real-data checkpoint

**Due:** Saturday November 7, 2026, 10 a.m. America/Indiana/Indianapolis. **Budget:** 2–3 hours each, counted toward Week 1. Claim A/B in Teams. The source is UCI's openly licensed international-return dataset; no Kaggle login is needed.

## Both — setup (20–30 minutes)

Pull the repo, follow README environment setup, run `python scripts/run_forecasting.py --demo` and `python -m unittest discover -s tests`. Read DATA.md and FEATURES.md. Use REAL_DATA_VERIFICATION.md to check your results.

## A — data and provenance (60–90 minutes)

```bash
python scripts/fetch_data.py
python scripts/inspect_source.py
python scripts/prepare_forecasting.py
```

Check 536 rows, 10 columns, unique dates, the source/processed hashes, and the date range. Explain the catalog/file date discrepancy and two ISE columns without guessing their meaning. Document numeric missingness on training/validation data only. Record the CC BY 4.0 attribution and normalization changes. Keep the final period out of exploratory plots.

**Bring:** the local prepared CSV/manifest and the data section of CHECKPOINT_TEMPLATE.md. No data file needs to be committed; both people can download the same 64 KB source independently.

## B — features and baselines (60–90 minutes)

```bash
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
```

If working independently, run A's three commands first. Inspect `outputs/real/metrics.csv`, `feature_catalog.csv`, `missingness.csv` and `manifest.json`. Explain one lag and one rolling-window calculation, the 21-row warm-up, training-only preprocessing and why same-day features are excluded.

Record validation scores for zero, mean, persistence and ridge. Compare with REAL_DATA_VERIFICATION.md; the verified ridge score is negative, which is a valid finding. Propose one lag-only-versus-rolling-feature experiment for Week 1; do not tune yet.

**Bring:** the baseline table, one feature explanation and one hypothesis. Final test remains withheld.

## Both — review (20–30 minutes)

Each opens one small PR with their completed Markdown note under `docs/checkpoints/`, reviews the other's work and reruns one command. Include source credit/license when reporting derived results. Prepare a two-minute walkthrough each. No dashboard is due.

If blocked for 30 minutes, record the error and what you tried (no secrets). Report it by Friday 6 p.m. and continue using the labeled synthetic demo. Saturday will start with your outputs and questions, then choose the next experiment.
