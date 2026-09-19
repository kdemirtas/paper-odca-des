# HANDOVER: ODCA-DES paper
Type: paper
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: /architect retrofit (2026-09-19)
- Manuscript: revision 1 done 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages). Waiting for Kerem's review of `paper/paper-odca-des.pdf` and `paper/revision.diff`.
- Code: `/architect` retrofit 2026-09-19 wrote `ARCHITECTURE.md` and `DECISIONS.md`. `code/output/` is not in this checkout and there is no `pyproject.toml`, so no paper number can be re-checked until N1 runs.
- This paper predates the 2026-09-18 doc set: `AGENDA.md` (research-lead) stays as the manuscript plan, and this file holds the code task list.
**RESUME:** N1, rebuild the baseline: add `code/pyproject.toml`, regenerate `code/output/`, confirm the paper's numbers reproduce, record `code/golden/fingerprint.json` (D-2026-09-19-5). Kerem's review of the PDF is his own step and runs in parallel.

## NEXT STEPS (pick up here)
Waiting on Kerem (not a `/next-task` item): review `paper/paper-odca-des.pdf` and `paper/revision.diff`; advisor feedback; target journal confirmation.

Code items, ranked by what would ship wrong first. Each is behaviour-neutral and proven by the golden fingerprint (exact match) unless it says otherwise.

1. **N1. Rebuild the baseline** (D-2026-09-19-5). Add `code/pyproject.toml` + `uv.lock` (simpy, numpy, matplotlib, pygame) so the README's `uv sync` works. Regenerate `code/output/` (`run_all_phase1.sh`, `aggregate_multiseed.py`, the single-run scripts), compare every quoted number in the manuscript with the fresh CSVs: none may move, a move is a finding for `AGENDA.md`. Then write the golden script and commit `code/golden/fingerprint.json` (S1-S4 and bottleneck, `--quick`, seeds 1-3, stats and counters). Cost: the full Phase 1 ran for hours in April.
2. **N2. One driver-heterogeneity sampler** in `odca/entity/`, used by `generator.py`, `engine.seed_vehicles`, `run_demand_sweep.py`, `diagnose_fd_capacity.py` (invariant 4). Same draw order. Also fixes the stale "each vehicle gets its own RNG" docstrings in `rng.py` and `vehicle.py`. Proof: golden exact, sweep JSON identical.
3. **N3. `aggregate_multiseed.py` is the only aggregator** (D-2026-09-19-3). Delete the aggregate CSV writers and the two t-table copies in `run_experiments.py` and `run_bottleneck.py`. Proof: the contract CSVs are byte-identical.
4. **N4. Named seeds** (D-2026-09-19-4). `REPLICATION_SEEDS` and `ILLUSTRATIVE_SEED` in `config.py`; replace the seed 42 hard-coded in 7 scripts; seed 99 in `plot_car_following.py` becomes a named constant unless the figure is unchanged at 42. Proof: golden exact, figures unchanged.
5. **N5. Diagnostics write to `figures/`.** `diagnose_fd_capacity.py` and `plot_car_following.py` write to `code/output/figures/`, while the paper includes `figures/fig_fd_diagnosis*.pdf` and `figures/fig_car_following*.pdf` (copied by hand). Proof: regenerated PDFs match the included ones.
6. **N6. Types into `odca/params.py`** (D-2026-09-19-2). `config.py` keeps only values; nothing in `odca/` imports `config`. Proof: golden exact.
7. **N7. `Vehicle` takes `VehicleParams`.** `Vehicle.__init__` goes from 24 parameters to about 8; `HDV` and `AV` stop unpacking. Proof: golden exact.
8. **N8. `SimulationResult` dataclass** replaces the results dict. Proof: golden exact.

After N2, N6 and N7, note the divergence of `code/odca/` in STATUS.md for the three other ODCA repos (BACKLOG B6).

## Infra
- Repo: `kdemirtas/paper-odca-des` (kdemirtas, private); push with `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Venue: Transportation Research Part B; deadline: none (no hard deadline; advisor feedback not yet received).
- Toolchain: `pdflatex + bibtex, elsarticle (elsarticle-harv.bst)`; build `pdflatex -interaction=nonstopmode paper-odca-des && bibtex paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des && pdflatex -interaction=nonstopmode paper-odca-des` from `paper/`.
- Python: `uv`, `code/.venv/`; run from `code/` as `.venv/bin/python <script>`.
- Data: none external; every result is simulated by `code/` (NGSIM/highD calibration is out of scope); `data/` and `code/output/` gitignored.
- Manuscript state: revision 1 complete 2026-04-21 (critic round 2: 0 Critical, 0 Major; 40 pages), waiting for Kerem's review before sending.
