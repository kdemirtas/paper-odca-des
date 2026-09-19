"""Contract of this paper's result files: per-seed JSONs in, the aggregate CSV schema out."""

import csv

import aggregate_multiseed
from odca.experiment import RunRecord, write_run


def test_aggregation_writes_the_figure_schema(tmp_path, monkeypatch):
    batch = tmp_path / "multiseed" / "s1_s4" / "batch1"
    batch.mkdir(parents=True)
    for seed in (1, 2):
        stats = {"throughput_per_hour": 3000.0 + seed, "avg_delay": 20.0}
        write_run(batch / f"S1_baseline_seed{seed}.json",
                  RunRecord("S1_baseline", 0.0, seed, 1.0, 0.1, stats, {}))
    monkeypatch.setattr(aggregate_multiseed, "ROOT", tmp_path)
    aggregate_multiseed.aggregate_s1_s4()
    with open(tmp_path / "multiseed" / "s1_s4" / "aggregate.csv") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0]) == ["scenario", "av_penetration", "hdv_action_interval", "metric", "n",
                             "mean", "std", "ci95_lo", "ci95_hi"]
    throughput = next(r for r in rows if r["metric"] == "throughput_per_hour")
    assert (throughput["n"], throughput["mean"]) == ("2", "3001.500000")
