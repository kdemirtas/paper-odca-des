# ARCHITECTURE: paper-odca-des
> **Owned by `/architect`. Two pages max. Last updated 2026-09-19.** Code follows this file; when
> they disagree, either the code is wrong or this file is, and a `DECISIONS.md` entry says which.

## Purpose
The code side of the ODCA-DES paper: this paper's parameter values, scenario definitions, the runs that write `code/output/`, and the figure scripts that write `figures/`. The simulator itself is the external package `odca-des` (import `odca`, `~/Papers/odca-des`, D-2026-09-19-6 to -10), shared with the other ODCA papers; its contract is `~/Papers/odca-des/ARCHITECTURE.md`. The manuscript's structure belongs to `research-lead` and `paper-author` (`AGENDA.md`), not to this file.

## Boundaries
Modules, what each owns, and what it may import. A module not listed here does not exist yet;
`/architect` adds it before code does.

| Module | Owns | May import | Never imports |
|---|---|---|---|
| `odca` (package `odca-des`, editable path dependency) | the simulator, parameter types, analysis and the one CI function, NaSch, viewers, the experiment kit (D-2026-09-19-9) | its own modules only | this repo: nothing in `odca` imports `config` or a script. |
| `config.py`, `configs/*.yaml` | this paper's values: S1 network, demand and run in `configs/` (vehicle and driver values are the odca defaults, `odca://`); `config.py` loads them as `HDV_VEHICLE`, `HDV_DRIVER`, `AV_VEHICLE`, `AV_DRIVER`, `S1_NETWORK`, `S1_OD_FLOWS`, `sim_config()`; `REPLICATION_SEEDS` (1 to 20), `SENSITIVITY_SEEDS` (first 10), `SCALABILITY_SEEDS` (first 3), `ILLUSTRATIVE_SEED` (42, from `configs/simulation.yaml`), `FIGURES_DIR` | `odca.params` | nothing in `odca` imports it. |
| scenarios: today `run_experiments.py`, `run_bottleneck.py`, `run_incident.py`, `run_demand_sweep.py`, `run_scalability.py`, `run.py` | this paper's scenario definitions, run through `odca.experiment` into `code/output/` | `odca.experiment`, `odca.simulation`, `odca.analysis`, `config` | `odca.entity`, `odca.infrastructure`, `odca.rng`. drift: `run_demand_sweep.py` builds its own simulation from entity, infrastructure and rng |
| `aggregate_multiseed.py` | every aggregate CSV (D-2026-09-19-3), through `odca.experiment` (`read_runs`, `aggregate`, `write_aggregate_csv`; the one 95% CI is `odca.analysis.intervals`) (D-2026-09-19-9) | `odca.experiment`, stdlib | the rest of `odca` |
| diagnostics: `diagnose_fd_capacity.py`, `plot_car_following.py` | ring-road capacity check, car-following figure; may build simulations below the engine | entity, infrastructure, rng, analysis, `config` | nothing. Write to `figures/` (`config.FIGURES_DIR`) |
| reporting: `manuscript_numbers.py`, `analyse_incident.py` | every number the manuscript quotes, printed from `code/output/`: the aggregates with their intervals, and the incident run's queue growth and recovery (D-2026-09-20-1) | `odca.experiment`, `config`, stdlib | the simulator; they run nothing |
| figures: `generate_figures.py`, `generate_paper_figures.py` | `figures/*.pdf` | `config`, `odca.baselines`, `odca.simulation` (single-run figures) | entity internals |
| viewers: `visualize.py`, `animate.py` | command lines over `odca.viewer` (playback, animation, time-space diagram); not paper inputs (D-2026-09-19-9) | `odca.viewer`, `odca.simulation`, `config` | `code/output/` result files |
| demo: `demo_trajectories.py`, `configs/demo_corridor.yaml` | one small corridor run and `figures/demo_trajectories.{pdf,png}`; not a manuscript figure (D-2026-09-19-36) | `odca.simulation`, `config`, matplotlib | `code/output/` result files |

## Layout (paper)

    paper/           paper-odca-des.tex, references.bib, elsarticle.cls; tables inline, no tables/ dir
    code/            experiments and figure scripts; .venv/ (uv) and output/ gitignored
    figures/         generated figure PDFs the manuscript includes
    review/external/ journal reviewer reports, advisor comments, response letters
    review/self/     manuscript-critic reports and author responses, numbered NN
    slides/          Beamer talks, created when the first talk exists
    data/            external datasets, gitignored, created when the first one lands
    docs/            longer reference docs that ARCHITECTURE.md or PROJECT.md link
    sources/         reference material, catalogued in sources/SOURCES.md
    CONTEXT.md       paper identity: title, authors, venue, dissertation source, notation

The code side has real modules (the table above) and a real data contract: `code/output/`
results are written by the experiment scripts, read by the figure scripts and by the manuscript's
quoted numbers. A change to a result format is a contract change.

## Data contracts
Every artifact that crosses a module boundary or leaves the project: its grain, its writer, its
readers, and where the contract is asserted. "Nowhere" is a legal entry and a backlog item.

| Artifact | Grain (key) | Written by | Read by | Asserted in |
|---|---|---|---|---|
| per-seed JSON: `output/multiseed/{s1_s4,bottleneck}/batch*/<label>_seed<n>.json`, `output/sensitivity_action_interval/ai_*/batch*/` | (label, seed, hdv_action_interval) | `run_experiments.py`, `run_bottleneck.py` with `--seeds` | `aggregate_multiseed.py` | nowhere |
| `output/multiseed/s1_s4/aggregate.csv`, `output/multiseed/bottleneck/bottleneck_aggregate.csv` | (scenario, av_penetration, hdv_action_interval, metric) | `aggregate_multiseed.py` only (D-2026-09-19-3) | `generate_figures.py`, manuscript tables | nowhere. drift: the runners also write an `aggregate.csv` with other columns |
| `output/sensitivity_action_interval/comparison.csv` | (scenario, av_penetration, action_interval, metric) | `aggregate_multiseed.py` | `generate_figures.py`, sensitivity subsection | nowhere |
| `output/scalability_benchmark.csv` | (num_cells, seed) | `run_scalability.py` | `generate_figures.py`, `tab:scalability` | nowhere |
| single-run JSON: `output/{experiments,bottleneck,demand_sweep,incident}/*.json` | label (sweep: density), at `ILLUSTRATIVE_SEED` | runners without `--seeds`, `run_demand_sweep.py`, `run_incident.py` | figure scripts | nowhere |
| golden fingerprint: `odca-des/tests/golden/paper_odca_des/` (this paper's `config.py` copy, `scenarios.py`, `fingerprint.json`) | (scenario, seed) in `--quick` mode: summary stats and counters | `uv run pytest --write-golden` in odca-des | odca-des `tests/test_golden.py` (D-2026-09-19-8) | the check itself, exact match |
| `figures/*.pdf` | one file per figure | figure scripts, diagnostics | manuscript `\includegraphics` | the compile |

## Core types
The concepts the code passes around. Each has one definition; functions take the type, not its
fields.
The rows below are `odca-des`'s types, listed here for reference; `~/Papers/odca-des/ARCHITECTURE.md` owns them.

| Type | Meaning | Defined in |
|---|---|---|
| `VehicleConfig`, `HumanDriverConfig`, `AutonomousDriverConfig`, `LogisticLaneChangeConfig` | one vehicle type's parameters; this paper's values are `HDV_VEHICLE`, `HDV_DRIVER`, `AV_VEHICLE`, `AV_DRIVER` in `config.py` | schemas in `odca/params.py` (D-2026-09-19-23) |
| `SimConfig`, `NetworkConfig`, `ODFlow`, `Destination` | one run; `config.sim_config(**overrides)` gives the S1 run with changes | schemas in `odca/params.py`, values in `config.py` |
| `Cell`, `Lane`, `Freeway` | the spatial resources | `odca/infrastructure/` |
| `Vehicle` (`HDV`, `AV`) | one vehicle with its movement and driver processes | `odca/entity/vehicle.py` |
| `TrajectoryRecord` | one T(x, n) passage record | `odca/entity/vehicle.py` |
| `SimulationResult`, `RunCounters` | vehicles, completed vehicles, counters and config of one run | `odca/simulation/result.py` |

## Invariants
What must hold after every run, each with the check that proves it.

1. **One vehicle per cell.** `Cell.resource` has capacity 1. Checked by construction (`cell.py`), no test.
2. **Headway by delayed release.** A cell is released tau seconds after its vehicle leaves it (`_delayed_release`, `_exit`), so homogeneous single-lane capacity is 3600 / (tau + d / v_max) = 2127 veh/h at HDV defaults. Checked by eye in `diagnose_fd_capacity.py`; no assertion (BACKLOG B2).
3. **Same config and seed, same numbers.** `Simulation` spawns its streams in a fixed order: six behaviour streams, then one per OD flow in `od_flows` order. A new stream goes last, or every number moves. Checked by the golden fingerprint (planned, D-2026-09-19-5).
4. **One driver-heterogeneity rule.** tau LogNormal clipped to [0.5, 3.0], action_interval LogNormal clipped to [0.3, 3.0], slowdown_prob Normal clipped to [0, 1], drawn in that order from their own streams. drift: copied in `generator.py`, `engine.py`, `run_demand_sweep.py`, `diagnose_fd_capacity.py`.
5. **Units stay inside.** Cells, cells/s and seconds everywhere in `odca/`; km/h, veh/h and veh/km appear only at the reporting edge, through `CELL_LENGTH_M`.
6. **Every quoted number has a file.** Each number in the abstract, body, tables and conclusion is read from a CSV named in Data contracts. Checked at revision time by `manuscript-critic`; no script.

## Proof strategy
How a change is shown to be neutral, and how a change that is meant to move a number is shown
to move only that number.

- **Golden fingerprint (code changes).** S1-S4 and the bottleneck in `--quick` mode (300 s) for seeds 1-3:
  summary statistics and event counters, recorded 2026-09-19, now `odca-des/tests/golden/paper_odca_des/`,
  run by `uv run pytest` in odca-des (D-2026-09-19-8). During the code-quality refactor it may be
  re-recorded, with the moved values stated (Kerem, 2026-09-19); a change meant to move numbers reruns the full
  20-seed set and pastes before/after of every quoted number (D-2026-09-19-5).
- **Compile.** `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`: 0 errors, 0 undefined references, 0 missing
  citations, no overfull hbox over 10 pt. The `.log` is the evidence.
- **Numbers.** Every quoted number is traced to a file under `code/output/`; a PR that regenerates
  results pastes the before/after of every quoted figure it moves. A number with no source file is a finding, not a caveat.
- **Reproduction.** The commands in `README.md` regenerate `figures/` and `code/output/` from the
  seeds in `code/config.py`; a seed change is a decision, not a tweak.
- **References.** `bib-validator` passes on `paper/references.bib`: no orphan, no uncited, no
  unresolvable entry.
- **Review.** A revision pass ends with `review/self/critic_report_NN.md` showing 0 Critical and
  0 Major open items, and `paper/revision.diff` against the baseline commit.

## Longer material
What does not fit in two pages lives under `docs/` and is linked from the row or section it
supports; a doc no row links is a candidate for deletion.

Manuscript workstreams live in `AGENDA.md` (owned by `research-lead`); notation, parameters and the paper's identity in `CONTEXT.md`.

## Change protocol
A structural change (a new module, a moved boundary, a changed contract or type) starts with
`/architect`, cites a `D-` id from `DECISIONS.md` in its commit, and is reviewed by `/reviewer`
against this file. A behavior change cites the decision that moved the number and updates every
place the number is quoted in the same PR.
