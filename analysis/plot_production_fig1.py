"""Build production Figure 1 from S=4 production summaries.

Run:
  uv run python analysis/plot_production_fig1.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from insurance_sim.production_figures import write_production_fig1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the promoted production Figure 1")
    parser.add_argument(
        "--core",
        type=Path,
        default=Path("data/sim/production/fig1_s4_highres_v1/summaries.parquet"),
        help="Core S=4 production summary parquet",
    )
    parser.add_argument(
        "--highsigma",
        type=Path,
        default=Path("data/sim/production/fig1_s4_highsigma_v1/summaries.parquet"),
        help="High-sigma S=4 production summary parquet",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("analysis/reports/fig1_panels"),
        help="Output prefix for PNG, PDF, and summary CSV",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_production_fig1(
        core_path=args.core,
        highsigma_path=args.highsigma,
        out_png=args.out_prefix.with_suffix(".png"),
        out_pdf=args.out_prefix.with_suffix(".pdf"),
        summary_out=args.out_prefix.with_name(args.out_prefix.name + "_summary.csv"),
    )
    print(f"Wrote production Figure 1 to {args.out_prefix.parent}")


if __name__ == "__main__":
    main()
