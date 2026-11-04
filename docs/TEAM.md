# Two-person working agreement

| Seat | Ownership | Reviewer | Name |
|---|---|---|---|
| A | Data contract, preprocessing, baseline and ridge model, evaluation report | B | Fill at kickoff |
| B | Static/online covariance monitor, dashboard exports, reproduction | A | Fill at kickoff |

Budget 6–8 hours per person per week for four weeks. Each authors one small PR weekly and reviews the other person's work. Swap reproduction responsibility in Week 4. Both explain the model, monitoring assumptions and portfolio-statistics exercise. The mentor handles scientific scope and acceptance decisions.

Use `week-N/short-topic` branches, one notebook owner per branch, and the existing PR template. Keep reusable code in `src/`. PRs include a reproduction command, test evidence and a limitation. Never approve your own PR. Record assistant use in [AI_LOG.csv](AI_LOG.csv), following [AGENT_POLICY.md](AGENT_POLICY.md).

Weekly meeting: 5 minutes blockers, 20 minutes two demos, 15 minutes evidence review, 15 minutes pair planning and 5 minutes assignments. Record named owners at kickoff. If blocked for 30 minutes, pair; after one day, escalate and use the documented fallback. HPC is conditional on access and must not block the CPU-first MVP.

See [ROADMAP.md](ROADMAP.md) and [BACKLOG.csv](BACKLOG.csv) for dates and acceptance gates. The archived five-seat plan is historical only.
