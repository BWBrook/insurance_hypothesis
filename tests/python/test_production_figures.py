from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from insurance_sim.production_figures import (
    make_production_fig1,
    make_production_fig2_richness,
    make_production_fig3_synchrony,
    make_production_fig4_cv_synchrony,
    make_production_fig5_persistence,
    summarize_fig2_richness_production,
    summarize_fig1_production,
    summarize_fig3_synchrony_production,
    summarize_fig4_cv_synchrony_production,
    summarize_fig5_persistence_production,
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


def test_make_production_fig1_writes_outputs(tmp_path: Path) -> None:
    summary = summarize_fig1_production(_tiny_production_frame())
    out_png = tmp_path / "fig1.png"
    out_pdf = tmp_path / "fig1.pdf"
    out_csv = tmp_path / "fig1_summary.csv"

    make_production_fig1(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()


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


def test_make_production_fig2_richness_writes_outputs(tmp_path: Path) -> None:
    summary = pd.DataFrame(
        {
            "sigma_env": [0.0, 0.0, 0.5, 0.5],
            "n_species": [2, 4, 2, 4],
            "cv_mean": [0.0, 0.0, 0.25, 0.12],
            "cv_min": [0.0, 0.0, 0.2, 0.1],
            "cv_max": [0.0, 0.0, 0.3, 0.14],
            "extinction_mean": [0.0, 0.0, 0.001, 0.001],
            "extinction_max": [0.0, 0.0, 0.002, 0.002],
            "rho_count": [2, 2, 2, 2],
        }
    )
    out_png = tmp_path / "fig2.png"
    out_pdf = tmp_path / "fig2.pdf"
    out_csv = tmp_path / "fig2_summary.csv"

    make_production_fig2_richness(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()


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


def test_make_production_fig3_synchrony_writes_outputs(tmp_path: Path) -> None:
    summary = pd.DataFrame(
        {
            "slope_mode": ["mixed", "mixed", "positive", "positive"],
            "n_species": [2, 4, 2, 4],
            "rho_eff": [0.0, 1.0, 0.0, 1.0],
            "pair_corr_mean": [-0.1, -0.4, 0.2, 0.8],
            "pair_corr_sd": [0.01, 0.01, 0.01, 0.01],
            "phi_ldm_mean": [0.2, 0.3, 0.4, 0.5],
            "cv_total_mean": [0.1, 0.2, 0.3, 0.4],
            "extinction_mean": [0.0, 0.0, 0.0, 0.0],
            "replicate_rows": [1000, 1000, 1000, 1000],
            "delta_corr": [-0.1, -1.4, 0.2, -0.2],
        }
    )
    out_png = tmp_path / "fig3.png"
    out_pdf = tmp_path / "fig3.pdf"
    out_csv = tmp_path / "fig3_summary.csv"

    make_production_fig3_synchrony(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()


def test_summarize_fig4_cv_synchrony_production_filters_and_aggregates() -> None:
    rows: list[dict[str, float | int | str]] = []
    for sigma_env in [0.0, 0.5]:
        for n_species in [2, 4]:
            for rho_eff in [0.0, 0.5]:
                for replicate in [0, 1]:
                    rows.append(
                        {
                            "slope_mode": "mixed",
                            "sigma_env": sigma_env,
                            "rho_eff": rho_eff,
                            "n_species": n_species,
                            "replicate": replicate,
                            "cv_total": sigma_env + (1.0 / n_species) + replicate * 0.1,
                            "phi_ldm": 0.1 + rho_eff,
                            "mean_pairwise_corr": -0.2 + rho_eff,
                            "mean_extinction_freq": 0.0,
                        }
                    )

    summary = summarize_fig4_cv_synchrony_production(pd.DataFrame.from_records(rows))

    assert len(summary) == 4
    assert set(summary["sigma_env"]) == {0.5}
    row = summary[summary["n_species"].eq(4) & summary["rho_eff"].eq(0.5)].iloc[0]
    assert row["cv_total_mean"] == pytest.approx(0.8)
    assert row["phi_ldm_mean"] == pytest.approx(0.6)
    assert row["pair_corr_mean"] == pytest.approx(0.3)


def test_make_production_fig4_cv_synchrony_writes_outputs(tmp_path: Path) -> None:
    summary = pd.DataFrame(
        {
            "n_species": [2, 4, 6, 8],
            "sigma_env": [0.2, 0.5, 1.0, 2.0],
            "rho_eff": [0.0, 0.25, 0.5, 1.0],
            "cv_total_mean": [0.05, 0.12, 0.3, 0.7],
            "phi_ldm_mean": [0.05, 0.1, 0.2, 0.35],
            "pair_corr_mean": [-0.2, -0.05, 0.1, 0.25],
            "extinction_mean": [0.0, 0.0, 0.0, 0.001],
            "replicate_rows": [1000, 1000, 1000, 1000],
        }
    )
    out_png = tmp_path / "fig4.png"
    out_pdf = tmp_path / "fig4.pdf"
    out_csv = tmp_path / "fig4_summary.csv"

    make_production_fig4_cv_synchrony(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()


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


def test_make_production_fig5_persistence_writes_outputs(tmp_path: Path) -> None:
    rows: list[dict[str, float | int]] = []
    for n_species in [2, 4]:
        for phi in [0.0, 0.7, 0.9, 0.95]:
            for rho_eff in [-0.5, 0.0, 0.5, 1.0]:
                rows.append(
                    {
                        "n_species": n_species,
                        "phi": phi,
                        "sigma_env": 0.5,
                        "rho_eff": rho_eff,
                        "cv_total_mean": 0.1 + phi + (0.05 * n_species) - (0.03 * rho_eff),
                        "cv_total_sd": 0.01,
                        "extinction_mean": 0.0,
                        "extinction_max": 0.0,
                        "replicate_rows": 1000,
                    }
                )
    summary = pd.DataFrame.from_records(rows)
    out_png = tmp_path / "fig5.png"
    out_pdf = tmp_path / "fig5.pdf"
    out_csv = tmp_path / "fig5_summary.csv"

    make_production_fig5_persistence(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()
