# Experiment contract

## Freeze before testing

Record the dataset version/hash, row filters, feature list, target, weight field, missing-value policy, split boundaries, seed, dependency versions and machine. Sort by date/time and symbol. All symbols at a timestamp belong to the same chronological partition. Use the first 60% of distinct dates for training, next 20% for validation and final 20% for testing; replace percentages with explicit date IDs in the frozen configuration. If label horizons overlap a boundary, purge that overlap using the documented horizon.

Fit imputation/scaling on training only; add missingness indicators where useful. Never backfill from the future. Exclude all responder columns from predictors in the MVP. Do not use lagged labels unless their availability is explicitly verified and tested. Predict from allowed current features; log predictions before labels are read. Evaluate historical labels offline, without using them to update the predictor during the test.

## Models and scores

Compare zero, training weighted-mean and ridge regression. Tune ridge regularization using only three predeclared values on validation; no test-driven feature selection. Use identical rows and weights for every comparison.

Proposed primary metric is weighted zero-mean R²: `1 - sum(w * (y - prediction)^2) / sum(w * y^2)`. Verify it against the competition evaluation page before freezing. Do not substitute centered R². Reject negative/nonfinite weights and nonfinite predictions; zero total weight or zero denominator yields an explicitly undefined score, not zero. Also show weighted RMSE, per-day results, row counts and missingness. Report pooled scores from summed numerators and denominators, not an average of daily R² values.

## Cotton-library monitoring experiment

Use the same fixed, training-standardized feature vectors for a static training covariance and one `precise` exponentially weighted covariance estimator. Select features using training missingness and variance, never held-out performance. Record deterministic handling of simultaneous rows; prefer one feature-mean vector per timestamp across the frozen symbols to avoid arbitrary symbol-order updates. This measures covariance of aggregate feature observations, not asset-return covariance.

Score each new vector against the preceding monitor state, then update with that vector. Regularize covariance before inversion; log warm-up, singularity and insufficient-observation cases. Choose a single forgetting rate and alert percentile on validation, then freeze them. Compare covariance drift and alert frequency, and examine subsequent error descriptively. Without known shift labels, do not claim detection accuracy or a calibrated false-positive rate. Monitoring is not a trading signal.

If testing an alert-based abstention rule, define it before unlocking test labels and compare coverage as well as error. Otherwise leave abstention out of the MVP.

## Leakage and uncertainty checks

- Changing future rows must not change earlier predictions or monitor scores.
- Changing held-out labels must not change preprocessing, model fitting or alerts.
- Train/validation/test timestamps must not overlap; no duplicate keys.
- Hand-check weighted R² and RMSE on a tiny table, including zero-weight and constant-zero-target cases.
- Check covariance dimensions, symmetry, finite values and update ordering.
- Bootstrap paired model error differences in contiguous day blocks, not independent rows; use 200 resamples and state the chosen block length and sensitivity. Interpret intervals cautiously when the test slice has few days.

Freeze after Week 3 and open the test partition once in Week 4. Corrections after a discovered bug require a versioned rerun and disclosure; they do not justify retuning on test outcomes.

## Keep portfolio learning honest

Use the existing return-data exercise to hand-check two-asset variance and compare equal weight, inverse volatility and minimum variance. Retain it as a bounded learning exercise separate from the forecasting benchmark. Anonymous responder values and input-feature covariances are not tradable returns: do not compute portfolio Sharpe, P&L or dollar risk from them. If the fallback becomes the main project, use documented genuine return units and the starter's cost/rebalancing conventions.
