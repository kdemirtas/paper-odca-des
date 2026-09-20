# N11: before and after, every manuscript number the rerun moved

Left: the manuscript before the 2026-09-20 rerun (`paper/paper-odca-des-prerevision-2.tex`).
Right: the restated text, read from `code/output/` by `code/manuscript_numbers.py`.
Unchanged rows are left out; the theoretical-capacity table did not move (it is analytic).

## `tab:results_mixed`

| row | before | after |
|---|---|---|
| Throughput (veh/h) | 4,494 +- 14 & 5,416 +- 24 & 6,423 +- 25 & 6,664 +- 48 | 5,874 +- 19 & 6,679 +- 25 & 6,972 +- 34 & 6,983 +- 34 |
| Avg.\ travel time (s) | 380.8 +- 6.5 & 329.7 +- 6.5 & 235.2 +- 10.2 & 158.1 +- 1.1 | 347.4 +- 5.7 & 250.4 +- 12.2 & 159.3 +- 1.0 & 141.6 +- 0.4 |
| Avg.\ delay (s) | 254.1 +- 6.6 & 201.3 +- 6.6 & 105.0 +- 10.3 & 27.6 +- 1.1 | 216.6 +- 5.8 & 119.1 +- 12.2 & 27.9 +- 0.9 & 10.2 +- 0.3 |
| LC frequency (/veh/km) | 4.89 +- 0.02 & 3.49 +- 0.02 & 2.23 +- 0.04 & 1.22 +- 0.01 | 2.53 +- 0.01 & 1.99 +- 0.04 & 1.20 +- 0.01 & 0.72 +- 0.01 |
| Vehicles delayed $>20$\,s (\%) | not reported | 99.9 +- 0.0 & 97.6 +- 0.6 & 66.3 +- 2.2 & 9.9 +- 1.0 |

## `tab:results_bottleneck`

| row | before | after |
|---|---|---|
| Throughput (veh/h) | 1,341 +- 111 & 1,569 +- 99 & 1,773 +- 164 & 1,780 +- 174 | 2,501 +- 11 & 3,127 +- 23 & 3,571 +- 34 & 3,602 +- 41 |
| Avg.\ travel time (s) | not reported | 378.2 +- 7.8 & 236.5 +- 11.6 & 133.3 +- 2.1 & 121.3 +- 0.3 |
| Avg.\ delay (s) | 318.1 +- 32.0 & 320.3 +- 43.2 & 214.7 +- 42.9 & 142.3 +- 42.6 | 263.0 +- 7.8 & 121.3 +- 11.6 & 18.1 +- 2.1 & 6.1 +- 0.3 |
| LC frequency (/veh/km) | 2.11 +- 0.26 & 1.59 +- 0.14 & 1.22 +- 0.14 & 0.74 +- 0.07 | 1.09 +- 0.01 & 0.96 +- 0.02 & 0.59 +- 0.01 & 0.35 +- 0.01 |
| Vehicles delayed $>20$\,s (\%) | not reported | 97.3 +- 0.4 & 94.2 +- 2.0 & 34.7 +- 6.2 & 2.1 +- 0.6 |

## `tab:sensitivity_ai`

| row | before | after |
|---|---|---|
| Throughput (veh/h) | 4,870 +- 16 & 4,762 +- 23 & 4,494 +- 14 | 6,252 +- 32 & 6,164 +- 26 & 5,874 +- 19 |
| Avg.\ travel time (s) | 330.2 +- 4.1 & 346.4 +- 8.6 & 380.8 +- 6.5 | 326.2 +- 8.2 & 329.9 +- 7.7 & 347.4 +- 5.7 |
| Avg.\ delay (s) | 202.6 +- 4.2 & 219.0 +- 8.6 & 254.1 +- 6.6 | 194.3 +- 8.1 & 198.6 +- 7.7 & 216.6 +- 5.8 |
| LC frequency (/veh/km) | 4.10 +- 0.02 & 4.39 +- 0.03 & 4.89 +- 0.02 | 2.15 +- 0.01 & 2.30 +- 0.01 & 2.53 +- 0.01 |

## `tab:scalability`

| row | before | after |
|---|---|---|
| Cells/lane | Total cells & Events (\times 10^3) & Wall clock (s) & Realtime ratio | Total cells & SimPy events (\times 10^6) & Wall clock (s) & Realtime ratio |
| 200 | 800 & 394 & 227 & 8.0\times | 800 & 6.01 & 18.0 & 100.3\times |
| 400 | 1,600 & 619 & 370 & 5.2\times | 1,600 & 11.31 & 35.9 & 50.2\times |
| 800 | 3,200 & 910 & 448 & 4.1\times | 3,200 & 20.78 & 71.2 & 25.3\times |
| 1{,}600 | 6,400 & 1,364 & 786 & 2.3\times | 6,400 & 37.87 & 147.1 & 12.2\times |
| 3{,}200 | 12,800 & 1,935 & 1,533 & 1.2\times | 12,800 & 65.05 & 304.3 & 5.9\times |

## `tab:computational`

| row | before | after |
|---|---|---|
| SimPy events ($\times 10^6$) | not reported | 40.0 & 41.0 & 39.3 & 38.5 |
| Speed evaluations ($\times 10^6$) | not reported | 2.20 & 6.19 & 6.03 & 7.08 |
| of which car following ($\times 10^6$) | not reported | 1.89 & 5.55 & 4.86 & 5.32 |
| Timestep updates ($\times 10^6$) | 6.4 & 6.4 & 6.8 & 5.8 | 7.41 & 6.47 & 4.43 & 3.95 |
| Lane changes | 126,773 & 105,959 & 80,206 & 42,334 | 76,837 & 67,680 & 41,280 & 24,928 |
| Average vehicles in network | not reported | 515 & 449 & 308 & 274 |
| Wall-clock time --- ODCA-DES (s) | 802 & 477 & 318 & 277 | 150 & 166 & 147 & 142 |

## Prose and captions

| claim | before | after |
|---|---|---|
| abstract, throughput gain 0 to 70% AV | 48% | 18.9% |
| abstract, delay reduction | 89% (254 +- 7 to 28 +- 1 s) | 95% (217 +- 6 to 10.2 +- 0.3 s) |
| abstract, bottleneck plateau | ~1,773 veh/h, merge saturation | two open lanes carry the full 3,600 veh/h from 50% AV; delay 263 +- 8 to 6.1 +- 0.3 s |
| results, throughput CV | < 1.6% | 0.7 to 1.1% |
| bottleneck, CV claim | 10 to 21% throughput | 0.9 to 2.4% throughput, up to 24% delay |
| sensitivity, 1.0 s to 0.25 s | 8.4% throughput, 20% delay | 6.4% throughput, 10% delay |
| computational note, wall clock | 277 to 802 s, 4.5 to 13x real time | 142 to 166 s, 22 to 25x real time |
| event count, S1 decisions vs timestep | 2.09M CF evaluations vs 6.4M updates | 2.20M speed evaluations vs 7.41M updates; at 70% AV 7.08M vs 3.95M |
| scalability, growth | events x4.9, wall x6.8, exponent 0.57 | events x10.8, wall x16.9, exponent 0.86 |
| scalability, real-time ratio | 8.0x to 1.2x | 100x to 5.9x |
| incident scenario | one lane closed, 3,000 veh/h, queue to t~3000 s, 25 min recovery | lanes 3 and 4 closed, 4,500 veh/h, queue 0.94 km at reopening to 1.69 km, 16 min recovery |
| FD capacity | envelope closely follows theory | ring road 1,948 to 1,978 veh/h (92 to 93% of 2,127); open sweep peaks at 1,587 |
| travel-time figure reference | full-segment free flow 154 s | demand-weighted free-flow trip 131 s |
