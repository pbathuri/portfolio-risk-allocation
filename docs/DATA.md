# Data acquisition and checkpoint contract

Primary source: [Jane Street Real-Time Market Data Forecasting data](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/data). Read the [rules](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/rules) with your own account. Public access does not establish unrestricted redistribution. No real competition data is bundled or downloaded by the demo.

## Verified access preflight

On November 3, 2026, the official file-listing command succeeded using Kaggle CLI 2.2.5. The smallest listed training partition was `train.parquet/partition_id=0/part-0.parquet` (470,341,709 bytes, about 470 MB). Listing files does **not** prove download access: the subsequent download returned HTTP 403 for the current account. Real-data execution is pending access resolution.

Before allocating download time, review/accept the competition rules in the same account used by the CLI. If already accepted, check that the CLI credentials belong to that account. Do not share tokens. A missing-dependency error before any HTTP request indicates a broken local CLI environment, not a competition permission failure; use a clean CLI environment or the web download route.

Once access is enabled, the verified command target is:

```bash
kaggle competitions download jane-street-real-time-market-data-forecasting -f 'train.parquet/partition_id=0/part-0.parquet' -p data/raw
```

Inspect the actual downloaded path before passing it to `inspect_source.py`; no real source schema or date IDs have yet been verified by this repository's maintainer.

## Pull a bounded input

Use Kaggle's web file listing to inspect size and download **one training file**, not the whole competition. If you already use the authenticated official CLI:

```bash
kaggle competitions files jane-street-real-time-market-data-forecasting
kaggle competitions download jane-street-real-time-market-data-forecasting -f 'EXACT_FILE_FROM_LISTING' -p data/raw
```

Replace the placeholder with the actual listed path; extract a ZIP locally if returned. See [official CLI commands](https://github.com/Kaggle/kaggle-cli/blob/main/docs/competitions.md). Credentials belong in Kaggle's documented local credential mechanism, never in Git or notebook cells. CLI installation is optional; web download is sufficient.

Prefer a private Kaggle notebook if the source is too large for the laptop. Attach the official competition data there; place this repo's `src/forecasting.py` and `scripts/prepare_forecasting.py` in the same relative layout, inspect the actual mounted training path, then run the same selection command using that path. Kaggle normally supplies Parquet support; check the environment. Export a bounded CSV only if terms permit, otherwise keep the entire exercise in that environment.

## Inspect, choose, prepare

```bash
python scripts/inspect_source.py --input data/raw/SELECTED_FILE.parquet
```

This streams only date and symbol identifiers and prints schema plus group counts. Choose the earliest suitable block of about 30 consecutive available dates and 2–3 symbols. Record exclusions without consulting responder values. Identify the chosen source's partition boundaries so no selected date/symbol group is incomplete. The tool guarantees completeness only within the supplied file.

Example command shape — **replace all IDs and the filename with the inspected values**:

```bash
python scripts/prepare_forecasting.py --input data/raw/SELECTED_FILE.parquet --start-date 0 --end-date 29 --symbols 0 1 2 --output data/processed/checkpoint.csv
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
```

IDs 0–29 and symbols 0/1/2 are examples, not guaranteed available rows. The preparation command accepts CSV too. It streams in batches, projects required columns, preserves matching groups and fails above 500,000 selected rows. Reduce whole groups if needed. At least 10 distinct dates are required; 30+ is preferable. Hashing reads the whole source file once for provenance; account for that I/O.

## Required schema

| Columns | Contract |
|---|---|
| `date_id`, `time_id`, `symbol_id` | Nonnegative integer identifiers; unique combined key |
| `weight` | Finite nonnegative evaluation/sample weight; positive total in each scored split |
| `feature_00` … `feature_09` | Ten numeric contemporaneous inputs; NaN allowed, infinity rejected |
| `responder_6` | Numeric target; finite for train/validation, never used as a feature; final test target may be missing |

Confirm field availability and timing against the official schema before making competition-equivalence claims. The web data page did not expose readable schema during preparation. Unexpected schema is a blocker to resolve, not a reason to rename unrelated columns.

The ordered distinct dates split 60% train, 20% validation, 20% withheld test; exact IDs are written to the run manifest. This initial subset is educational and does not reproduce the official competition evaluation API. Audit target horizon and any boundary purge at Saturday's methods review before research conclusions.

## What may be committed

Code, selection recipes, source URLs and permitted aggregate summaries. Local raw/processed/demo data and generated outputs are ignored. Do not commit Kaggle credentials, row-level predictions, raw CSV/Parquet, or executed real-data notebook outputs. A private GitHub repo does not automatically satisfy data terms.

If access remains blocked, use `--demo` for mechanics and report the limitation. A switch to genuine-return research is a mentor scope decision; archived acquisition helpers live under `legacy/portfolio/scripts/`.
