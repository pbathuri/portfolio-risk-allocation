# Global Return Forecasting & Risk Monitor

A four-week DSC project for two people: test whether lagged international market returns help predict the published S&P return series, then compare static and adaptive covariance estimates.

The first real-data run is complete. On validation, ridge regression scored **−0.079 zero-mean R²**, below the zero-return benchmark. The next step is to test whether the rolling features help and whether the result is stable across earlier time periods. [Results and reproduction details](docs/REAL_DATA_VERIFICATION.md).

## Get started

Python 3.11, from the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/fetch_data.py
python scripts/inspect_source.py
python scripts/prepare_forecasting.py
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
python -m unittest discover -s tests
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. The download needs no account or API key. For an offline exercise, run `python scripts/run_forecasting.py --demo`.

Results are written to `outputs/real/`; synthetic runs use `outputs/demo/`. Raw data, generated outputs and credentials stay out of Git.

## Data and scope

The [UCI Istanbul Stock Exchange dataset](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange) has 536 historical observations from 2009–2011 and is listed under CC BY 4.0. We use two-observation-lagged inputs, chronological splits and training-only preprocessing. The final 103 observations remain unscored.

This is a small research study. It does not establish current-market performance or trading profitability. Jane Street's public research themes inform the evaluation approach; Peter Cotton's `precise` library is the planned covariance experiment. No Jane Street data is used.

## Work plan

- **Implemented:** download, data checks, lag/rolling features, four baselines, tests and learning notebooks.
- **Next:** one feature ablation, development-period stability checks, static versus online covariance, and a focused results dashboard.
- **Final:** freeze the method, evaluate the reserved period once, and publish a short report with reproducible evidence.

**Next deadline:** [work due November 14](docs/BEFORE_NOVEMBER_14.md). If you still need setup, use the [first checklist](docs/BEFORE_SATURDAY.md). The [four-week plan](docs/ROADMAP.md) covers ownership and deliverables.

## Repository guide

| Path | Contents |
|---|---|
| `src/forecasting.py` | Features, time splits, baselines and metrics |
| `scripts/` | Download, inspection, preparation, execution and notebook verification |
| `tests/` | Numerical, data-contract and temporal-leakage checks |
| `notebooks/` | Four short synthetic exercises |
| `docs/` | Data, methods, plan and recorded results |

[Data and attribution](docs/DATA.md) · [Methods](docs/METHODS.md) · [DSC learning goals](docs/LEARNING_MAP.md) · [Validation](docs/VALIDATION.md) · [Sources and career context](docs/SOURCES.md) · [Contributing](CONTRIBUTING.md).
