"""Contracts of the result files: per-seed JSON input to the aggregation, strict encoding."""

import json

import numpy as np
import pytest

from aggregate_multiseed import collect_jsons
from json_default import numpy_default


def _write(path, **payload):
    path.write_text(json.dumps(payload))


def test_collect_jsons_rejects_a_seed_seen_twice(tmp_path):
    for batch in ("batch1", "batch2"):
        (tmp_path / batch).mkdir()
        _write(tmp_path / batch / "S1_seed1.json", label="S1_baseline", av_penetration=0.0,
               hdv_action_interval=1.0, seed=1, stats={})
    with pytest.raises(ValueError, match="duplicate run"):
        list(collect_jsons(str(tmp_path / "batch*" / "*.json")))


def test_collect_jsons_rejects_an_unreadable_file(tmp_path):
    (tmp_path / "broken.json").write_text("{not json")
    with pytest.raises(json.JSONDecodeError):
        list(collect_jsons(str(tmp_path / "*.json")))


def test_collect_jsons_reads_distinct_seeds(tmp_path):
    for seed in (1, 2):
        _write(tmp_path / f"S1_seed{seed}.json", label="S1_baseline", av_penetration=0.0,
               hdv_action_interval=1.0, seed=seed, stats={})
    assert len(list(collect_jsons(str(tmp_path / "*.json")))) == 2


def test_numpy_scalars_encode_as_numbers():
    encoded = json.dumps({"n": np.int64(3), "x": np.float64(0.5)}, default=numpy_default)
    assert json.loads(encoded) == {"n": 3, "x": 0.5}


def test_unknown_objects_fail_instead_of_becoming_strings():
    with pytest.raises(TypeError):
        json.dumps({"vehicle": object()}, default=numpy_default)
