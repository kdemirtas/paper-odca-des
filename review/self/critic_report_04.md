# Critic report -- ODCA-DES -- round 4 -- 2026-09-20

Context: this is the submission-readiness review. The manuscript is at revision 2, with all round-3 items applied and answered in `review/self/critic_author_response_03.md`. Two changes landed today: (1) the Section 4.3 paradigm figure now runs a platoon through a posted speed-limit zone (D-2026-09-20-12), and (2) the same section carries a paragraph explaining why the model is first order with no acceleration bound (odca-des:D-2026-09-20-20). Every reported number was verified against `code/manuscript_numbers.py` and `code/analyse_incident.py`; the build was rerun (pdflatex, bibtex, pdflatex, pdflatex: 44 pages, 0 errors, 0 undefined references, 0 missing citations, 0 overfull boxes, 4 harmless hyperref warnings).

## Verification of round-3 items

All 3 Major and 6 Minor items from report 03 are resolved:

- **M1 (bottleneck "all" overstatement).** Closed. The abstract (line 47), conclusion (line 1302) and fig:bottleneck_throughput caption (line 1124) now correctly say 99% at 50% AV and all of it at 70%, matching the body and Table 6.
- **M2 (conclusion drops FD number).** Closed. Line 1302: "on a ring road, which removes the entry boundary effect, the simulated capacity reaches 92 to 93% of the analytic q_max."
- **M3 (131 s not derived).** Closed. The fig:travel_time caption (line 1082) now names the quantity, explains why it is shorter than 154 s, points at the demand section, and names `code/manuscript_numbers.py`. Verified: 130.9 s from the script.
- **m1 (Cassidy reference).** Closed. `cassidy1999some` added to `references.bib` (line 315) and cited at line 1263.
- **m2 (scalability caption).** Closed. Line 1194: "sub-linearly (empirical exponent 0.86)."
- **m3 (S1 label reuse).** Closed. Line 968: "the baseline parameters of Table 3 with mainline demand reduced to 3,000 veh/h."
- **m4 (bib key-year mismatches).** Closed. All four keys renamed; all 31 entries verified, no orphan, no uncited.
- **m5 (abstract word count).** Closed. Abstract is approximately 189 words, under the 200-word TR-B guideline.
- **m6 (warm-up difference).** Closed. Section 5.7 (line 1248) now explains why the incident scenario uses 200 s instead of 300 s.

## Assessment of today's changes

### Section 4.3 paradigm figure (D-2026-09-20-12)

The speed-limit-zone scenario is a significant improvement over the previous "start from rest on an empty road." It exercises both deceleration (approaching the zone) and acceleration (leaving it) in both models, making the comparison more informative. The choice of a posted speed-limit zone rather than a blockage or scripted leader is sound: it is the only mechanism both models can run as the identical scenario, so the figure stays about representation rather than capability. The numbers quoted in the paragraph and caption (1,328 cell entries, 14 on a whole second, 19 distinct speeds, 1.86 to 5.20 cells/s, NaSch lead at cells 64 and 67) are verified from the script output (STATUS session 23).

### First-order paragraph (odca-des:D-2026-09-20-20)

The paragraph is convincing and does NOT invite the objection it tries to close. Its structure is:

1. It names the visible asymmetry: approach to the zone is gradual (spacing rule constrains through Eq. 1), departure is a single step (nothing constrains a vehicle whose road is clear).
2. It shows that adding only an acceleration bound would be physically inconsistent: the spacing rule already implies decelerations of about 1.5 cells/s^2 (11.3 m/s^2) for a free-flowing vehicle meeting a standing queue 9 cells ahead, so bounding acceleration to a plausible 3 m/s^2 while leaving deceleration at 11 m/s^2 "would not describe a car."
3. It draws the scope boundary: bounding both requires a second-order car-following law in place of Newell, which is a different paper.

For a TR-B audience, this is the right argument. Newell's model is widely accepted as first-order, the consistency argument is sound, and the scope boundary is clearly drawn. A referee reading this paragraph will see that the authors understand the limitation, have considered addressing it, and have a principled reason for not doing so. Verified: 1.5 cells/s^2 = v_f^2 / (2 * 9 cells) = 5.2^2 / 18 = 1.50 cells/s^2; 1.50 * 7.5 m = 11.3 m/s^2.

## Critical

None.

## Major (should fix before submission)

- **[Section 5, lines 759 and 926]** Python version contradicts itself within the same section. Line 759 says "Python~3.10"; line 926 says "Python (3.13)". The actual venv is Python 3.13.13. A referee reading Section 5 top to bottom sees both versions 167 lines apart, in text about reproducibility. **Suggested fix:** change "Python~3.10" at line 759 to "Python~3.13", or remove the version from line 759 entirely since line 926 states it precisely.

## Minor (polish)

- **[Section 5.7, line 1248]** "cells 250--260 ($\approx$75\,m incident zone)": cells 250 through 260 inclusive is 11 cells, and 11 * 7.5 m = 82.5 m, not 75 m. The code comment (`run_incident.py` line 39) has the same error. **Suggested fix:** either say "cells 250--259" (10 cells = 75 m) or "$\approx$82\,m."

- **[Section 3.7.2, line 410]** The AV controller interval is introduced as $\Delta t_{\text{ctrl}}$ but this symbol never appears again. Table 3 (line 873) lists the same quantity under $\delta_{\text{eval}}$ with the parenthetical "(controller cycle)." A referee looking for $\Delta t_{\text{ctrl}}$ in the parameters will not find it. **Suggested fix:** either use $\delta_{\text{eval}}$ at line 410 with a note that it is fixed for AVs, or add $\Delta t_{\text{ctrl}}$ to Table 3.

## Open questions for the author

- The first-order nature of the model is addressed in Section 4.3 but is not listed among the six items in the Limitations section (Section 6.1). A referee who thinks acceleration bounds matter might look there and not find it. This is a judgment call: Newell's model is well-accepted as first-order, and many papers using it do not list this as a limitation, so adding it risks inviting the demand for a fix. But omitting it risks looking like an oversight. The current placement in the body is defensible either way.

- Line 759 says Python 3.10: was the section-5 introduction written when the experiments were run on 3.10 (before the upgrade to 3.13), or is this simply a typo? If some early runs were on 3.10, that should be noted.

## Checks passed

- **Build.** 44 pages, 0 errors, 0 undefined references, 0 missing citations, 0 overfull boxes. Four hyperref warnings (harmless).
- **Citations.** 31 keys in tex, 31 keys in bib: exact one-to-one match. No orphans, no missing keys, no uncited entries.
- **Figures.** All 14 figure labels are referenced in the text and interpreted in prose. All captions stand alone.
- **Tables.** All 11 table labels are referenced in the text and discussed in prose.
- **Contributions alignment.** The 8 contributions in the introduction (lines 70-86) map one-to-one to the 8 items in the conclusion (lines 1280-1296). Each is paid off by a specific section: (1) Section 3 + 4.3; (2) Section 3.4; (3) Section 3.5 + 4.2; (4) Section 4.1 + 5.2; (5) Section 3.6 + 3.7; (6) Section 3.6 + 5.5 + 5.6; (7) Section 3.6.2 + 5.7; (8) Section 4.2.4 + 5.3.
- **Number traceability.** Every headline number verified against `code/manuscript_numbers.py` and `code/analyse_incident.py`:
  - 18.9% throughput: (6983.13 - 5874.22) / 5874.22 = 18.88%, rounds to 18.9%.
  - 95% delay reduction: (216.64 - 10.18) / 216.64 = 95.3%, rounds to 95%.
  - 99.8% demand served: 6983.13 / 7000 = 99.76%, rounds to 99.8%.
  - 83.9% demand served at S1: 5874.22 / 7000 = 83.9%.
  - 6.4% sensitivity improvement: (6251.89 - 5874.22) / 5874.22 = 6.43%, rounds to 6.4%.
  - Bottleneck 99.2% at 50% AV: 3571.07 / 3600 = 99.2%.
  - Factor of three in bottleneck delay: 18.1 / 6.1 = 2.97, correctly stated.
  - Incident: 4262 veh/h, 237.1 s delay, queue 0.94 km at reopening, 1.69 km peak at t = 1860 s, recovery at t = 2460 s (16 min): all match `analyse_incident.py` output.
  - Scalability exponent 0.86, wall-clock 16.9x for 16x length: match `manuscript_numbers.py`.
  - 131 s demand-weighted free-flow trip time (130.9 s from the script): match.
  - All Table 5 (S1-S4) and Table 6 (bottleneck) values: exact match.
  - Table 7 (sensitivity) values: exact match.
  - Table 8 (scalability) values: exact match.
  - Table 9 (computational) values: exact match (SimPy events, speed evaluations, CF evaluations, lane changes, wall-clock).
- **Rounding consistency.** Means round to nearest integer or one decimal; CI half-widths round up for integer presentation (5.79 to 6, 7.77 to 8) and to nearest for one-decimal presentation. The convention from round 3 holds throughout.
- **Abstract.** 189 words, under the 200-word TR-B guideline. Keeps the four key claims (paradigm, event-driven driver, analytical link, headline numbers). All numbers match the body.
- **Saturation framing.** The throughput-as-lower-bound-on-capacity argument is consistent across abstract, discussion (line 1066), bottleneck (line 1115), and conclusion (line 1302).
- **Event-count honesty.** The paper honestly acknowledges the unfavorable comparison at high AV share (7.08M evaluations vs 3.95M timestep updates at 70% AV) and attributes it to the fixed-rate AV controller (lines 1240-1241).
- **Statistical reporting.** All means accompanied by 95% CIs. Sensitivity scope note (N=10 vs N=20) properly disclosed (line 1163). Bottleneck CV analysis present (line 1119).
- **Warm-up justification.** The incident's 200 s vs. the main experiments' 300 s is now explained (line 1248).

## Verdict

**Ready for submission after one fix.** The Python version at line 759 is the only Major item. It is a one-word change ("3.10" to "3.13"). Two Minor items remain (incident zone length, dangling $\Delta t_{\text{ctrl}}$ notation) and one open question (first-order in Limitations). None of these would block submission.

The manuscript has 0 Critical and 1 Major item (a typo). After that fix, it has 0 Critical and 0 Major. This ends the review loop.
