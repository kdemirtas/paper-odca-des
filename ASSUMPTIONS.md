# ASSUMPTIONS: paper-odca-des

Every call I made on my own, in or out of a loop: a guess the docs did not settle, a default I
picked, a definition I chose. Provisional, never cited by code. Kerem reads the open rows each
session (`/pickup` lists them, `/next-assumption` walks them one at a time) and closes each one of
two ways: accepted as is, or corrected. Both end the same way: the call becomes a `DECISIONS.md`
entry whose `Source` column names this row (`accepted A-…` or `corrected A-…`), and the row leaves
this file. Nothing stays here once it has been discussed.

| Id | Made | What I assumed | Why | What would change it | Status |
|---|---|---|---|---|---|
| A-2026-09-20-2 | 2026-09-20 | The incident scenario becomes a two-lane closure (lanes 3 and 4) at 4,500 veh/h (1,125 per lane), from a one-lane closure at 3,000 veh/h (`run_incident.py`). Measured on 1,500 s probes: at 4,500 veh/h the open road runs at 21 s mean delay, one closed lane gives 38 s (no queue worth showing), two closed lanes give 131 s and a served flow of 3,558 against 4,583 veh/h. | Section 5.8 exists to show queue formation, spillback and recovery. With the fixed simulator a lane carries about 2,100 veh/h, so at 3,000 veh/h the three remaining lanes absorbed a one-lane closure and the figures showed free flow throughout. The old demand was tuned against the buggy capacity ("between 2800 too mild and 3200 gridlock"). | Kerem prefers a one-lane closure (then the demand has to rise to about 6,000 veh/h, which congests the baseline too), or a demand matched to a real site. | open |
