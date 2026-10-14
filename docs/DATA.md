# Market-data acquisition

## Preferred: WRDS / CRSP
Each student needs their own authorized institutional access and the required CRSP subscription. WRDS is not an appropriate source for the basketball or TCGA projects. Install the optional client with `pip install -r requirements-wrds.txt`. Run `python scripts/wrds_schema.py` interactively; it lists accessible CRSP schemas/tables and lets you inspect a table before querying. Never put passwords in a notebook or GitHub.

CRSP has legacy and CIZ formats. Do not assume a table or column exists. After inspecting the entitled table and reading its return definition, use the WRDS web query or a reviewed parameterized SQL query to export monthly date, permanent identifier and **total return**. CIZ return handling differs from legacy; do not add a delisting adjustment to a field that already includes it. For a legacy extraction, document whether and how `(1+RET)*(1+DLRET)-1` is applicable. Review missing delisting returns with the mentor instead of assigning zero.

Save the raw extract outside Git. Use `scripts/normalize_wrds.py --input PATH --date DATE_COLUMN --asset PERMANENT_ID_COLUMN --ret TOTAL_RETURN_COLUMN` after preparing any format-specific adjustments. The adapter deliberately does not infer CRSP methodology. It records the raw-file hash and refuses nonnumeric return flags, duplicates and impossible values. Put table/version, filters, adjustment rules, access date, coverage and terms in DATA_REGISTER.csv.

Choose the universe using information available at the training start. A present-day list of successful stocks creates survivorship bias. A fixed illustrative universe may be used for allocation education if selection bias is clearly disclosed; it cannot support claims of a tradable historical strategy. Restrict to a complete common date window only after reporting excluded securities and dates. Avoid silently dropping assets that delisted during testing.

## Public fallback: French 10 Industry Portfolios
Run `python scripts/fetch_french.py`. This fetches the value-weighted monthly returns section from the official ZIP, converts percentages to decimals, records the hash and writes the canonical file. Verify the resulting date span and metadata before analysis. These are research equity-industry portfolios, not ETFs you can directly buy and not bonds/commodities/cash. With this fallback, title the dashboard “Equity Industry Allocation” and narrow claims accordingly. Do not imply WRDS was used.

## Canonical contract: data/raw/returns.csv
| Field | Contract |
|---|---|
| date | ISO month-end; one observation per month per asset |
| asset | Stable identifier, not a time-varying ticker alone |
| ret | Decimal simple total return, including distributions; ≥ −1 |

At least 120 months, six assets recommended. Default frozen dates: 2010–2018 training, 2019–2021 validation, 2022–2025 test. The loader permits earlier training data; filter to 2010 onward for the stated default. Change dates only before inspecting the test outcomes and document the reason. No forward-fill of prices across missing return periods and no missing returns replaced by zero.

Only synthetic data is in the starter. The live downloader and WRDS entitlements must be checked by the team. Source licenses determine whether raw data or derived exports can leave the institution; a private GitHub repo is not automatically an approved data store.
