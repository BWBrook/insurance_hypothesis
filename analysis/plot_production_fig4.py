"""Build production Figure 4 from the mixed-slope richness production run.

Run:
  uv run python analysis/plot_production_fig4.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from insurance_sim.production_figures import write_production_fig4_cv_synchrony


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the production Figure 4 CV-synchrony panels")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sim/production/fig2_richness_mixed_v1/summaries.parquet"),
        help="Mixed-slope production summary parquet",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("analysis/reports/fig4_cv_vs_synchrony_mixed"),
        help="Output prefix for PNG, PDF, and summary CSV",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_production_fig4_cv_synchrony(
        production_path=args.input,
        out_png=args.out_prefix.with_suffix(".png"),
        out_pdf=args.out_prefix.with_suffix(".pdf"),
        summary_out=args.out_prefix.with_name(args.out_prefix.name + "_summary.csv"),
    )
    print(f"Wrote production Figure 4 to {args.out_prefix.parent}")


if __name__ == "__main__":
    main()
