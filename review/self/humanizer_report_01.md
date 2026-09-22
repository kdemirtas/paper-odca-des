# Humanizer report -- ODCA-DES -- 01 -- 2026-09-22

**Files read:** `paper/paper-odca-des_smpt.tex` (1368 lines, superset, read in full),
`paper/paper-odca-des_trb.tex` (1364 lines, diffed against the SMPT file to confirm the six
divergent regions before scanning).

**Revision:** revision 3 (current, per HANDOVER.md / CLAUDE.md). Follows critic round 7
(`review/self/critic_report_07.md`), which closed at 0 Critical, 0 Major, 0 Minor.

**Divergence check:** `diff` shows exactly 6 hunks (journal line, abstract opening, introduction
first paragraph + bridge, introduction generality close, conclusion generality close, Future
Research bullet), matching CLAUDE.md's list. All six findings below sit outside those six
regions, in text identical between the two files, so every finding is scope `shared` and applies
to both.

**Finding count:** 6 total -- 1 Tier A, 5 Tier B. This is a clean manuscript: the mechanical
lexical scan (`delve`, `underscore`, `showcase`, `intricate`, `meticulous`, `commendable`,
`tapestry`, `realm`, `pivotal`, `testament`, `landscape`, `leverage` as noun, chatbot residue,
announcement hedges, em-dashes, curly quotes) returned only the one `leverage` hit below; no
em-dashes in prose (7 in TikZ comment lines only, invisible in the PDF, already noted by the
critic); no curly quotes. The Tier B candidates below are the small residue left after applying
the exclusion test hard against roughly three dozen participial tails and summary sentences that
are doing real technical work and are listed in "Not flagged" below.

---

### F01 | excess vocabulary (leverage) | Tier A | line 143 (TRB) / 145 (SMPT) | scope: shared

**Why:** `leverage` used as a verb is one of the Kobak et al. high-ratio excess words. It is a
finding on sight, independent of the exclusion test. "Uses" or "adopts" says the same thing in
one fewer syllable and matches how the paper describes its other dependencies elsewhere (e.g.
"built on SimPy" at line 774/776).

**Status:** accepted

```old
The present framework leverages the DES paradigm through SimPy
```
```new
The present framework adopts the DES paradigm through SimPy
```

---

### F02 | participial tail | Tier B | line 356 (TRB) / 358 (SMPT) | scope: shared

**Why:** the clause after the comma restates "the probability increases toward 1" in feelings
("urgency") rather than adding anything the reader does not already have from the equation and
the sentence before it. Cutting it loses no information a referee needs.

**Status:** accepted

```old
, capturing the increasing urgency of reaching the exit lane
```
```new
```

*Accepted by Kerem 2026-09-22 as a deletion, not the replacement first proposed: " as the vehicle nears its exit" repeats the clause the sentence opens with, "As $r$ decreases (vehicle approaches its exit)".*

---

### F03 | copula avoidance | Tier B | line 788 (TRB) / 790 (SMPT) | scope: shared

**Why:** "serves as" where "is" is true, shorter, and identical in meaning. The mainline entry
is the primary source; nothing about the word "serves" adds information about how it functions
as one.

**Status:** accepted

```old
serves as the primary source
```
```new
is the primary source
```

---

### F04 | copula avoidance + significance inflation | Tier B | line 1313 (TRB) / 1315 (SMPT) | scope: shared

**Why:** "represents a fundamental departure from" is "differs fundamentally from" wearing a
noun phrase, and "fundamental departure" is the kind of significance language the exclusion test
is built for: the sentence's own colon and the two clauses that follow it already carry the
technical claim (event-driven re-evaluation vs. predetermined intervals). The verb form is
shorter and matches the direct comparative language the paper uses elsewhere ("differ by a
factor of three," line 1132).

**Status:** accepted

```old
represents a fundamental departure from
```
```new
differs fundamentally from
```

---

### F05 | signposting that announces rather than says | Tier B | line 1077 (TRB) / 1079 (SMPT) | scope: shared

**Why:** "with several notable observations" tells the reader nothing the three \paragraph{}
subsections that follow (Throughput, Delay, Lane-change frequency) don't already say by being
there. "Notable" is doing no work: of course the results being reported are the notable ones.
The colon alone is enough to introduce the list.

**Status:** accepted

```old
, with several notable observations:
```
```new
:
```

---

### F06 | filler emphasis word | Tier B | line 422 (TRB) / 424 (SMPT) | scope: shared

**Why:** "Crucially," in front of "AVs perform only mandatory lane changes" asserts importance
instead of letting the sentence carry it. The claim is exactly as load-bearing without the
adverb, and the paper doesn't otherwise open sentences this way, so its one appearance reads as
an unweighed intensifier rather than a deliberate emphasis device.

**Status:** accepted

```old
Crucially, AVs perform only mandatory lane changes
```
```new
AVs perform only mandatory lane changes
```

---

## Not flagged

Patterns checked and deliberately left alone, with why:

- **Participial tails in general (~35 of ~40 candidates).** The large majority define or restate
  a mechanism the reader needs at that point, e.g. line 207/209 "meaning at most one vehicle can
  occupy (seize) the cell at any given time" (defines the resource semantics -- cutting it loses
  the definition), line 244/243 "since the chance of having acted after n evaluations is
  1-(1-P)^n" (derivation step, not decoration), and the closing clauses of the incident-analysis
  paragraphs (e.g. "because the vehicles at the back of the queue only learn of the discharge
  when the wave reaches them") which state the causal mechanism, not a restatement of it. Only
  F02 above crossed the line into pure restatement.
- **"This section ... " topic sentences (3 instances: lines 184, 507, 774/776).** This is at the
  literal threshold the rule gives ("used more than twice"), but each sentence names distinct,
  concrete section content (hybrid discretization and driver architecture; headway consistency
  and FD relationships; hardware and RNG setup) rather than repeating an empty announcement. Not
  the "This section will demonstrate that X" antipattern; these are ordinary elsarticle topic
  sentences.
- **"The key insight is that ..." (2 instances: lines 270/272, 618/620).** Each introduces the
  actual derivation result (no headway rule needed; the FD parameters fall out of the protocol
  parameters) rather than padding around it. Below the two-instance signposting threshold and
  each does real work.
- **Rule-of-three list at line 678/680 ("Deadlock-free," "Order-preserving," "Physically
  consistent").** Three distinct, separately justified properties, each with its own supporting
  clause. Removing any one loses a claim the paper makes elsewhere (deadlock-freedom is not
  restated anywhere else).
- **"Note that ..." (4 instances).** These introduce a genuine clarification each time (travel
  speed vs. running speed, which vehicle the headway depends on, simultaneity in the NaSch
  worked example, the unequal replication counts in the sensitivity analysis), not the vacuous
  "it is worth noting that" hedge the rules target. Left alone.
- **"Nothing in the model schedules this" / "Nothing in the model schedules any of this" (2
  instances, lines 987/989 and 1267/1269).** Reads like a stock transition but each time it is
  the paper's actual point: the described dynamic (backward wave, queue recovery) is emergent,
  not programmed. Technical content, not filler.
- **Em-dashes in TikZ comment lines (7, lines 455, 462, 465, 471, 487, 491, 799).** Already
  checked by critic round 7: invisible in the compiled PDF, not prose. Confirmed again here, not
  re-raised as a new finding.
- **Notation and domain terms (k, v, tau, m, ell; AV/HDV; MLC/DLC; PriorityResource, etc.).**
  Excluded per CONTEXT.md and the archetype's own rule against flagging fixed notation.

## Summary for Kerem

Report: `/home/kerem-demirtas/Papers/paper-odca-des/review/self/humanizer_report_01.md`

6 findings: 1 Tier A (leverage), 5 Tier B. This is a genuinely low count and that's the honest
read after the exclusion test -- the manuscript is unusually clean, consistent with closing the
critic loop at 0/0/0 after seven rounds.

If you only have time for three: F01 (leverage, mechanical, no judgment call), F02 (the
participial tail your calibration note flagged as the textbook example), F04 (the "represents a
fundamental departure" sentence sits in the Conclusion, the section a referee reads most
skeptically for overclaiming).

Where I'm least sure the phrase is pure filler: F06 ("Crucially,"). It's a one-word intensifier
and the sentence it introduces (AVs only perform mandatory lane changes) is a genuinely important
structural fact about the model, so there's a reading where the author wanted the emphasis on
purpose. I flagged it because the paper doesn't use this construction anywhere else, but it's the
softest call of the six.


## Applied 2026-09-22

- F01: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- F02: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- F03: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- F04: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- F05: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- F06: applied to paper-odca-des_smpt.tex, paper-odca-des_trb.tex
- divergence check after applying: 6 hunks

Build gate and the confirming critic round are not run by this script.
