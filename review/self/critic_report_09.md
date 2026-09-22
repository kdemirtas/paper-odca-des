# Critic report: paper-odca-des, 2026-09-22

Full end-to-end pre-submission review, round 9. NOT a confirming round: the
whole manuscript is read as the referee who will receive it. State: revision 3
closed, critic rounds 1--7 closed at 0/0/0, humanizer pass applied six rewrites,
round 8 confirmed none moved a claim.

Files read (SMPT in full, TRB at the six divergent regions plus build):
- `paper/paper-odca-des_smpt.tex` (1369 lines, 46 pages)
- `paper/paper-odca-des_trb.tex` (1363 lines, 45 pages)
- `paper/references.bib` (36 entries)
- `CLAUDE.md`, `CONTEXT.md`, `HANDOVER.md`, `STATUS.md`
- `review/self/critic_report_07.md`, `review/self/critic_report_08.md`
- `review/self/humanizer_report_01.md`
- Output of `code/manuscript_numbers.py` (all aggregate numbers)

## Critical (must fix before submission)

(none)

## Major (should fix)

- **[Both files, after Section 6 / before bibliography]** No Declaration of
  Competing Interests. Both TR-B and SMPT are Elsevier journals; current
  Elsevier policy requires a competing-interests statement in the manuscript
  text, not only in the submission portal. Its absence may cause a desk-reject
  or an immediate "revise before review" request. Suggested fix: add a
  `\section*{Declaration of competing interest}` block with the standard
  Elsevier text ("The authors declare that they have no known competing
  financial interests or personal relationships that could have appeared to
  influence the work reported in this paper.") before `\bibliography`.

- **[Both files, after Section 6 / before bibliography]** No Data Availability
  statement. Elsevier now requires one for both journals. The paper is
  simulation-based with four `\texttt{code/...}` references to reproducibility
  scripts (lines 651, 962, 1097, 1267 SMPT); those references are good practice
  but only useful if the reader can reach the code. Suggested fix: add a
  `\section*{Data availability}` block stating whether the simulation code
  and data-generating scripts will be made available (public repository URL,
  or "available from the corresponding author upon reasonable request").

## Minor (polish)

- **[Both files, absent]** No Acknowledgments section. A dissertation-based
  paper with three authors typically acknowledges the doctoral committee, the
  department or any fellowship. If there is nothing to acknowledge, this can be
  omitted, but Kerem should confirm deliberately.

- **[SMPT line 651, 962, 1097, 1267]** Four references to code scripts in the
  manuscript body (`plot_paradigm_comparison.py`, `diagnose_fd_capacity.py`,
  `manuscript_numbers.py`, `analyse_incident.py`). These are an asset if the
  code is public, and become the useful detail inside the Data Availability
  statement. If the code will remain private, soften to "available from the
  corresponding author". Not urgent: writing the Data Availability statement
  (Major above) settles the question for all four.

## Open questions for the author

(none from the content; the two Major items require a sentence each)

## Checks passed

Numbers verification (manuscript_numbers.py against every quoted number):
- All S1--S4 table values (throughput, travel time, delay, LC frequency,
  pct delayed) match to the last printed digit.
- All bottleneck table values (BN_0 through BN_70) match.
- All sensitivity table values (action intervals 0.25, 0.5, 1.0 s) match.
- All computational table values (events, speed evals, cf evals, lane changes,
  wall clock) match.
- All scalability table values (events, wall clock, realtime ratio) match.
- Abstract numbers: 18.9%, 5874 +/- 19, 6983 +/- 34, 95%, 217 +/- 6,
  10.2 +/- 0.3, 99.8% all verified against script output.
- Conclusion numbers repeat the same set and match.
- Derived inline percentages verified arithmetically: 13.7%, 83.9%, 0.9%
  (bottleneck step), 99.2%, factor-of-three delay ratio, 6.4%, 10% delay
  reduction, 1.4%, CoV ranges (0.7--1.1%, 0.9--2.4%, 24%).
- Demand-weighted free-flow trip time: script prints 130.9 s, manuscript
  says 131 s (correct rounding). Full-segment: 153.8 s, manuscript says
  154 s (correct rounding). S4 exceeds the weighted time by 8.1%, manuscript
  says 8% (correct rounding).
- Analytical capacity: 5.2/(5.2*1.5+1) = 0.591 veh/cell/s = 2127 veh/h.
  Backward wave speed: 1.0/1.5 = 0.667 cells/s = 18 km/h. Both match.
- Theoretical mixed-traffic capacity table: all four rows recomputed and match.

Build gate:
- TRB: 0 errors, 0 undefined references, 0 missing citations, 0 overfull
  hbox, 45 pages.
- SMPT: 0 errors, 0 undefined references, 0 missing citations, 0 overfull
  hbox, 46 pages.

Citation coverage:
- 36 unique keys cited in the SMPT file.
- 36 entries in references.bib.
- 0 keys cited but absent from bib (no missing citations).
- 0 bib entries never cited (no orphans).
- Same 36/36 for TRB (shared bibliography).

Figure/table integrity:
- All 12 `\includegraphics` paths resolve to existing PDFs in `figures/`.
- Every `\label{fig:*}` and `\label{tab:*}` has at least one `\ref` in text.
- Every figure and table is interpreted in prose, not just referenced.
- Captions stand alone: each includes parameter values, scenario identifiers
  and what the reader should see.
- 0 references to undefined labels.

Two-file split:
- `diff` shows exactly 6 hunks: `\journal` line, abstract opening,
  introduction first paragraph, introduction generality close, conclusion
  generality close, Future Research bullet on second domain.
- Both divergent passages read correctly in their own context.
- TRB abstract: 187 words (limit 200). SMPT abstract: 258 words (no strict
  limit).

Narrative coherence:
- Abstract matches body: every claim is paid off.
- Introduction lists 8 contributions; each is delivered by a named later
  section.
- Conclusion re-enumerates all 8 (different ordering, same substance).
- Cell-DEVS positioning (SMPT) is hedged: "in principle," "asserted, not
  demonstrated," "one domain is reported." Future Research names the open
  question.

House rules:
- 0 em-dashes in prose in either file (7 in TikZ comment lines, invisible
  in PDF, noted in round 7).
- 0 TODOs, FIXMEs, notes to self.
- 0 commented-out substantive content (the only comment blocks are section
  dividers).
- Voice: consistent first-person-plural, present tense for methods, past
  for results.

Submission mechanics checked:
- Title, author block, affiliations, `\cortext`: present and correct.
- `\journal` line: correct in each file.
- `\begin{keyword}`: present with 7 keywords.
- Missing: Declaration of competing interests (Major above).
- Missing: Data availability statement (Major above).
- Missing: Acknowledgments (Minor above).
- Highlights: not present. SMPT requires them but they are entered in the
  submission portal, not in the .tex file. Not a manuscript finding.
