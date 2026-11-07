# Four-week plan

Current assignment: [complete before November 14](BEFORE_NOVEMBER_14.md).

**Team:** two people, 6–8 hours each per week. Preparation for November 7 counts toward Week 1. Allow for Thanksgiving during Week 3.

A owns acquisition, feature experiments and the prediction report. B owns covariance comparisons, output checks and the dashboard. Each reviews the other's changes; both must reproduce the final run.

| Week | A | B | Evidence for the review |
|---|---|---|---|
| Nov 7–13 | Reproduce the baseline; compare lag-only with lag-plus-rolling features | Check lag boundaries and repeat the comparison on expanding training windows within development data | One experiment table with all variants, dates and errors |
| Nov 14–20 | Explain period-by-period errors; select the forecasting specification | Integrate one `precise` covariance estimator and compare it with static covariance | Versioned monitor run, score-before-update test and covariance comparison |
| Nov 21–27 | Draft findings and limitations; freeze model choices | Build dashboard from saved outputs; reconcile its values with the report | Working views and a written freeze before final scoring |
| Nov 28–Dec 4 | Evaluate the final period once; add paired block-bootstrap uncertainty | Reproduce from a clean environment and finish the demonstration | Reproducible report, dashboard and contribution record |

Reviews: November 7, 14, 21 and 28 at 10 a.m.; final review December 5 at 10 a.m., America/Indiana/Indianapolis. Use the first meeting for a two-minute walkthrough from each person, questions about the data, and agreement on the first experiment.

## Research choices

| Perspective | Consequence for this project |
|---|---|
| Statistical | Keep zero and persistence baselines. Report failed hypotheses. Use several earlier time windows to check stability; never recycle the reserved test set. |
| Financial | The source calendar and market-close alignment are imperfect. Delay predictors, discuss uncertainty, and avoid converting forecast scores into P&L. |
| Engineering | Keep the download small and the pipeline reproducible. Tests, hashes, consistent outputs and an independent rerun matter more here than cloud infrastructure. |
| Usability | A reviewer should be able to compare models, inspect changing correlations and trace a number to its run. Build those three views before polishing the interface. |
| Career preparation | Demonstrate the reasoning behind a model, not just that a library ran. Keep examples of code review, a failed experiment and a corrected data assumption. See SOURCES.md for the employer evidence behind these choices. |

## Scope limits

Use one feature ablation and one online covariance estimator. Keep a CPU workflow and the existing dependencies until a new requirement is justified. Deep networks, LLM explanations, live trading and deployment are outside the four-week scope. SQL is useful in broader analytics work, but this small single-table study does not justify adding a database solely for a résumé keyword.

The dataset is adequate for learning and a modest research demonstration. A later extension should use a larger, independently licensed dataset and a new untouched period; four weeks of work on 536 rows cannot establish general market predictability.

## Finished work

Deliver a 2–3 page report, a five-minute demonstration and the code to reproduce both. The dashboard needs three views: baseline/error comparison, static/online covariance, and data/run provenance. Display dates, sample counts and whether a value is training, validation or final-test evidence.

Before release, check that tests pass, another person can reproduce the outputs, every figure agrees with the saved computations, data attribution is present, and each contribution is recorded. A negative result is acceptable if the question and evidence are clear.
