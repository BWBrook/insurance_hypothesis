"""Simulation utilities for insurance hypothesis experiments."""

from .model import (
    SimulationConfig,
    build_env_cov,
    effective_rho,
    generate_environment,
    simulate_ricker,
    simulate_replicates,
    slopes_for_mode,
    summarise_timeseries,
)

__all__ = [
    "SimulationConfig",
    "build_env_cov",
    "effective_rho",
    "generate_environment",
    "simulate_ricker",
    "simulate_replicates",
    "slopes_for_mode",
    "summarise_timeseries",
]
