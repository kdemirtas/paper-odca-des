# Critic report -- ODCA-DES -- 2026-04-21

## Critical (must-fix before submission)

- **[Section 5.3 Discussion, line 1038, fig:travel_time caption]** Caption states "approaching the theoretical free-flow travel time of 131\,s" but the full-segment free-flow travel time is 800/5.2 = 153.8\,s. The 131\,s figure is presumably the OD-weighted average free-flow trip time (since many vehicles exit before cell 800), but this is never stated or derived. An unexplained number that contradicts the verifiable full-segment value will confuse reviewers. **Fix:** Either derive the 131\,s explicitly (state it is the weighted-average free-flow time across the OD distribution) or replace with the full-segment value of 154\,s and adjust the claim, or remove the comparison entirely.

- **[Section 5.5, line 1088]** Sensitivity analysis uses N=10 replications for ai=0.25 and ai=0.5, vs N=20 for the baseline ai=1.0. The asymmetric N is disclosed, but the 95% CIs are computed with different degrees of freedom and are not directly comparable. For a 3-point sensitivity curve this is a reviewable weakness. **Fix:** Add one sentence acknowledging the statistical asymmetry (we already ruled out re-running in the scope pivot — see STATUS.md session 7).

## Major (should-fix)

- **[Abstract line 50 vs Section 5.3 line 992]** Abstract reports delay CIs as $254 \pm 7$ and $28 \pm 1$; body reports $254.1 \pm 6.6$ and $27.6 \pm 1.1$. Half-widths round in opposite directions. **Fix:** Use consistent rounding (round half-widths up, or both to nearest integer).

- **[Section 5.4, line 1069]** Bottleneck delay for BN_0% ($318.1 \pm 32.0$\,s) and BN_30% ($320.3 \pm 43.2$\,s) shows no improvement with 30% AVs despite a 17% throughput increase. Counter-intuitive; undiscussed. **Fix:** Add one sentence: higher throughput at BN_30 means more vehicles complete long-delay trips that would have been blocked at BN_0; per-vehicle delay stays similar. Alternatively, note the CIs overlap.

- **[Section 5.4, line 1071]** The "capacity-limited merge saturation" mechanism claim invokes $q_{\max}(\alpha)$ flattening, but $q_{\max}(\alpha)$ is concave, not flat. The plateau is empirical, not a theoretical prediction from Eq. 21. **Fix:** Soften to "qualitatively consistent with the concavity of the theoretical capacity function"; attribute plateau to merge dynamics not captured in the idealized single-stream capacity formula.

- **[references.bib]** Two uncited entries: `daganzo2005variational`, `greenshields1935study`. Dead weight. **Fix:** Either cite them (Greenshields in the FD discussion, Daganzo 2005 in the variational theory context) or remove.

- **[Section 5.5, line 1113]** Bare mean values "(from 254 to 203\,s)" without CIs, inconsistent with the rest of the section. **Fix:** Report as "from $254 \pm 7$ to $203 \pm 4$\,s" or reference the table.

- **[Section 1 lines 73-85 vs Section 6 lines 1229-1245]** Intro lists 6 contributions; conclusion lists 8. Items 6 (lane-change safety) and 8 (closed-form capacity) in conclusion are not previewed. **Fix:** Expand intro to 8 or consolidate conclusion to 6.

- **[Section 5.6, line 1187 / computational claims]** Table 8 wall-clock times and Section 6 "real-time ratios of 1.2-8.0×" lack machine specs. **Fix:** Add one sentence in Section 5.1 with CPU (Intel i7-1255U), RAM (32GB), Python version (3.10.18). Also note how wall-clock was measured.

## Minor (nice-to-fix)

- **[Section 5.6, line 1152]** "Sub-linearly" is accurate but imprecise. 4.9× events for 16× cells ≈ $O(n^{0.57})$. **Fix:** State empirical exponent explicitly.

- **[Section 5.2, line 931]** Uses "S1" label for a different-demand experiment (3000 veh/h vs main 6000 veh/h). **Fix:** Clarify "S1 parameters with reduced demand" or rename.

- **[Section 5.3, line 992 vs line 1026]** LC frequency values in both table and discussion paragraph — redundancy. **Fix:** Keep table; reduce paragraph to interpretation only.

- **[Section 4.3, line 644]** `sec:example` label is unused. **Fix:** Remove or add forward reference.

- **[Section 5.4, line 1073]** "Coefficient of variation 10-21%" would be stronger with S1-S4 CV range for direct comparison. **Fix:** Add "(compared to 0.7-1.6\% for S1-S4)" inline.

- **[Abstract, line 50]** Plateau finding stated qualitatively without the anchor number. **Fix:** Add "≈1,775\,veh/h" parenthetically.

- **[Section 6 Conclusion, line 1253]** Machine specs for real-time ratios missing. (Covered by Major fix above.)

## Formatting

- **[Line 1221]** `\clearpage` before Conclusion may cause awkward half-empty page in final format. **Fix:** Remove unless needed to anchor a float.

- **[Lines 1000-1014, Table 6]** Theoretical capacity table placement — confirm `[ht]` is robust, consider `[t]`.

- **[references.bib, line 35]** `knospe2004towards` has year=2000; key says 2004. **Fix (Phase 6):** Rename key to `knospe2000towards`, update .tex cite.

- **[references.bib, line 220]** `barcelo2005fundamentals` has year=2010; key says 2005. **Fix (Phase 6):** Rename to `barcelo2010fundamentals`.

- **[references.bib, line 229]** `osorio2015urban` has year=2013, volume=61. **Fix (Phase 6):** Rename to `osorio2013urban`.

## VERDICT

VERDICT: ready-for-fixes

---

## Not-verifiable-locally

- Table 8 wall-clock times (802, 477, 318, 277\,s for S1-S4): no CSV source. Presumably from experiment logs.
- "131\,s theoretical free-flow travel time": would require OD distribution code to compute weighted average trip length.
- CF evaluation counts in Table 8: not in aggregate CSV.

## Follow-ups

- **paper-author (Phase 5)**: apply Critical + Major items. Minor optional if trivial.
- **bibliography (Phase 6)**: already in flight. Will handle key-year mismatches and dead entries.
