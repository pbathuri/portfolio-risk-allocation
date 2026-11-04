# Sources and attribution

- [UCI Istanbul Stock Exchange](https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange), [DOI](https://doi.org/10.24432/C54P4J), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): selected data and reuse terms. Credit Oguz Akbilgic (2013); describe date normalization and derived features.
- [Official UCI metadata](https://archive.ics.uci.edu/api/dataset?id=247) and [CSV](https://archive.ics.uci.edu/static/public/247/data.csv): verified acquisition endpoints, no account required.
- [Peter Cotton](https://github.com/microprediction) and [precise](https://github.com/microprediction/precise): selected online covariance work; no claim of broad institutional adoption or endorsement.
- [Jane Street competition overview](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/overview): methodological motivation only. [Rules](https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/rules) restrict competition data use; that dataset is not part of this project.

Sources checked November 3, 2026. No specific LinkedIn post was supplied. `timemachines` and `skaters` are background reading, not required integrations. Source facts and experimental findings must be distinguished in the final report.

## Career context used to choose the scope

Reviewed November 3, 2026. This is a small sample of employer requirements and a broad occupational projection, not a survey of the quant hiring market.

| Evidence | Project implication |
|---|---|
| [Jane Street quantitative researcher](https://www.janestreet.com/join-jane-street/position/8573726002/) discusses experiment design, dataset generation, time series, feature engineering, Python and communication. | Make the hypothesis, data assumptions and reproducible comparisons the main deliverables. Linear models are a reasonable starting point. |
| [Citadel graduate quantitative research analyst](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/) asks for probability/statistics, research experience, translating algorithms into code and communication; the work also includes backtesting. | Show tested research code and interpretation. This project covers forecast evaluation; it does not claim execution-aware trading backtesting. |
| [BLS data-scientist outlook](https://www.bls.gov/ooh/math/data-scientists.htm) projects 35% employment growth over 2025–2035 and about 24,800 annual openings. | These are broad US data-science projections, not quant-specific vacancies or evidence that a particular project guarantees interviews. |

Our design judgment: a small study with defensible experiments, reliable code and a readable report is a better use of four weeks than a larger unvalidated demo. The role descriptions support those skills; they do not endorse this dataset or project. A stronger follow-on would test the selected method on new, licensed data rather than add model complexity to the same short sample.
