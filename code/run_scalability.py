"""Scalability benchmark: measure wall-clock runtime vs. network size.

Runs the S1 (0% AV) mixed-traffic scenario (but with no AVs so it's pure
HDV) at several network sizes. Flow scales with the number of lanes to keep
per-lane demand constant across configurations. Records the SimPy event count, the
behaviour counters (lane changes, slowdowns, CF evaluations, controller updates) and
wall-clock time per run.

Output: code/output/scalability_benchmark.csv with one row per (cells,seed).
"""

from dataclasses import asdict
import argparse
import csv
import logging
import time
from pathlib import Path

from config import HDV_VEHICLE, SCALABILITY_SEEDS, sim_config
from odca.params import NetworkConfig
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
PER_LANE_FLOW = 1500.0  # veh/h per lane (matches S1 default)


def build_demand(num_lanes: int):
    """Mainline-only demand: each lane enters at cell 0 and leaves at the segment end, from
    any lane, so per-lane flow stays constant across sizes.

    Args:
        num_lanes: lanes of the corridor.
    """
    return {f"mainline_lane_{lane}": {"end": PER_LANE_FLOW} for lane in range(1, num_lanes + 1)}


def run_one(num_cells: int, num_lanes: int, seed: int) -> dict:
    config = sim_config(
        network=NetworkConfig.corridor(num_lanes=num_lanes, num_cells=num_cells,
                              speed_limit=HDV_VEHICLE.v_max),
        demand=build_demand(num_lanes),
        av_penetration=0.0,
        sim_duration=SIM_DURATION,
        warmup=WARMUP,
        seed=seed,
    )

    sim = Simulation(config)

    t0 = time.time()
    results = sim.run()
    wall = time.time() - t0

    counters = asdict(results.counters)
    behaviour_events = (
        counters["lane_changes"] + counters["slowdowns"]
        + counters["cf_evaluations"] + counters["av_controller_updates"]
    )
    total_generated = results.num_generated
    total_cells = num_cells * num_lanes

    return {
        "num_cells": num_cells,
        "num_lanes": num_lanes,
        "total_cells": total_cells,
        "seed": seed,
        "vehicles_generated": total_generated,
        "simpy_events": counters["simpy_events"],
        "behaviour_events": behaviour_events,
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
                   help=f"Override seeds (default {list(SCALABILITY_SEEDS)})")
    return p.parse_args()


def main():
    args = parse_args()
    cell_sizes = args.cells or CELL_SIZES
    seeds = args.seeds or SCALABILITY_SEEDS

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for cells in cell_sizes:
        for seed in seeds:
            logger.info(f"=== cells={cells} lanes={NUM_LANES} seed={seed} ===")
            row = run_one(cells, NUM_LANES, seed)
            logger.info(
                f"  wall={row['wall_clock_seconds']}s "
                f"events={row['simpy_events']} "
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
