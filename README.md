# Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata

This repository contains the manuscript, simulation code, and figures for the paper:

> **Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata**
> Kerem Demirtas, Pitu Mirchandani, Xuesong Zhou
> Target journal undecided: a version is written for *Transportation Research Part B:
> Methodological* and for *Simulation Modelling Practice and Theory* (D-2026-09-20-14).

## Overview

ODCA-DES is a traffic microsimulation framework in which the cell is passive and the vehicle is the process. Cellular automata have been simulated on discrete-event engines since Cell-DEVS, and that combination is not claimed here (D-2026-09-20-13); what is new is the inversion. Each vehicle is an asynchronous SimPy process that acquires cell resources through a request-wait-seize-delay-release protocol, and each cell is a resource of capacity one with no transition function of its own. Congestion emerges from resource contention rather than from cell rules, speed is a real number carried by the vehicle rather than a discrete cell state, and the delayed cell-release mechanism produces headways consistent with Newell's simplified car-following model, yielding a triangular fundamental diagram without explicit calibration.

Key features:

- **Event-driven**: time advances event-to-event, not in fixed timesteps
- **Continuous speeds** on a discrete spatial grid (hybrid discretization)
- **Per-driver heterogeneity**: reaction time, action interval, and slowdown probability drawn from distributions
- **Mixed traffic**: human-driven vehicles (HDV) with per-vehicle driver processes and autonomous vehicles (AV) with a central controller
- **Native T(x,n) trajectories**: passage-time output aligned with Newell's kinematic wave theory

## Repository Structure

```
paper/                     LaTeX manuscript (Elsevier elsarticle format)
  paper-odca-des_trb.tex     Source, Transportation Research Part B version
  paper-odca-des_smpt.tex    Source, Simulation Modelling Practice and Theory version
  references.bib             Bibliography (shared)
  paper-odca-des_*.pdf       Compiled PDFs

figures/            Paper figures (PDF)

slides/             Presentation slides (Beamer)

code/               Simulation codebase (Python + SimPy)
  odca/             Core framework
    infrastructure/ Cell, Lane, Freeway spatial classes
    entity/         Vehicle, HDV, AV, AV Controller
    models/         Car-following (Newell) and lane-changing models
    simulation/     SimPy engine and vehicle generator
    analysis/       Edie's generalized FD metrics
    baselines/      NaSch classical CA baseline
    rng.py          Reproducible RNG via numpy SeedSequence
  config.py         Vehicle parameters and defaults
  run_experiments.py       S1-S4 scenario experiments
  run_demand_sweep.py      Density-initialized FD sweeps
  run_bottleneck.py        Lane-closure bottleneck experiments
  run_incident.py          Temporary incident scenario
  diagnose_fd_capacity.py  Ring-road FD capacity diagnosis
  generate_figures.py      Generate all paper figures
  plot_car_following.py    Two-vehicle car-following visualization
  animate.py               Grid animation and time-space diagrams
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

The simulator is the shared package `odca-des`, installed editable from a sibling checkout
(`~/Papers/odca-des`, repo `kdemirtas/odca-des`):

```bash
git clone https://github.com/kdemirtas/odca-des.git ../odca-des   # from the Papers folder
cd code
uv sync
```

### Running Simulations

All scripts should be run from the `code/` directory:

```bash
# Run main scenario experiments (S1-S4)
uv run python run_experiments.py

# Generate fundamental diagrams via density sweep
uv run python run_demand_sweep.py

# Run bottleneck (lane closure) experiments
uv run python run_bottleneck.py

# Run incident scenario (baseline + incident)
uv run python run_incident.py

# Diagnose FD capacity on ring road
uv run python diagnose_fd_capacity.py
```

Results are written to `code/output/`.

### Generating Figures

```bash
cd code
uv run python generate_figures.py
```

Figures are saved to `figures/`.

### Compiling the Paper

```bash
cd paper
for f in paper-odca-des_trb paper-odca-des_smpt; do
  pdflatex -interaction=nonstopmode $f \
    && bibtex $f \
    && pdflatex -interaction=nonstopmode $f \
    && pdflatex -interaction=nonstopmode $f
done
```

The two files are the same manuscript aimed at two journals (D-2026-09-20-14). They differ in six
places (the `\journal` line, the abstract opening, the introduction's first paragraph, the
generality sentences closing the introduction and the conclusion, and a Future Research bullet on
transfer to a second domain); everything else is shared, and a change to shared content goes into
both files in the same edit.

## Key Parameters (HDV Defaults)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `tau` | 1.5 s | Minimum time headway |
| `d` | 1.0 cell | Minimum spacing |
| `v_max` | 5.2 cells/s (140 km/h) | Maximum speed |
| Cell length | 7.5 m | Spatial discretization |
| Theoretical capacity | 2127 veh/h | From Newell triangular FD |

## License

This repository is part of a PhD dissertation at Arizona State University.
