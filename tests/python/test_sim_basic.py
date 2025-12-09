import numpy as np

from insurance_sim.model import (
    SimulationConfig,
    build_env_cov,
    generate_environment,
    simulate_ricker,
    simulate_replicates,
    summarise_timeseries,
)


def test_env_cov_positive_definite():
    cov = build_env_cov(sigma_env=1.0, rho=-0.1, n_species=5)
    eigvals = np.linalg.eigvalsh(cov)
    assert eigvals.min() > 0, "Covariance matrix must be positive definite"


def test_sigma_zero_converges_to_equilibrium():
    n_species = 2
    n_steps = 400
    env = np.zeros((n_steps, n_species))
    traj = simulate_ricker(
        env,
        r0=1.0,
        K=100.0,
        b_slopes=[-0.2, 0.2],
        alpha_intra=1.0,
        alpha_inter=0.3,
        floor=1e-9,
    )
    obs = traj[300:]
    mean_per_species = obs.mean(axis=0)
    expected = 100.0 / (1 + 0.3 * (n_species - 1))
    assert np.allclose(mean_per_species, expected, rtol=0.15), (
        mean_per_species,
        expected,
    )


def test_non_negative_with_variation():
    config = SimulationConfig(
        n_species=3,
        n_steps=120,
        burn_in=20,
        sigma_env=0.5,
        rho_env=0.2,
        phi=0.3,
    )
    env = generate_environment(
        n_steps=config.n_steps,
        n_species=config.n_species,
        phi=config.phi,
        sigma_env=config.sigma_env,
        rho=config.rho_env,
        rng=123,
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
    )
    assert np.all(traj >= 0), "Abundances must remain non-negative"


def test_simulate_replicates_returns_expected_length():
    config = SimulationConfig(
        n_species=2,
        n_steps=80,
        burn_in=10,
        sigma_env=0.3,
        rho_env=0.1,
    )
    df = simulate_replicates(config, n_reps=5, seed=42)
    assert len(df) == 5
    assert {"mean_total", "var_total", "cv_total"}.issubset(df.columns)


def test_synchrony_metrics_deterministic_cases():
    # Perfect synchrony: identical series => phi_ldm ~ 1, corr ~ 1
    obs_sync = np.array([[1.0, 1.0], [2.0, 2.0], [1.0, 1.0]])
    stats_sync = summarise_timeseries(obs_sync, burn_in=0)
    assert np.isclose(stats_sync["phi_ldm"], 1.0, atol=1e-6)
    assert np.isclose(stats_sync["mean_pairwise_corr"], 1.0, atol=1e-6)

    # Perfect asynchrony (one up while other down): phi_ldm ~ 0, corr ~ -1
    obs_async = np.array([[1.0, 2.0], [2.0, 1.0], [1.0, 2.0]])
    stats_async = summarise_timeseries(obs_async, burn_in=0)
    assert stats_async["phi_ldm"] < 0.05
    assert np.isclose(stats_async["mean_pairwise_corr"], -1.0, atol=1e-6)
