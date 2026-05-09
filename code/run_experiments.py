"""Run all ODCA-DES experiments for the paper.

Scenarios:
  S1: Baseline       (0% AV)
  S2: Low AV          (30% AV)
  S3: Medium AV       (50% AV)
  S4: High AV         (70% AV)

Each scenario runs for 3600s with 300s warmup.

Single-seed mode (default): outputs to output/experiments/ as before.
Multi-seed mode (--seeds 1 2 3 ...): writes per-seed JSONs to a target
directory, plus an aggregate CSV with mean and 95% CI (t-distribution).
HDV action_interval may be overridden with --action-interval.
"""

import argparse
import logging
import json
import csv
import math
import time
from dataclasses import replace
from pathlib import Path

from config import SimConfig, HDV_PARAMS
from odca.simulation.engine import Simulation
from odca.analysis.metrics import summary_statistics, passage_time_flow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SCENARIOS = [
    ("S1_baseline", 0.0),
    ("S2_low_av", 0.3),
    ("S3_med_av", 0.5),
    ("S4_high_av", 0.7),
]

# Measurement cells for FD data (spaced across the 800-cell network)
FD_MEASUREMENT_CELLS = [150, 250, 450, 650]


# ──────────────────────────────────────────────────────────────────────
# Student's t critical values at 95% confidence (two-tailed), df = n-1
# Hard-coded to avoid a scipy dependency.
# ──────────────────────────────────────────────────────────────────────
T_95_TABLE = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
}


def t_critical_95(df: int) -> float:
    if df <= 0:
        return float("nan")
    if df in T_95_TABLE:
        return T_95_TABLE[df]
    if df > 30:
        # large-sample approximation converges to z = 1.96
        return 1.96
    return T_95_TABLE[max(T_95_TABLE.keys())]


def mean_std_ci95(values):
    """Return (mean, std [sample], ci95_lo, ci95_hi, n)."""
    n = len(values)
    if n == 0:
        return (float("nan"), float("nan"), float("nan"), float("nan"), 0)
    m = sum(values) / n
    if n == 1:
        return (m, 0.0, m, m, 1)
    var = sum((x - m) ** 2 for x in values) / (n - 1)
    std = math.sqrt(var)
    tc = t_critical_95(n - 1)
    half = tc * std / math.sqrt(n)
    return (m, std, m - half, m + half, n)


def run_single(label: str, av_pen: float, seed: int, hdv_action_interval: float,
               quick: bool = False):
    """Run a single scenario+seed and return (stats_dict, counters_dict, fd_data)."""
    config = SimConfig(av_penetration=av_pen, seed=seed)
    if hdv_action_interval is not None:
        config.hdv_params = replace(config.hdv_params,
                                    action_interval=hdv_action_interval)
    if quick:
        config.sim_duration = 300.0
        config.warmup = 30.0

    logger.info(
        f"  [{label} seed={seed} av={av_pen:.0%} "
        f"hdv_ai={config.hdv_params.action_interval}]"
    )

    t0 = time.time()
    sim = Simulation(config)
    results = sim.run()
    wall_time = time.time() - t0

    stats = summary_statistics(
        results["completed_vehicles"],
        warmup=config.warmup,
        sim_duration=config.sim_duration,
    )
    stats["wall_time_s"] = round(wall_time, 2)
    stats["av_penetration"] = av_pen
    stats["seed"] = seed
    stats["hdv_action_interval"] = config.hdv_params.action_interval

    fd_data = {}
    all_vehicles = results["vehicles"]
    for mc in FD_MEASUREMENT_CELLS:
        fd_data[mc] = passage_time_flow(
            all_vehicles,
            measurement_cell=mc,
            time_interval=60.0,
            sim_duration=config.sim_duration,
        )

    counters = results.get("counters", {})

    return stats, counters, fd_data, config


def save_per_seed_json(out_path: Path, label: str, av_pen: float, seed: int,
                       stats: dict, counters: dict, fd_data: dict, config: SimConfig):
    out = {
        "label": label,
        "av_penetration": av_pen,
        "seed": seed,
        "sim_duration": config.sim_duration,
        "warmup": config.warmup,
        "hdv_action_interval": config.hdv_params.action_interval,
        "av_action_interval": config.av_params.action_interval,
        "stats": stats,
        "counters": counters,
        "fd_data": {
            str(mc): [
                {"t": t, "flow": q, "density": k, "speed": v}
                for t, q, k, v in points
            ]
            for mc, points in fd_data.items()
        },
    }
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)


# Metrics we aggregate over seeds
AGG_METRICS = [
    "throughput_per_hour",
    "avg_travel_time",
    "avg_delay",
    "avg_lc_per_km",
    "pct_delayed_20s",
    "num_completed",
    "wall_time_s",
]


def write_aggregate_csv(out_csv: Path, per_seed_rows: list, extra_col: str = None,
                        extra_value=None):
    """Write aggregate CSV (scenario,metric,mean,std,ci95_lo,ci95_hi[,extra])."""
    # Group by (label, maybe extra_value)
    groups = {}
    for row in per_seed_rows:
        key = row["label"]
        groups.setdefault(key, []).append(row)

    rows_out = []
    for label, rows in groups.items():
        for metric in AGG_METRICS:
            vals = [r["stats"].get(metric) for r in rows
                    if r["stats"].get(metric) is not None]
            m, std, lo, hi, n = mean_std_ci95(vals)
            out_row = {
                "scenario": label,
                "metric": metric,
                "mean": m,
                "std": std,
                "ci95_lo": lo,
                "ci95_hi": hi,
                "n": n,
            }
            if extra_col is not None:
                out_row[extra_col] = extra_value
            rows_out.append(out_row)

    if not rows_out:
        return
    fieldnames = list(rows_out[0].keys())
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true",
                   help="Quick mode: 300s sim, 30s warmup.")
    p.add_argument("--seeds", type=int, nargs="+", default=None,
                   help="List of seeds. If omitted, runs single seed=42 "
                        "to preserve legacy behavior.")
    p.add_argument("--action-interval", type=float, default=None,
                   help="Override HDV action_interval (s). AV unchanged.")
    p.add_argument("--out-dir", type=str, default=None,
                   help="Output directory. Defaults: output/experiments "
                        "(single seed) or output/multiseed (--seeds).")
    p.add_argument("--scenarios", type=str, nargs="+", default=None,
                   help="Scenario labels to run (subset of S1_baseline, "
                        "S2_low_av, S3_med_av, S4_high_av). Default: all.")
    return p.parse_args()


def main():
    args = parse_args()

    scenarios = SCENARIOS
    if args.scenarios:
        allowed = set(args.scenarios)
        scenarios = [(lbl, av) for (lbl, av) in SCENARIOS if lbl in allowed]
        if not scenarios:
            raise SystemExit(f"No valid scenarios in --scenarios {args.scenarios}; "
                             f"choose from {[s[0] for s in SCENARIOS]}")

    # Legacy single-seed path (backward compatible)
    if args.seeds is None:
        out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "experiments"
        out_dir.mkdir(parents=True, exist_ok=True)
        all_stats, all_counters = [], []
        for label, av_pen in scenarios:
            logger.info(f"=== {label} (AV={av_pen:.0%}) ===")
            stats, counters, fd_data, config = run_single(
                label, av_pen, seed=42,
                hdv_action_interval=args.action_interval, quick=args.quick,
            )
            save_per_seed_json(out_dir / f"{label}.json", label, av_pen, 42,
                               stats, counters, fd_data, config)
            all_stats.append({"label": label, **stats})
            all_counters.append({"label": label, **counters})
        if all_stats:
            keys = all_stats[0].keys()
            with open(out_dir / "summary.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=keys)
                w.writeheader()
                w.writerows(all_stats)
        if all_counters:
            keys = all_counters[0].keys()
            with open(out_dir / "counters.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=keys)
                w.writeheader()
                w.writerows(all_counters)
        logger.info("All experiments complete.")
        return

    # Multi-seed path
    out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "multiseed"
    out_dir.mkdir(parents=True, exist_ok=True)

    per_seed_rows = []
    per_seed_counters = []
    for label, av_pen in scenarios:
        logger.info(f"=== {label} (AV={av_pen:.0%}) — {len(args.seeds)} seeds ===")
        for seed in args.seeds:
            stats, counters, fd_data, config = run_single(
                label, av_pen, seed=seed,
                hdv_action_interval=args.action_interval, quick=args.quick,
            )
            json_path = out_dir / f"{label}_seed{seed}.json"
            save_per_seed_json(json_path, label, av_pen, seed,
                               stats, counters, fd_data, config)
            per_seed_rows.append({"label": label, "av_penetration": av_pen,
                                  "seed": seed, "stats": stats})
            per_seed_counters.append({"label": label, "seed": seed,
                                      "av_penetration": av_pen, **counters})

    # Per-seed flat CSV
    flat_rows = []
    for r in per_seed_rows:
        flat = {"label": r["label"], "av_penetration": r["av_penetration"],
                "seed": r["seed"]}
        flat.update(r["stats"])
        flat_rows.append(flat)
    if flat_rows:
        keys = sorted({k for r in flat_rows for k in r.keys()})
        with open(out_dir / "per_seed.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(flat_rows)

    # Aggregate CSV
    agg_csv = out_dir / "aggregate.csv"
    write_aggregate_csv(agg_csv, per_seed_rows)
    logger.info(f"Aggregate CSV written to {agg_csv}")
    logger.info("All multi-seed experiments complete.")


if __name__ == "__main__":
    main()
