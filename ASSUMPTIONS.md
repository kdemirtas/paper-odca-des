# ASSUMPTIONS: paper-odca-des

Every call I made on my own, in or out of a loop: a guess the docs did not settle, a default I
picked, a definition I chose. Provisional, never cited by code. Kerem reads the open rows each
session (`/pickup` lists them, `/next-assumption` walks them one at a time) and closes each one of
two ways: accepted as is, or corrected. Both end the same way: the call becomes a `DECISIONS.md`
entry whose `Source` column names this row (`accepted A-…` or `corrected A-…`), and the row leaves
this file. Nothing stays here once it has been discussed.

| Id | Made | What I assumed | Why | What would change it | Status |
|---|---|---|---|---|---|
| A-2026-09-19-18 | 2026-09-19 | `wall_time_s` in every run file times `Simulation.run()` only, not building the network (`odca.experiment.run_once`); before, `run_experiments.py` also timed `Simulation(config)`, while `run_bottleneck.py` and `run_scalability.py` did not. The "Wall-clock time" row of the computational table (tex:1192, 802/477/318/277 s) is restated from the new definition at N11. | One definition across every script; building a 4-lane, 1000-cell network is a small, constant cost that says nothing about the event engine the table compares. | Kerem wants the table to be end-to-end time a user waits (then `run_once` times construction too, and bottleneck and scalability move with it). | open |
