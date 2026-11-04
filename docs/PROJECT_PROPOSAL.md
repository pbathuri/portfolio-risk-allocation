# DSC Fintech: Adaptive Market Forecasting & Risk Monitor

Status: selected four-week project direction for `pbathuri/portfolio-risk-allocation`. A synthetic-tested acquisition/feature/baseline starter is implemented. Real-data research, covariance monitoring and the dashboard remain team work; no market results are claimed. Updated November 3, 2026.

## Decision

Combine the two equally supported options (one vote each): an experimental Python component inspired by Peter Cotton, evaluated in a research setting using Jane Street's public market-forecasting competition. Build a reproducible analytical project and dashboard in four weeks with two students. Live trading and alpha claims are outside scope.

**Research question:** Does a simple market-response predictor remain useful across time, and can an online covariance monitor expose changes in its input distribution and error profile?

This separates two measurable questions: predictive accuracy and monitoring usefulness. A covariance monitor does not automatically improve a predictor. A negative result is acceptable if the experiment is reproducible and its limitations are clear.

## Minimum credible deliverable

1. A documented, bounded slice of Jane Street's 2024–2025 Real-Time Market Data Forecasting competition dataset, obtained under its access and reuse terms.
2. Zero-prediction and training-mean baselines, plus one regularized linear model predicting `responder_6` from permitted contemporaneous features. Verify these field names and availability against the downloaded schema before implementation.
3. One Cotton-library experiment: `precise` exponentially weighted covariance on a fixed, small set of input features; compare it with a fixed training covariance. Monitor input structure, with errors shown retrospectively once labels become available.
4. A dashboard showing held-out model scores, daily error patterns, changing feature correlations, and data/provenance information.
5. A short research report, a five-minute demonstration, a clean reproduction path, and individually attributable reviewed work.

The AI component is the fitted predictive model. A chatbot is unnecessary. The dashboard replays historical data and refreshes computed results; it must not imply a live market feed.

## Scope and feasibility

Budget assumption: 6–8 hours per student per week, including the Saturday meeting; 48–64 combined hours. CPU-first. Start with at most 500,000 rows, a small training-selected symbol universe, and at most 10 features for covariance monitoring. Read selected Parquet columns/partitions instead of loading the full dataset. Freeze the actual row count, chronological boundaries, symbols, columns, and file hashes after profiling. Preserve complete selected date/symbol groups; do not randomly sample individual rows across time.

Keep the existing Python data-analysis stack where possible. The starter already includes scikit-learn. Proposed additions for implementation are a Parquet reader and `precise`, with exact versions recorded after an installation smoke test. The default CSV checkpoint uses the existing dependencies; Parquet input uses an already-available pyarrow environment. No new required dependencies were added. Use the existing Tableau/Power BI export workflow if present; an extra web framework is optional only after the analysis works.

Cut first: neural networks, hyperparameter sweeps, LLM summaries, automated trading, full-dataset training, and cloud deployment. If Kaggle access fails, use the starter's documented public-return source and recast the question as adaptive portfolio risk; label it Jane Street-inspired, not a Jane Street-data study. Synthetic data remains a plumbing test only.

## Evidence and attribution

- [Jane Street-hosted competition overview](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/overview): the public benchmark motivates studying non-stationarity and distribution shifts. It is a historical competition, not a newly announced 2026 release.
- [Competition data](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/data) and [rules](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/rules): verify access, schema, label timing, evaluation definition and redistribution permissions at kickoff. The data page did not expose readable schema text during this review.
- [Peter Cotton's profile](https://github.com/microprediction) and [`precise`](https://github.com/microprediction/precise): primary attribution for online covariance estimation. This is the selected experimental library; its exact API/version must be frozen before use.
- [`timemachines`](https://github.com/microprediction/timemachines) now describes anomaly detection built on `skaters`; older forecasting-wrapper tutorials may be incompatible. Treat it as background reading, not a second required integration.
- [`skaters`](https://github.com/microprediction/skaters) is an optional reading source. Its own README cautions about use on price/return series; do not assume universal forecasting superiority.

Sources inspected November 3, 2026. These support library capabilities and research motivation, not broad industry adoption, endorsement, guaranteed performance, or access to Jane Street's proprietary strategies. No particular LinkedIn post was supplied or verified.
