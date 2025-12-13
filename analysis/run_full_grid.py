"""Run simulation grid for the insurance hypothesis study.

Defaults (full grid):
- sigma_env: 0, 0.2, 0.5, 1.0, 1.5
- rho_env: -0.5, 0, 0.5, 0.9, 1.0
- n_species: 2, 4, 8
- phi: 0.4
- replicates: 200

Outputs parquet summaries to data/sim/grid/<run_name>/summaries.parquet
"""

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
from typing import Iterable, Sequence, Tuple

import numpy as np
import pandas as pd

from insurance_sim.model import SimulationConfig, simulate_replicates


def _parse_float_list(val: str | None, default: Sequence[float]) -> Sequence[float]:
    if val is None:
        return default
    return [float(x) for x in val.split(",") if x != ""]


def _parse_int_list(val: str | None, default: Sequence[int]) -> Sequence[int]:
    if val is None:
        return default
    return [int(x) for x in val.split(",") if x != ""]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run insurance hypothesis grid")
    parser.add_argument("--reps", type=int, default=200, help="Replicates per scenario")
    parser.add_argument("--steps", type=int, default=600, help="Total time steps")
    parser.add_argument("--burn", type=int, default=300, help="Burn-in steps to discard")
    parser.add_argument("--phi", type=float, default=0.4, help="AR(1) persistence")
    parser.add_argument(
        "--sigma-list",
        type=str,
        default=None,
        help="Comma-separated sigma_env values (default 0,0.2,0.5,1.0,1.5)",
    )
    parser.add_argument(
        "--rho-list",
        type=str,
        default=None,
        help="Comma-separated rho_env values (default -0.5,0,0.5,0.9,1.0)",
    )
    parser.add_argument(
        "--species-list",
        type=str,
        default=None,
        help="Comma-separated species richness values (default 2,4,8)",
    )
    parser.add_argument(
        "--slope-mode",
        choices=["mixed", "positive", "positive_matched", "mixed_narrow"],
        default="mixed",
        help="Slope configuration: mixed = linear -0.5..0.5; positive = 0.1..1.0; mixed_narrow = -0.25..0.25",
    )
    parser.add_argument(
        "--alpha-inter",
        type=float,
        default=0.3,
        help="Interspecific competition coefficient (relative to alpha_intra=1.0). Use 0 for no competition.",
    )
    parser.add_argument(
        "--run-name",
        type=str,
        default="run1",
        help="Name for output folder under data/sim/grid",
    )
    return parser.parse_args()


def scenario_grid(
    sigma_vals: Sequence[float], rho_vals: Sequence[float], species_vals: Sequence[int]
) -> Iterable[Tuple[float, float, int]]:
    return product(sigma_vals, rho_vals, species_vals)


def slopes_for_mode(mode: str, n_species: int) -> np.ndarray | None:
    if mode == "mixed":
        return None  # handled in simulator as default -0.5..0.5
    if mode == "positive":
        return np.linspace(0.1, 1.0, n_species)
    if mode == "positive_matched":
        # Magnitude-matched aligned regime: use abs of the mixed-slope magnitudes.
        # This isolates sign structure from overall forcing magnitude.
        return np.abs(np.linspace(-0.5, 0.5, n_species))
    if mode == "mixed_narrow":
        return np.linspace(-0.25, 0.25, n_species)
    raise ValueError(f"Unknown slope mode: {mode}")


def main() -> None:
    args = parse_args()
    sigma_vals = _parse_float_list(args.sigma_list, [0.0, 0.2, 0.5, 1.0, 1.5])
    rho_vals = _parse_float_list(args.rho_list, [-0.5, 0.0, 0.5, 0.9, 1.0])
    species_vals = _parse_int_list(args.species_list, [2, 4, 8])

    out_dir = Path("data/sim/grid") / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    all_records = []
    base_seed = 12345  # fixed for reproducibility

    for sigma_env, rho_env, n_species in scenario_grid(sigma_vals, rho_vals, species_vals):
        b_slopes = slopes_for_mode(args.slope_mode, n_species)
        config = SimulationConfig(
            n_species=n_species,
            n_steps=args.steps,
            burn_in=args.burn,
            sigma_env=sigma_env,
            rho_env=rho_env,
            phi=args.phi,
            r0=1.0,
            K=100.0,
            b_slopes=b_slopes,
            alpha_intra=1.0,
            alpha_inter=args.alpha_inter,
        )
        df = simulate_replicates(config, n_reps=args.reps, seed=base_seed)
        df["sigma_env"] = sigma_env
        df["rho_env"] = rho_env
        df["n_species"] = n_species
        df["phi"] = args.phi
        df["slope_mode"] = args.slope_mode
        all_records.append(df)
        rows_so_far = sum(len(x) for x in all_records)
        print(
            f"Completed sigma={sigma_env}, rho={rho_env}, S={n_species}, slope={args.slope_mode}; rows so far: {rows_so_far}"
        )

    all_df = pd.concat(all_records, ignore_index=True)
    out_path = out_dir / "summaries.parquet"
    all_df.to_parquet(out_path, index=False)
    print(f"Wrote {len(all_df)} rows to {out_path}")


if __name__ == "__main__":
    main()
