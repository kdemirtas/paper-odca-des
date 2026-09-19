"""Bottleneck experiment: lane closure creating congestion dynamics.

Simulates a lane drop (lane closure) on the leftmost lane starting at a
specified cell. Measures queue formation, throughput drop, and recovery
across AV penetration scenarios.

Usage (legacy single-seed):
    python run_bottleneck.py [--quick]

Multi-seed (one JSON per seed; aggregate_multiseed.py writes the CSVs):
    python run_bottleneck.py --seeds 1 2 3 ... 20 [--action-interval 0.5]
"""

import argparse
import json
import logging
from dataclasses import replace
from pathlib import Path

from config import HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED, sim_config
from odca.params import NetworkConfig
from odca.analysis.metrics import edie_fd_points, summary_statistics
from odca.experiment import RunRecord, numpy_default, run_once, write_run

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


def _prepare(sim):
    """Close the lane and place the initial vehicles.

    Args:
        sim: the built simulation.
    """
    sim.freeway.block_cells(lane_idx=CLOSURE_LANE, start_cell=CLOSURE_START,
                            end_cell=CLOSURE_END)
    sim.seed_vehicles(spacing=SEED_SPACING, destination="end")


def _measure(result) -> dict:
    """Summary statistics of one run, with the scenario keys the aggregation groups by.

    Args:
        result: the run's `SimulationResult`.
    """
    config = result.config
    stats = summary_statistics(result.completed_vehicles, warmup=config.warmup,
                               sim_duration=config.sim_duration)
    stats["av_penetration"] = config.av_penetration
    stats["seed"] = config.seed
    stats["hdv_action_interval"] = config.hdv_driver.action_interval
    return stats


def run_single_bottleneck(label: str, av_pen: float, seed: int,
                          hdv_action_interval: float, quick: bool = False) -> RunRecord:
    """One bottleneck run; the record carries Edie FD points up- and downstream of the drop."""
    per_lane_flow = MAINLINE_FLOW / NUM_LANES
    hdv_driver = (HDV_DRIVER if hdv_action_interval is None
                  else replace(HDV_DRIVER, action_interval=hdv_action_interval))
    config = sim_config(
        network=NetworkConfig.corridor(num_lanes=NUM_LANES, num_cells=NUM_CELLS,
                                       speed_limit=HDV_VEHICLE.v_max),
        demand={f"mainline_lane_{lane}": {"end": per_lane_flow}
                for lane in range(1, NUM_LANES + 1)},
        hdv_driver=hdv_driver,
        av_penetration=av_pen,
        sim_duration=1800.0 if not quick else 600.0,
        warmup=120.0 if not quick else 60.0,
        seed=seed,
    )
    record, result = run_once(label, config, _measure, prepare=_prepare)
    fd_json = {}
    for region_name, (lo, hi) in [("upstream", UPSTREAM_REGION),
                                  ("downstream", DOWNSTREAM_REGION)]:
        fd_json[region_name] = edie_fd_points(
            result.vehicles, region_lo=lo, region_hi=hi, warmup=config.warmup,
            duration=config.sim_duration, interval=30.0,
            num_lanes=NUM_LANES if region_name == "upstream" else (NUM_LANES - 1),
        )
    record.extra.update(fd_data=fd_json, closure={"lane": CLOSURE_LANE,
                                                  "start_cell": CLOSURE_START,
                                                  "end_cell": CLOSURE_END})
    return record


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true")
    p.add_argument("--seeds", type=int, nargs="+", default=None,
                   help="List of seeds. If omitted, runs the single ILLUSTRATIVE_SEED.")
    p.add_argument("--action-interval", type=float, default=None,
                   help="Override HDV action_interval (s). AV unchanged.")
    p.add_argument("--out-dir", type=str, default=None)
    return p.parse_args()


def main():
    args = parse_args()

    if args.seeds is None:
        # the illustrative seed, one file per scenario plus a summary
        out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "bottleneck"
        out_dir.mkdir(parents=True, exist_ok=True)
        summary = []
        for label, av_pen in AV_SCENARIOS:
            logger.info(f"=== {label} (AV={av_pen:.0%}) ===")
            record = run_single_bottleneck(label, av_pen, seed=ILLUSTRATIVE_SEED,
                                           hdv_action_interval=args.action_interval,
                                           quick=args.quick)
            logger.info(f"  Throughput: {record.stats.get('throughput_per_hour', 0):.0f} veh/h")
            write_run(out_dir / f"{label}.json", record)
            summary.append({"label": record.label, "av_penetration": record.av_penetration,
                            **record.stats,
                            **{f"cnt_{k}": v for k, v in record.counters.items()}})
        with open(out_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2, default=numpy_default)
        logger.info("Bottleneck experiments complete.")
        return

    # Multi-seed path: one JSON per (scenario, seed); aggregate_multiseed.py writes the CSVs
    out_dir = (Path(args.out_dir) if args.out_dir
               else Path("output") / "multiseed" / "bottleneck" / "batch1")
    out_dir.mkdir(parents=True, exist_ok=True)
    for label, av_pen in AV_SCENARIOS:
        logger.info(f"=== {label} (AV={av_pen:.0%}), {len(args.seeds)} seeds ===")
        for seed in args.seeds:
            logger.info(f"  seed={seed}")
            record = run_single_bottleneck(label, av_pen, seed=seed,
                                           hdv_action_interval=args.action_interval,
                                           quick=args.quick)
            write_run(out_dir / f"{label}_seed{seed}.json", record)
    logger.info("All multi-seed bottleneck experiments complete; run aggregate_multiseed.py.")


if __name__ == "__main__":
    main()
