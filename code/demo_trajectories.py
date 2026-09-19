"""Demonstration run: trajectories on a 3-lane corridor with lane crossing and an incident.

D-2026-09-19-36.

Not a manuscript figure. Runs `configs/demo_corridor.yaml` (every mainline lane sends traffic
to every lane end, 20% AVs, lane 2 blocked for two minutes) and draws
  (a) the time-space diagram of each lane, coloured by speed, with lane-change arrivals marked;
  (b) the lane against position of the vehicles going from lane 1 to the end of lane 3.
Writes figures/demo_trajectories.pdf and .png, and prints the run's counters.

Usage:
    .venv/bin/python demo_trajectories.py
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

from config import CELL_LENGTH_M, CONFIG_DIR
from odca.simulation.engine import Simulation

logging.basicConfig(level=logging.WARNING)

FIGURES = Path(__file__).resolve().parent.parent / "figures"
KMH = CELL_LENGTH_M * 3.6  # cells/s to km/h
KM = CELL_LENGTH_M / 1000.0  # cells to km


def lane_segments(vehicles, lane_idx):
    """Line segments (time, km) and their speeds (km/h) for every vehicle while in `lane_idx`.

    Args:
        vehicles: the run's vehicles.
        lane_idx: the lane to draw.
    """
    segments, speeds = [], []
    for v in vehicles:
        traj = v.trajectory
        for a, b in zip(traj, traj[1:]):
            if a.lane_idx == lane_idx and b.lane_idx == lane_idx:
                segments.append([(a.time, a.cell_idx * KM), (b.time, b.cell_idx * KM)])
                speeds.append(a.speed * KMH)
    return segments, np.array(speeds)


def lane_change_points(vehicles, lane_idx):
    """(time, km) where a vehicle arrived in `lane_idx` from another lane.

    Args:
        vehicles: the run's vehicles.
        lane_idx: the lane arrived in.
    """
    return [(b.time, b.cell_idx * KM) for v in vehicles
            for a, b in zip(v.trajectory, v.trajectory[1:])
            if b.lane_idx == lane_idx and a.lane_idx != lane_idx]


def main():
    """Run the demo corridor, draw both panels, save the figure and print the counters."""
    sim = Simulation(CONFIG_DIR / "demo_corridor.yaml")
    results = sim.run()
    cfg = sim.cfg
    vehicles = results.vehicles
    num_lanes = cfg.network.num_lanes

    fig = plt.figure(figsize=(11, 7.5))
    grid = fig.add_gridspec(num_lanes, 2, width_ratios=[2.2, 1], wspace=0.25, hspace=0.12)
    norm = plt.Normalize(0, cfg.hdv_vehicle.v_max * KMH)
    collection = None
    for row, lane_idx in enumerate(range(num_lanes, 0, -1)):  # leftmost lane on top
        ax = fig.add_subplot(grid[row, 0])
        segments, speeds = lane_segments(vehicles, lane_idx)
        collection = LineCollection(segments, cmap="RdYlGn", norm=norm, linewidths=0.6)
        collection.set_array(speeds)
        ax.add_collection(collection)
        points = lane_change_points(vehicles, lane_idx)
        if points:
            t, x = zip(*points)
            ax.scatter(t, x, s=3, c="black", zorder=3, label="lane-change arrival")
        for inc in cfg.incidents:
            if inc.lane == lane_idx:
                ax.add_patch(Rectangle((inc.start, inc.first_cell * KM), inc.duration,
                                       (inc.last_cell - inc.first_cell + 1) * KM,
                                       facecolor="none", edgecolor="black", hatch="///",
                                       label="blocked cells"))
                ax.legend(loc="upper left", fontsize=7, framealpha=0.9)
        ax.set_xlim(0, cfg.sim_duration)
        ax.set_ylim(0, cfg.network.num_cells * KM)
        ax.set_ylabel(f"lane {lane_idx}\nposition (km)")
        if row == 0:
            ax.set_title("(a) time-space diagram per lane")
            ax.legend(loc="upper left", fontsize=7, framealpha=0.9)
        if lane_idx == 1:
            ax.set_xlabel("time (s)")
        else:
            ax.tick_params(labelbottom=False)
    lane_axes = list(fig.axes)
    fig.colorbar(collection, ax=lane_axes, location="bottom", pad=0.09, fraction=0.04,
                 aspect=40, label="speed (km/h)")

    ax = fig.add_subplot(grid[:, 1])
    crossers = [v for v in vehicles if v.origin_cell.lane.idx == 1 and v.destination_lane == 3
                and v.time_exited is not None][:12]
    for v in crossers:
        x = [r.cell_idx * KM for r in v.trajectory]
        lane = [r.lane_idx for r in v.trajectory]
        ax.step(x, lane, where="post", lw=1.0, alpha=0.8,
                ls="--" if v.kind == "autonomous" else "-")
    ax.set_yticks(range(1, num_lanes + 1))
    ax.set_xlim(0, cfg.network.num_cells * KM)
    ax.set_xlabel("position (km)")
    ax.set_ylabel("lane")
    ax.set_title("(b) lane 1 to end of lane 3\n(dashed: AV)")

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"demo_trajectories.{ext}", dpi=200, bbox_inches="tight")
    counters = results.counters
    print(f"generated {results.num_generated}, completed {results.num_completed}, "
          f"active at end {results.num_active_at_end}")
    print(f"lane changes {counters.lane_changes}, lc failures {counters.lc_failures}, "
          f"missed exits {counters.missed_exits}, events {counters.simpy_events}")
    print(f"wrote {FIGURES / 'demo_trajectories.pdf'}")


if __name__ == "__main__":
    main()
