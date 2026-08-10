"""Diagnostic summaries for production simulation outputs."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd


def _require_columns(df: pd.DataFrame, columns: set[str]) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ValueError(f"Missing required diagnostic columns: {', '.join(missing)}")


def deterministic_equilibrium(
    *,
    r0: float,
    K: Sequence[float] | np.ndarray,
    alpha_intra: float,
    alpha_inter: float,
) -> np.ndarray:
    """Return the positive interior equilibrium of the deterministic Ricker map."""
    K_arr = np.asarray(K, dtype=float)
    if K_arr.ndim != 1 or K_arr.size < 1:
        raise ValueError("K must be a non-empty one-dimensional vector.")
    interaction = np.full((K_arr.size, K_arr.size), float(alpha_inter), dtype=float)
    np.fill_diagonal(interaction, float(alpha_intra))
    equilibrium = np.linalg.solve(interaction, float(r0) * K_arr)
    if np.any(~np.isfinite(equilibrium)) or np.any(equilibrium <= 0):
        raise ValueError("The treatment does not have a positive finite interior equilibrium.")
    return equilibrium


def weighted_alignment_index(
    weights: Sequence[float] | np.ndarray,
    response_slopes: Sequence[float] | np.ndarray,
) -> float:
    """Return A=(sum a)^2/(S sum a^2), where a_i=weight_i*b_i."""
    weight_arr = np.asarray(weights, dtype=float)
    slope_arr = np.asarray(response_slopes, dtype=float)
    if weight_arr.shape != slope_arr.shape or weight_arr.ndim != 1:
        raise ValueError("weights and response_slopes must be same-length vectors.")
    contributions = weight_arr * slope_arr
    squared_norm = float(contributions @ contributions)
    if not np.isfinite(squared_norm) or squared_norm <= 0:
        raise ValueError("Weighted response vector must have positive finite norm.")
    alignment = float(contributions.sum() ** 2 / (contributions.size * squared_norm))
    return float(np.clip(alignment, 0.0, 1.0))


def equicorrelated_forcing_ratio(
    *,
    alignment_index: float,
    n_species: int,
    rho_low: float,
    rho_high: float,
) -> float:
    """Return the first-order forcing-variance ratio between two correlations."""
    if n_species < 1:
        raise ValueError("n_species must be positive.")
    if not 0.0 <= alignment_index <= 1.0:
        raise ValueError("alignment_index must lie in [0, 1].")
    low = (1.0 - rho_low) + rho_low * n_species * alignment_index
    high = (1.0 - rho_high) + rho_high * n_species * alignment_index
    if low <= 0:
        raise ValueError("The low-correlation forcing variance must be positive.")
    return float(high / low)


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
    total-abundance variance gives the aggregate covariance term, i.e.
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
