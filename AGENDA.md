# Research agenda -- paper-odca-des

**Last updated:** 2026-09-20
**Target venue / deadline:** Transportation Research Part B (no hard deadline; advisor feedback not yet received)
**One-line thesis:** ODCA-DES combines the spatial simplicity of cellular automata with discrete-event asynchronous dynamics, producing smooth fundamental diagrams and realistic mixed-traffic congestion without synchronous updates or integer speeds.

> **Execution note:** The orchestrator (main Claude session or human) executes all dispatches below. The research-lead agent produced this plan but does not spawn agents or run experiments itself.

## Contributions (current best articulation)
1. A novel simulation paradigm merging CA spatial structure with DES asynchronous event-driven mechanics.
2. A resource-based movement protocol whose delayed-release mechanism reproduces Newell's car-following headways analytically.
3. An event-driven driver process that concentrates computation where interactions occur.
4. Closed-form capacity expressions linking resource protocol parameters to macroscopic traffic quantities under mixed AV/HDV traffic.

## Current state (2026-09-20)
- Manuscript is 1337 lines, 42 pages, revision 2 plus critic round 3 applied (STATUS session 19); every section drafted.
- 28 figure PDFs in `figures/`; every number restated from `code/output/` after the 124-job rerun of 2026-09-20 (STATUS session 18).
- The "10 replications / seed 42" inconsistency is resolved: 20 replications, seeds 1-20 throughout (STATUS session 8).
- Known shortcomings that remain (Limitations, 6 items): no empirical calibration, static demand only, limited network scope, sensitivity on S1 only, heterogeneity calibration, creeping. Single-seed results and undemonstrated scalability are closed (WS-1, WS-3).
- References: 31 entries in `paper/references.bib`, validated 2026-03-28 (2 fixed), re-validated in revision 1 (`sources/SOURCES.md`); the bib items raised in critic rounds 01 and 03 are fixed (STATUS session 19).

## Results drift protocol

When new multi-seed or sensitivity results differ from the current single-seed numbers, `paper-author` must:
1. Replace all affected numeric values, tables, and figure references with the new data.
2. If a qualitative claim no longer holds (e.g., monotonicity breaks, improvement percentages change direction), rewrite the surrounding narrative to match the new evidence. Do not hedge or soften -- state what the data shows.
3. If a result that was previously noise (e.g., the 50-to-70% bottleneck throughput dip) is confirmed across seeds, treat it as a real finding and discuss possible mechanisms.
4. Do not escalate to the human for results-driven text changes -- the user has pre-authorized all such rewrites.
5. Update the abstract's numeric claims to match the body.

---

## Workstreams

### WS-1: Multi-replication experiments
- **Status:** done 2026-04-21 (20 seeds, S1-S4 and bottleneck; STATUS session 7), rerun 2026-09-20 with the fixed simulator (124 jobs, STATUS session 18)
- **Owner:** orchestrator (Bash)
- **Goal:** Run S1-S4 and bottleneck with 20 seeds each; output JSON with per-seed and aggregate (mean, std, 95% CI) results.
- **Next action:** Modify `run_experiments.py` and `run_bottleneck.py` to accept a seed list, loop over seeds, and write aggregate statistics. Then execute.

### WS-2: Action-interval sensitivity
- **Status:** done 2026-04-21, scope-pivoted to S1 only, 10 seeds at 0.5 and 0.25 plus WS-1 at 1.0 (D-2026-04-20-2; STATUS session 7), rerun 2026-09-20
- **Owner:** orchestrator (Bash)
- **Goal:** Run S1-S4 and bottleneck at action_interval values {1.0 (current default), 0.5, 0.25} with 20 seeds each. Output comparison tables.
- **Next action:** Parameterize action_interval in the run scripts; execute the sweep.

### WS-3: Computational scalability benchmark
- **Status:** done 2026-04-21 (5 network sizes x 3 seeds, `code/output/scalability_benchmark.csv`; STATUS session 7), re-measured 2026-09-20 (STATUS session 18)
- **Owner:** orchestrator (Bash)
- **Goal:** Measure wall-clock time vs. network size (varying cell count and/or lane count). Produce a scalability table or figure.
- **Next action:** Write a small benchmark script that runs the simulation at several network sizes and records wall-clock per sim-second.

### WS-4: Time-varying demand assessment
- **Status:** done (decision made)
- **Outcome:** No time-varying demand infrastructure exists in `code/odca/` (confirmed by code search). Building it is new infra. Per scope rules, this drops to Limitations section.

### WS-5: Manuscript rewrite (results + narrative)
- **Status:** done 2026-04-20 (Section 5 rewritten on the 20-replication data; STATUS session 8), restated again 2026-09-20 after the rerun (STATUS session 18)
- **Owner:** paper-author
- **Goal:** Rewrite Section 5 (Computational Experiments) with new multi-seed data, sensitivity results, and scalability benchmark. Update abstract, conclusion, and any forward references. Fix the "10 replications" / "seed 42" inconsistency.
- **Depends on:** WS-1, WS-2, WS-3

### WS-6: Limitations / Future Work expansion
- **Status:** done 2026-04-20 (Limitations 6 items, Future Work 7 items; STATUS session 8)
- **Owner:** paper-author
- **Goal:** Expand Limitations (Section 6.1) to honestly acknowledge: (a) no empirical calibration against NGSIM/highD, (b) limited network scope, (c) static demand only (time-varying dropped to limitations). Expand Future Research (Section 6.2) accordingly.
- **Parallel with:** WS-5 (different subsections, no label conflicts)

### WS-7: Critic review
- **Status:** done; three rounds, `review/self/critic_report_01.md` (2026-04-20), `_02.md` (2026-04-21), `_03.md` (2026-09-20)
- **Owner:** manuscript-critic
- **Goal:** Produce a structured fix list covering correctness, completeness, presentation, and internal consistency.
- **Depends on:** WS-5 and WS-6 complete

### WS-8: Fix loop (bounded)
- **Status:** done 2026-09-20; round 3 left 0 Critical, and its 3 Major and 6 Minor items are applied and answered in `review/self/critic_author_response_03.md` (STATUS session 19)
- **Owner:** paper-author (fixes) then manuscript-critic (re-review)
- **Goal:** Address all items from the critic report. Maximum 3 iterations of critic-then-fix. If unresolved items remain after 3 rounds, the orchestrator surfaces them to the human.
- **Depends on:** WS-7

### WS-9: Bibliography re-validation
- **Status:** done; validated 2026-03-28 (26 entries, 2 fixed), re-validated in revision 1 (`sources/SOURCES.md`), bib items from critic rounds 01 and 03 fixed 2026-09-20
- **Owner:** bibliography
- **Goal:** Confirm all references in `references.bib` are correct (titles, years, venues, DOIs). Check for any new citations added during WS-5/WS-6 that need validation.
- **Parallel with:** WS-8 (non-overlapping files: `.bib` vs `.tex`)

### WS-10: Final compile and PDF check
- **Status:** done 2026-04-21 (40 pages, `paper/revision.diff`; STATUS session 10) and again 2026-09-20 (42 pages, 0 errors, 0 undefined references, 0 missing citations, no overfull box, `paper/revision-2.diff`). The human gate stays open
- **Owner:** orchestrator (Bash) then human gate
- **Goal:** Clean `latexmk` build, no warnings, no undefined references, no overfull hboxes. Produce final PDF + diff against pre-revision version.
- **Depends on:** WS-8 and WS-9 complete

### WS-11: Restate the paper after the odca-des bug fixes (opened 2026-09-19)
- **Status:** done 2026-09-20 (rerun of 124 jobs, 0 failed; every number restated; STATUS session 18)
- **Owner:** orchestrator (full rerun, HANDOVER N11) then paper-author
- **Goal:** Every quoted number moves: the simulator bugs fixed on 2026-09-19 (odca-des D-2026-09-19-11 to -20) and the lane-change rate rule (odca-des D-2026-09-19-22) changed all golden runs, and so did the one-request-one-lane-change fix (odca-des DECISIONS.md, entry 31 of 2026-09-19). Rerun, then restate abstract, tables, body and conclusion from the fresh CSVs. Manuscript fixes found on the way: tex:232 says T_req = T_arr + l/v, the request is immediate (D-2026-09-19-16); the metric definitions at tex:874, 973 to 978 now match the code; the event and scalability claims (tex:1157, 1183, 1197) use the SimPy event count (S1 seed 1 about 2.25M, the old counter summed about 57k); drop the maximum queue length; describe the MLC per distance, DLC per second rule in the lane-changing section.
- **Depends on:** HANDOVER N11

---

## Dispatch plan (in execution order)

### Phase 1: Experiments (WS-1 + WS-2 + WS-3, parallel)

#### Dispatch 1A -- orchestrator: Bash -- Multi-replication runs
- **Goal:** Run S1-S4 and bottleneck experiments with 20 seeds (1-20), collect per-seed metrics, compute aggregate statistics (mean, std, 95% CI).
- **Why now:** Everything downstream depends on real multi-seed data.
- **Prompt outline:**
  - Read `code/run_experiments.py`, `code/run_bottleneck.py`, `code/config.py`.
  - Modify scripts to accept a `--seeds` argument (list of ints) and loop, accumulating results.
  - Run with seeds 1..20 for all four S1-S4 scenarios and all four bottleneck AV scenarios.
  - Save per-seed JSON to `code/output/multiseed/` and an aggregate summary CSV with columns: scenario, metric, mean, std, ci95_lo, ci95_hi.
  - Do NOT change the simulation logic, vehicle parameters, or network config.
- **Acceptance:** `code/output/multiseed/` contains per-seed JSONs and a summary CSV. Spot-check: S1 mean throughput is within 10% of the single-seed value (4455).
- **Parallel-safe?** Yes -- can run alongside 1B and 1C (different output dirs, no file overlap).

#### Dispatch 1B -- orchestrator: Bash -- Action-interval sensitivity
- **Goal:** Run S1-S4 and bottleneck at HDV action_interval = {1.0, 0.5, 0.25} with 20 seeds each.
- **Why now:** Sensitivity analysis is independent of the baseline multi-seed runs.
- **Prompt outline:**
  - Read `code/config.py` (line 57: `action_interval=1.0`), `code/run_experiments.py`, `code/run_bottleneck.py`.
  - For each action_interval value, override `HDV_PARAMS.action_interval` before running scenarios.
  - Save results to `code/output/sensitivity_action_interval/` with subdirs per value.
  - Produce a comparison CSV: scenario x action_interval x metric (mean, CI).
  - The AV action_interval (0.5s) stays fixed -- only HDV varies.
- **Acceptance:** Comparison CSV exists and shows results for all 3 action_interval values x 4 scenarios x 4 bottleneck scenarios.
- **Parallel-safe?** Yes -- separate output directory.

#### Dispatch 1C -- orchestrator: Bash -- Scalability benchmark
- **Goal:** Measure wall-clock runtime vs. network size to demonstrate computational scalability.
- **Why now:** Independent of other experiments; can run concurrently.
- **Prompt outline:**
  - Read `code/config.py` (NetworkConfig), `code/run_experiments.py`.
  - Create `code/run_scalability.py` that runs the S1 (0% AV) scenario at network sizes: {200, 400, 800, 1600, 3200} cells, 4 lanes, for 1800s sim-time, 3 seeds each.
  - Record: num_cells, num_lanes, total_cells, vehicles_generated, total_events, wall_clock_seconds, sim_seconds, realtime_ratio.
  - Save to `code/output/scalability_benchmark.csv`.
- **Acceptance:** CSV exists with 5 network sizes x 3 seeds = 15 rows. Wall-clock increases sub-quadratically with cell count (expected from event locality).
- **Parallel-safe?** Yes -- separate script and output.

### Phase 2: Figure regeneration (after Phase 1)

#### Dispatch 2 -- orchestrator: Bash -- Regenerate figures
- **Goal:** Regenerate all paper figures using the new multi-seed data. Add new figures: (a) error bars / CIs on throughput and delay bar charts, (b) sensitivity comparison plot, (c) scalability plot.
- **Why now:** Figures must use the new data before the manuscript rewrite.
- **Prompt outline:**
  - Read `code/generate_figures.py`, `code/generate_paper_figures.py`.
  - Modify figure generation to read from `code/output/multiseed/` aggregate data.
  - Add error bars (95% CI) to `fig_throughput_bar.pdf` and `fig_travel_time.pdf`.
  - Create `fig_sensitivity_action_interval.pdf` (grouped bar or line chart comparing metrics across action_interval values).
  - Create `fig_scalability.pdf` (wall-clock vs. network size, log-log or semi-log).
  - Regenerate `fig_bottleneck_throughput.pdf` with CI error bars.
  - Output all figures to `figures/`.
- **Acceptance:** New/updated PDFs exist in `figures/`. Visual spot-check: error bars visible on bar charts.
- **Parallel-safe?** No -- must follow Phase 1.

### Phase 3: Manuscript rewrite (WS-5 + WS-6, parallel-safe)

#### Dispatch 3A -- paper-author -- Rewrite results sections
- **Goal:** Rewrite Sections 5.3 (Mixed Traffic Scenarios), 5.4 (Computational Performance), and add new subsections for action-interval sensitivity and scalability. Update abstract and conclusion numeric claims.
- **Why now:** New data and figures are ready.
- **Prompt outline:**
  - Read the full manuscript: `/home/kdemirtas/Academic/Papers/paper-odca-des/paper/paper-odca-des.tex`.
  - Read aggregate results: `code/output/multiseed/summary.csv`, `code/output/sensitivity_action_interval/comparison.csv`, `code/output/scalability_benchmark.csv`.
  - Read new figures in `figures/`.
  - **Apply the results drift protocol** (see above). All numeric claims must match the new multi-seed means. Replace "seed 42" caption with proper "N=20 replications" language. Add 95% CI to all reported metrics.
  - Fix the inconsistency at line 965 vs line 984: either both say 20 replications (preferred) or reconcile.
  - Add a new subsection "Sensitivity to Action Interval" in Section 5 presenting the action_interval results.
  - Expand Section 5.4 (Computational Performance) with the scalability benchmark data and figure.
  - Update abstract (line 46-51): replace "54% throughput improvement and 89% delay reduction" with actual multi-seed means.
  - Update conclusion (line 1128): same numeric updates.
  - Add `\includegraphics` for any new figures; add citations if needed (flag them for bibliography).
  - Out of scope: do not touch Sections 1-4 (theory), do not touch references.bib.
  - **Report contract:** After editing, list every numeric value changed and every new subsection/figure added.
- **Acceptance:** All tables show means +/- CIs. No remaining "seed 42" references. Abstract and conclusion numbers match body.
- **Parallel-safe?** Yes with 3B (3A edits Sections 5 and abstract/conclusion; 3B edits Section 6.1-6.2 only).

#### Dispatch 3B -- paper-author -- Expand Limitations / Future Work
- **Goal:** Rewrite Section 6.1 (Limitations) and Section 6.2 (Future Research Directions) to add: (a) no empirical calibration against NGSIM/highD, (b) single freeway scope, (c) time-varying demand not supported (dropped from experiments to limitations).
- **Why now:** Can run in parallel with 3A since it touches different sections.
- **Prompt outline:**
  - Read `/home/kdemirtas/Academic/Papers/paper-odca-des/paper/paper-odca-des.tex`, lines 1132-1162.
  - The current Limitations already mention items (a)-(d). Strengthen them:
    - Empirical calibration: note that parameters are literature-derived, not fitted to NGSIM/highD trajectory data. Future validation would require matching simulated and observed FDs at specific sites.
    - Network scope: single unidirectional segment. No merge/diverge junctions, no route choice.
    - Time-varying demand: all experiments use constant OD flows. The framework's event-driven architecture is compatible with time-varying demand in principle, but the current implementation does not support it.
  - Keep existing limitations (creeping behavior, heterogeneity calibration).
  - Out of scope: do not touch Sections 1-5, do not touch references.bib.
  - **Report contract:** List every added/modified bullet point.
- **Acceptance:** Limitations section has at least 6 items. Time-varying demand is explicitly noted.
- **Parallel-safe?** Yes with 3A.

### Phase 4: Critic review (WS-7)

#### Dispatch 4 -- manuscript-critic -- Full manuscript review
- **Goal:** Produce a structured fix list covering: (a) internal numeric consistency (do tables match text match abstract?), (b) figure references and captions, (c) statistical reporting (CIs present everywhere?), (d) logical flow and missing argumentation, (e) formatting for TR Part B.
- **Why now:** The rewrite is settled; this is the quality gate.
- **Prompt outline:**
  - Read the full manuscript: `/home/kdemirtas/Academic/Papers/paper-odca-des/paper/paper-odca-des.tex`.
  - Read `references.bib`.
  - Read the results data files to cross-check reported numbers.
  - Produce `paper/critic_report_01.md` with sections: Critical (must-fix), Major (should-fix), Minor (nice-to-fix), Formatting.
  - Each item: location (section/line), issue, suggested fix.
  - Out of scope: do not edit the manuscript. Read-only.
- **Acceptance:** Report exists and every item has a clear location and actionable fix.
- **Parallel-safe?** No -- must see the settled draft.

### Phase 5: Fix loop (WS-8, max 3 iterations)

#### Dispatch 5 -- paper-author then manuscript-critic -- Bounded fix loop
- **Iteration protocol:**
  1. `paper-author` reads the latest `critic_report_NN.md` and fixes all Critical and Major items. Produces a changelog.
  2. `manuscript-critic` re-reviews, producing `critic_report_NN+1.md`.
  3. If no Critical or Major items remain, exit the loop.
  4. If Critical/Major items persist after 3 iterations, the orchestrator surfaces the remaining items to the human for a decision.
- **Cap:** 3 iterations maximum.
- **Prompt outline for paper-author (each iteration):**
  - Read `paper/critic_report_NN.md`.
  - Read `paper/paper-odca-des.tex`.
  - Address every Critical item and every Major item. Minor items: fix if trivial, skip if subjective.
  - Do not introduce new content beyond what the critic requested.
  - **Report contract:** For each critic item, state: fixed (with diff summary) or deferred (with reason).
- **Prompt outline for manuscript-critic (each re-review):**
  - Same as Dispatch 4, but also check whether prior Critical/Major items are resolved.
  - Produce `critic_report_NN+1.md`.
- **Acceptance:** Zero Critical and zero Major items in the final critic report.
- **Parallel-safe?** No -- strictly serial (author then critic).

### Phase 6: Bibliography validation (WS-9, parallel with Phase 5)

#### Dispatch 6 -- bibliography -- Reference re-validation
- **Goal:** Validate all entries in `references.bib` against authoritative sources. Check for any new citations added during Phases 3-5.
- **Why now:** Can run alongside the fix loop since it only touches `.bib`, not `.tex`.
- **Prompt outline:**
  - Read `/home/kdemirtas/Academic/Papers/paper-odca-des/paper/references.bib`.
  - For each entry: verify title, authors, year, venue/journal, DOI/URL against Semantic Scholar or CrossRef.
  - Flag: (a) entries not cited in the `.tex`, (b) citations in `.tex` with no `.bib` entry, (c) incorrect metadata.
  - Produce a validation report. Fix any errors directly in `references.bib`.
  - Last validation was 2026-03-28 (26 refs, 2 fixed). Focus on anything added since then.
- **Acceptance:** Every `.bib` entry matches its authoritative source. No orphan citations.
- **Parallel-safe?** Yes with Phase 5 (`.bib` vs `.tex`).

### Phase 7: Final compile and human gate (WS-10)

#### Dispatch 7 -- orchestrator: Bash -- Final compile
- **Goal:** Clean build of the manuscript. Produce final PDF and a latexdiff against the pre-revision version.
- **Why now:** Everything is done; this is the last mechanical step.
- **Prompt outline:**
  - `cd /home/kdemirtas/Academic/Papers/paper-odca-des/paper/`
  - Save a copy of the current tex as `paper-odca-des-prerevision.tex` (if not already saved -- check git).
  - Run `latexmk -pdf paper-odca-des.tex`. Verify: zero errors, zero undefined references, zero missing citations.
  - Check for overfull hbox warnings > 10pt; fix if trivial.
  - Run `latexdiff paper-odca-des-prerevision.tex paper-odca-des.tex > paper-odca-des-diff.tex && latexmk -pdf paper-odca-des-diff.tex` to produce a visual diff PDF.
  - Commit the final state.
- **Acceptance:** `paper-odca-des.pdf` and `paper-odca-des-diff.pdf` both compile cleanly.
- **Parallel-safe?** No -- must be last.

#### Human gate
- The user reviews the final PDF and the diff PDF.
- If approved, the revision is complete.
- If changes requested, re-enter Phase 5 (fix loop).

---

## Open decisions (need human input)
- **Investigation: discretionary lane changes with nothing to gain (opened 2026-09-19).** After the one-request-one-lane-change fix (odca-des DECISIONS.md, entry 31 of 2026-09-19) S1 still makes about 2.3 lane changes per vehicle-km, about 45% of them away from the lane the vehicle needs: the DLC curve gives 0.047 per second at zero speed advantage, and the MLC then brings the vehicle back. Measured options in odca-des `docs/lane-change-rate.md`: no DLC away from a lane an MLC needs (S1 1.49 per vehicle-km), DLC only toward a faster lane (1.94), both (1.23). Each changes the model the paper describes (Eq. dlc_logistic), so Kerem decides. The N11 rerun went ahead without this call on 2026-09-20 (STATUS session 18), so changing the rule now means a second full rerun of the 124 jobs, not a cheaper one. Evidence plot: `figures/demo_trajectories.pdf` panel (b).
- **Target journal (opened 2026-09-20, researched, needs Kerem's call).** The header still says Transportation Research Part B. Kerem asked which venue maximises acceptance probability and minimises time to decision while keeping a respectable index. Measured, from LetPub journal profiles and Elsevier journal insights, September 2026:

| Journal | CiteScore | Quartile | Articles/yr | Peer review | Competitiveness | Fit |
|---|---|---|---|---|---|---|
| Transportation Research Part B | 10.7 | Q1, 10/66 Transportation | 131 | about 6.3 months | high | best: 9 of this paper's 24 references |
| Transportation Research Part C | 15.4 | Q1 | 393 | about 12 months | high | good, simulation and computation welcome |
| IEEE T-ITS | 17.8 | Q1 | 1,400 | about 3 months | very difficult | moderate, an ITS rather than a traffic-theory venue |
| Simulation Modelling Practice and Theory | 9.9 | Q1, 27/128 CS Software Eng | 158 | about 3 months | easy | strong: it is a simulation-methodology journal and this is a simulation framework |
| Physica A | 6.7 | Q2 Physics, Q1 Statistics | 753 | about 7.3 months | easy | good: the CA traffic literature's own lineage |
| Transportmetrica B | 6.1 (IF 3.4) | Q2 | quarterly | not published | moderate | good |

  **Recommendation: Simulation Modelling Practice and Theory**, with Transportation Research Part C as the aspirational alternative and Physica A as the fallback. On Kerem's three criteria it is the only one that wins all three: a CiteScore of 9.9 against TR-B's 10.7, so the index barely moves; about 3 months of review against TR-B's 6.3; and a competitiveness LetPub rates easy against TR-B's 131 slots a year. The scope match is the real argument: this paper's contribution is a simulation paradigm (discrete-event mechanics on a cellular automaton), which is that journal's subject, whereas at TR-B it competes against traffic-flow theory papers on their own ground.

  The cost, stated plainly: audience. Transport researchers read TR-B and TR-C; a paradigm paper in SMPT reaches simulation and computer-science readers instead, and the three ODCA papers that follow would cite it from outside their own literature. The second cost is emphasis: an SMPT referee asks what is new as simulation methodology, where DES and CA hybrids already exist, so the framing would need to lead with the resource protocol and the event-driven driver rather than with the capacity expression.
- Otherwise none. The user has pre-authorized all results-driven text changes and scope decisions. The only gate is the final PDF review.

## Parked / deprioritized
- **Time-varying demand experiments:** dropped to Limitations. No infrastructure exists in `code/odca/`; building it is new feature work, out of scope for this revision.
- **Paper 3 (AV platooning):** separate project, explicitly out of scope.
- **Empirical calibration study:** out of scope; acknowledged in Limitations.
- **Speed-change notification wake-up trigger (STATUS.md Priority 2 item 3):** a code improvement, not needed for this paper revision.
- **Advisor feedback:** not received; revision proceeds without it.

## Not-dispatching-because
- **knowledge-builder:** No new domain sources are needed. The literature review is complete and the experimental scope is fixed.
- **lecture-outline / lecture-tex:** Not a lecture project.
