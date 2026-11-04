# Current verification — November 3, 2026

The primary workflow uses the openly licensed UCI Istanbul Stock Exchange dataset. Jane Street competition data is not used.

## Passed

- Official real-data download using `scripts/fetch_data.py`: 64,063 bytes and 536 rows.
- Exact student command sequence: download, inspect, prepare, baseline run; provenance and input hashes recorded.
- Real baseline run repeated with identical metric outputs. Details, dates, versions, attribution and limitations: [REAL_DATA_VERIFICATION.md](REAL_DATA_VERIFICATION.md).
- 17 forecasting tests passed on Python 3.11 with no skips, covering metrics, source dates, download validation, lag/window causality, split boundaries, training isolation, withheld-test isolation, missing data and changed-input rejection.
- Four revised notebooks executed in actual Jupyter kernels; synthetic outputs clearly labeled.
- Python compilation, active Markdown links, backlog structure and diff-whitespace checks passed.
- The active test suite covers this forecasting project. Previous portfolio exercises and their separate CI step have been removed.

No new required dependency was added. No lint/type-check tooling is configured; compilation is not claimed as a type-checker run. Hosted CI verifies code and notebooks without requiring a live data endpoint.

## Not yet completed

`precise` monitor integration, feature ablations, uncertainty analysis, final test scoring, interactive dashboard and a student-independent reproduction are still project work. This is a real-data forecast checkpoint, not a completed trading backtest. The final 103 observations remain unscored; see the source-inspection disclosure in the real-data report.

The historical dataset is short and lacks fully documented point-in-time availability and cross-market calendar alignment. No trading-profit, current-market or broad generalization claim is supported.
