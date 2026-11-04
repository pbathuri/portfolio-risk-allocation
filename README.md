# DSC Fintech — Global Return Forecasting & Risk Monitor

**Two people, four weeks:** study whether lagged international market returns predict the published S&P series, then evaluate Peter Cotton's online covariance tools for monitoring changing risk. Jane Street inspires chronological evaluation and attention to non-stationarity; **this project does not use Jane Street data**.

The source is [UCI's Istanbul Stock Exchange dataset](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange), listed by UCI under CC BY 4.0. It is a small historical methods benchmark, not a current-market trading system.

## Before Saturday

Complete the [checklist](docs/BEFORE_SATURDAY.md) before **Saturday November 7, 10 a.m. America/Indiana/Indianapolis**. Budget 2–3 hours each. A verifies the data and provenance; B explains features and reproduces the baseline scores. No Kaggle account or API key is needed.

## Run the verified path

From the repository root using Python 3.11:

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

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`. For an offline mechanics exercise run `python scripts/run_forecasting.py --demo`. Real artifacts go to `outputs/real/`; synthetic artifacts go to `outputs/demo/`. Raw data and generated outputs stay out of Git.

**Verified on actual data:** official download → schema/date checks → hashed preparation → lagged features → train/validation baseline scores. See [recorded results and limitations](docs/REAL_DATA_VERIFICATION.md). Ridge did not beat zero on validation. The final test is intentionally withheld.

## Implemented versus planned

Implemented: downloader, source validation, two-row-lagged returns, rolling features, training-only preprocessing, chronological 60/20/20 splits after warm-up, zero/mean/persistence/ridge baselines, 17 tests and four notebooks.

Still team work: feature ablations, `precise` monitor integration, uncertainty analysis, interactive dashboard and final test evaluation. No trade execution or P&L backtest is claimed.

| Location | Purpose |
|---|---|
| `src/forecasting.py` | Features, splits, baseline models and metrics |
| `scripts/` | Download, inspect, prepare, run and notebook verification |
| `notebooks/` | Four guided synthetic exercises; real runs use the explicit CLI |
| `docs/` | Checklist, roadmap, methods, source attribution and recorded real results |
| `legacy/portfolio/` | Original allocation exercises, isolated from this workflow |

[Data and license](docs/DATA.md) · [Features](docs/FEATURES.md) · [Methods](docs/METHODS.md) · [Roadmap](docs/ROADMAP.md) · [Team](docs/TEAM.md) · [DSC learning map](docs/LEARNING_MAP.md) · [Delivery](docs/DELIVERY.md).

Repository name retained for continuity. Earlier plans in Git history and `docs/archive/five-week-plan/` are historical, not current instructions.
