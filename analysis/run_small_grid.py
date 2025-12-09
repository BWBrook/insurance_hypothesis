"""Run a minimal preview simulation grid for the insurance hypothesis project.

Scenarios:
- n_species = 2
- sigma_env in {0, 0.5}
- rho_env in {0, 0.5}
- 20 replicates each

Outputs a parquet summary to data/sim/preview/summaries.parquet.
"""

from itertools import product
from pathlib import Path

import pandas as pd

from insurance_sim.model import SimulationConfig, simulate_replicates


def main() -> None:
    out_dir = Path("data/sim/preview")
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = list(product([0.0, 0.5], [0.0, 0.5]))
    all_records = []

    for sigma_env, rho_env in scenarios:
        config = SimulationConfig(
            n_species=2,
            n_steps=200,
            burn_in=100,
            sigma_env=sigma_env,
            rho_env=rho_env,
            phi=0.4,
            r0=1.0,
            K=100.0,
            alpha_intra=1.0,
            alpha_inter=0.3,
        )
        df = simulate_replicates(config, n_reps=20, seed=123)
        df["sigma_env"] = sigma_env
        df["rho_env"] = rho_env
        df["n_species"] = config.n_species
        df["phi"] = config.phi
        all_records.append(df)

    all_df = pd.concat(all_records, ignore_index=True)
    out_path = out_dir / "summaries.parquet"
    all_df.to_parquet(out_path, index=False)
    print(f"Wrote {len(all_df)} rows to {out_path}")


if __name__ == "__main__":
    main()
