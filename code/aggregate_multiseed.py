"""Aggregate per-seed JSONs from the Phase 1 batch output dirs into final CSVs.

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

import csv
import glob
import json
import math
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent / "output"

# ---- small t-table (same as run_experiments.py) ----
T_TABLE = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
    8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
    15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080,
    22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048,
    29: 2.045, 30: 2.042,
}

def t_crit(df):
    if df in T_TABLE:
        return T_TABLE[df]
    return 1.96 if df > 30 else T_TABLE[30]

def ci95(values):
    n = len(values)
    if n == 0:
        return (float('nan'),) * 4
    mean = sum(values) / n
    if n == 1:
        return mean, 0.0, mean, mean
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    std = math.sqrt(var)
    sem = std / math.sqrt(n)
    t = t_crit(n - 1)
    return mean, std, mean - t * sem, mean + t * sem


def collect_jsons(pattern):
    """Yield (path, json) for all JSON files matching pattern."""
    for p in sorted(glob.glob(pattern, recursive=True)):
        with open(p) as f:
            try:
                yield Path(p), json.load(f)
            except Exception as e:
                print(f"  skip unreadable {p}: {e}")


def aggregate_s1_s4():
    out_dir = ROOT / "multiseed" / "s1_s4"
    pattern = str(out_dir / "batch*" / "*.json")
    rows = list(collect_jsons(pattern))
    if not rows:
        print(f"[s1_s4] no JSONs at {pattern}"); return

    # per_seed.csv: rows are (label, av_pen, seed, hdv_action_interval, metrics...)
    # Extract metrics from each JSON. Based on smoketest layout:
    metric_keys = ["throughput_per_hour", "avg_travel_time", "avg_delay",
                   "pct_delayed_20s", "avg_lc_per_km"]
    per_seed_rows = []
    # group for aggregation: (label, av_pen) -> {metric: [values across seeds]}
    groups = defaultdict(lambda: defaultdict(list))
    for _, j in rows:
        label = j["label"]
        av_pen = j.get("av_penetration")
        seed = j.get("seed")
        ai = j.get("hdv_action_interval", 1.0)
        stats = j.get("stats", j)  # stats nested or flat
        row = {"label": label, "av_penetration": av_pen, "seed": seed,
               "hdv_action_interval": ai}
        for m in metric_keys:
            v = stats.get(m)
            if v is None and "num_completed" in stats and m == "throughput_per_hour":
                # fallback if structure differs
                v = stats.get("throughput_per_hour")
            row[m] = v
            if v is not None:
                groups[(label, av_pen, ai)][m].append(v)
        per_seed_rows.append(row)

    # write per_seed.csv
    fieldnames = ["label", "av_penetration", "seed", "hdv_action_interval"] + metric_keys
    with open(out_dir / "per_seed.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in sorted(per_seed_rows, key=lambda x: (x["label"], x["seed"])):
            w.writerow(r)

    # aggregate.csv
    with open(out_dir / "aggregate.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "av_penetration", "hdv_action_interval", "metric",
                    "n", "mean", "std", "ci95_lo", "ci95_hi"])
        for (label, av_pen, ai), metrics in sorted(groups.items()):
            for m, vals in metrics.items():
                mean, std, lo, hi = ci95(vals)
                w.writerow([label, av_pen, ai, m, len(vals),
                            f"{mean:.6f}", f"{std:.6f}",
                            f"{lo:.6f}", f"{hi:.6f}"])

    print(f"[s1_s4] wrote per_seed.csv ({len(per_seed_rows)} rows) and "
          f"aggregate.csv ({sum(len(m) for m in groups.values())} rows)")


def aggregate_bottleneck():
    out_dir = ROOT / "multiseed" / "bottleneck"
    pattern = str(out_dir / "batch*" / "*.json")
    rows = list(collect_jsons(pattern))
    if not rows:
        print(f"[bottleneck] no JSONs at {pattern}"); return

    metric_keys = ["throughput_per_hour", "avg_delay", "avg_lc_per_km",
                   "avg_travel_time", "pct_delayed_20s"]
    per_seed_rows = []
    groups = defaultdict(lambda: defaultdict(list))
    for _, j in rows:
        label = j["label"]
        av_pen = j.get("av_penetration")
        seed = j.get("seed")
        ai = j.get("hdv_action_interval", 1.0)
        stats = j.get("stats", j)
        row = {"label": label, "av_penetration": av_pen, "seed": seed,
               "hdv_action_interval": ai}
        for m in metric_keys:
            v = stats.get(m)
            row[m] = v
            if v is not None:
                groups[(label, av_pen, ai)][m].append(v)
        per_seed_rows.append(row)

    with open(out_dir / "bottleneck_per_seed.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["label", "av_penetration", "seed",
                                          "hdv_action_interval"] + metric_keys)
        w.writeheader()
        for r in sorted(per_seed_rows, key=lambda x: (x["av_penetration"] or 0, x["seed"])):
            w.writerow(r)

    with open(out_dir / "bottleneck_aggregate.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "av_penetration", "hdv_action_interval", "metric",
                    "n", "mean", "std", "ci95_lo", "ci95_hi"])
        for (label, av_pen, ai), metrics in sorted(groups.items()):
            for m, vals in metrics.items():
                mean, std, lo, hi = ci95(vals)
                w.writerow([label, av_pen, ai, m, len(vals),
                            f"{mean:.6f}", f"{std:.6f}",
                            f"{lo:.6f}", f"{hi:.6f}"])
    print(f"[bottleneck] wrote bottleneck_per_seed.csv and bottleneck_aggregate.csv")


def aggregate_sensitivity():
    """Walk ai_*/batch*/*.json and also include WS-1 (ai=1.0) from multiseed/s1_s4 for comparison."""
    out_dir = ROOT / "sensitivity_action_interval"
    out_dir.mkdir(parents=True, exist_ok=True)

    # include WS-1 (ai=1.0) baseline so comparison.csv has all three values
    pattern_ws1 = str(ROOT / "multiseed" / "s1_s4" / "batch*" / "*.json")
    pattern_sens = str(out_dir / "ai_*" / "batch*" / "*.json")

    metric_keys = ["throughput_per_hour", "avg_travel_time", "avg_delay",
                   "pct_delayed_20s", "avg_lc_per_km"]
    groups = defaultdict(lambda: defaultdict(list))

    for src_pattern in (pattern_ws1, pattern_sens):
        for _, j in collect_jsons(src_pattern):
            label = j["label"]
            av_pen = j.get("av_penetration")
            ai = j.get("hdv_action_interval", 1.0)
            stats = j.get("stats", j)
            for m in metric_keys:
                v = stats.get(m)
                if v is not None:
                    groups[(label, av_pen, ai)][m].append(v)

    with open(out_dir / "comparison.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "av_penetration", "action_interval", "metric",
                    "n", "mean", "std", "ci95_lo", "ci95_hi"])
        for (label, av_pen, ai), metrics in sorted(groups.items(), key=lambda x: (x[0][0], x[0][2])):
            for m, vals in metrics.items():
                mean, std, lo, hi = ci95(vals)
                w.writerow([label, av_pen, ai, m, len(vals),
                            f"{mean:.6f}", f"{std:.6f}",
                            f"{lo:.6f}", f"{hi:.6f}"])
    print(f"[sensitivity] wrote comparison.csv ({len(groups)} (scenario,ai) groups)")


if __name__ == "__main__":
    aggregate_s1_s4()
    aggregate_bottleneck()
    aggregate_sensitivity()
    print("Aggregation complete.")
