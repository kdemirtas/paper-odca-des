"""Run all ODCA-DES experiments for the paper.

Scenarios:
  S1: Baseline       (0% AV)
  S2: Low AV          (30% AV)
  S3: Medium AV       (50% AV)
  S4: High AV         (70% AV)

Each scenario runs for 3600s with 300s warmup.

Single-seed mode (default): outputs to output/experiments/ as before.
Multi-seed mode (--seeds 1 2 3 ...): writes one JSON per (scenario, seed) to a target
directory; aggregate_multiseed.py turns them into the CSVs (D-2026-09-19-3).
HDV action_interval may be overridden with --action-interval.
"""

import argparse
import logging
import csv
from dataclasses import replace
from pathlib import Path

from config import HDV_DRIVER, sim_config
from odca.analysis.metrics import summary_statistics, passage_time_flow
from odca.experiment import RunRecord, run_once, write_run

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SCENARIOS = [
    ("S1_baseline", 0.0),
    ("S2_low_av", 0.3),
    ("S3_med_av", 0.5),
    ("S4_high_av", 0.7),
]

# Measurement cells for FD data (spaced across the 800-cell network)
FD_MEASUREMENT_CELLS = [150, 250, 450, 650]


def measure(result) -> dict:
    """Summary statistics of one run, with the scenario keys the aggregation groups by.

    Args:
        result: the run's `SimulationResult`.
    """
    config = result.config
    stats = summary_statistics(result.completed_vehicles, warmup=config.warmup,
                               sim_duration=config.sim_duration)
    stats["av_penetration"] = config.av_penetration
    stats["seed"] = config.seed
    stats["hdv_action_interval"] = config.hdv_driver.action_interval
    return stats


def run_single(label: str, av_pen: float, seed: int, hdv_action_interval: float,
               quick: bool = False) -> RunRecord:
    """Run one scenario and seed; the record carries the flow-density data per measurement cell."""
    overrides = dict(sim_duration=300.0, warmup=30.0) if quick else {}
    if hdv_action_interval is not None:
        overrides["hdv_driver"] = replace(HDV_DRIVER, action_interval=hdv_action_interval)
    config = sim_config(av_penetration=av_pen, seed=seed, **overrides)

    logger.info(
        f"  [{label} seed={seed} av={av_pen:.0%} "
        f"hdv_ai={config.hdv_driver.action_interval}]"
    )
    record, result = run_once(label, config, measure)
    fd_data = {
        str(mc): [{"t": t, "flow": q, "density": k, "speed": v}
                  for t, q, k, v in passage_time_flow(result.vehicles, measurement_cell=mc,
                                                      time_interval=60.0,
                                                      sim_duration=config.sim_duration)]
        for mc in FD_MEASUREMENT_CELLS
    }
    record.extra.update(sim_duration=config.sim_duration, warmup=config.warmup, fd_data=fd_data)
    return record


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true",
                   help="Quick mode: 300s sim, 30s warmup.")
    p.add_argument("--seeds", type=int, nargs="+", default=None,
                   help="List of seeds. If omitted, runs single seed=42 "
                        "to preserve legacy behavior.")
    p.add_argument("--action-interval", type=float, default=None,
                   help="Override HDV action_interval (s). AV unchanged.")
    p.add_argument("--out-dir", type=str, default=None,
                   help="Output directory. Defaults: output/experiments "
                        "(single seed) or output/multiseed/s1_s4/batch1 (--seeds), "
                        "where aggregate_multiseed.py reads.")
    p.add_argument("--scenarios", type=str, nargs="+", default=None,
                   help="Scenario labels to run (subset of S1_baseline, "
                        "S2_low_av, S3_med_av, S4_high_av). Default: all.")
    return p.parse_args()


def main():
    args = parse_args()

    scenarios = SCENARIOS
    if args.scenarios:
        allowed = set(args.scenarios)
        scenarios = [(lbl, av) for (lbl, av) in SCENARIOS if lbl in allowed]
        if not scenarios:
            raise SystemExit(f"No valid scenarios in --scenarios {args.scenarios}; "
                             f"choose from {[s[0] for s in SCENARIOS]}")

    # Legacy single-seed path
    if args.seeds is None:
        out_dir = Path(args.out_dir) if args.out_dir else Path("output") / "experiments"
        out_dir.mkdir(parents=True, exist_ok=True)
        records = []
        for label, av_pen in scenarios:
            logger.info(f"=== {label} (AV={av_pen:.0%}) ===")
            record = run_single(label, av_pen, seed=42,
                                hdv_action_interval=args.action_interval, quick=args.quick)
            write_run(out_dir / f"{label}.json", record)
            records.append(record)
        for name, rows in (("summary.csv", [{"label": r.label, **r.stats} for r in records]),
                           ("counters.csv", [{"label": r.label, **r.counters} for r in records])):
            if rows:
                with open(out_dir / name, "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=rows[0].keys())
                    w.writeheader()
                    w.writerows(rows)
        logger.info("All experiments complete.")
        return

    # Multi-seed path: one JSON per (scenario, seed); aggregate_multiseed.py writes the CSVs
    out_dir = (Path(args.out_dir) if args.out_dir
               else Path("output") / "multiseed" / "s1_s4" / "batch1")
    out_dir.mkdir(parents=True, exist_ok=True)
    for label, av_pen in scenarios:
        logger.info(f"=== {label} (AV={av_pen:.0%}), {len(args.seeds)} seeds ===")
        for seed in args.seeds:
            record = run_single(label, av_pen, seed=seed,
                                hdv_action_interval=args.action_interval, quick=args.quick)
            write_run(out_dir / f"{label}_seed{seed}.json", record)
    logger.info("All multi-seed experiments complete; run aggregate_multiseed.py for the CSVs.")


if __name__ == "__main__":
    main()
