from __future__ import annotations

import pandas as pd
import pytest

from insurance_sim.production_figures import (
    summarize_fig2_richness_production,
    summarize_fig1_production,
    summarize_fig3_synchrony_production,
    summarize_fig4_weighted_boundary,
    summarize_fig5_persistence_production,
    summarize_figs3_positive_matched_control,
    summarize_mixed_heatmap_supplement,
    summarize_species_cv_supplement,
)


def _tiny_production_frame() -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for slope_mode in ["mixed", "positive"]:
        for sigma_env in [0.0, 1.0, 3.0]:
            for rho_eff in [0.0, 1.0]:
                for replicate in [0, 1]:
                    base = 0.2 + sigma_env
                    multiplier = 1.0 if slope_mode == "mixed" else 2.0
                    rows.append(
                        {
                            "slope_mode": slope_mode,
                            "sigma_env": sigma_env,
                            "rho_env": rho_eff,
                            "rho_eff": rho_eff,
                            "n_species": 4,
                            "replicate": replicate,
                            "cv_total": multiplier * base + replicate * 0.01,
                            "mean_extinction_freq": 0.01 * sigma_env,
                            "phi_ldm": 0.2 + 0.1 * rho_eff,
                            "mean_pairwise_corr": 0.3 + 0.1 * rho_eff,
                        }
                    )
    return pd.DataFrame.from_records(rows)


def test_summarize_fig1_production_aggregates_replicates() -> None:
    summary = summarize_fig1_production(_tiny_production_frame())

    assert len(summary) == 12
    row = summary[
        summary["slope_mode"].eq("positive")
        & summary["sigma_env"].eq(1.0)
        & summary["rho_eff"].eq(0.0)
    ].iloc[0]
    assert row["cv_total_mean"] == pytest.approx(2.405)
    assert row["extinction_mean"] == pytest.approx(0.01)


def test_summarize_fig2_richness_production_averages_scenario_means() -> None:
    rows: list[dict[str, float | int | str]] = []
    for n_species in [2, 4]:
        for rho_eff in [0.0, 0.5]:
            for replicate in [0, 1]:
                rows.append(
                    {
                        "slope_mode": "mixed",
                        "sigma_env": 0.5,
                        "rho_env": rho_eff,
                        "rho_eff": rho_eff,
                        "n_species": n_species,
                        "replicate": replicate,
                        "cv_total": (1.0 / n_species) + rho_eff + replicate * 0.1,
                        "mean_extinction_freq": 0.001 * n_species,
                    }
                )

    summary = summarize_fig2_richness_production(pd.DataFrame.from_records(rows))

    assert len(summary) == 2
    row = summary[summary["n_species"].eq(4)].iloc[0]
    assert row["cv_mean"] == pytest.approx(0.55)
    assert row["rho_count"] == 2


def test_summarize_fig3_synchrony_production_computes_delta() -> None:
    rows: list[dict[str, float | int | str]] = []
    for slope_mode in ["mixed", "positive"]:
        for n_species in [2, 4]:
            for rho_eff in [0.0, 0.5]:
                for replicate in [0, 1]:
                    pair_corr = (0.2 if slope_mode == "positive" else -0.2) + rho_eff + replicate * 0.01
                    rows.append(
                        {
                            "slope_mode": slope_mode,
                            "sigma_env": 0.5,
                            "rho_env": rho_eff,
                            "rho_eff": rho_eff,
                            "n_species": n_species,
                            "replicate": replicate,
                            "mean_pairwise_corr": pair_corr,
                            "phi_ldm": 0.2 + rho_eff,
                            "cv_total": 0.1 + rho_eff,
                            "mean_extinction_freq": 0.0,
                        }
                    )

    summary = summarize_fig3_synchrony_production(pd.DataFrame.from_records(rows))

    assert len(summary) == 8
    row = summary[
        summary["slope_mode"].eq("mixed")
        & summary["n_species"].eq(2)
        & summary["rho_eff"].eq(0.5)
    ].iloc[0]
    assert row["pair_corr_mean"] == pytest.approx(0.305)
    assert row["delta_corr"] == pytest.approx(-0.195)


def test_summarize_figs3_positive_matched_control_filters_and_aggregates() -> None:
    rows: list[dict[str, float | int | str]] = []
    offsets = {"mixed": -0.2, "positive_matched": 0.05, "positive": 0.2}
    for slope_mode in ["mixed", "positive_matched", "positive"]:
        for n_species in [4, 8]:
            for sigma_env in [0.5, 1.0]:
                for rho_eff in [0.0, 0.5]:
                    for replicate in [0, 1]:
                        rows.append(
                            {
                                "slope_mode": slope_mode,
                                "sigma_env": sigma_env,
                                "rho_eff": rho_eff,
                                "n_species": n_species,
                                "replicate": replicate,
                                "mean_pairwise_corr": offsets[slope_mode] + rho_eff + replicate * 0.01,
                                "phi_ldm": 0.2 + rho_eff,
                                "cv_total": 0.1 + rho_eff + replicate * 0.1,
                                "mean_extinction_freq": 0.0,
                            }
                        )

    summary = summarize_figs3_positive_matched_control(pd.DataFrame.from_records(rows))

    assert len(summary) == 12
    assert set(summary["sigma_env"]) == {0.5}
    row = summary[
        summary["slope_mode"].eq("positive_matched")
        & summary["n_species"].eq(8)
        & summary["rho_eff"].eq(0.5)
    ].iloc[0]
    assert row["pair_corr_mean"] == pytest.approx(0.555)
    assert row["cv_total_mean"] == pytest.approx(0.65)
    assert row["replicate_rows"] == 2


def test_summarize_fig4_weighted_boundary_computes_theory_and_simulation_ratios() -> None:
    rows: list[dict[str, float | int | str]] = []
    treatment_specs = [
        ("balanced", "mixed", "[-0.5,-0.166666666667,0.166666666667,0.5]", 0.0),
        ("aligned", "positive_matched", "[0.5,0.166666666667,0.166666666667,0.5]", 1.0),
    ]
    for treatment_id, slope_mode, slopes_json, level in treatment_specs:
        for rho_eff, base_cv in [(0.0, 0.2), (0.999999, 0.1 if slope_mode == "mixed" else 0.3)]:
            for replicate in [0, 1]:
                rows.append(
                    {
                        "treatment_id": treatment_id,
                        "treatment_path": "alignment",
                        "treatment_level": level,
                        "slope_mode": slope_mode,
                        "n_species": 4,
                        "r0": 1.0,
                        "K_json": "[100.0,100.0,100.0,100.0]",
                        "b_slopes_json": slopes_json,
                        "alpha_intra": 1.0,
                        "alpha_inter": 0.3,
                        "rho_eff": rho_eff,
                        "cv_total": base_cv + replicate * 0.01,
                        "mean_total": 210.0,
                        "mean_extinction_freq": 0.0,
                    }
                )

    summary = summarize_fig4_weighted_boundary(pd.DataFrame.from_records(rows))

    assert len(summary) == 2
    balanced = summary[summary["treatment_id"].eq("balanced")].iloc[0]
    aligned = summary[summary["treatment_id"].eq("aligned")].iloc[0]
    assert balanced["alignment_index"] == pytest.approx(0.0, abs=1e-12)
    assert balanced["cv2_ratio"] < 1.0
    assert aligned["alignment_index"] == pytest.approx(0.8)
    assert aligned["predicted_forcing_ratio"] == pytest.approx(3.1999978)
    assert aligned["cv2_ratio"] > 1.0


def test_summarize_fig5_persistence_production_filters_and_aggregates() -> None:
    rows: list[dict[str, float | int | str]] = []
    for sigma_env in [0.5, 1.0]:
        for phi in [0.0, 0.9]:
            for n_species in [2, 4]:
                for rho_eff in [-0.5, 0.5]:
                    for replicate in [0, 1]:
                        rows.append(
                            {
                                "slope_mode": "mixed",
                                "sigma_env": sigma_env,
                                "rho_eff": rho_eff,
                                "n_species": n_species,
                                "phi": phi,
                                "replicate": replicate,
                                "cv_total": sigma_env + phi + (1.0 / n_species) + replicate * 0.1,
                                "mean_extinction_freq": 0.0,
                            }
                        )

    summary = summarize_fig5_persistence_production(pd.DataFrame.from_records(rows), sigma_target=0.5)

    assert len(summary) == 8
    assert set(summary["sigma_env"]) == {0.5}
    row = summary[summary["n_species"].eq(4) & summary["phi"].eq(0.9) & summary["rho_eff"].eq(0.5)].iloc[0]
    assert row["cv_total_mean"] == pytest.approx(1.7)
    assert row["replicate_rows"] == 2


def test_summarize_mixed_heatmap_supplement_filters_species_and_rho() -> None:
    rows: list[dict[str, float | int | str]] = []
    for slope_mode in ["mixed", "positive"]:
        for n_species in [2, 4, 6, 8]:
            for sigma_env in [0.0, 0.5]:
                for rho_eff in [-0.2, 0.0, 0.5]:
                    for replicate in [0, 1]:
                        rows.append(
                            {
                                "slope_mode": slope_mode,
                                "n_species": n_species,
                                "sigma_env": sigma_env,
                                "rho_eff": rho_eff,
                                "replicate": replicate,
                                "cv_total": n_species + sigma_env + rho_eff + replicate * 0.1,
                                "mean_extinction_freq": 0.0,
                            }
                        )

    summary = summarize_mixed_heatmap_supplement(
        pd.DataFrame.from_records(rows),
        metric="cv_total",
        species_values=(2, 8),
    )

    assert "slope_mode" not in summary.columns
    assert set(summary["n_species"]) == {2, 8}
    assert set(summary["rho_eff"]) == {0.0, 0.5}
    row = summary[
        summary["n_species"].eq(2)
        & summary["sigma_env"].eq(0.5)
        & summary["rho_eff"].eq(0.5)
    ].iloc[0]
    assert row["metric_mean"] == pytest.approx(3.05)
    assert row["replicate_rows"] == 2


def test_summarize_species_cv_supplement_derives_cv_sp() -> None:
    rows: list[dict[str, float | int | str]] = []
    for slope_mode in ["mixed", "positive"]:
        for n_species in [4, 8]:
            for rho_eff in [0.0, 0.5]:
                for replicate in [0, 1]:
                    rows.append(
                        {
                            "slope_mode": slope_mode,
                            "sigma_env": 0.5,
                            "rho_eff": rho_eff,
                            "n_species": n_species,
                            "replicate": replicate,
                            "mean_species_mean": 10.0,
                            "mean_species_var": 4.0 + replicate,
                            "mean_extinction_freq": 0.0,
                        }
                    )

    summary = summarize_species_cv_supplement(pd.DataFrame.from_records(rows))

    assert len(summary) == 8
    row = summary[
        summary["slope_mode"].eq("mixed")
        & summary["n_species"].eq(4)
        & summary["rho_eff"].eq(0.0)
    ].iloc[0]
    expected = ((4.0**0.5) / 10.0 + (5.0**0.5) / 10.0) / 2.0
    assert row["cv_sp_mean"] == pytest.approx(expected)
    assert row["replicate_rows"] == 2
