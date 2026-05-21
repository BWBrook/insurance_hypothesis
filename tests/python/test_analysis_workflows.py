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


def _production_record(
    *,
    slope_mode: str,
    n_species: int,
    sigma_env: float,
    rho_eff: float,
    phi: float = 0.4,
    replicate: int = 0,
) -> dict[str, float | int | str | bool]:
    slope_offset = {
        "mixed": 0.0,
        "positive_matched": 0.05,
        "positive": 0.15,
    }[slope_mode]
    richness_buffer = 1.0 / float(n_species)
    cv_total = 0.04 + slope_offset + 0.03 * float(sigma_env) + 0.04 * float(rho_eff) + 0.03 * richness_buffer
    if slope_mode == "mixed":
        pair_corr = 0.1 - 0.2 * float(rho_eff)
    else:
        pair_corr = min(0.95, 0.15 + slope_offset + 0.6 * float(rho_eff))
    return {
        "run_id": "test-production",
        "scenario_id": f"{slope_mode}-{n_species}-{sigma_env:g}-{rho_eff:g}-{phi:g}",
        "scenario_index": 0,
        "shard_id": "shard000000",
        "replicate": replicate,
        "replicate_seed": 1000 + replicate,
        "n_steps": 600,
        "burn_in": 300,
        "mean_total": 100.0 * n_species,
        "var_total": cv_total**2,
        "cv_total": cv_total,
        "mean_species_mean": 100.0,
        "mean_species_var": (20.0 + 5.0 * float(sigma_env)) ** 2,
        "mean_extinction_freq": 0.0,
        "phi_ldm": min(1.0, max(0.0, 0.15 + 0.25 * float(rho_eff) + slope_offset)),
        "mean_pairwise_corr": pair_corr,
        "rho_eff": rho_eff,
        "rho_clipped": bool(abs(float(rho_eff) - 1.0) < 1e-12),
        "sigma_env": sigma_env,
        "rho_env": 1.0 if abs(float(rho_eff) - 0.999999) < 1e-12 else rho_eff,
        "n_species": n_species,
        "phi": phi,
        "slope_mode": slope_mode,
        "alpha_inter": 0.3,
    }


def _write_parquet(path: Path, rows: list[dict[str, float | int | str | bool]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(rows).to_parquet(path, index=False)


def _write_minimal_production_summaries(root: Path) -> None:
    """Create compact production-shaped inputs without any legacy grid caches."""
    rho_vals = [0.0, 0.999999]

    fig1_core = [
        _production_record(slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho)
        for mode in ["mixed", "positive"]
        for sigma in [0.0, 2.0]
        for rho in rho_vals
    ]
    _write_parquet(root / "data/sim/production/fig1_s4_highres_v1/summaries.parquet", fig1_core)

    fig1_high = [
        _production_record(slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho)
        for mode in ["mixed", "positive"]
        for sigma in [3.0, 4.0]
        for rho in rho_vals
    ]
    _write_parquet(root / "data/sim/production/fig1_s4_highsigma_v1/summaries.parquet", fig1_high)

    fig2 = [
        _production_record(slope_mode="mixed", n_species=n_species, sigma_env=sigma, rho_eff=rho)
        for n_species in [2, 4, 8]
        for sigma in [0.0, 0.5, 1.0, 2.0]
        for rho in rho_vals
    ]
    _write_parquet(root / "data/sim/production/fig2_richness_mixed_v1/summaries.parquet", fig2)

    fig3 = [
        _production_record(slope_mode=mode, n_species=n_species, sigma_env=0.5, rho_eff=rho)
        for mode in ["mixed", "positive"]
        for n_species in [2, 4, 8]
        for rho in rho_vals
    ]
    _write_parquet(root / "data/sim/production/fig3_synchrony_v1/summaries.parquet", fig3)

    figs3 = [
        _production_record(slope_mode=mode, n_species=n_species, sigma_env=0.5, rho_eff=rho)
        for mode in ["mixed", "positive_matched", "positive"]
        for n_species in [4, 8]
        for rho in rho_vals
    ]
    _write_parquet(root / "data/sim/production/figs3_positive_matched_control_v1/summaries.parquet", figs3)

    fig5 = [
        _production_record(slope_mode="mixed", n_species=n_species, sigma_env=0.5, rho_eff=rho, phi=phi)
        for n_species in [2, 4]
        for phi in [0.0, 0.7, 0.9, 0.95]
        for rho in [-0.5, 0.5, 0.999999]
    ]
    _write_parquet(root / "data/sim/production/fig5_persistence_mixed_v1/summaries.parquet", fig5)


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


def test_run_all_uses_production_summaries_without_cached_grid_inputs(tmp_path: Path) -> None:
    _write_minimal_production_summaries(tmp_path)

    result = _run_repo_script(
        "analysis/run_all.py",
        "--skip-guard-audit",
        cwd=tmp_path,
    )

    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode == 0, combined
    assert not (tmp_path / "data/sim/grid/run1/summaries.parquet").exists()
    assert (tmp_path / "analysis/reports/fig1_panels.png").exists()
    assert (tmp_path / "analysis/reports/figS3_positive_matched_control.png").exists()
    assert (tmp_path / "paper/manuscript/figures/figS3_positive_matched_control.pdf").exists()
