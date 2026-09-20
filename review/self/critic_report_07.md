# Critic report -- ODCA-DES (SMPT version) -- round 7 -- 2026-09-20

Confirming pass: round 6 returned 0 Critical, 1 Major, 2 Minor.
The author response (`critic_author_response_06.md`) applied all three.
This round checks the four items named in the dispatch and nothing else.

## Files read

- `CLAUDE.md`, `STATUS.md`
- `review/self/critic_report_06.md`
- `review/self/critic_author_response_06.md`
- `paper/paper-odca-des_smpt.tex` (full)
- `paper/paper-odca-des_trb.tex` (full, for diff)
- `paper/references.bib` (key cross-reference only)

## Check 1: generality hedge (was Major)

**Resolved.** Both SMPT-only paragraphs now read "in principle" and add a
concession sentence.

- Introduction (line 90): "is in principle applicable wherever discrete space
  is a contended medium rather than a field of local rules. That transfer is
  asserted here as a structural property of the protocol, not demonstrated: one
  domain is reported, and a second is future work."
- Conclusion (line 1319): "it is in principle transferable wherever discrete
  space is a contended medium. That is a structural observation about the
  protocol rather than a demonstrated result, and one domain is reported here."
- Future Research (line 1356): new bullet "Transfer to a second contended-space
  domain", naming two concrete candidates (block-signalled rail, automated
  warehouse aisles) and framing the open question (whether the analytical
  tractability belongs to the protocol or to the traffic case).

The hedge is proportionate. It does not over-qualify: the structural observation
is stated confidently ("is in principle applicable/transferable"), and only the
demonstration gap is conceded. A referee who wants a second domain cannot
require-revise this, because the paper already calls it future work and names the
question the second domain would answer. The claim remains useful because it
tells the SMPT reader what the modelling pattern is, which a pure traffic framing
would not. No over-hedging detected.

## Check 2: introduction transition (was Minor)

**Resolved.** Line 64 now opens "That setting is not a convenience." The pronoun
"that setting" picks up "Freeway traffic...is the setting" from the end of the
preceding formalism paragraph (line 62). The bridge works: it tells the reader
that the choice of traffic is substantive, not arbitrary, and the rest of the
paragraph ("Traffic simulation is an essential tool for...") explains why. The
two-introduction effect the critic identified in round 6 is gone; the reader now
follows one line of reasoning through the formalism question, the choice of
domain, and the motivation for that domain.

## Check 3: divergence count (was Minor)

**Confirmed: exactly 6 hunks.** `diff paper-odca-des_trb.tex paper-odca-des_smpt.tex`
returns 6 diff blocks:

1. Line 21: `\journal` line.
2. Line 47: abstract opening.
3. Lines 62--64: introduction first paragraph + bridge sentence.
4. Line 90: generality sentences closing the introduction.
5. Line 1319: generality sentences closing the conclusion.
6. Lines 1355--1356: Future Research bullet on transfer to a second domain.

This matches the six places now listed by name in CLAUDE.md, HANDOVER.md, and
DECISIONS.md D-2026-09-20-14. No seventh hunk.

## Check 4: no collateral damage from round-6 edits

- **Build:** `pdflatex` on `paper-odca-des_smpt.tex` produces 46 pages,
  0 errors, 0 undefined references, 0 missing citations, 0 overfull hbox.
- **Em-dashes:** 0 in prose. Seven occurrences of the Unicode em-dash character
  exist in TikZ comment lines (lines 455, 462, 465, 471, 487, 491, 799); these
  are invisible in the PDF and do not violate the project rule, which targets
  prose.
- **Citations:** 36 unique keys cited in the SMPT file, 36 entries in
  `references.bib`, 0 orphans, 0 missing.
- **No contradictions:** the hedged passages do not conflict with the
  contributions list (which claims what the paper demonstrates, not what the
  pattern can in principle do), the Limitations section, or any other passage in
  the paper. The TRB file has no generality claim at all, as expected.
- **No broken sentences.** The added text reads as complete, grammatical English.

## Blockers (must fix before submission)

None.

## Major (should fix)

None.

## Minor (polish)

None.

## Open questions for the author

None from this round. The strategic question raised in round 6 (whether to pitch
the paper as a simulation-methodology contribution or a traffic contribution) was
correctly routed to AGENDA.md and is Kerem's call, not a manuscript finding.

## Checks passed

- Generality claim hedged proportionately in both SMPT-only paragraphs; future
  work names the open item with two concrete candidates.
- Introduction transition bridges the formalism paragraph into the traffic
  paragraph without a restart.
- Journal file divergence is exactly six hunks, matching the project
  documentation.
- Build gate met (0 errors, 0 undefined references, 0 overfull hbox).
- Citation coverage is 36/36 with no orphans.
- No em-dashes in prose, no broken sentences, no contradictions introduced.

## Verdict

0 Critical, 0 Major, 0 Minor. All round-6 findings are resolved. No new finding.
The critic loop can close: the SMPT version is submission-ready, subject to
Kerem's decision on the journal question recorded in AGENDA.md.
