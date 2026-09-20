"""The representation figure of Section 4.3: NaSch beside ODCA-DES on the same platoon.

Both models start the same eight vehicles from standstill on the same cells of the same road and
run deterministically (no random slowdown, no driver heterogeneity), so the picture shows what the
two paradigms represent differently and nothing else:

  NaSch     fixed space, fixed time, integer speed: a position only at whole seconds, and a jump
            of a whole number of cells.
  ODCA-DES  fixed space, continuous time, continuous speed: a cell is entered at any real instant,
            at any speed in [0, v_max].

Each model runs at the top speed it can represent, which is part of the point: the paper's HDV
holds 5.2 cells/s (140 km/h), and an integer-speed CA has no such value, only 5 cells/s (135 km/h)
or 6 (162 km/h).

Writes `figures/fig_paradigm_comparison.pdf` (D-2026-09-20-9).

Usage:
    .venv/bin/python plot_paradigm_comparison.py
"""

import logging
from dataclasses import replace as dc_replace
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import simpy

from config import FIGURES_DIR, HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED
from odca.baselines.nasch import NaSchConfig, NaSchSimulation
from odca.entity.driver import DriverStreams, HumanDriver, TraitSampler
from odca.entity.vehicle import Vehicle
from odca.infrastructure.freeway import Freeway
from odca.params import NetworkConfig
from odca.rng import RNGRegistry

logging.basicConfig(level=logging.WARNING)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

NUM_CELLS = 200          # long enough that nothing wraps or exits inside the window
START_CELLS = [10, 13, 16, 19, 22, 25, 28, 31]   # a standing platoon, 3 cells apart
WINDOW_S = 15.0          # the window both panels show
V_MAX = HDV_VEHICLE.v_max     # 5.2 cells/s, the paper's HDV top speed (140 km/h)
V_MAX_NASCH = int(V_MAX)      # 5 cells per step: the nearest an integer-speed CA can hold
FOCUS = 4                # the vehicle panel (c) follows, counted from the back of the platoon

# deterministic drivers: the figure is about representation, not about randomness
DETERMINISTIC_DRIVER = dc_replace(
    HDV_DRIVER, slowdown_prob=0.0, slowdown_prob_std=0.0,
    tau_std=0.0, action_interval_std=0.0,
)
DETERMINISTIC_VEHICLE = HDV_VEHICLE


def nasch_trajectories() -> List[List[Tuple[float, int, int]]]:
    """One (time, cell, speed) list per vehicle, from the NaSch rules on the platoon.

    The road is set directly so both models start from the same cells; nothing wraps inside the
    window, so the vehicles keep their order and rank identifies them.
    """
    sim = NaSchSimulation(NaSchConfig(
        num_cells=NUM_CELLS, v_max=V_MAX_NASCH, slowdown_prob=0.0,
        density=0.0, seed=ILLUSTRATIVE_SEED,
    ))
    sim.road[:] = -1
    for cell in START_CELLS:
        sim.road[cell] = 0

    tracks: List[List[Tuple[float, int, int]]] = [[(0.0, c, 0)] for c in START_CELLS]
    for step in range(1, int(WINDOW_S) + 1):
        positions, speeds = sim.step()
        for rank, (pos, v) in enumerate(zip(positions, speeds)):
            tracks[rank].append((float(step), pos, v))
    return tracks


def odca_trajectories() -> List[List[Tuple[float, int, float]]]:
    """One (time, cell, speed) list per vehicle, from an ODCA-DES run of the same platoon."""
    registry = RNGRegistry(master_seed=ILLUSTRATIVE_SEED)
    streams = DriverStreams.spawn(registry)
    sampler = TraitSampler.spawn(registry)
    Vehicle._id_counter = 0

    env = simpy.Environment()
    freeway = Freeway(env, NetworkConfig.corridor(1, NUM_CELLS, V_MAX))
    lane = freeway.lane(1)

    vehicles = []
    for cell in START_CELLS:
        driver = HumanDriver(DETERMINISTIC_DRIVER, streams, sampler.draw(DETERMINISTIC_DRIVER))
        vehicle = Vehicle(env, DETERMINISTIC_VEHICLE, driver, lane.cells[cell])
        vehicles.append(vehicle)
        env.process(vehicle.start())

    env.run(until=WINDOW_S)
    return [[(r.time, r.cell_idx, r.speed) for r in v.trajectory if r.time <= WINDOW_S]
            for v in vehicles]


def _draw_time_space(ax, tracks, title: str, stepped: bool, markersize: float = 2.6):
    """Draw one time-space panel.

    Args:
        ax: the axes to draw on.
        tracks: one (time, cell, speed) list per vehicle.
        title: the panel title.
        stepped: hold each position until the next update (NaSch), else join the points (ODCA).
        markersize: size of the marker drawn at every recorded position.
    """
    for track in tracks:
        times = [t for t, _, _ in track]
        cells = [c for _, c, _ in track]
        ax.plot(times, cells, drawstyle="steps-post" if stepped else "default",
                color="#1f77b4", linewidth=1.0, zorder=2)
        ax.plot(times, cells, linestyle="none", marker="o", markersize=markersize,
                color="#d62728", zorder=3)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("time (s)")
    ax.set_xlim(0, WINDOW_S)
    ax.grid(True, which="both", alpha=0.25, linewidth=0.4)


def main():
    """Draw the three panels and write the figure."""
    nasch, odca = nasch_trajectories(), odca_trajectories()

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6))

    _draw_time_space(axes[0], nasch, "(a) NaSch: whole seconds, whole cells", stepped=True)
    axes[0].set_ylabel("cell")
    axes[0].set_xticks(range(0, int(WINDOW_S) + 1, 1))
    axes[0].tick_params(axis="x", labelsize=7)

    _draw_time_space(axes[1], odca, "(b) ODCA-DES: any instant, whole cells", stepped=False,
                     markersize=1.5)
    axes[1].set_xticks(range(0, int(WINDOW_S) + 1, 3))

    lo = min(min(c for _, c, _ in t) for t in nasch + odca)
    hi = max(max(c for _, c, _ in t) for t in nasch + odca)
    for ax in axes[:2]:
        ax.set_ylim(lo - 1, hi + 1)

    ax = axes[2]
    n_times = [t for t, _, _ in nasch[FOCUS]]
    n_speeds = [v for _, _, v in nasch[FOCUS]]
    o_times = [t for t, _, _ in odca[FOCUS]]
    o_speeds = [v for _, _, v in odca[FOCUS]]
    ax.plot(n_times, n_speeds, drawstyle="steps-post", color="#7f7f7f",
            linewidth=1.4, label=f"NaSch (integer, max {V_MAX_NASCH})")
    ax.plot(o_times, o_speeds, drawstyle="steps-post", color="#1f77b4",
            linewidth=1.4, label=f"ODCA-DES (real, max {V_MAX})")
    ax.plot(o_times, o_speeds, linestyle="none", marker="o", markersize=2.6, color="#d62728")
    for level in range(V_MAX_NASCH + 1):
        ax.axhline(level, color="#7f7f7f", linewidth=0.4, alpha=0.35, zorder=1)
    ax.axhline(V_MAX, color="#1f77b4", linewidth=0.5, linestyle=":", alpha=0.8, zorder=1)
    ax.text(WINDOW_S * 0.02, V_MAX + 0.06, f"$v_{{\\max}} = {V_MAX}$ cells/s (140 km/h)",
            fontsize=7, color="#1f77b4")
    ax.set_title(f"(c) speed of vehicle {FOCUS + 1}", fontsize=10)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("speed (cells/s)")
    ax.set_xlim(0, WINDOW_S)
    ax.set_ylim(-0.2, V_MAX + 0.6)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.25, linewidth=0.4)

    fig.tight_layout()
    out = FIGURES_DIR / "fig_paradigm_comparison.pdf"
    fig.savefig(out)
    plt.close(fig)

    speeds = sorted({round(v, 3) for t in odca for _, _, v in t})
    print(f"wrote {out}")
    print(f"NaSch distinct speeds: {sorted({v for t in nasch for _, _, v in t})}")
    print(f"ODCA distinct speeds: {len(speeds)} values, "
          f"{speeds[0]:.3f} to {speeds[-1]:.3f} cells/s")
    entries = sorted(t for track in odca for t, _, _ in track)
    whole = sum(1 for t in entries if abs(t - round(t)) < 1e-9)
    print(f"ODCA cell entries: {len(entries)}, of which {whole} fall on a whole second")


if __name__ == "__main__":
    main()
