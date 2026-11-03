"""The worked example of Section 4.3: vehicles A, B and C under NaSch and under ODCA-DES.

Three vehicles on a ten-cell single-lane road, cells 1 to 10, leaving the road after cell 10.
At t = 0: A in cell 8 at 2 cells/s, B in cell 5 at 3 cells/s, C in cell 1 at 3 cells/s; tau = 1 s,
one cell per cell length. Both models are computed here from the rules the paper states, by hand
rather than through the simulator, so every number of the two example tables can be read off:

  NaSch     synchronous update at dt = 1 s, v_max = 3, no random slowdown: accelerate by one,
            slow to the number of empty cells ahead of the leader's previous-step position, move.
  ODCA-DES  the protocol of Section 3.4: request the next cell on arrival, seize it once the
            vehicle ahead releases it, cross it in 1/v seconds (waiting at the boundary until the
            vehicle ahead has left it), release the previous cell tau after the next one is seized.
            A vehicle in the last cell leaves the road on arrival and keeps that cell locked for tau,
            exactly as if it had seized a cell 11.

Prints both tables and writes `figures/fig_example_trajectories.pdf`.

Usage:
    uv run --no-project --with matplotlib python plot_example_trajectories.py
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

ROAD_END = 10            # last cell; a vehicle beyond it has left the road
TAU = 1.0                # s
NASCH_V_MAX = 3          # cells per step
NASCH_STEPS = 4
START: Dict[str, Tuple[int, float]] = {"A": (8, 2.0), "B": (5, 3.0), "C": (1, 3.0)}
ORDER = ("A", "B", "C")  # front to back
COLOURS = {"A": "#1f77b4", "B": "#d62728", "C": "#2ca02c"}


def nasch() -> List[Dict[str, Optional[Tuple[int, int]]]]:
    """NaSch states at t = 0, 1, ...: per vehicle (cell, speed), or None once it has left."""
    state: Dict[str, Optional[Tuple[int, int]]] = {k: (c, int(v)) for k, (c, v) in START.items()}
    states = [dict(state)]
    for _ in range(NASCH_STEPS):
        new: Dict[str, Optional[Tuple[int, int]]] = {}
        for i, name in enumerate(ORDER):
            if state[name] is None:
                new[name] = None
                continue
            cell, v = state[name]
            v = min(v + 1, NASCH_V_MAX)
            leader = next((state[o] for o in ORDER[:i] if state[o] is not None), None)
            if leader is not None:
                v = min(v, leader[0] - cell - 1)   # empty cells ahead, seen at the last step
            cell += v
            new[name] = None if cell > ROAD_END else (cell, v)
        state = new
        states.append(dict(state))
    return states


@dataclass
class OdcaVehicle:
    """One vehicle's protocol times: T_acq, T_arr and T_rel per cell."""

    name: str
    speed: float
    acquired: Dict[int, float] = field(default_factory=dict)
    arrived: Dict[int, float] = field(default_factory=dict)
    released: Dict[int, float] = field(default_factory=dict)


def odca() -> Dict[str, OdcaVehicle]:
    """ODCA-DES protocol times, front vehicle first, since each depends only on the one ahead."""
    out: Dict[str, OdcaVehicle] = {}
    ahead: Optional[OdcaVehicle] = None
    for name in ORDER:
        cell, speed = START[name]
        veh = OdcaVehicle(name, speed)
        veh.acquired[cell] = 0.0
        veh.arrived[cell] = 0.0
        while cell < ROAD_END:
            request = veh.arrived[cell]
            free_at = ahead.released.get(cell + 1, 0.0) if ahead else 0.0
            veh.acquired[cell + 1] = max(request, free_at)
            veh.released[cell] = veh.acquired[cell + 1] + TAU
            left_at = ahead.arrived.get(cell + 2, 0.0) if ahead else 0.0
            if ahead and cell + 1 == ROAD_END:
                left_at = ahead.arrived[ROAD_END]   # the vehicle ahead leaves on arrival
            veh.arrived[cell + 1] = max(veh.acquired[cell + 1] + 1.0 / speed, left_at)
            cell += 1
        veh.released[ROAD_END] = veh.arrived[ROAD_END] + TAU   # leaves, keeps the lock tau
        out[name] = veh
        ahead = veh
    return out


def print_tables(states, vehicles: Dict[str, OdcaVehicle]):
    """Both tables as the manuscript prints them."""
    print("NaSch (t: cell, v per vehicle)")
    for t, s in enumerate(states):
        cells = [f"{s[n][0]:>2} v={s[n][1]}" if s[n] else "  left " for n in ORDER]
        print(f"  t={t}: " + "   ".join(f"{n} {c}" for n, c in zip(ORDER, cells)))
    print("ODCA-DES events (time, vehicle, event, cell)")
    events = []
    for v in vehicles.values():
        start = START[v.name][0]
        for c, t in v.acquired.items():
            if c != start:
                events.append((t, v.name, "seize", c))
        for c, t in v.arrived.items():
            if c != start:
                events.append((t, v.name, "arrive", c))
        for c, t in v.released.items():
            events.append((t, v.name, "release", c))
    for t, name, kind, c in sorted(events, key=lambda e: (round(e[0], 6), e[1])):
        print(f"  {t:6.3f}  {name}  {kind:<7} {c}")


def plot(states, vehicles: Dict[str, OdcaVehicle]):
    """Two panels side by side: NaSch positions at whole seconds, ODCA-DES cell entries."""
    fig, (ax_n, ax_o) = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for name in ORDER:
        pts = [(t, s[name][0]) for t, s in enumerate(states) if s[name] is not None]
        ts, cs = zip(*pts)
        ax_n.step(ts, cs, where="post", color=COLOURS[name], lw=1.2)
        ax_n.plot(ts, cs, "o", color=COLOURS[name], ms=4, label=name)
        veh = vehicles[name]
        cells = sorted(veh.arrived)
        ts = [veh.arrived[c] for c in cells]
        ax_o.step(ts, cells, where="post", color=COLOURS[name], lw=1.2)
        ax_o.plot(ts, cells, "o", color=COLOURS[name], ms=4, label=name)
        waits = [(c, veh.acquired[c], veh.arrived[c - 1]) for c in cells[1:]
                 if veh.acquired[c] > veh.arrived[c - 1] + 1e-9]
        for c, t_acq, t_req in waits:
            ax_o.plot([t_req, t_acq], [c - 1, c - 1], color=COLOURS[name], lw=3.0, alpha=0.35)
    for ax, title in ((ax_n, "(a) NaSch, $\\Delta t = 1$ s"), (ax_o, "(b) ODCA-DES")):
        ax.set_xlim(-0.1, 3.6)
        ax.set_ylim(0.5, ROAD_END + 0.5)
        ax.set_yticks(range(1, ROAD_END + 1))
        ax.set_xlabel("time (s)")
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.3, lw=0.5)
    ax_n.set_ylabel("cell")
    ax_n.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "fig_example_trajectories.pdf")


def main():
    """Compute both models, print the tables, write the figure."""
    states = nasch()
    vehicles = odca()
    print_tables(states, vehicles)
    plot(states, vehicles)


if __name__ == "__main__":
    main()
