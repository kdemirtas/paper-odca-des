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
| B6 | Switch `paper-lc-logistic`, `paper-odca-platoon`, `paper-odca-adaptive-platoon` onto `odca-des`: bring their additions (`lc_events`, `platoon/`, engine changes) into the package off by default, add their goldens, and recheck their numbers, which will move (creep fix D-2026-03-26-1, `dlc_enabled` D-2026-03-28-1) | D-2026-09-19-6: one central package; their copies are frozen until then | N1 has created odca-des (then each paper's own task, in its own repo) | 2026-09-19 |
| B8 | Replace the 25 em-dashes in `paper/paper-odca-des.tex` | the house rule is no em-dashes, colon, comma, parentheses or split the sentence; the manuscript predates it being applied to the .tex, so they sit in the body text (lines 62, 66, 71, 81, 88, 131, 185, 256, 291, 373, 410, 412, 417 and on) | after Kerem's read of revision 2, so the 25 edits do not land in the diff he is reading | 2026-09-20 |
| ~~B7~~ | ~~Decide whether the model should bound acceleration~~ | closed 2026-09-20 the day it was raised: built, measured and rejected, odca-des:D-2026-09-20-20. The model stays first order. Section 4.3 now says so, so a referee reads the answer rather than asking the question | closed | 2026-09-20 |
