# Week 1 Feature Comparison

## Question

Do SP rolling statistics improve Ridge forecasts beyond lagged returns on the Original window?

## Method

- **Target:** SP return.
- **Feature timing:** Predict each row using information ending at *t−2*.
- **Lag-only:** Nine lagged return features and their nine missingness flags.
- **Lags + rolling:** The lag-only features plus four SP rolling statistics and their four missingness flags.
- **Warm-up:** First 21 rows removed for both feature sets.
- **Training:** 2009-02-03–2010-04-26; 309 rows.
- **Validation:** 2010-04-27–2010-09-22; 103 rows.
- **Model:** Ridge with alpha=1. Imputation and scaling fit on training data only.
- **Metrics:** Equal-weight RMSE and zero-mean R².
- **Reserved test:** 2010-09-23–2011-02-22; not scored or used for feature selection.

## Original-Window Results

| window | model | feature_set | train_start | train_end | validation_start | validation_end | train_rows | validation_rows | rmse | zero_mean_r2 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| Original | zero | not_applicable | 2009-02-03 | 2010-04-26 | 2010-04-27 | 2010-09-22 | 309 | 103 | 0.015011 | 0.000000 |
| Original | training_mean | not_applicable | 2009-02-03 | 2010-04-26 | 2010-04-27 | 2010-09-22 | 309 | 103 | 0.015116 | -0.013963 |
| Original | persistence_lag2 | not_applicable | 2009-02-03 | 2010-04-26 | 2010-04-27 | 2010-09-22 | 309 | 103 | 0.021095 | -0.974787 |
| Original | ridge | lag_only | 2009-02-03 | 2010-04-26 | 2010-04-27 | 2010-09-22 | 309 | 103 | 0.015498 | -0.065935 |
| Original | ridge | lags_plus_rolling | 2009-02-03 | 2010-04-26 | 2010-04-27 | 2010-09-22 | 309 | 103 | 0.015595 | -0.079350 |

## Finding

On the Original validation window, adding rolling features increased Ridge RMSE by approximately 0.000097 (`RMSE(lags + rolling) − RMSE(lag-only)`). Rolling features did not improve the result on this window. Both Ridge variants had higher RMSE than the zero baseline. This is one historical validation comparison and does not establish predictive performance beyond this sample.

## Earlier-Window Results

Person B: append the results for Earlier 1 and Earlier 2 here using the same table columns. Do not score or inspect the reserved test period. If Earlier 2 is unfinished, mark it unfinished rather than filling in values.

## Reproduction

Run from the repository root:

- `python scripts/run_forecasting.py --input data/processed/checkpoint.csv --feature-set lag_only --output outputs/week1/original_lag_only`
- `python scripts/run_forecasting.py --input data/processed/checkpoint.csv --feature-set lags_plus_rolling --output outputs/week1/original_lags_plus_rolling`
- `python -m unittest discover -s tests` — 20 tests passed.

The final test remains withheld in both run manifests.

## Version and Environment

- Updated main base: `f23f650`
- Python: `3.14.9` (confirm with `python --version` before submitting)
- PR commit: [fill in after committing this work]

## Limitations

The dataset is short and historical, follows the Istanbul trading calendar, and does not fully document cross-market timing. The Earlier windows share training history, so their scores are not independent experiments. Forecast error comparisons do not establish trading profitability.

## Attribution

Akbilgic, O. (2013). *ISTANBUL STOCK EXCHANGE*. UCI Machine Learning Repository. https://doi.org/10.24432/C54P4J. Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Changes: dates parsed, sorted, and normalized; causal lag and rolling features derived.
