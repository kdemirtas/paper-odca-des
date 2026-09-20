# Critic report -- ODCA-DES (SMPT version) -- round 6 -- 2026-09-20

Context: focused review of the material added in session 27 (D-2026-09-20-13, D-2026-09-20-14), not a full re-review. Rounds 1--5 are closed clean. This round covers the Cell-DEVS positioning, the SMPT-specific framing, the narrowed novelty sentence, the generality claim, and the structural diff between the two journal files.

## Files read

- `CLAUDE.md`, `CONTEXT.md`, `STATUS.md`, `HANDOVER.md`
- `review/self/critic_report_05.md`
- `paper/paper-odca-des_smpt.tex` (full)
- `paper/paper-odca-des_trb.tex` (full)
- `paper/references.bib` (Cell-DEVS entries)

## Blockers (must fix before submission)

None.

## Major (should fix)

- **[Introduction, line 90; Conclusion, line 1319] Generality claim is unhedged.** Both SMPT-only paragraphs assert the pattern "applies to any domain in which discrete space is a contended medium" (line 90) and "it transfers to any domain where discrete space is a contended medium" (line 1319). "Any domain" is a universal quantifier backed by exactly one domain. A referee at SMPT can reasonably ask "show a second domain or remove the claim," and that is a required-revision scenario. The structural observation is correct (request-wait-seize-delay-release is a standard DES pattern, not traffic-specific), but the assertion of transferability should be hedged. Suggested fix: "in principle applies" or "is in principle transferable" in both places, and optionally note in the Future Research that demonstrating transfer to a second domain is future work. Two-word fix, large reduction in referee attack surface.

## Minor (polish)

- **[Diff: 5 differences, docs say 4] The SMPT introduction has a generality paragraph (line 90) absent from TRB, not accounted for in the project documentation.** The diff between the two files shows five differences, not the four listed in HANDOVER.md, STATUS.md session 27, and the project rules (D-2026-09-20-14): (1) `\journal` line, (2) abstract, (3) introduction first paragraph, (4) introduction generality paragraph after the contributions list (line 90), (5) conclusion generality sentences (line 1319). The documentation lists four: it either counts the two generality paragraphs as one, or it was not aware of the second. Neither file is wrong (both generality paragraphs belong in SMPT and not in TRB), but the documentation should say "five places" or list them accurately.

- **[Introduction, lines 62--64] Transition from formalism frame to traffic motivation is abrupt.** The SMPT-only first paragraph (P1, line 62) poses "where does behaviour live?" and ends "Freeway traffic...is the setting, because it is one in which the answer can be measured against theory." The next paragraph (P2, line 64) starts fresh: "Traffic simulation is an essential tool for evaluating freeway operations..." as if P1 never happened. The effect is two introductions rather than one argument: a formalism introduction and a traffic introduction, pasted together. The bridge at the end of P1 exists but is weak; P2 does not pick it up. Suggested fix: either make P2's opening reference the formalism question ("Within this setting, the dominant simulation approaches...") or merge the last sentence of P1 into the start of P2, so the reader sees one line of reasoning rather than a restart.

## Open questions for the author

- The generality claim, once hedged, raises a strategic question: does SMPT want the paper to pitch itself as a general simulation-methodology contribution (the pattern) that happens to be demonstrated on traffic, or as a traffic contribution whose protocol happens to be general? The current framing leans toward the first. If the answer is the first, the generality paragraphs belong, hedged. If the answer is the second, cutting both generality paragraphs and using the TRB framing is simpler and lower-risk.

## Checks passed

**Cell-DEVS positioning: accurate, fair, and internally consistent.**
- All five Cell-DEVS mentions (abstract, intro P1, contribution 1, Section 2.3, conclusion contribution 1) explicitly acknowledge that putting a CA on a discrete-event engine is established ground since 2001, and disclaim that combination.
- The three-point comparison in Section 2.3 (what is active, what a speed is, where congestion comes from) is specific, accurate per the cited Cell-DEVS traffic models, and gives Cell-DEVS credit for removing synchronous updates.
- No sentence elsewhere in the paper implicitly claims the CA+DES combination as novel. The sentence at Section 3.1 ("while removing the two most restrictive CA assumptions: integer speeds and synchronous timesteps") describes what the ODCA-DES scheme achieves, consistent with the acknowledgment that Cell-DEVS also removes synchronous updates; it is not a novelty claim.
- The statement "the integer-speed artifact of classical CA survives the move to discrete events" (Section 2.3) is accurate for the Cell-DEVS traffic models cited, where cell transition functions encode speed as an integer state. It is not a claim about Cell-DEVS as a formalism (which could in principle encode continuous speed).

**Narrowed novelty sentence: defensible as written.**
- "to the authors' knowledge, no prior work models individual vehicle movement as resource acquisition on a cell lattice, and none derives headway and capacity in closed form from the acquisition protocol itself" (Section 2.3; identical in both files).
- The "to the authors' knowledge" hedge is appropriate. The two-part claim is specific and verifiable. Cell-DEVS does not model resource acquisition (it models cell state transitions). DES traffic models (Burghout, Osorio) do not use cellular lattices. Microscopic simulators (SUMO, Vissim) do not use cells. The closed-form capacity derivation from the protocol parameters is Section 4 of this paper and has no counterpart in the cited Cell-DEVS traffic literature. No additional hedging is needed.

**File divergence: intentional and correct, except for the documentation count.**
- The diff shows exactly 5 diff hunks. All are content-appropriate: the SMPT-only material (formalism frame, generality claims) belongs in a simulation-methodology journal and not in a transportation-methodology journal. No shared content diverges. No accidental edit went into one file and not the other.
- Citation sets are identical: 36 unique keys in each file, 36 entries in `references.bib`, 0 orphans, 0 missing.

**Build (SMPT).** 46 pages, 0 errors, 0 undefined references, 0 missing citations, 0 overfull boxes. Four hyperref warnings (harmless, unchanged from round 5).

**All round-5 checks still hold.** Figures 14/14, tables 11/11, contributions 8/8, em-dashes 0 remaining. No number moved.

## Verdict

1 Major (unhedged generality), 2 Minor (doc count, intro transition). The Major is a two-word fix. After that fix, the SMPT version is submission-ready.
