# Critic report -- ODCA-DES -- iteration 2 -- 2026-04-21

## Verification of critic_report_01 items
- All Critical items: resolved.
- Major items: 6 of 7 resolved. One new Major arose from the iteration-1 fix overshooting (see below).
- Minor/Formatting: mostly resolved.

## Critical
None.

## Major
- **[Abstract line 50, Conclusion line 1256]** Delay CI "$28 \pm 2$" inconsistent with body table "$27.6 \pm 1.1$". Throughput CIs round nearest (14.2→14, 48.4→48); delay CI 1.1 should round to 1, not 2. **Fix:** "$28 \pm 2$" → "$28 \pm 1$".

## Minor
- **[Abstract line 50]** Plateau throughput "$\approx 1{,}775$\,veh/h" vs body/CSV 1,772.5 → rounds to 1,773. **Fix:** "$\approx 1{,}773$\,veh/h".
- **[Section 5.6, line 1158]** "Faster-than-realtime execution" at largest network — mean is 1.2× but one seed recorded 0.97×. **Fix:** "near-realtime or faster execution".
- **[Section 4.3, line 648]** Unused `\label{sec:example}`. **Fix:** Remove or add `\ref{}`.

## Formatting
- **[Table 5]** Mixed precision — throughput halfwidths integer, delay halfwidths one decimal. Not wrong; polish only.

## VERDICT: ready-for-fixes (single Major + 3 minor)
