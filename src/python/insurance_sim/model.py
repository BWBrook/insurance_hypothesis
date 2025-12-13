"""
Core simulation utilities for the insurance hypothesis experiments.

Implements:
- Correlated environmental AR(1) generator.
- Discrete-time stochastic Ricker model with competition.
- Convenience wrappers for running replicates and summarising outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, TypeAlias

import numpy as np
import pandas as pd


DEFAULT_FLOOR = 1e-9  # small positive floor to avoid extinction-driven NaNs
DEFAULT_MAX_EXP = 50.0  # cap on exponent to avoid overflow in exp


SlopeSpec: TypeAlias = Sequence[float] | np.ndarray


def effective_rho(rho: float, n_species: int, eps: float = 1e-6) -> float:
    """Return the feasible equicorrelation after enforcing PD constraints.

    For an equicorrelation matrix of size S, positive definiteness requires:
      rho > -1/(S-1)  (and rho < 1)

    We clip to those bounds (plus a small epsilon) to avoid singular matrices.
    """
    if n_species < 2:
        return float(rho)
    min_rho = -1.0 / (n_species - 1) + eps
    max_rho = 1.0 - eps
    return float(min(max(rho, min_rho), max_rho))


@dataclass
class SimulationConfig:
    """Configuration container for a simulation scenario."""

    n_species: int
    n_steps: int
    burn_in: int = 0
    r0: float = 1.0
    K: float | Sequence[float] = 100.0
    b_slopes: SlopeSpec | None = None
    phi: float = 0.4
    sigma_env: float = 0.5
    rho_env: float = 0.0
    alpha_intra: float = 1.0
    alpha_inter: float = 0.3
    floor: float = DEFAULT_FLOOR
    max_exp: float = DEFAULT_MAX_EXP


def build_env_cov(sigma_env: float, rho: float, n_species: int) -> np.ndarray:
    """
    Build an equicorrelated covariance matrix for environmental innovations.

    The equicorrelation matrix is positive definite only if rho > -1/(S-1).
    We clip rho to that bound + small epsilon to ensure numerical stability.
    """
    if n_species < 2:
        return np.array([[sigma_env**2]], dtype=float)

    rho_eff = effective_rho(rho, n_species)

    ones = np.ones((n_species, n_species), dtype=float)
    ident = np.eye(n_species, dtype=float)
    corr = rho_eff * ones + (1.0 - rho_eff) * ident
    cov = sigma_env**2 * corr
    return cov


def generate_environment(
    n_steps: int,
    n_species: int,
    phi: float,
    sigma_env: float,
    rho: float,
    rng: np.random.Generator | int | None = None,
) -> np.ndarray:
    """
    Generate correlated environmental anomalies via multivariate AR(1).

    Returns array of shape (n_steps, n_species).
    """
    if rng is None:
        rng = np.random.default_rng()
    elif not isinstance(rng, np.random.Generator):
        rng = np.random.default_rng(rng)
    if sigma_env == 0:
        return np.zeros((n_steps, n_species), dtype=float)

    cov = build_env_cov(sigma_env, rho, n_species)
    if np.allclose(cov, 0.0):
        return np.zeros((n_steps, n_species), dtype=float)

    z = np.zeros((n_steps, n_species), dtype=float)
    prev = np.zeros(n_species, dtype=float)

    # Precompute Cholesky for speed/stability
    L = np.linalg.cholesky(cov)

    for t in range(n_steps):
        eps = rng.standard_normal(n_species) @ L.T
        current = phi * prev + eps
        z[t] = current
        prev = current
    return z


def _prepare_b_slopes(b_slopes: SlopeSpec | None, n_species: int) -> np.ndarray:
    if b_slopes is None:
        return np.linspace(-0.5, 0.5, n_species, dtype=float)
    b_arr = np.asarray(b_slopes, dtype=float)
    if b_arr.shape[0] != n_species:
        raise ValueError("Length of b_slopes must match n_species.")
    return b_arr


def _prepare_K(K: float | Sequence[float], n_species: int) -> np.ndarray:
    K_arr = np.asarray(K, dtype=float)
    if K_arr.size == 1:
        K_arr = np.full(n_species, float(K_arr), dtype=float)
    if K_arr.size != n_species:
        raise ValueError("Length of K must be 1 or n_species.")
    return K_arr


def simulate_ricker(
    env: np.ndarray,
    *,
    r0: float,
    K: float | Sequence[float],
    b_slopes: SlopeSpec | None,
    alpha_intra: float,
    alpha_inter: float,
    floor: float = DEFAULT_FLOOR,
    max_exp: float = DEFAULT_MAX_EXP,
    initial: Optional[Sequence[float]] = None,
) -> np.ndarray:
    """
    Simulate discrete-time stochastic Ricker dynamics with competition.

    Parameters
    ----------
    env : array (T, S)
        Environmental anomalies per time step and species.
    r0 : float
        Intrinsic growth intercept (shared).
    K : float or array
        Carrying capacities per species.
    b_slopes : array
        Species-specific slopes linking environment to per-capita growth.
    alpha_intra : float
        Intraspecific competition coefficient.
    alpha_inter : float
        Interspecific competition coefficient (relative strength).
    floor : float
        Minimum abundance to avoid zeros.
    max_exp : float
        Cap on the exponent to prevent overflow in exp().
    initial : array or None
        Initial abundances. If None, starts at K / 2.
    """
    T, S = env.shape
    b = _prepare_b_slopes(b_slopes, S)
    K_arr = _prepare_K(K, S)

    N = np.zeros((T + 1, S), dtype=float)
    if initial is None:
        N[0] = K_arr * 0.5
    else:
        init = np.asarray(initial, dtype=float)
        if init.size != S:
            raise ValueError("Initial abundance must have length n_species.")
        N[0] = init

    for t in range(T):
        total_biomass = np.sum(N[t])
        comp = alpha_intra * N[t] + alpha_inter * (total_biomass - N[t])
        exponent = r0 + b * env[t] - comp / K_arr
        exponent = np.clip(exponent, -max_exp, max_exp)
        N[t + 1] = np.maximum(floor, N[t] * np.exp(exponent))
    return N[1:]  # drop initial state to align length with env


def simulate_ricker_with_diagnostics(
    env: np.ndarray,
    *,
    r0: float,
    K: float | Sequence[float],
    b_slopes: SlopeSpec | None,
    alpha_intra: float,
    alpha_inter: float,
    floor: float = DEFAULT_FLOOR,
    max_exp: float = DEFAULT_MAX_EXP,
    initial: Optional[Sequence[float]] = None,
) -> tuple[np.ndarray, dict[str, float]]:
    """Simulate Ricker dynamics and report numerical-guard rates.

    This is a diagnostics helper to quantify how often numerical safeguards are
    activated (exponent clipping and abundance flooring). It is not used in the
    main pipeline by default.

    Returns
    -------
    traj : array (T, S)
        Abundance trajectories (aligned with env length).
    diagnostics : dict
        - frac_exp_clipped_high: fraction of (t,i) where exponent > +max_exp
        - frac_exp_clipped_low: fraction of (t,i) where exponent < -max_exp
        - frac_floor: fraction of (t,i) where N_i(t) == floor (post-update)
    """
    T, S = env.shape
    b = _prepare_b_slopes(b_slopes, S)
    K_arr = _prepare_K(K, S)

    N = np.zeros((T + 1, S), dtype=float)
    if initial is None:
        N[0] = K_arr * 0.5
    else:
        init = np.asarray(initial, dtype=float)
        if init.size != S:
            raise ValueError("Initial abundance must have length n_species.")
        N[0] = init

    n_hi = 0
    n_lo = 0
    n_floor = 0
    denom = T * S

    for t in range(T):
        total_biomass = np.sum(N[t])
        comp = alpha_intra * N[t] + alpha_inter * (total_biomass - N[t])
        exponent_raw = r0 + b * env[t] - comp / K_arr
        n_hi += int(np.sum(exponent_raw > max_exp))
        n_lo += int(np.sum(exponent_raw < -max_exp))
        exponent = np.clip(exponent_raw, -max_exp, max_exp)
        N[t + 1] = np.maximum(floor, N[t] * np.exp(exponent))
        n_floor += int(np.sum(N[t + 1] <= floor))

    traj = N[1:]
    diagnostics = {
        "frac_exp_clipped_high": float(n_hi / denom) if denom > 0 else np.nan,
        "frac_exp_clipped_low": float(n_lo / denom) if denom > 0 else np.nan,
        "frac_floor": float(n_floor / denom) if denom > 0 else np.nan,
    }
    return traj, diagnostics


def summarise_timeseries(
    traj: np.ndarray,
    burn_in: int,
    floor: float = DEFAULT_FLOOR,
) -> dict:
    """
    Compute summary statistics for a single trajectory (after burn-in).
    """
    if burn_in >= traj.shape[0]:
        raise ValueError("burn_in must be less than number of time steps.")

    obs = traj[burn_in:]
    total = obs.sum(axis=1)
    mean_total = float(total.mean())
    var_total = float(total.var(ddof=1)) if total.size > 1 else 0.0
    cv_total = float(np.std(total, ddof=1) / mean_total) if mean_total > 0 else np.nan

    mean_species = obs.mean(axis=0)
    var_species = obs.var(axis=0, ddof=1) if obs.shape[0] > 1 else np.zeros(obs.shape[1])
    extinction_freq = (obs <= floor).mean(axis=0)

    # Loreau–de Mazancourt synchrony (abundance-based)
    std_species = np.sqrt(var_species)
    denom = np.sum(std_species) ** 2
    phi_ldm_raw = float(var_total / denom) if denom > 0 else np.nan
    # Numerical guard: theoretical bounds [0,1]; clip small overshoots
    if np.isnan(phi_ldm_raw):
        phi_ldm = np.nan
    else:
        phi_ldm = float(np.clip(phi_ldm_raw, 0.0, 1.0))

    # Mean pairwise correlation of per-capita growth rates
    growth = np.diff(np.log(obs + floor), axis=0)  # log change; floor avoids -inf
    if growth.shape[0] > 1:
        stds = growth.std(axis=0, ddof=1)
        if np.any(stds < 1e-12):
            mean_pairwise_corr = np.nan
        else:
            corr_mat = np.corrcoef(growth, rowvar=False)
            s = corr_mat.shape[0]
            upper = corr_mat[np.triu_indices(s, k=1)]
            mean_pairwise_corr = float(np.nanmean(upper)) if upper.size else np.nan
    else:
        mean_pairwise_corr = np.nan

    return {
        "mean_total": mean_total,
        "var_total": var_total,
        "cv_total": cv_total,
        "mean_species": mean_species,
        "var_species": var_species,
        "extinction_freq": extinction_freq,
        "phi_ldm": phi_ldm,
        "mean_pairwise_corr": mean_pairwise_corr,
    }


def simulate_replicates(
    config: SimulationConfig,
    n_reps: int,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Run multiple replicate simulations for a given scenario.

    Returns a DataFrame with per-replicate summaries.
    """
    records = []
    base_rng = np.random.default_rng(seed)
    rho_eff = effective_rho(config.rho_env, config.n_species)
    rho_clipped = bool(abs(rho_eff - float(config.rho_env)) > 1e-12)

    for rep in range(n_reps):
        rng = base_rng if seed is None else np.random.default_rng(base_rng.integers(0, 2**32 - 1))
        env = generate_environment(
            n_steps=config.n_steps,
            n_species=config.n_species,
            phi=config.phi,
            sigma_env=config.sigma_env,
            rho=config.rho_env,
            rng=rng,
        )
        traj = simulate_ricker(
            env,
            r0=config.r0,
            K=config.K,
            b_slopes=config.b_slopes,
            alpha_intra=config.alpha_intra,
            alpha_inter=config.alpha_inter,
            floor=config.floor,
            max_exp=config.max_exp,
            initial=None,
        )
        stats = summarise_timeseries(traj, burn_in=config.burn_in, floor=config.floor)
        records.append(
            {
                "replicate": rep,
                "n_steps": int(config.n_steps),
                "burn_in": int(config.burn_in),
                "mean_total": stats["mean_total"],
                "var_total": stats["var_total"],
                "cv_total": stats["cv_total"],
                "mean_species_mean": float(np.mean(stats["mean_species"])),
                "mean_species_var": float(np.mean(stats["var_species"])),
                "mean_extinction_freq": float(np.mean(stats["extinction_freq"])),
                "phi_ldm": stats["phi_ldm"],
                "mean_pairwise_corr": stats["mean_pairwise_corr"],
                "rho_eff": rho_eff,
                "rho_clipped": rho_clipped,
            }
        )
    return pd.DataFrame.from_records(records)
