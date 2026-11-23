# Before Saturday, December 5 — working dashboard and method freeze

**Due: December 5, 2026, 10 a.m. Eastern.** Complete the [November 28 result package](BEFORE_NOVEMBER_28.md) first. This checkpoint prepares the project for final scoring; it does not authorize scoring early.

## Andrew — report and evaluation specification

- [ ] Resolve PR feedback and consolidate the three-window forecast comparison. Recommend one feature set using all development evidence; retain zero, training mean and persistence as benchmarks. Keep alpha=1 unless a separately documented development-only decision is approved before the freeze.
- [ ] Draft the 2–3 page report: question, data/attribution, chronology, features, forecast comparison, covariance comparison and limitations. Insert real development tables and figures. Mark final results as pending.
- [ ] Implement the final-evaluation entry point and test it only on synthetic or development data. It must require an explicit opt-in and record the frozen commit/configuration, source hash, versions, dates and output path. The default starter must continue to withhold test scoring.
- [ ] Write `docs/results/freeze.md` with the selected features, ridge setting, benchmark definitions, covariance estimator/version/rate, weights, preprocessing, update timing, missing-data handling and metrics. List every development experiment; do not hide negative results.

## Manish — dashboard and independent checks

- [ ] Build a local dashboard with three views: forecast error comparison by development window; static/online basket variance over validation dates; data and run provenance. Use saved outputs. Controls must not retrain or tune on final labels.
- [ ] Reconcile at least three displayed numbers with the saved tables. Confirm that sample counts and dates remain visible and that missing final results are labeled pending.
- [ ] Reproduce Andrew's selected forecast configuration and have Andrew reproduce the covariance comparison. Record commands, environment and any discrepancies.
- [ ] Review the final-evaluation tests and `freeze.md`, especially training-only preprocessing, the two-observation delay, and no duplicate state updates. Run CI and make a clean-install rehearsal.

## Freeze requirements

The maintainer must approve the freeze PR before either person runs the final test. Both must agree on this final protocol in advance:

- Test period stays September 23, 2010–February 22, 2011, 103 observations. No additional model families or parameter searches.
- After selecting the configuration on development data, refit forecasting preprocessing/model and training-mean baseline on the 412 post-warm-up development observations. Predictor values for each test row still use only t−2 or earlier.
- Reinitialize both covariance estimators on the same history beginning February 3, 2009 and ending two observed rows before the first test row. Static covariance stays fixed; the online estimator follows the score-before-update contract. Freeze this initialization policy rather than choosing it from test results.
- Forecast metrics: RMSE and zero-mean R² with equal weights. Risk metric: MAE against the squared equal-weight basket-return proxy. Do not combine these different objectives into one score.
- Uncertainty: paired moving-block bootstrap of per-observation loss differences, block length 5, 200 resamples, seed 42, with a percentile 95% interval. For forecasting compare squared error with zero; for covariance compare online versus static absolute errors. Sample the same blocks for both methods, truncate each replicate to the original length, and state that the short correlated sample limits precision. Any extra sensitivity analysis must be specified before scoring.
- Independent reproduction may rerun identical frozen code; it must not select different settings. Bug fixes require a new commit, an explanation and a disclosed rerun.

**Bring:** a working development dashboard, report draft, green tests, review links and `freeze.md`. Leave the final period unscored until the freeze is approved. Aim to resolve integration blockers by Wednesday, December 2; use the remaining time for verification rather than extra features.
