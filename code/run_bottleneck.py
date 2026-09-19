"""Bottleneck experiment: lane closure creating congestion dynamics.

Simulates a lane drop (lane closure) on the leftmost lane starting at a
specified cell. Measures queue formation, throughput drop, and recovery
across AV penetration scenarios.

Usage (legacy single-seed):
    python run_bottleneck.py [--quick]

Multi-seed with CIs:
    python run_bottleneck.py --seeds 1 2 3 ... 20 [--action-interval 0.5]
"""

import argparse
import csv
import json
import logging
import math
import time
from dataclasses import replace
from pathlib import Path

from json_default import numpy_default
from config import SimConfig, NetworkConfig, ODFlow, HDV_PARAMS
from odca.simulation.engine import Simulation
from odca.analysis.metrics import edie_fd_points, summary_statistics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Bottleneck configuration
NUM_LANES = 3
NUM_CELLS = 600
CLOSURE_LANE = 3       # close leftmost lane (lane drop)
CLOSURE_START = 300
CLOSURE_END = 599
MAINLINE_FLOW = 3600
SEED_SPACING = 25

UPSTREAM_REGION = (200, 280)
DOWNSTREAM_REGION = (350, 450)

AV_SCENARIOS = [
    ("BN_0av", 0.0),
    ("BN_30av", 0.3),
    ("BN_50av", 0.5),
    ("BN_70av", 0.7),
]


# ──────────────────────────────────────────────────────────────────────
# Student's t critical values at 95% confidence (two-tailed), df = n-1
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
        return 1.96
    return T_95_TABLE[max(T_95_TABLE.keys())]


def mean_std_ci95(values):
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


AGG_METRICS = [
    "throughput_per_hour",
    "avg_travel_time",
    "avg_delay",
    "avg_lc_per_km",
    "pct_delayed_20s",
    "num_completed",
    "wall_time_s",
]


def run_single_bottleneck(label: str, av_pen: float, seed: int,
                          hdv_action_interval: float, quick: bool = False):
    config = SimConfig(
        network=NetworkConfig(
            num_lanes=NUM_LANES,
            num_cells=NUM_CELLS,
            speed_limit=HDV_PARAMS.v_max,
            onramp_cells=[],
            offramp_cells=[],
        ),
        av_penetration=av_pen,
        sim_duration=1800.0 if not quick else 600.0,
        warmup=120.0 if not quick else 60.0,
        seed=seed,
    )
    if hdv_action_interval is not None:
        config.hdv_params = replace(config.hdv_params,
                                    action_interval=hdv_action_interval)

    per_lane_flow = MAINLINE_FLOW / NUM_LANES
    config.od_flows = [
        ODFlow(f"mainline_lane_{lane}", flow_rate=per_lane_flow,
               destinations=[(NUM_CELLS, 1.0)])
        for lane in range(1, NUM_LANES + 1)
    ]

    sim = Simulation(config)
    sim.freeway.block_cells(
        lane_idx=CLOSURE_LANE,
        start_cell=CLOSURE_START,
        end_cell=CLOSURE_END,
    )
    sim.seed_vehicles(spacing=SEED_SPACING, destination_cell_idx=NUM_CELLS)

    t0 = time.time()
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

    fd_json = {}
    for region_name, (lo, hi) in [
        ("upstream", UPSTREAM_REGION),
        ("downstream", DOWNSTREAM_REGION),
    ]:
        pts = edie_fd_points(
            results["vehicles"],
            region_lo=lo,
            region_hi=hi,
            warmup=config.warmup,
            duration=config.sim_duration,
            interval=30.0,
            num_lanes=NUM_LANES if region_name == "upstream" else (NUM_LANES - 1),
        )
        fd_json[region_name] = pts

    payload = {
        "label": label,
        "av_penetration": av_pen,
        "seed": seed,
        "hdv_action_interval": config.hdv_params.action_interval,
        "av_action_interval": config.av_params.action_interval,
        "stats": stats,
        "counters": results.get("counters", {}),
        "fd_data": fd_json,
        "closure": {
            "lane": CLOSURE_LANE,
            "start_cell": CLOSURE_START,
            "end_cell": CLOSURE_END,
        },
    }
    return payload, config


def write_aggregate_csv(out_csv: Path, per_seed_payloads: list):
    groups = {}
    for p in per_seed_payloads:
        groups.setdefault(p["label"], []).append(p)

    rows_out = []
    for label, items in groups.items():
        for metric in AGG_METRICS:
            vals = [it["stats"].get(metric) for it in items
                    if it["stats"].get(metric) is not None]
            m, std, lo, hi, n = mean_std_ci95(vals)
            rows_out.append({
                "scenario": label,
                "metric": metric,
                "mean": m,
                "std": std,
                "ci95_lo": lo,
                "ci95_hi": hi,
                "n": n,
            })
    if not rows_out:
        return
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true")
    p.add_argument("--seeds", type=int, nargs="+", default=None,
                   help="List of seeds. If omitted, runs single seed=42.")
    p.add_argument("--action-interval", type=float, default=None,
                   help="Override HDV action_interval (s). AV unchanged.")
    p.add_argument("--out-dir", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()

    if args.seeds is None:
        # legacy single-seed behavior
        out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "bottleneck"
        out_dir.mkdir(parents=True, exist_ok=True)
        all_results = []
        for label, av_pen in AV_SCENARIOS:
            logger.info(f"=== {label} (AV={av_pen:.0%}) ===")
            payload, _ = run_single_bottleneck(
                label, av_pen, seed=42,
                hdv_action_interval=args.action_interval, quick=args.quick,
            )
            logger.info(
                f"  Throughput: {payload['stats'].get('throughput_per_hour', 0):.0f} veh/h"
            )
            with open(out_dir / f"{label}.json", "w") as f:
                json.dump(payload, f, indent=2, default=numpy_default)
            all_results.append(payload)
        summary = []
        for r in all_results:
            summary.append({
                "label": r["label"],
                "av_penetration": r["av_penetration"],
                **r["stats"],
                **{f"cnt_{k}": v for k, v in r["counters"].items()},
            })
        with open(out_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2, default=numpy_default)
        logger.info("Bottleneck experiments complete.")
        return

    # Multi-seed path
    out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "multiseed"
    out_dir.mkdir(parents=True, exist_ok=True)

    per_seed_payloads = []
    for label, av_pen in AV_SCENARIOS:
        logger.info(f"=== {label} (AV={av_pen:.0%}) — {len(args.seeds)} seeds ===")
        for seed in args.seeds:
            logger.info(f"  seed={seed}")
            payload, _ = run_single_bottleneck(
                label, av_pen, seed=seed,
                hdv_action_interval=args.action_interval, quick=args.quick,
            )
            json_path = out_dir / f"{label}_seed{seed}.json"
            with open(json_path, "w") as f:
                json.dump(payload, f, indent=2, default=numpy_default)
            per_seed_payloads.append(payload)

    # Flat per-seed CSV
    flat_rows = []
    for p in per_seed_payloads:
        flat = {"label": p["label"], "seed": p["seed"],
                "av_penetration": p["av_penetration"]}
        flat.update(p["stats"])
        flat_rows.append(flat)
    if flat_rows:
        keys = sorted({k for r in flat_rows for k in r.keys()})
        with open(out_dir / "bottleneck_per_seed.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(flat_rows)

    agg_csv = out_dir / "bottleneck_aggregate.csv"
    write_aggregate_csv(agg_csv, per_seed_payloads)
    logger.info(f"Aggregate CSV written to {agg_csv}")
    logger.info("All multi-seed bottleneck experiments complete.")


if __name__ == "__main__":
    main()
