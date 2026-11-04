# Four weeks, two owners

Preparation: complete [BEFORE_SATURDAY.md](BEFORE_SATURDAY.md) before the kickoff; count its 2–3 hours per person toward Week 1.

Kickoff: Saturday November 7, 2026, 10:00–11:00 a.m., America/Indiana/Indianapolis (assumed from this week's meeting request). Final review: Saturday December 5, 10:00 a.m., after four build weeks. Account for Thanksgiving availability at kickoff.

A owns data and predictive modeling; B owns covariance monitoring and dashboard exports. Each reviews the other's PR. Both explain the methods and rerun the other's work. Fill in names at kickoff; the mentor handles scope decisions. Each student authors at least one small PR per week. Preserve the repository's assistant-use log and peer-review requirements.

| Week / review | A delivers | B delivers | Acceptance gate |
|---|---|---|---|
| 1: Nov 7–13 / Nov 14 | Review prepared CSV; resolve schema/timing and run first feature ablation | Review starter splits/tests; review lag/window boundaries and monitor experiment | Confirmed real-data contract or fallback decision; reproduction and causal split evidence |
| 2: Nov 14–20 / Nov 21 | Zero/mean/persistence/ridge comparisons on validation | `precise` smoke test and static-vs-online covariance comparison | Reproducible validation table; causal update test; portfolio-statistics hand exercise |
| 3: Nov 21–27 / Nov 28 | Error breakdowns, small tuning log, frozen model | Three dashboard pages linked to real computed outputs | Peer walkthrough, frozen configuration, limitations draft; test remains unscored |
| 4: Nov 28–Dec 4 / Dec 5 | One final test evaluation, paired uncertainty analysis | Clean-environment reproduction, dashboard and demonstration | Both reproduce; report and run manifest agree; no invented results |

Plan Week 3 as a lighter holiday week: no new model families or infrastructure. If work slips, reduce dashboard polish and retain the benchmark, monitor, leakage tests and report.


See [learning goals](LEARNING_MAP.md), [kickoff](KICKOFF.md), and [task backlog](BACKLOG.csv).
