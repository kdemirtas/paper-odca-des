# Critic report -- ODCA-DES -- iteration 3 -- 2026-09-20

Context: the full experimental rerun of 2026-09-20 changed every number in the manuscript (see review/self/n11_before_after.md). The text was rewritten against fresh outputs. This review assesses the restated manuscript on its own terms: narrative coherence after the rewrite, whether each claim is still supported by the number beside it, consistency of the saturation framing across abstract/results/conclusion, citation coverage for new claims, and figure/table utilisation.

Items from reports 01 and 02 that were resolved are not re-raised. Items that remain open are noted with their original report number.

## Verification of prior items

- All Critical items from report 01: resolved. The 131 s free-flow time is now named ("demand-weighted free-flow trip time") in the fig:travel_time caption and the body no longer asserts it as a bare number. However, it is still not derivable from the manuscript (see Major 3 below).
- All Major items from report 01: resolved. Contributions 8/8 match; CIs consistently rounded; bottleneck delay discussed; merge-saturation claim removed; dead bib entries cited; sensitivity CIs have values; machine specs present.
- Major item from report 02 (abstract delay rounding): resolved by the rewrite (new numbers throughout).
- Minor item from report 02 (sec:example label): resolved (label removed).
- Formatting items from report 01 (bib key-year mismatches): **not resolved** (see Minor 4 below).

## Critical

None.

## Major (should fix before submission)

- **[Abstract, line 50; Conclusion, line 1281; fig:bottleneck_throughput caption, line 1103]** The abstract says the two remaining lanes "carry ... all of it at 50% AV and above." The conclusion says "the full 3,600 veh/h from 50% AV at the lane drop." The caption says "the two remaining lanes already carry the full 3,600 veh/h demand." But Table 6 shows BN_50% throughput of $3{,}571 \pm 34$ veh/h, which is 99.2% of the 3,600 demand, not 100%. Only BN_70% ($3{,}602 \pm 41$) actually reaches the full demand. The body text at line 1094 is precise ("99.2%... at 70% they carry all of it"). The abstract, conclusion and caption overstate. **Suggested fix:** say "essentially all of it from 50% AV" or "99% from 50% AV and all of it at 70%," matching the body text.

- **[Conclusion, line 1281]** "The fundamental diagram validation confirmed close agreement with the theoretical triangular FD" drops the quantification from Section 5.2, where the ring-road simulation reaches 92--93% of the analytic capacity. A reviewer who reads the 7--8% shortfall in Section 5.2 and then reads "close agreement" in the conclusion will want the number. **Suggested fix:** add "within 8% of the analytic capacity on a ring road" or reproduce the 92--93% figure.

- **[fig:travel_time caption, line 1061]** The "demand-weighted free-flow trip time of 131 s" is named but not derived. A reader can verify 154 s (800 cells x 7.5 m / 140 km/h) from the parameters, but 131 s requires knowing the OD split and each trip's cell count. The body text does not show that calculation. This was the Critical item in report 01; the fix was to name the quantity, which is half the job. **Suggested fix:** add one sentence or parenthetical: "shorter than the full-segment 154 s because a share of the traffic exits at off-ramps 1--3 before the segment end" (that is sufficient to make the direction obvious; the exact weighting can stay in the code).

## Minor (polish)

- **[Section 5.7, line 1242]** "The queue discharges more slowly than it formed, the hysteresis that empirical studies of incident recovery report (Cassidy 1998)." Cassidy (1998) is about bivariate flow-density relations in nearly stationary traffic. The canonical reference for capacity drop and slower-than-expected discharge after incidents is Cassidy and Bertini (1999, "Some traffic features at freeway bottlenecks," Transportation Research Part B 33(1):25--42). **Suggested fix:** cite Cassidy and Bertini (1999) here instead of or alongside Cassidy (1998), or soften to "consistent with empirical observations of reduced discharge capacity."

- **[fig:scalability caption, line 1173]** "Event count scales sub-linearly with network size" -- the body states the exponent is 0.86, but the caption omits it. Captions should be readable without the body. **Suggested fix:** "sub-linearly (empirical exponent 0.86)."

- **[Section 5.3, line 952]** "S1 parameters with reduced mainline demand of 3,000 veh/h" reuses the S1 label for an experiment at half the demand. Unchanged from report 01. **Suggested fix:** "the baseline parameters (Table 3) with mainline demand reduced to 3,000 veh/h" avoids the S1 collision.

- **[references.bib]** Three key-year mismatches from report 01 remain:
  - `knospe2004towards`: key says 2004, year field is 2000.
  - `barcelo2005fundamentals`: key says 2005, year field is 2010.
  - `osorio2015urban`: key says 2015, year field is 2013.
  These do not affect the rendered PDF (elsarticle-harv prints author-year from the bib fields), but they will confuse anyone who reads the .bib file and could trip a reviewer who checks references by key name. **Suggested fix:** rename keys to match years and update cite commands.

- **[Abstract]** Word count is approximately 400 words. Transportation Research Part B guidelines ask for a maximum of 200 words. Whether this is enforced at review or only at copyediting varies, but it is worth being aware of.

- **[Sections 5.2 and 5.7]** Warm-up periods differ: 300 s for S1--S4 (line 986), 200 s for the incident scenario (line 1227). The difference is not motivated. Not necessarily wrong (the incident uses a pre-initialized road and a shorter segment), but a sentence of justification would pre-empt the question.

## Open questions for the author

- The conclusion says "the full 3,600 veh/h from 50% AV." Is this a deliberate rounding of 99.2% to 100%, or an oversight? If deliberate, say "essentially all" and note the precise figure in Section 5.4 covers the nuance.
- The 131 s number: is there an analytical expression (weighted average of OD-pair trip lengths at free-flow speed) that could go in a footnote, or is it purely an output of the simulation? If the latter, say so ("computed from the OD demand table and the network geometry; the calculation is reproduced by ...").

## Checks passed

- All 30 citation keys match bib entries one-to-one: no orphans, no missing keys.
- All 13 figures are referenced in text and described in prose. All 11 tables likewise.
- Contributions in introduction (8 items) match conclusion (8 items), each clearly corresponding.
- Build: 0 errors, 0 undefined references, 0 missing citations, 0 overfull boxes. The 4 warnings are harmless elsarticle/hyperref metadata issues.
- The 18.9% throughput gain, 95% delay reduction, 99.8% demand served, 6.4% sensitivity gain, 0.86 scalability exponent, and all five table means and CIs are internally consistent between abstract, body, tables, figure captions, and conclusion.
- Rounding from body to abstract is consistent: means round to nearest integer, halfwidths round up (e.g. 5.8 to 6, 7.8 to 8).
- The saturation framing (throughput as lower bound on capacity, delay as the continued benefit) is consistent across abstract, results discussion, and conclusion.
- The event-count argument honestly acknowledges the unfavourable comparison at high AV share (7.08M evaluations vs 3.95M timestep updates at 70% AV) and attributes it to the fixed-rate AV controller.
- Sensitivity scope note (N=10 vs N=20, wider CIs) is properly disclosed (line 1142).
- Machine specs present in Section 5.1 (Intel i7-1255U, 12 cores, 32 GB RAM, Python 3.13, SimPy 4.1).
- The incident scenario change (one lane at 3,000 veh/h to two lanes at 4,500 veh/h) is clearly described with quantitative metrics (queue length, recovery time).
- The sec:example unused label is gone.

## VERDICT: ready-for-fixes (3 Major, 6 Minor, 0 Critical)
