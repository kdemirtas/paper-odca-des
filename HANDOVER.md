# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top entry); shape of the code in `ARCHITECTURE.md`.

## CURRENT: submission-ready for Transportation Engineering, repos public (2026-09-22)
- **Send `paper/paper-odca-des_treng.pdf`** (46 pages) with `paper/highlights_treng.txt`. Three
  files (D-2026-09-20-14, -22-2, -22-3): `_treng` is `_trb` with four differences (journal line,
  `number` class option, the journal's competing-interest template naming Zhou's Associate Editor
  role and recusal, `elsarticle-num-names`); `diff` shows 4 hunks against `_trb`, 9 against
  `_smpt`, 6 between those two. All three clean: 0 errors, 0 undefined, 0 missing citations, 0
  "Author undefined", 0 overfull over 10 pt; 46 / 46 / 47 pages.
- **The Guide for Authors was read in full** (Kerem pasted it, D-2026-09-22-3). Every required
  item is in: generative-AI declaration (Kerem's wording, all three files), funding sentence,
  CRediT, data statement in the present tense citing `odca-des` as software reference 37 of 37,
  numbered references in TRENG, Highlights. Item 2 "Open Science Article" is an article type, not
  a waiver; single paper, no companion.
- Review closed at ten critic rounds (round 9 the full pre-submission read, round 10 confirming
  0/0/0) plus two humanizer passes; nothing that writes prose has run since except the guide's
  required sections. Marked sets and diffs current for all three journals.
- Repos `kdemirtas/odca-des` (tag `v0.1.0`, MIT) and `kdemirtas/paper-odca-des` public as of this
  session on Kerem's word; the data statement is true as written.
- ⏳ **Unverified, worth up to USD 2,310:** the APC waiver Zhou described. It is in neither the
  guide nor Elsevier's written policy. Get it in writing before submitting.
**RESUME:** Kerem submits. Before the portal: (1) mint a Zenodo DOI for `odca-des` v0.1.0 and one
for the paper repo, then add them to the data statement and to `demirtas2026odcades` in
`references.bib` and `references-marked.bib` (one line each, all three files, rebuild, `diff`
counts 4 / 9 / 6); (2) the waiver in writing. At the portal: the editor declaration under "Other
Activities" in the declarations tool, inform the journal before completing submission, upload
`highlights_treng.txt`, the .tex sources and figure PDFs, decide on the free SSRN preprint. After
submission, `/putdown` records the sent version as a version heading in `CHANGELOG.md`.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): the Zenodo DOIs, the waiver, the submission.

Ranked.

1. **DOIs into the manuscript** once minted: the one-line edits above, then the build gate and the
   marked sets for all three.
2. **After submission**: the `CHANGELOG.md` version heading; keep `_trb` and `_smpt` in step with
   any change a referee asks for.
3. **The rerun that carries the new columns**: 124 jobs, about three hours on a quiet machine
   (odca-des:D-2026-09-20-5). Settle the discretionary lane-change rate first (AGENDA Open
   decisions) or it runs twice. A referee request is the likely trigger now.
4. **The trajectory figures**: flat wait then move, or one smoothed line; Kerem's call.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, public); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Engineering (Elsevier, gold OA, single-anonymized review, D-2026-09-22-2); TR-B and SMPT versions kept. Deadline: none.
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst for `_trb` and `_smpt`, elsarticle-num-names.bst for `_treng`)`, `latexdiff` 1.3.2; build `pdflatex -interaction=nonstopmode <f> && bibtex <f> && pdflatex -interaction=nonstopmode <f> && pdflatex -interaction=nonstopmode <f>` from `paper/` for `<f>` each of `paper-odca-des_treng`, `_trb`, `_smpt`; also check `grep -c "Author undefined" <f>.log` is 0. Marked pair and diff: `./make-marked.sh 3 <journal>`. Humanizer apply: `python3 apply_rewrites.py ../review/self/humanizer_report_NN.md [--write]`.
- Agents (global, `~/.claude-personal/agents/`): `research-lead`, `paper-author`, `manuscript-critic`, `manuscript-humanizer`, `bibliography`; `TEAM.md` there holds the pipeline order.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/`; `data/` and `code/output/` gitignored.
- Manuscript state: submission-ready 2026-09-22 for Transportation Engineering; waiting on Zenodo DOIs and the waiver confirmation, then Kerem sends.
