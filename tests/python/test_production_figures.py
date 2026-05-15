from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from insurance_sim.production_figures import (
    make_production_fig1,
    make_production_fig2_richness,
    summarize_fig2_richness_production,
    summarize_fig1_production,
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
