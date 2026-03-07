"""Plot summaries of simulation grid outputs.

Usage:
  uv run python analysis/plot_grid.py --input data/sim/grid/run1/summaries.parquet --out-prefix analysis/reports/run1

Produces:
  <out-prefix>_cv.png, <out-prefix>_phi.png, and <out-prefix>_summary.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def ensure_effective_rho(df: pd.DataFrame) -> pd.DataFrame:
    if "rho_eff" in df.columns:
        return df
    if "rho_env" not in df.columns or "n_species" not in df.columns:
        raise ValueError("Cannot reconstruct rho_eff without rho_env and n_species.")

    out = df.copy()
    eps = 1e-6
    rho_env = out["rho_env"].to_numpy(dtype=float)
    n_species = out["n_species"].to_numpy(dtype=int)
    rho_eff = rho_env.copy()

    mask = n_species >= 2
    if mask.any():
        min_rho = (-1.0 / (n_species[mask] - 1)) + eps
        max_rho = 1.0 - eps
        rho_eff[mask] = np.clip(rho_env[mask], min_rho, max_rho)

    out["rho_eff"] = rho_eff
    out["rho_clipped"] = np.abs(rho_eff - rho_env) > 1e-12
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot grid summaries")
    parser.add_argument("--input", required=True, help="Path to summaries.parquet")
    parser.add_argument(
        "--out-prefix",
        default="analysis/reports/run1",
        help="Output prefix for figures/summary",
    )
    return parser.parse_args()


def pivot_metric(df: pd.DataFrame, metric: str, s: int) -> pd.DataFrame:
    sub = df[df["n_species"] == s]
    return sub.pivot_table(index="rho_eff", columns="sigma_env", values=metric, aggfunc="mean")


def plot_heatmaps(df: pd.DataFrame, metric: str, out_path: Path) -> None:
    richness = sorted(df["n_species"].unique())
    ncols = len(richness)
    fig, axes = plt.subplots(1, ncols, figsize=(4 * ncols, 4), constrained_layout=True)
    if ncols == 1:
        axes = [axes]
    for ax, s in zip(axes, richness):
        table = pivot_metric(df, metric, s)
        im = ax.imshow(table.values, origin="lower", aspect="auto", cmap="viridis")
        ax.set_title(f"{metric} (S={s})")
        ax.set_xlabel(r"$\sigma_{\mathrm{env}}$")
        ax.set_ylabel(r"$\rho_{\mathrm{env}}$")
        ax.set_xticks(range(len(table.columns)))
        ax.set_xticklabels([f"{c:.1f}" for c in table.columns])
        ax.set_yticks(range(len(table.index)))
        ax.set_yticklabels([f"{r:.1f}" for r in table.index])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    df = pd.read_parquet(args.input)
    df = ensure_effective_rho(df)
    if "slope_mode" not in df.columns:
        df = df.copy()
        df["slope_mode"] = "mixed"

    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    summary_path = Path(f"{out_prefix}_summary.csv")
    summary = (
        df.groupby(["slope_mode", "n_species", "sigma_env", "rho_env", "rho_eff", "phi"])
        [["cv_total", "phi_ldm", "mean_pairwise_corr"]]
        .mean()
        .reset_index()
    )
    # Effective stationary environmental SD for AR(1) with innovation SD sigma_env
    summary["sigma_eff"] = summary["sigma_env"] / (1.0 - summary["phi"] ** 2) ** 0.5
    summary.to_csv(summary_path, index=False)

    plot_heatmaps(summary, "cv_total", Path(f"{out_prefix}_cv.png"))
    plot_heatmaps(summary, "phi_ldm", Path(f"{out_prefix}_phi.png"))
    print(f"Wrote summary CSV and figures to {out_prefix.parent}")


if __name__ == "__main__":
    main()
