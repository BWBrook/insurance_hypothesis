from __future__ import annotations

import re
from typing import Callable

import pytest

from insurance_sim.model import SimulationConfig, simulate_replicates, slopes_for_mode


def test_positive_slopes_high_rho_increases_cv_and_realised_correlation() -> None:
    low_rho = SimulationConfig(
        n_species=4,
        n_steps=240,
        burn_in=120,
        sigma_env=0.5,
        rho_env=-0.5,
        phi=0.4,
        b_slopes=slopes_for_mode("positive", 4),
    )
    high_rho = SimulationConfig(
        n_species=4,
        n_steps=240,
        burn_in=120,
        sigma_env=0.5,
        rho_env=1.0,
        phi=0.4,
        b_slopes=slopes_for_mode("positive", 4),
    )

    low = simulate_replicates(low_rho, n_reps=40, seed=20260307)
    high = simulate_replicates(high_rho, n_reps=40, seed=20260307)

    assert high["cv_total"].mean() > low["cv_total"].mean()
    assert high["mean_pairwise_corr"].mean() > low["mean_pairwise_corr"].mean()


def test_mixed_slopes_higher_richness_reduces_mean_cv() -> None:
    low_richness = SimulationConfig(
        n_species=2,
        n_steps=240,
        burn_in=120,
        sigma_env=0.5,
        rho_env=0.5,
        phi=0.4,
    )
    high_richness = SimulationConfig(
        n_species=8,
        n_steps=240,
        burn_in=120,
        sigma_env=0.5,
        rho_env=0.5,
        phi=0.4,
    )

    low = simulate_replicates(low_richness, n_reps=40, seed=20260307)
    high = simulate_replicates(high_richness, n_reps=40, seed=20260307)

    assert high["cv_total"].mean() < low["cv_total"].mean()


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (lambda: SimulationConfig(n_species=0, n_steps=10), "n_species must be at least 1."),
        (
            lambda: SimulationConfig(n_species=2, n_steps=10, burn_in=10),
            "burn_in must satisfy 0 <= burn_in < n_steps.",
        ),
        (
            lambda: SimulationConfig(n_species=2, n_steps=10, sigma_env=-0.1),
            "sigma_env must be finite and non-negative.",
        ),
        (
            lambda: SimulationConfig(n_species=2, n_steps=10, phi=1.0),
            "phi must be finite and satisfy abs(phi) < 1.",
        ),
        (
            lambda: SimulationConfig(n_species=2, n_steps=10, K=0.0),
            "K values must be finite and strictly positive.",
        ),
        (
            lambda: SimulationConfig(n_species=2, n_steps=10, b_slopes=[0.1]),
            "Length of b_slopes must match n_species.",
        ),
    ],
)
def test_simulation_config_rejects_invalid_inputs(factory: Callable[[], object], message: str) -> None:
    with pytest.raises(ValueError, match=re.escape(message)):
        factory()


def test_simulate_replicates_requires_positive_n_reps() -> None:
    config = SimulationConfig(n_species=2, n_steps=10)
    with pytest.raises(ValueError, match="n_reps must be positive."):
        simulate_replicates(config, n_reps=0, seed=1)
