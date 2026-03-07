"""Check numerical-guard activation rates in a few stress-test scenarios.

This script is intentionally small and fast. It does *not* change any cached
simulation outputs; it just verifies that exponent clipping and abundance
flooring are rare (or at least quantified) in high-variance corners.

Run:
  uv run python analysis/check_numerical_guards.py

Outputs:
  analysis/reports/numerical_guard_rates.csv
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from insurance_sim.model import (
    SimulationConfig,
    generate_environment,
    simulate_ricker_with_diagnostics,
    slopes_for_mode,
)


@dataclass(frozen=True)
class GuardScenario:
    name: str
    slope_mode: str
    config: SimulationConfig


def run_guard_scenario(scenario: GuardScenario, n_reps: int, seed: int) -> pd.DataFrame:
    base_rng = np.random.default_rng(seed)
    rows = []

    for rep in range(n_reps):
        rng = np.random.default_rng(base_rng.integers(0, 2**32 - 1))
        env = generate_environment(
            n_steps=scenario.config.n_steps,
            n_species=scenario.config.n_species,
            phi=scenario.config.phi,
            sigma_env=scenario.config.sigma_env,
            rho=scenario.config.rho_env,
            rng=rng,
        )
        _, diag = simulate_ricker_with_diagnostics(
            env,
            r0=scenario.config.r0,
            K=scenario.config.K,
            b_slopes=scenario.config.b_slopes,
            alpha_intra=scenario.config.alpha_intra,
            alpha_inter=scenario.config.alpha_inter,
            floor=scenario.config.floor,
            max_exp=scenario.config.max_exp,
        )
        rows.append(
            {
                "scenario": scenario.name,
                "slope_mode": scenario.slope_mode,
                "replicate": rep,
                "n_species": scenario.config.n_species,
                "phi": scenario.config.phi,
                "sigma_env": scenario.config.sigma_env,
                "rho_env_requested": scenario.config.rho_env,
                **diag,
            }
        )

    return pd.DataFrame.from_records(rows)


def main() -> None:
    out_dir = Path("analysis/reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        GuardScenario(
            name="mixed_phi095_sigma1_rho1_S4",
            slope_mode="mixed",
            config=SimulationConfig(
                n_species=4,
                n_steps=400,
                burn_in=0,
                sigma_env=1.0,
                rho_env=1.0,
                phi=0.95,
                r0=1.0,
                K=100.0,
                alpha_intra=1.0,
                alpha_inter=0.3,
            ),
        ),
        GuardScenario(
            name="positive_phi095_sigma1_rho1_S4",
            slope_mode="positive",
            config=SimulationConfig(
                n_species=4,
                n_steps=400,
                burn_in=0,
                sigma_env=1.0,
                rho_env=1.0,
                phi=0.95,
                r0=1.0,
                K=100.0,
                b_slopes=slopes_for_mode("positive", 4),
                alpha_intra=1.0,
                alpha_inter=0.3,
            ),
        ),
        GuardScenario(
            name="positive_phi04_sigma15_rho1_S8",
            slope_mode="positive",
            config=SimulationConfig(
                n_species=8,
                n_steps=600,
                burn_in=0,
                sigma_env=1.5,
                rho_env=1.0,
                phi=0.4,
                r0=1.0,
                K=100.0,
                b_slopes=slopes_for_mode("positive", 8),
                alpha_intra=1.0,
                alpha_inter=0.3,
            ),
        ),
    ]

    all_rows = []
    for sc in scenarios:
        df = run_guard_scenario(sc, n_reps=30, seed=12345)
        all_rows.append(df)

    out = pd.concat(all_rows, ignore_index=True)
    out_path = out_dir / "numerical_guard_rates.csv"
    out.to_csv(out_path, index=False)

    summary = (
        out.groupby(["scenario", "slope_mode", "n_species", "phi", "sigma_env", "rho_env_requested"])[
            ["frac_exp_clipped_high", "frac_exp_clipped_low", "frac_floor"]
        ]
        .mean()
        .reset_index()
        .sort_values(["scenario"])
    )
    print(summary.to_string(index=False))
    print(f"\nWrote replicate-level diagnostics to {out_path}")


if __name__ == "__main__":
    main()
