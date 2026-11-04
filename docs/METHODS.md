# Forecasting methods

The implemented checkpoint predicts `responder_6` from permitted current features and causal feature lags. It compares zero, training weighted-mean and ridge (fixed alpha=1). Sample weights enter ridge fitting and all reported metrics; preprocessing uses training rows only.

The primary provisional metric is weighted zero-mean R²: `1 - sum(w*(y-prediction)^2)/sum(w*y^2)`. Zero denominator is undefined and exported as an empty CSV value / JSON null, never as a fabricated score. Weighted RMSE is `sqrt(sum(w*(y-prediction)^2)/sum(w))`. Zero total weight is an error. Confirm the official evaluation contract at kickoff before claiming exact competition parity.

Chronological splits operate on whole date IDs (60/20/20). Current scripts score only train and validation. Final test scoring deliberately has no CLI flag. Missingness reports also use development rows only. The notebook runs are synthetic by default and explicitly labeled.

See [FEATURES.md](FEATURES.md) for implemented transformations and [EXPERIMENT.md](EXPERIMENT.md) for the future monitor, selection, uncertainty and release protocol. Before final research evaluation, resolve label horizons and purge overlapping boundaries as necessary. The starter does not implement Kaggle's online inference API or a purged splitter.

Peter Cotton's `precise` integration remains a Week 2 task. Study one exponentially weighted covariance estimator on fixed training-standardized features, score before updating, and compare with a static training estimate. Measure its behavior; do not presume better predictions or profitable trades. There is no live trading, P&L, or portfolio-return calculation on anonymous responders.

The optional portfolio-statistics exercise uses real returns or labeled synthetic returns in `legacy/portfolio/`, with a separate source/output contract.
