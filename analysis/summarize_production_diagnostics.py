"""Write production-derived diagnostic summaries for manuscript support."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from insurance_sim.diagnostics import (
    select_variance_decomposition_rows,
    summarize_fig4_partial_association,
    summarize_variance_decomposition,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fig2-production",
        type=Path,
        default=Path("data/sim/production/fig2_richness_mixed_v1/summaries.parquet"),
        help="Production parquet used for Figures 2 and 4.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("analysis/reports"),
        help="Output directory for diagnostic CSVs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(args.fig2_production)

    variance = summarize_variance_decomposition(df)
    variance.to_csv(args.out_dir / "variance_decomposition_fig2_mixed_summary.csv", index=False)
    select_variance_decomposition_rows(variance).to_csv(
        args.out_dir / "variance_decomposition_fig2_mixed_selected_summary.csv",
        index=False,
    )

    partial = summarize_fig4_partial_association(df)
    partial.to_csv(args.out_dir / "fig4_partial_association_summary.csv", index=False)


if __name__ == "__main__":
    main()
