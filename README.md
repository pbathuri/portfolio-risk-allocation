# DSC Fintech — Adaptive Market Forecasting & Risk Monitor

**Selected direction:** combine the equally supported experimental and research options: evaluate a simple predictive model on Jane Street's public competition data and use Peter Cotton's `precise` library to study changing feature covariance. Two students, four weeks, one reproducible analytical dashboard.

**Research question:** Does a simple market-response predictor remain useful across time, and can an online covariance monitor expose changes in its inputs and error profile?

## Start here

- [Project scope and verified sources](docs/PROJECT_PROPOSAL.md)
- [Saturday November 7, 10 a.m. kickoff](docs/KICKOFF.md)
- [Four-week roadmap](docs/ROADMAP.md), [two-person ownership](docs/TEAM.md), and [eight-task backlog](docs/BACKLOG.csv)
- [DSC learning goals](docs/LEARNING_MAP.md) and [experiment contract](docs/EXPERIMENT.md)
- [Dashboard, research report and resume evidence](docs/DELIVERY.md)

## What works today versus what the team will build

The existing runnable code and notebooks implement the original portfolio-risk learning exercises using synthetic fixtures or separately acquired return data. The Jane Street loader, predictive benchmark, `precise` integration and new dashboard are **planned work**, not implemented results. Follow the four-week roadmap; the numbered Week 1–5 notebooks remain reference exercises, not the current schedule.

Preserve those exercises to learn portfolio variance and allocation comparison. Never treat anonymized competition responders as tradable returns or translate their scores into profit. A well-supported negative finding meets the research objective.

## First run (Python 3.11)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_demo.py
jupyter lab
```
Windows PowerShell activation: `.venv\Scripts\Activate.ps1`. On macOS, Tableau is a practical choice; Power BI Desktop requires a supported Windows environment.

Open `notebooks/00_kickoff.ipynb` for the existing starter. Use later notebooks as the portfolio learning exercises selected in the new roadmap. All Python notebook kernels use this environment. `PROJECT_MODE=demo` is the default and uses generated synthetic fixtures. Real mode reads files described in `docs/DATA.md`. To launch real mode on macOS/Linux:
```bash
PROJECT_MODE=real jupyter lab
```
PowerShell: `$env:PROJECT_MODE="real"; jupyter lab`. Never combine real and demo exports; each has its own output directory.

## Work agreement
Read `docs/ROADMAP.md` for milestones, `docs/TEAM.md` for owners and reviews, and `docs/AGENT_POLICY.md` before using a coding assistant. Start with `docs/KICKOFF.md` at the first Zoom call. The executive mentor owns scientific scope and acceptance decisions; students own implementation and explanations. The previous five-week planning documents are retained under `docs/archive/five-week-plan/` for provenance.

## Files you will use
- `notebooks/`: six working notebooks, with prompts for the team's decisions.
- `src/project.py`: tested baseline calculations; refactor small pieces here rather than copying cells.
- `docs/DATA.md`, `docs/METHODS.md`: contracts, acquisition and statistical choices.
- `docs/DELIVERY.md`: figures, dashboard or scientific presentation, and acceptance checklist.
- `hpc/`: parameterized Slurm examples; allocation and environment are configured locally.
- `tests/`: numerical and data-contract checks. Run `python -m unittest discover -s tests`.

Dependencies are bounded in `requirements.txt`, not claimed as a cross-platform lock. After the team confirms its environment, save `python -m pip freeze > environment.lock.txt`, record OS/Python, and use that file for reruns. Do not put credentials or raw licensed data in Git.
