# BACKLOG: paper-odca-des

Parked ideas and decisions, not committed work. One entry each: what, why, and the trigger that
promotes it to HANDOVER's NEXT list. Committed and ordered work lives in `HANDOVER.md`; what was
decided lives in `DECISIONS.md`; what shipped lives in `CHANGELOG.md`. Promotion is Kerem's call
at `/pickup`, which lists the entries whose trigger is now true.

| # | what | why | trigger | parked |
|---|---|---|---|---|
| B1 | Route `run_demand_sweep.py` through `Simulation` (density-initialised and ring-road starts in the engine) | it bypasses the engine with its own placement and inflow code (helpers with 10 to 12 parameters) | the engine next gains an initial-condition feature, or a sweep result is questioned | 2026-09-19 |
| B2 | Capacity invariant test: ring road at critical density gives 2127 veh/h within a tolerance | offered in the proof question on 2026-09-19, not chosen; invariant 2 is checked by eye only | N1 has run and shows the current measured value | 2026-09-19 |
| B3 | Wake the driver when a neighbouring cell's speed limit changes | STATUS Priority 2 item 3; today only the driver's own cell change interrupts it | a scenario with variable speed limits is planned | 2026-03-28 |
| B4 | Time-varying demand | dropped to Limitations (AGENDA WS-4) | a reviewer or advisor asks for it | 2026-04-20 |
| B5 | Empirical calibration against NGSIM or highD | out of scope, in Limitations | a reviewer or advisor asks for it | 2026-04-20 |
| B6 | Carry the core refactors (N2, N6, N7) into the other three ODCA repos | the repos copy `code/odca/`, no submodule | N2, N6 or N7 lands here | 2026-09-19 |
