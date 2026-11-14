# Before Saturday, November 21: does updating covariance improve the risk estimate?

**Due: November 21, 2026, by 10 a.m. Eastern.** Bring one forecast decision and one side-by-side risk comparison. Budget about 6–8 hours each, including peer review.

Andrew's [November 14 submission](https://github.com/pbathuri/portfolio-risk-allocation/blob/477ac2a16b7e60ff5174c0e09d4ce2b47bb44ea8/docs/checkpoints/BEFORE_NOVEMBER_15_CHECKPOINT.md) reports original-window RMSE of 0.015498 for lag-only ridge, 0.015595 with rolling features and 0.015011 for zero. The rolling features did not help on that window. On November 14 the work was on `week-2-work` with no PR; the two earlier-window results were not in the shared repo.

## Andrew — close the forecast comparison and build the static benchmark

- [ ] Open a PR from `week-2-work` into `main`; ask Manish to reproduce the original-window table. Fill in the actual Python version and commit in the submission note.
- [ ] Once Manish shares the earlier results, summarize all three windows: where did rolling features lower RMSE, and did either ridge model beat zero? Recommend one forecast specification to carry forward. If the evidence is mixed, say so. Keep zero as the benchmark.
- [ ] On a separate branch, implement the **static** basket-variance estimate described below. Hand-check the calculation on a two-series example, including the covariance term. Give Manish the date column, series order, weights and date range so both outputs can be joined without guessing.

## Manish — finish the time-window check and build the online estimate

- [ ] If Earlier 1 and Earlier 2 are already complete locally, push your branch and link the table; no need to rerun from scratch. Otherwise reuse Andrew's feature switch and the [November 14 windows](BEFORE_NOVEMBER_14.md). Report both ridge variants and the three simple baselines on the same dates. Send Andrew the results before the forecast decision.
- [ ] Try Peter Cotton's [precise](https://github.com/microprediction/precise) in an isolated environment. Use one exponentially weighted covariance estimator with a fixed update rate of 0.05. Record the installed version, estimator name and reproduction command. First run a small synthetic stream and check that the covariance matrix has the expected shape and is symmetric.
- [ ] Run the **online** estimate on the same UCI basket and dates as Andrew. Test the timing: changing the returns at row *t* or *t−1* must not change the variance predicted for *t*. If library setup blocks you, share the exact error and a minimal reproduction; label the online result incomplete.

## Agree on this comparison before looking at scores

The forecast experiment predicts the SP **return**. This experiment estimates **basket variance**. Success on one question does not imply success on the other.

1. Use the nine published return columns in the order defined in `src/forecasting.py`. Give each weight 1/9. This is a diagnostic basket; the two ISE columns are distinct published series, not evidence of nine independent investments.
2. Score the **Original validation window only**: April 27–September 22, 2010 (103 rows). For its first row, initialize both estimators from the same training observations, starting February 3, 2009 and ending two observed rows before the first validation row. Use complete rows and document any exclusions.
3. Andrew computes the sample covariance once and holds it fixed. Manish feeds the initialization rows to the online estimator chronologically. For each validation row *t*, save both variance predictions as `wᵀΣw` using information through *t−2*. Only after saving that prediction may the online state ingest row *t−1* for the next step. Use source return units throughout; do not annualize.
4. Compare each estimate with the squared observed basket return, `(wᵀr_t)²`. This is a noisy proxy for variance that assumes a near-zero daily mean. Report each method's **mean absolute error** against that proxy on identical dates. A lower error on this sample is a finding to discuss, not a reason to tune the update rate.

Andrew can start the static benchmark while Manish finishes the earlier forecast windows. Neither task requires opening the final test period (September 23, 2010–February 22, 2011).

## What to bring

- [ ] A reviewable PR from each person, with tests and the command the other person used to reproduce one result.
- [ ] One short note at `docs/results/week2.md`: the forecast decision, a two-row static/online error table with sample counts, and one chart showing both risk estimates over the validation period. Identify one date or interval where the estimates differed and explain what the update rule did.
- [ ] Keep daily outputs in `outputs/week2/`. Include a date, both predicted variances and the squared basket return. Check that dates match, estimates are finite and variances are nonnegative within numerical tolerance.

If something is unfinished, name the missing result and blocker. Dashboard work and final-test scoring are outside this week's assignment.
