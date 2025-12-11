"""End-to-end runner for the insurance hypothesis simulations and figures.

Default behaviour (no flags):
- Uses existing simulation outputs under data/sim/grid/ (run1, pos_full, phi0/07/09/095_reduced).
- Regenerates summary tables and figures into analysis/reports/.
- Copies key panels into manuscript/figures/.

Optional: rerun simulations with `--rerun-data`, which will rerun a smaller set
of grids with the same configurations used in the paper. This is slower
(several minutes).
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_RUNS = {
    "run1": {
        "args": ["--reps", "150"],
        "slope_mode": "mixed",
        "desc": "Mixed slopes main grid",
        "path": Path("data/sim/grid/run1/summaries.parquet"),
    },
    "pos_full": {
        "args": ["--reps", "100", "--slope-mode", "positive", "--species-list", "4,8"],
        "desc": "Positive slopes grid",
        "path": Path("data/sim/grid/pos_full/summaries.parquet"),
    },
    "phi095_reduced": {
        "args": [
            "--reps",
            "80",
            "--phi",
            "0.95",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list",
            "-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
        ],
        "desc": "High persistence sensitivity (φ=0.95)",
        "path": Path("data/sim/grid/phi095_reduced/summaries.parquet"),
    },
}

REPORTS = Path("analysis/reports")
FIG_DIR = Path("manuscript/figures")


def run_command(cmd: list[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def rerun_data() -> None:
    for name, cfg in DATA_RUNS.items():
        args = ["python", "analysis/run_full_grid.py", "--run-name", name] + cfg["args"]
        run_command(["uv", "run"] + args)


def load_summary(run_name: str) -> pd.DataFrame:
    path = DATA_RUNS[run_name]["path"]
    return pd.read_parquet(path)


def ensure_reports(summary_df: pd.DataFrame, out_prefix: Path) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    # Heatmaps of CV and phi_ldm per richness
    for metric in ["cv_total", "phi_ldm"]:
        richness = sorted(summary_df["n_species"].unique())
        ncols = len(richness)
        fig, axes = plt.subplots(1, ncols, figsize=(4 * ncols, 4), constrained_layout=True)
        if ncols == 1:
            axes = [axes]
        for ax, s in zip(axes, richness):
            table = summary_df[summary_df["n_species"] == s].pivot_table(
                index="rho_env", columns="sigma_env", values=metric, aggfunc="mean"
            )
            im = ax.imshow(table.values, origin="lower", aspect="auto", cmap="viridis")
            ax.set_title(f"{metric} (S={s})")
            ax.set_xlabel("sigma_env")
            ax.set_ylabel("rho_env")
            ax.set_xticks(range(len(table.columns)))
            ax.set_xticklabels([f"{c:.1f}" for c in table.columns])
            ax.set_yticks(range(len(table.index)))
            ax.set_yticklabels([f"{r:.1f}" for r in table.index])
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.savefig(out_prefix.with_name(out_prefix.name + f"_{metric}.png"), dpi=200)
        plt.close(fig)

    # Save summary CSV
    summary_df.to_csv(out_prefix.with_name(out_prefix.name + "_summary.csv"), index=False)


def make_panel(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel A mixed heatmap S=4
    table = summary_mixed[summary_mixed["n_species"] == 4].pivot_table(
        index="rho_env", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    im = axes[0, 0].imshow(table.values, origin="lower", aspect="auto", cmap="viridis")
    axes[0, 0].set(title="CV mixed slopes (S=4)", xlabel="sigma_env", ylabel="rho_env")
    axes[0, 0].set_xticks(range(len(table.columns)))
    axes[0, 0].set_xticklabels([f"{c:.1f}" for c in table.columns])
    axes[0, 0].set_yticks(range(len(table.index)))
    axes[0, 0].set_yticklabels([f"{r:.1f}" for r in table.index])
    fig.colorbar(im, ax=axes[0, 0], fraction=0.046, pad=0.04)

    # Panel B positive heatmap S=4
    table_pos = summary_pos[summary_pos["n_species"] == 4].pivot_table(
        index="rho_env", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    im2 = axes[0, 1].imshow(table_pos.values, origin="lower", aspect="auto", cmap="magma")
    axes[0, 1].set(title="CV positive slopes (S=4)", xlabel="sigma_env", ylabel="rho_env")
    axes[0, 1].set_xticks(range(len(table_pos.columns)))
    axes[0, 1].set_xticklabels([f"{c:.1f}" for c in table_pos.columns])
    axes[0, 1].set_yticks(range(len(table_pos.index)))
    axes[0, 1].set_yticklabels([f"{r:.1f}" for r in table_pos.index])
    fig.colorbar(im2, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # Panel C CV lines sigma=0.5
    sigma_target = 0.5
    ax = axes[1, 0]
    for s, marker in [(4, "o"), (8, "s")]:
        m_slice = summary_mixed[(summary_mixed["sigma_env"] == sigma_target) & (summary_mixed["n_species"] == s)]
        p_slice = summary_pos[(summary_pos["sigma_env"] == sigma_target) & (summary_pos["n_species"] == s)]
        ax.plot(m_slice["rho_env"], m_slice["cv_total"], marker=marker, label=f"mixed S={s}")
        ax.plot(p_slice["rho_env"], p_slice["cv_total"], marker=marker, linestyle="--", label=f"positive S={s}")
    ax.set(title=f"CV vs rho (sigma={sigma_target})", xlabel="rho_env", ylabel="CV_total")
    ax.legend(fontsize=8)

    # Panel D imposed vs realised synchrony
    ax = axes[1, 1]
    ax.scatter(summary_mixed["rho_env"], summary_mixed["mean_pairwise_corr"], s=15, alpha=0.4, label="mixed")
    ax.scatter(summary_pos["rho_env"], summary_pos["mean_pairwise_corr"], s=15, alpha=0.4, label="positive")
    ax.axline((0, 0), (1, 1), color="k", linestyle="--", linewidth=0.8, label="y=x")
    ax.set(title="Imposed vs realised synchrony", xlabel="rho_env", ylabel="Realised growth corr")
    ax.legend()

    fig.suptitle("Insurance simulations: mixed vs aligned responses", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=250)
    plt.close(fig)


def make_synchrony_panels(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    """Panels separating imposed vs realised synchrony by slope mode and delta."""
    sigma_target = 0.5
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)

    # Helper to build mean curves at sigma_target
    def mean_sync(df: pd.DataFrame) -> pd.DataFrame:
        sub = df[df["sigma_env"] == sigma_target]
        grp = (
            sub.groupby(["n_species", "rho_env"])[["mean_pairwise_corr"]]
            .mean()
            .reset_index()
        )
        grp["delta_corr"] = grp["mean_pairwise_corr"] - grp["rho_env"]
        return grp

    mixed_mean = mean_sync(summary_mixed)
    pos_mean = mean_sync(summary_pos)

    # Panel A: mixed slopes
    ax = axes[0]
    for s, group in mixed_mean.groupby("n_species"):
        ax.plot(
            group["rho_env"],
            group["mean_pairwise_corr"],
            marker="o",
            label=f"S={s}",
        )
    ax.plot([-0.5, 1.0], [-0.5, 1.0], "k--", lw=0.8, label="y=x")
    ax.set(
        title="Mixed slopes (σ_env=0.5)",
        xlabel="Imposed driver correlation ρ_env",
        ylabel="Realised growth corr",
    )
    ax.legend(fontsize=8)

    # Panel B: positive slopes
    ax = axes[1]
    for s, group in pos_mean.groupby("n_species"):
        ax.plot(
            group["rho_env"],
            group["mean_pairwise_corr"],
            marker="s",
            label=f"S={s}",
        )
    ax.plot([-0.5, 1.0], [-0.5, 1.0], "k--", lw=0.8, label="y=x")
    ax.set(
        title="Positive slopes (σ_env=0.5)",
        xlabel="Imposed driver correlation ρ_env",
        ylabel="Realised growth corr",
    )
    ax.legend(fontsize=8)

    # Panel C: delta_corr by rho_env
    ax = axes[2]
    for label, df_mean, marker in [
        ("mixed", mixed_mean, "o"),
        ("positive", pos_mean, "s"),
    ]:
        ax.plot(
            df_mean["rho_env"],
            df_mean["delta_corr"],
            marker=marker,
            label=label,
        )
    ax.axhline(0, color="k", lw=0.8, ls="--")
    ax.set(
        title="Realised − imposed correlation",
        xlabel="ρ_env",
        ylabel="Δcorr",
    )
    ax.legend(fontsize=8)

    fig.suptitle("Imposed vs realised synchrony", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_cv_vs_synchrony(summary_mixed: pd.DataFrame, out_path: Path) -> None:
    """Scatter of CV_total vs synchrony metrics for mixed slopes."""
    # Aggregate by scenario to reduce overplotting
    grp = (
        summary_mixed.groupby(["n_species", "sigma_env", "rho_env"])[
            ["cv_total", "phi_ldm", "mean_pairwise_corr"]
        ]
        .mean()
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # CV vs phi_LdM
    ax = axes[0]
    for s, sub in grp.groupby("n_species"):
        ax.scatter(sub["phi_ldm"], sub["cv_total"], s=25, alpha=0.6, label=f"S={s}")
    ax.set_xlabel("Synchrony φ_LdM")
    ax.set_ylabel("CV_total")
    ax.set_title("CV vs φ_LdM (mixed slopes)")
    ax.legend(fontsize=8)

    # CV vs mean pairwise growth corr
    ax = axes[1]
    for s, sub in grp.groupby("n_species"):
        ax.scatter(sub["mean_pairwise_corr"], sub["cv_total"], s=25, alpha=0.6, label=f"S={s}")
    ax.set_xlabel("Mean pairwise growth corr")
    ax.set_title("CV vs realised growth corr (mixed slopes)")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_phi_overlay(phi_runs: dict[str, pd.DataFrame], out_path: Path, sigma_target: float = 0.5) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    labels = {
        "phi0_reduced": "φ=0",
        "phi07_reduced": "φ=0.7",
        "phi09_reduced": "φ=0.9",
        "phi095_reduced": "φ=0.95",
    }
    markers = ["s", "^", "v", "d"]
    for idx, s in enumerate([2, 4]):
        ax = axes[idx]
        for (key, df), marker in zip(phi_runs.items(), markers):
            sub = df[(df["sigma_env"] == sigma_target) & (df["n_species"] == s)]
            if sub.empty:
                continue
            phi_val = float(sub["phi"].iloc[0])
            sigma_eff = sigma_target / (1.0 - phi_val**2) ** 0.5
            label = f"{labels.get(key, key)} (σ_eff≈{sigma_eff:.2f})"
            ax.plot(sub["rho_env"], sub["cv_total"], marker=marker, label=label)
        ax.set(title=f"S={s}, sigma={sigma_target}", xlabel="rho_env")
        if idx == 0:
            ax.set_ylabel("CV_total")
        ax.legend(fontsize=8)
    fig.suptitle("CV vs rho across φ (mixed slopes)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def copy_figures(fig_paths: list[Path]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for p in fig_paths:
        if p.exists():
            target = FIG_DIR / p.name
            target.write_bytes(p.read_bytes())
            print(f"Copied {p} -> {target}")
        else:
            print(f"Warning: missing figure {p}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simulations and regenerate figures")
    parser.add_argument("--rerun-data", action="store_true", help="Rerun simulations instead of using cached parquet files")
    args = parser.parse_args()

    if args.rerun_data:
        rerun_data()

    # Load summaries
    summary_mixed = load_summary("run1")
    summary_pos = load_summary("pos_full")
    phi_runs = {
        "phi0_reduced": pd.read_parquet("data/sim/grid/phi0_reduced/summaries.parquet"),
        "phi07_reduced": pd.read_parquet("data/sim/grid/phi07_reduced/summaries.parquet"),
        "phi09_reduced": pd.read_parquet("data/sim/grid/phi09_reduced/summaries.parquet"),
        "phi095_reduced": pd.read_parquet("data/sim/grid/phi095_reduced/summaries.parquet"),
    }

    # Per-run summary figs
    ensure_reports(summary_mixed, REPORTS / "run1")
    ensure_reports(summary_pos, REPORTS / "pos_full")
    for key, df in phi_runs.items():
        ensure_reports(df, REPORTS / key)

    # Panels
    panel_path = REPORTS / "manuscript_panels.png"
    make_panel(summary_mixed, summary_pos, panel_path)

    sync_panel_path = REPORTS / "imposed_vs_realised_panels.png"
    make_synchrony_panels(summary_mixed, summary_pos, sync_panel_path)

    phi_overlay_path = REPORTS / "cv_phi_sensitivity_sigma0.5_extended.png"
    make_phi_overlay(phi_runs, phi_overlay_path)

    cv_sync_path = REPORTS / "cv_vs_synchrony_mixed.png"
    make_cv_vs_synchrony(summary_mixed, cv_sync_path)

    # Copy key panels to manuscript/figures
    copy_figures(
        [
            panel_path,
            sync_panel_path,
            cv_sync_path,
            phi_overlay_path,
            REPORTS / "run1_cv_total.png",
            REPORTS / "run1_phi_ldm.png",
            REPORTS / "cv_richness_scaling_mixed.png",
        ]
    )

    print("Run complete. Figures in analysis/reports and manuscript/figures.")


if __name__ == "__main__":
    main()
