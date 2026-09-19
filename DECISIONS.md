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
