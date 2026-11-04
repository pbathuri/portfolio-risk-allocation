# Forecasting checkpoint validation — November 3, 2026

## Implemented and exercised

- New forecasting tests: 17 cases. Fresh Python 3.11 environment: 16 passed, one optional Parquet test skipped because the default requirements do not include a Parquet engine. In the existing environment with pyarrow: all 17 pass.
- Four new notebooks: valid schemas and successful execution in actual fresh Jupyter kernels on Python 3.11.
- Synthetic CLI: zero/mean/ridge metrics, predictions, missingness, feature catalog and manifests generated; final test not scored.
- Source inspection and bounded preparation exercised with synthetic CSV; Parquet selection exercised in the pyarrow-enabled environment.
- Original portfolio exercises: six numerical/data-contract tests still pass after relocation.
- Python compile checks, active documentation links, ten-task owner/reviewer backlog, empty committed notebook outputs and `git diff --check` pass.

Meaningful coverage includes hand-calculated weighted metrics, undefined denominators, invalid weights, duplicate keys, complete-date splits, same-symbol/day lag resets, future-feature isolation, held-out-target isolation, training-only preprocessing, all-missing columns, demo/real output separation, row-cap rejection and changed-input manifest rejection.

No lint/type-check tooling is configured in the repository; compile checks are not presented as a type-checker run. No new required dependencies were added. Versions of numerical packages and Python are written into each run manifest; record a full environment lock for research releases.

## Real-source attempt

November 3, 2026: repaired a broken machine-local Kaggle CLI in a temporary environment (no required dependency change). Official competition file listing succeeded. Downloading only `train.parquet/partition_id=0/part-0.parquet` returned HTTP 403. Removing the environment token to test the alternate credential configuration instead returned authentication required. No training data was downloaded; no real-data score or end-to-end pass is claimed. Account rules acceptance or credentials must be resolved before continuing.

## Not validated or completed

Real Kaggle access/downloads, exact competition field availability and label-release timing, a purged split, the competition online inference API, real-data accuracy, `precise` integration, uncertainty analysis, final test evaluation, interactive dashboard and cluster execution remain team work. No market-performance or profitable-trading claim is made. The default workflow intentionally withholds test evaluation.

Source-partition completeness must be checked by the data owner; preparation preserves groups within the supplied file only. A small selected slice is not proof of representativeness.

The previous project's validation record is retained under `legacy/portfolio/docs/VALIDATION.md` and does not validate the new workflow. Hosted CI status is available on GitHub for the published commit.

## Signed-in browser follow-up

The user is signed in, but the data page still requests competition-rules acceptance. The official data description confirms `responder_6`, 79 anonymized input features, unique date/time/symbol keys, varying time intervals, and prior-day responder availability at the next day's first time step. More importantly, rules section B.7 limits use to competition participation/Kaggle forums and requires deleting data after the competition. The standalone student-project data route is on hold pending a permitted replacement source or appropriate permission. No agreement was accepted and no real data was downloaded.
