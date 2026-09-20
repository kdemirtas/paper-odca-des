"""Queue growth and recovery of the incident run, the numbers Section 5.8 quotes (D-2026-09-20-1).

Reads the two trajectory files `run_incident.py` writes and reports, per minute of simulated
time: the mean speed in the kilometre upstream of the blocked cells, the same quantity in the
baseline run, and how far upstream the queue reaches. It then prints the three figures the
manuscript states: the queue at reopening, its maximum, and when upstream speeds come back to
within two percent of the baseline.

A cell counts as queued when its mean speed in that minute is below half of free flow; the
queue reaches back to the furthest upstream block that is queued.

Usage:
    .venv/bin/python analyse_incident.py [--bin 60] [--quiet]
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from config import CELL_LENGTH_M, HDV_VEHICLE

INCIDENT_DIR = Path("output") / "incident"
BLOCK_CELLS = 25  # cells per position block, about 190 m
QUEUE_SPEED_RATIO = 0.5  # below half of free flow counts as queued
RECOVERED_RATIO = 0.98  # back to within two percent of the baseline
UPSTREAM_BLOCKS = 4  # blocks upstream of the closure that "upstream speed" averages over


def mean_speeds(path, bin_seconds):
    """Mean speed per (time bin, position block) of one run, and the run's config.

    Args:
        path: a trajectory JSON written by `run_incident.py`.
        bin_seconds: width of a time bin.
    """
    data = json.load(open(path))
    speeds = defaultdict(list)
    for vehicle in data["trajectories"]:
        for record in vehicle["trajectory"]:
            speeds[(int(record["t"] // bin_seconds), record["cell"] // BLOCK_CELLS)].append(
                record["speed"])
    return data["config"], {key: sum(v) / len(v) for key, v in speeds.items()}


def upstream_speed(grid, time_bin, closure_block):
    """Mean speed over the blocks just upstream of the closure in one time bin, or None.

    Args:
        grid: from `mean_speeds`.
        time_bin: the bin to read.
        closure_block: position block holding the blocked cells.
    """
    values = [speed for (tb, block), speed in grid.items()
              if tb == time_bin and closure_block - UPSTREAM_BLOCKS <= block <= closure_block]
    return sum(values) / len(values) if values else None


def queue_back_km(grid, time_bin, closure_block):
    """How far upstream of the closure the queue reaches in one time bin, in km.

    Args:
        grid: from `mean_speeds`.
        time_bin: the bin to read.
        closure_block: position block holding the blocked cells.
    """
    queued = [block for (tb, block), speed in grid.items()
              if tb == time_bin and block <= closure_block
              and speed < QUEUE_SPEED_RATIO * HDV_VEHICLE.v_max]
    if not queued:
        return 0.0
    return (closure_block - min(queued)) * BLOCK_CELLS * CELL_LENGTH_M / 1000.0


def main():
    """Print the per-minute table and the three quoted figures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin", type=int, default=60, help="time bin in seconds (default 60)")
    parser.add_argument("--quiet", action="store_true", help="only the summary")
    args = parser.parse_args()

    config, incident = mean_speeds(INCIDENT_DIR / "incident_trajectory.json", args.bin)
    _, baseline = mean_speeds(INCIDENT_DIR / "baseline_trajectory.json", args.bin)
    closure_block = config["closure_start_cell"] // BLOCK_CELLS
    on, off = config["incident_on"], config["incident_off"]
    bins = int(config["sim_duration"] // args.bin)

    print(f"lanes closed {config.get('closure_lanes')}, demand {config['mainline_flow']} veh/h, "
          f"closed {on:.0f} to {off:.0f} s")
    if not args.quiet:
        print(" t (s)   incident   baseline   queue back (km)")
    at_reopening, peak, peak_time, recovered_at = 0.0, 0.0, None, None
    for time_bin in range(bins):
        incident_speed = upstream_speed(incident, time_bin, closure_block)
        baseline_speed = upstream_speed(baseline, time_bin, closure_block)
        back = queue_back_km(incident, time_bin, closure_block)
        seconds = time_bin * args.bin
        if not args.quiet and incident_speed and baseline_speed:
            print(f"{seconds:6.0f}   {incident_speed:8.2f}   {baseline_speed:8.2f}   {back:8.2f}")
        if seconds <= off:
            at_reopening = back
        if back > peak:
            peak, peak_time = back, seconds
        if (recovered_at is None and seconds > off and incident_speed and baseline_speed
                and incident_speed >= RECOVERED_RATIO * baseline_speed):
            recovered_at = seconds

    print(f"\nqueue at reopening ({off:.0f} s): {at_reopening:.2f} km")
    print(f"maximum queue: {peak:.2f} km at t = {peak_time:.0f} s")
    if recovered_at is not None:
        print(f"upstream speed within {100 * (1 - RECOVERED_RATIO):.0f}% of baseline at "
              f"t = {recovered_at:.0f} s, {(recovered_at - off) / 60:.0f} min after reopening")
    else:
        print("upstream speed had not returned to the baseline by the end of the run")


if __name__ == "__main__":
    main()
