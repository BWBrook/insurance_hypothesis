"""Build production Figure 5 from the mixed-slope persistence production run.

Run:
  uv run python analysis/plot_production_fig5.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from insurance_sim.production_figures import write_production_fig5_persistence


def with_literal_suffix(prefix: Path, suffix: str) -> Path:
    """Append a file suffix without treating dots in parameter labels as extensions."""
    return prefix.parent / f"{prefix.name}{suffix}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the production Figure 5 persistence panels")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sim/production/fig5_persistence_mixed_v1/summaries.parquet"),
        help="Figure 5 production summary parquet",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("analysis/reports/fig5_phi_sensitivity_sigma0.5_extended"),
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
    write_production_fig5_persistence(
        production_path=args.input,
        out_png=with_literal_suffix(args.out_prefix, ".png"),
        out_pdf=with_literal_suffix(args.out_prefix, ".pdf"),
        summary_out=args.out_prefix.with_name(args.out_prefix.name + "_summary.csv"),
        sigma_target=args.sigma_target,
    )
    print(f"Wrote production Figure 5 to {args.out_prefix.parent}")


if __name__ == "__main__":
    main()
