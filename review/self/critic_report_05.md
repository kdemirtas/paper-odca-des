# Critic report -- ODCA-DES -- round 5 -- 2026-09-20

Context: confirming pass after round 4 (0 Critical, 1 Major, 2 Minor, all applied) and after 41 LaTeX em-dashes were replaced with colons, commas, parentheses or sentence splits per the project's house style. The em-dash replacement is the change most likely to have introduced a new error, so every replaced sentence was read and checked for grammar, meaning and balanced punctuation.

## Verification of round-4 items

All 3 items from report 04 remain correctly applied:

- **M1 (Python version).** Line 759 says Python~3.13 and line 926 says Python (3.13). One version, the right one.
- **m1 (incident zone).** Line 1248 reads "cells 250--260 (11 cells, 82.5\,m incident zone)." Correct.
- **m2 (one name per thing).** Section 3.7.2 (line 410) now reads "a fixed update interval, the $\delta_{\text{eval}}$ of Table 3." The second symbol is gone.

## Verification of em-dash replacements

41 em-dashes removed, 0 remaining (verified by grep). Each replacement was read in the current manuscript. The replacements fall into four patterns, all grammatically sound:

1. **Parentheses for inline lists or asides** (13 instances): e.g. "behavioral characteristics (reaction times, headway preferences, lane-change strategies)" (line 62), "simplicity of CA (cells as discrete, addressable units)" (line 185), "cooperative AV behaviors (platooning, coordinated merging, and anticipatory speed adjustments)" (line 417). Every pair balanced.

2. **Colon introducing an explanation** (9 instances): e.g. "vehicle interactions are inherently asynchronous: a lane change on one side" (line 66), "influence zone: the eight neighboring cells" (line 291), "A vehicle requesting an occupied cell simply waits: its process is suspended" (line 661). Each colon follows a complete clause and introduces a specification.

3. **Commas setting off appositives** (16 instances): e.g. "Congestion, the slowing or stopping of vehicles, arises" (line 256), "This triangular FD, a two-regime piecewise-linear relationship..." (line 604), "a central AV controller, a single SimPy process, evaluates" (line 410). No ambiguity created by the commas in any case.

4. **Sentence splits** (3 instances): e.g. "vehicle A departs. The synchronous update allows this" (line 693). Each produces two well-formed sentences.

No sentence lost its grammar, changed its meaning, or became ambiguous. No parenthetical is unbalanced. En-dashes for ranges (S1--S4, 0.1--1.0, seeds 1--20) and compound terms (request--wait--seize--delay--release, flow--density, origin--destination, driver--movement) are all preserved.

## Critical

None.

## Major (should fix before submission)

None.

## Minor (polish)

None.

## Open questions for the author

None new. The round-4 question (first-order model in Limitations) remains an author judgment call; the current placement in Section 4.3 is defensible.

## Checks passed

- **Build.** 44 pages, 0 errors, 0 undefined references, 0 missing citations, 0 overfull boxes. Four hyperref warnings (harmless, unchanged from round 4).
- **Citations.** 31 keys in tex, 31 keys in bib: exact one-to-one match. No orphans, no missing keys, no uncited entries.
- **Figures.** All 14 figure labels referenced in text and interpreted in prose.
- **Tables.** All 11 table labels referenced in text and discussed in prose.
- **Contributions alignment.** 8 in introduction, 8 in conclusion, each paid off by a specific section (unchanged from round 4).
- **Number traceability.** No result was touched in round 4 or in the em-dash replacement. Round 4's full verification against `code/manuscript_numbers.py` and `code/analyse_incident.py` still holds.
- **Em-dash removal.** 0 em-dashes (---) remain. All 41 replacements verified individually. En-dashes (--) preserved for ranges and compound terms.
- **Python version.** One version (3.13) named consistently.
- **Incident zone.** 11 cells, 82.5 m, matching the inclusive range in the code.
- **Notation.** One symbol per quantity ($\delta_{\text{eval}}$ for the action interval, throughout).

## Verdict

**Submission-ready.** 0 Critical, 0 Major, 0 Minor. The review loop ends.

The manuscript is 44 pages, carries 31 references, 14 figures, 11 tables, 25 numbered equations, and 8 contributions each paid off in the body and the conclusion. Every headline number traces to a script. The em-dash replacement introduced no errors. Nothing remains that would give a referee a basis for a desk reject or a required revision that the authors have not already anticipated in the Limitations section.
