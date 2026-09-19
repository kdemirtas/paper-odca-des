# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: running on odca-des; simulator bugs fixed (2026-09-19)
- Manuscript: revision 1 done 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages). Waiting for Kerem's review of `paper/paper-odca-des.pdf` and `paper/revision.diff`.
- Code: the simulator is now `kdemirtas/odca-des` (`~/Papers/odca-des`, PR #1 merged), an editable dependency; `code/odca/` is gone. Its bug fixes and the lane-change rate rule moved every golden run, so every number in the manuscript is stale until N11 (AGENDA WS-11).
- Configs are YAML (`code/configs/`), demand is veh/h per named pair with per-lane ends (D-2026-09-19-25, -26); S1-S4 numbers all moved.
- Paper-side fixes shipped here (D-2026-09-19-21): demand sweep replacement inflow, time-split density heatmap, strict aggregation input, speed profile warm-up filter, S1-only sensitivity runs; `code/tests/` result contracts (5 pass).
**RESUME:** N11: the full rerun is running (`code/output/orchestration.log`); when `ALL PHASE 1 JOBS DONE` appears, regenerate the figures and restate every number from the fresh CSVs. N9 and N10 shipped.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/paper-odca-des.pdf` and `paper/revision.diff`; advisor feedback; target journal confirmation. The PDF review is best done after N11, since every number will change.

Ranked. N2 to N10 shipped (N2 to N8 in odca-des).

1. **N11. Full rerun and manuscript restatement** (D-2026-09-19-5, AGENDA WS-11): 20-seed S1-S4 and bottleneck, S1 sensitivity, scalability, all 12 cores; restate every quoted number from the fresh CSVs; fix tex:232 (immediate request), the event and scalability claims, drop maximum queue length, describe the lane-change rate rule. Then recompile and rerun the critic loop.

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Research Part B; deadline: none (no hard deadline; advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`; build `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 1 complete 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages), waiting for Kerem's review before sending.
