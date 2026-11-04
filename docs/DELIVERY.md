# Dashboard and resume evidence

First checkpoint: [BEFORE_SATURDAY.md](BEFORE_SATURDAY.md). Saturday requires the data/feature/baseline note, not the finished dashboard below.

## Three dashboard pages

1. **Forecast benchmark:** dataset identity, train/validation/test dates, zero/mean/persistence/ridge scores, daily error, selected series and sample counts. Mark test results unavailable until the final evaluation.
2. **Adaptive monitor:** static and online feature-correlation views, covariance drift, alert counts and retrospective prediction errors. Explain warm-up and historical replay. Include a labeled synthetic shift test to demonstrate mechanics without claiming it validates real-market detection.
3. **Research audit:** data permissions, frozen configuration, versions, missingness, runtime/memory, limitations and links to the run manifest/report. Keep the portfolio learning exercise in a separate view or notebook with its own data labels.

Controls select precomputed model/day/series views; they must not silently retune a model using the test set. Export CSVs at explicit grains with unique keys. Never sum R², volatility or correlation across dashboard rows. Show the actual source and date range in each view.

## Release gate

- Working loader, baselines, one fitted model and one real Cotton-library integration; the integration is not satisfied by merely citing a package.
- One frozen run manifest and a single documented reproduction command; exact dependency versions and machine captured after execution.
- Numerical and temporal-leakage checks pass; second student reproduces from a clean environment.
- Held-out results, uncertainty and a failure-case discussion appear in a 2–3 page research report.
- Dashboard totals reconcile with exported computations; five-minute peer demo completes the three intended tasks: compare models, inspect drift, trace provenance.
- Permitted aggregate exports only; no unapproved raw UCI data, credentials or sensitive notebook outputs in Git.
- Contribution record identifies each student's authored and reviewed work; assistant-use log is current.

Success does not require beating the baseline. A carefully explained failed hypothesis is credible research. Do not claim production readiness, profitable alpha, institutional adoption or affiliation with Jane Street/Peter Cotton.

## Resume wording after completion

“Co-developed a reproducible market-forecasting and online covariance-monitoring pipeline using UCI international-return data and Python; compared ridge regression with simple baselines using chronological validation and built an interactive dashboard of held-out errors and distribution shifts.”

Add measured dataset size, runtime and score differences only after verification. Never describe this as a Jane Street-data project. Each person should mention their own contribution and be able to explain the other half.
