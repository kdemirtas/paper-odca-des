"""Two-vehicle car-following visualization.

Places a leader and follower on a single-lane segment. The leader follows
a scripted speed profile; the follower uses the ODCA-DES driver process
(Newell car-following). Two scenarios:
  1. Moderate deceleration (v_max → ~40 km/h → v_max)
  2. Hard braking (v_max → near-zero → v_max)

Usage:
    python plot_car_following.py
"""

import numpy as np
import simpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dataclasses import replace

from config import CELL_LENGTH_M, FIGURES_DIR, HDV_DRIVER, HDV_VEHICLE, ILLUSTRATIVE_SEED
from odca.infrastructure.freeway import Freeway
from odca.params import NetworkConfig
from odca.entity.driver import DriverStreams, DriverTraits, HumanDriver
from odca.entity.vehicle import Direction, Vehicle
from odca.rng import RNGRegistry

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

NUM_CELLS = 600

# Scenario definitions: (profile, duration, decel_rate, title_suffix, filename)
SCENARIOS = {
    "moderate": {
        "profile": [
            (15.0, HDV_VEHICLE.v_max),
            (28.0, 1.5),               # ~40 km/h
            (42.0, 1.5),
            (55.0, HDV_VEHICLE.v_max),
            (999.0, HDV_VEHICLE.v_max),
        ],
        "duration": 100.0,
        "decel_rate": 0.8,
        "accel_rate": 0.8,
        "shade_spans": [(15, 28, "red"), (28, 42, "orange"), (42, 55, "green")],
        "title": "Moderate Deceleration",
        "filename": "fig_car_following.pdf",
    },
    "hard_brake": {
        "profile": [
            (12.0, HDV_VEHICLE.v_max),
            (22.0, 0.2),               # near-zero (~5 km/h)
            (35.0, 0.2),
            (50.0, HDV_VEHICLE.v_max),
            (999.0, HDV_VEHICLE.v_max),
        ],
        "duration": 110.0,
        "decel_rate": 1.0,
        "accel_rate": 0.8,
        "shade_spans": [(12, 22, "red"), (22, 35, "orange"), (35, 50, "green")],
        "title": "Hard Braking (near-zero)",
        "filename": "fig_car_following_hard_brake.pdf",
    },
}


class ScriptedLeader(HumanDriver):
    """A driver following a scripted speed profile (no car following), always forward."""

    def __init__(self, cfg, streams, profile, rates):
        """A scripted driver.

        Args:
            cfg: the driver config (its action interval paces the ramps).
            streams: the decision streams.
            profile: (until time, target speed) steps.
            rates: (deceleration, acceleration) in cells/s per decision.
        """
        super().__init__(cfg, streams, DriverTraits.exact(cfg))
        self._profile = profile
        self._decel_rate, self._accel_rate = rates

    def evaluate_speed(self):
        """Ramp toward the profile's speed at the scripted rates."""
        vehicle = self.vehicle
        t = self.env.now
        target_speed = HDV_VEHICLE.v_max
        for until, spd in self._profile:
            if t < until:
                target_speed = spd
                break

        speed = vehicle.speed
        delta = target_speed - speed
        if delta > 0:
            speed = min(target_speed, speed + self._accel_rate * self.action_interval)
        elif delta < 0:
            speed = max(target_speed, speed - self._decel_rate * self.action_interval)
        vehicle.set_target_speed(max(0.1, min(speed, vehicle.cfg.v_max)))

    def evaluate_direction(self):
        """Always forward."""
        self.vehicle.request_direction(Direction.FORWARD)


def run_scenario(scenario_cfg):
    rng_registry = RNGRegistry(master_seed=ILLUSTRATIVE_SEED)
    streams = DriverStreams.spawn(rng_registry)
    Vehicle._id_counter = 0

    env = simpy.Environment()
    freeway = Freeway(env, NetworkConfig.corridor(1, NUM_CELLS, HDV_VEHICLE.v_max))
    lane = freeway.lane(1)
    end = freeway.destination("end_lane_1")

    # no random slowdowns and a fixed 0.5 s decision interval, to show pure car following
    driver_cfg = replace(HDV_DRIVER, slowdown_prob=0.0, slowdown_delta=0.0, action_interval=0.5)
    follower = Vehicle(env, HDV_VEHICLE,
                       HumanDriver(driver_cfg, streams, DriverTraits.exact(driver_cfg)),
                       lane.cells[10], end)
    leader_driver = ScriptedLeader(driver_cfg, streams, scenario_cfg["profile"],
                                   (scenario_cfg["decel_rate"], scenario_cfg["accel_rate"]))
    leader = Vehicle(env, HDV_VEHICLE, leader_driver, lane.cells[18], end)

    env.process(leader.start())
    env.process(follower.start())
    env.run(until=scenario_cfg["duration"])

    return leader, follower


def plot_scenario(leader, follower, scenario_cfg):
    def extract(veh):
        t = [r.time for r in veh.trajectory]
        x = [r.cell_idx for r in veh.trajectory]
        v = [r.speed for r in veh.trajectory]
        return np.array(t), np.array(x), np.array(v)

    t_l, x_l, v_l = extract(leader)
    t_f, x_f, v_f = extract(follower)

    x_l_m = x_l * CELL_LENGTH_M
    x_f_m = x_f * CELL_LENGTH_M
    v_l_kmh = v_l * CELL_LENGTH_M * 3.6
    v_f_kmh = v_f * CELL_LENGTH_M * 3.6

    # Spacing via interpolation
    x_l_interp = np.interp(t_f, t_l, x_l)
    spacing = x_l_interp - x_f
    spacing_m = spacing * CELL_LENGTH_M

    # Desired spacing
    v_l_at_f = np.interp(t_f, t_l, v_l)
    s_star = HDV_VEHICLE.standstill_spacing + v_l_at_f * HDV_DRIVER.tau
    s_star_m = s_star * CELL_LENGTH_M

    shade_labels = ["Leader decelerating", "Leader crawling", "Leader accelerating"]
    spans = scenario_cfg["shade_spans"]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

    # Panel 1: Time-space trajectories
    ax1.plot(t_l, x_l_m, "r-", linewidth=1.5, label="Leader")
    ax1.plot(t_f, x_f_m, "b-", linewidth=1.5, label="Follower")
    for (t0, t1, clr), lbl in zip(spans, shade_labels):
        ax1.axvspan(t0, t1, alpha=0.08, color=clr, label=lbl)
    ax1.set_ylabel("Position (m)")
    ax1.set_title("(a) Time-Space Trajectory")
    ax1.legend(fontsize=8, loc="upper left", ncol=2)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Speed profiles
    ax2.plot(t_l, v_l_kmh, "r-", linewidth=1.5, label="Leader")
    ax2.plot(t_f, v_f_kmh, "b-", linewidth=1.5, label="Follower")
    for t0, t1, clr in spans:
        ax2.axvspan(t0, t1, alpha=0.08, color=clr)
    ax2.set_ylabel("Speed (km/h)")
    ax2.set_title("(b) Speed Profile")
    ax2.legend(fontsize=8, loc="upper right")
    ax2.set_ylim(bottom=0)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Spacing
    ax3.plot(t_f, spacing_m, "k-", linewidth=1.5, label="Actual spacing")
    ax3.plot(t_f, s_star_m, "k--", linewidth=1.0, alpha=0.6,
             label=r"Desired $s^* = d + v_L \cdot \tau$")
    for t0, t1, clr in spans:
        ax3.axvspan(t0, t1, alpha=0.08, color=clr)
    ax3.set_ylabel("Spacing (m)")
    ax3.set_xlabel("Time (s)")
    ax3.set_title("(c) Spacing (leader-follower gap)")
    ax3.legend(fontsize=8, loc="upper right")
    ax3.set_ylim(bottom=0)
    ax3.grid(True, alpha=0.3)

    fig.suptitle(
        f"Car-Following: {scenario_cfg['title']} "
        rf"(Newell, $\tau$={HDV_DRIVER.tau}s, $d$={HDV_VEHICLE.standstill_spacing})",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout()

    out = FIGURES_DIR / scenario_cfg["filename"]
    fig.savefig(out)
    plt.close(fig)
    print(f"  Saved {out}")


if __name__ == "__main__":
    for name, cfg in SCENARIOS.items():
        print(f"\n=== Scenario: {name} ===")
        leader, follower = run_scenario(cfg)
        print(f"  Leader: {len(leader.trajectory)} pts, "
              f"exited={leader.time_exited is not None}")
        print(f"  Follower: {len(follower.trajectory)} pts, "
              f"exited={follower.time_exited is not None}, "
              f"CF evals={follower.driver.count_cf_evaluations}")
        plot_scenario(leader, follower, cfg)
