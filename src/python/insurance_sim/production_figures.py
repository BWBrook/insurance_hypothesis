"""Production-scale figure helpers for the insurance-hypothesis manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def load_fig1_production_runs(core_path: Path, highsigma_path: Path) -> pd.DataFrame:
    """Load and combine the core and high-sigma S=4 production summaries."""
    missing = [str(path) for path in (core_path, highsigma_path) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing production summary file(s): "
            + ", ".join(missing)
            + ". Retrieve compact production outputs before rebuilding this figure."
        )
    return pd.concat(
        [pd.read_parquet(core_path), pd.read_parquet(highsigma_path)],
        ignore_index=True,
    )


def summarize_fig1_production(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate replicate-level production rows to scenario means."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_env",
        "rho_eff",
        "cv_total",
        "mean_extinction_freq",
        "phi_ldm",
        "mean_pairwise_corr",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    summary = (
        df.groupby(["slope_mode", "sigma_env", "rho_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            cv_total_mean=("cv_total", "mean"),
            cv_total_sd=("cv_total", "std"),
            extinction_mean=("mean_extinction_freq", "mean"),
            extinction_max=("mean_extinction_freq", "max"),
            phi_ldm_mean=("phi_ldm", "mean"),
            pair_corr_mean=("mean_pairwise_corr", "mean"),
        )
        .reset_index(drop=True)
    )
    return pd.DataFrame(summary)


def _pivot_mode(summary: pd.DataFrame, slope_mode: str, metric: str) -> pd.DataFrame:
    sigmas = sorted(summary["sigma_env"].unique())
    rhos = sorted(summary["rho_eff"].unique())
    table = summary[summary["slope_mode"].eq(slope_mode)].pivot_table(
        index="rho_eff",
        columns="sigma_env",
        values=metric,
        aggfunc="mean",
    )
    return table.reindex(index=rhos, columns=sigmas)


def _label_heatmap_axes(ax: Axes, sigmas: list[float], rhos: list[float]) -> None:
    ax.set_xlabel(r"Environmental variability, $\sigma_{\mathrm{env}}$")
    ax.set_ylabel(r"Effective driver correlation, $\rho_{\mathrm{eff}}$")
    ax.set_xticks(range(len(sigmas)))
    ax.set_xticklabels(
        [f"{value:g}" if i % 2 == 0 or value in {3.5, 4.0} else "" for i, value in enumerate(sigmas)],
        rotation=45,
        ha="right",
        fontsize=8,
    )
    ax.set_yticks(range(len(rhos)))
    ax.set_yticklabels([f"{value:.2g}" for value in rhos], fontsize=8)


def _mean_cv_by_sigma(summary: pd.DataFrame) -> pd.DataFrame:
    mean_cv = (
        summary.groupby(["slope_mode", "sigma_env"], as_index=False, observed=True)
        .agg(
            cv_mean=("cv_total_mean", "mean"),
            cv_min=("cv_total_mean", "min"),
            cv_max=("cv_total_mean", "max"),
            extinction_mean=("extinction_mean", "mean"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(mean_cv)
    out = out.sort_values("sigma_env").sort_values("slope_mode", kind="stable")
    return out.reset_index(drop=True)


def _add_panel_label(ax: Axes, label: str) -> None:
    ax.text(
        -0.09,
        1.05,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def _load_required_parquet(path: Path, *, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {label} production summary file: {path}. "
            "Retrieve compact production outputs before rebuilding this figure."
        )
    return pd.read_parquet(path)


def make_production_fig1(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write the promoted production Figure 1.

    The figure intentionally emphasises (a) the aligned positive-slope response
    surface and (b) the divergence between aligned and mixed responses across
    the environmental-variability gradient. The full mixed-slope heatmap is
    better suited to supplementary diagnostics because its rho-axis structure is
    weak relative to the sigma effect.
    """
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    sigmas = sorted(summary["sigma_env"].unique())
    rhos = sorted(summary["rho_eff"].unique())
    pos_cv = _pivot_mode(summary, "positive", "cv_total_mean")
    vmax = float(np.nanmax(pos_cv.values))

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12.5, 5.4),
        gridspec_kw={"width_ratios": [1.05, 1.1]},
        constrained_layout=True,
    )

    ax_surface = axes[0]
    image = ax_surface.imshow(
        pos_cv.values,
        origin="lower",
        aspect="auto",
        cmap="magma",
        vmin=0.0,
        vmax=vmax,
    )
    ax_surface.set_title("Aligned responses: community variability")
    _label_heatmap_axes(ax_surface, sigmas, rhos)
    if 2.0 in sigmas:
        ax_surface.axvline(sigmas.index(2.0), color="white", lw=1.2, ls=":", alpha=0.9)
    cbar = fig.colorbar(image, ax=ax_surface, fraction=0.046, pad=0.03)
    cbar.set_label(r"Mean $\mathrm{CV}_{\mathrm{tot}}$")
    _add_panel_label(ax_surface, "A")

    ax_gradient = axes[1]
    mean_cv = _mean_cv_by_sigma(summary)
    colors = {"mixed": "#1f77b4", "positive": "#d95f02"}
    labels = {"mixed": "mixed responses", "positive": "aligned responses"}
    for slope_mode, linestyle in [("mixed", "-"), ("positive", "--")]:
        sub = mean_cv[mean_cv["slope_mode"].eq(slope_mode)]
        x = np.asarray(sub["sigma_env"], dtype=float)
        y = np.asarray(sub["cv_mean"], dtype=float)
        ymin = np.asarray(sub["cv_min"], dtype=float)
        ymax = np.asarray(sub["cv_max"], dtype=float)
        color = colors[slope_mode]
        ax_gradient.fill_between(x, ymin, ymax, color=color, alpha=0.12, linewidth=0)
        ax_gradient.plot(
            x,
            y,
            linestyle,
            marker="o",
            lw=2.2,
            ms=4.5,
            color=color,
            label=labels[slope_mode],
        )

    wide_cv = mean_cv.pivot(index="sigma_env", columns="slope_mode", values="cv_mean")
    gap = wide_cv["positive"] - wide_cv["mixed"]
    ax_gradient.plot(
        gap.index.to_numpy(dtype=float),
        gap.to_numpy(dtype=float),
        color="0.25",
        lw=1.9,
        marker="s",
        ms=3.5,
        alpha=0.85,
        label="aligned - mixed gap",
    )

    ax_gradient.axvline(2.0, color="0.35", lw=1.1, ls=":")
    ax_gradient.axvspan(3.0, max(sigmas), color="#8c2d04", alpha=0.08, lw=0)
    ax_gradient.text(
        max(sigmas) - 0.08,
        5.0,
        "stress\nextension",
        color="#8c2d04",
        fontsize=8,
        ha="right",
        va="center",
    )
    ax_gradient.set(
        title="Insurance contrast across environmental variability",
        xlabel=r"Environmental variability, $\sigma_{\mathrm{env}}$",
        ylabel=r"Mean $\mathrm{CV}_{\mathrm{tot}}$ across $\rho_{\mathrm{eff}}$",
    )
    ax_gradient.set_xlim(min(sigmas) - 0.05, max(sigmas) + 0.05)
    ax_gradient.legend(loc="upper left", fontsize=8, frameon=True)
    _add_panel_label(ax_gradient, "B")

    fig.suptitle("Figure 1: aligned variability and biodiversity insurance", fontsize=12)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig1(
    *,
    core_path: Path,
    highsigma_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Load production outputs and write the promoted Figure 1."""
    df = load_fig1_production_runs(core_path, highsigma_path)
    summary = summarize_fig1_production(df)
    make_production_fig1(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


def summarize_fig2_richness_production(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mixed-slope production rows for the richness-scaling figure."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_env",
        "rho_eff",
        "n_species",
        "cv_total",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    mixed = df[df["slope_mode"].eq("mixed") & (df["rho_eff"] >= -1e-12)].copy()
    if mixed.empty:
        raise ValueError("No mixed-slope rows with non-negative rho_eff were found.")

    scenario_means = (
        mixed.groupby(["sigma_env", "rho_eff", "n_species"], as_index=False, observed=True)
        .agg(
            cv_total_mean=("cv_total", "mean"),
            extinction_mean=("mean_extinction_freq", "mean"),
        )
        .reset_index(drop=True)
    )
    richness = (
        scenario_means.groupby(["sigma_env", "n_species"], as_index=False, observed=True)
        .agg(
            cv_mean=("cv_total_mean", "mean"),
            cv_min=("cv_total_mean", "min"),
            cv_max=("cv_total_mean", "max"),
            extinction_mean=("extinction_mean", "mean"),
            extinction_max=("extinction_mean", "max"),
            rho_count=("rho_eff", "nunique"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(richness)
    return out.sort_values(["sigma_env", "n_species"]).reset_index(drop=True)


def make_production_fig2_richness(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production Figure 2: mixed-slope richness buffering."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    sigmas = sorted(float(value) for value in summary["sigma_env"].unique())
    colors = plt.get_cmap("viridis")(np.linspace(0.12, 0.88, len(sigmas)))

    fig, ax = plt.subplots(figsize=(7.0, 4.8), constrained_layout=True)
    for sigma_val, color in zip(sigmas, colors):
        sub = pd.DataFrame(summary[summary["sigma_env"].eq(sigma_val)].copy())
        sub = sub.iloc[np.argsort(np.asarray(sub["n_species"], dtype=int))].reset_index(drop=True)
        x = np.asarray(sub["n_species"], dtype=float)
        y = np.asarray(sub["cv_mean"], dtype=float)
        ymin = np.asarray(sub["cv_min"], dtype=float)
        ymax = np.asarray(sub["cv_max"], dtype=float)
        if sigma_val > 0:
            ax.fill_between(x, ymin, ymax, color=color, alpha=0.10, linewidth=0)
        ax.plot(
            x,
            y,
            marker="o",
            lw=2.0,
            ms=4.5,
            color=color,
            label=f"{sigma_val:g}",
        )

    ax.set(
        title="Richness buffers community variability under mixed responses",
        xlabel=r"Species richness, $S$",
        ylabel=r"Mean $\mathrm{CV}_{\mathrm{tot}}$ across non-negative $\rho_{\mathrm{eff}}$",
        xticks=sorted(int(value) for value in summary["n_species"].unique()),
    )
    ax.legend(title=r"$\sigma_{\mathrm{env}}$", fontsize=8, title_fontsize=9, frameon=False)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig2_richness(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Load production richness outputs and write Figure 2."""
    df = _load_required_parquet(production_path, label="Figure 2 richness")
    summary = summarize_fig2_richness_production(df)
    make_production_fig2_richness(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )
