from __future__ import annotations

import pandas as pd

from insurance_sim.diagnostics import (
    select_variance_decomposition_rows,
    summarize_fig4_partial_association,
    summarize_variance_decomposition,
)


def _diagnostic_rows() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for n_species in [2, 4, 8]:
        for sigma_env in [0.0, 0.5, 1.0, 2.0]:
            for rho_env in [0.0, 0.5, 1.0]:
                for replicate in range(2):
                    rho_eff = 0.999999 if rho_env == 1.0 else rho_env
                    cv_total = 0.02 + 0.08 * sigma_env + 0.03 / n_species - 0.01 * rho_eff
                    phi_ldm = 0.05 + 0.1 * sigma_env + 0.04 * rho_eff
                    rows.append(
                        {
                            "slope_mode": "mixed",
                            "n_species": n_species,
                            "sigma_env": sigma_env,
                            "rho_env": rho_env,
                            "rho_eff": rho_eff,
                            "phi": 0.4,
                            "alpha_inter": 0.3,
                            "mean_total": 100.0 * n_species,
                            "var_total": (100.0 * n_species * cv_total) ** 2,
                            "cv_total": cv_total,
                            "mean_species_var": 12.0 + sigma_env + replicate,
                            "phi_ldm": phi_ldm,
                            "mean_pairwise_corr": 0.1 - 0.2 * rho_eff,
                        }
                    )
    return rows


def test_variance_decomposition_uses_species_variance_and_covariance_terms() -> None:
    df = pd.DataFrame.from_records(_diagnostic_rows())
    summary = summarize_variance_decomposition(df)
    selected = select_variance_decomposition_rows(summary)

    row = selected[(selected["n_species"] == 4) & (selected["rho_env"] == 0.5)].iloc[0]
    assert row["replicate_rows"] == 2
    assert row["summed_species_variance"] > 0
    assert row["total_variance"] == row["summed_species_variance"] + row["aggregate_covariance_term"]


def test_fig4_partial_association_reports_nested_model_diagnostics() -> None:
    df = pd.DataFrame.from_records(_diagnostic_rows())
    summary = summarize_fig4_partial_association(df)

    assert list(summary["model"]) == [
        "grid covariates",
        "grid covariates + phi_LdM",
        "grid covariates + realised log-growth correlation",
        "grid covariates + both synchrony metrics",
    ]
    assert set(summary["n_scenarios"]) == {27}
    assert summary["r2"].between(0, 1).all()
