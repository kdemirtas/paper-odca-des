# STATUS — ODCA-DES Paper

## Session 20 (2026-09-20): assumptions walked, the parameter justification written into the paper
- Seven odca-des assumption rows closed with Kerem (its PR #16, D-2026-09-20-6 to -12), all
  accepted: the readable origin and destination names, the any-lane `end` kept for the lane-drop,
  incident and scalability runs, the wrong end lane counted as a missed exit, the exposure
  references, exposure starting at the first evaluation, the old `Vehicle` constants as config
  fields, and the vehicle-driver link with its counter split. Six rows left there.
- Manuscript (D-2026-09-20-8 here): Section 3.4.2 now justifies the lane-change parameters instead
  of only defining the conversion. Neither exposure reference is fitted: both are one free-flow
  driver-second (a human decides about once a second, and one second of free flow covers 5.2 cells),
  so k = 8.0, r_0 = 0.3, k_d = 3.0 and Delta v_0 = 1.0 cells/s state the chance of acting at one
  ordinary decision, and a reference c times longer would need every probability transformed as
  1 - P' = (1 - P)^c. Table `tab:vehicle_params` gained the two exposure-reference rows, and its
  "Perception delay" row, a name no parameter carries, is now "Action interval (max. re-evaluation
  gap)", delta_eval, 1.0 s HDV and 0.1 s AV controller cycle (Kerem: "rename that row").
- Build after both edits: 42 pages, 0 errors, 0 undefined references, 0 missing citations, no
  overfull box over 10 pt. Text only, no number moved; the edits sit on top of revision 2, so
  `paper-odca-des-prerevision-2.tex` and `revision-2.diff` still read as they did.
- Kerem's one code call: `lc_failures` is split into `lc_patience_failures` and `gap_rejections`
  (odca-des D-2026-09-20-12). Here only `code/demo_trajectories.py` prints both. The 124 result
  files keep the old single key until the pending rerun, and the manuscript quotes no lane-change
  failure count, so nothing in the paper changes. odca-des golden re-recorded, nothing moved.
- Measured on the way, from the 20-seed files: missed exits are 16.4% of completions in S1 (17,668
  of 107,694), 10.0% in S2, 6.7% in S3, 5.4% in S4. The counter bundles a missed off-ramp with a
  wrong end lane and only the total is stored.
- `/fix-drift` here: `AGENDA.md` workstream statuses WS-1 to WS-10 said "not-started" although
  sessions 7 to 10 and 18 finished them, and its Current state was four months stale; the open
  decision on discretionary lane changes said Kerem decides "before the N11 rerun", which has
  already run, so it now says a change means a second rerun. `STATUS.md` summary sections below the
  entries: "Latest Results (seed 42)" relabelled as the superseded 2026-03-28 record with a pointer
  to the aggregates, two Known Shortcomings struck as closed, the 2026-03-28 TODO list marked as
  history. `ARCHITECTURE.md`: the golden is recorded rather than "planned", the trait-sampling and
  aggregate-CSV drift notes are gone (both fixed in sessions 14 and 16), the review line names
  `revision-N.diff`. `CONTEXT.md` still drew the `code/odca/` tree that moved out on 2026-09-19.
  `README.md` said `pdflatex main`; the file is `paper-odca-des.tex`.
- ⏳ Unchanged: Kerem's read of the PDF against `revision-2.diff`, and the 124-job rerun that would
  let the tables carry mean cells held and mean origin wait.

## Session 19 (2026-09-20): assumptions walked with Kerem, free flow per vehicle and per cell
- Three odca-des assumption rows closed (its PRs #10 and #11): vehicles placed at t=0 leave from any
  lane (D-2026-09-20-1 there); travel time still starts when the origin cell is taken, with the wait
  before entry parked for the next rerun (D-2026-09-20-2 there, BACKLOG B10 there); free-flow speed
  is per vehicle and per cell (D-2026-09-20-3 there).
- The third is a correction and it changed code and text. Free-flow speed is now
  v_f(n, c) = min(v_max(n), v_lim(c)): the vehicle's maximum speed capped by the cell's posted limit.
  Delay is the per-cell excess over it, so a cell driven at a work-zone limit adds no delay and the
  lowered limit changes the free-flow travel time instead. Manuscript Section 3.4 defines the three
  symbols (Eq. free_flow_speed), Section 5.2 states the delay metric with them (Eq. delay), the FD
  derivation says it assumes a uniform road, and `CONTEXT.md` carries the same (D-2026-09-20-5).
- No number moved: every cell in every scenario posts 5.2 cells/s and both vehicle types have v_max
  5.2, so the minimum binds nowhere. odca-des golden 24/24 exact, 85/85 tests. Build after the text
  change: 42 pages, 0 errors, 0 undefined references, 0 missing citations, no overfull hbox.
- The edits land on top of revision 2; `paper/paper-odca-des-prerevision-2.tex` and
  `paper/revision-2.diff` are untouched, so what Kerem has not read yet still reads as it did.
- `manuscript-critic` round 3: `review/self/critic_report_03.md`, 0 Critical, 3 Major, 6 Minor, all
  applied and answered in `review/self/critic_author_response_03.md`. The three Major: the abstract,
  conclusion and bottleneck caption said the two open lanes carry "all" the demand from 50% AV when
  the table says 99.2% (all of it only at 70%); the conclusion said "close agreement" with the FD
  theory without the 92 to 93% ring-road number; the 131 s demand-weighted free-flow trip time was
  named but not derived, and is now derived in the caption and computed by `manuscript_numbers.py`
  (130.9 s against 153.8 s for the full segment). Minor: the 0.86 exponent in the scalability
  caption, the S1 label no longer reused for the half-demand run, the incident's 200 s warm-up
  motivated, the abstract cut from 408 to 198 words (accepted the same day, D-2026-09-20-7), and the
  bibliography items. `ASSUMPTIONS.md` is empty again.
- The odca-des finding is fixed, not parked: a speed limit now takes effect on the cell that posts
  it (odca-des D-2026-09-20-4, its PR #13), which closed its BACKLOG B11 the same day it opened.
- ⏳ Open: 14 assumption rows in odca-des, walked one at a time.

## Session 18 (2026-09-20): N11, the full rerun and the manuscript restated
- Rerun: 124 jobs (20 seeds x S1-S4, 20 seeds bottleneck, 10 seeds x two action intervals, plus the single runs) on 10 workers, 0 failed, then the timed runs alone on the machine. `run_all_phase1.sh` is now a job pool that reads its seed sets from `config.py`.
- Every number in the abstract, the five tables, the figure captions and the conclusion is restated from `code/output/`. What moved most:
  - S1-S4 throughput 4,494 to 5,874 veh/h (S1) and 6,664 to 6,983 (S4): the 0 to 70% AV gain is 18.9%, not 48%, because at 70% AV the network serves 99.8% of the 7,000 veh/h offered. Delay 254 to 216.6 s (S1) and 27.6 to 10.2 s (S4): a 95% reduction.
  - Bottleneck throughput 1,341 to 2,501 veh/h (0% AV) and 1,780 to 3,602 (70%). The plateau above 50% AV is demand saturation (the two open lanes carry the full 3,600 veh/h), not merge saturation; the paper says so now.
  - Sensitivity: 1.0 s to 0.25 s action interval gives 6.4% throughput (was 8.4%), most of it in the first halving.
  - Computational: SimPy events about 40 million per run (the old "total events" summed behaviour counters, about 57k); wall time 142-166 s, 22-25x real time, was 277-802 s. The honest comparison is decisions against timestep updates: S1 makes 2.20M speed evaluations against 7.41M updates at 0.25 s, but S4 makes 7.08M against 3.95M, because the controller decides at 10 Hz whatever happens.
  - Scalability: events x10.8 and wall x16.9 for a 16-fold longer network; real-time ratio 100x down to 5.9x.
- Two scenario findings, both written up and logged as assumptions:
  - The incident at 3,000 veh/h no longer congested anything (three lanes absorb one closed lane), so the figures showed free flow. It is now a two-lane closure at 4,500 veh/h: baseline delay 17.5 s, incident 237.1 s, queue 0.94 km at reopening growing to 1.69 km six minutes later, upstream speeds back within 2% of baseline 16 minutes after clearance, all three printed by the new `code/analyse_incident.py` (A-2026-09-20-2, accepted 2026-09-20 as D-2026-09-20-4).
  - Fundamental diagram: on a ring road the model reaches 1,948 veh/h (deterministic) to 1,978 (full stochastic), 92-93% of the analytic 2,127; the open sweep peaks at 1,587 because of its entry boundary. The claim of "close agreement" is now these numbers.
- Bug: `generate_paper_figures.py` and `generate_figures.py` both wrote `figures/fig_fd_theoretical.pdf`, and the analytic-only triangle overwrote the four-panel figure the manuscript cites. The analytic one is now `fig_fd_analytical.pdf`.
- Also fixed: `run_scalability.py` records `simpy_events` and `behaviour_events` (the old `total_events` was the counter sum; odca-des DECISIONS.md, entry 20 of 2026-09-19); the incident figures take a list of closed lanes; the manuscript gained an Implementation and Hardware subsection, which the conclusion had been citing.
- Manuscript: `paper/paper-odca-des-prerevision-2.tex` is the entry state, `paper/revision-2.diff` the diff (395 lines); the numbering is the rule since D-2026-09-20-3. Build: 0 errors, 0 undefined references, 0 missing citations, no overfull box over 10 pt, 42 pages.

## Session 17 (2026-09-20): named seeds (N9), diagnostics to figures/ (N10), rerun started (N11)
- N9 (D-2026-09-19-4): `config.py` declares `REPLICATION_SEEDS` (1 to 20), `SENSITIVITY_SEEDS` (first 10), `SCALABILITY_SEEDS` (first 3) and `ILLUSTRATIVE_SEED` (42, the seed of `configs/simulation.yaml`); no script names a seed. `plot_car_following.py` moved from 99 to the illustrative seed: its trajectories are identical at both (1,746 records compared; no random draw in that figure). `run_all_phase1.sh` reads its seed sets from `config.py`.
- N10: `diagnose_fd_capacity.py` and `plot_car_following.py` write to `figures/` (`config.FIGURES_DIR`); the ring road uses `lane.make_periodic()` (odca-des PR #9, its DECISIONS entry 35 of 2026-09-19), FD points byte-identical against the old wiring. `fig_car_following*.pdf` regenerated (not in the manuscript).
- `run_all_phase1.sh` is now a job pool: one job per (scenario, seed) for S1-S4, bottleneck and S1 sensitivity, plus the single runs (bottleneck, incident, demand sweeps), then aggregation, then the timed runs (single-seed S1-S4 for the computational table, scalability) alone on the machine.
- ⏳ N11: full rerun started 2026-09-20 00:00 with 10 parallel jobs (`code/output/orchestration.log`); restatement follows when it ends.

## Session 16 (2026-09-19): scripts on SimulationResult, the experiment kit and odca.viewer (odca-des PRs #6 to #8, N5 to N7); demo trajectories
- N5: every script reads `SimulationResult` (`completed_vehicles`, `counters`, `num_generated`) instead of the old results dict.
- N6: `run_experiments.py` and `run_bottleneck.py` use `odca.experiment` (`run_once`, `write_run`); `aggregate_multiseed.py` uses `read_runs`, `aggregate`, `write_aggregate_csv`; the CSVs it writes are byte-identical to the old aggregation on the same run files. `json_default.py` removed (`numpy_default` now in `odca.experiment`); `tests/test_result_contracts.py` is one contract test (passes).
- N7: `visualize.py` and `animate.py` are thin CLIs over `odca.viewer`; `animate.py --trajectory` smoke run saved a time-space diagram.
- Demo (Kerem: "run a simple scenario and plot some trajectories"): `configs/demo_corridor.yaml` (3 lanes, 400 cells, every lane to every lane end, 20% AV, lane 2 blocked cells 250-254 from t=240 s for 120 s, 720 s, seed 42) and `demo_trajectories.py` write `figures/demo_trajectories.{pdf,png}`: time-space diagram per lane plus lane-by-position traces of lane 1 to lane 3 crossers. Run: 487 generated, 426 completed, 61 on the road at the end, 2161 lane changes, 6285 lane-change attempts refused by patience, 44 missed exits. Not a manuscript figure.
- Review (paper diff): conformance 1 (demo script not in ARCHITECTURE, fixed: row plus D-2026-09-19-36); correctness 3, none moving a current number: (a) `wall_time_s` now excludes building the simulation in `run_experiments.py` too, logged as A-2026-09-19-18, accepted 2026-09-20 as D-2026-09-20-2; (b) the runners no longer write their own aggregate CSV with `num_completed` and `wall_time_s` intervals (nothing read them; the per-seed JSONs still carry both); (c) `scalability_benchmark.csv` column `vehicles_generated` was always 0 (it read a key the result never had) and is now the real count, a bug fixed.
- ⏳ Open for Kerem (AGENDA, Open decisions): discretionary lane changes with nothing to gain (about 2.3 per vehicle-km remain after odca-des D-31).

## Session 15 (2026-09-19): scripts on the driver split (odca-des PR #4, N4)
- `plot_car_following.py` (scripted leader is now a `HumanDriver` subclass), `diagnose_fd_capacity.py`, `run_demand_sweep.py`, `visualize.py`, `animate.py`, `run_incident.py` use `Vehicle(env, cfg, driver, ...)`, `HumanDriver`, `vehicle.kind`; outputs byte-identical old against new (demand sweep, ring-road FD, car-following trajectories). No number moved.

## Session 14 (2026-09-19): scripts use the odca-des trait sampler (odca-des PR #3, N3)
- `run_demand_sweep.py` and `diagnose_fd_capacity.py` drop their own copies of the human-driver trait draws and call `TraitSampler(...).driver_config(params)`; same streams in the same order, 2000 draws identical to the old functions. No number moved (golden 24/24 exact in odca-des).

## Session 13 (2026-09-19): configs as YAML, named OD demand, incidents (odca-des PR #2)

- **Code follows odca-des N2** (odca-des D-2026-09-19-23 to -29, inherited here as D-2026-09-19-25 to -28):
  `code/config.py` now only loads `code/configs/simulation.yaml`, which names `network_s1.yaml`,
  `demand_s1.yaml` and the odca package defaults for vehicles and drivers. Every script uses
  `sim_config(**overrides)`; configs are frozen.
- **S1-S4 demand changed** (Kerem, "Keep 6 km S1, spread end lanes"): veh/h per named pair; each
  origin's end-of-segment traffic spread evenly over `end_lane_1..4`, so vehicles cross lanes
  before the end (dissertation 4.1 has per-lane ends A-D). Every S1-S4 number moves: quick golden
  seed 1 S1 lane changes per km 2.09 -> 4.98, delay 29.1 -> 30.6 s. tex:874 (segment end from any
  lane) no longer holds for S1-S4: N11.
- **Incident run** uses `IncidentConfig` (same cells 250-260 on lane 4, 300 s to 1500 s); bottleneck,
  incident and scalability keep the any-lane `end` (odca-des A-2026-09-19-10, accepted 2026-09-20 as
  its D-2026-09-20-7).
- Proof: odca-des pytest 59/59; here 5/5, every script imports, `run.py --quick` and
  `run_incident.py --quick` run.
- ⏳ Manuscript and README still quote pre-fix numbers (N11).
- Next: odca-des N3 to N8, then N9 here.

## Session 12 (2026-09-19): simulator moved to odca-des, bugs fixed, refactor designed

- **odca-des created** (old HANDOVER N1, D-2026-09-19-6 to -10): `code/odca/` moved with its history to `kdemirtas/odca-des` (PR #1 there, merged); this paper depends on it editable (`code/pyproject.toml`, project renamed `paper-odca-des-code` to avoid a uv name clash). The move was byte-identical: golden 24/24 exact from both sides before any fix. The golden now lives in `odca-des/tests/golden/paper_odca_des/`; `code/golden.py` is gone.
- **Simulator bugs fixed in odca-des** (Kerem: "Fix every bug", paper is the spec, D-2026-09-19-16): odca-des D-2026-09-19-11 to -20 and the lane-change rate rule D-2026-09-19-22. Every golden run moved, so every manuscript number is stale: AGENDA WS-11, HANDOVER N11. Manuscript bug found: tex:232 has T_req = T_arr + l/v; Kerem: "immediate request is required (consider freeflow). that is a bug."
- **Paper-side fixes** (D-2026-09-19-21): `run_demand_sweep.py` replaces each exiting vehicle at cell 0 (measured density at k = 0.3 is 0.298 to 0.306); `generate_figures.py` density splits time across bins; `generate_paper_figures.py` speed profile filters on exit after warm-up; `aggregate_multiseed.py` raises on unreadable or duplicate input; `json_default.py` replaces `default=str`; sensitivity runs S1 only. `code/tests/test_result_contracts.py`: 5 pass.
- **Refactor design** (odca-des D-2026-09-19-23, -24): ConfigMixin configs, Driver split from Vehicle. N2 to N8 moved to the odca-des HANDOVER.
- Old HANDOVER block (superseded): RESUME was N1, create odca-des; the 20-seed rerun was stopped at 43/80 S1-S4 and 12/80 bottleneck runs, to run once after the refactor (N11).
- ⏳ README key-results table and the manuscript quote pre-fix numbers until N11.
- ⏳ Human gate still open: Kerem reviews the PDF, best after N11.
- Next: the odca-des refactor (N2), then N9 here.

## Session 11 (2026-09-19): /architect retrofit, code contract written

- **Docs only, no code or result changed.** Added `ARCHITECTURE.md` (boundaries, result-file contracts, core types, invariants, proof), `DECISIONS.md` (12 entries: 5 today, 7 mined from STATUS, AGENDA, CLAUDE.md and git), `HANDOVER.md` (resume pointer, ranked code list N1 to N8), `PROJECT.md`, `BACKLOG.md` (B1 to B6), `CHANGELOG.md` (from git, no PRs before today), empty `ASSUMPTIONS.md`, `IDEAS.md`, `STATUS_ARCHIVE.md`, `sources/SOURCES.md`. `CLAUDE.md` rewritten to the common rules plus this paper's.
- **Kerem's calls:** parameter types move to `odca/params.py` (D-2026-09-19-2); `aggregate_multiseed.py` is the only aggregator (D-2026-09-19-3); named seeds `REPLICATION_SEEDS` 1-20 and `ILLUSTRATIVE_SEED` 42 (D-2026-09-19-4); proof is a committed `--quick` golden fingerprint, exact match (D-2026-09-19-5). `HANDOVER.md` stays beside `STATUS.md`; `~/Papers/CLAUDE.md` updated to allow it (that folder is not a repo).
- **Inventory findings:** driver-parameter sampling copied in 4 files, 95% CI code in 3; seed 42 hard-coded in 7 scripts; `Vehicle.__init__` takes 24 parameters; two diagnostics write figures to `code/output/figures/` while the paper includes hand-copied ones in `figures/`; no tests, no golden record.
- ⏳ `code/output/` and `code/.venv/` absent in this checkout, and no `pyproject.toml` although README says `uv sync`: no paper number can be re-checked until N1.
- ⏳ `paper/paper-odca-des-prerevision.tex` missing (Papers rule); critic reports now in `review/self/` (Session 10 names `paper/`); no `critic_author_response_NN.md` files.
- ⏳ Human gate still open: Kerem reviews `paper/paper-odca-des.pdf` and `paper/revision.diff`. AGENDA workstream statuses still read "not-started" though Sessions 7 to 10 finished them.
- Next: N1 in `HANDOVER.md`.

## Session 10 (2026-04-21) — Revision complete, ready for human gate

- **Phase 5 iteration 2**: critic re-review produced `critic_report_02.md`. Critical: 0. Major: 1 (abstract/conclusion rounded $28 \pm 1.1$ → $28 \pm 2$ overshoot). Minor: 3. Orchestrator applied the fixes directly (4 small edits) rather than dispatching another agent iteration.
- **Phase 7 final compile**: 0 errors, 0 undefined references, 40 pages, 30 MB PDF.
- **Diff artifact**: `paper/revision.diff` — git diff of `paper-odca-des.tex` vs commit 1587642 (2026-03-28 baseline). 334 diff lines; +158/-33 insertions/deletions on the manuscript. latexdiff attempted but hit diff-markup breakage in the expanded Limitations itemize; plain git-diff chosen as cleaner.
- **Files for review**:
  - `paper/paper-odca-des.pdf` — final manuscript, 40 pages
  - `paper/revision.diff` — textual diff vs pre-revision
  - `paper/critic_report_01.md`, `paper/critic_report_02.md` — critic trail

## Session 9 (2026-04-20) — Phase 5 iteration 1: critic fixes applied

Applied all Critical and Major items from `critic_report_01.md`. Fixed fig:travel_time caption (131 s -> 154 s with derivation), added sensitivity N-asymmetry acknowledgment, rounded abstract/conclusion CIs consistently, added BN_0%/BN_30% delay discussion, softened q_max flattening claim to concavity, cited orphan bib entries (Greenshields in FD derivation, Daganzo 2005 in variational theory), added CIs to bare sensitivity numbers, expanded intro contributions to 8 items matching conclusion, added machine specs to Section 5.1, removed clearpage before Conclusion. Applied trivial Minor items: explicit O(n^0.57) exponent, S1 demand clarification, LC paragraph trimming, CV range inline, abstract plateau anchor. Compilation clean: 0 errors, 0 undefined references, 0 missing citations. Next: Phase 5 iteration 2 re-review (critic_report_02) or human gate.

## Session 8 (2026-04-20) — Phase 3 complete (Dispatches 3A + 3B)

Phase 3 manuscript rewrite executed. All single-seed numbers in Section 5 replaced with 20-replication means and 95% CIs. Abstract and conclusion updated to match. New subsections added: Bottleneck Analysis (with plateau-near-50% finding), Sensitivity to HDV Action Interval (S1 only, 3-point curve), Scalability with Network Size. Five new figures integrated. Limitations expanded to 6 items (empirical calibration, network scope, static demand, heterogeneity calibration, sensitivity scope, creeping). Future Work expanded to 7 items mirroring limitations. The "10 replications / seed 42" inconsistency is resolved (now consistently "20 replications, seeds 1-20"). Compilation not yet verified (needs `latexmk -pdf`). Next: compile, then Phase 4 (manuscript-critic).

## Session 7 (2026-04-20 → 2026-04-21) — Phase 1 complete; Phase 2 starting

### Experiments finished
- **WS-1 S1-S4**: 20 seeds complete, `code/output/multiseed/s1_s4/aggregate.csv`.
- **WS-1 bottleneck**: 20 seeds complete, `code/output/multiseed/bottleneck/bottleneck_aggregate.csv`.
- **WS-3 scalability**: 5 cell sizes × 3 seeds complete, `code/output/scalability_benchmark.csv`.
- **WS-2 sensitivity (scope-pivoted)**: S1 only, 10 seeds × {ai=0.5, ai=0.25}, combined with WS-1 at ai=1.0 for a 3-point curve. `code/output/sensitivity_action_interval/comparison.csv`.
  - **Why scope-pivoted**: S2 runs at ai ≤ 0.5 became pathologically slow (event storm) and were additionally starved by an apt system update; stuck for 12h producing no JSONs. Killed, discarded partial S2 data.
  - **Defensibility**: S1 is where HDV action_interval sensitivity matters most (HDV-only scenario). Higher-AV scenarios have proportionally less HDV behavioural influence. Single-scenario sensitivity is standard.

### Key deltas vs old single-seed (for paper-author)
- **S1-S4**: all within ±2.6% of old numbers. Monotonicity preserved. Tight CIs.
- **Bottleneck BN0%**: throughput 1146 → 1341 (+17%). Old single-seed was unrepresentative.
- **Bottleneck 50% vs 70% AV**: means 1772 vs 1780 with large overlapping CIs — **statistically indistinguishable**. New finding: AV benefit in bottleneck plateaus near 50%.
- **Sensitivity (S1)**: lower ai → higher throughput + lower delay, monotonic. Supports the STATUS.md Priority-2 hypothesis that finer-grained HDV decisions close the structural gap vs continuous-time models.
- **Scalability**: near-linear event count in cells; realtime ratio 7.1× (200 cells) to ~1× (3200 cells × 4 lanes = 12,800 total).

### Next
- Phase 2: regenerate figures with error bars + sensitivity + scalability plots.
- Phase 3: paper-author rewrite (results + limitations).
- Phase 4-5: critic → fix loop (max 3 iterations).
- Phase 6: bibliography re-validation.
- Phase 7: final compile + latexdiff + human gate.

## Session 6 (2026-04-20) — research-lead planning

1. Full project state review.
2. Identified inconsistency: §5.3 text claims "10 replications, 95% CIs" but Table 5 caption says "seed 42".
3. Time-varying demand infra absent in `code/odca/` — dropped to Limitations.
4. `AGENDA.md` produced: 7 phases, 3-iteration critic cap, results-drift protocol.

---

## Previous Session (2026-03-28, session 5)

### What Was Done
1. **Disabled DLC for AVs** — centrally controlled AVs now perform mandatory lane changes only (blockage avoidance, destination approach). Rationale: central controller optimizes longitudinal behavior directly; speed-seeking lane changes create merge turbulence in mixed traffic.
   - Added `dlc_enabled` flag to `VehicleParams` (default `True`, `False` for AVs)
   - Guarded `_evaluate_dlc()` in `vehicle.py`
   - Updated `config.py`, `av.py`, `hdv.py`

2. **Resolved AV non-monotonicity in bottleneck** — was Priority 1 item. With DLC disabled:
   - Bottleneck throughput now monotonically improves with AV penetration
   - S1-S4 experiments show stronger, cleaner AV benefits

3. **Re-ran all AV experiments** — bottleneck and S1-S4 with new DLC-disabled AVs
4. **Regenerated all paper figures**
5. **Updated paper text** — abstract, DLC section, AV controller section, parameter table, results table, discussion (all numbers and narrative updated)
6. **Verified all 26 references** against Google Scholar — fixed 2 substantive issues:
   - `fellendorf2010microscopic`: `@techreport` → `@incollection`
   - `banks2014discrete`: year 2014 → 2010 (5th edition publication date)
7. **Updated DLC logistic figure** — panel (b) now shows HDV-only curve with "AV: DLC disabled" annotation

### Results as of 2026-03-28 (single seed 42, superseded)
The tables below are the pre-rerun single-seed record and are kept as history. The current values
are the 20-replication means in `code/output/multiseed/*/aggregate.csv`, printed by
`code/manuscript_numbers.py` and quoted in the manuscript tables; the rerun of 2026-09-20 moved
every one of them (STATUS session 18: S1 throughput 5,874 veh/h, S4 6,983; bottleneck 2,501 at 0%
AV and 3,602 at 70%).

**S1-S4 (4-lane, 800 cells, per-lane OD):**
| Scenario | Throughput | Avg Travel Time | Avg Delay | LCs/km |
|----------|-----------|-----------------|-----------|--------|
| S1 (0%)  | 4,455     | 391s            | 264s      | 4.90   |
| S2 (30%) | 5,374     | 341s            | 212s      | 3.54   |
| S3 (50%) | 6,485     | 255s            | 124s      | 2.27   |
| S4 (70%) | 6,845     | 160s            | 29s       | 1.19   |

All metrics now monotonically improve with AV penetration. LC frequency *decreases* (AVs don't DLC).

**Bottleneck (3-lane, lane drop, 3600 veh/h):**
| AV%  | Throughput | Avg Delay | LCs/km |
|------|-----------|-----------|--------|
| 0%   | 1,146     | 260s      | 1.52   |
| 30%  | 1,526     | 332s      | 1.61   |
| 50%  | 1,860     | 356s      | 1.30   |
| 70%  | 1,779     | 180s      | 0.69   |

Non-monotonicity resolved. 50→70% throughput dip likely noise (single seed).

**Incident (4-lane, 20-min closure, 3000 veh/h) — unchanged (HDV-only):**
- 2,972 veh/h throughput, 310.5s avg delay

### Previous Sessions
- Session 4 (2026-03-27): Seminar slides, slide reordering
- Session 3 (2026-03-26): Pygame visualization, zero-speed deadlock fix
- Session 2 (2026-03-14): Paper draft sent to advisors
- Session 1 (2026-03-12–13): Core framework, OD redesign, LC improvements

## Known Shortcomings

1. ~~**Single-seed results**~~ — closed 2026-04-21: 20 replications, seeds 1-20, with 95% intervals (D-2026-04-20-1, WS-1)
2. **No empirical calibration** — parameters from literature, not calibrated to NGSIM/highD
3. **Static demand only** — constant OD flows, no time-varying demand
4. **Limited network scope** — single unidirectional freeway segment
5. ~~**Computational scalability not demonstrated**~~ — closed 2026-04-21: 5 network sizes x 3 seeds, `code/output/scalability_benchmark.csv` (WS-3)

## TODO — Next Session

This list is the 2026-03-28 plan and is kept as history. What is still open is in `HANDOVER.md`
NEXT and `BACKLOG.md`; what shipped is in the dated entries above.

### Priority 1: Statistical Rigor
1. ~~**Multi-replication runs**~~ — done 2026-04-21 (WS-1), rerun 2026-09-20

### Priority 2: Sensitivity & Robustness
2. ~~**Action_interval sensitivity test**~~ (0.5, 0.25) — done 2026-04-21 on S1 (WS-2, D-2026-04-20-2)
3. **Speed change notification as wake-up trigger** — parked as `BACKLOG.md` B3; odca-des took the other route on 2026-09-20, a limit taking effect on the cell that posts it (its D-2026-09-20-4)

### Priority 3: Paper 3 Preparation
4. **Begin AV platooning paper** — its own repo, `~/Papers/paper-odca-platoon`, with `paper-odca-adaptive-platoon` beside it
5. **V2V cooperative lane changing** — belongs to those two papers, out of scope here

### Backlog
- Rolling time-space diagram animation (not in `BACKLOG.md`)
- Time-varying demand support (`BACKLOG.md` B4)
- Empirical calibration against NGSIM/highD (`BACKLOG.md` B5)

## Completed (cumulative)
- ~~AV non-monotonicity in bottleneck~~ (2026-03-28, disabled DLC for AVs)
- ~~Reference verification~~ (2026-03-28, 26 refs checked, 2 fixed)
- ~~Seminar slides~~ (2026-03-27, `slides/seminar.tex`)
- ~~Pygame interactive visualization~~ (2026-03-26, `code/visualize.py`)
- ~~Zero-speed deadlock~~ (2026-03-26, creep speed fix)

## Awaiting
- Advisor feedback on draft (Dr. Mirchandani, Dr. Zhou)
- Journal target confirmation (TR Part B or alternative)

## Critic report 03 (2026-09-20): post-rerun review

Manuscript reviewed after the N11 rerun restated every number. No Critical items. Three Major: (1) abstract, conclusion and fig:bottleneck_throughput caption say "all" or "the full 3,600" at 50% AV, but the table shows 3,571 (99.2%); body text is precise, the three summaries overstate. (2) Conclusion says "close agreement" with the FD theory without the 92--93% ring-road quantification that Section 5.2 provides. (3) The 131 s demand-weighted free-flow time is named but still not derived or explained. Six Minor: Cassidy (1998) cited for incident recovery hysteresis (Cassidy and Bertini 1999 is the canonical ref), scalability caption omits the 0.86 exponent, S1 label reused for a half-demand experiment, three bib key-year mismatches from report 01, abstract over 200 words, warm-up periods differ without motivation. Verdict: ready-for-fixes.
