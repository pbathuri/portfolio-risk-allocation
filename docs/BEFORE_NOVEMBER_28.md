# Before Saturday, November 28

**Due: November 28, 2026, by 10 a.m. Eastern.** This week is for finishing the forecast checks and getting a reproducible static/online covariance comparison. Keep the final test period unscored. Allow about 4–6 hours each; flag holiday availability early rather than rushing an unverified result.

## Where we stand

As of November 23, Andrew's [PR #1](https://github.com/pbathuri/portfolio-risk-allocation/pull/1) is open and its automated checks pass. The original-window comparison is documented: adding rolling features slightly worsened ridge RMSE, and neither ridge version beat zero. The PR description is still blank and no peer review is recorded. Earlier-window results and covariance outputs are not yet present on the shared branches; if completed locally, push and link them instead of repeating the work.

## Andrew — finish the PR and supply the static benchmark

- [ ] Fill in PR #1 with the question, commands, findings and test results. Replace the environment/commit placeholders in the checkpoint note with verified values. Ask Manish to reproduce it and address any review comments. Passing CI alone is not a methods review; leave merging to the maintainer after review.
- [ ] On a separate branch, implement the fixed sample-covariance benchmark from the [November 21 specification](BEFORE_NOVEMBER_21.md). Use the same nine-series order, equal weights and initialization history agreed with Manish. Use sample covariance with `ddof=1`; record that convention.
- [ ] Export one predicted basket variance per validation date. Hand-check a two-series example and test symmetry, finite entries and nonnegative basket variance within a stated numerical tolerance.
- [ ] Once Manish's earlier-window tables are available, write a short forecast recommendation across all three periods. Keep zero in the comparison and explain mixed results rather than selecting only the best window. If those tables are missing, mark the decision provisional.

**Deliver:** updated PR #1, a static-covariance PR and the forecast summary. The static work can proceed while the forecast PR is under review.

## Manish — publish the earlier windows and supply the online estimate

- [ ] Review Andrew's PR and reproduce the original-window results. Leave a short review describing what you ran and whether it matched, not just an approval.
- [ ] Push the Earlier 1 and Earlier 2 comparisons using the [fixed November 14 windows](BEFORE_NOVEMBER_14.md). Include both ridge feature sets plus zero, training-mean and persistence baselines. Refit preprocessing on each training window; do not retune alpha or dates.
- [ ] Implement one exponentially weighted covariance estimator from `precise` at the fixed update rate of 0.05, following the November 21 specification. Record the package version, exact estimator and parameter meaning. Do not change the rate after inspecting errors.
- [ ] Test the estimator first on a small synthetic stream, then run it on the same real-data initialization and validation dates as Andrew. Verify that changing row t or t−1 cannot alter the variance predicted for row t, and that the state receives each eligible row exactly once.

**Deliver:** the earlier-window results, a review on PR #1, and an online-covariance PR with a reproduction command. If setup fails, push the small reproducible example and error; do not present a substitute implementation as a completed `precise` integration.

## Agree on the shared input before running the comparison

Use [November 21](BEFORE_NOVEMBER_21.md) as the common method contract:

- Nine return series in the order defined by `src/forecasting.py`; weights are all 1/9. No annualization or rescaling.
- Validation: April 27–September 22, 2010, 103 observations. Both estimators initialize on the same complete rows starting February 3, 2009 and ending at t−2 for the first validation observation.
- At date t, save `wᵀΣw` before the online estimator ingests row t−1 for the next prediction. The static estimate never updates. The delay counts observed rows, not calendar days.
- Compare predicted variance with `(wᵀr_t)²`, using mean absolute error over identical dates. Squared basket return is a noisy variance proxy under a near-zero-mean assumption, not a direct observation of true variance or trading profit.

Before pairing the outputs, exchange the source hash, series order, weights, initialization dates and observation count. Join on date with a one-to-one check. A mismatch is a bug to resolve, not a reason to silently drop rows. Explain any exclusions.

## Joint handoff

- [ ] Save local daily outputs under `outputs/week2/` with columns `date`, `static_variance`, `online_variance` and `squared_basket_return`. Include both methods in a two-row summary table with MAE, date range and sample count.
- [ ] Andrew owns `docs/results/week2.md`; Manish reviews it. Include the earlier forecast results, forecast recommendation, covariance table, one chart, commands, source attribution and package versions. Discuss one period where static and online estimates differed.
- [ ] Each person reproduces one result from the other's branch. Link those checks in the PRs and resolve failures before calling the work complete. Use feature branches and PRs into `main`; do not overwrite each other's work.
- [ ] Record a brief proposal for the final experiment: chosen forecast features, baselines, covariance estimator/rate and evaluation rules. This is ready for review only when the supporting development results are complete.

## Thanksgiving priorities and what comes next

By **Wednesday, November 25**, share branch links and any blockers so the other person can keep working. If time is tight, finish the PR review and earlier-window tables first, then get the static and online outputs aligned. A documented incomplete online run is better than an invented comparison. Defer chart polish and dashboard work.

On Saturday, bring a two-minute explanation each and the result links. We will decide whether the evidence is ready to freeze. **Do not score September 23, 2010–February 22, 2011 yet.** Dashboard work and the December 5 final review depend on completing these checks; if necessary, revise the release date instead of skipping evaluation safeguards.
