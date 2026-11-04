# DSC Fintech — Adaptive Market Forecasting & Risk Monitor

> **Real-data plan on hold:** The signed-in official rules were inspected November 3, 2026. They restrict the data to competition participation/Kaggle forums and require deletion after the competition ends (section B.7). This does not establish permission for the proposed standalone student project. Do not accept rules or download this dataset merely to complete this checklist. Use the synthetic exercises while the organizer chooses an appropriately permitted source or obtains permission. No competition data has been downloaded. [Official rules](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/rules).

A **two-person, four-week** research project combining Jane Street's public forecasting challenge with Peter Cotton's online covariance work. We ask: **does a simple predictor remain useful over time, and can an adaptive covariance monitor expose changes in its inputs and errors?**

## Before Saturday: start here

Complete the [pre-Saturday checklist](docs/BEFORE_SATURDAY.md) before **November 7, 2026, 10 a.m. America/Indiana/Indianapolis**. Budget 2–3 hours each. Bring a reproducible small data slice, a feature explanation, a first validation table, and any access blockers. A synthetic-only run is an honest fallback, not a real-data result.

## Run the new starter

From the repository root, with Python 3.11:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_forecasting.py --demo
python -m unittest discover -s tests
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`. All subsequent commands are the same. CSV mode and the synthetic demo use existing dependencies. For Parquet, use an environment that already includes `pyarrow` (such as Kaggle's notebook environment), or export the bounded CSV there. No new dependency is required by the default workflow.

The demo writes clearly labeled synthetic artifacts under `outputs/demo/`: baseline metrics, train/validation predictions, development missingness, a feature catalog and a split/version manifest. **The final test partition is withheld.**

For permitted real inputs, follow [DATA.md](docs/DATA.md), then run:

```bash
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
```

Real outputs go to `outputs/real/`. Keep inputs, row-level predictions and generated notebook outputs off GitHub. Only commit approved aggregate summaries and code. The [checkpoint template](docs/CHECKPOINT_TEMPLATE.md) tells you what evidence to bring.

## What is implemented

- Chunked local CSV/Parquet selection with explicit dates, symbols, row cap and source hashes.
- Schema checks, duplicate-key rejection, chronological whole-date 60/20/20 splits.
- Ten raw features, missingness flags and three same-symbol/same-day lag features.
- Training-only median imputation/scaling and zero/mean/ridge baselines.
- Tests of metrics, future-data isolation, lags and data selection; four learning notebooks.

**Still to build during the four weeks:** the real-data experiment, `precise` monitor, model/feature ablations, uncertainty analysis, interactive dashboard and final test evaluation. Synthetic results validate the starter mechanics only. Existing notebooks do not claim a completed model or dashboard.

## Team workflow

[Saturday preparation](docs/BEFORE_SATURDAY.md) → [meeting agenda](docs/KICKOFF.md) → [roadmap](docs/ROADMAP.md) → [experiment contract](docs/EXPERIMENT.md) → [delivery criteria](docs/DELIVERY.md).

[Two-person ownership](docs/TEAM.md), [task backlog](docs/BACKLOG.csv), [DSC learning map](docs/LEARNING_MAP.md), [source evidence](docs/SOURCES.md), [validation record](docs/VALIDATION.md) and [assistant-use policy](docs/AGENT_POLICY.md).

| Location | Purpose |
|---|---|
| `src/forecasting.py` | Validated features, splits, baseline metrics and checkpoint exports |
| `scripts/` | Source inspection, slice preparation, baseline runs and notebook checks |
| `notebooks/00_setup.ipynb` through `03_baselines.ipynb` | Guided synthetic exercises; explicit opt-in instructions for real data |
| `docs/` | Current forecasting plan, task assignments, methods and evidence templates |
| `legacy/portfolio/` | Original portfolio allocation code and notebooks, isolated as an optional DSC statistics exercise |

The original five-seat planning documents are archived under `docs/archive/five-week-plan/`. They do not define current deadlines. The repository name is retained for continuity.
