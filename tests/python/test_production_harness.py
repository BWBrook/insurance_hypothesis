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
MODEL_CONSTANTS = {
    "r0": 1.0,
    "K": 100.0,
    "alpha_intra": 1.0,
    "alpha_inter": 0.3,
    "floor": 1e-9,
    "max_exp": 50.0,
}


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


def _spec(
    *,
    run_id: str,
    reps: int = 3,
    replicates_per_shard: int = 2,
    phi_vals: list[float] | None = None,
) -> dict[str, object]:
    manifest: dict[str, object] = {
        "reps_per_scenario": reps,
        "replicates_per_shard": replicates_per_shard,
        "steps": 30,
        "burn": 10,
        "base_seed": 12345,
        "sigma_vals": [0.0, 0.5],
        "rho_vals": [0.0],
        "species_vals": [2],
        "slope_modes": ["mixed", "positive"],
        **MODEL_CONSTANTS,
    }
    if phi_vals is None:
        manifest["phi"] = 0.4
    else:
        manifest["phi_vals"] = phi_vals
    scenario_count = 4 if phi_vals is None else 8
    shard_count = scenario_count * ((reps + replicates_per_shard - 1) // replicates_per_shard)
    return {
        "spec_version": 1,
        "run_id": run_id,
        "manifest": manifest,
        "expected": {
            "scenario_count": scenario_count,
            "shard_count": shard_count,
            "expected_rows": scenario_count * reps,
        },
    }


def _write_spec(path: Path, spec: dict[str, object]) -> None:
    path.write_text(json.dumps(spec), encoding="utf-8")


def test_manifest_counts_constants_and_replicate_seeds_are_stable() -> None:
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
        r0=1.0,
        K=100.0,
        alpha_intra=1.0,
        alpha_inter=0.3,
        floor=1e-9,
        max_exp=50.0,
        base_seed=12345,
    )

    assert manifest["scenario_count"] == 8
    assert manifest["shard_count"] == 24
    assert manifest["expected_rows"] == 40
    assert {key: manifest["scenarios"][0][key] for key in MODEL_CONSTANTS} == MODEL_CONSTANTS
    assert seed_for_replicate(12345, 0, 0) == seed_for_replicate(12345, 0, 0)
    assert seed_for_replicate(12345, 0, 0) != seed_for_replicate(12345, 0, 1)
    assert seed_for_replicate(12345, 0, 0) != seed_for_replicate(12345, 1, 0)


def test_spec_cli_preserves_phi_values_and_expected_counts(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    manifest_path = tmp_path / "manifest.json"
    _write_spec(spec_path, _spec(run_id="spec-phi", phi_vals=[0.0, 0.9]))

    create = _run_production_script(
        "create",
        "--spec",
        str(spec_path),
        "--output",
        str(manifest_path),
        cwd=tmp_path,
    )
    assert create.returncode == 0, create.stderr or create.stdout

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert sorted({scenario["phi"] for scenario in manifest["scenarios"]}) == [0.0, 0.9]
    assert manifest["scenario_order"] == [
        "slope_mode",
        "n_species",
        "phi",
        "sigma_env",
        "rho_env",
    ]
    assert manifest["scenario_count"] == 8
    assert manifest["expected_rows"] == 24


def test_production_cli_runs_combines_and_validates_a_spec(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.json"
    manifest_path = tmp_path / "prod_smoke/manifest.json"
    combined_path = tmp_path / "prod_smoke/summaries.parquet"
    validation_path = tmp_path / "prod_smoke/validation.json"
    _write_spec(spec_path, _spec(run_id="prod_smoke"))

    create = _run_production_script(
        "create",
        "--spec",
        str(spec_path),
        "--output",
        str(manifest_path),
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
    spec_path = tmp_path / "spec.json"
    manifest_path = tmp_path / "missing/manifest.json"
    combined_path = tmp_path / "missing/summaries.parquet"
    _write_spec(
        spec_path,
        _spec(run_id="missing", reps=2, replicates_per_shard=1),
    )

    create = _run_production_script(
        "create",
        "--spec",
        str(spec_path),
        "--output",
        str(manifest_path),
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
