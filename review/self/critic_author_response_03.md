# Author response to critic report 03, 2026-09-20

Every item of report 03 is answered below: 3 Major, 6 Minor, plus the two open questions. All are
applied in the manuscript unless the row says otherwise. Build after the changes: 42 pages,
0 errors, 0 undefined references, 0 missing citations, no overfull box.

## Major

**M1. "All" of the bottleneck demand from 50% AV (abstract, conclusion, fig:bottleneck_throughput
caption).** Agreed, the three summaries overstated what Table 6 shows. All three now say 99% (99.2%
where the precise figure fits) at 50% AV and all of it at 70%, matching the body text.

**M2. Conclusion drops the fundamental-diagram number.** Agreed. The conclusion now reads "on a ring
road, which removes the entry boundary effect, the simulated capacity reaches 92 to 93% of the
analytic q_max", the figure Section 5.2 reports.

**M3. The 131 s free-flow trip time is named but not derived.** Agreed, and taken one step further
than suggested. The caption now says what the quantity is (the mean of each origin-destination
pair's free-flow time weighted by its flow), why it is shorter than the 154 s full-segment time
(most traffic leaves at off-ramps 1 to 3), points at the demand section that gives the flows, and
names the script that reproduces it. `code/manuscript_numbers.py` gained that calculation, so the
number now has a source like every other number in the paper: 130.9 s against 153.8 s for the full
800 cells.

## Minor

**m1. Cassidy (1998) for incident recovery hysteresis.** Agreed: Cassidy and Bertini (1999), "Some
traffic features at freeway bottlenecks", is the reference for the reduced discharge capacity after
a bottleneck activates, and Section 5.7 now cites it (`cassidy1999some`) with the sentence reworded
to say reduced discharge capacity rather than hysteresis. Added through the bibliography skills and
verified against CrossRef.

**m2. Scalability caption omits the 0.86 exponent.** Applied: the caption now reads "sub-linearly
(empirical exponent 0.86)".

**m3. S1 label reused for a half-demand experiment (Section 5.3).** Applied: "the baseline
parameters of Table 3 with mainline demand reduced to 3,000 veh/h".

**m4. Three bib key-year mismatches.** Fixed through the bibliography skills, which checked each
year field against CrossRef first: in all three the field was right and the key was wrong, so the
keys moved, `knospe2004towards` to `knospe2000towards`, `barcelo2005fundamentals` to
`barcelo2010models`, `osorio2015urban` to `osorio2013simulation`, with the `\cite` commands in the
same pass. A fourth of the same kind that the report did not list, `banks2014discrete` against its
2010 year field, is fixed too (`banks2010discrete`). All 31 entries verified, no orphan, no uncited
entry, no undefined citation in the build.

**m5. Abstract at about 400 words against the journal's 200.** Applied: rewritten at 198 words,
keeping the protocol, the event-driven driver, the analytical link, and the headline numbers
(18.9% throughput, 95% delay, 99.8% of demand served). What went: the second paragraph's detail on
lane-change gaps and urgency inflation, and the bottleneck's individual figures, all of which the
body carries. The 408-word version is in the git history and in
`paper/paper-odca-des-prerevision-2.tex` if Kerem prefers it back (`ASSUMPTIONS.md` A-2026-09-20-3).

**m6. Warm-up differs between S1 to S4 (300 s) and the incident (200 s).** Applied: Section 5.7 now
says why, that the road starts populated and is shorter, so a vehicle entering at t = 0 has left
before the closure, and that the measurement is the transient timed from the closure rather than a
steady-state mean.

## Open questions

**"Is 100% at 50% AV a deliberate rounding?"** No, an oversight. Fixed as M1 says.

**"Is there an analytical expression for the 131 s?"** Yes, and it is now in the caption:
sum over origin-destination pairs of flow times cells over v_f, divided by the total flow. The
calculation is in `code/manuscript_numbers.py`.

## Not changed

Nothing in the report was declined.
