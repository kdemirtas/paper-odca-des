# CLAUDE.md: paper-odca-des

Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata: journal
manuscript from Kerem's ASU dissertation. Type `paper`. Target journal undecided between Transportation Research Part B and Simulation Modelling Practice and Theory, a version written for each (D-2026-09-20-14); `AGENDA.md`
Open decisions holds the comparison and the recommendation.

Read `HANDOVER.md` first, then the top of `STATUS.md`, then `ARCHITECTURE.md` before touching
code. `AGENDA.md` is the manuscript plan (owned by `research-lead`); `CONTEXT.md` holds the
paper's identity, parameters and notation.

Doc set: HANDOVER, STATUS (+ STATUS_ARCHIVE), AGENDA, PROJECT, ARCHITECTURE, DECISIONS,
CHANGELOG, BACKLOG, CONTEXT, sources/SOURCES.md. The code map, contracts and invariants are in
`ARCHITECTURE.md`; HDV defaults and notation in `CONTEXT.md`.

## Rules
- **Structure before code.** A new module, a moved boundary, or a changed contract or core type
  goes through `/architect` first and cites its `D-` id in the commit.
- **Code is the source of truth.** A doc that disagrees with the code is a defect in the doc unless
  `DECISIONS.md` says the code is wrong.
- **No history in code.** Comments say what the code does now; why lives in `DECISIONS.md`.
- **No switch without a decision.** A new flag or mode names the `D-` id that needs it.
- **Types, not tuples.** Pass `SimConfig`, the driver and vehicle configs and the other Core types whole; configs are frozen, change them with `dataclasses.replace`. A
  function over 6 parameters is a review finding.
- **Prove neutrality with the golden fingerprint** (`uv run pytest` in `~/Papers/odca-des`,
  D-2026-09-19-8). During the refactor only the quick golden runs; it may be re-recorded, with
  the moved values stated. "It runs" is not a proof.
- **Numbers come from `code/output/`.** Every number in the abstract, body, tables and conclusion
  is read from the aggregate CSVs before it is written; a regenerated result re-checks every place
  it is quoted, in the same change.
- **Seeds are named** in `config.py`: `REPLICATION_SEEDS` for tables, `ILLUSTRATIVE_SEED` for
  single-run figures (D-2026-09-19-4). A seed change is a decision.
- **numpy RNG only, never `import random`.** One `SeedSequence` stream per source; a new stream is
  spawned last, or every number moves.
- **Units:** cells (7.5 m, `CELL_LENGTH_M`), cells/s, seconds inside `odca/`; km/h and veh/h only
  when reporting. Notation shared across ODCA papers: k, v, tau, m, l.
- **Environment:** `uv`, venv at `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
  `code/output/`, `data/`, `*.csv` are gitignored. Figures land in `figures/`, never in `code/`.
- **Build:** pdflatex, bibtex, pdflatex, pdflatex from `paper/` with `-interaction=nonstopmode`,
  on both journal files; done means 0 errors, 0 undefined references, 0 missing citations, no
  overfull hbox over 10 pt, in each of them.
- **Bibliography through the bib skills only.** No invented, orphan or uncited entries.
- **Critic loop is bounded:** `review/self/critic_report_NN.md`, answered in
  `critic_author_response_NN.md`; stop when no Critical or Major item remains.
- **Humanization closes a revision** (D-2026-09-22-1): after the critic loop closes,
  `manuscript-humanizer` writes `review/self/humanizer_report_NN.md` over both journal files,
  Kerem marks findings `accepted`, `paper/apply_rewrites.py --write` applies them to both at once
  (it refuses any old text that is not unique in each, and prints the hunk count afterwards), and
  the critic takes a confirming round on the changed sentences only. Nothing that writes prose
  runs after it in the same revision.
- **One manuscript file per target journal** (D-2026-09-20-14): `paper/paper-odca-des_trb.tex`
  for Transportation Research Part B and `paper/paper-odca-des_smpt.tex` for Simulation Modelling
  Practice and Theory. They differ in six places and nowhere else: the `\journal` line, the abstract opening, the introduction's first paragraph, the
  generality sentences closing the introduction, the generality sentences closing the
  conclusion, and the Future Research bullet on transfer to a second domain.
  Every other edit goes into both files in the same change, and both pass the gate before anything
  ships. `diff paper-odca-des_trb.tex paper-odca-des_smpt.tex` must show six hunks; a seventh means
  a shared edit landed in one file only. A third journal is a third file with a new suffix, never
  a branch.
- **Revisions keep their baseline, one numbered set each** (D-2026-09-20-3, D-2026-09-20-11,
  D-2026-09-20-14): revision N saves its entry state as
  `paper/paper-odca-des_<journal>-prerevision-N.tex` before, and ends with
  `paper/revision-N-<journal>.diff` and the change-marked pair `paper/revision-N-<journal>-marked.tex`
  and `.pdf`, one set per journal file. The highest N is the current one. An earlier revision's
  files are never overwritten, so a revision Kerem has not read yet stays readable in the working
  tree. The marked PDF is what he reads, the diff is the machine-readable record. Build it with
  `./make-marked.sh N <journal>` from `paper/`: it carries the four measures a marked build needs
  (`--exclude-textcmd="textbf"`, tables shrunk to the text width, inline math allowed to break,
  `\sloppy` for latexdiff's `\mbox`ed citations) and holds the marked build to the manuscript's own
  gate. Marked builds cite `paper/references-marked.bib`, references plus the entries later
  revisions dropped, never `references.bib`. Revisions 1 and 2 predate the journal split and keep
  their unsuffixed names; `make-marked.sh` reads their exit states from git (commit 1587642 for
  revision 1's baseline, ee64ce8 for revision 2's exit state), and revision 1 has
  `paper/revision.diff` and no baseline file.
- **The simulator is the shared package `odca-des`** (`~/Papers/odca-des`, import `odca`, editable
  path dependency, D-2026-09-19-6 to -9). Fix bugs and add capabilities there, never in a local copy;
  this paper's golden is a test there. This repo has no `code/odca/` any more.
- **Never submit, never add yourself as co-author.** Kerem sends the paper.
- One plain name per thing, descriptive snake_case. No em-dashes anywhere.

## Environment
Repo `kdemirtas/paper-odca-des` (private). Push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
Session account: `pclaude`.
