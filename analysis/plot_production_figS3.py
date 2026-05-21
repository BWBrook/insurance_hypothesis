"""Build production Figure S3 from the positive-matched control run.

Run:
  uv run python analysis/plot_production_figS3.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from insurance_sim.production_figures import write_production_figs3_positive_matched_control


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build production Figure S3 positive-matched control")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sim/production/figs3_positive_matched_control_v1/summaries.parquet"),
        help="Figure S3 production summary parquet",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("analysis/reports/figS3_positive_matched_control"),
        help="Output prefix for PNG, PDF, and summary CSV",
    )
    parser.add_argument(
        "--sigma-target",
        type=float,
        default=0.5,
        help="sigma_env value to plot",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_production_figs3_positive_matched_control(
        production_path=args.input,
        out_png=args.out_prefix.with_suffix(".png"),
        out_pdf=args.out_prefix.with_suffix(".pdf"),
        summary_out=args.out_prefix.with_name(args.out_prefix.name + "_summary.csv"),
        sigma_target=args.sigma_target,
    )
    print(f"Wrote production Figure S3 to {args.out_prefix.parent}")


if __name__ == "__main__":
    main()
