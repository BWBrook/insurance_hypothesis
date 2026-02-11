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

from matplotlib.image import AxesImage
import matplotlib.pyplot as plt
import numpy as np
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
    "pos_matched": {
        "args": ["--reps", "100", "--slope-mode", "positive_matched", "--species-list", "4,8"],
        "desc": "Magnitude-matched aligned slopes control",
        "path": Path("data/sim/grid/pos_matched/summaries.parquet"),
    },
    "phi0_reduced": {
        "args": [
            "--reps",
            "80",
            "--phi",
            "0.0",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ],
        "desc": "No persistence sensitivity (φ=0.0)",
        "path": Path("data/sim/grid/phi0_reduced/summaries.parquet"),
    },
    "phi07_reduced": {
        "args": [
            "--reps",
            "80",
            "--phi",
            "0.7",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ],
        "desc": "Persistence sensitivity (φ=0.7)",
        "path": Path("data/sim/grid/phi07_reduced/summaries.parquet"),
    },
    "phi09_reduced": {
        "args": [
            "--reps",
            "80",
            "--phi",
            "0.9",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ],
        "desc": "High persistence sensitivity (φ=0.9)",
        "path": Path("data/sim/grid/phi09_reduced/summaries.parquet"),
    },
    "phi095_reduced": {
        "args": [
            "--reps",
            "80",
            "--phi",
            "0.95",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
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
    df = pd.read_parquet(path)
    return ensure_effective_rho(df)


def ensure_effective_rho(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure df has rho_eff and rho_clipped columns.

    Older cached parquet files predate these columns; we reconstruct them from
    (rho_env, n_species) using the equicorrelation PD bounds.
    """
    if "rho_eff" in df.columns:
        if "rho_clipped" not in df.columns and "rho_env" in df.columns:
            out = df.copy()
            out["rho_clipped"] = (out["rho_eff"] - out["rho_env"]).abs() > 1e-12
            return out
        return df

    if "rho_env" not in df.columns or "n_species" not in df.columns:
        raise ValueError("Cannot reconstruct rho_eff without rho_env and n_species columns.")

    out = df.copy()
    eps = 1e-6

    rho_env = out["rho_env"].to_numpy(dtype=float)
    n_species = out["n_species"].to_numpy(dtype=int)
    rho_eff = rho_env.copy()

    mask = n_species >= 2
    if np.any(mask):
        min_rho = (-1.0 / (n_species[mask] - 1)) + eps
        max_rho = 1.0 - eps
        rho_eff[mask] = np.clip(rho_env[mask], min_rho, max_rho)

    out["rho_eff"] = rho_eff
    out["rho_clipped"] = np.abs(rho_eff - rho_env) > 1e-12
    return out


def sort_by_rho_eff(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy sorted by rho_eff with a clean index.

    Using an explicit numpy-based sort avoids pandas type-stub ambiguity in
    static analysis while keeping runtime behaviour identical.
    """
    order = np.argsort(np.asarray(df["rho_eff"], dtype=float))
    return df.iloc[order].reset_index(drop=True)


def ensure_reports(summary_df: pd.DataFrame, out_prefix: Path) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    summary_df = ensure_effective_rho(summary_df)
    metric_labels = {
        "cv_total": r"$\mathrm{CV}_{\mathrm{tot}}$",
        "phi_ldm": r"$\phi_{\mathrm{LdM}}$",
    }
    # Heatmaps of CV and phi_ldm per richness
    for metric in ["cv_total", "phi_ldm"]:
        richness = sorted(summary_df["n_species"].unique())
        metric_label = metric_labels.get(metric, metric)
        tables: dict[int, pd.DataFrame] = {}
        for s in richness:
            table = summary_df[summary_df["n_species"] == s].pivot_table(
                index="rho_eff", columns="sigma_env", values=metric, aggfunc="mean"
            )
            tables[s] = table
        vmin_shared = float(np.nanmin([np.nanmin(t.values) for t in tables.values()]))
        vmax_shared = float(np.nanmax([np.nanmax(t.values) for t in tables.values()]))
        ncols = len(richness)
        fig, axes = plt.subplots(1, ncols, figsize=(4 * ncols, 4), constrained_layout=True)
        if ncols == 1:
            axes_list = [axes]
        else:
            axes_list = list(np.ravel(axes))
        im: AxesImage | None = None
        for i, (ax, s) in enumerate(zip(axes_list, richness)):
            table = tables[s]
            im = ax.imshow(
                table.values,
                origin="lower",
                aspect="auto",
                cmap="viridis",
                vmin=vmin_shared,
                vmax=vmax_shared,
            )
            ax.set_title(rf"{metric_label} (S={s})")
            ax.set_xlabel(r"$\sigma_{\mathrm{env}}$")
            if i == 0:
                ax.set_ylabel(r"$\rho_{\mathrm{env}}$")
            ax.set_xticks(range(len(table.columns)))
            ax.set_xticklabels([f"{c:.1f}" for c in table.columns])
            ax.set_yticks(range(len(table.index)))
            ax.set_yticklabels([f"{r:.1f}" for r in table.index])
        assert im is not None
        cbar = fig.colorbar(im, ax=axes_list, fraction=0.030, pad=0.04)
        cbar.set_label(metric_label)
        fig.savefig(out_prefix.with_name(out_prefix.name + f"_{metric}.png"), dpi=200)
        plt.close(fig)

    # Save summary CSV
    summary_df.to_csv(out_prefix.with_name(out_prefix.name + "_summary.csv"), index=False)


def make_panel(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    summary_mixed = ensure_effective_rho(summary_mixed)
    summary_pos = ensure_effective_rho(summary_pos)

    # Panel A mixed heatmap S=4
    table = summary_mixed[summary_mixed["n_species"] == 4].pivot_table(
        index="rho_eff", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    # Use a shared color scale across mixed and positive panels for direct magnitude contrast
    table_pos = summary_pos[summary_pos["n_species"] == 4].pivot_table(
        index="rho_eff", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    vmin_shared = float(
        np.nanmin([np.nanmin(table.values), np.nanmin(table_pos.values)])
    )
    vmax_shared = float(
        np.nanmax([np.nanmax(table.values), np.nanmax(table_pos.values)])
    )

    im = axes[0, 0].imshow(
        table.values,
        origin="lower",
        aspect="auto",
        cmap="viridis",
        vmin=vmin_shared,
        vmax=vmax_shared,
    )
    axes[0, 0].set(
        title=r"$\mathrm{CV}_{\mathrm{tot}}$ mixed slopes (S=4)",
        xlabel=r"$\sigma_{\mathrm{env}}$",
        ylabel=r"$\rho_{\mathrm{env}}$",
    )
    axes[0, 0].set_xticks(range(len(table.columns)))
    axes[0, 0].set_xticklabels([f"{c:.1f}" for c in table.columns])
    axes[0, 0].set_yticks(range(len(table.index)))
    axes[0, 0].set_yticklabels([f"{r:.1f}" for r in table.index])
    fig.colorbar(im, ax=axes[0, 0], fraction=0.046, pad=0.04)

    # Panel B positive heatmap S=4
    im2 = axes[0, 1].imshow(
        table_pos.values,
        origin="lower",
        aspect="auto",
        cmap="viridis",
        vmin=vmin_shared,
        vmax=vmax_shared,
    )
    axes[0, 1].set(
        title=r"$\mathrm{CV}_{\mathrm{tot}}$ positive slopes (S=4)",
        xlabel=r"$\sigma_{\mathrm{env}}$",
        ylabel=r"$\rho_{\mathrm{env}}$",
    )
    axes[0, 1].set_xticks(range(len(table_pos.columns)))
    axes[0, 1].set_xticklabels([f"{c:.1f}" for c in table_pos.columns])
    axes[0, 1].set_yticks(range(len(table_pos.index)))
    axes[0, 1].set_yticklabels([f"{r:.1f}" for r in table_pos.index])
    fig.colorbar(im2, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # Panel C CV lines sigma=0.5
    sigma_target = 0.5
    ax = axes[1, 0]
    for s, marker in [(4, "o"), (8, "s")]:
        m_rep = summary_mixed[
            (summary_mixed["sigma_env"] == sigma_target) & (summary_mixed["n_species"] == s)
        ]
        p_rep = summary_pos[
            (summary_pos["sigma_env"] == sigma_target) & (summary_pos["n_species"] == s)
        ]
        m_slice = summary_mixed[
            (summary_mixed["sigma_env"] == sigma_target) & (summary_mixed["n_species"] == s)
        ].groupby("rho_eff", as_index=False, observed=True).agg(cv_total=("cv_total", "mean"))
        p_slice = summary_pos[
            (summary_pos["sigma_env"] == sigma_target) & (summary_pos["n_species"] == s)
        ].groupby("rho_eff", as_index=False, observed=True).agg(cv_total=("cv_total", "mean"))
        m_slice = sort_by_rho_eff(pd.DataFrame(m_slice))
        p_slice = sort_by_rho_eff(pd.DataFrame(p_slice))
        m_line = ax.plot(m_slice["rho_eff"], m_slice["cv_total"], marker=marker, label=f"mixed S={s}")[0]
        p_line = ax.plot(
            p_slice["rho_eff"],
            p_slice["cv_total"],
            marker=marker,
            linestyle="--",
            label=f"positive S={s}",
        )[0]
        # Overlay replicate-level points so points=replicates, lines=scenario means.
        ax.scatter(
            m_rep["rho_eff"],
            m_rep["cv_total"],
            s=10,
            alpha=0.15,
            color=m_line.get_color(),
            marker=marker,
            edgecolors="none",
            label="_nolegend_",
            zorder=1,
        )
        ax.scatter(
            p_rep["rho_eff"],
            p_rep["cv_total"],
            s=10,
            alpha=0.15,
            color=p_line.get_color(),
            marker=marker,
            edgecolors="none",
            label="_nolegend_",
            zorder=1,
        )
    ax.set(
        title=rf"$\mathrm{{CV}}_{{\mathrm{{tot}}}}$ vs $\rho_{{\mathrm{{env}}}}$ ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel=r"$\mathrm{CV}_{\mathrm{tot}}$",
    )
    ax.legend(fontsize=8)

    # Panel D imposed vs realised synchrony
    ax = axes[1, 1]
    mixed_scatter = (
        summary_mixed.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False)["mean_pairwise_corr"]
        .mean()
        .dropna()
    )
    pos_scatter = (
        summary_pos.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False)["mean_pairwise_corr"]
        .mean()
        .dropna()
    )
    ax.scatter(mixed_scatter["rho_eff"], mixed_scatter["mean_pairwise_corr"], s=20, alpha=0.5, label="mixed")
    ax.scatter(pos_scatter["rho_eff"], pos_scatter["mean_pairwise_corr"], s=20, alpha=0.5, label="positive")
    ax.axline((0, 0), (1, 1), color="k", linestyle="--", linewidth=0.8, label="y=x")
    ax.set(
        title="Imposed vs realised synchrony",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Realised growth corr",
    )
    ax.legend()

    # Add panel labels A–D (matching manuscript text Fig. 1A–D)
    for label, ax in zip(["A", "B", "C", "D"], axes.flatten()):
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=14,
            fontweight="bold",
            va="top",
            ha="left",
        )

    fig.suptitle("Insurance simulations: mixed vs aligned responses", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_path, dpi=250)
    # Also emit a vector version for manuscripts/slides.
    if out_path.suffix.lower() == ".png":
        fig.savefig(out_path.with_suffix(".pdf"))
    plt.close(fig)


def make_synchrony_panels(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    """Panels separating imposed vs realised synchrony by slope mode and delta."""
    sigma_target = 0.5
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)
    summary_mixed = ensure_effective_rho(summary_mixed)
    summary_pos = ensure_effective_rho(summary_pos)

    # Helper to build mean curves at sigma_target
    def mean_sync(df: pd.DataFrame) -> pd.DataFrame:
        sub = df[df["sigma_env"] == sigma_target]
        grp = (
            sub.groupby(["n_species", "rho_eff"])[["mean_pairwise_corr"]]
            .mean()
            .reset_index()
        )
        grp["delta_corr"] = grp["mean_pairwise_corr"] - grp["rho_eff"]
        return grp

    mixed_mean = mean_sync(summary_mixed)
    pos_mean = mean_sync(summary_pos)

    # Panel A: mixed slopes
    ax = axes[0]
    for s, group in mixed_mean.groupby("n_species"):
        ax.plot(
            group["rho_eff"],
            group["mean_pairwise_corr"],
            marker="o",
            label=f"S={s}",
        )
    ax.plot([-0.5, 1.0], [-0.5, 1.0], "k--", lw=0.8, label="y=x")
    ax.set(
        title=rf"Mixed slopes ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"Imposed driver correlation $\rho_{\mathrm{env}}$",
        ylabel="Realised growth corr",
    )
    ax.legend(fontsize=8)

    # Panel B: positive slopes
    ax = axes[1]
    for s, group in pos_mean.groupby("n_species"):
        ax.plot(
            group["rho_eff"],
            group["mean_pairwise_corr"],
            marker="s",
            label=f"S={s}",
        )
    ax.plot([-0.5, 1.0], [-0.5, 1.0], "k--", lw=0.8, label="y=x")
    ax.set(
        title=rf"Positive slopes ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"Imposed driver correlation $\rho_{\mathrm{env}}$",
        ylabel="Realised growth corr",
    )
    ax.legend(fontsize=8)

    # Panel C: delta_corr by rho_env
    ax = axes[2]
    for label, df_mean, marker in [
        ("mixed", mixed_mean, "o"),
        ("positive", pos_mean, "s"),
    ]:
        # Collapse across richness to one regime-level curve per slope mode.
        regime_mean = sort_by_rho_eff(
            pd.DataFrame(df_mean.groupby("rho_eff", as_index=False)[["delta_corr"]].mean())
        )
        ax.plot(
            regime_mean["rho_eff"],
            regime_mean["delta_corr"],
            marker=marker,
            label=label,
        )
    ax.axhline(0, color="k", lw=0.8, ls="--")
    ax.set(
        title="Realised − imposed correlation",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Δcorr",
    )
    ax.legend(fontsize=8)

    # Add panel labels A–C (left to right) to match manuscript references
    for label, ax in zip(["A", "B", "C"], axes):
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=14,
            fontweight="bold",
            va="top",
            ha="left",
        )

    fig.suptitle("Imposed vs realised synchrony", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_cv_vs_synchrony(summary_mixed: pd.DataFrame, out_path: Path) -> None:
    """Scatter of CV_total vs synchrony metrics for mixed slopes."""
    # Aggregate by scenario to reduce overplotting
    summary_mixed = ensure_effective_rho(summary_mixed)
    grp = (
        summary_mixed.groupby(["n_species", "sigma_env", "rho_eff"])[
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
    ax.set_xlabel(r"Synchrony $\phi_{\mathrm{LdM}}$")
    ax.set_ylabel(r"$\mathrm{CV}_{\mathrm{tot}}$")
    ax.set_title(r"$\mathrm{CV}_{\mathrm{tot}}$ vs $\phi_{\mathrm{LdM}}$ (mixed slopes)")
    # Move legend slightly down to avoid clash with panel label
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.9))

    # CV vs mean pairwise growth corr
    ax = axes[1]
    for s, sub in grp.groupby("n_species"):
        ax.scatter(sub["mean_pairwise_corr"], sub["cv_total"], s=25, alpha=0.6, label=f"S={s}")
    ax.set_xlabel("Mean pairwise growth corr")
    ax.set_title(r"$\mathrm{CV}_{\mathrm{tot}}$ vs realised growth corr (mixed slopes)")

    # Add panel labels A–B (left to right)
    for label, ax in zip(["A", "B"], axes):
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=14,
            fontweight="bold",
            va="top",
            ha="left",
        )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_phi_overlay(phi_runs: dict[str, pd.DataFrame], out_path: Path, sigma_target: float = 0.5) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    markers = ["s", "^", "v", "d"]
    for idx, s in enumerate([2, 4]):
        ax = axes[idx]
        for (key, df), marker in zip(phi_runs.items(), markers):
            df = ensure_effective_rho(df)
            sub = df[(df["sigma_env"] == sigma_target) & (df["n_species"] == s)]
            if sub.empty:
                continue
            sub_mean = (
                sub.groupby("rho_eff", as_index=False, observed=True)
                .agg(cv_total=("cv_total", "mean"))
            )
            sub_mean = sort_by_rho_eff(pd.DataFrame(sub_mean))
            phi_val = float(np.asarray(sub["phi"], dtype=float)[0])
            sigma_eff = sigma_target / (1.0 - phi_val**2) ** 0.5
            label = f"{phi_val:g} (~{sigma_eff:.2f})"
            line = ax.plot(sub_mean["rho_eff"], sub_mean["cv_total"], marker=marker, label=label)[0]
            # Overlay replicate values (faint) so points=replicates and lines=means.
            ax.scatter(
                sub["rho_eff"],
                sub["cv_total"],
                s=10,
                alpha=0.12,
                color=line.get_color(),
                marker=marker,
                edgecolors="none",
                label="_nolegend_",
                zorder=1,
            )
        ax.set(
            title=f"S={s}",
            xlabel=r"$\rho_{\mathrm{env}}$",
            xlim=(-0.5, 1.0),
        )
        if idx == 0:
            ax.set_ylabel(r"$\mathrm{CV}_{\mathrm{tot}}$")
            ax.legend(
                fontsize=8,
                title=r"$\phi$ ($\sigma_{\mathrm{eff}}$)",
                title_fontsize=9,
            )
    fig.suptitle(
        rf"$\mathrm{{CV}}_{{\mathrm{{tot}}}}$ versus $\rho_{{\mathrm{{env}}}}$ at $\sigma_{{\mathrm{{env}}}}={sigma_target}$ across $\phi$ (mixed slopes)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_richness_scaling(summary_mixed: pd.DataFrame, out_path: Path) -> None:
    """Plot mean community CV vs richness for mixed slopes.

    The curve averages CV_total over imposed driver correlations ρ_env for each σ_env.

    Note: under an equicorrelation structure, strongly negative correlations become
    infeasible as richness increases (rho must exceed -1/(S-1)). To keep the averaging
    comparable across richness, we average over the shared non-negative subset
    (ρ_env >= 0) by default.
    """
    summary_mixed = ensure_effective_rho(summary_mixed)
    if "rho_env" in summary_mixed.columns:
        summary_mixed = summary_mixed.query("rho_env >= 0").copy()

    grp = (
        summary_mixed.groupby(["sigma_env", "n_species"])["cv_total"]
        .mean()
        .reset_index()
        .sort_values(by=["sigma_env", "n_species"])
    )

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for sigma_val, sub in grp.groupby("sigma_env"):
        sigma_val_f = float(np.asarray(sigma_val, dtype=float).item())
        ax.plot(
            sub["n_species"],
            sub["cv_total"],
            marker="o",
            lw=1.6,
            label=f"{sigma_val_f:.1f}",
        )

    ax.set_xlabel(r"Species richness $S$")
    ax.set_ylabel(r"Mean $\mathrm{CV}_{\mathrm{tot}}$ across $\rho_{\mathrm{env}}$")
    ax.set_title(r"Richness stabilises community biomass (mixed slopes)")
    ax.legend(title=r"$\sigma_{\mathrm{env}}$", fontsize=8, title_fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_positive_matched_control(
    summary_mixed: pd.DataFrame,
    summary_pos: pd.DataFrame,
    summary_pos_matched: pd.DataFrame,
    out_path: Path,
    *,
    sigma_target: float = 0.5,
) -> None:
    """Control plot: aligned slopes with matched magnitudes vs mixed slopes.

    This isolates the effect of *sign alignment* from the overall forcing magnitude
    of the slope distribution.
    """
    summary_mixed = ensure_effective_rho(summary_mixed)
    summary_pos = ensure_effective_rho(summary_pos)
    summary_pos_matched = ensure_effective_rho(summary_pos_matched)

    def scenario_means(df: pd.DataFrame, n_species: int) -> pd.DataFrame:
        sub = df[(df["sigma_env"] == sigma_target) & (df["n_species"] == n_species)]
        out = (
            sub.groupby("rho_eff", as_index=False)[["cv_total", "mean_pairwise_corr"]]
            .mean()
        )
        return sort_by_rho_eff(pd.DataFrame(out))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharex=True)

    # Panel A: CV_total vs rho
    ax = axes[0]
    for s, marker in [(4, "o"), (8, "s")]:
        mixed = scenario_means(summary_mixed, n_species=s)
        pos = scenario_means(summary_pos, n_species=s)
        pos_matched = scenario_means(summary_pos_matched, n_species=s)

        ax.plot(mixed["rho_eff"], mixed["cv_total"], marker=marker, label=f"mixed S={s}")
        ax.plot(pos_matched["rho_eff"], pos_matched["cv_total"], marker=marker, ls=":", label=f"pos-matched S={s}")
        ax.plot(pos["rho_eff"], pos["cv_total"], marker=marker, ls="--", label=f"positive S={s}")

    ax.set(
        title=rf"$\mathrm{{CV}}_{{\mathrm{{tot}}}}$ vs $\rho_{{\mathrm{{env}}}}$ ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel=r"$\mathrm{CV}_{\mathrm{tot}}$",
    )
    ax.legend(fontsize=8, ncol=2)

    # Panel B: realised growth correlation vs rho
    ax = axes[1]
    for s, marker in [(4, "o"), (8, "s")]:
        mixed = scenario_means(summary_mixed, n_species=s)
        pos = scenario_means(summary_pos, n_species=s)
        pos_matched = scenario_means(summary_pos_matched, n_species=s)

        ax.plot(mixed["rho_eff"], mixed["mean_pairwise_corr"], marker=marker, label=f"mixed S={s}")
        ax.plot(
            pos_matched["rho_eff"],
            pos_matched["mean_pairwise_corr"],
            marker=marker,
            ls=":",
            label=f"pos-matched S={s}",
        )
        ax.plot(pos["rho_eff"], pos["mean_pairwise_corr"], marker=marker, ls="--", label=f"positive S={s}")

    ax.plot([-0.5, 1.0], [-0.5, 1.0], "k--", lw=0.8, label="y=x")
    ax.set(
        title=rf"Realised growth corr vs $\rho_{{\mathrm{{env}}}}$ ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Realised growth corr",
    )
    ax.legend(fontsize=8, ncol=2)

    # Add panel labels
    for label, ax in zip(["A", "B"], axes):
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=14,
            fontweight="bold",
            va="top",
            ha="left",
        )

    fig.suptitle("Magnitude-matched aligned-slope control", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
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
    summary_pos_matched = load_summary("pos_matched") if DATA_RUNS["pos_matched"]["path"].exists() else None
    phi_runs = {
        "phi0_reduced": pd.read_parquet("data/sim/grid/phi0_reduced/summaries.parquet"),
        "phi07_reduced": pd.read_parquet("data/sim/grid/phi07_reduced/summaries.parquet"),
        "phi09_reduced": pd.read_parquet("data/sim/grid/phi09_reduced/summaries.parquet"),
        "phi095_reduced": pd.read_parquet("data/sim/grid/phi095_reduced/summaries.parquet"),
    }

    # Per-run summary figs
    ensure_reports(summary_mixed, REPORTS / "run1")
    ensure_reports(summary_pos, REPORTS / "pos_full")
    if summary_pos_matched is not None:
        ensure_reports(summary_pos_matched, REPORTS / "pos_matched")
    for key, df in phi_runs.items():
        ensure_reports(df, REPORTS / key)

    # Panels
    panel_path = REPORTS / "fig1_panels.png"
    make_panel(summary_mixed, summary_pos, panel_path)
    panel_pdf_path = panel_path.with_suffix(".pdf")

    sync_panel_path = REPORTS / "fig3_imposed_vs_realised_panels.png"
    make_synchrony_panels(summary_mixed, summary_pos, sync_panel_path)

    phi_overlay_path = REPORTS / "fig5_phi_sensitivity_sigma0.5_extended.png"
    make_phi_overlay(phi_runs, phi_overlay_path)

    cv_sync_path = REPORTS / "fig4_cv_vs_synchrony_mixed.png"
    make_cv_vs_synchrony(summary_mixed, cv_sync_path)

    # Richness scaling curve (prefer dedicated richness sweep if available)
    richness_path = Path("data/sim/grid/run1_richness/summaries.parquet")
    if richness_path.exists():
        richness_df = pd.read_parquet(richness_path)
    else:
        richness_df = summary_mixed
    richness_fig_path = REPORTS / "fig2_richness_scaling_mixed.png"
    make_richness_scaling(richness_df, richness_fig_path)

    # Promote mixed-grid heatmaps to supplementary figure names.
    supp_cv_src = REPORTS / "run1_cv_total.png"
    supp_phi_src = REPORTS / "run1_phi_ldm.png"
    supp_cv_path = REPORTS / "figS1_run1_cv_total.png"
    supp_phi_path = REPORTS / "figS2_run1_phi_ldm.png"
    if supp_cv_src.exists():
        supp_cv_path.write_bytes(supp_cv_src.read_bytes())
        supp_cv_src.unlink()
    if supp_phi_src.exists():
        supp_phi_path.write_bytes(supp_phi_src.read_bytes())
        supp_phi_src.unlink()

    # Magnitude-matched aligned-slope control (if available)
    matched_path: Path | None = None
    if summary_pos_matched is not None:
        matched_path = REPORTS / "figS3_positive_matched_control.png"
        make_positive_matched_control(summary_mixed, summary_pos, summary_pos_matched, matched_path)

    # Copy key panels to manuscript/figures
    figure_paths = [
        panel_path,
        panel_pdf_path,
        sync_panel_path,
        cv_sync_path,
        phi_overlay_path,
        supp_cv_path,
        supp_phi_path,
        richness_fig_path,
    ]
    if matched_path is not None:
        figure_paths.append(matched_path)
    copy_figures(figure_paths)

    # Remove stale supplementary filenames after transition to figS* names.
    for legacy in [
        FIG_DIR / "run1_cv_total.png",
        FIG_DIR / "run1_phi_ldm.png",
        REPORTS / "positive_matched_control.png",
        FIG_DIR / "positive_matched_control.png",
    ]:
        if legacy.exists():
            legacy.unlink()
            print(f"Removed legacy figure {legacy}")

    print("Run complete. Figures in analysis/reports and manuscript/figures.")


if __name__ == "__main__":
    main()
