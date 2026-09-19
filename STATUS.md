# STATUS — ODCA-DES Paper

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

### Latest Results (seed 42)

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

1. **Single-seed results** — S1-S4 use seed=42 only; need multi-replication with confidence intervals
2. **No empirical calibration** — parameters from literature, not calibrated to NGSIM/highD
3. **Static demand only** — constant OD flows, no time-varying demand
4. **Limited network scope** — single unidirectional freeway segment
5. **Computational scalability not demonstrated** on larger networks

## TODO — Next Session

### Priority 1: Statistical Rigor
1. **Multi-replication runs** — run S1-S4 and bottleneck with multiple seeds, report means and 95% CIs

### Priority 2: Sensitivity & Robustness
2. **Action_interval sensitivity test** (0.5, 0.25) — test if reducing action interval closes structural gap vs continuous-time models
3. **Speed change notification as wake-up trigger** — interrupt driver when neighboring cell speed_limit changes

### Priority 3: Paper 3 Preparation
4. **Begin AV platooning paper** — design platoon formation/dissolution logic on top of ODCA-DES
5. **V2V cooperative lane changing** — coordinated merging for platoon members

### Backlog
- Rolling time-space diagram animation
- Time-varying demand support
- Empirical calibration against NGSIM/highD

## Completed (cumulative)
- ~~AV non-monotonicity in bottleneck~~ (2026-03-28, disabled DLC for AVs)
- ~~Reference verification~~ (2026-03-28, 26 refs checked, 2 fixed)
- ~~Seminar slides~~ (2026-03-27, `slides/seminar.tex`)
- ~~Pygame interactive visualization~~ (2026-03-26, `code/visualize.py`)
- ~~Zero-speed deadlock~~ (2026-03-26, creep speed fix)

## Awaiting
- Advisor feedback on draft (Dr. Mirchandani, Dr. Zhou)
- Journal target confirmation (TR Part B or alternative)
