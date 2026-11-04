# Feature engineering checkpoint

All transformations are in `src/forecasting.py`; read them before changing them.

| Feature family | Implemented definition | Why / limitation |
|---|---|---|
| Raw inputs | `feature_00` through `feature_09` at the current row | Small fixed initial set; anonymized semantics; not selected for predictive importance |
| Missingness flags | 1 when each raw input is NaN, otherwise 0 | Explicit missingness signal; missingness may shift over time |
| Three lags | Previous observed value of features 00, 01 and 02 within the same symbol and date | Causal feature-only memory; missing at each day's first observation; elapsed time need not be constant |
| Imputation | Median computed from training rows only | No future fill; all-missing training columns are dropped and cataloged |
| Scaling | Mean and scale fit on imputed training rows only | Validation and test never fit preprocessing |

No responder column, target lag, future value or random train/test split is allowed. The lag is **not** yesterday's label or the immediately preceding global row. Sorting uses date, time and symbol; duplicate keys fail.

For one symbol with feature values `2, NaN, 5` at successive times within a day, the lag is `NaN, 2, NaN`; missingness flags are `0, 1, 0`. Imputation is performed later using training-only medians. At the next day the lag resets to NaN. Explain this example at Saturday's meeting.

The default ridge uses alpha=1, fixed for the checkpoint. Proposed follow-up: compare raw-only versus raw+missingness versus raw+missingness+lags on the same validation rows. Freeze the hypothesis before running it, record every variant and do not use the final test to select features.
