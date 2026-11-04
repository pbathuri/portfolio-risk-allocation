# Before Saturday: a small forecasting checkpoint

> **Real-data plan on hold:** The signed-in official rules were inspected November 3, 2026. They restrict the data to competition participation/Kaggle forums and require deletion after the competition ends (section B.7). This does not establish permission for the proposed standalone student project. Do not accept rules or download this dataset merely to complete this checklist. Use the synthetic exercises while the organizer chooses an appropriately permitted source or obtains permission. No competition data has been downloaded. [Official rules](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/rules).

**Due:** Saturday November 7, 2026, before the 10 a.m. meeting (America/Indiana/Indianapolis). **Budget:** 2–3 hours per person. Claim A or B in the Teams channel now. Work together on the same agreed source/slice; do not independently choose different datasets.

The starter intentionally supplies basic code. Your work is to obtain permitted data, make and document the selection, verify what the features mean computationally, inspect development outputs, and explain what you learned. Running a supplied command alone is not the full assignment.

## Both — setup and first run (20–30 minutes)

1. Pull the latest repository and follow the README environment instructions.
2. Run `python scripts/run_forecasting.py --demo` and `python -m unittest discover -s tests`.
3. Read [DATA.md](DATA.md) and [FEATURES.md](FEATURES.md). Agree who is A and B; record your names in the checkpoint note.
4. Do not inspect or score the final test labels. Do not tune a model yet.

## Person A — data acquisition and QA (60–90 minutes)

1. Open the official competition data/rules pages linked in DATA.md; confirm your own access and permitted use. Record access status and any restrictions.
2. Select one training Parquet file/partition using the actual Kaggle listing. Inspect its size before downloading. If too large, use a private Kaggle notebook with attached competition data and export a bounded CSV only where terms permit.
3. Use `scripts/inspect_source.py` to inspect identifiers and schema without target statistics. Agree a small universe of 2–3 symbols and about 30 consecutive available date IDs from an early source partition. Use at least 10 dates and at most 500,000 rows. Freeze this initial choice before looking at validation scores; this is a teaching subset, not a representative market claim.
4. Use `scripts/prepare_forecasting.py` with those actual IDs. Keep complete selected groups within the source file; verify that source partition boundaries do not split those groups. If the cap fails, narrow whole date/symbol groups rather than taking a random sample.
5. Fill in the data section of [CHECKPOINT_TEMPLATE.md](CHECKPOINT_TEMPLATE.md): source filename/hash, dimensions, selected IDs, column names, duplicate/missingness checks and selection limitations. Share the reproducible selection recipe with B; raw data stays in approved storage.

**Bring:** a local `data/processed/checkpoint.csv` and its manifest, a completed data note, and one concrete QA observation. Do not commit the data or credentials.

## Person B — features and initial benchmark (60–90 minutes)

1. While A works, run the synthetic workflow and read `src/forecasting.py` alongside FEATURES.md.
2. Hand-check three rows for one symbol: current feature, missingness indicator, and previous observed same-day feature. Explain why the first lag of each day is missing and why no responder becomes an input.
3. When A's slice is ready, run `python scripts/run_forecasting.py --input data/processed/checkpoint.csv`. If it is not ready, continue with the labeled demo and record the blocker.
4. Inspect `outputs/real/feature_catalog.csv`, `missingness.csv`, `metrics.csv`, and `manifest.json`. Record train/validation dates, rows, weighted RMSE and zero-mean R² for zero, mean and ridge. Report an undefined R² honestly if applicable.
5. Propose **one** future feature experiment (for example, removing the lag features or comparing missingness indicators). Specify the hypothesis and the validation comparison; do not run a tuning sweep before Saturday.

**Bring:** a short feature note, one baseline table, one data/model concern and one experiment proposal. A negative score is useful evidence, not something to hide.

## Both — cross-check (20–30 minutes)

- Each opens one small PR/branch: A's acquisition/QA note and B's feature/baseline note. Use `docs/checkpoints/` for the completed Markdown note only after verifying aggregate publication permission. Otherwise present the note locally.
- Review the other person's explanation and rerun one command. Record who reproduced what.
- Bring a two-minute walkthrough each. Saturday starts with these outputs, not environment installation.

## If blocked

After 30 minutes, record the exact error (without tokens), what you tried and what help is needed. By Friday 6 p.m. post a short access status in Teams yourself. Continue with synthetic data so the feature/metric exercise still gets done. Do not switch to a different financial dataset silently; the meeting will decide the scope fallback.

**Saturday success:** one documented slice or precise access blocker; an explainable feature pipeline; a correctly labeled baseline comparison; and a concrete Week 1 experiment. No dashboard, deep learning or live trading is due this week.
