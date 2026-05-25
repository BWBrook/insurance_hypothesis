"""Diagnostic summaries for production simulation outputs."""

from __future__ import annotations

import json
from collections.abc import Sequence

import numpy as np
import pandas as pd


def _require_columns(df: pd.DataFrame, columns: set[str]) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ValueError(f"Missing required diagnostic columns: {', '.join(missing)}")


def summarize_variance_decomposition(
    df: pd.DataFrame,
    *,
    group_cols: Sequence[str] = (
        "slope_mode",
        "n_species",
        "sigma_env",
        "rho_env",
        "rho_eff",
        "phi",
        "alpha_inter",
    ),
) -> pd.DataFrame:
    """Summarize total variance as species-variance and covariance terms.

    Production rows store the mean species variance for each replicate. Multiplying
    by richness gives the summed species-variance term; subtracting this from
    total-biomass variance gives the aggregate covariance term, i.e.
    ``2 * sum_{i<j} cov(N_i, N_j)``.
    """
    required = {
        "n_species",
        "mean_total",
        "var_total",
        "cv_total",
        "mean_species_var",
        *group_cols,
    }
    _require_columns(df, required)

    work = df.copy()
    work["sum_species_variance"] = work["mean_species_var"] * work["n_species"]
    work["aggregate_covariance_term"] = work["var_total"] - work["sum_species_variance"]
    work["species_variance_to_total_variance"] = np.where(
        work["var_total"] > 0,
        work["sum_species_variance"] / work["var_total"],
        np.nan,
    )
    work["covariance_to_total_variance"] = np.where(
        work["var_total"] > 0,
        work["aggregate_covariance_term"] / work["var_total"],
        np.nan,
    )

    summary = (
        work.groupby(list(group_cols), as_index=False, observed=True)
        .agg(
            mean_total=("mean_total", "mean"),
            total_variance=("var_total", "mean"),
            summed_species_variance=("sum_species_variance", "mean"),
            aggregate_covariance_term=("aggregate_covariance_term", "mean"),
            cv_total=("cv_total", "mean"),
            species_variance_to_total_variance=("species_variance_to_total_variance", "mean"),
            covariance_to_total_variance=("covariance_to_total_variance", "mean"),
            replicate_rows=("cv_total", "size"),
        )
        .reset_index(drop=True)
    )
    return pd.DataFrame(summary).sort_values(list(group_cols)).reset_index(drop=True)


def select_variance_decomposition_rows(
    summary: pd.DataFrame,
    *,
    species_values: Sequence[int] = (2, 4, 8),
    sigma_env: float = 0.5,
    rho_env_values: Sequence[float] = (0.0, 0.5, 1.0),
) -> pd.DataFrame:
    """Select a compact set of rows suitable for a manuscript supplement table."""
    required = {"n_species", "sigma_env", "rho_env"}
    _require_columns(summary, required)
    out = summary[
        summary["n_species"].isin(species_values)
        & np.isclose(summary["sigma_env"], sigma_env)
        & summary["rho_env"].isin(rho_env_values)
    ].copy()
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def _standardize(values: np.ndarray) -> np.ndarray:
    sd = values.std(axis=0, ddof=0)
    if np.any(sd == 0):
        raise ValueError("Cannot standardize a constant predictor for partial-association diagnostics.")
    return (values - values.mean(axis=0)) / sd


def _fit_r2_and_standardized_betas(y: np.ndarray, x: np.ndarray) -> tuple[float, np.ndarray]:
    xz = _standardize(x)
    yz = (y - y.mean()) / y.std(ddof=0)
    design = np.column_stack([np.ones(len(xz)), xz])
    beta = np.linalg.lstsq(design, yz, rcond=None)[0]
    fitted = design @ beta
    ss_res = float(np.sum((yz - fitted) ** 2))
    ss_tot = float(np.sum((yz - yz.mean()) ** 2))
    return 1.0 - (ss_res / ss_tot), beta[1:]


def summarize_fig4_partial_association(df: pd.DataFrame) -> pd.DataFrame:
    """Fit compact scenario-level diagnostics for CV-synchrony associations."""
    required = {
        "n_species",
        "sigma_env",
        "rho_env",
        "rho_eff",
        "phi",
        "cv_total",
        "phi_ldm",
        "mean_pairwise_corr",
    }
    _require_columns(df, required)

    scenario = (
        df.groupby(["n_species", "sigma_env", "rho_env", "rho_eff", "phi"], as_index=False, observed=True)
        .agg(
            cv_total=("cv_total", "mean"),
            phi_ldm=("phi_ldm", "mean"),
            mean_pairwise_corr=("mean_pairwise_corr", "mean"),
        )
        .reset_index(drop=True)
    )
    scenario = pd.DataFrame(scenario[scenario["sigma_env"] > 0].copy())
    if len(scenario) < 10:
        raise ValueError("Need at least 10 non-deterministic scenario means for partial diagnostics.")

    model_specs: list[tuple[str, list[str]]] = [
        ("grid covariates", ["sigma_env", "n_species", "rho_eff"]),
        ("grid covariates + phi_LdM", ["sigma_env", "n_species", "rho_eff", "phi_ldm"]),
        (
            "grid covariates + realised log-growth correlation",
            ["sigma_env", "n_species", "rho_eff", "mean_pairwise_corr"],
        ),
        (
            "grid covariates + both synchrony metrics",
            ["sigma_env", "n_species", "rho_eff", "phi_ldm", "mean_pairwise_corr"],
        ),
    ]

    y = scenario["cv_total"].to_numpy(dtype=float)
    records: list[dict[str, float | int | str]] = []
    base_r2: float | None = None
    for label, predictors in model_specs:
        x = scenario[predictors].to_numpy(dtype=float)
        r2, betas = _fit_r2_and_standardized_betas(y, x)
        if base_r2 is None:
            base_r2 = r2
        beta_map = {predictor: float(beta) for predictor, beta in zip(predictors, betas)}
        records.append(
            {
                "model": label,
                "predictors": ", ".join(predictors),
                "n_scenarios": int(len(scenario)),
                "r2": float(r2),
                "delta_r2_vs_grid_covariates": float(r2 - base_r2),
                "standardized_coefficients_json": json.dumps(beta_map, sort_keys=True),
            }
        )

    return pd.DataFrame.from_records(records)
