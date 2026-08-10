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


def _run_all(cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "analysis/run_all.py")],
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
    slope_offset = {"mixed": 0.0, "positive_matched": 0.05, "positive": 0.15}[slope_mode]
    cv_total = 0.04 + slope_offset + 0.03 * sigma_env + 0.04 * rho_eff + 0.03 / n_species
    pair_corr = (
        0.1 - 0.2 * rho_eff
        if slope_mode == "mixed"
        else min(0.95, 0.15 + slope_offset + 0.6 * rho_eff)
    )
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
        "mean_species_var": (20.0 + 5.0 * sigma_env) ** 2,
        "mean_extinction_freq": 0.0,
        "phi_ldm": min(1.0, max(0.0, 0.15 + 0.25 * rho_eff + slope_offset)),
        "mean_pairwise_corr": pair_corr,
        "rho_eff": rho_eff,
        "rho_clipped": bool(abs(rho_eff - 1.0) < 1e-12),
        "sigma_env": sigma_env,
        "rho_env": 1.0 if abs(rho_eff - 0.999999) < 1e-12 else rho_eff,
        "n_species": n_species,
        "phi": phi,
        "slope_mode": slope_mode,
        "alpha_inter": 0.3,
    }


def _write_parquet(path: Path, rows: list[dict[str, float | int | str | bool]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(rows).to_parquet(path, index=False)


def _write_minimal_production_summaries(root: Path) -> None:
    rho_vals = [0.0, 0.999999]
    paths = {
        "fig1_s4_highres_v1": [
            _production_record(slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho)
            for mode in ["mixed", "positive"]
            for sigma in [0.0, 2.0]
            for rho in rho_vals
        ],
        "fig1_s4_highsigma_v1": [
            _production_record(slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho)
            for mode in ["mixed", "positive"]
            for sigma in [3.0, 4.0]
            for rho in rho_vals
        ],
        "fig2_richness_mixed_v1": [
            _production_record(slope_mode="mixed", n_species=n_species, sigma_env=sigma, rho_eff=rho)
            for n_species in [2, 4, 8]
            for sigma in [0.0, 0.5, 1.0, 2.0]
            for rho in rho_vals
        ],
        "fig3_synchrony_v1": [
            _production_record(slope_mode=mode, n_species=n_species, sigma_env=0.5, rho_eff=rho)
            for mode in ["mixed", "positive"]
            for n_species in [2, 4, 8]
            for rho in rho_vals
        ],
        "figs3_positive_matched_control_v1": [
            _production_record(slope_mode=mode, n_species=n_species, sigma_env=0.5, rho_eff=rho)
            for mode in ["mixed", "positive_matched", "positive"]
            for n_species in [4, 8]
            for rho in rho_vals
        ],
        "fig5_persistence_mixed_v1": [
            _production_record(
                slope_mode="mixed",
                n_species=n_species,
                sigma_env=0.5,
                rho_eff=rho,
                phi=phi,
            )
            for n_species in [2, 4]
            for phi in [0.0, 0.7, 0.9, 0.95]
            for rho in [-0.5, 0.5, 0.999999]
        ],
    }
    for run_name, rows in paths.items():
        _write_parquet(root / f"data/sim/production/{run_name}/summaries.parquet", rows)


def test_run_all_lists_every_missing_production_input(tmp_path: Path) -> None:
    result = _run_all(tmp_path)
    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "Missing production summaries required to regenerate the paper" in combined
    assert combined.count("summaries.parquet") == 6


def test_run_all_regenerates_complete_paper_output(tmp_path: Path) -> None:
    _write_minimal_production_summaries(tmp_path)
    result = _run_all(tmp_path)
    assert result.returncode == 0, result.stderr or result.stdout

    reports = tmp_path / "analysis/reports"
    figure_stems = [
        "fig1_panels",
        "fig2_richness_scaling_mixed",
        "fig3_imposed_vs_realised_panels",
        "fig4_cv_vs_synchrony_mixed",
        "fig5_phi_sensitivity_sigma0.5_extended",
        "figS1_production_mixed_cv_total",
        "figS2_production_mixed_phi_ldm",
        "figS3_positive_matched_control",
        "figS4_production_species_cv_vs_rho",
    ]
    for stem in figure_stems:
        assert (reports / f"{stem}.png").is_file()
        assert (reports / f"{stem}.pdf").is_file()
        assert (reports / f"{stem}_summary.csv").is_file()

    assert (reports / "variance_decomposition_fig2_mixed_summary.csv").is_file()
    assert (reports / "variance_decomposition_fig2_mixed_selected_summary.csv").is_file()
    assert (reports / "fig4_partial_association_summary.csv").is_file()
    assert not (tmp_path / "paper/manuscript/figures").exists()
