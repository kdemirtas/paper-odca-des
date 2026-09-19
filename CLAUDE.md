# CLAUDE.md: paper-odca-des

Discrete Event Traffic Simulation Framework using Object-Driven Cellular Automata: TR Part B
manuscript from Kerem's ASU dissertation. Type `paper`.

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
- **Build:** pdflatex, bibtex, pdflatex, pdflatex from `paper/` with `-interaction=nonstopmode`;
  done means 0 errors, 0 undefined references, 0 missing citations, no overfull hbox over 10 pt.
- **Bibliography through the bib skills only.** No invented, orphan or uncited entries.
- **Critic loop is bounded:** `review/self/critic_report_NN.md`, answered in
  `critic_author_response_NN.md`; stop when no Critical or Major item remains.
- **Revisions keep their baseline:** `paper/paper-odca-des-prerevision.tex` before, `paper/revision.diff` after.
- **The simulator is the shared package `odca-des`** (`~/Papers/odca-des`, import `odca`, editable
  path dependency, D-2026-09-19-6 to -9). Fix bugs and add capabilities there, never in a local copy;
  this paper's golden is a test there. This repo has no `code/odca/` any more.
- **Never submit, never add yourself as co-author.** Kerem sends the paper.
- One plain name per thing, descriptive snake_case. No em-dashes anywhere.

## Environment
Repo `kdemirtas/paper-odca-des` (private). Push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
Session account: `pclaude`.
