# Completion plan — December 12

**Final review: Saturday, December 12, 2026, at 10 a.m. Eastern.** This replaces the original December 5 completion date. Plan for 6–8 hours per person in each full week, with a lighter Thanksgiving week. Finish the pending experiments before adding presentation work.

Current assignment: [November 28 checklist](BEFORE_NOVEMBER_28.md). Next: [December 5](BEFORE_DECEMBER_5.md) and [December 12](BEFORE_DECEMBER_12.md).

## Repository audit — November 23

| Item | Evidence in the shared repo | Remaining work |
|---|---|---|
| Data and starter | UCI download-to-baseline results recorded; tests and notebook workflow on main | Students independently reproduce the selected runs |
| Feature ablation | Andrew's [PR #1](https://github.com/pbathuri/portfolio-risk-allocation/pull/1), head 477ac2a, has original-window results and passing CI | Complete PR description/environment details, peer review and maintainer merge |
| Earlier windows | Submission note still has a placeholder; no separate results branch found | Manish publishes both windows and reproduction evidence |
| Covariance comparison | Method specified, but no implementation or result table found on shared branches | Static and precise estimators, timing tests and aligned daily outputs |
| Dashboard and final report | Requirements only | Build from verified outputs and review figures |
| Final test | Starter leaves 103 observations unscored | Review freeze first; implement and run final evaluation afterward |

This is a submission/readiness audit, not approval of the unmerged code. Work kept locally may exist; push it for review. Green CI does not establish scientific correctness.

## Milestones and ownership

| Due | Andrew | Manish | Completion gate |
|---|---|---|---|
| **Nov 28, 10 a.m.** | Finish PR #1; consolidate forecast table; implement static covariance | Review PR #1; finish earlier windows; implement precise online covariance | 15-row forecast table, two-row covariance error table, 103 aligned daily covariance rows, tests and peer reproduction |
| **Dec 5, 10 a.m.** | Write report draft and proposed freeze; implement/test final-evaluation path using synthetic/development data only | Build dashboard from development outputs; review timing and reproduce computations | Dashboard works, report draft exists, method freeze approved by maintainer; final test still unscored |
| **Dec 8** | Run frozen final evaluation once and save manifests/metrics | Independently reproduce frozen outputs and check dashboard reconciliation | Traceable final results and discrepancies resolved without tuning to test outcomes |
| **Dec 10** | Finish findings, uncertainty and limitations | Complete clean-environment instructions and demo rehearsal | Release candidate: report, dashboard, reproduction commands and contribution record |
| **Dec 12, 10 a.m.** | Present forecast findings | Present risk comparison and reproduce one result | Five-minute joint demo, 2–3 page report, reviewed code, green CI and final release record |

Use one primary owner per shared result note and reciprocal PR review. The maintainer approves merges and the final method freeze. Record a brief description of any assisted work and the checks you performed in the PR; do not commit conversations.

## If a gate slips

Share blockers by November 25 and resolve integration issues by December 2. Cut extra model experiments, chart polish and hosting first. Keep the single feature comparison, one actual precise integration, both covariance benchmarks, leakage checks and reproducible evidence. The dashboard can run locally; no cloud deployment is required.

Do not silently turn an incomplete method into a completed result. If the December 5 freeze gate fails, keep final scoring locked and agree a revised release scope/date. A methods prototype can still be presented, explicitly labeled as such.

## Research choices

| Perspective | Consequence for this project |
|---|---|
| Statistical | Keep zero and persistence baselines. Report failed hypotheses. Use several earlier time windows to check stability; never recycle the reserved test set. |
| Financial | The source calendar and market-close alignment are imperfect. Delay predictors, discuss uncertainty, and avoid converting forecast scores into P&L. |
| Engineering | Keep the download small and the pipeline reproducible. Tests, hashes, consistent outputs and an independent rerun matter more here than cloud infrastructure. |
| Usability | A reviewer should be able to compare models, inspect changing correlations and trace a number to its run. Build those three views before polishing the interface. |
| Career preparation | Demonstrate the reasoning behind a model, not just that a library ran. Keep examples of code review, a failed experiment and a corrected data assumption. See SOURCES.md for the employer evidence behind these choices. |

## Scope limits

Use one feature ablation and one online covariance estimator. Keep a CPU workflow and the existing dependencies until a new requirement is justified. Deep networks, LLM explanations, live trading and deployment are outside the remaining project scope. SQL is useful in broader analytics work, but this small single-table study does not justify adding a database solely for a résumé keyword.

The dataset is adequate for learning and a modest research demonstration. A later extension should use a larger, independently licensed dataset and a new untouched period; a short study on 536 rows cannot establish general market predictability.

## Finished work

Deliver a 2–3 page report, a five-minute demonstration and the code to reproduce both. The dashboard needs three views: baseline/error comparison, static/online covariance, and data/run provenance. Display dates, sample counts and whether a value is training, validation or final-test evidence.

Before release, check that tests pass, another person can reproduce the outputs, every figure agrees with the saved computations, data attribution is present, and each contribution is recorded. A negative result is acceptable if the question and evidence are clear.
