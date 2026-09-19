"""Interactive Pygame visualization for ODCA-DES simulation.

Runs the S1 scenario, then replays it with `odca.viewer.playback` (controls listed there).

Usage:
    python visualize.py [--duration 300] [--av 0.0] [--demand 1.0] [--seed 42]
    python visualize.py --record output.mp4 [--record-speed 5] [--record-fps 30]
"""

import argparse
import logging
from dataclasses import replace

from config import sim_config
from odca.simulation.engine import Simulation
from odca.viewer.playback import TrafficVisualizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Interactive Pygame visualization for ODCA-DES")
    parser.add_argument("--duration", type=float, default=300,
                        help="Simulation duration in seconds (default: 300)")
    parser.add_argument("--av", type=float, default=0.0,
                        help="AV penetration rate 0.0-1.0 (default: 0.0)")
    parser.add_argument("--demand", type=float, default=1.0,
                        help="Demand multiplier (default: 1.0)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--record", type=str, default=None,
                        help="Record to MP4 file (e.g. --record demo.mp4)")
    parser.add_argument("--record-speed", type=float, default=5.0,
                        help="Playback speed for recording (default: 5.0)")
    parser.add_argument("--record-fps", type=int, default=30,
                        help="Video FPS for recording (default: 30)")
    args = parser.parse_args()

    config = sim_config(sim_duration=args.duration, warmup=0.0, av_penetration=args.av,
                        seed=args.seed)
    if args.demand != 1.0:
        config = replace(config, demand={
            origin: {dest: rate * args.demand for dest, rate in row.items()}
            for origin, row in config.demand.items()
        })
    logger.info(f"Running simulation ({args.duration}s, AV={args.av:.0%}, "
                f"demand={args.demand:.1f}x, seed={args.seed})...")
    result = Simulation(config).run()
    logger.info(f"{len(result.vehicles)} vehicles ({result.num_completed} completed)")
    viz = TrafficVisualizer.from_result(result)
    if args.record:
        viz.record(args.record, playback_speed=args.record_speed, fps=args.record_fps)
    else:
        viz.run()


if __name__ == "__main__":
    main()
