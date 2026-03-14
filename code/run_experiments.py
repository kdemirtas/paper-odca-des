"""Run all ODCA-DES experiments for the paper.

Scenarios:
  S1: Baseline       (0% AV)
  S2: Low AV          (30% AV)
  S3: Medium AV       (50% AV)
  S4: High AV         (70% AV)

Each scenario runs for 3600s with 300s warmup.
Results are saved to output/ as JSON and CSV.
"""

import logging
import sys
import json
import csv
import time
from pathlib import Path
from dataclasses import asdict

from config import SimConfig
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


def run_scenario(label: str, av_pen: float, out_dir: Path, quick: bool = False):
    """Run a single scenario and save results."""
    config = SimConfig(av_penetration=av_pen)
    if quick:
        config.sim_duration = 300.0
        config.warmup = 30.0

    logger.info(f"=== {label} (AV={av_pen:.0%}) ===")

    t0 = time.time()
    sim = Simulation(config)
    results = sim.run()
    wall_time = time.time() - t0

    # Summary stats (post-warmup completed vehicles)
    stats = summary_statistics(
        results["completed_vehicles"],
        warmup=config.warmup,
        sim_duration=config.sim_duration,
    )
    stats["wall_time_s"] = round(wall_time, 2)
    stats["av_penetration"] = av_pen

    logger.info(f"  Wall time: {wall_time:.1f}s")
    for k, v in stats.items():
        if isinstance(v, float):
            logger.info(f"  {k}: {v:.2f}")
        else:
            logger.info(f"  {k}: {v}")

    # FD data at measurement cells
    fd_data = {}
    all_vehicles = results["vehicles"]
    for mc in FD_MEASUREMENT_CELLS:
        fd_data[mc] = passage_time_flow(
            all_vehicles,
            measurement_cell=mc,
            time_interval=60.0,
            sim_duration=config.sim_duration,
        )

    # Save scenario results
    scenario_out = {
        "label": label,
        "av_penetration": av_pen,
        "sim_duration": config.sim_duration,
        "warmup": config.warmup,
        "seed": config.seed,
        "stats": stats,
        "counters": results.get("counters", {}),
        "fd_data": {
            str(mc): [
                {"t": t, "flow": q, "density": k, "speed": v}
                for t, q, k, v in points
            ]
            for mc, points in fd_data.items()
        },
    }

    with open(out_dir / f"{label}.json", "w") as f:
        json.dump(scenario_out, f, indent=2, default=str)

    return stats, results.get("counters", {})


def main():
    quick = "--quick" in sys.argv
    if quick:
        logger.info("Quick mode: 300s simulations")

    out_dir = Path("output") / "experiments"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_stats = []
    all_counters = []

    for label, av_pen in SCENARIOS:
        stats, counters = run_scenario(label, av_pen, out_dir, quick=quick)
        all_stats.append({"label": label, **stats})
        all_counters.append({"label": label, **counters})

    # Write summary CSV
    if all_stats:
        keys = all_stats[0].keys()
        with open(out_dir / "summary.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_stats)
        logger.info(f"Summary CSV: {out_dir / 'summary.csv'}")

    # Write counters CSV
    if all_counters:
        keys = all_counters[0].keys()
        with open(out_dir / "counters.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_counters)

    logger.info("All experiments complete.")


if __name__ == "__main__":
    main()
