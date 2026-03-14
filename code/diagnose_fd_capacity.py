"""Diagnose FD capacity gap using a ring road (periodic boundary).

Vehicles wrap around from last cell to first — density is perfectly
conserved. Runs four configurations:
  1. Deterministic: no slowdowns, no heterogeneity
  2. Slowdowns only: slowdown_prob=0.15
  3. Heterogeneity only: heterogeneous tau/action_interval
  4. Full stochastic: all sources active

Usage:
    python diagnose_fd_capacity.py
"""

import logging
import time
from dataclasses import replace as dc_replace
from pathlib import Path

import numpy as np
import simpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import VehicleParams, CELL_LENGTH_M, HDV_PARAMS
from odca.infrastructure.freeway import Freeway
from odca.entity.vehicle import Vehicle, VehicleType
from odca.entity.hdv import HDV
from odca.rng import RNGRegistry
from odca.analysis.metrics import edie_fd_points

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

NUM_CELLS = 400
FD_INTERVAL = 20.0

# Fine density grid up to near-jam
DENSITIES = [
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10,
    0.12, 0.14, 0.16, 0.18, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
    0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95,
]

DURATION = 600.0
WARMUP = 100.0

# Diagnostic configurations
CONFIGS = {
    "Deterministic": dc_replace(
        HDV_PARAMS,
        slowdown_prob=0.0, slowdown_prob_std=0.0,
        tau_std=0.0, action_interval_std=0.0,
    ),
    "Slowdowns only": dc_replace(
        HDV_PARAMS,
        tau_std=0.0, action_interval_std=0.0,
        slowdown_prob_std=0.0,
    ),
    "Heterogeneity only": dc_replace(
        HDV_PARAMS,
        slowdown_prob=0.0, slowdown_prob_std=0.0,
    ),
    "Full stochastic": HDV_PARAMS,
}


def _make_ring_road(env, num_cells, speed_limit):
    """Create a single-lane ring road (periodic boundary)."""
    freeway = Freeway(
        env=env, num_lanes=1, num_cells=num_cells,
        speed_limit=speed_limit, onramp_cells=[], offramp_cells=[],
    )
    lane = freeway.lane(1)
    # Wire periodic boundary: last → first, first ← last
    lane.cells[-1]._next = lane.cells[0]
    lane.cells[0]._prev = lane.cells[-1]
    return freeway, lane


def _sample_params(params, rng_tau, rng_ai, rng_sp):
    overrides = {}
    if params.tau_std > 0:
        mean, std = params.tau, params.tau_std
        sigma2 = np.log(1 + (std / mean) ** 2)
        mu = np.log(mean) - sigma2 / 2
        overrides["tau"] = float(np.clip(
            rng_tau.lognormal(mu, np.sqrt(sigma2)), 0.5, 3.0))
    if params.action_interval_std > 0:
        mean, std = params.action_interval, params.action_interval_std
        sigma2 = np.log(1 + (std / mean) ** 2)
        mu = np.log(mean) - sigma2 / 2
        overrides["action_interval"] = float(np.clip(
            rng_ai.lognormal(mu, np.sqrt(sigma2)), 0.3, 3.0))
    if params.slowdown_prob_std > 0:
        val = rng_sp.normal(params.slowdown_prob, params.slowdown_prob_std)
        overrides["slowdown_prob"] = float(np.clip(val, 0.0, 1.0))
    return dc_replace(params, **overrides) if overrides else params


def run_ring(density, params):
    """Run ring road at given density, return FD points."""
    rng_reg = RNGRegistry(master_seed=42)
    rng_slowdown = rng_reg.spawn("slowdown")
    rng_mlc = rng_reg.spawn("mlc")
    rng_dlc = rng_reg.spawn("dlc")
    rng_tau = rng_reg.spawn("tau")
    rng_ai = rng_reg.spawn("ai")
    rng_sp = rng_reg.spawn("sp")
    Vehicle._id_counter = 0

    env = simpy.Environment()
    freeway, lane = _make_ring_road(env, NUM_CELLS, params.v_max)

    num_veh = max(1, int(NUM_CELLS * density))
    spacing = NUM_CELLS / num_veh

    vehicles = []
    for i in range(num_veh):
        ci = int(i * spacing) % NUM_CELLS
        dp = _sample_params(params, rng_tau, rng_ai, rng_sp)
        # destination_cell_idx=None → vehicle never exits, loops forever
        veh = HDV(env=env, rng_slowdown=rng_slowdown, rng_mlc=rng_mlc,
                  rng_dlc=rng_dlc, params=dp,
                  origin_cell=lane.cells[ci],
                  destination_cell_idx=None, destination_lane=1)
        vehicles.append(veh)
        env.process(veh.start())

    env.run(until=DURATION)

    # Edie's definitions from trajectory data
    region_lo, region_hi = 100, 300
    pts = edie_fd_points(vehicles, region_lo, region_hi,
                         WARMUP, DURATION, FD_INTERVAL)
    return [
        {"k_vpkm": p["density_vpkm"], "q_vph": p["flow_vph"],
         "v_kmh": p["speed_kmh"]}
        for p in pts
    ]


def analytical_fd(tau, v_max, d=1.0, n=200):
    k_jam = 1.0 / d
    q_max = v_max / (v_max * tau + d)
    k_c = q_max / v_max
    k_f = np.linspace(0, k_c, n // 2)
    q_f = k_f * v_max
    k_cg = np.linspace(k_c, k_jam, n // 2)
    q_cg = (1.0 / tau) * (1.0 - k_cg * d)
    k = np.concatenate([k_f, k_cg])
    q = np.concatenate([q_f, q_cg])
    return k, q, q_max, k_c


def main():
    out_dir = Path("output/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    colors = {
        "Deterministic": "#2ca02c",
        "Slowdowns only": "#ff7f0e",
        "Heterogeneity only": "#9467bd",
        "Full stochastic": "#1f77b4",
    }
    markers = {
        "Deterministic": "o",
        "Slowdowns only": "s",
        "Heterogeneity only": "^",
        "Full stochastic": "D",
    }

    # Collect all results
    all_results = {}
    for name, params in CONFIGS.items():
        print(f"\n=== {name} ===")
        all_pts = []
        t0 = time.time()
        for density in DENSITIES:
            print(f"  k={density:.2f}", end="", flush=True)
            pts = run_ring(density, params)
            all_pts.extend(pts)
            print(f"  ({len(pts)} pts)")
        wall = time.time() - t0
        print(f"  Wall time: {wall:.1f}s, total FD points: {len(all_pts)}")
        all_results[name] = all_pts

    # Theoretical reference
    k_an, q_an, q_max, k_c = analytical_fd(HDV_PARAMS.tau, HDV_PARAMS.v_max)
    k_an_km = k_an / CELL_LENGTH_M * 1000
    q_an_h = q_an * 3600
    q_max_h = q_max * 3600
    k_jam_km = 1.0 / HDV_PARAMS.standstill_spacing * 1000 / CELL_LENGTH_M

    # --- Figure 1: All four on one plot ---
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(k_an_km, q_an_h, "k-", linewidth=2, label="Theoretical", zorder=10)
    ax.axhline(q_max_h, color="gray", ls=":", lw=0.8, alpha=0.5)

    for name, pts in all_results.items():
        if pts:
            k = [p["k_vpkm"] for p in pts]
            q = [p["q_vph"] for p in pts]
            max_q = max(q)
            ax.scatter(k, q, s=10, alpha=0.4, c=colors[name],
                       marker=markers[name], edgecolors="none",
                       label=f"{name} (max={max_q:.0f})", zorder=3)

    ax.set_xlabel("Density (veh/km)")
    ax.set_ylabel("Flow (veh/h)")
    ax.set_title("FD Capacity Diagnosis — Ring Road (periodic boundary)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_xlim(0, k_jam_km * 1.05)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_fd_diagnosis.pdf")
    plt.close(fig)
    print(f"\nSaved {out_dir / 'fig_fd_diagnosis.pdf'}")

    # --- Figure 2: 3-panel side-by-side ---
    panel_configs = [
        ("Deterministic", "Deterministic"),
        ("Slowdowns only", "+ Stochastic slowdowns"),
        ("Full stochastic", "+ All stochastic components"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)

    for ax_i, (name, title) in enumerate(panel_configs):
        ax = axes[ax_i]
        ax.plot(k_an_km, q_an_h, "k-", linewidth=1.8, label="Theoretical", zorder=10)
        ax.axhline(q_max_h, color="gray", ls=":", lw=0.8, alpha=0.5)

        pts = all_results[name]
        if pts:
            k = [p["k_vpkm"] for p in pts]
            q = [p["q_vph"] for p in pts]
            max_q = max(q)
            ax.scatter(k, q, s=12, alpha=0.5, c=colors[name],
                       marker=markers[name], edgecolors="none",
                       label=f"ODCA-DES (max={max_q:.0f})", zorder=3)

        panel_letter = chr(ord('a') + ax_i)
        ax.set_title(f"({panel_letter}) {title}", fontsize=10)
        ax.set_xlabel("Density (veh/km)")
        ax.set_xlim(0, k_jam_km * 1.05)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.2)

    axes[0].set_ylabel("Flow (veh/h)")
    fig.suptitle("Effect of Stochastic Components on Fundamental Diagram",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_dir / "fig_fd_diagnosis_panels.pdf")
    plt.close(fig)
    print(f"Saved {out_dir / 'fig_fd_diagnosis_panels.pdf'}")


if __name__ == "__main__":
    main()
