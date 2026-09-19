"""Temporary incident scenario: lane closure with congestion and recovery.

Blocks one lane for a limited duration, creating three phases:
  1. Free flow (before closure)
  2. Queue buildup (during closure)
  3. Recovery (after reopening)

Saves full per-vehicle trajectory data to JSON for visualization.

Usage:
    python run_incident.py [--quick]
"""

import json
import logging
import sys
import time
from dataclasses import asdict, replace
from pathlib import Path

from odca.experiment import numpy_default
from config import CELL_LENGTH_M, HDV_VEHICLE, ILLUSTRATIVE_SEED, sim_config
from odca.params import IncidentConfig, NetworkConfig
from odca.simulation.engine import Simulation
from odca.analysis.metrics import summary_statistics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- Incident configuration ---
NUM_LANES = 4
NUM_CELLS = 600          # 600 cells × 7.5m = 4.5 km
CLOSURE_LANE = 4         # leftmost lane (passing lane)
CLOSURE_START_CELL = 250
CLOSURE_END_CELL = 260   # short incident (~75 m)
INCIDENT_ON = 300.0      # seconds — closure activates
INCIDENT_OFF = 1500.0    # seconds — closure removed (20 min incident)
SIM_DURATION = 3600.0    # seconds — extended for full recovery observation
WARMUP = 200.0           # long warmup — seeded vehicles fully stabilize
MAINLINE_FLOW = 3000     # veh/h total (750/lane) — between 2800 (too mild) and 3200 (gridlock)
SEED_SPACING = 30        # cells between initial vehicles (~lower free-flow density)


def _serialize_trajectories(vehicles):
    """Convert vehicle trajectories to JSON-serializable list.

    Returns list of dicts, one per vehicle that entered the network.
    Each dict contains the vehicle's full T(x,n) trajectory with lane info.
    """
    records = []
    for v in vehicles:
        if not v.trajectory:
            continue
        records.append({
            "id": v.id,
            "kind": v.kind,
            "time_entered": v.time_entered,
            "time_exited": v.time_exited,
            "trajectory": [
                {
                    "t": round(tr.time, 4),
                    "cell": tr.cell_idx,
                    "lane": tr.lane_idx,
                    "speed": round(tr.speed, 4),
                }
                for tr in v.trajectory
            ],
        })
    return records


def _make_config(quick: bool = False):
    """Build SimConfig shared by baseline and incident runs."""
    duration = SIM_DURATION if not quick else 800.0
    warmup = WARMUP if not quick else 60.0

    per_lane_flow = MAINLINE_FLOW / NUM_LANES
    config = sim_config(
        network=NetworkConfig.corridor(num_lanes=NUM_LANES, num_cells=NUM_CELLS,
                              speed_limit=HDV_VEHICLE.v_max),
        demand={f"mainline_lane_{lane}": {"end": per_lane_flow}
                for lane in range(1, NUM_LANES + 1)},
        av_penetration=0.0,  # all HDV for clearest demonstration
        sim_duration=duration,
        warmup=warmup,
        seed=ILLUSTRATIVE_SEED,
    )
    return config, duration, warmup


def _run_and_save(config, duration, warmup, scenario_name, out_filename,
                  incident=False):
    """Run simulation and save trajectory JSON."""
    if incident:
        config = replace(config, incidents=[IncidentConfig(
            start=INCIDENT_ON, duration=INCIDENT_OFF - INCIDENT_ON, lane=CLOSURE_LANE,
            first_cell=CLOSURE_START_CELL, last_cell=CLOSURE_END_CELL,
        )])
    sim = Simulation(config)

    sim.seed_vehicles(
        spacing=SEED_SPACING,
        destination="end",
    )

    t0 = time.time()
    results = sim.run()
    wall_time = time.time() - t0

    stats = summary_statistics(
        results.completed_vehicles,
        warmup=warmup,
        sim_duration=duration,
    )
    stats["wall_time_s"] = round(wall_time, 2)

    logger.info("Serializing trajectories...")
    trajectory_data = _serialize_trajectories(results.vehicles)
    logger.info(f"  {len(trajectory_data)} vehicles with trajectory data")

    output = {
        "scenario": scenario_name,
        "config": {
            "num_lanes": NUM_LANES,
            "num_cells": NUM_CELLS,
            "closure_lane": CLOSURE_LANE,
            "closure_start_cell": CLOSURE_START_CELL,
            "closure_end_cell": CLOSURE_END_CELL,
            "incident_on": INCIDENT_ON,
            "incident_off": INCIDENT_OFF,
            "sim_duration": duration,
            "warmup": warmup,
            "mainline_flow": MAINLINE_FLOW,
            "cell_length_m": CELL_LENGTH_M,
        },
        "stats": stats,
        "counters": asdict(results.counters),
        "trajectories": trajectory_data,
    }

    out_dir = Path("output") / "incident"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / out_filename

    logger.info(f"Writing {out_file}...")
    with open(out_file, "w") as f:
        json.dump(output, f, indent=None, default=numpy_default)
    file_size_mb = out_file.stat().st_size / 1024 / 1024
    logger.info(f"  Saved: {file_size_mb:.1f} MB")

    logger.info(f"Stats: throughput={stats.get('throughput_per_hour', 0):.0f} veh/h, "
                f"avg_delay={stats.get('avg_delay', 0):.1f}s, "
                f"wall_time={wall_time:.1f}s")
    logger.info(f"{scenario_name} complete.")


def run_baseline(quick: bool = False):
    """Run baseline (no-incident) scenario with identical config."""
    logger.info("=== Baseline (no incident) ===")
    config, duration, warmup = _make_config(quick)
    _run_and_save(config, duration, warmup,
                  scenario_name="baseline",
                  out_filename="baseline_trajectory.json",
                  incident=False)


def run_incident(quick: bool = False):
    """Run temporary incident scenario and save results."""
    logger.info("=== Incident scenario ===")
    config, duration, warmup = _make_config(quick)
    _run_and_save(config, duration, warmup,
                  scenario_name="temporary_incident",
                  out_filename="incident_trajectory.json",
                  incident=True)


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    run_baseline(quick=quick)
    run_incident(quick=quick)
