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
from pathlib import Path

import simpy

from config import (
    SimConfig, NetworkConfig, ODFlow, CELL_LENGTH_M,
    HDV_PARAMS, AV_PARAMS,
)
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


def _incident_process(env: simpy.Environment, freeway, t_on, t_off):
    """SimPy process: block lane at t_on, unblock at t_off."""
    yield env.timeout(t_on)
    logger.info(f"  INCIDENT ON at t={env.now:.0f}s — "
                f"blocking lane {CLOSURE_LANE}, cells {CLOSURE_START_CELL}-{CLOSURE_END_CELL}")
    freeway.block_cells(
        lane_idx=CLOSURE_LANE,
        start_cell=CLOSURE_START_CELL,
        end_cell=CLOSURE_END_CELL,
    )

    yield env.timeout(t_off - t_on)
    logger.info(f"  INCIDENT OFF at t={env.now:.0f}s — "
                f"unblocking lane {CLOSURE_LANE}")
    freeway.unblock_cells(
        lane_idx=CLOSURE_LANE,
        start_cell=CLOSURE_START_CELL,
        end_cell=CLOSURE_END_CELL,
    )


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
            "vtype": v.vtype.value,
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


def run_incident(quick: bool = False):
    """Run temporary incident scenario and save results."""
    duration = SIM_DURATION if not quick else 800.0
    warmup = WARMUP if not quick else 60.0

    config = SimConfig(
        network=NetworkConfig(
            num_lanes=NUM_LANES,
            num_cells=NUM_CELLS,
            speed_limit=HDV_PARAMS.v_max,
            onramp_cells=[],
            offramp_cells=[],
        ),
        av_penetration=0.0,  # all HDV for clearest demonstration
        sim_duration=duration,
        warmup=warmup,
        seed=42,
    )
    # Distribute demand evenly across all lanes; all exit downstream end
    per_lane_flow = MAINLINE_FLOW / NUM_LANES
    config.od_flows = [
        ODFlow(f"mainline_lane_{lane}", flow_rate=per_lane_flow,
               destinations=[(NUM_CELLS, 1.0)])
        for lane in range(1, NUM_LANES + 1)
    ]

    sim = Simulation(config)

    # Seed road with vehicles at free-flow density
    sim.seed_vehicles(
        spacing=SEED_SPACING,
        destination_cell_idx=NUM_CELLS,
    )

    # Schedule the incident as a SimPy process
    sim.env.process(_incident_process(
        sim.env, sim.freeway,
        t_on=INCIDENT_ON, t_off=INCIDENT_OFF,
    ))

    t0 = time.time()
    results = sim.run()
    wall_time = time.time() - t0

    # Summary stats
    stats = summary_statistics(
        results["completed_vehicles"],
        warmup=warmup,
        sim_duration=duration,
    )
    stats["wall_time_s"] = round(wall_time, 2)

    # Serialize all trajectories
    logger.info("Serializing trajectories...")
    trajectory_data = _serialize_trajectories(results["vehicles"])
    logger.info(f"  {len(trajectory_data)} vehicles with trajectory data")

    output = {
        "scenario": "temporary_incident",
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
        "counters": results.get("counters", {}),
        "trajectories": trajectory_data,
    }

    out_dir = Path("output") / "incident"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "incident_trajectory.json"

    logger.info(f"Writing {out_file}...")
    with open(out_file, "w") as f:
        json.dump(output, f, indent=None, default=str)
    file_size_mb = out_file.stat().st_size / 1024 / 1024
    logger.info(f"  Saved: {file_size_mb:.1f} MB")

    logger.info(f"Stats: throughput={stats.get('throughput_per_hour', 0):.0f} veh/h, "
                f"avg_delay={stats.get('avg_delay', 0):.1f}s, "
                f"wall_time={wall_time:.1f}s")
    logger.info("Incident scenario complete.")


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    run_incident(quick=quick)
