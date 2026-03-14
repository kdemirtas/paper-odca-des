# HANDOFF — ODCA-DES Paper Session State

## Last Session (2026-03-14)

### What Was Done
1. **OD matrix redesign** — per-lane mainline origins with destination distributions (Option B)
2. **All experiments re-run** with new OD (S1-S4, bottleneck, incident)
3. **Bottleneck scenario fixed** — block-before-seed, Edie's FD, demand reduced to 3600 veh/h
4. **Heatmap NaN fix** — no-data bins show white, zero speed shows color
5. **Paper updated** — Tables 3 & 5, discussion paragraphs, conclusion numbers
6. **All figures regenerated** — publication-quality

### Latest Results (seed 42)

**S1-S4 (4-lane, 800 cells, per-lane OD):**
| Scenario | Throughput | Avg Speed | Avg Delay | LCs/km |
|----------|-----------|-----------|-----------|--------|
| S1 (0%)  | 4,419     | 393 km/h  | 266s      | 4.96   |
| S2 (30%) | 4,905     | 356 km/h  | 229s      | 6.76   |
| S3 (50%) | 5,515     | 335 km/h  | 206s      | 8.07   |
| S4 (70%) | 6,531     | 242 km/h  | 111s      | 8.34   |

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

## TODO — Next Session

### Priority 1: Investigate & Fix
1. **AV non-monotonicity in bottleneck** (30-50% worse than 0%) — likely AV DLC params (dlc_cooldown=3s, dlc_v0=0.4) creating merge turbulence
2. **Vehicles stuck at zero speed** for long durations (visible in trajectory plots)
3. **Speed change notification as wake-up trigger** — interrupt driver when neighboring cell speed_limit changes

### Priority 2: Sensitivity & Robustness
4. **Action_interval sensitivity test** (0.5, 0.25) — test if reducing action interval closes structural gap
5. **Multi-replication runs** for confidence intervals (current: single seed=42)

### Backlog
- Pygame real-time interactive visualization
- Rolling time-space diagram animation

## Key Files Modified
- `code/config.py` — ODFlow with destination distributions
- `code/odca/simulation/generator.py` — `_sample_destination()` from distribution
- `code/odca/simulation/engine.py` — blocked cell skip in `seed_vehicles()`
- `code/run_bottleneck.py` — Edie's FD, block-before-seed, 3600 veh/h
- `code/run_incident.py` — new ODFlow format
- `code/generate_figures.py` — NaN heatmap fix, bottleneck FD from Edie data
- `paper/main.tex` — updated tables, discussion, conclusion
