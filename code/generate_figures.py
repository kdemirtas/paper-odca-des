"""Generate all figures for the ODCA-DES paper.

Reads experiment results from output/ and produces:
  - fig_fd_validation.pdf         : Demand sweep FD vs analytical triangular FD
  - fig_fd_nasch_comparison.pdf   : ODCA-DES FD vs NaSch FD
  - fig_fd_scenarios.pdf          : FD across AV penetration scenarios
  - fig_throughput_bar.pdf        : Throughput comparison bar chart (multi-seed, 95% CI)
  - fig_travel_time.pdf           : Travel time and delay grouped bars (multi-seed, 95% CI)
  - fig_bottleneck_throughput.pdf : Bottleneck throughput by AV% (multi-seed, 95% CI)
  - fig_bottleneck_fd.pdf         : FD upstream vs downstream of bottleneck
  - fig_lc_logistic.pdf           : MLC + DLC logistic probability curves
  - fig_sensitivity_action_interval.pdf : S1 metrics vs HDV action_interval
  - fig_scalability.pdf           : Wall-clock vs network size (log-log)
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

from odca.baselines.nasch import NaSchConfig, sweep_density
from config import CELL_LENGTH_M, HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED

# Style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.figsize": (5.5, 4.0),
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
EXP_DIR = Path("output") / "experiments"
SWEEP_DIR = Path("output") / "demand_sweep"
BN_DIR = Path("output") / "bottleneck"
MULTISEED_S1S4_CSV = Path("output") / "multiseed" / "s1_s4" / "aggregate.csv"
MULTISEED_BN_CSV = Path("output") / "multiseed" / "bottleneck" / "bottleneck_aggregate.csv"
BN_DEMAND_VPH = 3600.0  # run_bottleneck.MAINLINE_FLOW: what the lane drop is asked to carry
SENSITIVITY_CSV = Path("output") / "sensitivity_action_interval" / "comparison.csv"
SCALABILITY_CSV = Path("output") / "scalability_benchmark.csv"

SCENARIO_LABELS = {
    "S1_baseline": "0% AV",
    "S2_low_av": "30% AV",
    "S3_med_av": "50% AV",
    "S4_high_av": "70% AV",
}
SCENARIO_COLORS = {
    "S1_baseline": "#1f77b4",
    "S2_low_av": "#ff7f0e",
    "S3_med_av": "#2ca02c",
    "S4_high_av": "#d62728",
}

INC_DIR = Path("output") / "incident"

BN_LABELS = {
    "BN_0av": "0% AV",
    "BN_30av": "30% AV",
    "BN_50av": "50% AV",
    "BN_70av": "70% AV",
}
BN_COLORS = {
    "BN_0av": "#1f77b4",
    "BN_30av": "#ff7f0e",
    "BN_50av": "#2ca02c",
    "BN_70av": "#d62728",
}


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_aggregate_csv(path: Path) -> dict:
    """Load a multi-seed aggregate CSV into a nested dict.

    Returns: agg[scenario][metric] = dict(mean, std, ci95_lo, ci95_hi, n,
             av_penetration, hdv_action_interval)
    """
    agg = defaultdict(dict)
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            scenario = row["scenario"]
            metric = row["metric"]
            agg[scenario][metric] = {
                "mean": float(row["mean"]),
                "std": float(row["std"]),
                "ci95_lo": float(row["ci95_lo"]),
                "ci95_hi": float(row["ci95_hi"]),
                "n": int(row["n"]),
                "av_penetration": float(row["av_penetration"]),
                "hdv_action_interval": float(row["hdv_action_interval"]),
            }
    return agg


def _err_pair(entry: dict) -> tuple:
    """Return (lower, upper) error bar magnitudes relative to the mean."""
    return (entry["mean"] - entry["ci95_lo"], entry["ci95_hi"] - entry["mean"])


def analytical_triangular_fd(tau, v_max, d=1.0, num_points=200):
    """Compute analytical triangular FD.

    Free-flow:   q = k * v_max
    Congested:   q = (1/tau) * (1 - k * d)
    Capacity:    q_max = v_max / (v_max * tau + d)
    Jam density: k_jam = 1/d
    """
    k_jam = 1.0 / d
    q_max = v_max / (v_max * tau + d)
    k_crit = q_max / v_max

    k_free = np.linspace(0, k_crit, num_points // 2)
    q_free = k_free * v_max

    k_cong = np.linspace(k_crit, k_jam, num_points // 2)
    q_cong = (1.0 / tau) * (1.0 - k_cong * d)

    return (
        np.concatenate([k_free, k_cong]),
        np.concatenate([q_free, q_cong]),
        k_crit,
        q_max,
    )


# ------------------------------------------------------------------
# Figure 1: Single-lane FD (Theoretical + NaSch + ODCA-DES)
# ------------------------------------------------------------------

def _load_sweep_fd(fname: str):
    """Load density sweep FD points from JSON."""
    data = load_json(SWEEP_DIR / fname)
    k, q, v = [], [], []
    for run in data["results"]:
        for p in run["fd_points"]:
            k.append(p["density_vpkm"])
            q.append(p["flow_vph"])
            v.append(p["speed_kmh"])
    return np.array(k), np.array(q), np.array(v)




# ------------------------------------------------------------------
# Figure 2: Multi-lane FD (Theoretical + ODCA-DES)
# ------------------------------------------------------------------

def fig_fd_multi_lane():
    """Multi-lane FD: Theoretical triangular and ODCA-DES (per-lane)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # --- Theoretical triangular FD (same per-lane theory) ---
    k_an, q_an, k_crit, q_max = analytical_triangular_fd(
        HDV_DRIVER.tau, HDV_VEHICLE.v_max,
    )
    k_an_km = k_an / CELL_LENGTH_M * 1000
    q_an_h = q_an * 3600
    for ax in (ax1, ax2):
        ax.plot(k_an_km, q_an_h, "k-", linewidth=1.8, label="Theoretical",
                zorder=4)

    # --- ODCA-DES multi-lane ---
    try:
        odca_k, odca_q, _ = _load_sweep_fd("sweep_4lane.json")
        for ax in (ax1, ax2):
            ax.scatter(odca_k, odca_q, s=12, alpha=0.5, c="#2ca02c",
                       marker="o", edgecolors="none",
                       label="ODCA-DES (4 lanes, per-lane)", zorder=3)
    except FileNotFoundError:
        print("  (sweep_4lane.json not found — run run_demand_sweep.py)")

    # --- Also overlay single-lane for comparison ---
    try:
        odca_k1, odca_q1, _ = _load_sweep_fd("sweep_1lane.json")
        for ax in (ax1, ax2):
            ax.scatter(odca_k1, odca_q1, s=10, alpha=0.3, c="#1f77b4",
                       marker="^", edgecolors="none",
                       label="ODCA-DES (1 lane)", zorder=2)
    except FileNotFoundError:
        pass

    # --- Formatting ---
    ax1.set_xlabel("Density (veh/km)")
    ax1.set_ylabel("Flow (veh/h/lane)")
    ax1.set_title("(a) Full range")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)

    q_max_h = q_max * 3600
    k_crit_km = k_crit / CELL_LENGTH_M * 1000
    ax2.set_xlabel("Density (veh/km)")
    ax2.set_title("(b) Near capacity")
    ax2.set_xlim(0, k_crit_km * 3)
    ax2.set_ylim(0, q_max_h * 1.3)
    ax2.axhline(q_max_h, color="gray", ls=":", lw=0.8, alpha=0.6)
    ax2.axvline(k_crit_km, color="gray", ls=":", lw=0.8, alpha=0.6)
    ax2.legend(fontsize=8, loc="upper right")

    fig.suptitle("Fundamental Diagram — Multi-Lane (per-lane)", fontsize=12,
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_fd_multi_lane.pdf")
    plt.close(fig)
    print("  -> fig_fd_multi_lane.pdf")


# ------------------------------------------------------------------
# Figure 4: Throughput bar chart (from run_experiments)
# ------------------------------------------------------------------

def fig_throughput_bar():
    """Throughput comparison bar chart across scenarios (multi-seed, 95% CI)."""
    if not MULTISEED_S1S4_CSV.exists():
        print(f"  (missing {MULTISEED_S1S4_CSV})")
        return
    agg = load_aggregate_csv(MULTISEED_S1S4_CSV)

    labels = []
    means = []
    err_lo = []
    err_hi = []
    colors = []
    n_seeds = None
    for scenario, display in SCENARIO_LABELS.items():
        if scenario not in agg or "throughput_per_hour" not in agg[scenario]:
            continue
        entry = agg[scenario]["throughput_per_hour"]
        labels.append(display)
        means.append(entry["mean"])
        lo, hi = _err_pair(entry)
        err_lo.append(lo)
        err_hi.append(hi)
        colors.append(SCENARIO_COLORS[scenario])
        n_seeds = entry["n"]

    if not labels:
        print("  (No data for throughput bar chart)")
        return

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(labels, means, color=colors,
                  edgecolor="black", linewidth=0.5,
                  yerr=[err_lo, err_hi], capsize=4,
                  error_kw={"elinewidth": 1.0, "ecolor": "black"})

    for bar, val, ehi in zip(bars, means, err_hi):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + ehi + 40,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Throughput (veh/h)")
    title = "Network Throughput by AV Penetration Rate"
    if n_seeds is not None:
        title += f"\n(mean $\\pm$ 95% CI, N={n_seeds})"
    ax.set_title(title)
    ax.set_ylim(bottom=0)

    fig.savefig(OUT_DIR / "fig_throughput_bar.pdf")
    plt.close(fig)
    print("  -> fig_throughput_bar.pdf")


# ------------------------------------------------------------------
# Figure 5: Travel time + delay (from run_experiments)
# ------------------------------------------------------------------

def fig_travel_time():
    """Travel time and delay grouped bar chart (multi-seed, 95% CI)."""
    if not MULTISEED_S1S4_CSV.exists():
        print(f"  (missing {MULTISEED_S1S4_CSV})")
        return
    agg = load_aggregate_csv(MULTISEED_S1S4_CSV)

    labels = []
    tt_mean, tt_lo, tt_hi = [], [], []
    delay_mean, delay_lo, delay_hi = [], [], []
    n_seeds = None
    for scenario, display in SCENARIO_LABELS.items():
        if scenario not in agg:
            continue
        if "avg_travel_time" not in agg[scenario] or "avg_delay" not in agg[scenario]:
            continue
        labels.append(display)
        e_tt = agg[scenario]["avg_travel_time"]
        e_d = agg[scenario]["avg_delay"]
        tt_mean.append(e_tt["mean"])
        lo, hi = _err_pair(e_tt)
        tt_lo.append(lo)
        tt_hi.append(hi)
        delay_mean.append(e_d["mean"])
        lo, hi = _err_pair(e_d)
        delay_lo.append(lo)
        delay_hi.append(hi)
        n_seeds = e_tt["n"]

    if not labels:
        print("  (No data for travel time chart)")
        return

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w / 2, tt_mean, w, label="Avg Travel Time (s)",
           color="#1f77b4", edgecolor="black", linewidth=0.5,
           yerr=[tt_lo, tt_hi], capsize=3,
           error_kw={"elinewidth": 1.0, "ecolor": "black"})
    ax.bar(x + w / 2, delay_mean, w, label="Avg Delay (s)",
           color="#ff7f0e", edgecolor="black", linewidth=0.5,
           yerr=[delay_lo, delay_hi], capsize=3,
           error_kw={"elinewidth": 1.0, "ecolor": "black"})

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Time (s)")
    title = "Travel Time and Delay by AV Penetration Rate"
    if n_seeds is not None:
        title += f"\n(mean $\\pm$ 95% CI, N={n_seeds})"
    ax.set_title(title)
    ax.legend()

    fig.savefig(OUT_DIR / "fig_travel_time.pdf")
    plt.close(fig)
    print("  -> fig_travel_time.pdf")


# ------------------------------------------------------------------
# Figure 6: Bottleneck throughput comparison
# ------------------------------------------------------------------

def fig_bottleneck_throughput():
    """Bar chart: throughput and delay at bottleneck across AV scenarios (multi-seed, 95% CI)."""
    if not MULTISEED_BN_CSV.exists():
        print(f"  (missing {MULTISEED_BN_CSV})")
        return
    agg = load_aggregate_csv(MULTISEED_BN_CSV)

    labels = []
    tp_mean, tp_lo, tp_hi = [], [], []
    d_mean, d_lo, d_hi = [], [], []
    colors = []
    n_seeds = None
    for scenario, display in BN_LABELS.items():
        if scenario not in agg:
            continue
        if "throughput_per_hour" not in agg[scenario] or "avg_delay" not in agg[scenario]:
            continue
        labels.append(display)
        e_tp = agg[scenario]["throughput_per_hour"]
        e_d = agg[scenario]["avg_delay"]
        tp_mean.append(e_tp["mean"])
        lo, hi = _err_pair(e_tp)
        tp_lo.append(lo); tp_hi.append(hi)
        d_mean.append(e_d["mean"])
        lo, hi = _err_pair(e_d)
        d_lo.append(lo); d_hi.append(hi)
        colors.append(BN_COLORS[scenario])
        n_seeds = e_tp["n"]

    if not labels:
        print("  (No bottleneck data)")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

    # Throughput
    bars1 = ax1.bar(labels, tp_mean, color=colors,
                    edgecolor="black", linewidth=0.5,
                    yerr=[tp_lo, tp_hi], capsize=4,
                    error_kw={"elinewidth": 1.0, "ecolor": "black"})
    for bar, val, ehi in zip(bars1, tp_mean, tp_hi):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + ehi + 40,
                 f"{val:.0f}", ha="center", va="bottom", fontsize=9)
    ax1.axhline(BN_DEMAND_VPH, ls="--", lw=1.0, color="black",
                label=f"offered demand ({BN_DEMAND_VPH:,.0f} veh/h)")
    ax1.legend(fontsize=7, loc="lower right")
    ax1.set_ylabel("Throughput (veh/h)")
    ax1.set_title("(a) Bottleneck Throughput")
    ax1.set_ylim(bottom=0)

    # Delay
    bars2 = ax2.bar(labels, d_mean, color=colors,
                    edgecolor="black", linewidth=0.5,
                    yerr=[d_lo, d_hi], capsize=4,
                    error_kw={"elinewidth": 1.0, "ecolor": "black"})
    for bar, val, ehi in zip(bars2, d_mean, d_hi):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + ehi + 8,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=9)
    ax2.set_ylabel("Average Delay (s)")
    ax2.set_title("(b) Bottleneck Delay")
    ax2.set_ylim(bottom=0)

    suptitle = "Bottleneck: Throughput and Delay by AV Penetration"
    if n_seeds is not None:
        suptitle += f" (mean $\\pm$ 95% CI, N={n_seeds})"
    fig.suptitle(suptitle, fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_bottleneck_throughput.pdf")
    plt.close(fig)
    print("  -> fig_bottleneck_throughput.pdf")


# ------------------------------------------------------------------
# Figure 7: Bottleneck FD (upstream vs downstream)
# ------------------------------------------------------------------

def fig_bottleneck_fd():
    """FD at upstream vs downstream of bottleneck, for 0% and 70% AV."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    for idx, (label, title) in enumerate([
        ("BN_0av", "0% AV"),
        ("BN_70av", "70% AV"),
    ]):
        ax = axes[idx]
        try:
            data = load_json(BN_DIR / f"{label}.json")
        except FileNotFoundError:
            ax.set_title(f"{title} (no data)")
            continue

        fd = data["fd_data"]

        for region, clr, lbl in [
            ("upstream", "#d62728", "Upstream"),
            ("downstream", "#2ca02c", "Downstream"),
        ]:
            if region not in fd:
                continue
            k_all = [p["density_vpkm"] for p in fd[region] if p["flow_vph"] > 0]
            q_all = [p["flow_vph"] for p in fd[region] if p["flow_vph"] > 0]
            if k_all:
                ax.scatter(k_all, q_all, s=14, alpha=0.6, c=clr, label=lbl)

        # Analytical reference
        k_an, q_an, _, _ = analytical_triangular_fd(
            HDV_DRIVER.tau, HDV_VEHICLE.v_max
        )
        ax.plot(k_an / CELL_LENGTH_M * 1000, q_an * 3600,
                "k--", linewidth=1, alpha=0.5, label="Analytical")

        ax.set_xlabel("Density (veh/km)")
        ax.set_title(title)
        ax.legend(fontsize=8)
        ax.set_xlim(0, 150)
        ax.set_ylim(0, 2500)

    axes[0].set_ylabel("Flow (veh/h/lane)")
    fig.suptitle("Fundamental Diagram: Upstream vs Downstream of Bottleneck",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_bottleneck_fd.pdf")
    plt.close(fig)
    print("  -> fig_bottleneck_fd.pdf")


# ------------------------------------------------------------------
# Figure 7: Incident — Lane-by-lane time-space trajectories
# ------------------------------------------------------------------

def _load_incident():
    """Load incident trajectory data."""
    return load_json(INC_DIR / "incident_trajectory.json")


def _load_baseline():
    """Load baseline (no-incident) trajectory data."""
    return load_json(INC_DIR / "baseline_trajectory.json")


def _extract_lane_trajs(data):
    """Extract per-lane trajectory segments from trajectory data."""
    cfg = data["config"]
    num_lanes = cfg["num_lanes"]
    cell_len = cfg["cell_length_m"]

    lane_trajs = {i: [] for i in range(num_lanes)}
    for traj in data["trajectories"]:
        pts = traj["trajectory"]
        if len(pts) < 2:
            continue
        times = np.array([p["t"] for p in pts])
        cells = np.array([p["cell"] for p in pts])
        lanes = np.array([p["lane"] for p in pts])
        speeds = np.array([p["speed"] for p in pts])
        positions = cells * cell_len / 1000

        lane_changes = np.where(lanes[:-1] != lanes[1:])[0]
        boundaries = np.concatenate([[0], lane_changes + 1, [len(pts)]])
        for b in range(len(boundaries) - 1):
            s, e = boundaries[b], boundaries[b + 1]
            if e - s < 2:
                continue
            li = int(lanes[s]) - 1
            if li >= num_lanes:
                continue
            avg_spd = float(np.mean(speeds[s:e])) * cell_len * 3.6
            lane_trajs[li].append((times[s:e], positions[s:e], avg_spd))
    return lane_trajs


def _compute_density(data, lane=None):
    """Compute density heatmap from trajectory data.

    Args:
        data: trajectory JSON data.
        lane: 1-based lane index to filter, or None for all lanes.

    Returns density_vpkm, t_edges, x_edges.
    """
    cfg = data["config"]
    cell_len = cfg["cell_length_m"]
    num_cells = cfg["num_cells"]
    sim_dur = cfg["sim_duration"]

    dt = 15.0
    dx = 10
    nt = int(sim_dur / dt)
    nx = int(num_cells / dx)

    W = np.zeros((nt, nx))
    for traj in data["trajectories"]:
        pts = traj["trajectory"]
        for k in range(len(pts) - 1):
            p0, p1 = pts[k], pts[k + 1]
            if lane is not None and p0["lane"] != lane:
                continue
            t0, t1 = p0["t"], p1["t"]
            c0 = p0["cell"]
            if t1 <= t0:
                continue
            xi = int(c0 / dx)
            if xi < 0 or xi >= nx:
                continue
            # split the time spent in the cell across every time bin it overlaps
            ti = max(int(t0 / dt), 0)
            while ti < nt and ti * dt < t1:
                overlap = min(t1, (ti + 1) * dt) - max(t0, ti * dt)
                if overlap > 0:
                    W[ti, xi] += overlap
                ti += 1

    A = dx * dt
    density_vpkm = (W / A) * 1000 / cell_len
    density_vpkm[W == 0] = np.nan

    t_edges = np.arange(nt + 1) * dt
    x_edges = np.arange(nx + 1) * dx * cell_len / 1000
    return density_vpkm, t_edges, x_edges


def _closure_lanes(cfg):
    """The lanes the incident closed, from the run's config block.

    Args:
        cfg: the `config` dict of an incident JSON.
    """
    return cfg.get("closure_lanes") or [cfg["closure_lane"]]


def fig_incident_trajectories():
    """Combined baseline vs incident lane-by-lane time-space trajectories (2 columns x 4 rows)."""
    data_bl = _load_baseline()
    data_inc = _load_incident()
    cfg = data_inc["config"]
    num_lanes = cfg["num_lanes"]
    cell_len = cfg["cell_length_m"]
    t_on = cfg["incident_on"]
    t_off = cfg["incident_off"]

    trajs_bl = _extract_lane_trajs(data_bl)
    trajs_inc = _extract_lane_trajs(data_inc)

    fig, ax_arr = plt.subplots(num_lanes, 2, figsize=(12, 12),
                               sharey=True, sharex=True,
                               layout="constrained")

    v_max_kmh = HDV_VEHICLE.v_max * cell_len * 3.6
    cmap = plt.cm.RdYlGn
    norm = plt.Normalize(0, v_max_kmh)
    warmup = cfg.get("warmup", 0)
    y_max = cfg["num_cells"] * cell_len / 1000

    lane_labels = ["Lane 1 (rightmost)", "Lane 2",
                   "Lane 3", f"Lane {num_lanes} (leftmost)"]

    for row in range(num_lanes):
        for col, (trajs, label) in enumerate([(trajs_bl, "Baseline"), (trajs_inc, "Incident")]):
            ax = ax_arr[row, col]
            for t_arr, x_arr, avg_spd in trajs[row]:
                color = cmap(norm(avg_spd))
                ax.plot(t_arr, x_arr, "-", color=color, linewidth=0.4, alpha=0.6)

            ax.set_xlim(warmup, cfg["sim_duration"])
            ax.set_ylim(0, y_max)

            if row == 0:
                ax.set_title(label, fontsize=11, fontweight="bold")

            # Incident markers on right column only
            if col == 1:
                ax.axvline(t_on, color="red", ls="--", lw=1.0, alpha=0.8)
                ax.axvline(t_off, color="blue", ls="--", lw=1.0, alpha=0.8)
                if (row + 1) in _closure_lanes(cfg):
                    y_lo = cfg["closure_start_cell"] * cell_len / 1000
                    y_hi = cfg["closure_end_cell"] * cell_len / 1000
                    ax.axhspan(y_lo, y_hi, xmin=t_on / cfg["sim_duration"],
                               xmax=t_off / cfg["sim_duration"],
                               color="red", alpha=0.2)

        # Lane label on left column
        ax_arr[row, 0].set_ylabel(f"{lane_labels[row]}\nPosition (km)", fontsize=9)

    ax_arr[-1, 0].set_xlabel("Time (s)")
    ax_arr[-1, 1].set_xlabel("Time (s)")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax_arr, location="right", shrink=0.8, pad=0.02,
                 label="Speed (km/h)")

    fig.savefig(OUT_DIR / "fig_incident_trajectories.pdf")
    plt.close(fig)
    print("  -> fig_incident_trajectories.pdf")


# ------------------------------------------------------------------
# Figure: Combined baseline vs incident density heatmap
# ------------------------------------------------------------------

def fig_incident_density_heatmap():
    """Lane-by-lane baseline vs incident density heatmaps (4 rows x 2 columns)."""
    data_bl = _load_baseline()
    data_inc = _load_incident()
    cfg = data_inc["config"]
    num_lanes = cfg["num_lanes"]
    cell_len = cfg["cell_length_m"]
    sim_dur = cfg["sim_duration"]
    t_on = cfg["incident_on"]
    t_off = cfg["incident_off"]
    warmup = cfg.get("warmup", 0)

    fig, ax_arr = plt.subplots(num_lanes, 2, figsize=(12, 12),
                               sharey=True, sharex=True,
                               layout="constrained")

    cmap_density = plt.cm.YlOrRd.copy()
    cmap_density.set_bad("white")

    lane_labels = ["Lane 1 (rightmost)", "Lane 2",
                   "Lane 3", f"Lane {num_lanes} (leftmost)"]

    for row in range(num_lanes):
        lane = row + 1  # 1-based
        density_bl, t_edges, x_edges = _compute_density(data_bl, lane=lane)
        density_inc, _, _ = _compute_density(data_inc, lane=lane)

        for col, (density, label) in enumerate([(density_bl, "Baseline"), (density_inc, "Incident")]):
            ax = ax_arr[row, col]
            im = ax.pcolormesh(t_edges, x_edges, density.T,
                               cmap=cmap_density, shading="flat",
                               vmin=0, vmax=120)
            ax.set_xlim(warmup, sim_dur)

            if row == 0:
                ax.set_title(label, fontsize=11, fontweight="bold")

            # Incident markers on right column only
            if col == 1:
                ax.axvline(t_on, color="white", ls="--", lw=1.0, alpha=0.9)
                ax.axvline(t_off, color="white", ls="--", lw=1.0, alpha=0.9)
                if (row + 1) in _closure_lanes(cfg):
                    y_lo = cfg["closure_start_cell"] * cell_len / 1000
                    y_hi = cfg["closure_end_cell"] * cell_len / 1000
                    ax.plot([t_on, t_on, t_off, t_off],
                            [y_lo, y_hi, y_hi, y_lo], "w-", lw=1.5, alpha=0.8)

        ax_arr[row, 0].set_ylabel(f"{lane_labels[row]}\nPosition (km)", fontsize=9)

    ax_arr[-1, 0].set_xlabel("Time (s)")
    ax_arr[-1, 1].set_xlabel("Time (s)")

    sm = plt.cm.ScalarMappable(cmap=cmap_density, norm=plt.Normalize(0, 120))
    sm.set_array([])
    fig.colorbar(sm, ax=ax_arr, location="right", shrink=0.8, pad=0.02,
                 label="Density (veh/km)")

    fig.savefig(OUT_DIR / "fig_incident_heatmap.pdf")
    plt.close(fig)
    print("  -> fig_incident_heatmap.pdf")



# ------------------------------------------------------------------
# Figure: Heterogeneous FD — Effect of AV Penetration (single panel)
# ------------------------------------------------------------------

def fig_fd_theoretical():
    """2x2 FD comparison: ODCA-DES (top) and NaSch (bottom), full range and near capacity."""
    from odca.baselines.nasch import NaSchConfig, sweep_density as nasch_sweep

    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
    (ax_odca_full, ax_odca_zoom) = axes[0]
    (ax_nasch_full, ax_nasch_zoom) = axes[1]

    # --- Theoretical triangular FD ---
    k_an, q_an, k_crit, q_max = analytical_triangular_fd(
        HDV_DRIVER.tau, HDV_VEHICLE.v_max,
    )
    k_an_km = k_an / CELL_LENGTH_M * 1000
    q_an_h = q_an * 3600
    q_max_h = q_max * 3600
    k_crit_km = k_crit / CELL_LENGTH_M * 1000

    for ax in axes.flat:
        ax.plot(k_an_km, q_an_h, "k-", linewidth=1.8, label="Theoretical",
                zorder=4)

    # --- ODCA-DES data ---
    try:
        odca_k, odca_q, _ = _load_sweep_fd("sweep_1lane.json")
        for ax in (ax_odca_full, ax_odca_zoom):
            ax.scatter(odca_k, odca_q, s=12, alpha=0.5, c="#1f77b4",
                       marker="o", edgecolors="none",
                       label=f"ODCA-DES ($v_{{\\max}}$={HDV_VEHICLE.v_max})",
                       zorder=3)
    except FileNotFoundError:
        print("  (sweep_1lane.json not found — run run_demand_sweep.py)")

    # --- NaSch data ---
    print("  Running NaSch density sweep (single lane)...")
    nasch_cfg = NaSchConfig(
        num_cells=800, v_max=5, slowdown_prob=0.3,
        num_steps=3000, warmup_steps=500, seed=ILLUSTRATIVE_SEED,
    )
    nasch_results = nasch_sweep(
        densities=[i / 100 for i in range(1, 85)],
        config=nasch_cfg,
    )
    nasch_k = [r["density"] * 1000 / CELL_LENGTH_M for r in nasch_results]
    nasch_q = [r["flow"] * 3600 for r in nasch_results]
    for ax in (ax_nasch_full, ax_nasch_zoom):
        ax.scatter(nasch_k, nasch_q, s=12, alpha=0.5, c="#ff7f0e",
                   marker="s", edgecolors="none",
                   label=f"NaSch ($v_{{\\max}}$=5, $p$=0.3)", zorder=2)

    # --- Formatting ---
    # Full range panels
    for ax, title in [(ax_odca_full, "(a) ODCA-DES — full range"),
                      (ax_nasch_full, "(c) NaSch — full range")]:
        ax.set_xlabel("Density (veh/km)")
        ax.set_ylabel("Flow (veh/h/lane)")
        ax.set_title(title)
        ax.legend(fontsize=8, loc="upper right")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)

    # Zoomed panels
    for ax, title in [(ax_odca_zoom, "(b) ODCA-DES — near capacity"),
                      (ax_nasch_zoom, "(d) NaSch — near capacity")]:
        ax.set_xlabel("Density (veh/km)")
        ax.set_title(title)
        ax.set_xlim(0, k_crit_km * 3)
        ax.set_ylim(0, q_max_h * 1.3)
        ax.axhline(q_max_h, color="gray", ls=":", lw=0.8, alpha=0.6)
        ax.axvline(k_crit_km, color="gray", ls=":", lw=0.8, alpha=0.6)
        ax.legend(fontsize=8, loc="upper right")

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_fd_theoretical.pdf")
    plt.close(fig)
    print("  -> fig_fd_theoretical.pdf")


# ------------------------------------------------------------------
# Figure: Lane-Change Logistic Probabilities (MLC + DLC combined)
# ------------------------------------------------------------------

def fig_lc_logistic():
    """Side-by-side: (a) MLC probability vs remaining distance, (b) DLC probability vs speed advantage."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # --- Panel (a): MLC ---
    k = HDV_DRIVER.lane_change.mlc_k        # 8.0
    r0 = HDV_DRIVER.lane_change.mlc_r0      # 0.3
    r = np.linspace(0, 1, 500)

    colors_mlc = {1: "#1f77b4", 2: "#ff7f0e", 3: "#d62728"}
    for n in [1, 2, 3]:
        r_n = n * r0
        p = 1.0 / (1.0 + np.exp(-k * (r_n - r)))
        ax1.plot(r, p, "-", color=colors_mlc[n], linewidth=1.8,
                 label=f"$n = {n}$ ($r_0^{{(n)}}$ = {r_n:.1f})")

    ax1.set_xlabel("Remaining distance ratio $r$")
    ax1.set_ylabel("$P_{\\mathrm{MLC}}(r)$")
    ax1.set_title("(a) Mandatory lane change")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.02, 1.05)
    ax1.legend(fontsize=8, loc="upper left")
    ax1.axhline(0.5, color="gray", ls="--", lw=0.7, alpha=0.5)
    ax1.annotate("approaching exit", xy=(0.15, 0.08), xytext=(0.65, 0.08),
                 xycoords="axes fraction", fontsize=8, style="italic",
                 ha="center", va="center",
                 arrowprops=dict(arrowstyle="->", color="black", lw=1.2))

    # --- Panel (b): DLC ---
    dv = np.linspace(-2, 4, 500)
    dv_kmh = dv * CELL_LENGTH_M * 3.6

    k_hdv = HDV_DRIVER.lane_change.dlc_k       # 3.0
    dv0_hdv = HDV_DRIVER.lane_change.dlc_v0    # 1.0
    p_hdv = 1.0 / (1.0 + np.exp(-k_hdv * (dv - dv0_hdv)))

    ax2.plot(dv_kmh, p_hdv, "-", color="#1f77b4", linewidth=1.8,
             label=f"HDV ($k_d$={k_hdv}, $\\Delta v_0$={dv0_hdv})")
    ax2.text(0.5, 0.85, "AV: DLC disabled\n(central control)",
             transform=ax2.transAxes, fontsize=8, ha="center",
             style="italic", color="#d62728")

    ax2.set_xlabel("Speed advantage $\\Delta v$ (km/h)")
    ax2.set_ylabel("$P_{\\mathrm{DLC}}(\\Delta v)$")
    ax2.set_title("(b) Discretionary lane change")
    ax2.set_xlim(dv_kmh[0], dv_kmh[-1])
    ax2.set_ylim(-0.02, 1.05)
    ax2.legend(fontsize=8, loc="lower right")
    ax2.axhline(0.5, color="gray", ls="--", lw=0.7, alpha=0.5)
    ax2.axvline(0, color="gray", ls=":", lw=0.7, alpha=0.5)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_lc_logistic.pdf")
    plt.close(fig)
    print("  -> fig_lc_logistic.pdf")


# ------------------------------------------------------------------
# Figure: Sensitivity to HDV action_interval (S1 only)
# ------------------------------------------------------------------

def fig_sensitivity_action_interval():
    """S1 metrics vs HDV action_interval {0.25, 0.5, 1.0}, 2x2 panels with 95% CI."""
    if not SENSITIVITY_CSV.exists():
        print(f"  (missing {SENSITIVITY_CSV})")
        return

    # Collect S1-only rows keyed by action_interval -> metric -> entry
    rows_by_ai = defaultdict(dict)
    with open(SENSITIVITY_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["scenario"] != "S1_baseline":
                continue
            ai = float(row["action_interval"])
            metric = row["metric"]
            rows_by_ai[ai][metric] = {
                "mean": float(row["mean"]),
                "std": float(row["std"]),
                "ci95_lo": float(row["ci95_lo"]),
                "ci95_hi": float(row["ci95_hi"]),
                "n": int(row["n"]),
            }

    ais = sorted(rows_by_ai.keys())
    if not ais:
        print("  (No S1 rows in sensitivity CSV)")
        return

    panels = [
        ("throughput_per_hour", "Throughput (veh/h)", "(a) Throughput"),
        ("avg_delay", "Avg Delay (s)", "(b) Average delay"),
        ("avg_travel_time", "Avg Travel Time (s)", "(c) Average travel time"),
        ("avg_lc_per_km", "Lane changes / km", "(d) Lane-change rate"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(9.5, 6.5))
    axes = axes.flatten()

    x = np.array(ais, dtype=float)

    for ax, (metric, ylabel, title) in zip(axes, panels):
        y, lo, hi = [], [], []
        for ai in ais:
            entry = rows_by_ai[ai].get(metric)
            if entry is None:
                y.append(np.nan); lo.append(0); hi.append(0)
                continue
            y.append(entry["mean"])
            lo.append(entry["mean"] - entry["ci95_lo"])
            hi.append(entry["ci95_hi"] - entry["mean"])
        y = np.array(y, dtype=float)
        lo = np.array(lo, dtype=float)
        hi = np.array(hi, dtype=float)

        ax.errorbar(x, y, yerr=[lo, hi], fmt="o-", color="#1f77b4",
                    ecolor="black", capsize=4, linewidth=1.6,
                    markersize=6, markerfacecolor="#1f77b4",
                    markeredgecolor="black")
        ax.set_xlabel("HDV action interval (s)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.grid(True, alpha=0.3)
        # annotate each point
        for xi, yi in zip(x, y):
            if not np.isnan(yi):
                ax.annotate(f"{yi:.1f}" if yi < 100 else f"{yi:.0f}",
                            xy=(xi, yi), xytext=(5, 5),
                            textcoords="offset points", fontsize=8)

    # N annotation: 10 for ai=0.25, 10 for ai=0.5, 20 for ai=1.0
    n_info = ", ".join(
        f"N={rows_by_ai[ai]['throughput_per_hour']['n']} at ai={ai}"
        for ai in ais if "throughput_per_hour" in rows_by_ai[ai]
    )
    fig.suptitle(
        f"Sensitivity to HDV action interval (Scenario S1, 0% AV; mean $\\pm$ 95% CI; {n_info})",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_sensitivity_action_interval.pdf")
    plt.close(fig)
    print("  -> fig_sensitivity_action_interval.pdf")


# ------------------------------------------------------------------
# Figure: Computational scalability
# ------------------------------------------------------------------

def fig_scalability():
    """Wall-clock vs total cells (log-log), with the SimPy event count overlaid as 2nd panel."""
    if not SCALABILITY_CSV.exists():
        print(f"  (missing {SCALABILITY_CSV})")
        return

    # Aggregate by total_cells: list wall-clock, events
    by_cells = defaultdict(lambda: {"wall": [], "events": [], "rt_ratio": []})
    with open(SCALABILITY_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            tc = int(row["total_cells"])
            by_cells[tc]["wall"].append(float(row["wall_clock_seconds"]))
            by_cells[tc]["events"].append(float(row["simpy_events"]))
            by_cells[tc]["rt_ratio"].append(float(row["realtime_ratio"]))

    cells_sorted = sorted(by_cells.keys())
    wall_mean = np.array([np.mean(by_cells[c]["wall"]) for c in cells_sorted])
    wall_min = np.array([np.min(by_cells[c]["wall"]) for c in cells_sorted])
    wall_max = np.array([np.max(by_cells[c]["wall"]) for c in cells_sorted])
    ev_mean = np.array([np.mean(by_cells[c]["events"]) for c in cells_sorted])
    ev_min = np.array([np.min(by_cells[c]["events"]) for c in cells_sorted])
    ev_max = np.array([np.max(by_cells[c]["events"]) for c in cells_sorted])
    n_seeds = len(by_cells[cells_sorted[0]]["wall"])
    cells = np.array(cells_sorted, dtype=float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # --- Panel (a): wall-clock vs cells (log-log) ---
    # Error bars use min/max (N=3 is too few for meaningful CI).
    ax1.errorbar(
        cells, wall_mean,
        yerr=[wall_mean - wall_min, wall_max - wall_mean],
        fmt="o-", color="#1f77b4", ecolor="black", capsize=4,
        linewidth=1.6, markersize=7, markerfacecolor="#1f77b4",
        markeredgecolor="black", label="Measured (mean, min/max)",
    )

    # Reference slopes anchored at first point
    x_ref = cells
    c0 = cells[0]; w0 = wall_mean[0]
    ax1.plot(x_ref, w0 * (x_ref / c0), "k--", lw=1.0, alpha=0.5,
             label="Linear $O(N)$")
    ax1.plot(x_ref, w0 * (x_ref / c0) ** 2, "k:", lw=1.0, alpha=0.5,
             label="Quadratic $O(N^2)$")

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("Total cells ($N_\\mathrm{lanes} \\times N_\\mathrm{cells}$)")
    ax1.set_ylabel("Wall-clock time (s)")
    ax1.set_title("(a) Runtime vs network size")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=8, loc="upper left")
    ax1.set_xticks(cells)
    ax1.set_xticklabels([f"{int(c)}" for c in cells])

    # --- Panel (b): event count vs cells (log-log) ---
    ax2.errorbar(
        cells, ev_mean,
        yerr=[ev_mean - ev_min, ev_max - ev_mean],
        fmt="s-", color="#d62728", ecolor="black", capsize=4,
        linewidth=1.6, markersize=7, markerfacecolor="#d62728",
        markeredgecolor="black", label="SimPy events",
    )
    # Linear reference
    e0 = ev_mean[0]
    ax2.plot(x_ref, e0 * (x_ref / c0), "k--", lw=1.0, alpha=0.5,
             label="Linear $O(N)$")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("Total cells")
    ax2.set_ylabel("SimPy events")
    ax2.set_title("(b) Event count vs network size")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.set_xticks(cells)
    ax2.set_xticklabels([f"{int(c)}" for c in cells])

    fig.suptitle(
        f"Computational scalability (S1, 4 lanes, 1800\\,s sim; {n_seeds} seeds per size)",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_scalability.pdf")
    plt.close(fig)
    print("  -> fig_scalability.pdf")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating figures...")

    # Theoretical FD: 2x2 ODCA-DES vs NaSch comparison
    try:
        fig_fd_theoretical()
    except FileNotFoundError as e:
        print(f"  Skipping theoretical FD: {e}")
        print("  Run 'python run_demand_sweep.py' first.")

    # Multi-lane FD
    try:
        fig_fd_multi_lane()
    except FileNotFoundError as e:
        print(f"  Skipping multi-lane FD: {e}")
        print("  Run 'python run_demand_sweep.py --lanes 4' first.")

    # Lane-change logistic probability plots (analytical)
    fig_lc_logistic()

    # Scenario figures (from run_experiments)
    try:
        fig_throughput_bar()
        fig_travel_time()
    except FileNotFoundError as e:
        print(f"  Skipping scenario figures: {e}")
        print("  Run 'python run_experiments.py' first.")

    # Bottleneck figures
    try:
        fig_bottleneck_throughput()
        fig_bottleneck_fd()
    except FileNotFoundError as e:
        print(f"  Skipping bottleneck figures: {e}")
        print("  Run 'python run_bottleneck.py' first.")

    # Incident figures (baseline vs incident combined)
    try:
        fig_incident_trajectories()
        fig_incident_density_heatmap()
    except FileNotFoundError as e:
        print(f"  Skipping incident figures: {e}")
        print("  Run 'python run_incident.py' first.")

    # Sensitivity to HDV action_interval (new, multi-seed)
    try:
        fig_sensitivity_action_interval()
    except FileNotFoundError as e:
        print(f"  Skipping sensitivity figure: {e}")

    # Scalability benchmark (new)
    try:
        fig_scalability()
    except FileNotFoundError as e:
        print(f"  Skipping scalability figure: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
