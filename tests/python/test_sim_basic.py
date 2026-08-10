import numpy as np

from insurance_sim.model import (
    SimulationConfig,
    build_env_cov,
    effective_rho,
    generate_environment,
    simulate_ricker,
    simulate_ricker_with_diagnostics,
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


def test_diagnostic_and_standard_simulators_share_the_same_trajectory():
    env = generate_environment(
        n_steps=80,
        n_species=4,
        phi=0.4,
        sigma_env=0.8,
        rho=0.25,
        rng=20260810,
    )
    kwargs = {
        "r0": 1.0,
        "K": 100.0,
        "b_slopes": [-0.5, -1 / 6, 1 / 6, 0.5],
        "alpha_intra": 1.0,
        "alpha_inter": 0.3,
        "floor": 1e-9,
        "max_exp": 50.0,
    }

    standard = simulate_ricker(env, **kwargs)
    diagnostic, rates = simulate_ricker_with_diagnostics(env, **kwargs)

    assert np.array_equal(standard, diagnostic)
    assert set(rates) == {
        "frac_exp_clipped_high",
        "frac_exp_clipped_low",
        "frac_floor",
    }


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


def test_effective_rho_clips_infeasible_negative_equicorrelation():
    # For S=8, equicorrelation must satisfy rho > -1/(S-1).
    s = 8
    rho_req = -0.5
    rho_eff = effective_rho(rho_req, n_species=s, eps=1e-6)
    min_rho = -1.0 / (s - 1) + 1e-6
    assert np.isclose(rho_eff, min_rho, atol=1e-10)

    config = SimulationConfig(n_species=s, n_steps=50, burn_in=0, sigma_env=0.2, rho_env=rho_req)
    df = simulate_replicates(config, n_reps=1, seed=0)
    assert "rho_eff" in df.columns
    assert "rho_clipped" in df.columns
    assert np.isclose(df.loc[0, "rho_eff"], min_rho, atol=1e-10)
    assert bool(df.loc[0, "rho_clipped"]) is True


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


def test_phi_ldm_bound():
    # Random trajectory should yield phi_ldm within [0,1]
    rng = np.random.default_rng(0)
    traj = np.abs(rng.normal(size=(50, 5))) + 0.1
    stats = summarise_timeseries(traj, burn_in=0)
    assert 0.0 <= stats["phi_ldm"] <= 1.0 + 1e-9


def test_ar1_stationary_variance_matches_formula():
    # For long series, empirical variance should match sigma_env^2 / (1-phi^2)
    n_species = 3
    n_steps = 5000
    sigma_env = 0.5
    phi = 0.7
    rho = 0.2
    env = generate_environment(
        n_steps=n_steps,
        n_species=n_species,
        phi=phi,
        sigma_env=sigma_env,
        rho=rho,
        rng=123,
    )
    # Average variance across species
    emp_var = env.var(axis=0, ddof=1).mean()
    expected_var = sigma_env**2 / (1.0 - phi**2)
    assert np.isclose(emp_var, expected_var, rtol=0.2), (emp_var, expected_var)
