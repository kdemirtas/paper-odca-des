# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: running on odca-des; simulator bugs fixed (2026-09-19)
- Manuscript: revision 1 done 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages). Waiting for Kerem's review of `paper/paper-odca-des.pdf` and `paper/revision.diff`.
- Code: the simulator is now `kdemirtas/odca-des` (`~/Papers/odca-des`, PR #1 merged), an editable dependency; `code/odca/` is gone. Its bug fixes and the lane-change rate rule moved every golden run, so every number in the manuscript is stale until N11 (AGENDA WS-11).
- Configs are YAML (`code/configs/`), demand is veh/h per named pair with per-lane ends (D-2026-09-19-25, -26); S1-S4 numbers all moved.
- Paper-side fixes shipped here (D-2026-09-19-21): demand sweep replacement inflow, time-split density heatmap, strict aggregation input, speed profile warm-up filter, S1-only sensitivity runs; `code/tests/` result contracts (5 pass).
**RESUME:** N11 is done: the rerun is in `code/output/` and every quoted number is restated. Next is Kerem's read of `paper/paper-odca-des.pdf` with `paper/revision-2.diff`, and the open assumptions (`ASSUMPTIONS.md`), the incident scenario and the DLC rate among them.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/paper-odca-des.pdf` and `paper/revision.diff`; advisor feedback; target journal confirmation. The PDF review is best done after N11, since every number will change.

Ranked. N2 to N10 shipped (N2 to N8 in odca-des).

1. **Critic loop on the restated manuscript**: `manuscript-critic` on `paper/paper-odca-des.tex` as it now stands, then `paper-author` answers. N11 (the rerun and the restatement) shipped 2026-09-20; the numbers, the incident scenario and the capacity discussion all changed, so the last critic round (2026-04-21) no longer covers the text.
2. **Close the open assumptions** with `/next-assumption`: the incident demand and closure (A-2026-09-20-2), the revision-2 file names (A-2026-09-20-1) and the odca-des rows. The wall-time definition closed 2026-09-20 as D-2026-09-20-2.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Research Part B; deadline: none (no hard deadline; advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`; build `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 1 complete 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages), waiting for Kerem's review before sending.
