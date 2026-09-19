# DECISIONS: paper-odca-des
> One entry per decision, newest first, never edited after the fact: a reversed decision gets a
> new entry that names the one it replaces. Ids are `D-YYYY-MM-DD-n`. Code that implements a
> decision cites the id; `/reviewer` checks the citation both ways. `Source` says where the
> decision came from: Kerem directly, an `ASSUMPTIONS.md` row he accepted or corrected (the row
> then leaves that file, `/next-assumption`), or another project's decision this one inherits.
> Entries dated before 2026-09-19 were mined from `STATUS.md`, `AGENDA.md` and git by the
> `/architect` retrofit; the decision itself was Kerem's at the date shown.

| Id | Decided | What | Source | Replaces |
|---|---|---|---|---|
| D-2026-09-19-36 | 2026-09-19 | A demo corridor run with a trajectory figure, outside the manuscript | Kerem | none |
| D-2026-09-19-28 | 2026-09-19 | Incidents as config (`run_incident.py` uses `IncidentConfig`) | inherited: odca-des D-2026-09-19-28 | none |
| D-2026-09-19-27 | 2026-09-19 | Origin and destination cells, transparent unless limited | inherited: odca-des D-2026-09-19-27 | none |
| D-2026-09-19-26 | 2026-09-19 | Named origins and destinations, OD demand in veh/h; S1 end traffic spread over the four lane ends: moves every S1-S4 number | inherited: odca-des D-2026-09-19-26 | D-2026-09-19-11 for S1-S4 |
| D-2026-09-19-25 | 2026-09-19 | YAML configs: this paper's network, demand and run in `code/configs/`, vehicle and driver values from the odca defaults | inherited: odca-des D-2026-09-19-25 | none |
| D-2026-09-19-24 | 2026-09-19 | Driver split from Vehicle in the simulator | inherited: odca-des D-2026-09-19-24 | none |
| D-2026-09-19-23 | 2026-09-19 | Simulator configs: one per class, ConfigMixin, schemas in `odca/params.py` | inherited: odca-des D-2026-09-19-23 | none |
| D-2026-09-19-22 | 2026-09-19 | Lane-change probability per 5.2 cells driven (MLC) and per second (DLC); moves this paper's numbers and its lane-changing method text | inherited: odca-des D-2026-09-19-22 | none |
| D-2026-09-19-21 | 2026-09-19 | Paper-side bug fixes: replacement inflow in the demand sweep, time-split density heatmap, strict aggregation and JSON, speed-profile vehicle set | Kerem (fix every bug) | none |
| D-2026-09-19-16 | 2026-09-19 | Where manuscript and code disagree, the manuscript is the spec; bugs are fixed before the cleanup | Kerem | none |
| D-2026-09-19-10 | 2026-09-19 | odca-des is MIT licensed | Kerem | none |
| D-2026-09-19-9 | 2026-09-19 | odca-des holds the core, parameter types, analysis with the one CI function, NaSch, viewers (optional extra) and an experiment kit; papers keep parameter values, scenario definitions and figures | Kerem | none |
| D-2026-09-19-8 | 2026-09-19 | Papers depend on odca-des as an editable path dependency; each paper's golden fingerprint is a test inside odca-des; a submitted paper records the odca-des tag it ran on | Kerem | none |
| D-2026-09-19-7 | 2026-09-19 | The central package is a new private repo `kdemirtas/odca-des` at `~/Papers/odca-des`, import name `odca`; the older `kdemirtas/odca` stays untouched as the archive | Kerem | none |
| D-2026-09-19-6 | 2026-09-19 | One central `odca` simulator package, published with this paper; other papers add features to it, never change this paper's results except by a bug fix. Extracted and refactored first, with a new golden | Kerem | Papers rule: each ODCA repo keeps its own copy of `code/odca/` |
| D-2026-09-19-5 | 2026-09-19 | Proof of neutrality: committed quick-mode golden fingerprint, exact match; full 20-seed rerun before any quoted number moves | Kerem | none |
| D-2026-09-19-4 | 2026-09-19 | Two named seed sets in `config.py`: `REPLICATION_SEEDS` (1-20) and `ILLUSTRATIVE_SEED` (42) | Kerem | none |
| D-2026-09-19-3 | 2026-09-19 | `aggregate_multiseed.py` is the only writer of aggregate CSVs and the only CI code | Kerem | none |
| D-2026-09-19-2 | 2026-09-19 | Parameter types move into `odca/params.py`; `odca/` never imports `config` | Kerem | none |
| D-2026-09-19-1 | 2026-09-19 | Doc set retrofitted; `AGENDA.md` stays the manuscript plan, `HANDOVER.md` holds the code list | Kerem | none |
| D-2026-04-20-4 | 2026-04-20 | Scalability benchmark: S1, 200 to 3200 cells x 4 lanes, 1800 s, 3 seeds | Kerem (AGENDA) | none |
| D-2026-04-20-3 | 2026-04-20 | Time-varying demand is not built; it goes to Limitations | Kerem (AGENDA) | none |
| D-2026-04-20-2 | 2026-04-20 | Action-interval sensitivity on S1 only: 10 seeds at 0.5 and 0.25, plus the 20-seed 1.0 runs | Kerem (STATUS) | AGENDA Dispatch 1B scope |
| D-2026-04-20-1 | 2026-04-20 | Every table number is a mean over 20 replications (seeds 1-20) with a 95% t-interval | Kerem (AGENDA) | single seed 42 |
| D-2026-03-28-1 | 2026-03-28 | AVs make no discretionary lane changes (`dlc_enabled=False`) | Kerem (STATUS) | none |
| D-2026-03-26-1 | 2026-03-26 | A vehicle behind a moving leader never stops dead: creep at 0.1 cells/s | Kerem (STATUS) | none |
| D-2026-03-14-1 | 2026-03-14 | Randomness comes from one `SeedSequence` stream per source, shared by all vehicles, not one per vehicle | Kerem (CLAUDE.md) | none |

## D-2026-09-19-36: a demo corridor run with a trajectory figure
**What.** `code/configs/demo_corridor.yaml` (3 lanes, 400 cells, every lane to every lane end, 20% AV, lane 2 blocked for two minutes) and `code/demo_trajectories.py`, which writes `figures/demo_trajectories.{pdf,png}`: a time-space diagram per lane and the lane-by-position traces of vehicles crossing from lane 1 to lane 3. A check of the simulator after the refactor, not a manuscript figure. Id 36 skips 29 to 35, which odca-des uses the same day.
**Evidence.** Kerem, 2026-09-19: "run a simple scenario and plot some trajectories". Run: 487 generated, 426 completed, 2161 lane changes, 44 missed exits (STATUS session 16).
**Replaces.** nothing
**Cited by.** `code/demo_trajectories.py`

## D-2026-09-19-26 to -28: demand, endpoints, incidents (inherited)
**What.** See odca-des D-2026-09-19-26, -27, -28. For this paper: S1-S4 demand is now
`code/configs/demand_s1.yaml` (veh/h per named pair, end traffic spread over `end_lane_1..4`), so
every S1-S4 number moves and tex:874 (segment end from any lane) must be rewritten at N11; the
incident run uses `IncidentConfig`.
**Evidence.** odca-des `DECISIONS.md`, Kerem 2026-09-19.
**Replaces.** D-2026-09-19-11 for S1-S4.
**Cited by.** `code/configs/`, `code/run_incident.py`, AGENDA WS-11.

## D-2026-09-19-25: YAML configs (inherited)
**What.** See odca-des D-2026-09-19-25. `config.py` loads `code/configs/simulation.yaml`.
**Evidence.** odca-des `DECISIONS.md`, Kerem 2026-09-19.
**Replaces.** nothing.
**Cited by.** `code/config.py`, `code/configs/`.

## D-2026-09-19-24: driver split from vehicle (inherited)
**What.** See odca-des D-2026-09-19-24. Refactor only; this paper's scripts that build vehicles
directly (`run_demand_sweep.py`, `diagnose_fd_capacity.py`) follow when odca-des N4 lands.
**Evidence.** odca-des `DECISIONS.md`, Kerem 2026-09-19.
**Replaces.** nothing.
**Cited by.** STATUS Session 12.

## D-2026-09-19-23: simulator configs (inherited)
**What.** See odca-des D-2026-09-19-23. This paper's `config.py` keeps values only; the schemas
live in `odca/params.py`.
**Evidence.** odca-des `DECISIONS.md`, Kerem 2026-09-19.
**Replaces.** nothing.
**Cited by.** STATUS Session 12.

## D-2026-09-19-22: lane-change probability per distance and per second (inherited)
**What.** See odca-des D-2026-09-19-22. The logistic MLC curve is a probability per 5.2 cells
driven, DLC per second, converted over each evaluation's exposure. It moves every golden run of
this paper, and the lane-changing section must describe it (AGENDA WS-11).
**Evidence.** Kerem, 2026-09-19: "MLC per distance, DLC per second (Recommended)";
odca-des `docs/lane-change-rate.md`.
**Replaces.** nothing.
**Cited by.** AGENDA WS-11, HANDOVER N11.

## D-2026-09-19-21: paper-side bug fixes
**What.** `run_demand_sweep.py` replaces every exiting vehicle at the start of its lane (tex:902) instead of a Poisson inflow at k * v_max, and through vehicles exit from any lane. `generate_figures.py` `_compute_density` splits each cell visit across the 15 s bins it overlaps. `aggregate_multiseed.py` fails on an unreadable file or a seed present twice. Result JSON uses `json_default.numpy_default` instead of `default=str`. `generate_paper_figures.py` `fig_speed_profile` uses the vehicles exiting in the measurement period (odca-des D-2026-09-19-14).
**Evidence.** Opus principal-engineer review 2026-09-19 (`docs/code-review-2026-09-19.md`); Kerem, 2026-09-19: "Fix every bug." (top-10 #7, #8, A22, A23, A25) and the review of the bug fixes (correctness finding 3). Sweep check: target k = 0.3 veh/cell measured 0.298 to 0.306.
**Replaces.** Nothing.
**Cited by.** `code/run_demand_sweep.py`, `code/generate_figures.py`, `code/aggregate_multiseed.py`, `code/json_default.py`, `code/generate_paper_figures.py`.

## D-2026-09-19-16: the manuscript is the spec; bugs before cleanup
**What.** Where the manuscript's stated model and the code disagree, the code is fixed to the text (exit lane tex:874, throughput tex:973, delay tex:975); "maximum queue length" (tex:978), listed but never reported, is dropped from the list at N11. Correctness bugs are fixed in odca-des before the cleanup items. The fixes are odca-des D-2026-09-19-11 to -15 (ids 11 to 15 are used there, so this entry is 16). An exception found by the same check: tex:232 (T_req(c+1) = T_arr(c) + l/v) is the manuscript bug; the code's immediate request T_req(c+1) = T_arr(c) is right and eq. 278 depends on it.
**Evidence.** Kerem, 2026-09-19: "Yes fix bugs first."; "Paper is the spec"; "you are allowed to make reasonable decisions after bringing something you are about to assume to me"; "immediate request is required (consider freeflow). that is a bug."
**Replaces.** Nothing.
**Cited by.** odca-des `DECISIONS.md` D-2026-09-19-11 to -15; HANDOVER N11 (manuscript edits).

## D-2026-09-19-10: odca-des is MIT licensed
**What.** `odca-des` carries an MIT `LICENSE` from its first commit.
**Evidence.** Kerem, 2026-09-19, `/architect` ("MIT"), chosen over BSD-3, GPL-3 (the old `kdemirtas/odca`) and deciding later.
**Replaces.** Nothing.
**Cited by.** `odca-des/LICENSE`, `odca-des/pyproject.toml`, when the repo is created (N1).

## D-2026-09-19-9: package scope, core plus experiment kit
**What.** `odca-des` contains: the simulator core (`infrastructure`, `models`, `entity`, `simulation`,
`rng`), the parameter types (`odca/params.py`), `analysis` including the single 95% interval
function, the NaSch baseline, the viewers as an optional `[viewer]` extra (pygame), and an
experiment kit (`odca.experiment`: run a scenario over a seed list, write one JSON per
(scenario, seed), aggregate them into the CSV schema of Data contracts). A paper keeps only its
parameter values (`config.py`), its scenario definitions, its figure scripts and its diagnostics.
Paper-specific capabilities (platooning, lane-change event logs) enter the package through that
paper's switch-over, switched off by default.
**Evidence.** Kerem, 2026-09-19, `/architect` ("Core + experiment kit"), chosen over core with stats
and viewers, and core only. The CI code existed in 3 copies and the runner machinery is repeated
per paper.
**Replaces.** Nothing. It absorbs D-2026-09-19-3: the one aggregator becomes `odca.experiment`.
**Cited by.** `~/Papers/odca-des/ARCHITECTURE.md` (Boundaries); odca-des HANDOVER N6.

## D-2026-09-19-8: editable dependency, fingerprints as package tests
**What.** Every paper declares `odca-des = { path = "../../odca-des", editable = true }` in
`code/pyproject.toml`, so a fix reaches all papers at once. Each paper's golden fingerprint lives
in `odca-des/tests/golden/<paper>/` (its scenario definitions plus `fingerprint.json`) and must
match exactly before a change to `odca-des` merges. At submission a paper tags the `odca-des`
commit it ran on (for example `paper-odca-des-v1`) and names the tag in its README and STATUS.
**Evidence.** Kerem, 2026-09-19, `/architect` ("Editable + fingerprint tests"), chosen over pinning
at submission and always pinning.
**Replaces.** Nothing.
**Cited by.** `ARCHITECTURE.md` Proof strategy; HANDOVER N1.

## D-2026-09-19-7: the package home
**What.** A new private repo `kdemirtas/odca-des`, checked out at `~/Papers/odca-des`, next to the
papers that use it. The import name stays `odca`. It starts from this paper's `code/odca/` with its
git history. The older `kdemirtas/odca` (dissertation-era code, GPL-3, last push 2025-04) is left
untouched as the archive.
**Evidence.** Kerem, 2026-09-19, `/architect` ("New repo kdemirtas/odca-des"), chosen over reusing
`kdemirtas/odca`. The import name is kept because the papers import from `odca` in 18 to 25 places each.
**Replaces.** Nothing.
**Cited by.** HANDOVER N1.

## D-2026-09-19-6: one central odca package, extracted first
**What.** `code/odca/` leaves this repo and becomes one simulator package in its own repo, published
with this paper (the first ODCA paper). The other three ODCA papers stop carrying copies and use the
package; what they need (platooning, lane-change event logging) is added to it as capabilities, so
in the end one package does both platooning and lane changing, and each paper uses what its
context needs. A bug is fixed once, centrally. Another paper's work may change this paper's results
only through a bug fix. Order: the extraction and the N2 to N8 cleanup happen first, before the full
rerun; the running rerun was stopped, and a new golden fingerprint is recorded from the migrated,
refactored package.
**Evidence.** Kerem, 2026-09-19: "There should be a central simulator code odca, which gets
published with the first paper. The other paper's usage should not change the results of this first
paper unless there is a bug, but improve odca with additional capabilities and features. In the end,
we have a single odca that allows both platooning and lane changing, it is one simulation package."
"If we fix a bug, we don't have to fix that bug everywhere, so it should be central." On timing: "I
would rather stop the running simulations and do it as the first task, as that would also move the
golden. We will get a new golden with the migrated refactored package." Prompted by the fork
comparison of 2026-09-19: `paper-lc-logistic`, `paper-odca-platoon` and `paper-odca-adaptive-platoon`
lack both the creep fix (D-2026-03-26-1) and `dlc_enabled` (D-2026-03-28-1), and each added its own
changes (`lc_events`; `platoon/` plus 117 and 139 changed engine lines).
**Replaces.** The Papers-wide rule in `~/Papers/CLAUDE.md` ("The four ODCA repos each carry their own
copy of `code/odca/`, no submodule"); no earlier `D-` id.
**Cited by.** When the extraction task is built.
⚠️ My reading, not Kerem's words: (1) "unless there is a bug" is enforced by keeping each paper's
golden fingerprint as a test inside the package, with new capabilities switched off by default; a
change that makes this paper's fingerprint differ needs a bug-fix decision and a re-recorded golden.
(2) The fingerprint recorded today (`code/golden/fingerprint.json`, from the pre-migration code) is
still the check that the migration and refactor are neutral: if the new golden differs from it, each
difference is either an intended bug fix with its own decision, or a defect. (3) Where the new repo
lives and how the papers depend on it (editable path dependency while developing, a pinned version
at submission) is not decided yet.

## D-2026-09-19-5: neutrality is proven by a quick-mode golden fingerprint
**What.** `code/golden/fingerprint.json`, committed, holds S1-S4 and the bottleneck in `--quick`
mode (300 s) for seeds 1-3: summary statistics and event counters. A refactor must reproduce it
exactly. Before any quoted number is allowed to move, the full 20-seed set is rerun and compared
with the manuscript. The first item (N1) rebuilds `code/output/` and records the fingerprint.
**Evidence.** Kerem, 2026-09-19, `/architect` retrofit ("Quick golden + full check"). No test or
reference result existed; `code/output/` was absent from the checkout.
**Replaces.** Nothing.
**Cited by.** `ARCHITECTURE.md` Proof strategy; `HANDOVER.md` N1. Code: none yet.

## D-2026-09-19-4: two named seed sets
**What.** `config.py` declares `REPLICATION_SEEDS = 1..20` for every table and interval and
`ILLUSTRATIVE_SEED = 42` for every single-run figure. No script hard-codes a seed. The car-following
figure's seed 99 becomes a named constant unless the figure is unchanged at 42.
**Evidence.** Kerem, 2026-09-19, `/architect` retrofit. Seed 42 was hard-coded in 7 scripts, 99 in
`plot_car_following.py`, seeds 1-20 only in `run_all_phase1.sh`.
**Replaces.** Nothing.
**Cited by.** `HANDOVER.md` N4. Code: none yet.

## D-2026-09-19-3: one aggregator
**What.** Runners write one JSON per (scenario, seed). `aggregate_multiseed.py` alone writes the
aggregate CSVs and holds the only 95% interval code. The aggregate writers and t-tables inside
`run_experiments.py` and `run_bottleneck.py` are deleted.
**Evidence.** Kerem, 2026-09-19, `/architect` retrofit. Two `aggregate.csv` schemas existed; the
figures and the paper read only the `aggregate_multiseed.py` one. The t-table was copied 3 times.
**Replaces.** Nothing.
**Cited by.** `ARCHITECTURE.md` Data contracts; `HANDOVER.md` N3. Code: none yet.

## D-2026-09-19-2: parameter types live in odca
**What.** `VehicleParams`, `ODFlow`, `NetworkConfig`, `SimConfig` and `CELL_LENGTH_M` move to
`odca/params.py`. `config.py` keeps only this paper's values and imports the types. Nothing in
`odca/` imports `config`, so the framework copied into the other ODCA repos carries no paper's settings.
**Evidence.** Kerem, 2026-09-19, `/architect` retrofit. `odca/entity`, `odca/simulation` and
`odca/analysis` imported `config` for both types and `CELL_LENGTH_M`.
**Replaces.** Nothing.
**Cited by.** `ARCHITECTURE.md` Boundaries; `HANDOVER.md` N6. Code: none yet.

## D-2026-09-19-1: doc set retrofitted
**What.** The 2026-09-18 doc set is added to this pre-existing paper. `AGENDA.md` stays the
manuscript plan owned by `research-lead`; `HANDOVER.md` carries the code task list; `STATUS.md`
stays the session log. `DECISIONS.md` (this file) replaces the per-paper `decisions.md` convention.
**Evidence.** Kerem, 2026-09-19, `/pickup and retrofit /architect`.
**Replaces.** Nothing.
**Cited by.** `HANDOVER.md` (Type stamp).

## D-2026-04-20-4: scalability benchmark shape
**What.** S1 (all HDV) at 200, 400, 800, 1600 and 3200 cells per lane, 4 lanes, 1800 s simulated,
3 seeds each; wall-clock, event count and real-time ratio recorded.
**Evidence.** `AGENDA.md` Dispatch 1C (2026-04-20); `STATUS.md` Session 7.
**Replaces.** Nothing.
**Cited by.** `code/run_scalability.py`; manuscript `tab:scalability`.

## D-2026-04-20-3: no time-varying demand
**What.** Demand stays constant per OD flow. Building time-varying demand is new infrastructure;
it is listed in Limitations instead.
**Evidence.** `AGENDA.md` WS-4 (2026-04-20): no such support in `code/odca/`.
**Replaces.** Nothing.
**Cited by.** `BACKLOG.md` B4; manuscript Limitations.

## D-2026-04-20-2: sensitivity on S1 only
**What.** HDV action-interval sensitivity runs S1 only, 10 seeds each at 0.5 s and 0.25 s,
combined with the 20-seed runs at 1.0 s into a 3-point curve.
**Evidence.** `STATUS.md` Session 7: S2 at 0.5 s and below ran for 12 hours without output
(event storm), was killed and discarded. S1 is the all-HDV case, where the interval matters most.
**Replaces.** `AGENDA.md` Dispatch 1B scope (S1-S4 and bottleneck, 20 seeds each).
**Cited by.** `code/aggregate_multiseed.py` `aggregate_sensitivity`; manuscript sensitivity subsection.

## D-2026-04-20-1: 20 replications with 95% t-intervals
**What.** Every S1-S4 and bottleneck number in the paper is a mean over seeds 1-20 with a
two-sided 95% Student-t interval.
**Evidence.** `AGENDA.md` WS-1 (2026-04-20); `STATUS.md` Session 7 and 8. The earlier single seed 42
made the 0% AV bottleneck throughput 1146 veh/h against a 20-seed mean of 1341 (+17%).
**Replaces.** Single-seed results at seed 42.
**Cited by.** `code/run_all_phase1.sh`; `code/aggregate_multiseed.py`.

## D-2026-03-28-1: AVs make no discretionary lane changes
**What.** Centrally controlled AVs change lanes only when they must (a blockage, reaching the exit
lane). `VehicleParams.dlc_enabled` is `False` for AVs and `Vehicle._evaluate_direction` skips DLC.
**Evidence.** `STATUS.md` Session 5 (2026-03-28): speed-seeking AV lane changes caused merge
turbulence and a non-monotone bottleneck result; with DLC off every metric improved monotonically
with penetration. Commit `1587642`.
**Replaces.** Nothing.
**Cited by.** `code/config.py` `AV_PARAMS`; `code/odca/entity/vehicle.py` `_evaluate_direction`.

## D-2026-03-26-1: creep speed instead of a zero-speed deadlock
**What.** When Newell's rule gives a speed of 0 or less but the leader is moving and there is space,
the follower moves at 0.1 cells/s so the gap can grow.
**Evidence.** `STATUS.md` "Completed" (2026-03-26, zero-speed deadlock); commit `e4dc209`.
**Replaces.** Nothing.
**Cited by.** `code/odca/entity/vehicle.py` `_MIN_CREEP_SPEED`, `_speed_for_leader`.

## D-2026-03-14-1: one random stream per source
**What.** `RNGRegistry` spawns one `SeedSequence` child per source of randomness (slowdown, MLC,
DLC, the three driver-parameter draws, one per OD generator), shared by all vehicles.
**Evidence.** `CLAUDE.md` Key Architecture ("per-source streams ... not per-vehicle"); `code/odca/rng.py`
in the initial commit `e6133bb`.
**Replaces.** Nothing.
**Cited by.** `code/odca/rng.py`; `code/odca/simulation/engine.py`. The "each vehicle gets its own RNG"
docstrings in both files are stale (`HANDOVER.md` N2).
