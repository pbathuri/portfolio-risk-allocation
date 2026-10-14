# Five-week roadmap

Week 1 begins at kickoff; enter actual dates on the issue board. Every gate needs a peer review and mentor sign-off.

## Week 1 — Acquire and define the experiment

**Build:** Check WRDS access and schema; agree universe, frequency and fixed date boundaries.

**Learn:** Distinguish prices from total returns; inspect delistings, identifiers and missing returns.

**Evidence:** Canonical returns.csv, data register and signed experiment plan.

**Done when:** Unique date/asset keys; decimal returns; approved training/validation/test dates.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 2 — Measure return and risk

**Build:** Calculate annualized mean, covariance, volatility, correlation and drawdown.

**Learn:** Derive portfolio variance, including covariance terms, for two assets.

**Evidence:** Metric notebook, covariance heatmap and benchmark report.

**Done when:** Hand calculation matches Python; covariance is symmetric; no filling missing returns with zero.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 3 — Compare allocation rules

**Build:** Fit three baselines; generate feasible portfolios; select any tuning on validation only.

**Learn:** Explain instability in estimated means and the effect of concentration.

**Evidence:** Weights, validation comparison, allocation cloud and method decision.

**Done when:** Weights sum to one; no negative weights; all estimates use pre-test data.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 4 — Stress and visualize

**Build:** Freeze method; evaluate test period once; add block-bootstrap uncertainty and dashboard controls.

**Learn:** Explain expected versus realized risk; test sensitivity to start dates and costs.

**Evidence:** Dashboard, held-out metrics, HPC run record and stress memo.

**Done when:** Test dates are untouched during selection; rebalancing convention and costs are visible.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 5 — Release and defend

**Build:** Reproduce results from a fresh environment; document data-publication restrictions.

**Learn:** Communicate uncertainty and distinguish historical comparison from advice.

**Evidence:** Interactive dashboard, 6-slide brief and release record.

**Done when:** Second student reruns; export permissions checked; limitations and benchmark included.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## If time gets tight

Keep acquisition, one defensible baseline, validation and the final explanation. Defer extra seasons/assets, advanced models and visual polish. Do not replace missing real data with unlabeled demo outputs.
