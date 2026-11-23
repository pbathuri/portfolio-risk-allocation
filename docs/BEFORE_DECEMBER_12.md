# Final review — Saturday, December 12

**Due: December 12, 2026, 10 a.m. Eastern.** Run this checklist only after the [December 5 freeze](BEFORE_DECEMBER_5.md) is approved. If that gate is incomplete, record the blocker and agree a revised scope/date before scoring final data.

## By Tuesday, December 8 — final results

- [ ] **Andrew:** Run the frozen final-evaluation command. Save source/config hashes, code commit, environment, sample counts and forecast/risk metrics under a distinct final-output directory. Keep every baseline and the selected model in the report, regardless of rank.
- [ ] **Andrew:** Run the predeclared paired block-bootstrap comparisons. Describe the intervals and small-sample limitations without claiming that a non-significant difference proves equivalence.
- [ ] **Manish:** Reproduce that exact frozen run and compare output metrics within a documented numerical tolerance. Explain any mismatch before publishing results. This is a reproduction check, not a new tuning round.
- [ ] **Manish:** Load the final exports into the dashboard. Clearly separate development comparisons from final results, and reconcile the displayed values, counts and dates with the saved outputs.

## By Thursday, December 10 — release candidate

- [ ] **Andrew:** Finish the 2–3 page report and `docs/results/final.md`: research question, data/license, frozen method, development findings, final findings, uncertainty and limitations. Link the run manifest and PRs. Distinguish return forecasting from risk estimation; neither is a trading P&L backtest.
- [ ] **Manish:** Test installation and reproduction from a clean checkout. Update README commands, dependency versions and local dashboard instructions. Verify the dashboard's three intended tasks without relying on your development environment.
- [ ] **Both:** Close review comments, run tests/CI, check source attribution and ensure no credentials or unintended raw/output files are committed. Record who implemented, reviewed and reproduced each part.
- [ ] **Both:** Rehearse a five-minute demonstration: question and data, forecast finding, covariance finding, limitations and reproduction. Each person explains one calculation and one design choice.

## Saturday acceptance

The maintainer reviews the result package and approves the release. Completion requires:

1. Reviewed code for the feature comparison and actual `precise` integration.
2. Three development-window forecast comparisons and aligned static/online covariance evidence.
3. An approved freeze followed by a traceable final evaluation and independent reproduction.
4. A working local dashboard, report, clear setup commands and passing CI.
5. A candid account of negative findings, dataset limits and each person's contribution.

Keep the test results even if a baseline wins. Do not turn a disappointing result into another parameter search. If part of the package remains incomplete, list it explicitly and present the project as a prototype rather than a completed research release. Hosting, live feeds and additional models are not release requirements.
