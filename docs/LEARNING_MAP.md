# DSC learning goals

The original DSC goals are retained as exercises within this project; a separate allocation application is no longer required.

| Goal | Evidence |
|---|---|
| Acquire and clean financial data | Download the official CSV, verify its schema and hashes, explain the source-date discrepancy and attribution. |
| Understand portfolio statistics | Hand-check two-asset variance and covariance; compare a static training covariance with an online estimate. |
| Compare allocation methods | Use the same training covariance for equal-weight, inverse-volatility and long-only minimum-variance weights; explain concentration and estimation sensitivity. See METHODS.md. |
| Evaluate and visualize risk-return trade-offs | Compare forecast errors separately from basket-risk estimates; explain why neither establishes trading profit. |
| Communicate decision support responsibly | Reproduce another person's run, write a short report, and defend the assumptions and negative results. |

Both students write and review code. Each should explain a lag calculation, a baseline metric and a covariance example without relying on the notebook output alone. Cluster execution is outside this CPU-sized project; it is not a claimed learning outcome.
