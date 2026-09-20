"""Print every number the manuscript quotes, read from the aggregate CSVs and run files.

D-2026-09-20-1.

One place to look when restating the paper: each block names the manuscript element it feeds
(a table, a sentence, the abstract) and prints the values with their 95% intervals, so a number
is never typed from memory.

Usage:
    .venv/bin/python manuscript_numbers.py
"""

import csv
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import config

OUTPUT = Path("output")
S1_S4 = OUTPUT / "multiseed" / "s1_s4" / "aggregate.csv"
BOTTLENECK = OUTPUT / "multiseed" / "bottleneck" / "bottleneck_aggregate.csv"
SENSITIVITY = OUTPUT / "sensitivity_action_interval" / "comparison.csv"
SCALABILITY = OUTPUT / "scalability_benchmark.csv"
EXPERIMENTS = OUTPUT / "experiments"

SCENARIOS = ["S1_baseline", "S2_low_av", "S3_med_av", "S4_high_av"]
BN_SCENARIOS = ["BN_0av", "BN_30av", "BN_50av", "BN_70av"]


def read_aggregate(path):
    """{(scenario, action_interval): {metric: (n, mean, ci_lo, ci_hi)}} of one aggregate CSV.

    Args:
        path: the CSV written by aggregate_multiseed.py.
    """
    table = defaultdict(dict)
    if not path.exists():
        return table
    with open(path) as f:
        for row in csv.DictReader(f):
            interval = row.get("hdv_action_interval") or row.get("action_interval")
            table[(row["scenario"], float(interval))][row["metric"]] = (
                int(row["n"]), float(row["mean"]), float(row["ci95_lo"]), float(row["ci95_hi"]))
    return table


def show(title, table, scenarios, action_interval=1.0):
    """Print one aggregate table as mean +- half-interval.

    Args:
        title: the manuscript element it feeds.
        table: from `read_aggregate`.
        scenarios: row order.
        action_interval: which HDV action interval to show.
    """
    print(f"\n== {title}")
    for scenario in scenarios:
        stats = table.get((scenario, action_interval))
        if not stats:
            print(f"  {scenario}: missing")
            continue
        for metric, (n, mean, lo, hi) in stats.items():
            print(f"  {scenario:<12} {metric:<22} {mean:12.2f} +- {(hi - lo) / 2:7.2f}  (n={n})")


def show_single_runs():
    """The single-seed S1-S4 runs: the computational table (events, CF evaluations, wall time)."""
    print("\n== Table tab:computational (single seed, quiet machine)")
    for scenario in SCENARIOS:
        path = EXPERIMENTS / f"{scenario}.json"
        if not path.exists():
            print(f"  {scenario}: missing")
            continue
        record = json.load(open(path))
        counters, stats = record["counters"], record["stats"]
        keys = ("simpy_events", "cf_evaluations", "speed_evaluations", "lane_changes",
                "slowdowns", "av_controller_updates")
        values = "  ".join(f"{key}={counters.get(key, 0):,}" for key in keys)
        print(f"  {scenario:<12} {values}  wall={stats.get('wall_time_s', 0):.1f}s "
              f"completed={stats.get('num_completed', 0)}  "
              f"written={datetime.fromtimestamp(path.stat().st_mtime):%Y-%m-%d %H:%M}")


def show_free_flow_trip():
    """The demand-weighted free-flow trip time in the fig:travel_time caption."""
    print("\n== Caption fig:travel_time (demand-weighted free-flow trip time)")
    network, demand = config.S1_NETWORK, config.S1_DEMAND
    v_max = config.HDV_VEHICLE.v_max
    weighted = flow_total = 0.0
    for origin, destinations in demand.items():
        start = network.origins[origin].cell
        for destination, flow in destinations.items():
            cells = network.destinations[destination].cell - start
            weighted += flow * cells / v_max
            flow_total += flow
    print(f"  offered demand {flow_total:,.0f} veh/h over {len(demand)} origins")
    print(f"  weighted mean {weighted / flow_total:.1f} s against "
          f"{network.num_cells / v_max:.1f} s for the full {network.num_cells}-cell segment")


def show_scalability():
    """The scalability table and its sub-linear claim."""
    print("\n== Table tab:scalability")
    if not SCALABILITY.exists():
        print("  missing")
        return
    by_cells = defaultdict(lambda: defaultdict(list))
    with open(SCALABILITY) as f:
        rows = list(csv.DictReader(f))
    if "simpy_events" not in (rows[0] if rows else {}):
        print("  stale file: no simpy_events column, rerun run_scalability.py")
        return
    for row in rows:
        for key in ("simpy_events", "wall_clock_seconds", "realtime_ratio", "vehicles_generated"):
            by_cells[int(row["num_cells"])][key].append(float(row[key]))
    sizes = sorted(by_cells)
    for cells in sizes:
        values = by_cells[cells]
        mean = {k: sum(v) / len(v) for k, v in values.items()}
        print(f"  {cells:>5} cells/lane  total={cells * 4:>6}  "
              f"events={mean['simpy_events']:>12,.0f}  wall={mean['wall_clock_seconds']:>8.1f}s  "
              f"realtime={mean['realtime_ratio']:>6.2f}x  "
              f"generated={mean['vehicles_generated']:>7,.0f}")
    if len(sizes) > 1:
        small, large = sizes[0], sizes[-1]
        ratio = (sum(by_cells[large]["simpy_events"]) / sum(by_cells[small]["simpy_events"]))
        wall = (sum(by_cells[large]["wall_clock_seconds"])
                / sum(by_cells[small]["wall_clock_seconds"]))
        size_ratio = large / small
        exponent = math.log(ratio) / math.log(size_ratio)
        print(f"  events x{ratio:.2f} and wall x{wall:.2f} for a x{size_ratio:.0f} network: "
              f"empirical exponent {exponent:.2f}")


def main():
    """Print every block."""
    s1_s4 = read_aggregate(S1_S4)
    show("Table tab:results_mixed and the abstract (S1-S4, 20 seeds)", s1_s4, SCENARIOS)
    show("Table tab:bottleneck (20 seeds)", read_aggregate(BOTTLENECK), BN_SCENARIOS)
    sensitivity = read_aggregate(SENSITIVITY)
    print("\n== Sensitivity to the HDV action interval (S1)")
    for action_interval in sorted({ai for (label, ai) in sensitivity if label == "S1_baseline"}):
        show(f"action interval {action_interval}s", sensitivity, ["S1_baseline"], action_interval)
    show_single_runs()
    show_free_flow_trip()
    show_scalability()


if __name__ == "__main__":
    main()
