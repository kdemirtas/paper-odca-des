# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: manuscript waiting on Kerem's read, now as a change-marked PDF (2026-09-20)
- Manuscript: revision 2 (the post-rerun restatement), critic round 3 applied in full and answered
  in `review/self/critic_author_response_03.md`, then two text additions on top: the v_f notation
  (D-2026-09-20-5), the lane-change parameter justification in Section 3.4.2 with the two new
  Table 3 rows (D-2026-09-20-8), and the paradigm figure `fig:paradigm` in Section 4.3
  (D-2026-09-20-9). Floats no longer cross a section boundary, so nothing prints after the
  references any more (D-2026-09-20-10). Build 44 pages, 0 errors, 0 undefined references, 0
  missing citations, no overfull box. Abstract 198 words. No number moved in any of it.
- Every quoted number comes from `code/output/` through `code/manuscript_numbers.py`, including the
  131 s demand-weighted free-flow trip time (130.9 s against 153.8 s for the full segment).
- `ASSUMPTIONS.md` is empty here and in odca-des: its thirteen rows were walked with Kerem on
  2026-09-20 and closed as odca-des:D-2026-09-20-6 to -18 (PRs #16 and #17 there). The one change he
  asked for, `lc_failures` split into `lc_patience_failures` and `gap_rejections`, changes nothing
  here until the rerun regenerates the result files; the manuscript quotes no failure count.
- The model stays first order (odca-des:D-2026-09-20-20): a vehicle acceleration bound was built,
  measured and rejected on 2026-09-20, and Section 4.3 now says why, so B7 is closed. With the
  deceleration half in it cost 24.7% of completed trips on S1. No result file moved.
- `fig:paradigm` now runs the platoon through a posted speed-limit zone (D-2026-09-20-12): it
  accelerates, slows at 21 cells posted at 2 cells/s, accelerates again, and each follower repeats
  the move. The NaSch panel needed a per-cell limit in the baseline, added as odca-des:D-2026-09-20-19
  with `tests/test_nasch.py`. Every quoted number in the paragraph and caption was re-read from the
  run. Open and parked as B7: neither model bounds acceleration, which the figure now makes visible.
- Every revision now also ships a change-marked PDF (D-2026-09-20-11), built by `paper/make-marked.sh N`:
  `paper/revision-1-marked.pdf` (40 pages) and `paper/revision-2-marked.pdf` (46 pages), both held to
  the manuscript's gate. The rule is in `CLAUDE.md` here and in `~/Papers/CLAUDE.md`; the marked
  builds cite `paper/references-marked.bib`, never the manuscript's `references.bib`.
- Open and Kerem's alone: the discretionary lane-change rate (`AGENDA.md` Open decisions, three
  measured options in odca-des `docs/lane-change-rate.md`), which would need a second rerun.
**RESUME:** Kerem's read of `paper/revision-2-marked.pdf` (46 pages, additions underlined blue,
deletions struck red), with `paper/paper-odca-des.pdf` for the clean text. Then the
one piece of work waiting on a decision: a 124-job rerun (about three hours, machine quiet) that
regenerates the per-seed files, so the tables can carry mean cells held and mean origin wait
(odca-des:D-2026-09-20-5) and the two failure counters (odca-des:D-2026-09-20-12). Offered, not started.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/revision-2-marked.pdf`; advisor feedback; target journal confirmation.

Ranked. N2 to N10 shipped (N2 to N8 in odca-des).

1. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine, so the tables can quote mean cells held and mean origin wait (odca-des:D-2026-09-20-5). Waiting for Kerem to say go, because it blocks the machine and the timed runs must not share it.
2. ~~**Close the odca-des assumptions**~~: done 2026-09-20, `ASSUMPTIONS.md` there is empty. What remains open is its BACKLOG (B12: whether the lane-change patience timeout is reachable) and the discretionary lane-change rate, which is an `AGENDA.md` decision here, not an assumption row. This repo's rows are all closed: the wall-time definition (D-2026-09-20-2), the numbered revision files (D-2026-09-20-3), the incident scenario (D-2026-09-20-4), the v_f notation (D-2026-09-20-5), the critic round (D-2026-09-20-6), the abstract length (D-2026-09-20-7) and the lane-change parameter justification (D-2026-09-20-8).
3. **A choice on the trajectory figures**: with T_acq now in every record, the time-space diagrams can draw a queued vehicle as a flat wait then a move instead of one smoothed line. It would change `fig:tsd` and the incident figures, so it is Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Research Part B; deadline: none (no hard deadline; advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`, `latexdiff` 1.3.2 for the marked builds; build `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 2 complete 2026-09-20 (critic round 3 applied: 0 Critical, 3 Major, 6 Minor, all answered), plus the three text additions of sessions 20 and 21; 44 pages, waiting for Kerem's review before sending.
