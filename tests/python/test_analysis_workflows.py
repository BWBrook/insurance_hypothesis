from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src/python"


def _script_env() -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("PYTHONPATH")
    src = str(SRC_PATH)
    env["PYTHONPATH"] = src if not current else f"{src}:{current}"
    return env


def _run_repo_script(script: str, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        cwd=cwd,
        env=_script_env(),
        capture_output=True,
        text=True,
        check=False,
    )


def test_run_full_grid_smoke_writes_expected_schema(tmp_path: Path) -> None:
    result = _run_repo_script(
        "analysis/run_full_grid.py",
        "--run-name",
        "tiny",
        "--reps",
        "2",
        "--steps",
        "30",
        "--burn",
        "10",
        "--sigma-list",
        "0,0.5",
        "--rho-list",
        "0,0.5",
        "--species-list",
        "2",
        "--slope-mode",
        "positive",
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr or result.stdout

    out_path = tmp_path / "data/sim/grid/tiny/summaries.parquet"
    assert out_path.exists()

    df = pd.read_parquet(out_path)
    assert len(df) == 8
    assert {
        "replicate",
        "n_steps",
        "burn_in",
        "mean_total",
        "var_total",
        "cv_total",
        "mean_species_mean",
        "mean_species_var",
        "mean_extinction_freq",
        "phi_ldm",
        "mean_pairwise_corr",
        "rho_eff",
        "rho_clipped",
        "sigma_env",
        "rho_env",
        "n_species",
        "phi",
        "slope_mode",
    }.issubset(df.columns)
    assert set(df["n_steps"]) == {30}
    assert set(df["burn_in"]) == {10}
    assert set(df["n_species"]) == {2}
    assert set(df["slope_mode"]) == {"positive"}


def test_plot_grid_fails_clearly_when_required_columns_are_missing(tmp_path: Path) -> None:
    bad_input = tmp_path / "bad_input.parquet"
    pd.DataFrame(
        {
            "sigma_env": [0.5],
            "rho_env": [0.0],
            "phi": [0.4],
            "cv_total": [0.1],
            "phi_ldm": [0.2],
            "mean_pairwise_corr": [0.3],
        }
    ).to_parquet(bad_input, index=False)

    result = _run_repo_script(
        "analysis/plot_grid.py",
        "--input",
        str(bad_input),
        "--out-prefix",
        str(tmp_path / "bad"),
        cwd=tmp_path,
    )

    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "Cannot reconstruct rho_eff without rho_env and n_species columns." in combined


def test_run_all_fails_clearly_without_cached_grid_inputs(tmp_path: Path) -> None:
    result = _run_repo_script(
        "analysis/run_all.py",
        "--skip-guard-audit",
        cwd=tmp_path,
    )

    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "data/sim/grid/run1/summaries.parquet" in combined
