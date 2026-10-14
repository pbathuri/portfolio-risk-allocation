# Portfolio experiment

Freeze the universe, dates and metric definitions in Week 1. The baseline uses training data only to estimate all three allocation rules and holds the target weights fixed thereafter, with monthly rebalancing. Validation is for diagnosing and choosing optional changes; all three predefined baselines may be reported on the test period. Do not repeatedly choose the best-looking test strategy.

For monthly decimal returns r and weights w:
- Expected annual arithmetic return = 12 × wᵀ mean(r). This is an estimate, not a promised return or CAGR.
- Annualized covariance = 12 × sample covariance(r); variance = wᵀΣw; volatility = sqrt(variance).
- Equal weight: 1/n. Inverse volatility: (1/σᵢ)/Σⱼ(1/σⱼ), which ignores correlation. Minimum variance: minimize wᵀΣw subject to w≥0 and Σw=1.
- Diversification/concentration: show pairwise correlations, HHI = Σwᵢ² and effective holdings = 1/HHI. More names alone do not ensure lower risk.
- Realized CAGR = ending wealth^(12/months) − 1. Drawdown is wealth / running peak − 1, including initial wealth 1.
- Historical 95% VaR is the 95th percentile of monthly losses; ES is the mean loss at or beyond it. These are descriptive, unstable in small samples, and not maximum possible losses.

The random Dirichlet allocation cloud is **not** a solved efficient frontier. It is a reproducible sample of feasible long-only portfolios. Include portfolio_id → asset weights so dashboard selection can be audited. A true frontier and covariance shrinkage are optional extensions; compare them on validation before testing.

Monthly turnover = half the L1 distance between target weights and weights after last month's returns. Costs are expressed in basis points per unit of this one-way turnover. The default illustration uses 10 bps; compare 0, 10 and 25. Initial entry costs are excluded; the first period starts invested at target. This convention must appear in the dashboard. No taxes, financing, market impact or shorting are modeled.

Annualization assumes stable enough moments; serial dependence can invalidate sqrt(12) scaling. The six-month circular block bootstrap is a sensitivity calculation conditional on fixed weights, not a correction for all estimation error. Try block lengths 3, 6 and 12 and show interval sensitivity. For mean-estimation uncertainty, refit in each training resample as an extension.

No Sharpe ratio is supplied without a correctly aligned risk-free series. Do not call mean return divided by volatility a Sharpe ratio unless its zero-risk-free assumption is explicit.

HPC task: repeat the allocation simulation and block bootstrap over five seeds. Compare wall time for 5,000 versus 100,000 candidate portfolios only after measuring memory. Report when the laptop is faster after queue overhead. A large GPU model is unnecessary here.
