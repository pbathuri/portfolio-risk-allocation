# Feature engineering

Predict the published SP return for observation t using information ending at t−2. All transformations are in `src/forecasting.py`.

| Family | Definition | Reason / limitation |
|---|---|---|
| Nine return lags | Each published return series shifted by two observed rows | Avoid current-row and same-day international close relationships; observations are not calendar days |
| Four SP rolling statistics | Mean and sample standard deviation over 5 and 20 observations, ending at t−2 | Simple return/risk history; fixed windows, not selected using validation scores |
| Missingness flags | One flag per engineered input | Explicit absent information; no missing inputs in this actual development run |
| Imputation/scaling | Medians, means and scales fit on training only | All-missing training inputs dropped; no future fill |

Fixed warm-up is 21 rows: at t=21 the 20-observation window ending at t−2 covers rows 0–19. Remaining 515 observations split 309/103/103 into train/validation/withheld test.

Hand check: for SP values 0,1,2,..., at row 21 the lag is 19, the 20-row mean is 9.5 and sample standard deviation uses ddof=1. Changing rows 20 onward cannot alter row 21's predictors.

Do not create same-day cross-market features or select features against the final test. Future student ablation: compare lag-only inputs with lags plus rolling statistics on identical validation rows. Missingness flags are an engineering safeguard, not evidence of a useful signal here.
