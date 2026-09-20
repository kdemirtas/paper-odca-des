# ODCA-DES paper: Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata (journal manuscript from Kerem's dissertation)
> **Last updated 2026-09-20.** Read this first; `STATUS.md` says where things stand, `ARCHITECTURE.md`
> says how the code is shaped, `DECISIONS.md` says what was decided and why.

## Overview
Journal version of the ODCA-DES chapter of Kerem's ASU dissertation. Target journal undecided between Transportation Research Part B and Simulation Modelling Practice and Theory, a version written for each (D-2026-09-20-14). ODCA-DES keeps the cell grid of cellular automata but moves vehicles by discrete events: each cell is a capacity-1 SimPy resource released tau seconds after its vehicle leaves, which reproduces Newell car-following headways, and each HDV driver re-evaluates on its own schedule or when a neighbour moves. Experiments: S1-S4 mixed traffic (0/30/50/70% AV), a lane-drop bottleneck, a temporary incident, fundamental-diagram sweeps, action-interval sensitivity and a scalability benchmark. Identity, authors and notation: `CONTEXT.md`. Manuscript plan: `AGENDA.md`.

## What "done" means
Kerem declares the manuscript submission-ready: 0 Critical and 0 Major critic items, a clean build of every journal file (0 errors, 0 undefined references, 0 missing citations, no overfull hbox over 10 pt, in each), every quoted number traced to a file in `code/output/`, and the code reproduces those files from `README.md`. Kerem submits; the docs never do.

## Design decisions
See `DECISIONS.md` (dated ids). The ones that shape results: AVs make no discretionary lane changes (D-2026-03-28-1); 20 replications with 95% t-intervals (D-2026-04-20-1); sensitivity on S1 only (D-2026-04-20-2).

## Out of scope
Empirical calibration, time-varying demand, networks beyond one freeway segment, AV platooning (its own paper, `paper-odca-platoon`).

Parameters and notation: `CONTEXT.md`.

## Phases
1. Advisor draft (done 2026-03-14). 2. Revision 1 (done 2026-04-21). 3. Code retrofit (2026-09-19 to 2026-09-20; `HANDOVER.md` N2 to N10 shipped, N2 to N8 of them in odca-des). 4. Revision 2 (done 2026-09-20, the post-rerun restatement). 5. Revision 3 (done 2026-09-20: the Cell-DEVS positioning and the split into one file per journal, D-2026-09-20-13 and -14). 6. Submission (Kerem), waiting on his journal choice and his read of the marked PDFs.

Detail of phases 1, 2, 4 and 5 is in `STATUS.md` and `AGENDA.md`; phase 3 is the ranked list in `HANDOVER.md`.
