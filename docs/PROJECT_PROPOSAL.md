# Project: Global Return Forecasting & Risk Monitor

Two students, four weeks, 6–8 hours per person per week. Combine the two equally supported directions: practitioner-inspired online covariance tooling and a disciplined empirical forecasting study.

**Question:** Can lagged international market returns improve prediction of the published SP series, and does an online covariance monitor describe changing risk structure better than a static estimate?

Use [UCI dataset 247](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange), listed under CC BY 4.0, with attribution in DATA.md. It is a small historical benchmark; research credibility comes from reproducibility, causal evaluation and clear limitations, not size or profitable claims. The organizer approved this replacement after the Jane Street competition-use restriction was confirmed. Do not describe this as a Jane Street-data project.

Jane Street inspiration: time-ordered evaluation, non-stationarity and strong baselines. Peter Cotton contribution: study one `precise` online covariance estimator against a static training covariance. Monitor quality and predictor quality are separate hypotheses.

Implemented: official CSV acquisition, provenance, lagged features, baseline pipeline and tests. Verified real results are in REAL_DATA_VERIFICATION.md. Still to build: feature ablation, `precise` integration, uncertainty, interactive dashboard and final held-out evaluation.

Scope: four fixed baselines; one feature ablation; one online/static covariance comparison; three dashboard views; a 2–3 page report and five-minute demonstration. CPU-only is sufficient. No neural-network search, LLM interface, live trading or cloud deployment is required. A negative result is a successful project if the analysis is sound.

Preserve the DSC portfolio-statistics and allocation-comparison exercises in `legacy/portfolio/`, separate from the primary forecast results. Follow ROADMAP.md, EXPERIMENT.md and DELIVERY.md. Public availability does not imply that the data are recent, representative or point-in-time tradable.
