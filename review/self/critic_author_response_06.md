# Author response to critic report 06 (2026-09-20)

Round 6 was a focused review of the material added in session 27 (D-2026-09-20-13, the Cell-DEVS
positioning, and D-2026-09-20-14, the journal split), not a full re-review. Verdict: 0 Critical,
1 Major, 2 Minor. All three are applied. No number moved; nothing in `code/` ran.

## Major

**M1. The generality claim was unhedged, in both SMPT-only paragraphs.** Accepted, and the critic
is right that "any domain" is a universal quantifier backed by one domain. Fixed in both places,
and the fix goes further than the two words suggested, because the honest problem is not the word
"any" but the absence of a second case.

- Introduction: "applies to any domain in which discrete space is a contended medium" becomes "is
  in principle applicable wherever discrete space is a contended medium", followed by "That
  transfer is asserted here as a structural property of the protocol, not demonstrated: one domain
  is reported, and a second is future work."
- Conclusion: "it transfers to any domain where discrete space is a contended medium" becomes "it
  is in principle transferable wherever discrete space is a contended medium", followed by "That is
  a structural observation about the protocol rather than a demonstrated result, and one domain is
  reported here."
- Future Research Directions gains a bullet naming the open item: applying the protocol to another
  discrete-space system where occupancy is exclusive and waiting is the congestion mechanism
  (block-signalled rail, automated warehouse aisles), to test whether the analytical tractability
  of Section 4 is a property of the protocol or of the traffic case.

The referee attack the critic describes, "show a second domain or remove the claim", now has the
paper's own answer in the paper: one domain is shown, the second is named as future work.

## Minor

**m1. The documentation said four differences between the journal files; there were five.** Correct,
and the count is now six after this round's Future Research bullet. The documentation undercounted
because it treated the generality material as one place when it lands in two (the introduction's
closing paragraph and the conclusion's). HANDOVER.md, STATUS.md and the project rules now list all
six by name rather than giving a count: the `\journal` line, the abstract opening, the
introduction's first paragraph, the generality sentences closing the introduction, the generality
sentences closing the conclusion, and the Future Research bullet on transfer to a second domain.

**m2. The introduction restarted rather than continuing.** Accepted. The traffic paragraph opened
"Traffic simulation is an essential tool for..." as if the formalism paragraph before it had not
happened. It now opens "That setting is not a convenience. Traffic simulation is an essential tool
for...", which picks up the last sentence of the formalism paragraph (that traffic is the setting
where the answer can be measured) instead of ignoring it.

## Open question the critic raised

The critic asks whether the paper should pitch itself as a general simulation-methodology
contribution demonstrated on traffic, or as a traffic contribution whose protocol happens to be
general, and notes that cutting both generality paragraphs and using the TR-B framing is the
lower-risk option. That is Kerem's call, not the author's, and it is the same call as the journal
choice: the generality framing exists because SMPT is a simulation-methodology journal. It is
recorded in `AGENDA.md` Open decisions beside the journal recommendation, not decided here.

## Verification after the fixes

`paper-odca-des_smpt.tex`: 46 pages, 0 errors, 0 undefined references, 0 missing citations, 0
overfull hbox over 10 pt, 0 em-dashes, 36 citations against 36 bib keys with no orphan either way.
`revision-3-smpt-marked.pdf` rebuilt, 46 pages, held to the same gate.
`paper-odca-des_trb.tex` is untouched by this round and unchanged since PR #24.
