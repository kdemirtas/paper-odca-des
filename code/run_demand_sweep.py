"""Demand sweep: density initialization for full fundamental diagram.

Initializes a segment at various densities (vehicles placed directly into
cells), then runs the simulation and measures emergent flow and speed using
Edie's generalized definitions over space-time regions. Supports both
single-lane and multi-lane configurations.

Usage:
    python run_demand_sweep.py [--quick] [--lanes 1] [--lanes 4]
"""

import json
import logging
import sys
import time
from pathlib import Path
from typing import List

import simpy

from config import CELL_LENGTH_M, HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED
from odca.params import ControllerConfig, NetworkConfig
from odca.infrastructure.freeway import Freeway
from odca.entity.vehicle import Vehicle
from odca.entity.driver import DriverStreams, HumanDriver, TraitSampler
from odca.entity.controller import AutonomousController
from odca.rng import RNGRegistry
from odca.analysis.metrics import edie_fd_points

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

NUM_CELLS = 400

# Measurement region: cells [LO, HI)
REGION_LO = 100
REGION_HI = 300
REGION_LEN = REGION_HI - REGION_LO
FD_INTERVAL = 20.0  # aggregation window (seconds)

# Fine density grid for rich FD
DENSITIES = [
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10,
    0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30,
    0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
]
DENSITIES_QUICK = [
    0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80,
]


# ──────────────────────────────────────────────────────────────────────
# Vehicle creation and placement
# ──────────────────────────────────────────────────────────────────────

def _human_maker(env, freeway, registry):
    """A function building a human-driven vehicle at a cell, bound for the segment end.

    Spawns the decision streams and the trait streams of `registry`, in that order.

    Args:
        env: the SimPy environment.
        freeway: the corridor.
        registry: the run's RNG registry.
    """
    streams = DriverStreams.spawn(registry)
    sampler = TraitSampler.spawn(registry)
    end = freeway.destination("end")

    def make(cell):
        driver = HumanDriver(HDV_DRIVER, streams, sampler.draw(HDV_DRIVER))
        return Vehicle(env, HDV_VEHICLE, driver, cell, end)
    return make


def _place_vehicles(freeway, num_lanes, density, make):
    """Place vehicles evenly across all lanes at given density."""
    vehicles = []
    num_per_lane = int(NUM_CELLS * density)
    if num_per_lane < 1:
        return vehicles

    spacing = NUM_CELLS / num_per_lane
    for lane_idx in range(1, num_lanes + 1):
        lane = freeway.lane(lane_idx)
        for i in range(num_per_lane):
            vehicles.append(make(lane.cells[int(i * spacing) % NUM_CELLS]))
    return vehicles


def _start_inflow(env, freeway, all_vehicles, make):
    """Replace every exiting vehicle with a new one at the start of its lane (tex:902).

    Keeps the number of vehicles on the segment at the target density; the replacement
    waits at cell 0 until that cell's lock is free.
    """
    def _run_and_replace(vehicle, lane_idx):
        """Drive the vehicle to its exit, then start its replacement in the same lane.

        Args:
            vehicle: the vehicle to run.
            lane_idx: the lane whose first cell the replacement enters.
        """
        yield env.process(vehicle.start())
        replacement = make(freeway.lane(lane_idx).cells[0])
        all_vehicles.append(replacement)
        env.process(_run_and_replace(replacement, lane_idx))

    return _run_and_replace


# ──────────────────────────────────────────────────────────────────────
# Main simulation runner
# ──────────────────────────────────────────────────────────────────────

def run_density_init(density: float, duration: float, warmup: float,
                     num_lanes: int = 1) -> dict:
    """Initialize segment at given density and measure emergent FD."""
    rng_registry = RNGRegistry(master_seed=ILLUSTRATIVE_SEED)
    Vehicle._id_counter = 0

    env = simpy.Environment()
    freeway = Freeway(env, NetworkConfig.corridor(num_lanes, NUM_CELLS, HDV_VEHICLE.v_max))
    controller = AutonomousController(ControllerConfig(dt=0.1), env)
    env.process(controller.run())
    make = _human_maker(env, freeway, rng_registry)

    num_per_lane = int(NUM_CELLS * density)
    if num_per_lane < 1:
        return {"density": density, "fd_points": []}

    vehicles = _place_vehicles(freeway, num_lanes, density, make)
    all_vehicles = list(vehicles)
    run_and_replace = _start_inflow(env, freeway, all_vehicles, make)
    for veh in vehicles:
        env.process(run_and_replace(veh, veh.origin_cell.lane.idx))

    env.run(until=duration)

    fd_points = edie_fd_points(all_vehicles, REGION_LO, REGION_HI,
                               warmup, duration, FD_INTERVAL, num_lanes)
    completed = sum(1 for v in all_vehicles if v.time_exited is not None)
    return {
        "density": density,
        "num_lanes": num_lanes,
        "num_initial": num_per_lane * num_lanes,
        "num_total": len(all_vehicles),
        "num_completed": completed,
        "fd_points": fd_points,
    }


def run_sweep(num_lanes: int, duration: float, warmup: float,
              densities: List[float]) -> List[dict]:
    """Run full density sweep for a given lane configuration."""
    logger.info(
        f"=== Density Sweep ({num_lanes} lane{'s' if num_lanes > 1 else ''}, "
        f"HDV only, {duration:.0f}s) ==="
    )
    results = []
    t0 = time.time()
    for density in densities:
        logger.info(
            f"  k={density:.2f} veh/cell "
            f"({density * 1000 / CELL_LENGTH_M:.1f} veh/km)"
        )
        result = run_density_init(density, duration, warmup, num_lanes)
        results.append(result)
        logger.info(
            f"    Vehicles: {result.get('num_initial', 0)} init, "
            f"{result.get('num_total', 0)} total, "
            f"{result.get('num_completed', 0)} completed, "
            f"{len(result['fd_points'])} FD pts"
        )
    wall_time = time.time() - t0
    logger.info(f"  Wall time: {wall_time:.1f}s")
    return results


def main():
    quick = "--quick" in sys.argv

    # Parse --lanes arguments (can specify multiple: --lanes 1 --lanes 4)
    lane_configs = []
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--lanes" and i + 1 < len(args):
            lane_configs.append(int(args[i + 1]))
    if not lane_configs:
        lane_configs = [1, 4]  # default: both single and multi-lane

    duration = 300.0 if quick else 1200.0
    warmup = 60.0 if quick else 200.0
    densities = DENSITIES_QUICK if quick else DENSITIES

    out_dir = Path("output") / "demand_sweep"
    out_dir.mkdir(parents=True, exist_ok=True)

    for num_lanes in lane_configs:
        results = run_sweep(num_lanes, duration, warmup, densities)

        output = {
            "config": f"density_init_{num_lanes}lane_hdv_edie",
            "num_lanes": num_lanes,
            "duration": duration,
            "warmup": warmup,
            "densities": densities,
            "results": results,
        }
        fname = f"sweep_{num_lanes}lane.json"
        with open(out_dir / fname, "w") as f:
            json.dump(output, f, indent=2)
        logger.info(f"  Saved to {out_dir / fname}")

    logger.info("All sweeps complete.")


if __name__ == "__main__":
    main()
