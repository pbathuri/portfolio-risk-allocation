# Before Saturday, November 14

**Due:** November 14, 2026, before the 10 a.m. meeting (America/Indiana/Indianapolis).

This week we will test one question: **do the rolling SP statistics improve ridge forecasts beyond lagged returns, and does the answer change across periods?** Budget 4–6 hours each, including review. Keep the final 103 observations unscored.

## Start together

- Pull the latest repo and reproduce the [recorded baseline](REAL_DATA_VERIFICATION.md).
- If setup is unfinished, complete the [first checklist](BEFORE_SATURDAY.md) by Monday, November 9.
- Agree who owns A and B. Use separate branches and avoid editing the same notebook simultaneously.
- Record the hypothesis and the fixed date windows below in your PR before inspecting new scores.

## Person A — compare the two feature sets

1. Read `engineer()` and `checkpoint()` in `src/forecasting.py`.
2. Add a way to choose between these two inputs while leaving the existing full-feature run as the default:
   - **Lag-only:** nine columns ending in `_lag2` for the published return series, plus their nine missingness flags.
   - **Lags + rolling:** those columns plus the four SP mean/standard-deviation features and their four missingness flags (the current 26-column feature set).
3. Use the **Original** window below. Keep the same rows, target, two-observation delay, equal weights, ridge alpha=1 and training-only preprocessing for both variants. Keep the 21-row warm-up even though lag-only needs less history; otherwise the comparison changes two things at once.
4. Report RMSE and zero-mean R² for both ridge variants and the zero, training-mean and persistence baselines. Record all results, including negative scores.
5. Add a test that confirms the selected columns are correct and that the existing default behavior is preserved. Run the full test suite.

**Bring:** one small PR, the comparison table, the reproduction command and a short answer to whether rolling features helped on this window.

## Person B — check stability over time

1. While A implements the feature choice, check the date windows and lag calculations against the current pipeline.
2. Add support for the two **Earlier** windows below. Reuse A's feature-selection code once available; do not create a second implementation.
3. Refit imputation, scaling and ridge from scratch on each window's training observations. Fit the training-mean baseline separately too. Score only that window's validation observations.
4. Run both feature variants and all three baselines on each earlier window. Keep alpha=1 and the same feature definitions. Do not adjust dates after seeing results.
5. Add a test for non-overlapping, ordered windows and rejection of any evaluation period entering the reserved test range. Check that changing later observations cannot change earlier predictions.

**Bring:** one PR, the two period-level comparison tables and a short explanation of whether A's conclusion is consistent across time. A small labeled chart is optional.

## Fixed windows

All rows refer to the sorted, prepared UCI data **after removing the first 21 warm-up rows**. Calculate causal features using the full preceding history before selecting the fitting/scoring rows; do not reset rolling windows at validation boundaries.

| Window | Training dates | Train rows | Validation dates | Validation rows |
|---|---|---:|---|---:|
| Earlier 1 | 2009-02-03–2009-09-09 | 154 | 2009-09-10–2010-01-05 | 77 |
| Earlier 2 | 2009-02-03–2010-01-05 | 231 | 2010-01-06–2010-04-26 | 78 |
| Original | 2009-02-03–2010-04-26 | 309 | 2010-04-27–2010-09-22 | 103 |

For zero-based Python slicing of the post-warm-up rows, these are `[:154] / [154:231]`, `[:231] / [231:309]` and `[:309] / [309:412]` respectively.

**Reserved test:** September 23, 2010–February 22, 2011. Do not score it, plot its target values or use it to choose features. Earlier validation observations may enter a later training window once they are in the past. These windows share training history, so their scores are not independent experiments or proof of statistical significance.

## Save and review the evidence

Use one result table with columns:

`window, model, feature_set, train_start, train_end, validation_start, validation_end, train_rows, validation_rows, rmse, zero_mean_r2`

For the three simple baselines, use `feature_set=not_applicable`; do not duplicate their rows for each ridge variant. Lower RMSE is better. Define the feature effect as `RMSE(lags + rolling) - RMSE(lag-only)`; a negative difference favors rolling features.

Keep generated files under `outputs/week1/`. Commit a short summary with the table, source attribution, commands, commit/version information and limitations to `docs/results/week1.md`. Coordinate one owner for that shared summary. Cite the UCI dataset and CC BY 4.0 license from [DATA.md](DATA.md).

By Friday evening, each person should review the other's PR and reproduce one result. Report blockers early with the command and error. If time runs short, prioritize the original-window comparison and one earlier window; explicitly mark the second window unfinished.

## What to bring to the meeting

- [ ] Both feature sets evaluated on the original window.
- [ ] Both feature sets and baselines evaluated on the two earlier windows, or an explicit unfinished item.
- [ ] Tests pass; the default starter's scores are unchanged.
- [ ] Each person has reproduced one result from the other's work.
- [ ] A two-minute explanation each: what changed, what happened, and what remains uncertain.

Do not add model families or tune alpha this week. We will review the evidence on Saturday and choose the forecasting specification before starting the `precise` covariance comparison. No finished dashboard is due.

The starter currently runs one fixed split with the full feature set. Feature selection and alternate-window support are this week's implementation tasks, not existing CLI options.
