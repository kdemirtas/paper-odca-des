# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top entry); shape of the code in `ARCHITECTURE.md`.

## CURRENT: submission-ready, target Transportation Engineering (2026-09-22)
- **Three manuscript files** (D-2026-09-20-14, D-2026-09-22-2). The one to send is
  `paper/paper-odca-des_treng.tex` (Transportation Engineering, 45 pages). `_trb` (TR-B, 45) and
  `_smpt` (SMPT, 47) are kept beside it. `_treng` is `_trb` with two differences, the `\journal`
  line and the competing-interest declaration naming Zhou's Associate Editor role and recusal;
  `diff` must show 2 hunks against `_trb`, 7 against `_smpt`, and `_trb` against `_smpt` 6.
- **Review closed, ten critic rounds.** Round 9 was the full pre-submission read Kerem asked for
  (every number matched to `manuscript_numbers.py`, 36/36 citations, zero em-dashes, zero TODOs):
  0 Critical, 2 Major (no competing-interest declaration, no data statement), applied with a CRediT
  block added; humanizer pass 02 on the new text found nothing; round 10 confirmed 0/0/0, "the
  paper can be sent". Acknowledgments deliberately absent. All three files clean: 0 errors, 0
  undefined, 0 missing citations, 0 overfull over 10 pt.
- Marked sets current for all three (`revision-3-<journal>-marked.pdf`, 46/46/47 pages, clean) with
  their `.diff`s; `make-marked.sh` writes the diff now. Novelty claim as narrowed in D-2026-09-20-13.
- The review flow has five agents (D-2026-09-22-1): critic loop, then `manuscript-humanizer`
  (advisory, Kerem accepts), `paper/apply_rewrites.py --write`, a confirming critic round. Nothing
  that writes prose runs after the humanizer in a revision.
- ⏳ **Unverified and worth USD 2,310:** the APC waiver for "open science components" that Zhou
  described. Elsevier's written policy does not list it; ScienceDirect blocked every fetch. Confirm
  in writing, and learn whether it needs the code public at submission (today's statement says on
  acceptance, both repos private).
- No number moved since the N11 rerun; `ASSUMPTIONS.md` empty here and in odca-des.
**RESUME:** Kerem submits `paper/paper-odca-des_treng.pdf` to Transportation Engineering, after
(1) confirming the APC waiver and its conditions with Zhou in writing, and switching the data
statement to present tense and making `kdemirtas/odca-des` and `kdemirtas/paper-odca-des` public
if the waiver needs open code at submission (a one-line edit in all three files, then rebuild);
(2) confirming Zhou's exact editorial title in the declaration. Then `/putdown` records the
submission as a version in `CHANGELOG.md`. Still Kerem's afterwards: the discretionary lane-change
rate, the 124-job rerun, the trajectory figures.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): the two confirmations above, then the submission.

Ranked.

1. **After submission**: record the sent version in `CHANGELOG.md` as a version heading; keep
   the `_trb` and `_smpt` files in step with any change a referee asks for.
2. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine, so
   the tables can quote mean cells held and mean origin wait (odca-des:D-2026-09-20-5). Blocks the
   machine; settle the discretionary lane-change rate first (AGENDA Open decisions, three measured
   options) or the rerun happens twice. A referee request is the likely trigger now.
3. **A choice on the trajectory figures**: with T_acq in every record, the time-space diagrams can
   draw a queued vehicle as a flat wait then a move instead of one smoothed line. Changes
   `fig:tsd` and the incident figures, so it is Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Engineering (Elsevier, gold OA, D-2026-09-22-2); TR-B and SMPT versions kept. Deadline: none.
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`, `latexdiff` 1.3.2 for the marked builds; build `pdflatex -interaction=nonstopmode <f> && bibtex <f> && pdflatex -interaction=nonstopmode <f> && pdflatex -interaction=nonstopmode <f>` from `paper/` for `<f>` each of `paper-odca-des_treng`, `_trb`, `_smpt`. Marked pair and diff: `./make-marked.sh 3 <journal>`. Humanizer apply: `python3 apply_rewrites.py ../review/self/humanizer_report_NN.md [--write]`.
- Agents (global, `~/.claude-personal/agents/`): `research-lead`, `paper-author`, `manuscript-critic`, `manuscript-humanizer`, `bibliography`; `TEAM.md` there holds the pipeline order.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: submission-ready 2026-09-22 (critic round 10 clean, declarations in); `_treng` 45 pages, `_trb` 45, `_smpt` 47, all clean; Kerem sends after the two confirmations.
