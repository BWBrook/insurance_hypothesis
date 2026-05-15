from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from insurance_sim.production_figures import (
    make_production_fig1_candidate,
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


def test_make_production_fig1_candidate_writes_outputs(tmp_path: Path) -> None:
    summary = summarize_fig1_production(_tiny_production_frame())
    out_png = tmp_path / "fig1.png"
    out_pdf = tmp_path / "fig1.pdf"
    out_csv = tmp_path / "fig1_summary.csv"

    make_production_fig1_candidate(summary, out_png, out_pdf=out_pdf, summary_out=out_csv)

    assert out_png.exists()
    assert out_pdf.exists()
    assert out_csv.exists()
