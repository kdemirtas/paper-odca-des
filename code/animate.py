"""Animate ODCA-DES simulation as a cell grid with vehicles colored by speed.

Runs a short simulation, reconstructs vehicle positions at each frame from
trajectory records, and renders as a Matplotlib FuncAnimation.

Usage:
    python animate.py [--duration 120] [--fps 10] [--speed 5] [--window 200]
                      [--save animation.mp4]
"""

import argparse
import logging
from dataclasses import replace

import matplotlib

from config import sim_config
from odca.simulation.engine import Simulation

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Animate ODCA-DES simulation")
    parser.add_argument("--duration", type=float, default=120,
                        help="Simulation duration in seconds (default: 120)")
    parser.add_argument("--fps", type=float, default=10,
                        help="Animation frames per second (default: 10)")
    parser.add_argument("--speed", type=float, default=5,
                        help="Playback speed multiplier (default: 5)")
    parser.add_argument("--window", type=int, default=None,
                        help="Number of cells to show (default: all)")
    parser.add_argument("--save", type=str, default=None,
                        help="Save to file (e.g. animation.mp4 or animation.gif)")
    parser.add_argument("--av", type=float, default=0.0,
                        help="AV penetration rate 0.0-1.0 (default: 0.0)")
    parser.add_argument("--demand", type=float, default=1.0,
                        help="Demand multiplier (default: 1.0, try 1.5-2.0 for congestion)")
    parser.add_argument("--trajectory", action="store_true",
                        help="Generate time-space trajectory diagram instead")
    parser.add_argument("--lane", type=int, default=None,
                        help="Filter trajectories to a single lane (1-based)")
    args = parser.parse_args()

    if args.save:
        matplotlib.use("Agg")
    from odca.viewer.animation import animate_result, plot_trajectories

    config = sim_config(sim_duration=args.duration, warmup=0.0, av_penetration=args.av)
    if args.demand != 1.0:
        config = replace(config, demand={
            origin: {dest: rate * args.demand for dest, rate in row.items()}
            for origin, row in config.demand.items()
        })
    logger.info(f"Running simulation ({args.duration}s, AV={args.av:.0%}, "
                f"demand={args.demand:.1f}x)...")
    result = Simulation(config).run()

    if args.trajectory:
        plot_trajectories(result, lane_filter=args.lane,
                          save_path=args.save or "output/trajectories.pdf")
    else:
        animate_result(result, fps=args.fps, playback_speed=args.speed,
                       cell_window=args.window, save_path=args.save)


if __name__ == "__main__":
    main()
