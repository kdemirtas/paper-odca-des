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
from dataclasses import replace as dc_replace
from pathlib import Path
from typing import List

import numpy as np
import simpy

from config import (
    VehicleParams,
    CELL_LENGTH_M, HDV_PARAMS,
)
from odca.infrastructure.freeway import Freeway
from odca.entity.vehicle import Vehicle
from odca.entity.hdv import HDV
from odca.entity.av_controller import AVController
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
# Per-driver sampling (mirrors generator.py logic)
# ──────────────────────────────────────────────────────────────────────

def _sample_hdv_params(params: VehicleParams, rng_tau, rng_action_interval,
                       rng_slowdown) -> VehicleParams:
    overrides = {}
    if params.tau_std > 0:
        mean, std = params.tau, params.tau_std
        sigma_ln2 = np.log(1 + (std / mean) ** 2)
        mu_ln = np.log(mean) - sigma_ln2 / 2
        val = rng_tau.lognormal(mu_ln, np.sqrt(sigma_ln2))
        overrides["tau"] = float(np.clip(val, 0.5, 3.0))
    if params.action_interval_std > 0:
        mean, std = params.action_interval, params.action_interval_std
        sigma_ln2 = np.log(1 + (std / mean) ** 2)
        mu_ln = np.log(mean) - sigma_ln2 / 2
        val = rng_action_interval.lognormal(mu_ln, np.sqrt(sigma_ln2))
        overrides["action_interval"] = float(np.clip(val, 0.3, 3.0))
    if params.slowdown_prob_std > 0:
        val = rng_slowdown.normal(params.slowdown_prob, params.slowdown_prob_std)
        overrides["slowdown_prob"] = float(np.clip(val, 0.0, 1.0))
    return dc_replace(params, **overrides) if overrides else params


# ──────────────────────────────────────────────────────────────────────
# Vehicle creation and placement
# ──────────────────────────────────────────────────────────────────────

def _make_hdv(env, cell, rng_slowdown, rng_mlc, rng_dlc, rng_tau,
              rng_action_interval, rng_slowdown_param, dest_cell_idx, dest_lane):
    driver_params = _sample_hdv_params(
        HDV_PARAMS, rng_tau, rng_action_interval, rng_slowdown_param,
    )
    return HDV(
        env=env, rng_slowdown=rng_slowdown, rng_mlc=rng_mlc, rng_dlc=rng_dlc,
        params=driver_params, origin_cell=cell,
        destination_cell_idx=dest_cell_idx, destination_lane=dest_lane,
    )


def _place_vehicles(env, freeway, num_lanes, density,
                    rng_slowdown, rng_mlc, rng_dlc,
                    rng_tau, rng_action_interval, rng_slowdown_param):
    """Place vehicles evenly across all lanes at given density."""
    vehicles = []
    num_per_lane = int(NUM_CELLS * density)
    if num_per_lane < 1:
        return vehicles

    spacing = NUM_CELLS / num_per_lane
    for lane_idx in range(1, num_lanes + 1):
        lane = freeway.lane(lane_idx)
        for i in range(num_per_lane):
            cell_idx = int(i * spacing) % NUM_CELLS
            veh = _make_hdv(
                env, lane.cells[cell_idx], rng_slowdown, rng_mlc, rng_dlc,
                rng_tau, rng_action_interval, rng_slowdown_param,
                dest_cell_idx=NUM_CELLS, dest_lane=lane_idx,
            )
            vehicles.append(veh)
            env.process(veh.start())
    return vehicles


def _start_inflow(env, freeway, num_lanes, density, all_vehicles,
                  rng_gen, rng_slowdown, rng_mlc, rng_dlc,
                  rng_tau, rng_action_interval, rng_slowdown_param):
    """Inflow process: replace exiting vehicles to maintain density."""
    inflow_rate_per_lane = density * HDV_PARAMS.v_max * 3600
    mean_interval = 3600.0 / max(inflow_rate_per_lane * num_lanes, 1.0)

    def _process():
        lane_cycle = 0
        while True:
            interval = rng_gen.exponential(mean_interval)
            yield env.timeout(interval)
            lane_idx = (lane_cycle % num_lanes) + 1
            lane_cycle += 1
            cell = freeway.lane(lane_idx).cells[0]
            veh = _make_hdv(
                env, cell, rng_slowdown, rng_mlc, rng_dlc,
                rng_tau, rng_action_interval, rng_slowdown_param,
                dest_cell_idx=NUM_CELLS, dest_lane=lane_idx,
            )
            all_vehicles.append(veh)
            env.process(veh.start())

    env.process(_process())






# ──────────────────────────────────────────────────────────────────────
# Main simulation runner
# ──────────────────────────────────────────────────────────────────────

def run_density_init(density: float, duration: float, warmup: float,
                     num_lanes: int = 1) -> dict:
    """Initialize segment at given density and measure emergent FD."""
    rng_registry = RNGRegistry(master_seed=42)
    rng_slowdown = rng_registry.spawn("slowdown")
    rng_mlc = rng_registry.spawn("mlc")
    rng_dlc = rng_registry.spawn("dlc")
    rng_tau = rng_registry.spawn("driver_tau")
    rng_action_interval = rng_registry.spawn("driver_action_interval")
    rng_slowdown_param = rng_registry.spawn("driver_slowdown")
    Vehicle._id_counter = 0

    env = simpy.Environment()
    freeway = Freeway(
        env=env, num_lanes=num_lanes, num_cells=NUM_CELLS,
        speed_limit=HDV_PARAMS.v_max, onramp_cells=[], offramp_cells=[],
    )
    av_controller = AVController(env=env, controller_dt=0.1)
    env.process(av_controller.run())

    num_per_lane = int(NUM_CELLS * density)
    if num_per_lane < 1:
        return {"density": density, "fd_points": []}

    vehicles = _place_vehicles(
        env, freeway, num_lanes, density,
        rng_slowdown, rng_mlc, rng_dlc,
        rng_tau, rng_action_interval, rng_slowdown_param,
    )
    all_vehicles = list(vehicles)

    rng_gen = rng_registry.spawn("generator")
    _start_inflow(env, freeway, num_lanes, density, all_vehicles,
                  rng_gen, rng_slowdown, rng_mlc, rng_dlc,
                  rng_tau, rng_action_interval, rng_slowdown_param)

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
