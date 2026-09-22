# Author response to critic report 09 (2026-09-22)

Round 9 was the full pre-submission read Kerem asked for ("one more e2e round of self review and
I will submit"). Verdict: 0 Critical, 2 Major, 2 Minor, content-ready. Every quoted number traces
to `code/output/` through `manuscript_numbers.py`; 36/36 citations both ways; six hunks between the
journal files; zero em-dashes; zero TODOs; both builds clean.

## Major 1: no Declaration of competing interest. Applied.
`\section*{Declaration of competing interest}` with the standard Elsevier sentence, inserted before
the References block in both files, identical text.

## Major 2: no Data availability statement. Applied.
`\section*{Data availability}`: the simulator (`odca-des`, MIT) and the scripts behind every result,
table and figure will be made public at `github.com/kdemirtas/odca-des` and
`github.com/kdemirtas/paper-odca-des` on acceptance. Kerem chose "public on acceptance, name the
repo" over "public now" and "on request" (2026-09-22). Both repos are private until then.

## Minor 1: no Acknowledgments section. Not applied, deliberately.
Kerem, 2026-09-22: none. No funding to declare, and the advisors are co-authors.

## Minor 2: the four code-script references in the body anchor to nothing. Resolved by Major 2.
The Data availability statement now names the repositories those scripts live in.

## Added beyond the report
`\section*{CRediT authorship contribution statement}`, the standard split (Demirtas:
conceptualization, methodology, software, validation, formal analysis, original draft; Mirchandani
and Zhou: supervision, review and editing). Kerem's choice, 2026-09-22, so the portal does not have
to be typed into.

All three blocks are shared text in both files; the divergence check still returns six hunks.
The new text goes through the humanizer and a confirming critic round before the marked builds,
per D-2026-09-22-1.
