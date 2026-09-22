# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top entry); shape of the code in `ARCHITECTURE.md`.

## CURRENT: revision 3 humanized, pre-submission critic round 9 in flight (2026-09-22)
- Two manuscript files, one per target journal (D-2026-09-20-14): `paper/paper-odca-des_trb.tex`
  (Transportation Research Part B, 45 pages) and `paper/paper-odca-des_smpt.tex` (Simulation
  Modelling Practice and Theory, 46 pages). They differ in six places and nowhere else;
  `diff` must show six hunks, a seventh means a shared edit landed in one file only.
- Novelty claim narrowed (D-2026-09-20-13): the inversion of Cell-DEVS (passive cell, vehicle
  as process), positioned against Zeigler, Wainer and ATLAS in Section 2.3. Bibliography 36/36.
- **The review flow gained a fifth agent and a terminal pass (D-2026-09-22-1).** After the critic
  loop closes, `manuscript-humanizer` (Sonnet, read-only) reports machine-written phrasings with
  a rewrite each into `review/self/humanizer_report_NN.md`; Kerem marks findings `accepted`;
  `paper/apply_rewrites.py --write <report>` applies them to both files (refuses non-unique old
  text, prints the hunk count); the critic takes a confirming round. Nothing that writes prose
  runs after the humanizer in a revision. Rule in `~/Papers/CLAUDE.md` for all five papers.
- Revision 3 went through it: critic rounds 1 to 7 closed (0/0/0), humanizer report 01 found 6
  (1 Tier A, 5 Tier B), all accepted and applied, critic round 8 confirmed none moved a claim
  (0/0/0). Both files clean: 0 errors, 0 undefined, 0 missing citations, 0 overfull over 10 pt.
- Marked sets current: `revision-3-trb-marked.pdf` (45 pages) and `revision-3-smpt-marked.pdf`
  (46), each clean; `revision-3-trb.diff` 148 lines, `revision-3-smpt.diff` 200. `make-marked.sh`
  now regenerates the `.diff` too. Baseline commit ee64ce8, saved as
  `paper/paper-odca-des_<journal>-prerevision-3.tex`.
- Zero em-dashes in both files, including TikZ comments (seven Unicode ones were there; session
  28's "zero" had looked for `---`). No number moved this session: nothing in `code/` ran.
- **Kerem: "one more e2e round of self review and I will submit."** Critic round 9, a full
  pre-submission read of both files with `manuscript_numbers.py` checking every quoted number,
  is running; its report is `review/self/critic_report_09.md` when it lands. A Critical or
  Major finding reopens the revision at `paper-author`, and the humanizer runs again at the end.
- `ASSUMPTIONS.md` is empty here and in odca-des.
**RESUME:** read `review/self/critic_report_09.md`. Clean: the paper is submission-ready and the
only remaining call is the journal (`AGENDA.md` Open decisions, SMPT recommended, both files
written; the choice is which file to send). Not clean: apply through `paper-author`, then
humanizer, then a confirming critic round, then `./make-marked.sh 3 <journal>` for both. Also
still Kerem's: the discretionary lane-change rate, the 124-job rerun, the trajectory figures.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): the journal; his read of `paper/revision-3-<journal>-marked.pdf`.

Ranked.

1. **Critic round 9 outcome** (above): apply if anything is Critical or Major, through the full flow.
2. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine, so
   the tables can quote mean cells held and mean origin wait (odca-des:D-2026-09-20-5). Waiting
   for Kerem to say go, because it blocks the machine and the timed runs must not share it.
   Settle the discretionary lane-change rate first (AGENDA Open decisions, three measured options)
   or the rerun happens twice.
3. **A choice on the trajectory figures**: with T_acq in every record, the time-space diagrams can
   draw a queued vehicle as a flat wait then a move instead of one smoothed line. Changes
   `fig:tsd` and the incident figures, so it is Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: undecided between Transportation Research Part B and Simulation Modelling Practice and
  Theory, a version of the manuscript written for each; deadline: none (advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`, `latexdiff` 1.3.2 for the marked builds; build `pdflatex -interaction=nonstopmode <f> && bibtex <f> && pdflatex -interaction=nonstopmode <f> && pdflatex -interaction=nonstopmode <f>` from `paper/` for `<f>` each of `paper-odca-des_trb` and `paper-odca-des_smpt`. Marked pair and diff: `./make-marked.sh N <journal>`. Humanizer apply: `python3 apply_rewrites.py ../review/self/humanizer_report_NN.md [--write]`.
- Agents (global, `~/.claude-personal/agents/`): `research-lead`, `paper-author`, `manuscript-critic`, `manuscript-humanizer`, `bibliography`; `TEAM.md` there holds the pipeline order.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 3 humanized 2026-09-22 (six wording edits, critic round 8 clean); `_trb` 45 pages, `_smpt` 46 pages, both clean; pre-submission critic round 9 in flight, then Kerem sends.
