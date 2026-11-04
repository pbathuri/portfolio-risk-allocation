# Experiment contract

## Frozen checkpoint

Source, attribution and normalization: DATA.md. Features: FEATURES.md. Download hash and observed results: REAL_DATA_VERIFICATION.md. Fixed target SP, two-observation predictor delay, 21-row warm-up, chronological 60/20/20 split and ridge alpha=1 were set before real scoring. Record every later change and its reason.

The 309 training observations fit preprocessing and models; 103 validation observations support choices. The final 103 observations are withheld. Do not use test outcomes for exploratory feature selection. The starter's tests verify lag/window causality, training isolation, metric edge cases, duplicate-date handling and input hashes.

## Week 1 feature hypothesis

Compare return-lag-only ridge with the existing lags plus rolling-statistics ridge on identical validation rows. Choose the comparison before running it. Keep alpha=1 for this ablation; extra tuning is optional only if time permits and logged as validation-driven. Report every variant, not only the winner.

## Cotton-library experiment (Week 2)

Implement one `precise` exponentially weighted covariance estimator on the nine return series, with a fixed rate selected on development data. Compare with static training covariance. Use covariance state based only on observations available before the scored vector; score first, update second. For same-target-date cross-market safety, use vectors delayed two observed rows in the forecasting monitor. Record the exact library version, warm-up and handling of missing/singular matrices.

Show covariance/correlation drift and an equal-weight basket variance estimate. A basket risk diagnostic is not a traded portfolio return. If comparing variance forecasts to realized squared basket returns, align the dates and state the noisy-proxy limitation. Do not claim shift-detection accuracy without ground-truth labels or prediction improvement from an unrelated covariance chart.

## Weeks 3–4

Freeze the feature/model/monitor choices before final evaluation. Report RMSE and zero-mean R² with identical rows across methods. Use paired contiguous-observation block resampling of error differences, with 200 resamples and a predeclared block length; show sensitivity and acknowledge the short test period. The source calendar is irregular, so describe blocks as observations, not uniform days.

The current runner intentionally has no final-test flag. Implement that evaluation only after the team records its freeze and peer review. A bug correction requires a disclosed rerun, not hidden retuning. Final outputs must distinguish training estimates, validation choices and one final test evaluation.

Retain the two-asset variance and three allocation-baseline exercise separately. No execution prices, costs, dividends or precise trading availability are established for the forecast project; no P&L or profitable-alpha claims.
