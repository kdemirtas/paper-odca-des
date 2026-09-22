"""Aggregate the per-seed JSONs of the batch output folders into the final CSVs.

The only writer of aggregate CSVs (D-2026-09-19-3); the interval is `odca.analysis.mean_ci95`
through `odca.experiment` (D-2026-09-19-9).

Walks:
  output/multiseed/s1_s4/batch*/         -> output/multiseed/s1_s4/
  output/multiseed/bottleneck/batch*/    -> output/multiseed/bottleneck/
  output/sensitivity_action_interval/ai_*/batch*/ -> output/sensitivity_action_interval/

Produces:
  output/multiseed/s1_s4/per_seed.csv, aggregate.csv
  output/multiseed/bottleneck/bottleneck_per_seed.csv, bottleneck_aggregate.csv
  output/sensitivity_action_interval/comparison.csv
"""
from __future__ import annotations

from pathlib import Path

from odca.experiment import aggregate, read_runs, write_aggregate_csv, write_per_seed_csv

ROOT = Path(__file__).parent / "output"

# occupancy and the failure counters beside the flow metrics (odca-des:D-2026-09-20-5, -12)
OCCUPANCY_METRICS = ["avg_cells_held", "avg_origin_wait", "num_never_entered",
                     "lc_patience_failures", "gap_rejections"]
S1_S4_METRICS = ["throughput_per_hour", "avg_travel_time", "avg_delay",
                 "pct_delayed_20s", "avg_lc_per_km", *OCCUPANCY_METRICS]
BOTTLENECK_METRICS = ["throughput_per_hour", "avg_delay", "avg_lc_per_km",
                      "avg_travel_time", "pct_delayed_20s", *OCCUPANCY_METRICS]


def aggregate_s1_s4():
    """per_seed.csv and aggregate.csv of the S1-S4 runs."""
    out_dir = ROOT / "multiseed" / "s1_s4"
    pattern = str(out_dir / "batch*" / "*.json")
    records = list(read_runs(pattern))
    if not records:
        print(f"[s1_s4] no JSONs at {pattern}")
        return
    write_per_seed_csv(out_dir / "per_seed.csv", records, S1_S4_METRICS,
                       order=lambda r: (r.label, r.seed))
    rows = aggregate(records, S1_S4_METRICS)
    write_aggregate_csv(out_dir / "aggregate.csv", rows)
    print(f"[s1_s4] wrote per_seed.csv ({len(records)} rows) and aggregate.csv ({len(rows)} rows)")


def aggregate_bottleneck():
    """bottleneck_per_seed.csv and bottleneck_aggregate.csv."""
    out_dir = ROOT / "multiseed" / "bottleneck"
    pattern = str(out_dir / "batch*" / "*.json")
    records = list(read_runs(pattern))
    if not records:
        print(f"[bottleneck] no JSONs at {pattern}")
        return
    write_per_seed_csv(out_dir / "bottleneck_per_seed.csv", records, BOTTLENECK_METRICS,
                       order=lambda r: (r.av_penetration or 0, r.seed))
    write_aggregate_csv(out_dir / "bottleneck_aggregate.csv",
                        aggregate(records, BOTTLENECK_METRICS))
    print("[bottleneck] wrote bottleneck_per_seed.csv and bottleneck_aggregate.csv")


def aggregate_sensitivity():
    """comparison.csv: the action-interval runs beside the S1-S4 runs at 1.0 s."""
    out_dir = ROOT / "sensitivity_action_interval"
    out_dir.mkdir(parents=True, exist_ok=True)
    records = [*read_runs(str(ROOT / "multiseed" / "s1_s4" / "batch*" / "*.json")),
               *read_runs(str(out_dir / "ai_*" / "batch*" / "*.json"))]
    rows = aggregate(records, S1_S4_METRICS)
    write_aggregate_csv(out_dir / "comparison.csv", rows, interval_column="action_interval")
    print(f"[sensitivity] wrote comparison.csv ({len({r.group for r in rows})} "
          f"(scenario,ai) groups)")


if __name__ == "__main__":
    aggregate_s1_s4()
    aggregate_bottleneck()
    aggregate_sensitivity()
    print("Aggregation complete.")
