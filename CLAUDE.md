# ODCA-DES Paper Project

## What This Is
From PhD dissertation: "Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata", targeting Transportation Research Part B.

## Project Layout
- `paper/` — LaTeX manuscript (`paper-odca-des.tex`)
- `code/` — simulation codebase (Python, SimPy)
  - `code/odca/` — core framework (infrastructure, entities, models, analysis)
  - `code/config.py` — vehicle parameters, cell length, defaults
  - `code/run_experiments.py` — S1-S4 scenario experiments
  - `code/run_demand_sweep.py` — density-init FD sweeps (single + multi-lane)
  - `code/run_bottleneck.py` — lane closure bottleneck experiments
  - `code/run_incident.py` — temporary incident scenario (baseline + incident runs)
  - `code/diagnose_fd_capacity.py` — ring road FD capacity diagnosis
  - `code/generate_figures.py` — all paper figures
  - `code/output/` — results JSON, figures PDF
- `figures/`, `tables/` — generated artifacts consumed by the paper
- `review/` — review artifacts
  - `review/external/` — journal reviewer reports, advisor comments, response letters
  - `review/self/` — `manuscript-critic` outputs and author responses to them

## Key Architecture
- **ODCA-DES**: cell-based spatial structure + SimPy discrete-event timing
- **Resource protocol**: PriorityResource(capacity=1) per cell; `_delayed_release` after tau enforces minimum headway
- **Car-following**: Newell model with fractional sub-cell positioning (`newell.py`)
- **Vehicle types**: HDV (per-vehicle driver SimPy process) and AV (central controller)
- **RNG**: per-source streams via numpy SeedSequence (not per-vehicle)
- **FD measurement**: Edie's generalized definitions from T(x,n) trajectory data

## Conventions
- Python environment: `uv` (venv in `code/.venv/`)
- Run scripts from `code/` directory
- numpy RNG only — never `import random`
- Units: cells/s for speed, cells for distance, seconds for time
- Cell length: 7.5m (`CELL_LENGTH_M` in config.py)

## Key Parameters (HDV defaults)
- tau=1.5s, d=1.0 cell, v_max=5.2 cells/s (140 km/h)
- Theoretical capacity: 2127 veh/h (Newell triangular FD)
- Heterogeneity: tau~LogNormal, action_interval~LogNormal, slowdown_prob~Normal
