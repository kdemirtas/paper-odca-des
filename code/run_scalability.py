"""Scalability benchmark: measure wall-clock runtime vs. network size.

Runs the S1 (0% AV) mixed-traffic scenario (but with no AVs so it's pure
HDV) at several network sizes. Flow scales with the number of lanes to keep
per-lane demand constant across configurations. Records total events
(lane changes + slowdowns + CF evaluations + AV controller updates) and
wall-clock time per run.

Output: code/output/scalability_benchmark.csv with one row per (cells,seed).
"""

import argparse
import csv
import logging
import time
from pathlib import Path

from config import SimConfig, NetworkConfig, ODFlow, HDV_PARAMS
from odca.simulation.engine import Simulation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


CELL_SIZES = [200, 400, 800, 1600, 3200]
NUM_LANES = 4
SIM_DURATION = 1800.0
WARMUP = 120.0
SEEDS = [1, 2, 3]
PER_LANE_FLOW = 1500.0  # veh/h per lane (matches S1 default)


def build_od_flows(num_cells: int, num_lanes: int):
    """Mainline-only OD: each lane has demand entering at cell 0 and exiting
    at the final cell. Keeps per-lane flow constant across sizes."""
    flows = []
    for lane in range(1, num_lanes + 1):
        flows.append(ODFlow(
            f"mainline_lane_{lane}",
            flow_rate=PER_LANE_FLOW,
            destinations=[(num_cells, 1.0)],
        ))
    return flows


def run_one(num_cells: int, num_lanes: int, seed: int) -> dict:
    config = SimConfig(
        network=NetworkConfig(
            num_lanes=num_lanes,
            num_cells=num_cells,
            speed_limit=HDV_PARAMS.v_max,
            onramp_cells=[],
            offramp_cells=[],
        ),
        av_penetration=0.0,
        sim_duration=SIM_DURATION,
        warmup=WARMUP,
        seed=seed,
    )
    config.od_flows = build_od_flows(num_cells, num_lanes)

    sim = Simulation(config)

    t0 = time.time()
    results = sim.run()
    wall = time.time() - t0

    counters = results.get("counters", {})
    total_events = (
        counters.get("lane_changes", 0)
        + counters.get("slowdowns", 0)
        + counters.get("cf_evaluations", 0)
        + counters.get("av_controller_updates", 0)
    )
    total_generated = results.get("total_generated", 0)
    total_cells = num_cells * num_lanes

    return {
        "num_cells": num_cells,
        "num_lanes": num_lanes,
        "total_cells": total_cells,
        "seed": seed,
        "vehicles_generated": total_generated,
        "total_events": total_events,
        "lane_changes": counters.get("lane_changes", 0),
        "slowdowns": counters.get("slowdowns", 0),
        "cf_evaluations": counters.get("cf_evaluations", 0),
        "av_controller_updates": counters.get("av_controller_updates", 0),
        "wall_clock_seconds": round(wall, 3),
        "sim_seconds": SIM_DURATION,
        "realtime_ratio": SIM_DURATION / wall if wall > 0 else float("inf"),
    }


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str,
                   default="output/scalability_benchmark.csv")
    p.add_argument("--cells", type=int, nargs="+", default=None,
                   help=f"Override cell sizes (default {CELL_SIZES})")
    p.add_argument("--seeds", type=int, nargs="+", default=None,
                   help=f"Override seeds (default {SEEDS})")
    return p.parse_args()


def main():
    args = parse_args()
    cell_sizes = args.cells or CELL_SIZES
    seeds = args.seeds or SEEDS

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for cells in cell_sizes:
        for seed in seeds:
            logger.info(f"=== cells={cells} lanes={NUM_LANES} seed={seed} ===")
            row = run_one(cells, NUM_LANES, seed)
            logger.info(
                f"  wall={row['wall_clock_seconds']}s "
                f"events={row['total_events']} "
                f"rtratio={row['realtime_ratio']:.2f}x"
            )
            rows.append(row)
            # write incrementally so partial failure still leaves data
            with open(out_path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)

    logger.info(f"Scalability benchmark complete. Output: {out_path}")


if __name__ == "__main__":
    main()
