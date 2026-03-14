"""Bottleneck experiment: lane closure creating congestion dynamics.

Simulates a lane drop (lane closure) on the leftmost lane starting at a
specified cell. Measures queue formation, throughput drop, and recovery
across AV penetration scenarios.

Usage:
    python run_bottleneck.py [--quick]
"""

import json
import logging
import sys
import time
from pathlib import Path

from config import SimConfig, NetworkConfig, ODFlow, CELL_LENGTH_M, HDV_PARAMS
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
CLOSURE_START = 300    # closure begins at cell 300
CLOSURE_END = 599      # closure extends to end of network
MAINLINE_FLOW = 3600   # veh/h total (1200/lane) — moderately above 2-lane capacity
SEED_SPACING = 25      # cells between initial vehicles

# Edie measurement regions: upstream and downstream of bottleneck
UPSTREAM_REGION = (200, 280)    # 80 cells upstream of closure
DOWNSTREAM_REGION = (350, 450)  # 100 cells downstream in the 2-lane section

AV_SCENARIOS = [
    ("BN_0av", 0.0),
    ("BN_30av", 0.3),
    ("BN_50av", 0.5),
    ("BN_70av", 0.7),
]


def run_bottleneck_scenario(
    label: str, av_pen: float, quick: bool = False
) -> dict:
    """Run a bottleneck scenario with lane closure."""
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

    # Block lane BEFORE seeding so seed_vehicles skips blocked cells
    sim.freeway.block_cells(
        lane_idx=CLOSURE_LANE,
        start_cell=CLOSURE_START,
        end_cell=CLOSURE_END,
    )
    logger.info(
        f"  Lane {CLOSURE_LANE} blocked: cells {CLOSURE_START}-{CLOSURE_END}"
    )

    # Seed road with vehicles at free-flow density (blocked cells skipped)
    sim.seed_vehicles(spacing=SEED_SPACING, destination_cell_idx=NUM_CELLS)

    t0 = time.time()
    results = sim.run()
    wall_time = time.time() - t0

    # Summary statistics
    stats = summary_statistics(
        results["completed_vehicles"],
        warmup=config.warmup,
        sim_duration=config.sim_duration,
    )
    stats["wall_time_s"] = round(wall_time, 2)

    # Edie's FD at upstream and downstream regions
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

    return {
        "label": label,
        "av_penetration": av_pen,
        "stats": stats,
        "counters": results.get("counters", {}),
        "fd_data": fd_json,
        "closure": {
            "lane": CLOSURE_LANE,
            "start_cell": CLOSURE_START,
            "end_cell": CLOSURE_END,
        },
    }


def main():
    quick = "--quick" in sys.argv

    out_dir = Path("output") / "bottleneck"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = []
    for label, av_pen in AV_SCENARIOS:
        logger.info(f"=== {label} (AV={av_pen:.0%}) ===")
        result = run_bottleneck_scenario(label, av_pen, quick=quick)

        logger.info(f"  Throughput: {result['stats'].get('throughput_per_hour', 0):.0f} veh/h")
        logger.info(f"  Avg delay: {result['stats'].get('avg_delay', 0):.1f}s")
        logger.info(f"  Wall time: {result['stats'].get('wall_time_s', 0):.1f}s")

        # Save individual scenario
        with open(out_dir / f"{label}.json", "w") as f:
            json.dump(result, f, indent=2, default=str)

        all_results.append(result)

    # Save summary comparison
    summary = []
    for r in all_results:
        summary.append({
            "label": r["label"],
            "av_penetration": r["av_penetration"],
            **r["stats"],
            **{f"cnt_{k}": v for k, v in r["counters"].items()},
        })

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    logger.info(f"Summary saved to {out_dir / 'summary.json'}")
    logger.info("Bottleneck experiments complete.")


if __name__ == "__main__":
    main()
