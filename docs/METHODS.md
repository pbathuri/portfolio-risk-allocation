# Methods and evaluation boundaries

The source is the UCI dataset described in DATA.md. Target SP is the publisher's S&P return series. Nine return lags and four SP rolling statistics end at t−2; see FEATURES.md. This is a historical statistical prediction study, not a trading strategy.

Remove the first 21 rows as fixed warm-up, then split the ordered observations 60/20/20. Fit median imputation, standardization and ridge on training only. Ridge alpha is fixed at 1 before the real run. Compare zero, training mean, two-row SP persistence and ridge. Do not retune to erase an unfavorable result.

Metrics use equal weights. Report RMSE in the source's return units and zero-mean R², `1 - sum((y-prediction)^2)/sum(y^2)`. Zero denominator is undefined. These retain an evaluation idea from market forecasting, but are not the Jane Street competition metric on its data. The zero predictor has R²=0 for a nonzero target denominator.

The CLI scores training and validation only. Test targets are not used in fitting, missingness reports, feature selection or score exports. Predictor histories in a later partition can include already observed earlier returns; all windows remain two observations behind their prediction target. No overlapping forward multi-day target is constructed.

Cross-market timing/holiday alignment and source revision timestamps are not fully documented. The lag is conservative, not proof of tradability. Use the findings to discuss predictive limits and risk, not alpha, return-on-investment or simulated trading profit.

The future `precise` experiment and final evaluation are specified in EXPERIMENT.md. The older portfolio exercise lives separately in `legacy/portfolio/`.
