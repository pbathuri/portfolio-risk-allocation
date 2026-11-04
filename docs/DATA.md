# Data source, attribution and verified acquisition

Source: [ISTANBUL STOCK EXCHANGE, UCI dataset 247](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange). UCI lists it under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), permitting adaptation and sharing with attribution. Keep credit, the license link and a description of changes in derivative reports.

**Attribution:** Akbilgic, O. (2013). *ISTANBUL STOCK EXCHANGE* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C54P4J.

Official metadata: https://archive.ics.uci.edu/api/dataset?id=247

Official CSV: https://archive.ics.uci.edu/static/public/247/data.csv

## Acquisition

```bash
python scripts/fetch_data.py
python scripts/inspect_source.py
python scripts/prepare_forecasting.py
python scripts/run_forecasting.py --input data/processed/checkpoint.csv
```

No authentication, Kaggle, Parquet engine or new dependency is needed. The downloader validates the CSV before writing it. Preparation preserves all returns and observations, sorts dates and normalizes dates to ISO format. It writes source/output hashes and attribution beside the prepared CSV. The runner rejects a CSV whose hash no longer matches that manifest.

Observed download: 64,063 bytes, 536 observations, 10 columns, January 5, 2009–February 22, 2011. The catalog's start-date wording differs from the actual CSV; the manifest uses parsed file dates. There are two ISE headers; pandas names them `ISE` and `ISE.1`. We preserve both as distinct published series and do not guess their units or currency distinction. UCI's type label for SP is inconsistent with its continuous numeric observations; we validate the file's numerical values.

## Contract and interpretation

One unique date per row; columns `date, ISE, ISE.1, SP, DAX, FTSE, NIKKEI, BOVESPA, EU, EM`. Numeric published returns may be missing in future compatible inputs; infinity and duplicate dates fail. The current source has no missing numeric cells.

Target: published `SP` return at observation t. Predictors use returns at t−2 or earlier. Rows follow the source's Istanbul trading calendar; gaps and cross-market holidays exist. A two-observation lag reduces same-day close-alignment risk but is not verified point-in-time vendor availability. No execution-price or investability claim is made.

Keep raw files and row-level outputs local for repository hygiene. Permitted derivative reports can include aggregate metrics with the attribution above, license link and changes. No third-party credentials or private data are needed.

## Source selection

UCI provides a small, openly licensed dataset that each team member can download without an account. Jane Street's competition data has competition-specific use restrictions and is not used here.
