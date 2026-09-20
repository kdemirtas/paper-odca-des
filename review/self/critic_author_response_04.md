# Author response to critic report 04

Round 4 returned 0 Critical, 1 Major and 2 Minor. All three are applied. Each was checked against
the code before being accepted, not taken on the report's word.

## M1 (Major): the Python version contradicted itself

**Report:** Section 5 says "Python~3.10" at line 759 and "Python (3.13)" at line 926.

**Checked:** `code/.venv/bin/python --version` reports Python 3.13.13.

**Done:** line 759 now says Python~3.13. The paper names one version, and it is the one the
results were produced on.

## m1 (Minor): the incident zone is 82.5 m, not 75

**Report:** "cells 250--260 ($\approx$75\,m incident zone)" is 11 cells at 7.5 m, so 82.5 m.

**Checked, because the arithmetic depends on whether the range is inclusive:** `run_incident.py`
sets `CLOSURE_START_CELL = 250` and `CLOSURE_END_CELL = 260`, and `Incident._cells` in odca-des
takes `lane.cells[cfg.first_cell:last + 1]`. Inclusive, so 11 cells, 82.5 m. The report is right.

**Done:** the text now reads "cells 250--260 (11 cells, 82.5\,m incident zone)". The same error
was in the code, where the comment on `CLOSURE_END_CELL` said "short incident (~75 m)"; it now
says the range is inclusive and the zone is 82.5 m. The 75 m in the heatmap caption is a
different quantity, the bin width of the density plot, and is unchanged.

## m2 (Minor): one name per thing

**Report:** $\Delta t_{\text{ctrl}}$ is introduced in Section 3.7.2 and never used again, while
Table 3 lists the same quantity as $\delta_{\text{eval}}$.

**Checked:** one occurrence in the whole manuscript. Table 3's row is "Action interval (max.
re-evaluation gap)", $\delta_{\text{eval}}$, 1.0 s for the HDV and 0.1 s for the AV controller
cycle, so the table already names the controller interval.

**Done:** Section 3.7.2 now refers to "a fixed update interval, the $\delta_{\text{eval}}$ of
Table~\ref{tab:vehicle_params}". The second symbol is gone.

## Build after the three edits

44 pages, 0 errors, 0 undefined references, 0 missing citations, no overfull box over 10 pt. No
number moved: none of the three edits touches a result, and no result file was regenerated.

## Not changed

Nothing in the report was declined.
