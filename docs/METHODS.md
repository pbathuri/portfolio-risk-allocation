# Methods and evaluation boundaries

The source is the UCI dataset described in DATA.md. Target SP is the publisher's S&P return series. Nine return lags and four SP rolling statistics end at t−2; see the feature definitions below. This is a historical statistical prediction study, not a trading strategy.

Remove the first 21 rows as fixed warm-up, then split the ordered observations 60/20/20. Fit median imputation, standardization and ridge on training only. Ridge alpha is fixed at 1 before the real run. Compare zero, training mean, two-row SP persistence and ridge. Do not retune to erase an unfavorable result.

Metrics use equal weights. Report RMSE in the source's return units and zero-mean R², `1 - sum((y-prediction)^2)/sum(y^2)`. Zero denominator is undefined. These retain an evaluation idea from market forecasting, but are not the Jane Street competition metric on its data. The zero predictor has R²=0 for a nonzero target denominator.

The CLI scores training and validation only. Test targets are not used in fitting, missingness reports, feature selection or score exports. Predictor histories in a later partition can include already observed earlier returns; all windows remain two observations behind their prediction target. No overlapping forward multi-day target is constructed.

Cross-market timing/holiday alignment and source revision timestamps are not fully documented. The lag is conservative, not proof of tradability. Use the findings to discuss predictive limits and risk, not alpha, return-on-investment or simulated trading profit.



## Feature definitions

Predict the published SP return for observation t using information ending at t−2. All transformations are in `src/forecasting.py`.

| Family | Definition | Reason / limitation |
|---|---|---|
| Nine return lags | Each published return series shifted by two observed rows | Avoid current-row and same-day international close relationships; observations are not calendar days |
| Four SP rolling statistics | Mean and sample standard deviation over 5 and 20 observations, ending at t−2 | Simple return/risk history; fixed windows, not selected using validation scores |
| Missingness flags | One flag per engineered input | Explicit absent information; no missing inputs in this actual development run |
| Imputation/scaling | Medians, means and scales fit on training only | All-missing training inputs dropped; no future fill |

Fixed warm-up is 21 rows: at t=21 the 20-observation window ending at t−2 covers rows 0–19. Remaining 515 observations split 309/103/103 into train/validation/withheld test.

Hand check: for SP values 0,1,2,..., at row 21 the lag is 19, the 20-row mean is 9.5 and sample standard deviation uses ddof=1. Changing rows 20 onward cannot alter row 21's predictors.

Do not create same-day cross-market features or select features against the final test. Future student ablation: compare lag-only inputs with lags plus rolling statistics on identical validation rows. Missingness flags are an engineering safeguard, not evidence of a useful signal here.

## Research comparisons

### Feature ablation


Compare return-lag-only ridge with the existing lags plus rolling-statistics ridge on identical validation rows. Choose the comparison before running it. Repeat it on two expanding training windows within the training/validation period to see whether the conclusion depends on one split. Write down those boundaries before running; keep the final 103 rows excluded. Keep alpha=1 for this ablation; extra tuning is optional only if time permits and logged as validation-driven. Report every variant, not only the winner.

## Covariance comparison (Week 2)

Implement one `precise` exponentially weighted covariance estimator on the nine return series, with a fixed rate selected on development data. Compare with static training covariance. Use covariance state based only on observations available before the scored vector; score first, update second. For same-target-date cross-market safety, use vectors delayed two observed rows in the forecasting monitor. Record the exact library version, warm-up and handling of missing/singular matrices.

Show covariance/correlation drift and an equal-weight basket variance estimate. A basket risk diagnostic is not a traded portfolio return. If comparing variance forecasts to realized squared basket returns, align the dates and state the noisy-proxy limitation. Do not claim shift-detection accuracy without ground-truth labels or prediction improvement from an unrelated covariance chart.

## Final evaluation (Weeks 3–4)

Freeze the feature/model/monitor choices before final evaluation. Report RMSE and zero-mean R² with identical rows across methods. Use paired contiguous-observation block resampling of error differences, with 200 resamples and a predeclared block length; show sensitivity and acknowledge the short test period. The source calendar is irregular, so describe blocks as observations, not uniform days.

The current runner intentionally has no final-test flag. Implement that evaluation only after the team records its freeze and peer review. A bug correction requires a disclosed rerun, not hidden retuning. Final outputs must distinguish training estimates, validation choices and one final test evaluation.


## Portfolio-statistics exercise

Use training returns only to hand-check two-asset variance, including covariance. Compare equal-weight, inverse-volatility and long-only minimum-variance allocations on the same nine-series training covariance. Normalize weights to sum to one; document any regularization and show concentration. This is a small risk-estimation exercise using published index series, not a separately traded portfolio or another application to build.

Keep the forecasting and risk questions separate. A lower estimated basket variance does not establish better return forecasts. The dashboard should allow a reader to trace each result to its data, dates and method.
