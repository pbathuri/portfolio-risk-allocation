# Learn the method, then build it

Work through the lesson that matches your next assignment. Each lesson follows the same sequence: read a small part of the project, work a toy example, implement your task, then explain the result to your partner. The examples below use made-up values and never open the final test data.

The weekly checklists still define the deadlines and deliverables. This guide helps you understand and complete them; it does not replace the experiments with prewritten answers. Plan for 20–30 minutes of reading and practice before each implementation task, within the existing weekly workload.

## 1. Follow one row through the pipeline

**Goal:** explain where an observation comes from and which values may be used to predict it.

Read [DATA.md](DATA.md), then follow these functions in order: `validate()`, `engineer()`, `split_dates()` and `checkpoint()` in `src/forecasting.py`. Run the four notebooks in order with `jupyter lab`; their cells use synthetic observations. Use the README commands separately for the real-data checkpoint.

A row is one date on the source's trading calendar. The prediction target is that row's SP return. A two-observation lag means using the value two rows earlier, not necessarily two calendar days earlier.

```python
import pandas as pd
returns = pd.Series([10., 20., 30., 40., 50., 60.])
print(pd.DataFrame({
    'value': returns,
    'lag2': returns.shift(2),
    'mean3_lag2': returns.shift(2).rolling(3).mean(),
}))
assert returns.shift(2).rolling(3).mean().iloc[4] == 20.
```

**Check your understanding:** at row 4, the rolling feature averages rows 0, 1 and 2. Changing row 3 or 4 cannot change it. Early NaNs mean there is not enough history; filling them with future values would leak information.

**Do:** reproduce the data manifest and trace one synthetic row through the feature calculation. Keep the same 21-row warm-up for both feature sets in the real comparison.

**Explain to your partner:** why do we shift before rolling, and why would a lag-only model still discard 21 rows? If the two variants use different observations, their score difference no longer isolates the feature choice.

## 2. Compare models fairly

**Goal:** understand what a baseline measures and why one split is not enough.

Read the [scikit-learn lagged-feature example](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html), concentrating on lag construction and chronological evaluation. Its hourly data, model and split parameters are different from ours; use the dates in the [November 14 assignment](BEFORE_NOVEMBER_14.md).

```python
import numpy as np
y = np.array([1., -1., 2.])
prediction = np.array([0., 0., 1.])
sse = np.sum((y - prediction) ** 2)
rmse = np.sqrt(sse / len(y))
r2_zero_mean = 1 - sse / np.sum(y ** 2)
assert np.isclose(rmse, 1.)
assert np.isclose(r2_zero_mean, .5)
print(rmse, r2_zero_mean)
```

**Check your understanding:** the zero predictor has zero-mean R² of zero when the denominator is nonzero. A negative score means worse squared error than zero. Do not substitute centered R² or average the R² values across windows.

**Andrew's task:** compare the 18 lag-only inputs with the full 26-input version, holding alpha, rows and preprocessing fixed. Read the feature catalog to check which columns belong to each set.

**Manish's task:** reproduce that comparison on Earlier 1 and Earlier 2. Fit imputation, scaling, the model and the mean baseline anew on each window's training rows. Create features from preceding history before slicing; do not reset a rolling window at the validation boundary.

**Verify:** make a copy of synthetic data and change values strictly after a window. Earlier predictions should not change. Report RMSE and zero-mean R² for every variant, including failures.

**Discuss:** if rolling features help one period but hurt another, what conclusion can you justify? The windows share history; three scores are not three independent experiments.

## 3. Turn covariance into basket risk

**Goal:** distinguish an individual series' variance from the variance of a basket.

Covariance measures how two return series move together around their means. For weights `w` and covariance matrix `Sigma`, basket variance is `w.T @ Sigma @ w`. It includes cross-series terms, not just each series' variance.

```python
import numpy as np
sigma = np.array([[0.0004, 0.0001], [0.0001, 0.0009]])
w = np.array([0.5, 0.5])
variance = w @ sigma @ w
hand = 0.5**2 * 0.0004 + 0.5**2 * 0.0009 + 2*0.5*0.5*0.0001
assert np.isclose(variance, 0.000375)
assert np.isclose(variance, hand)
print('variance:', variance, 'standard deviation:', np.sqrt(variance))
```

**Check your understanding:** variance is in squared-return units; its square root is standard deviation. Neither is an observed loss or a forecast of profit. Negative covariance can reduce basket variance even when both individual variances are positive.

**Andrew's task:** compute the sample covariance with `ddof=1` from the agreed initialization rows, then hold it fixed over validation. Use `rowvar=False` when calling `numpy.cov` on a matrix whose rows are dates and columns are series. Confirm the result is 9 by 9.

**Verify:** compare a two-series calculation with the hand result, then check matrix symmetry, finite entries, weights summing to one and nonnegative basket variance within tolerance. Keep the series order explicit; swapping columns without swapping weights can change the meaning.

**Small DSC exercise:** on training data only, compare equal, inverse-volatility and long-only minimum-variance weights as described in [METHODS.md](METHODS.md). Explain concentration and covariance sensitivity. Keep this separate from the fixed equal-weight covariance benchmark; do not change its weights to get a better score.

## 4. Update risk without reading ahead

**Goal:** understand the difference between a fixed estimate and an estimate that learns as observations arrive.

Read the estimator interface and examples in [precise](https://github.com/microprediction/precise). Use its installed version's documentation; record the estimator name and what its rate parameter means. Our experiment fixes the update rate at 0.05 rather than selecting a rate from validation scores.

An exponentially weighted estimator gives newer observations more influence. A larger update weight generally reacts faster but can make estimates noisier. The library must update its location and covariance consistently; replacing only a covariance matrix with an arbitrary weighted average is not automatically the same estimator.

Before coding, trace this toy timeline on paper:

| Prediction being saved | Latest row allowed in the covariance state | Row ingested only after saving |
|---|---|---|
| t = 5 | 3 | 4 |
| t = 6 | 4 | 5 |
| t = 7 | 5 | 6 |

The initialization history already ends at row 3 for the first prediction in this example. Do not ingest it a second time. Static covariance never updates.

**Manish's task:** build a small synthetic stream using the actual library, then apply the same loop to the agreed real dates. Reuse Andrew's input preparation, column order and weights.

**Verify:** change rows t−1 and t in a copy of the stream; the estimate saved for t must be unchanged. Count updates and assert that each eligible row is ingested exactly once. A reversed update/predict order can produce plausible-looking results with look-ahead leakage.

**Both:** join the daily results by date with a one-to-one check. Compare each variance estimate with the same squared basket-return proxy. Explain why that proxy is noisy and why a lower MAE does not establish better return forecasting.

## 5. Make a chart someone else can check

**Goal:** communicate results without hiding their source or uncertainty.

Read the [December 5 checklist](BEFORE_DECEMBER_5.md). Start with the result tables already produced; do not put training code behind dashboard controls.

**Manish's task:** build the forecast, risk and provenance views. First show a table and one working chart, then add filters. Label dates, sample counts, units, model and split. Mark final results pending until the freeze is approved.

**Andrew's task:** draft each finding as three sentences: what was compared, what the numbers show, and what they do not establish. Link the source table and method. A claim such as “the online method is better” needs the metric, period and limitations.

**Verify together:** pick one row from a saved table, calculate its displayed value independently and locate it in the dashboard. Repeat for three values. A filter must change the selected evidence, not silently change the experiment.

**Explain:** why is a correlation heatmap not evidence that a return predictor works? Which findings are training estimates, development choices or final evaluations?

## 6. Freeze, evaluate and explain uncertainty

**Goal:** separate choosing a method from assessing the method you chose.

Read the freeze requirements in the [December 5 checklist](BEFORE_DECEMBER_5.md), then the [December 12 checklist](BEFORE_DECEMBER_12.md). Practice the final-evaluation path on synthetic/development data only until the maintainer approves the freeze.

For the forecast comparison define each paired loss difference as selected-model squared error minus zero-baseline squared error. A negative mean favors the model. For covariance use online absolute error minus static absolute error. Pairing means both methods are assessed on the same observations.

For the moving-block bootstrap, practice these steps on a made-up 12-value loss-difference array with block length 3:

1. Enumerate consecutive blocks starting at indices 0 through 9.
2. Sample block starts with replacement, concatenate four blocks, and calculate the mean of the resulting 12 values.
3. Repeat with a fixed seed. Inspect which observations recur and whether order is preserved inside each block.
4. Explain why independently resampling the two methods destroys the paired comparison.

Then implement the frozen project settings: block length 5, 200 resamples, seed 42 and a percentile 95% interval, truncating each replicate to the original length. The interval describes uncertainty under this resampling procedure; it cannot fix a short or unrepresentative dataset. An interval containing zero does not prove the methods equivalent.

**Andrew:** implement and test the evaluator and loss calculation; document the freeze before running final scoring. **Manish:** inspect the boundaries, reproduce the approved run, and reconcile the dashboard.

**Final explanation:** describe one result that changed your expectation, one assumption that remains uncertain and one way you checked the code. A negative finding with sound evidence is a valid conclusion.

## When stuck

Write down the expected input/output, the smallest example that fails and what you already tried. Ask your partner to check the reasoning before changing models or parameters. If using a coding assistant, ask for an explanation or a small test, inspect the proposed change, and be prepared to explain it yourself. Put findings and verification in the PR; keep chat transcripts out of the repo.
