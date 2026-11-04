# Real-data verification — November 3, 2026

**Result: official download → preparation → features → baseline validation completed successfully.** This is a forecast-evaluation checkpoint, not a trading P&L backtest or a completed dashboard.

## Source and reproduction

Akbilgic, O. (2013). *ISTANBUL STOCK EXCHANGE* [Dataset]. UCI Machine Learning Repository. [DOI](https://doi.org/10.24432/C54P4J). [Source](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange). [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: date parsing/sorting and derived causal lag/rolling features; raw return values retained.

```bash
python scripts/fetch_data.py
python scripts/inspect_source.py
python scripts/prepare_forecasting.py
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
```

Actual source: 64,063 bytes, 536 rows, 10 columns, 2009-01-05 through 2011-02-22. No missing numeric source cells or duplicate dates. Source contains two distinct ISE columns with ambiguous metadata; they are retained without invented units. The actual parsed start date differs from the catalog description.

Source SHA-256: `a01d8921bd9bfa7bed330f2058279e7d587bb795007b612dc29dfea9905c2853`

Prepared SHA-256: `4108124c29592dc72364727bff5b045e98820c4866dda6c6ac301ce49b75d8f6`

## Frozen configuration and split

Target SP; all engineered inputs end at t−2; SP rolling windows 5/20; 21 warm-up rows; training-only imputation/scaling; ridge alpha=1; equal-weight metrics. No choices were changed in response to the real scores.

| Split | Rows | First date | Last date |
|---|---:|---|---|
| train | 309 | 2009-02-03 | 2010-04-26 |
| validation | 103 | 2010-04-27 | 2010-09-22 |
| test | 103 | 2010-09-23 | 2011-02-22 |

## Validation results

| Model | RMSE (source return units) | Zero-mean R² |
|---|---:|---:|
| zero | 0.01501122 | 0.000000 |
| training_mean | 0.01511566 | -0.013963 |
| persistence_lag2 | 0.02109483 | -0.974787 |
| ridge | 0.01559542 | -0.079350 |

Ridge is worse than the zero-return benchmark on validation. This is not evidence of profitable prediction. The team should reproduce and explain the result before testing one predeclared feature ablation.

## Limits

The final 103 observations were not scored or used to select features/hyperparameters. One final source row was viewed during the initial date/schema inspection; this is not a claim of perfect label blinding. No aggregate final-test outcome was inspected.

The source is short and historical, follows the Istanbul trading calendar, and does not establish point-in-time vendor availability, dividend/cost treatment, execution feasibility or current-market validity. The two-row delay is a conservative modeling convention, not a guaranteed trading timestamp.

`precise` integration, uncertainty analysis, final test scoring and the interactive dashboard are later team deliverables. Jane Street data is not used.

## Environment

Python 3.11.15; numpy 2.4.6; pandas 2.3.3; scikit-learn 1.9.1. Full run manifest remains in local outputs. No new required dependency was introduced.
