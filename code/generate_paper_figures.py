"""Generate additional paper figures not covered by generate_figures.py.

Produces:
  - fig_fd_theoretical.pdf    : Analytical triangular FD with annotations
  - fig_tsd_freeflow.pdf      : Time-space diagram (free-flow, from S1)
  - fig_tsd_congested.pdf     : Time-space diagram (congested, from S1)
  - fig_speed_profile.pdf     : Travel speed vs running speed by position
  - fig_event_density.pdf     : Event density heatmap
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import CELL_LENGTH_M, HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
EXP_DIR = Path("output") / "experiments"


def fig_fd_theoretical():
    """Analytical triangular FD with annotated key points."""
    tau = HDV_DRIVER.tau
    v_max = HDV_VEHICLE.v_max
    d = HDV_VEHICLE.standstill_spacing

    k_jam = 1.0 / d
    q_max = v_max / (v_max * tau + d)
    k_crit = q_max / v_max
    w = d / tau

    # Convert to per-km and per-hour
    k_jam_km = k_jam / CELL_LENGTH_M * 1000
    q_max_h = q_max * 3600
    k_crit_km = k_crit / CELL_LENGTH_M * 1000
    v_max_kmh = v_max * CELL_LENGTH_M * 3.6
    w_kmh = w * CELL_LENGTH_M * 3.6

    # Build triangular FD
    k_free = np.linspace(0, k_crit_km, 100)
    q_free = k_free * v_max_kmh

    k_cong = np.linspace(k_crit_km, k_jam_km, 100)
    q_cong = q_max_h - w_kmh * (k_cong - k_crit_km)

    fig, ax = plt.subplots(figsize=(5.5, 4))

    # FD curves
    ax.plot(k_free, q_free, "b-", linewidth=2, label="Free-flow branch")
    ax.plot(k_cong, q_cong, "r-", linewidth=2, label="Congested branch")

    # Annotate capacity
    ax.plot(k_crit_km, q_max_h, "ko", markersize=7, zorder=5)
    ax.annotate(
        f"$(k_c, q_{{\\max}})$\n({k_crit_km:.1f}, {q_max_h:.0f})",
        xy=(k_crit_km, q_max_h),
        xytext=(k_crit_km + 15, q_max_h - 200),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="black", lw=1),
    )

    # Annotate jam density
    ax.plot(k_jam_km, 0, "ko", markersize=7, zorder=5)
    ax.annotate(
        f"$k_j = 1/\\ell$\n({k_jam_km:.1f} veh/km)",
        xy=(k_jam_km, 0),
        xytext=(k_jam_km - 30, 400),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="black", lw=1),
    )

    # Annotate slopes
    ax.annotate(
        f"slope = $v_f$ = {v_max_kmh:.0f} km/h",
        xy=(k_crit_km / 2, q_max_h / 2),
        xytext=(k_crit_km / 2 + 20, q_max_h / 2 + 100),
        fontsize=8, color="blue",
        arrowprops=dict(arrowstyle="->", color="blue", lw=0.8),
    )
    k_mid_cong = (k_crit_km + k_jam_km) / 2
    q_mid_cong = q_max_h - w_kmh * (k_mid_cong - k_crit_km)
    ax.annotate(
        f"slope = $-w$ = $-\\ell/\\tau$\n= {w_kmh:.0f} km/h",
        xy=(k_mid_cong, q_mid_cong),
        xytext=(k_mid_cong - 10, q_mid_cong + 400),
        fontsize=8, color="red",
        arrowprops=dict(arrowstyle="->", color="red", lw=0.8),
    )

    ax.set_xlabel("Density $k$ (veh/km)")
    ax.set_ylabel("Flow $q$ (veh/h)")
    ax.set_xlim(0, k_jam_km * 1.1)
    ax.set_ylim(0, q_max_h * 1.2)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_fd_theoretical.pdf")
    plt.close(fig)
    print("  -> fig_fd_theoretical.pdf")


def _load_scenario_vehicles(label: str):
    """Load trajectory data from scenario JSON."""
    path = EXP_DIR / f"{label}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def fig_tsd_combined():
    """Side-by-side time-space diagrams: (a) free-flow, (b) congested."""
    from config import sim_config
    from odca.params import NetworkConfig
    from odca.simulation.engine import Simulation

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- Panel (a): Free-flow ---
    config_ff = sim_config(
        network=NetworkConfig.corridor(num_lanes=1, num_cells=200, speed_limit=HDV_VEHICLE.v_max),
        demand={"mainline_lane_1": {"end": 800.0}},
        av_penetration=0.0,
        sim_duration=180.0,
        warmup=10.0,
        seed=ILLUSTRATIVE_SEED,
    )

    sim_ff = Simulation(config_ff)
    results_ff = sim_ff.run()

    for veh in results_ff.vehicles[:50]:
        if len(veh.trajectory) < 2:
            continue
        t = [r.time for r in veh.trajectory]
        x = [r.cell_idx * CELL_LENGTH_M for r in veh.trajectory]
        ax1.plot(t, x, "-", linewidth=0.5, alpha=0.7, color="#1f77b4")

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position (m)")
    ax1.set_title("(a) Free-flow (800 veh/h)")
    ax1.set_xlim(10, 120)
    ax1.grid(True, alpha=0.3)

    # --- Panel (b): Congested ---
    config_cg = sim_config(
        network=NetworkConfig.corridor(num_lanes=1, num_cells=200, speed_limit=HDV_VEHICLE.v_max),
        demand={"mainline_lane_1": {"end": 2400.0}},
        av_penetration=0.0,
        sim_duration=600.0,
        warmup=60.0,
        seed=ILLUSTRATIVE_SEED,
    )

    sim_cg = Simulation(config_cg)
    results_cg = sim_cg.run()

    for veh in results_cg.vehicles[:120]:
        if len(veh.trajectory) < 2:
            continue
        t = [r.time for r in veh.trajectory]
        x = [r.cell_idx * CELL_LENGTH_M for r in veh.trajectory]
        speeds = [r.speed * CELL_LENGTH_M * 3.6 for r in veh.trajectory]
        avg_speed = np.mean(speeds) if speeds else 140
        if avg_speed < 40:
            color = "#d62728"
        elif avg_speed < 100:
            color = "#ff7f0e"
        else:
            color = "#1f77b4"
        ax2.plot(t, x, "-", linewidth=0.5, alpha=0.7, color=color)

    ax2.set_xlabel("Time (s)")
    ax2.set_title("(b) Congested (2400 veh/h)")
    ax2.set_xlim(60, 250)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_tsd_combined.pdf")
    plt.close(fig)
    print("  -> fig_tsd_combined.pdf")


def fig_speed_profile():
    """Travel speed vs running speed by position from S1 experiment."""
    from config import sim_config
    from odca.simulation.engine import Simulation

    # Run S1-like scenario for speed profile
    config = sim_config(
        av_penetration=0.0,
        sim_duration=1200.0,
        warmup=120.0,
        seed=ILLUSTRATIVE_SEED,
    )

    sim = Simulation(config)
    results = sim.run()
    vehicles = results.completed_vehicles

    # Compute per-cell travel speed
    num_cells = config.network.num_cells
    travel_speeds = [[] for _ in range(num_cells)]
    running_speeds = [[] for _ in range(num_cells)]

    for veh in vehicles:
        # same vehicle set as summary_statistics: exits in the measurement period (D-2026-09-19-14)
        if veh.time_exited is None or veh.time_exited < config.warmup:
            continue
        traj = veh.trajectory
        for i in range(len(traj) - 1):
            r0, r1 = traj[i], traj[i + 1]
            if r0.lane_idx != r1.lane_idx:
                continue  # skip lane changes
            dt = r1.time - r0.time
            if dt <= 0:
                continue
            cell_idx = r0.cell_idx
            if 0 <= cell_idx < num_cells:
                v_travel = CELL_LENGTH_M / dt  # m/s
                v_travel_kmh = v_travel * 3.6
                travel_speeds[cell_idx].append(v_travel_kmh)
                running_speeds[cell_idx].append(r0.speed * CELL_LENGTH_M * 3.6)

    positions = np.arange(num_cells) * CELL_LENGTH_M / 1000  # km
    avg_travel = np.array([np.mean(s) if s else np.nan for s in travel_speeds])
    avg_running = np.array([np.mean(s) if s else np.nan for s in running_speeds])

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(positions, avg_travel, "-", color="#1f77b4", linewidth=1.2,
            label="Travel speed")
    ax.plot(positions, avg_running, "--", color="#ff7f0e", linewidth=1.2,
            label="Running speed")

    # Mark ramp locations
    for ramp in config.network.onramp_cells:
        ax.axvline(ramp * CELL_LENGTH_M / 1000, color="green", ls=":",
                   alpha=0.5, lw=0.8)
    for ramp in config.network.offramp_cells:
        ax.axvline(ramp * CELL_LENGTH_M / 1000, color="red", ls=":",
                   alpha=0.5, lw=0.8)

    ax.set_xlabel("Position (km)")
    ax.set_ylabel("Speed (km/h)")
    ax.set_title("Average Travel Speed vs Running Speed (S1 Baseline)")
    ax.legend()
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_speed_profile.pdf")
    plt.close(fig)
    print("  -> fig_speed_profile.pdf")


def fig_event_density():
    """Event density heatmap from S1 experiment."""
    from config import sim_config
    from odca.simulation.engine import Simulation

    config = sim_config(
        av_penetration=0.0,
        sim_duration=1200.0,
        warmup=120.0,
        seed=ILLUSTRATIVE_SEED,
    )

    sim = Simulation(config)
    results = sim.run()
    vehicles = results.vehicles

    num_cells = config.network.num_cells
    num_lanes = config.network.num_lanes
    time_bins = 60  # number of time bins
    dt = (config.sim_duration - config.warmup) / time_bins

    # Count trajectory records per (lane, cell, time_bin)
    heatmap = np.zeros((num_lanes, num_cells, time_bins))

    for veh in vehicles:
        for r in veh.trajectory:
            if r.time < config.warmup:
                continue
            t_bin = int((r.time - config.warmup) / dt)
            if 0 <= t_bin < time_bins and 0 < r.lane_idx <= num_lanes:
                c_idx = min(r.cell_idx, num_cells - 1)
                heatmap[r.lane_idx - 1, c_idx, t_bin] += 1

    # Average over time to get per-cell-per-lane event rate
    event_rate = heatmap.sum(axis=2) / (config.sim_duration - config.warmup)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    positions_km = np.arange(num_cells) * CELL_LENGTH_M / 1000
    lane_labels = [f"Lane {i+1}" for i in range(num_lanes)]

    im = ax.imshow(
        event_rate, aspect="auto", origin="lower",
        extent=[0, positions_km[-1], 0.5, num_lanes + 0.5],
        cmap="YlOrRd",
    )
    ax.set_xlabel("Position (km)")
    ax.set_ylabel("Lane")
    ax.set_yticks(range(1, num_lanes + 1))
    ax.set_yticklabels(lane_labels)
    ax.set_title("Event Density (events/s/cell)")
    plt.colorbar(im, ax=ax, label="Events/s")

    # Mark ramp locations
    for ramp in config.network.onramp_cells:
        ax.axvline(ramp * CELL_LENGTH_M / 1000, color="white", ls="--",
                   alpha=0.8, lw=1)
    for ramp in config.network.offramp_cells:
        ax.axvline(ramp * CELL_LENGTH_M / 1000, color="cyan", ls="--",
                   alpha=0.8, lw=1)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_event_density.pdf")
    plt.close(fig)
    print("  -> fig_event_density.pdf")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating additional paper figures...")

    # Analytical FD (no simulation needed)
    fig_fd_theoretical()

    # Time-space diagrams (run quick simulations)
    print("\nGenerating time-space diagrams (running quick sims)...")
    fig_tsd_combined()

    # Speed profile and event density (run S1-like sim)
    print("\nGenerating speed profile and event density...")
    fig_speed_profile()
    fig_event_density()

    print("\nAll additional figures generated.")


if __name__ == "__main__":
    main()
