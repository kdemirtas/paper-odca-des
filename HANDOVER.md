# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: critic round 3 applied, parameter justification written, assumptions walked (2026-09-20)
- Manuscript: revision 2 (the post-rerun restatement) plus critic round 3 applied in full, 3 Major
  and 6 Minor, answered in `review/self/critic_author_response_03.md`. Build 42 pages, 0 errors,
  0 undefined references, 0 missing citations, no overfull box. The abstract is now 198 words.
- Every quoted number comes from `code/output/` through `code/manuscript_numbers.py`, which also
  derives the 131 s demand-weighted free-flow trip time (130.9 s against 153.8 s full segment).
- Notation: the manuscript now separates v_max (vehicle), v_lim (cell) and v_f = min of the two,
  and delay is the per-cell excess over v_f (D-2026-09-20-5 here, D-2026-09-20-3 in odca-des).
  No number moved: every cell in every scenario posts 5.2 cells/s.
- Section 3.4.2 now justifies the lane-change parameters rather than only defining the conversion:
  both exposure references are one free-flow driver-second, so k, r_0, k_d and Delta v_0 state the
  chance of acting at one ordinary decision (D-2026-09-20-8). Table 3 gained the two reference rows
  and its "Perception delay" row became "Action interval (max. re-evaluation gap)", delta_eval.
  Text only: 42 pages, 0 errors, 0 undefined references, no overfull box, no number moved.
- `ASSUMPTIONS.md` is empty; 6 rows remain open in odca-des (seven closed there 2026-09-20, its
  D-2026-09-20-6 to -12, PR #16). The last of those split `lc_failures` into `lc_patience_failures`
  and `gap_rejections` at Kerem's word: nothing here moves until the rerun regenerates the result
  files, and the manuscript quotes no failure count.
**RESUME:** Kerem's read of `paper/paper-odca-des.pdf` against `paper/revision-2.diff`. Then the
one piece of work waiting on a decision: a 124-job rerun (about three hours, machine quiet) that
regenerates the per-seed files so the tables can carry the two new columns odca-des D-2026-09-20-5
added, mean cells held and mean origin wait. Offered and not started.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/paper-odca-des.pdf` against `paper/revision-2.diff`; advisor feedback; target journal confirmation.

Ranked. N2 to N10 shipped (N2 to N8 in odca-des).

1. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine, so the tables can quote mean cells held and mean origin wait (odca-des D-2026-09-20-5). Waiting for Kerem to say go, because it blocks the machine and the timed runs must not share it.
2. **Close the odca-des assumptions** with `/next-assumption` there (6 rows left, the discretionary lane-change rate among them). This repo's rows are all closed: the wall-time definition (D-2026-09-20-2), the numbered revision files (D-2026-09-20-3), the incident scenario (D-2026-09-20-4), the v_f notation (D-2026-09-20-5), the critic round (D-2026-09-20-6), the abstract length (D-2026-09-20-7) and the lane-change parameter justification (D-2026-09-20-8).
3. **A choice on the trajectory figures**: with T_acq now in every record, the time-space diagrams can draw a queued vehicle as a flat wait then a move instead of one smoothed line. It would change `fig:tsd` and the incident figures, so it is Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Research Part B; deadline: none (no hard deadline; advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`; build `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 2 complete 2026-09-20 (critic round 3 applied: 0 Critical, 3 Major, 6 Minor, all answered; 42 pages), waiting for Kerem's review before sending.
