from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

from insurance_sim.production import create_manifest, seed_for_replicate


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src/python"


def _script_env() -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("PYTHONPATH")
    src = str(SRC_PATH)
    env["PYTHONPATH"] = src if not current else f"{src}:{current}"
    return env


def _run_production_script(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "analysis/production_grid.py"), *args],
        cwd=cwd,
        env=_script_env(),
        capture_output=True,
        text=True,
        check=False,
    )


def test_create_manifest_counts_and_replicate_seeds_are_stable() -> None:
    manifest = create_manifest(
        run_id="unit",
        reps_per_scenario=5,
        replicates_per_shard=2,
        sigma_vals=[0.0, 0.5],
        rho_vals=[0.0, 0.5],
        species_vals=[2],
        slope_modes=["mixed", "positive"],
        phi=0.4,
        steps=30,
        burn=10,
        alpha_inter=0.3,
        base_seed=12345,
    )

    assert manifest["scenario_count"] == 8
    assert manifest["shard_count"] == 24
    assert manifest["expected_rows"] == 40
    assert seed_for_replicate(12345, 0, 0) == seed_for_replicate(12345, 0, 0)
    assert seed_for_replicate(12345, 0, 0) != seed_for_replicate(12345, 0, 1)
    assert seed_for_replicate(12345, 0, 0) != seed_for_replicate(12345, 1, 0)


def test_create_manifest_from_spec_cli_checks_expected_counts(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    manifest_path = tmp_path / "manifest.json"
    spec = {
        "spec_version": 1,
        "run_id": "spec_smoke",
        "manifest": {
            "reps_per_scenario": 5,
            "replicates_per_shard": 2,
            "steps": 30,
            "burn": 10,
            "phi": 0.4,
            "alpha_inter": 0.3,
            "base_seed": 12345,
            "sigma_vals": [0.0, 0.5],
            "rho_vals": [0.0],
            "species_vals": [2],
            "slope_modes": ["mixed", "positive"],
        },
        "expected": {
            "scenario_count": 4,
            "shard_count": 12,
            "expected_rows": 20,
        },
    }
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    create = _run_production_script(
        "create-manifest-from-spec",
        "--spec",
        str(spec_path),
        "--output",
        str(manifest_path),
        cwd=tmp_path,
    )
    assert create.returncode == 0, create.stderr or create.stdout

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["run_id"] == "spec_smoke"
    assert manifest["scenario_count"] == 4
    assert manifest["shard_count"] == 12
    assert manifest["expected_rows"] == 20


def test_create_manifest_from_spec_cli_accepts_phi_values(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec_phi.json"
    manifest_path = tmp_path / "manifest_phi.json"
    spec = {
        "spec_version": 1,
        "run_id": "spec_phi_smoke",
        "manifest": {
            "reps_per_scenario": 5,
            "replicates_per_shard": 5,
            "steps": 30,
            "burn": 10,
            "phi_vals": [0.0, 0.9],
            "alpha_inter": 0.3,
            "base_seed": 12345,
            "sigma_vals": [0.5],
            "rho_vals": [0.0, 0.5],
            "species_vals": [2],
            "slope_modes": ["mixed"],
        },
        "expected": {
            "scenario_count": 4,
            "shard_count": 4,
            "expected_rows": 20,
        },
    }
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    create = _run_production_script(
        "create-manifest-from-spec",
        "--spec",
        str(spec_path),
        "--output",
        str(manifest_path),
        cwd=tmp_path,
    )
    assert create.returncode == 0, create.stderr or create.stdout

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    observed_phis = sorted({scenario["phi"] for scenario in manifest["scenarios"]})
    assert observed_phis == [0.0, 0.9]
    assert manifest["scenario_order"] == ["slope_mode", "n_species", "phi", "sigma_env", "rho_env"]
    assert manifest["scenario_count"] == 4


def test_production_cli_smoke_runs_combines_and_validates(tmp_path: Path) -> None:
    manifest_path = tmp_path / "prod_smoke/manifest.json"
    combined_path = tmp_path / "prod_smoke/summaries.parquet"
    validation_path = tmp_path / "prod_smoke/validation.json"

    create = _run_production_script(
        "create-manifest",
        "--output",
        str(manifest_path),
        "--run-id",
        "prod_smoke",
        "--reps",
        "3",
        "--replicates-per-shard",
        "2",
        "--steps",
        "30",
        "--burn",
        "10",
        "--sigma-list",
        "0,0.5",
        "--rho-list",
        "0",
        "--species-list",
        "2",
        "--slope-modes",
        "mixed,positive",
        cwd=tmp_path,
    )
    assert create.returncode == 0, create.stderr or create.stdout

    run = _run_production_script(
        "run-pending",
        "--manifest",
        str(manifest_path),
        "--jobs",
        "2",
        cwd=tmp_path,
    )
    assert run.returncode == 0, run.stderr or run.stdout

    combine = _run_production_script(
        "combine",
        "--manifest",
        str(manifest_path),
        "--output",
        str(combined_path),
        "--validation-output",
        str(validation_path),
        cwd=tmp_path,
    )
    assert combine.returncode == 0, combine.stderr or combine.stdout

    validate = _run_production_script(
        "validate",
        "--manifest",
        str(manifest_path),
        "--combined",
        str(combined_path),
        cwd=tmp_path,
    )
    assert validate.returncode == 0, validate.stderr or validate.stdout

    df = pd.read_parquet(combined_path)
    assert len(df) == 12
    assert set(df["run_id"]) == {"prod_smoke"}
    assert set(df["replicate"]) == {0, 1, 2}
    assert set(df["slope_mode"]) == {"mixed", "positive"}
    assert validation_path.exists()

    done_markers = sorted((manifest_path.parent / "shards").glob("*.done.json"))
    assert done_markers
    done_payload = json.loads(done_markers[0].read_text())
    assert done_payload["duration_seconds"] >= 0


def test_combine_fails_clearly_when_shards_are_missing(tmp_path: Path) -> None:
    manifest_path = tmp_path / "missing/manifest.json"
    combined_path = tmp_path / "missing/summaries.parquet"

    create = _run_production_script(
        "create-manifest",
        "--output",
        str(manifest_path),
        "--run-id",
        "missing",
        "--reps",
        "2",
        "--replicates-per-shard",
        "1",
        "--steps",
        "30",
        "--burn",
        "10",
        "--sigma-list",
        "0",
        "--rho-list",
        "0",
        "--species-list",
        "2",
        "--slope-modes",
        "mixed",
        cwd=tmp_path,
    )
    assert create.returncode == 0, create.stderr or create.stdout

    run_one = _run_production_script(
        "run-shard",
        "--manifest",
        str(manifest_path),
        "--shard-id",
        "shard000000",
        cwd=tmp_path,
    )
    assert run_one.returncode == 0, run_one.stderr or run_one.stdout

    combine = _run_production_script(
        "combine",
        "--manifest",
        str(manifest_path),
        "--output",
        str(combined_path),
        cwd=tmp_path,
    )
    combined_output = f"{combine.stdout}\n{combine.stderr}"
    assert combine.returncode != 0
    assert "Missing shard outputs" in combined_output
