# Portfolio dashboard build sheet

Use Tableau or Power BI with exports from notebook 04. Three pages:
1. **Allocation comparison:** training-estimated return/volatility scatter; select a portfolio_id to display its asset weights; compare the three named baselines and HHI.
2. **Realized performance:** held-out wealth curves, CAGR, volatility, drawdown and monthly VaR/ES; show test dates and the monthly rebalancing/cost convention.
3. **Risk structure:** training correlation heatmap, per-asset weights and stress/uncertainty view; keep expected and realized measures visually distinct.

Relate portfolio_cloud to portfolio_weights on portfolio_id (one-to-many). Keep strategy-level test metrics separate from candidate-portfolio estimates. Do not imply all random portfolios have a backtest. For arbitrary weight sliders, implement the same vector/matrix equations in the BI layer or a reviewed Python calculation service; static CSV exports support selection among precomputed portfolios only. The minimum deliverable is interactive selection and comparison of those portfolios.

Tableau: select portfolio_id via filter/highlight action, show weight bars linked through a relationship. Power BI: use portfolio_id slicer and a relationship to the weights table. Validate any aggregate at its grain; do not sum volatility or annualized return across rows.

Acceptance tasks: identify the lowest-volatility baseline on training data, compare its held-out drawdown with equal weight, and inspect a concentrated allocation. A peer should complete each in under two minutes. Reconcile three portfolio metrics manually and compare selected weight sums to 1.

A sample historical loss is not a future worst case. Label all expected values as training estimates. Submit a workbook or permitted interactive link, source/data-use note, outputs, and a six-slide presentation. If using French data, identify the investments as research industry portfolios. If WRDS terms restrict distribution, demonstrate within the permitted environment and publish only approved aggregate views.
