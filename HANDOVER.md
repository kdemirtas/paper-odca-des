# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: revision 3, two journal versions, waiting on Kerem (2026-09-20)
- The manuscript is now two files, one per target journal (D-2026-09-20-14):
  `paper/paper-odca-des_trb.tex` (Transportation Research Part B, 45 pages, 198-word abstract) and
  `paper/paper-odca-des_smpt.tex` (Simulation Modelling Practice and Theory, 46 pages, 269 words).
  They differ in six places and nowhere else: the `\journal` line, the abstract opening, the introduction's first paragraph, the
  generality sentences closing the introduction, the generality sentences closing the
  conclusion, and the Future Research bullet on transfer to a second domain.
  `diff` must show six hunks; a seventh means a shared edit landed in one file only. Every other
  edit goes into both in the same change, and both must pass the gate.
- **The novelty claim was narrowed, in both (D-2026-09-20-13).** A DEVS and Cell-DEVS search found
  that contribution 1 as worded described Cell-DEVS: a cellular automaton on a discrete-event
  engine is established since 2001, and ATLAS, the closest prior work, was published in SMPT, the
  journal being recommended. The paper now says so and claims the inversion instead: the cell is a
  passive resource with no transition function, the vehicle is the process. Section 2.3 positions
  against Zeigler, Wainer and ATLAS on three named points. Novelty now reads: no prior work models
  vehicle movement as resource acquisition on a cell lattice, and none derives headway and capacity
  in closed form from the protocol. Five verified references added, bibliography 36/36, no orphans.
- Revision 3 is open. Baseline commit ee64ce8, saved as `paper/paper-odca-des_<journal>-prerevision-3.tex`.
  Diffs: `paper/revision-3-trb.diff` (49 lines), `paper/revision-3-smpt.diff` (105 lines).
- All four marked PDFs rebuilt and clean: `revision-1-marked` (40 pages), `revision-2-marked` (47),
  `revision-3-trb-marked` (45), `revision-3-smpt-marked` (46), each 0 errors, 0 undefined, 0
  overfull over 10 pt. `revision-2-marked` grew by a page because it is now built from the
  committed revision-2 exit state, not from a stale working tree. `make-marked.sh` takes a journal
  suffix and reads revisions 1 and 2 from git.
- No number moved this session: nothing in `code/` ran, no result file was regenerated. Every
  quoted number still traces to `code/output/` through `code/manuscript_numbers.py`, including the
  131 s demand-weighted free-flow trip time.
- The critic/author loop is closed at seven rounds. Round 6 reviewed session 27's new text (1 Major
  on the generality claim, 2 Minor, all applied and answered in
  `review/self/critic_author_response_06.md`); round 7 confirmed all three resolved and returned
  0 Critical, 0 Major, 0 Minor (`review/self/critic_report_07.md`), re-checked here: both files
  build clean, 36 citations against 36 keys, 0 em-dashes, six diff hunks and no seventh. Rounds 1
  to 5 closed clean before them (`review/self/critic_report_05.md`: 0 Critical,
  0 Major, 0 Minor). The model stays first order (odca-des:D-2026-09-20-20); bounded acceleration
  was built, measured and rejected (24.7% of completed trips lost on S1) and Section 4.3 says why.
- `ASSUMPTIONS.md` is empty here and in odca-des. Open and Kerem's alone: the discretionary
  lane-change rate (`AGENDA.md` Open decisions, three measured options in odca-des
  `docs/lane-change-rate.md`), which would need a second rerun.
**RESUME:** four things, all Kerem's. (1) Pick the journal: `AGENDA.md` Open decisions has the
measured table and the SMPT recommendation, and both versions are now written, so the choice is
which file to send, not more work. (2) Read `paper/revision-3-trb-marked.pdf` or
`paper/revision-3-smpt-marked.pdf` (additions underlined blue, deletions struck red) for what
changed this session, with the clean PDFs beside them. (3) Say go on the 124-job rerun (about three
hours, machine quiet) that regenerates the per-seed files so the tables can carry mean cells held
and mean origin wait (odca-des:D-2026-09-20-5) and the two failure counters
(odca-des:D-2026-09-20-12). (4) The discretionary lane-change rate.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/revision-3-<journal>-marked.pdf`; advisor feedback; target journal confirmation.

Ranked. N2 to N10 shipped (N2 to N8 in odca-des).

1. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine, so the tables can quote mean cells held and mean origin wait (odca-des:D-2026-09-20-5). Waiting for Kerem to say go, because it blocks the machine and the timed runs must not share it.
2. ~~**Close the odca-des assumptions**~~: done 2026-09-20, `ASSUMPTIONS.md` there is empty. What remains open is its BACKLOG (B12: whether the lane-change patience timeout is reachable) and the discretionary lane-change rate, which is an `AGENDA.md` decision here, not an assumption row. This repo's rows are all closed: the wall-time definition (D-2026-09-20-2), the numbered revision files (D-2026-09-20-3), the incident scenario (D-2026-09-20-4), the v_f notation (D-2026-09-20-5), the critic round (D-2026-09-20-6), the abstract length (D-2026-09-20-7) and the lane-change parameter justification (D-2026-09-20-8).
3. **A choice on the trajectory figures**: with T_acq now in every record, the time-space diagrams can draw a queued vehicle as a flat wait then a move instead of one smoothed line. It would change `fig:tsd` and the incident figures, so it is Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: undecided between Transportation Research Part B and Simulation Modelling Practice and
  Theory, a version of the manuscript written for each; deadline: none (advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`, `latexdiff` 1.3.2 for the marked builds; build `pdflatex -interaction=nonstopmode <f> && bibtex <f> && pdflatex -interaction=nonstopmode <f> && pdflatex -interaction=nonstopmode <f>` from `paper/` for `<f>` each of `paper-odca-des_trb` and `paper-odca-des_smpt`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 3 complete 2026-09-20 (Cell-DEVS positioning, journal split); `_trb` 45 pages, `_smpt` 46 pages, both clean, waiting for Kerem's review before sending.
