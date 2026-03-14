# ODCA-DES Paper Project

## What This Is
Paper 2 of 3 from Kerem Demirtas's PhD dissertation at Arizona State University.
**Title:** "Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata"
**Target journal:** Transportation Research Part B

## Authors
- Kerem Demirtas (School of Computing and Augmented Intelligence, ASU)
- Pitu Mirchandani (School of Computing and Augmented Intelligence, ASU)
- Xuesong Zhou (School of Sustainable Engineering and the Built Environment, ASU)

## 3 Planned Papers (from dissertation)
1. Probabilistic Lane Changing Models based on Logistic Functions → *TR Part B*
2. **Discrete Event Traffic Simulation Framework using ODCA → *TR Part B* ← THIS PAPER**
3. Analysis of AV Platooning in Mixed Traffic on Freeways → *IEEE T-ITS*

## Repository Layout
```
paper-odca-des/
├── paper/              # LaTeX manuscript (main.tex, references.bib, elsarticle)
├── figures/            # All generated figure PDFs (output of code/)
├── tables/             # (reserved for generated table artifacts)
├── code/               # Python simulation codebase
│   ├── odca/           # Core framework
│   │   ├── infrastructure/   # Cell, Lane, Freeway (spatial resources)
│   │   ├── entity/           # Vehicle, HDV, AV, AV Controller
│   │   ├── models/           # Car-following (Newell), lane-changing (MLC/DLC)
│   │   ├── simulation/       # DES engine, vehicle generator
│   │   └── analysis/         # Metrics, Edie's FD measurement
│   ├── config.py             # Vehicle params, cell length, scenario configs
│   ├── generate_figures.py   # Main figure generation (FD, throughput, bottleneck, incident)
│   ├── generate_paper_figures.py  # Additional figures (TSD, speed profile, event density)
│   ├── run_experiments.py    # S1-S4 mixed traffic scenarios
│   ├── run_bottleneck.py     # Lane closure bottleneck experiments
│   ├── run_incident.py       # Dynamic incident scenario
│   ├── run_demand_sweep.py   # Density-init FD sweeps
│   ├── diagnose_fd_capacity.py   # Ring road FD capacity diagnosis
│   └── output/               # Raw simulation data (JSON, gitignored)
├── CONTEXT.md          # This file
├── CLAUDE.md           # AI assistant instructions
├── HANDOFF.md          # Session state and next steps
└── .gitignore
```

## Key Technical Concepts
- **ODCA-DES**: Cell-based spatial structure + SimPy discrete-event timing
- **Resource protocol**: PriorityResource(capacity=1) per cell; delayed release after τ enforces minimum headway
- **Car-following**: Newell model with fractional sub-cell positioning
- **Vehicle types**: HDV (per-vehicle driver SimPy process) and AV (central controller at 10 Hz)
- **FD measurement**: Edie's generalized definitions from T(x,n) trajectory data

## Conventions
- Python environment: `uv` (venv in `code/.venv/`)
- Run scripts from `code/` directory
- numpy RNG only — never `import random`
- Units: cells/s for speed, cells for distance, seconds for time
- Cell length: 7.5m (`CELL_LENGTH_M` in config.py)
- Figures output to `figures/` (project root), not inside `code/`

## Key Parameters
| Parameter | HDV | AV |
|-----------|-----|-----|
| τ (reaction time) | 1.5s | 0.5s |
| v_max | 5.2 cells/s (140 km/h) | 5.2 cells/s |
| MLC k / r0 | 8.0 / 0.3 | 8.0 / 0.3 |
| DLC k / Δv0 | 3.0 / 1.0 | 5.0 / 0.4 |

Theoretical capacity (homogeneous HDV): 2127 veh/h/lane
