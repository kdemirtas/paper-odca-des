"""Run ODCA-DES simulation."""

import logging
import sys
import json
from pathlib import Path

from json_default import numpy_default
from config import SimConfig
from odca.simulation.engine import Simulation
from odca.analysis.metrics import summary_statistics, passage_time_flow

logger = logging.getLogger(__name__)


def run_scenario(config: SimConfig, label: str = "default") -> dict:
    """Run a single scenario and return results."""
    logger.info(f"=== Scenario: {label} (AV={config.av_penetration:.0%}) ===")

    sim = Simulation(config)
    results = sim.run()

    stats = summary_statistics(
        results["completed_vehicles"],
        warmup=config.warmup,
        sim_duration=config.sim_duration,
    )

    logger.info(f"--- Results for {label} ---")
    for k, v in stats.items():
        if isinstance(v, float):
            logger.info(f"  {k}: {v:.2f}")
        else:
            logger.info(f"  {k}: {v}")

    return {
        "label": label,
        "config": str(config),
        "stats": stats,
        "counters": results.get("counters", {}),
    }


def main():
    # Default: run baseline (0% AV)
    config = SimConfig()

    if "--debug" in sys.argv:
        config.log_level = logging.DEBUG

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # In debug mode, also write to a log file
    if config.log_level == logging.DEBUG:
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        fh = logging.FileHandler(out_dir / "debug.log", mode="w")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        ))
        logging.getLogger().addHandler(fh)
        logger.info(f"Debug log: {out_dir / 'debug.log'}")

    # Quick test: shorter duration
    if "--quick" in sys.argv:
        config.sim_duration = 120.0
        config.warmup = 10.0
        logger.info("Quick mode: 120s simulation")

    results = run_scenario(config, label="S1_baseline")

    # Save results
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2, default=numpy_default)
    logger.info(f"Results saved to {out_dir / 'results.json'}")


if __name__ == "__main__":
    main()
