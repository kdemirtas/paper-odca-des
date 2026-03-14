"""Animate ODCA-DES simulation as a cell grid with vehicles colored by speed.

Runs a short simulation, reconstructs vehicle positions at each frame from
trajectory records, and renders as a Matplotlib FuncAnimation.

Usage:
    python animate.py [--duration 120] [--fps 10] [--speed 5] [--window 200]
                      [--save animation.mp4]
"""

import argparse
import logging
import sys
from bisect import bisect_right
from typing import Dict, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.animation import FuncAnimation

from config import SimConfig, CELL_LENGTH_M
from odca.entity.vehicle import Vehicle, VehicleType, TrajectoryRecord
from odca.simulation.engine import Simulation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────
# Trajectory index: fast lookup of vehicle positions at arbitrary times
# ──────────────────────────────────────────────────────────────────────

class VehicleSnapshot:
    """Pre-indexed trajectory for fast position lookup."""

    def __init__(self, vehicle: Vehicle):
        self.vid = vehicle.id
        self.vtype = vehicle.vtype
        traj = vehicle.trajectory
        self.times = [r.time for r in traj]
        self.cells = [r.cell_idx for r in traj]
        self.lanes = [r.lane_idx for r in traj]
        self.speeds = [r.speed for r in traj]
        self.t_enter = vehicle.time_entered
        self.t_exit = vehicle.time_exited

    def at(self, t: float) -> Optional[Tuple[int, int, float]]:
        """Return (cell_idx, lane_idx, speed) at time t, or None."""
        if self.t_enter is None or t < self.t_enter:
            return None
        if self.t_exit is not None and t >= self.t_exit:
            return None
        idx = bisect_right(self.times, t) - 1
        if idx < 0:
            return None
        return self.cells[idx], self.lanes[idx], self.speeds[idx]


def build_snapshots(vehicles: List[Vehicle]) -> List[VehicleSnapshot]:
    return [VehicleSnapshot(v) for v in vehicles if v.trajectory]


# ──────────────────────────────────────────────────────────────────────
# Grid reconstruction
# ──────────────────────────────────────────────────────────────────────

def reconstruct_grid(snapshots: List[VehicleSnapshot], t: float,
                     num_lanes: int, num_cells: int) -> np.ndarray:
    """Build a (num_lanes, num_cells) array: NaN = empty, value = speed."""
    grid = np.full((num_lanes, num_cells), np.nan)
    for snap in snapshots:
        pos = snap.at(t)
        if pos is None:
            continue
        cell_idx, lane_idx, speed = pos
        if 0 <= cell_idx < num_cells and 1 <= lane_idx <= num_lanes:
            row = num_lanes - lane_idx  # lane 1 (rightmost) at bottom
            grid[row, cell_idx] = speed
    return grid


# ──────────────────────────────────────────────────────────────────────
# Animation
# ──────────────────────────────────────────────────────────────────────

def _upscale_grid(grid: np.ndarray, row_height: int, col_width: int) -> np.ndarray:
    """Repeat each cell into a (row_height x col_width) block for visibility."""
    return np.repeat(np.repeat(grid, row_height, axis=0), col_width, axis=1)


def _draw_lane_dividers(ax, num_lanes: int, row_height: int, width: int):
    """Draw white lines between lanes."""
    for i in range(1, num_lanes):
        y = i * row_height - 0.5
        ax.axhline(y, color="white", lw=2)


def animate_simulation(
    snapshots: List[VehicleSnapshot],
    num_lanes: int,
    num_cells: int,
    sim_duration: float,
    v_max: float,
    fps: float = 10,
    playback_speed: float = 5.0,
    cell_window: Optional[int] = None,
    onramp_cells: Optional[List[int]] = None,
    offramp_cells: Optional[List[int]] = None,
    save_path: Optional[str] = None,
):
    """Create and display/save the animation."""
    dt = playback_speed / fps  # sim-seconds per frame
    times = np.arange(0, sim_duration, dt)

    # Viewing window
    window = cell_window or num_cells
    cell_lo = 0

    # Upscale: each cell becomes (row_height x col_width) pixels
    row_height = 20
    col_width = 3

    # Colormap: gray (stopped) -> red (slow) -> yellow -> green (v_max)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "traffic", ["#888888", "#d62728", "#ff7f0e", "#2ca02c"], N=256,
    )
    cmap.set_bad(color=(0.93, 0.93, 0.93, 1.0))  # empty cells: light gray
    norm = mcolors.Normalize(vmin=0, vmax=v_max)

    # Figure setup
    disp_w = window * col_width
    disp_h = num_lanes * row_height
    fig_w = min(20, max(12, disp_w / 80))
    fig_h = max(3.0, disp_h / 40 + 1.5)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    grid0 = reconstruct_grid(snapshots, 0, num_lanes, num_cells)
    view = np.ma.masked_invalid(grid0[:, cell_lo:cell_lo + window])
    upscaled = _upscale_grid(view, row_height, col_width)

    im = ax.imshow(
        upscaled, aspect="auto", interpolation="nearest",
        cmap=cmap, norm=norm,
    )

    _draw_lane_dividers(ax, num_lanes, row_height, disp_w)

    # Mark ramps
    if onramp_cells:
        for c in onramp_cells:
            if cell_lo <= c < cell_lo + window:
                x = (c - cell_lo) * col_width
                ax.axvline(x, color="#1f77b4", lw=1.5, ls="--", alpha=0.6)
    if offramp_cells:
        for c in offramp_cells:
            if cell_lo <= c < cell_lo + window:
                x = (c - cell_lo) * col_width
                ax.axvline(x, color="#d62728", lw=1.5, ls="--", alpha=0.6)

    # Lane labels
    lane_labels = [f"L{num_lanes - i}" for i in range(num_lanes)]
    lane_centers = [i * row_height + row_height // 2 for i in range(num_lanes)]
    ax.set_yticks(lane_centers)
    ax.set_yticklabels(lane_labels)

    # X-axis in km
    xtick_step = max(1, window // 10) * col_width
    xticks = list(range(0, disp_w, xtick_step))
    ax.set_xticks(xticks)
    ax.set_xticklabels(
        [f"{(cell_lo + x // col_width) * CELL_LENGTH_M / 1000:.1f}" for x in xticks]
    )
    ax.set_xlabel("Position (km)")

    title = ax.set_title("t = 0.0 s", fontsize=12, fontweight="bold")
    fig.colorbar(im, ax=ax, label="Speed (cells/s)", shrink=0.8, pad=0.02)

    count_text = ax.text(
        0.01, 1.02, "", transform=ax.transAxes, fontsize=9,
        verticalalignment="bottom",
    )

    fig.tight_layout()

    def update(frame_idx):
        t = times[frame_idx]
        grid = reconstruct_grid(snapshots, t, num_lanes, num_cells)
        view = np.ma.masked_invalid(grid[:, cell_lo:cell_lo + window])
        upscaled = _upscale_grid(view, row_height, col_width)
        im.set_data(upscaled)

        title.set_text(f"t = {t:.1f} s")
        n_active = np.count_nonzero(~np.isnan(grid))
        count_text.set_text(f"Vehicles: {n_active}")

        return [im, title, count_text]

    anim = FuncAnimation(
        fig, update, frames=len(times),
        interval=1000 / fps, blit=True,
    )

    if save_path:
        logger.info(f"Saving animation to {save_path} ({len(times)} frames)...")
        if save_path.endswith(".gif"):
            anim.save(save_path, writer="pillow", fps=fps)
        else:
            anim.save(save_path, writer="ffmpeg", fps=fps, dpi=120)
        logger.info(f"Saved: {save_path}")
    else:
        plt.show()

    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Time-space trajectory diagram
# ──────────────────────────────────────────────────────────────────────

def _split_contiguous_segments(traj: list, max_gap: float = 2.0):
    """Split trajectory records into contiguous segments.

    Breaks whenever the time gap between consecutive records exceeds
    max_gap, which indicates the vehicle was in a different lane.
    """
    if not traj:
        return []
    segments = []
    current = [traj[0]]
    for i in range(1, len(traj)):
        if traj[i].time - traj[i - 1].time > max_gap:
            if len(current) >= 2:
                segments.append(current)
            current = []
        current.append(traj[i])
    if len(current) >= 2:
        segments.append(current)
    return segments


def _draw_lane_trajectories(
    ax, vehicles: List[Vehicle], lane_idx: int, v_max: float,
    cmap, norm,
    t_range: Optional[Tuple[float, float]] = None,
    cell_range: Optional[Tuple[int, int]] = None,
):
    """Draw trajectories for a single lane onto the given axes."""
    for veh in vehicles:
        traj = [r for r in veh.trajectory if r.lane_idx == lane_idx]
        segments = _split_contiguous_segments(traj)

        for seg in segments:
            times = [r.time for r in seg]
            cells = [r.cell_idx for r in seg]
            speeds = [r.speed for r in seg]

            if t_range:
                mask = [(t_range[0] <= t <= t_range[1]) for t in times]
                times = [t for t, m in zip(times, mask) if m]
                cells = [c for c, m in zip(cells, mask) if m]
                speeds = [s for s, m in zip(speeds, mask) if m]
            if cell_range:
                mask = [(cell_range[0] <= c <= cell_range[1]) for c in cells]
                times = [t for t, m in zip(times, mask) if m]
                cells = [c for c, m in zip(cells, mask) if m]
                speeds = [s for s, m in zip(speeds, mask) if m]

            if len(times) < 2:
                continue

            positions_km = [c * CELL_LENGTH_M / 1000 for c in cells]
            for i in range(len(times) - 1):
                color = cmap(norm(speeds[i]))
                ax.plot(
                    [times[i], times[i + 1]],
                    [positions_km[i], positions_km[i + 1]],
                    color=color, linewidth=0.8, solid_capstyle="round",
                )


def plot_trajectories(
    vehicles: List[Vehicle],
    v_max: float,
    num_lanes: int = 4,
    lane_filter: Optional[int] = None,
    t_range: Optional[Tuple[float, float]] = None,
    cell_range: Optional[Tuple[int, int]] = None,
    save_path: Optional[str] = None,
):
    """Plot time-space diagram with trajectories colored by speed.

    If lane_filter is set, plots a single lane. Otherwise plots all lanes
    as vertically stacked subplots (lane 1 at bottom, highest lane at top).
    """
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "traffic", ["#888888", "#d62728", "#ff7f0e", "#2ca02c"], N=256,
    )
    norm = mcolors.Normalize(vmin=0, vmax=v_max)

    if lane_filter is not None:
        lanes = [lane_filter]
    else:
        lanes = list(range(num_lanes, 0, -1))  # top-to-bottom: L4, L3, L2, L1

    n = len(lanes)
    fig_h = 6.0 if n == 1 else 3.0 * n
    fig, axes = plt.subplots(n, 1, figsize=(14, fig_h), sharex=True, sharey=True,
                             squeeze=False)
    axes = [ax for ax in axes[:, 0]]

    for ax, lane_idx in zip(axes, lanes):
        _draw_lane_trajectories(ax, vehicles, lane_idx, v_max, cmap, norm,
                                t_range, cell_range)
        ax.set_ylabel(f"Lane {lane_idx}\nPosition (km)")

    axes[-1].set_xlabel("Time (s)")
    title = "Time-Space Diagram"
    if lane_filter is not None:
        title += f" (Lane {lane_filter})"
    fig.suptitle(title, fontsize=13, fontweight="bold")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=axes, label="Speed (cells/s)", shrink=0.6, pad=0.02)
    fig.subplots_adjust(hspace=0.15, top=0.94)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved trajectory plot: {save_path}")
    else:
        plt.show()
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def _run_sim(args):
    """Run simulation and return (results, config)."""
    from config import ODFlow
    config = SimConfig(
        sim_duration=args.duration,
        warmup=0.0,
        av_penetration=args.av,
    )
    # Scale demand if requested
    if args.demand != 1.0:
        config.od_flows = [
            ODFlow(od.origin_id, destination_cell=od.destination_cell,
                   flow_rate=od.flow_rate * args.demand,
                   destinations=od.destinations)
            for od in config.od_flows
        ]
    logger.info(
        f"Running simulation ({args.duration}s, AV={args.av:.0%}, "
        f"demand={args.demand:.1f}x)..."
    )
    sim = Simulation(config)
    return sim.run(), config


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

    # Use non-interactive backend when saving
    if args.save:
        matplotlib.use("Agg")

    results, config = _run_sim(args)
    vehicles = results["vehicles"]
    net = config.network

    if args.trajectory:
        logger.info(f"Plotting trajectories for {len(vehicles)} vehicles...")
        save = args.save or "output/trajectories.pdf"
        plot_trajectories(
            vehicles=vehicles,
            v_max=config.hdv_params.v_max,
            num_lanes=net.num_lanes,
            lane_filter=args.lane,
            save_path=save,
        )
    else:
        logger.info(f"Building animation from {len(vehicles)} vehicles...")
        snapshots = build_snapshots(vehicles)
        animate_simulation(
            snapshots=snapshots,
            num_lanes=net.num_lanes,
            num_cells=net.num_cells,
            sim_duration=args.duration,
            v_max=config.hdv_params.v_max,
            fps=args.fps,
            playback_speed=args.speed,
            cell_window=args.window,
            onramp_cells=net.onramp_cells,
            offramp_cells=net.offramp_cells,
            save_path=args.save,
        )


if __name__ == "__main__":
    main()
