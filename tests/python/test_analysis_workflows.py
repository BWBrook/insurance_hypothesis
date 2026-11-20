from __future__ import annotations

import json
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
    alpha_inter: float = 0.3,
) -> dict[str, float | int | str | bool]:
    slope_offset = {"mixed": 0.0, "positive_matched": 0.05, "positive": 0.15}[slope_mode]
    cv_total = (
        0.04 + slope_offset + 0.03 * sigma_env + 0.04 * rho_eff + 0.03 / n_species + 0.002 * replicate
    )
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
        "alpha_inter": alpha_inter,
    }


def _write_parquet(path: Path, rows: list[dict[str, float | int | str | bool]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(rows).to_parquet(path, index=False)


def _boundary_record(
    *,
    treatment_id: str,
    treatment_path: str,
    treatment_level: float,
    slope_mode: str,
    r0: float,
    rho_eff: float,
    cv_total: float,
    K_json: str = "[100.0,100.0,100.0,100.0]",
    sigma_env: float = 0.5,
) -> dict[str, float | int | str]:
    slopes = (
        "[-0.5,-0.166666666667,0.166666666667,0.5]"
        if slope_mode == "mixed"
        else "[0.5,0.166666666667,0.166666666667,0.5]"
    )
    return {
        "treatment_id": treatment_id,
        "treatment_path": treatment_path,
        "treatment_level": treatment_level,
        "slope_mode": slope_mode,
        "n_species": 4,
        "r0": r0,
        "K_json": K_json,
        "b_slopes_json": slopes,
        "alpha_intra": 1.0,
        "alpha_inter": 0.3,
        "rho_eff": rho_eff,
        "cv_total": cv_total,
        "mean_total": 210.0,
        "mean_extinction_freq": 0.0,
        "sigma_env": sigma_env,
    }


def _write_minimal_production_summaries(root: Path) -> None:
    rho_vals = [0.0, 0.999999]
    paths = {
        "fig1_s4_highres_v1": [
            _production_record(
                slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho, replicate=replicate
            )
            for mode in ["mixed", "positive"]
            for sigma in [0.0, 2.0]
            for rho in rho_vals
            for replicate in [0, 1]
        ],
        "fig1_s4_highsigma_v1": [
            _production_record(
                slope_mode=mode, n_species=4, sigma_env=sigma, rho_eff=rho, replicate=replicate
            )
            for mode in ["mixed", "positive"]
            for sigma in [3.0, 4.0]
            for rho in rho_vals
            for replicate in [0, 1]
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
        "fig4_weighted_balance_r0_v1": [
            _boundary_record(
                treatment_id=(
                    f"alignment-{mode}" if r0 == 1.0 else f"r0-{r0:g}-{mode}"
                ),
                treatment_path="alignment" if r0 == 1.0 else "r0",
                treatment_level=0.0 if mode == "mixed" and r0 == 1.0 else (
                    1.0 if mode == "positive_matched" and r0 == 1.0 else r0
                ),
                slope_mode=mode,
                r0=r0,
                rho_eff=rho,
                cv_total=(
                    (0.20 if rho == 0.0 else 0.12)
                    if mode == "mixed"
                    else (0.20 if rho == 0.0 else 0.32)
                ),
            )
            for mode in ["mixed", "positive_matched"]
            for r0 in [0.25, 0.5, 1.0, 1.5]
            for rho in [0.0, 0.999999]
        ]
        + [
            _boundary_record(
                treatment_id="dominance-0.5",
                treatment_path="dominance",
                treatment_level=0.5,
                slope_mode="mixed",
                r0=1.0,
                rho_eff=rho,
                cv_total=0.20 if rho == 0.0 else 0.15,
                K_json="[85.0,95.0,105.0,115.0]",
            )
            for rho in [0.0, 0.999999]
        ],
    }
    paths["boundary_by_sigma_v1"] = [
        _boundary_record(
            treatment_id=treatment_id,
            treatment_path=path,
            treatment_level=level,
            slope_mode=mode,
            r0=1.0,
            rho_eff=rho,
            cv_total=(0.20 if rho == 0.0 else shared) + 0.002 * replicate,
            K_json=K_json,
            sigma_env=sigma,
        )
        for treatment_id, path, level, mode, shared, K_json in [
            ("alignment-q000", "alignment", 0.0, "mixed", 0.08, "[100.0,100.0,100.0,100.0]"),
            ("alignment-q1000", "alignment", 1.0, "positive_matched", 0.34, "[100.0,100.0,100.0,100.0]"),
            ("dominance-d0500", "dominance", 0.5, "mixed", 0.15, "[85.0,95.0,105.0,115.0]"),
        ]
        for sigma in [0.1, 0.5, 1.3]
        for rho in rho_vals
        for replicate in [0, 1]
    ]
    for tag, alpha_inter in [("010", 0.1), ("030", 0.3), ("060", 0.6)]:
        paths[f"sigma_mechanism_alpha{tag}_v1"] = [
            _production_record(
                slope_mode="mixed",
                n_species=n_species,
                sigma_env=sigma,
                rho_eff=rho,
                phi=phi,
                replicate=replicate,
                alpha_inter=alpha_inter,
            )
            for n_species in [2, 4]
            for phi in [0.0, 0.4]
            for sigma in [0.1, 0.2]
            for rho in rho_vals
            for replicate in [0, 1]
        ]
    for tag, alpha_inter, phi, sigma in [
        ("a030_phi000_sig100", 0.3, 0.0, 1.0),
        ("a030_phi040_sig100", 0.3, 0.4, 1.0),
        ("a060_phi000_sig100", 0.6, 0.0, 1.0),
        ("a060_phi040_sig050", 0.6, 0.4, 0.5),
        ("a060_phi080_sig020", 0.6, 0.8, 0.2),
    ]:
        paths[f"longwindow_reversal_{tag}_v1"] = [
            {
                **_production_record(
                    slope_mode="mixed",
                    n_species=8,
                    sigma_env=sigma,
                    rho_eff=rho,
                    phi=phi,
                    replicate=replicate,
                    alpha_inter=alpha_inter,
                ),
                "run_id": f"longwindow-{tag}",
            }
            for rho in rho_vals
            for replicate in [0, 1]
        ]
    prediction_cells: list[dict[str, float | int | str]] = []
    for tag, alpha_inter in [("020", 0.2), ("045", 0.45)]:
        paths[f"ordering_test_alpha{tag}_v1"] = [
            _production_record(
                slope_mode="mixed",
                n_species=n_species,
                sigma_env=sigma,
                rho_eff=rho,
                phi=0.2,
                replicate=replicate,
                alpha_inter=alpha_inter,
            )
            for n_species in [4, 8, 12]
            for sigma in [0.2, 0.5]
            for rho in rho_vals
            for replicate in [0, 1]
        ]
        for n_species in [4, 8, 12]:
            for sigma in [0.2, 0.5]:
                cell: dict[str, float | int | str] = {
                    "alpha_inter": alpha_inter, "S": n_species, "phi": 0.2, "sigma_env": sigma,
                    "c": 2.0, "x": 2.0 * sigma**2,
                }
                if n_species == 12:
                    cell["R_ref_S8"] = 1.0
                else:
                    cell["R_pred"] = 1.0
                if n_species == 8:
                    cell["reversal_call"] = "no_reversal"
                prediction_cells.append(cell)
    predictions = root / "analysis/prespecified/ordering_predictions_2026-10-19.json"
    predictions.parent.mkdir(parents=True, exist_ok=True)
    predictions.write_text(json.dumps({"cells": prediction_cells}))
    for run_name, rows in paths.items():
        _write_parquet(root / f"data/sim/production/{run_name}/summaries.parquet", rows)


def test_run_all_lists_every_missing_production_input(tmp_path: Path) -> None:
    result = _run_all(tmp_path)
    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "Missing production summaries required to regenerate the paper" in combined
    assert combined.count("summaries.parquet") == 18


def test_run_all_regenerates_complete_paper_output(tmp_path: Path) -> None:
    _write_minimal_production_summaries(tmp_path)
    result = _run_all(tmp_path)
    assert result.returncode == 0, result.stderr or result.stdout

    reports = tmp_path / "analysis/reports"
    figure_stems = [
        "fig1_panels",
        "fig2_richness_scaling_mixed",
        "fig3_imposed_vs_realised_panels",
        "fig4_weighted_balance_boundary",
        "fig5_phi_sensitivity_sigma0.5_extended",
        "figS1_production_mixed_cv_total",
        "figS2_production_mixed_phi_ldm",
        "figS3_positive_matched_control",
        "figS4_production_species_cv_vs_rho",
        "fig6_amplitude_boundary",
        "fig7_mechanism_reversal",
        "figS9_boundary_by_sigma_paths",
    ]
    for stem in figure_stems:
        assert (reports / f"{stem}.png").is_file()
        assert (reports / f"{stem}.pdf").is_file()
        assert (reports / f"{stem}_summary.csv").is_file()

    for extra in [
        "fig6_amplitude_boundary_replication_summary.csv",
        "fig6_amplitude_boundary_richness_summary.csv",
        "fig7_mechanism_reversal_longwindow_summary.csv",
        "fig7_ordering_test_summary.csv",
        "fig7_ordering_test_criteria_summary.csv",
        "fig7_mechanism_trajectory_summary.csv",
        "figS9_boundary_by_sigma_crossings_summary.csv",
    ]:
        assert (reports / extra).is_file()
    assert (reports / "variance_decomposition_fig2_mixed_summary.csv").is_file()
    assert (reports / "variance_decomposition_fig2_mixed_selected_summary.csv").is_file()
    assert not (tmp_path / "paper/manuscript/figures").exists()
