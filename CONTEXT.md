# ODCA-DES Paper Project

## What This Is
From Kerem Demirtas's PhD dissertation at Arizona State University.
**Title:** "Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata"
**Target journal:** Transportation Research Part B

## Authors
- Kerem Demirtas (School of Computing and Augmented Intelligence, ASU)
- Pitu Mirchandani (School of Computing and Augmented Intelligence, ASU)
- Xuesong Zhou (School of Sustainable Engineering and the Built Environment, ASU)

## Repository Layout
```
paper-odca-des/
├── paper/              # LaTeX manuscript (paper-odca-des.tex, references.bib, elsarticle); tables inline
├── figures/            # All generated figure PDFs (output of code/)
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
│   ├── visualize.py              # Interactive Pygame visualization (ovals=AV, rects=HDV)
│   ├── animate.py                # Matplotlib grid animation and trajectory diagrams
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
| v_max (vehicle maximum speed) | 5.2 cells/s (140 km/h) | 5.2 cells/s |
| v_lim (cell speed limit) | 5.2 cells/s on every cell of every scenario | same |
| MLC k / r0 | 8.0 / 0.3 | 8.0 / 0.3 |
| DLC k / Δv0 | 3.0 / 1.0 | 5.0 / 0.4 |

Theoretical capacity (homogeneous HDV): 2127 veh/h/lane

Free-flow speed is per vehicle and per cell, v_f(n, c) = min(v_max(n), v_lim(c)): what the
vehicle would hold on that cell with nobody in the way (odca-des D-2026-09-20-3). Delay is the
per-cell excess over it, so a cell driven at a posted limit adds no delay. The three coincide
numerically in this paper, where every cell posts 5.2 cells/s and both vehicle types have that
maximum speed; they separate in a scenario with a work zone.
