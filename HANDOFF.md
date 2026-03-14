# HANDOFF — ODCA-DES Paper Session State

## Last Session (2026-03-14, session 2)

### What Was Done
1. **MLC + DLC logistic probability figures** — created combined side-by-side plot (fig_lc_logistic.pdf) with interpretive text after the lane-change formulas in Section 3.6.2
2. **Theoretical FD figures combined** — merged homogeneous FD and mixed-traffic AV penetration into single 2-panel figure (fig_fd_theoretical panels a+b, theory section)
3. **FD validation figure redesigned** — 2x2 grid: ODCA-DES full/zoomed (top), NaSch full/zoomed (bottom), all with theoretical overlay
4. **Time-space diagrams combined** — free-flow and congested into single side-by-side figure (fig_tsd_combined.pdf)
5. **Network diagram fixed** — lanes now clearly shown as bands between lines (solid edges, dashed dividers), no margin overflow
6. **Notation cleanup** — vehicle index v→i, speed stays v, lanes j, cells c throughout
7. **Zhou affiliation fixed** — SSEBE at ASU (not SCAI)
8. **Lane 1 exit references fixed** — updated for per-lane OD redesign
9. **All figures and tables cited** with interpretive text
10. **Margins set to 2cm** — paper reduced from 49 to 33 pages
11. **Draft-mode commands removed** — \todo{}, \note{} definitions and commented-out algorithm packages
12. **Repository restructured** — figures/ at project root, code outputs to ../figures/, empty dirs removed
13. **Git repo initialized** — pushed to github.com/kdemirtas/paper-odca-des (private)
14. **CONTEXT.md created** — project structure and conventions documented
15. **Draft sent to advisors** for review (Dr. Mirchandani and Dr. Zhou)

### Paper Status
- 33 pages, clean compile (no warnings, no undefined references)
- 7 figures (all combined/optimized), 7 tables
- All artifacts cited with interpretation
- Targeting Transportation Research Part B

### Latest Results (seed 42, unchanged from previous session)

**S1-S4 (4-lane, 800 cells, per-lane OD):**
| Scenario | Throughput | Avg Travel Time | Avg Delay | LCs/km |
|----------|-----------|-----------------|-----------|--------|
| S1 (0%)  | 4,419     | 393s            | 266s      | 4.96   |
| S2 (30%) | 4,905     | 356s            | 229s      | 6.76   |
| S3 (50%) | 5,515     | 335s            | 206s      | 8.07   |
| S4 (70%) | 6,531     | 242s            | 111s      | 8.34   |

**Bottleneck (3-lane, lane drop, 3600 veh/h):**
| AV%  | Throughput | Avg Delay |
|------|-----------|-----------|
| 0%   | 1,174     | 262s      |
| 30%  | 1,065     | 574s      |
| 50%  | 1,022     | 674s      |
| 70%  | 1,566     | 606s      |

Non-monotonic at 30-50% AV — mixed-traffic coordination friction at merge. 70% surpasses baseline by 33%.

**Incident (4-lane, 20-min closure, 3000 veh/h):**
- 2,972 veh/h throughput, 310.5s avg delay, 151s wall time

## Known Shortcomings (shared with advisors)

1. **No empirical calibration or validation** — parameters from literature, not calibrated to NGSIM/highD
2. **Single-seed results** — S1-S4 use seed=42 only; need multi-replication with confidence intervals
3. **Static demand only** — constant OD flows, no time-varying demand
4. **Limited network scope** — single unidirectional freeway segment
5. **Computational scalability not demonstrated** on larger networks
6. **Simplistic AV model** — AVs differ only in parameter values, no cooperative behaviors

## TODO — Next Session

### Priority 1: Simulation Methodology Improvements
1. **Multi-replication runs** — run S1-S4 with multiple seeds, report means and 95% CIs
2. **AV non-monotonicity in bottleneck** (30-50% worse than 0%) — investigate DLC params creating merge turbulence
3. **Vehicles stuck at zero speed** — diagnose and fix long-duration stops visible in trajectory plots
4. **Speed change notification as wake-up trigger** — interrupt driver when neighboring cell speed_limit changes

### Priority 2: Sensitivity & Robustness
5. **Action_interval sensitivity test** (0.5, 0.25) — test if reducing action interval closes structural gap
6. **Empirical calibration** — calibrate parameters against NGSIM or highD trajectory data

### Priority 3: Paper 3 Preparation
7. **Begin AV platooning paper** — design platoon formation/dissolution logic on top of ODCA-DES
8. **V2V cooperative lane changing** — coordinated merging for platoon members

### Backlog
- Pygame real-time interactive visualization
- Rolling time-space diagram animation
- Time-varying demand support

## Awaiting
- Advisor feedback on draft (Dr. Mirchandani, Dr. Zhou)
- Journal target confirmation (TR Part B or alternative)
