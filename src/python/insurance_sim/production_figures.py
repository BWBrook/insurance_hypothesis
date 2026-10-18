"""Production-scale figure helpers for the insurance-hypothesis manuscript."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

from .diagnostics import (
    balanced_small_noise_coefficient,
    contrast_mode_eigenvalue,
    deterministic_equilibrium,
    equicorrelated_forcing_ratio,
    weighted_alignment_index,
)
from .model import slopes_for_mode


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
    ax.set_ylabel(r"Effective exposure correlation, $\rho_{\mathrm{eff}}$")
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


def _format_tick(value: float) -> str:
    """Compact numeric tick labels, treating clipped 1.0 endpoints as 1."""
    if np.isclose(value, 1.0, atol=1e-5):
        return "1"
    return f"{value:g}"


def _load_required_parquet(path: Path, *, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {label} production summary file: {path}. "
            "Retrieve compact production outputs before rebuilding this figure."
        )
    return pd.read_parquet(path)


def summarize_mixed_heatmap_supplement(
    df: pd.DataFrame,
    *,
    metric: str,
    species_values: Sequence[int] = (2, 4, 8),
) -> pd.DataFrame:
    """Aggregate mixed-slope production rows for supplementary heatmaps."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "mean_extinction_freq",
        metric,
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    species_list = list(species_values)
    mixed = pd.DataFrame(
        df[
            df["slope_mode"].eq("mixed")
            & df["n_species"].isin(species_list)
            & (df["rho_eff"] >= -1e-12)
        ].copy()
    )
    if mixed.empty:
        raise ValueError("No mixed-slope production rows found for supplementary heatmaps.")

    summary = (
        mixed.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            metric_mean=(metric, "mean"),
            metric_sd=(metric, "std"),
            extinction_mean=("mean_extinction_freq", "mean"),
            replicate_rows=(metric, "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    out["metric"] = metric
    if metric == "phi_ldm":
        zero_noise = np.asarray(out["sigma_env"], dtype=float) == 0.0
        out.loc[zero_noise, ["metric_mean", "metric_sd"]] = np.nan
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["sigma_env"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def make_mixed_heatmap_supplement(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    metric_label: str,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production-backed mixed-slope supplementary heatmaps."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    species_values = sorted(int(value) for value in summary["n_species"].unique())
    sigmas = sorted(float(value) for value in summary["sigma_env"].unique())
    rhos = sorted(float(value) for value in summary["rho_eff"].unique())
    tables: dict[int, pd.DataFrame] = {}
    for n_species in species_values:
        table = summary[summary["n_species"].eq(n_species)].pivot_table(
            index="rho_eff",
            columns="sigma_env",
            values="metric_mean",
            aggfunc="mean",
        )
        tables[n_species] = table.reindex(index=rhos, columns=sigmas)

    vmin = float(np.nanmin([np.nanmin(table.values) for table in tables.values()]))
    vmax = float(np.nanmax([np.nanmax(table.values) for table in tables.values()]))
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#d9d9d9")

    fig, axes = plt.subplots(
        1,
        len(species_values),
        figsize=(4.4 * len(species_values), 4.2),
        constrained_layout=True,
        sharey=True,
    )
    axes_arr = np.asarray(axes).ravel()
    image = None
    for idx, (ax, n_species) in enumerate(zip(axes_arr, species_values)):
        table = tables[n_species]
        image = ax.imshow(
            table.values,
            origin="lower",
            aspect="auto",
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
        )
        ax.set_xlabel(r"Environmental variability, $\sigma_{\mathrm{env}}$")
        if idx == 0:
            ax.set_ylabel(r"Effective exposure correlation, $\rho_{\mathrm{eff}}$")
        ax.set_title(rf"$S={n_species}$", fontsize=10)
        ax.set_xticks(range(len(sigmas)))
        ax.set_xticklabels([_format_tick(value) for value in sigmas], rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(rhos)))
        ax.set_yticklabels([_format_tick(value) for value in rhos], fontsize=8)
        _add_panel_label(ax, chr(ord("A") + idx))

    if image is None:
        raise ValueError("No heatmap panels were drawn.")
    cbar = fig.colorbar(image, ax=list(axes_arr), fraction=0.030, pad=0.03)
    cbar.set_label(metric_label)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_mixed_heatmap_supplement(
    *,
    production_path: Path,
    metric: str,
    metric_label: str,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    species_values: Sequence[int] = (2, 4, 8),
) -> None:
    """Load production richness outputs and write a supplementary heatmap."""
    df = _load_required_parquet(production_path, label=f"supplementary {metric}")
    summary = summarize_mixed_heatmap_supplement(
        df,
        metric=metric,
        species_values=species_values,
    )
    make_mixed_heatmap_supplement(
        summary,
        out_png,
        metric_label=metric_label,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


def summarize_species_cv_supplement(
    df: pd.DataFrame,
    *,
    sigma_target: float = 0.5,
    species_values: Sequence[int] = (4, 8),
) -> pd.DataFrame:
    """Aggregate production rows for the species-level CV supplement."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "mean_species_mean",
        "mean_species_var",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    sigma_mask = np.isclose(np.asarray(df["sigma_env"], dtype=float), sigma_target)
    species_list = list(species_values)
    sub = pd.DataFrame(
        df[
            sigma_mask
            & df["slope_mode"].isin(["mixed", "positive"])
            & df["n_species"].isin(species_list)
            & (df["rho_eff"] >= -1e-12)
        ].copy()
    )
    if sub.empty:
        raise ValueError(f"No production rows found for sigma_env={sigma_target:g}.")

    species_mean = np.asarray(sub["mean_species_mean"], dtype=float)
    species_var = np.asarray(sub["mean_species_var"], dtype=float)
    cv_sp = np.full(species_mean.shape, np.nan, dtype=float)
    valid = species_mean > 0
    cv_sp[valid] = np.sqrt(np.maximum(species_var[valid], 0.0)) / species_mean[valid]
    sub["cv_sp"] = cv_sp

    summary = (
        sub.groupby(["slope_mode", "n_species", "sigma_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            cv_sp_mean=("cv_sp", "mean"),
            cv_sp_sd=("cv_sp", "std"),
            extinction_mean=("mean_extinction_freq", "mean"),
            replicate_rows=("cv_sp", "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
            np.asarray(out["slope_mode"], dtype=str),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def make_species_cv_supplement(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write the production-backed species-level CV diagnostic."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    colors = {"mixed": "#1f77b4", "positive": "#d95f02"}
    labels = {"mixed": "mixed responses", "positive": "aligned responses"}
    markers = {4: "o", 8: "s"}

    fig, ax = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    for slope_mode in ["mixed", "positive"]:
        mode = pd.DataFrame(summary[summary["slope_mode"].eq(slope_mode)].copy())
        if mode.empty:
            continue
        for n_species, group in mode.groupby("n_species", observed=True):
            group = pd.DataFrame(group).copy()
            group = group.iloc[np.argsort(np.asarray(group["rho_eff"], dtype=float))].reset_index(drop=True)
            species_count = int(np.asarray(group["n_species"], dtype=int)[0])
            ax.plot(
                group["rho_eff"],
                group["cv_sp_mean"],
                marker=markers.get(species_count, "o"),
                ls="-" if slope_mode == "mixed" else "--",
                lw=2.0,
                ms=4.8,
                color=colors[slope_mode],
                alpha=0.75 if species_count == 4 else 0.95,
                label=f"{labels[slope_mode]}, S={species_count}",
            )

    ax.set(
        xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
        ylabel=r"Approx. species-level $\mathrm{CV}_{\mathrm{sp}}$",
    )
    ax.legend(fontsize=8, frameon=False, ncol=2)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_species_cv_supplement(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    sigma_target: float = 0.5,
    species_values: Sequence[int] = (4, 8),
) -> None:
    """Load production synchrony outputs and write the species-CV supplement."""
    df = _load_required_parquet(production_path, label="supplementary species CV")
    summary = summarize_species_cv_supplement(
        df,
        sigma_target=sigma_target,
        species_values=species_values,
    )
    make_species_cv_supplement(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


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
        xlabel=r"Environmental variability, $\sigma_{\mathrm{env}}$",
        ylabel=r"Mean $\mathrm{CV}_{\mathrm{tot}}$ across $\rho_{\mathrm{eff}}$",
    )
    ax_gradient.set_xlim(min(sigmas) - 0.05, max(sigmas) + 0.05)
    ax_gradient.legend(loc="upper left", fontsize=8, frameon=True)
    _add_panel_label(ax_gradient, "B")

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


def summarize_fig3_synchrony_production(df: pd.DataFrame, *, sigma_target: float = 0.5) -> pd.DataFrame:
    """Aggregate production rows for the imposed-vs-realised synchrony figure."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "mean_pairwise_corr",
        "phi_ldm",
        "cv_total",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    sigma_mask = np.isclose(np.asarray(df["sigma_env"], dtype=float), sigma_target)
    sub = pd.DataFrame(df.loc[sigma_mask, :].copy())
    rho_mask = np.asarray(sub["rho_eff"], dtype=float) >= -1e-12
    sub = pd.DataFrame(sub.loc[rho_mask, :].copy())
    if sub.empty:
        raise ValueError(f"No production rows found for sigma_env={sigma_target:g}.")

    summary = (
        sub.groupby(["slope_mode", "n_species", "rho_eff"], as_index=False, observed=True)
        .agg(
            pair_corr_mean=("mean_pairwise_corr", "mean"),
            pair_corr_sd=("mean_pairwise_corr", "std"),
            phi_ldm_mean=("phi_ldm", "mean"),
            cv_total_mean=("cv_total", "mean"),
            extinction_mean=("mean_extinction_freq", "mean"),
            replicate_rows=("mean_pairwise_corr", "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    out["delta_corr"] = out["pair_corr_mean"] - out["rho_eff"]
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
            np.asarray(out["slope_mode"], dtype=str),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def make_production_fig3_synchrony(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production Figure 3: imposed versus realised synchrony."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    colors = {"mixed": "#1f77b4", "positive": "#d95f02"}
    labels = {"mixed": "mixed responses", "positive": "aligned responses"}
    markers = {2: "o", 4: "s", 8: "^"}

    fig, axes = plt.subplots(3, 1, figsize=(6.4, 9.0), constrained_layout=True)

    for ax, slope_mode, panel_label in zip(axes[:2], ["mixed", "positive"], ["A", "B"]):
        mode = pd.DataFrame(summary[summary["slope_mode"].eq(slope_mode)].copy())
        for n_species, group in mode.groupby("n_species", observed=True):
            group = pd.DataFrame(group).copy()
            group = group.iloc[np.argsort(np.asarray(group["rho_eff"], dtype=float))].reset_index(drop=True)
            species_count = int(np.asarray(group["n_species"], dtype=int)[0])
            ax.plot(
                group["rho_eff"],
                group["pair_corr_mean"],
                marker=markers.get(species_count, "o"),
                lw=2.0,
                ms=4.6,
                color=colors[slope_mode],
                alpha=0.55 + 0.05 * species_count,
                label=f"S={species_count}",
            )
        ax.plot([0, 1], [0, 1], color="0.25", lw=0.9, ls="--", label="y=x")
        ax.axhline(0, color="0.55", lw=0.8, ls=":")
        ax.set(
            xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
            ylabel="Realised mean log-growth correlation",
            xlim=(-0.02, 1.02),
            ylim=(-1.02, 1.02),
        )
        ax.tick_params(labelsize=8.5)
        ax.legend(fontsize=8.5, frameon=False)
        _add_panel_label(ax, panel_label)

    ax = axes[2]
    for slope_mode, marker in [("mixed", "o"), ("positive", "s")]:
        mode = pd.DataFrame(summary[summary["slope_mode"].eq(slope_mode)].copy())
        regime = (
            mode.groupby("rho_eff", as_index=False, observed=True)
            .agg(
                delta_mean=("delta_corr", "mean"),
                delta_min=("delta_corr", "min"),
                delta_max=("delta_corr", "max"),
            )
            .reset_index(drop=True)
        )
        regime = pd.DataFrame(regime)
        regime = regime.iloc[np.argsort(np.asarray(regime["rho_eff"], dtype=float))].reset_index(drop=True)
        x = np.asarray(regime["rho_eff"], dtype=float)
        ax.fill_between(
            x,
            np.asarray(regime["delta_min"], dtype=float),
            np.asarray(regime["delta_max"], dtype=float),
            color=colors[slope_mode],
            alpha=0.12,
            linewidth=0,
        )
        ax.plot(
            x,
            np.asarray(regime["delta_mean"], dtype=float),
            marker=marker,
            lw=2.0,
            ms=4.6,
            color=colors[slope_mode],
            label=labels[slope_mode],
        )
    ax.axhline(0, color="0.25", lw=0.9, ls="--")
    ax.set(
        xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
        ylabel=r"$\Delta$ log-growth correlation",
        xlim=(-0.02, 1.02),
    )
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=8.5, frameon=False)
    _add_panel_label(ax, "C")

    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig3_synchrony(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    sigma_target: float = 0.5,
) -> None:
    """Load production synchrony outputs and write Figure 3."""
    df = _load_required_parquet(production_path, label="Figure 3 synchrony")
    summary = summarize_fig3_synchrony_production(df, sigma_target=sigma_target)
    make_production_fig3_synchrony(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


def summarize_figs3_positive_matched_control(
    df: pd.DataFrame,
    *,
    sigma_target: float = 0.5,
    species_values: Sequence[int] = (4, 8),
) -> pd.DataFrame:
    """Aggregate production rows for the positive-matched sign-control supplement."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "mean_pairwise_corr",
        "phi_ldm",
        "cv_total",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    slope_order = ["mixed", "positive_matched", "positive"]
    species_list = list(species_values)
    sigma_mask = np.isclose(np.asarray(df["sigma_env"], dtype=float), sigma_target)
    sub = pd.DataFrame(
        df[
            sigma_mask
            & df["slope_mode"].isin(slope_order)
            & df["n_species"].isin(species_list)
            & (df["rho_eff"] >= -1e-12)
        ].copy()
    )
    if sub.empty:
        raise ValueError(f"No production rows found for Figure S3 at sigma_env={sigma_target:g}.")

    missing_modes = [mode for mode in slope_order if mode not in set(sub["slope_mode"])]
    if missing_modes:
        raise ValueError(f"Missing Figure S3 slope mode(s): {', '.join(missing_modes)}")

    summary = (
        sub.groupby(["slope_mode", "n_species", "sigma_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            cv_total_mean=("cv_total", "mean"),
            cv_total_sd=("cv_total", "std"),
            pair_corr_mean=("mean_pairwise_corr", "mean"),
            pair_corr_sd=("mean_pairwise_corr", "std"),
            phi_ldm_mean=("phi_ldm", "mean"),
            extinction_mean=("mean_extinction_freq", "mean"),
            extinction_max=("mean_extinction_freq", "max"),
            replicate_rows=("cv_total", "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    mode_rank = {mode: rank for rank, mode in enumerate(slope_order)}
    out["_mode_rank"] = [mode_rank[str(mode)] for mode in out["slope_mode"]]
    out = out.sort_values(["_mode_rank", "n_species", "rho_eff"]).drop(columns="_mode_rank")
    return out.reset_index(drop=True)


def make_production_figs3_positive_matched_control(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production Figure S3: positive-matched sign-structure control."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    slope_order = ["mixed", "positive_matched", "positive"]
    colors = {
        "mixed": "#1f77b4",
        "positive_matched": "#2ca02c",
        "positive": "#d95f02",
    }
    labels = {
        "mixed": "mixed",
        "positive_matched": "positive matched",
        "positive": "aligned positive",
    }
    markers = {4: "o", 8: "s"}
    linestyles = {4: "-", 8: "--"}

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6), constrained_layout=True)
    metric_specs = [
        ("cv_total_mean", r"Mean $\mathrm{CV}_{\mathrm{tot}}$"),
        ("pair_corr_mean", "Realised mean log-growth correlation"),
    ]
    for panel_index, (ax, (metric, ylabel)) in enumerate(zip(axes, metric_specs)):
        for slope_mode in slope_order:
            mode = pd.DataFrame(summary[summary["slope_mode"].eq(slope_mode)].copy())
            if mode.empty:
                continue
            for n_species, group in mode.groupby("n_species", observed=True):
                group = pd.DataFrame(group).copy()
                group = group.iloc[np.argsort(np.asarray(group["rho_eff"], dtype=float))].reset_index(drop=True)
                species_count = int(np.asarray(group["n_species"], dtype=int)[0])
                ax.plot(
                    group["rho_eff"],
                    group[metric],
                    marker=markers.get(species_count, "o"),
                    ls=linestyles.get(species_count, "-"),
                    lw=2.0,
                    ms=4.8,
                    color=colors[slope_mode],
                    label=f"{labels[slope_mode]}, S={species_count}" if panel_index == 0 else None,
                )
        ax.set(
            xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
            ylabel=ylabel,
            xlim=(-0.02, 1.02),
        )
        _add_panel_label(ax, chr(ord("A") + panel_index))

    axes[1].plot([0, 1], [0, 1], color="0.25", lw=0.9, ls="--")
    axes[1].axhline(0, color="0.55", lw=0.8, ls=":")
    axes[1].set_ylim(-1.02, 1.02)
    axes[0].legend(fontsize=7.5, frameon=False, loc="upper left")

    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_figs3_positive_matched_control(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    sigma_target: float = 0.5,
) -> None:
    """Load production positive-matched outputs and write Figure S3."""
    df = _load_required_parquet(production_path, label="Figure S3 positive-matched control")
    summary = summarize_figs3_positive_matched_control(df, sigma_target=sigma_target)
    make_production_figs3_positive_matched_control(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


def _json_vector(value: object, n_species: int) -> np.ndarray:
    raw = json.loads(str(value))
    array = np.asarray(raw, dtype=float)
    if array.size == 1:
        array = np.full(n_species, float(array), dtype=float)
    if array.shape != (n_species,):
        raise ValueError(f"Expected a length-{n_species} vector, found shape {array.shape}.")
    return array


def summarize_fig4_weighted_boundary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize paired correlation endpoints for the weighted-balance test."""
    required = {
        "treatment_id",
        "treatment_path",
        "treatment_level",
        "slope_mode",
        "n_species",
        "r0",
        "K_json",
        "b_slopes_json",
        "alpha_intra",
        "alpha_inter",
        "rho_eff",
        "cv_total",
        "mean_total",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required Figure 4 columns: {', '.join(missing)}")

    records: list[dict[str, float | int | str]] = []
    for treatment_id, treatment in df.groupby("treatment_id", observed=True):
        treatment = pd.DataFrame(treatment).copy()
        rho_values = sorted(float(value) for value in treatment["rho_eff"].unique())
        if len(rho_values) != 2 or not np.isclose(rho_values[0], 0.0, atol=1e-12):
            raise ValueError(f"{treatment_id} must contain rho=0 and one high-correlation endpoint.")
        rho_low, rho_high = rho_values
        low = pd.DataFrame(treatment[np.isclose(treatment["rho_eff"], rho_low)].copy())
        high = pd.DataFrame(treatment[np.isclose(treatment["rho_eff"], rho_high)].copy())
        if low.empty or high.empty:
            raise ValueError(f"{treatment_id} has an empty correlation endpoint.")

        cv2_low = np.square(np.asarray(low["cv_total"], dtype=float))
        cv2_high = np.square(np.asarray(high["cv_total"], dtype=float))
        mean_low = float(cv2_low.mean())
        mean_high = float(cv2_high.mean())
        if mean_low <= 0 or mean_high <= 0:
            raise ValueError(f"{treatment_id} has a non-positive mean squared CV.")
        ratio = mean_high / mean_low
        se_log_ratio = float(
            np.sqrt(
                cv2_high.var(ddof=1) / (cv2_high.size * mean_high**2)
                + cv2_low.var(ddof=1) / (cv2_low.size * mean_low**2)
            )
        )

        first = treatment.iloc[0]
        n_species = int(first["n_species"])
        K = _json_vector(first["K_json"], n_species)
        slopes = _json_vector(first["b_slopes_json"], n_species)
        equilibrium = deterministic_equilibrium(
            r0=float(first["r0"]),
            K=K,
            alpha_intra=float(first["alpha_intra"]),
            alpha_inter=float(first["alpha_inter"]),
        )
        alignment = weighted_alignment_index(equilibrium, slopes)
        predicted_ratio = equicorrelated_forcing_ratio(
            alignment_index=alignment,
            n_species=n_species,
            rho_low=rho_low,
            rho_high=rho_high,
        )
        records.append(
            {
                "treatment_id": str(treatment_id),
                "treatment_path": str(first["treatment_path"]),
                "treatment_level": float(first["treatment_level"]),
                "slope_mode": str(first["slope_mode"]),
                "n_species": n_species,
                "r0": float(first["r0"]),
                "rho_low": rho_low,
                "rho_high": rho_high,
                "alignment_index": alignment,
                "alignment_threshold": 1.0 / n_species,
                "response_norm": float(np.linalg.norm(slopes)),
                "weighted_response_norm": float(np.linalg.norm(equilibrium * slopes)),
                "equilibrium_total": float(equilibrium.sum()),
                "equilibrium_min": float(equilibrium.min()),
                "predicted_forcing_ratio": predicted_ratio,
                "cv2_low_mean": mean_low,
                "cv2_high_mean": mean_high,
                "cv2_ratio": ratio,
                "cv2_ratio_ci_low": float(ratio * np.exp(-1.96 * se_log_ratio)),
                "cv2_ratio_ci_high": float(ratio * np.exp(1.96 * se_log_ratio)),
                "cv_low_mean": float(low["cv_total"].mean()),
                "cv_high_mean": float(high["cv_total"].mean()),
                "mean_total_low": float(low["mean_total"].mean()),
                "mean_total_high": float(high["mean_total"].mean()),
                "floor_occupancy_max": float(
                    treatment.groupby("rho_eff", observed=True)["mean_extinction_freq"].mean().max()
                ),
                "replicates_per_endpoint": int(min(len(low), len(high))),
            }
        )

    out = pd.DataFrame.from_records(records)
    return out.sort_values(["treatment_path", "treatment_level", "slope_mode"]).reset_index(drop=True)


def make_production_fig4_weighted_boundary(
    matched_summary: pd.DataFrame,
    boundary_summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write Figure 4: matched signs, weighted-balance boundary, and r0 test."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        boundary_summary.to_csv(summary_out, index=False)

    colors = {"mixed": "#1f77b4", "positive_matched": "#d95f02"}
    labels = {"mixed": "balanced mixed", "positive_matched": "aligned, matched magnitude"}
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 9.0), constrained_layout=True)

    matched = pd.DataFrame(
        matched_summary[matched_summary["slope_mode"].isin(colors)].copy()
    )
    for slope_mode in ["mixed", "positive_matched"]:
        mode = pd.DataFrame(matched[matched["slope_mode"].eq(slope_mode)].copy())
        for n_species, group in mode.groupby("n_species", observed=True):
            group = pd.DataFrame(group).sort_values("rho_eff")
            species_count = int(np.asarray(group["n_species"], dtype=int)[0])
            axes[0].plot(
                group["rho_eff"],
                group["cv_total_mean"],
                color=colors[slope_mode],
                ls="-" if species_count == 4 else "--",
                marker="o" if species_count == 4 else "s",
                lw=2.0,
                ms=4.2,
                label=f"{labels[slope_mode]}, S={species_count}",
            )
    axes[0].set(
        xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
        ylabel=r"Mean $\mathrm{CV}_{\mathrm{tot}}$",
        xlim=(-0.02, 1.02),
    )
    axes[0].tick_params(labelsize=8.5)
    axes[0].legend(fontsize=8.5, frameon=False, loc="upper left")

    response_path = pd.DataFrame(
        boundary_summary[boundary_summary["treatment_path"].eq("alignment")].copy()
    ).sort_values("alignment_index")
    dominance_path = pd.DataFrame(
        boundary_summary[boundary_summary["treatment_path"].eq("dominance")].copy()
    ).sort_values("alignment_index")
    baseline = pd.DataFrame(response_path[response_path["treatment_level"].eq(0.0)].copy())
    dominance_path = pd.concat([baseline, dominance_path], ignore_index=True).sort_values(
        "alignment_index"
    )

    analytic_x = np.linspace(0.0, max(0.82, float(response_path["alignment_index"].max())), 200)
    axes[1].plot(analytic_x, 4.0 * analytic_x, color="0.3", ls=":", lw=1.5, label="first-order benchmark")
    for path, color, marker, label in [
        (response_path, "#6a3d9a", "o", "response alignment"),
        (dominance_path, "#1b9e77", "s", "abundance weighting"),
    ]:
        y = np.asarray(path["cv2_ratio"], dtype=float)
        yerr = np.vstack(
            [
                y - np.asarray(path["cv2_ratio_ci_low"], dtype=float),
                np.asarray(path["cv2_ratio_ci_high"], dtype=float) - y,
            ]
        )
        axes[1].errorbar(
            path["alignment_index"],
            y,
            yerr=yerr,
            color=color,
            marker=marker,
            lw=1.7,
            ms=4.8,
            capsize=2.0,
            label=label,
        )
    axes[1].axhline(1.0, color="0.45", lw=0.9, ls="--")
    axes[1].axvline(0.25, color="0.45", lw=0.9, ls="--")
    axes[1].set(
        xlabel=r"Abundance-weighted alignment, $A$",
        ylabel=r"High/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio",
        xlim=(-0.02, 0.84),
    )
    axes[1].tick_params(labelsize=8.5)
    axes[1].legend(fontsize=8.5, frameon=False, loc="upper left")

    inset = axes[1].inset_axes([0.53, 0.08, 0.44, 0.43])
    inset.plot(analytic_x, 4.0 * analytic_x, color="0.3", ls=":", lw=1.1)
    for path, color, marker in [
        (response_path, "#6a3d9a", "o"),
        (dominance_path, "#1b9e77", "s"),
    ]:
        y = np.asarray(path["cv2_ratio"], dtype=float)
        yerr = np.vstack(
            [
                y - np.asarray(path["cv2_ratio_ci_low"], dtype=float),
                np.asarray(path["cv2_ratio_ci_high"], dtype=float) - y,
            ]
        )
        inset.errorbar(
            path["alignment_index"],
            y,
            yerr=yerr,
            color=color,
            marker=marker,
            lw=1.0,
            ms=3.5,
            capsize=1.5,
        )
    inset.axhline(1.0, color="0.45", lw=0.7, ls="--")
    inset.axvline(0.25, color="0.45", lw=0.7, ls="--")
    inset.set(
        xlim=(0.20, 0.28),
        ylim=(0.90, 1.15),
        xticks=[0.20, 0.24, 0.28],
        yticks=[0.9, 1.0, 1.1],
    )
    inset.tick_params(labelsize=8.5, pad=1)
    inset.text(
        0.03, 0.96, "Near-boundary reversal", transform=inset.transAxes,
        fontsize=8.5, ha="left", va="top",
    )
    inset.set_facecolor("white")
    axes[1].indicate_inset_zoom(inset, edgecolor="0.25", linewidth=0.8)

    r0_rows = pd.DataFrame(
        boundary_summary[
            boundary_summary["treatment_path"].eq("r0")
            | (
                boundary_summary["treatment_path"].eq("alignment")
                & boundary_summary["treatment_level"].isin([0.0, 1.0])
            )
        ].copy()
    )
    for slope_mode, marker in [("mixed", "o"), ("positive_matched", "s")]:
        group = pd.DataFrame(r0_rows[r0_rows["slope_mode"].eq(slope_mode)].copy()).sort_values("r0")
        y = np.asarray(group["cv2_ratio"], dtype=float)
        yerr = np.vstack(
            [
                y - np.asarray(group["cv2_ratio_ci_low"], dtype=float),
                np.asarray(group["cv2_ratio_ci_high"], dtype=float) - y,
            ]
        )
        axes[2].errorbar(
            group["r0"],
            y,
            yerr=yerr,
            color=colors[slope_mode],
            marker=marker,
            lw=2.0,
            ms=5.0,
            capsize=2.0,
            label=labels[slope_mode],
        )
    axes[2].axhline(1.0, color="0.45", lw=0.9, ls="--")
    axes[2].set(
        xlabel=r"Intrinsic growth rate, $r_0$",
        ylabel=r"High/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio",
        xticks=[0.25, 0.5, 1.0, 1.5],
    )
    axes[2].tick_params(labelsize=8.5)
    axes[2].legend(fontsize=8.5, frameon=False, loc="center right")

    for label, ax in zip(["A", "B", "C"], axes):
        _add_panel_label(ax, label)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig4_weighted_boundary(
    *,
    matched_path: Path,
    sensitivity_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Load the two production sources and write the diagnostic Figure 4."""
    matched = _load_required_parquet(matched_path, label="Figure 4 matched-sign control")
    sensitivity = _load_required_parquet(sensitivity_path, label="Figure 4 boundary sensitivity")
    matched_summary = summarize_figs3_positive_matched_control(matched)
    boundary_summary = summarize_fig4_weighted_boundary(sensitivity)
    make_production_fig4_weighted_boundary(
        matched_summary,
        boundary_summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


def summarize_fig5_persistence_production(df: pd.DataFrame, *, sigma_target: float = 0.5) -> pd.DataFrame:
    """Aggregate mixed-slope production rows for the persistence-sensitivity figure."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "phi",
        "cv_total",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    sigma_mask = np.isclose(np.asarray(df["sigma_env"], dtype=float), sigma_target)
    mixed = pd.DataFrame(df.loc[df["slope_mode"].eq("mixed") & sigma_mask, :].copy())
    if mixed.empty:
        raise ValueError(f"No mixed-slope production rows found for sigma_env={sigma_target:g}.")

    summary = (
        mixed.groupby(["n_species", "phi", "sigma_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            cv_total_mean=("cv_total", "mean"),
            cv_total_sd=("cv_total", "std"),
            extinction_mean=("mean_extinction_freq", "mean"),
            extinction_max=("mean_extinction_freq", "max"),
            replicate_rows=("cv_total", "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["phi"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def _phi_legend_label(phi: float, sigma_env: float) -> str:
    sigma_eff = sigma_env / np.sqrt(1.0 - phi**2)
    return rf"$\phi={phi:g}$ ($\sigma_{{eff}}\approx {sigma_eff:.2f}$)"


def make_production_fig5_persistence(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production Figure 5: mixed-slope sensitivity to environmental persistence."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    species_values = sorted(int(value) for value in summary["n_species"].unique())
    phi_values = sorted(float(value) for value in summary["phi"].unique())
    colors = plt.get_cmap("cividis")(np.linspace(0.12, 0.88, len(phi_values)))
    markers = ["o", "s", "^", "D", "v", "P"]

    fig, axes = plt.subplots(1, len(species_values), figsize=(10.5, 4.4), constrained_layout=True, sharey=True)
    axes_arr = np.asarray(axes).ravel()

    for ax, n_species, panel_label in zip(axes_arr, species_values, ["A", "B", "C", "D"]):
        species = pd.DataFrame(summary[summary["n_species"].eq(n_species)].copy())
        for idx, phi in enumerate(phi_values):
            sub = pd.DataFrame(species[np.isclose(np.asarray(species["phi"], dtype=float), phi)].copy())
            if sub.empty:
                continue
            sub = sub.iloc[np.argsort(np.asarray(sub["rho_eff"], dtype=float))].reset_index(drop=True)
            sigma_env = float(np.asarray(sub["sigma_env"], dtype=float)[0])
            ax.plot(
                sub["rho_eff"],
                sub["cv_total_mean"],
                marker=markers[idx % len(markers)],
                lw=2.0,
                ms=4.8,
                color=colors[idx],
                label=_phi_legend_label(phi, sigma_env),
            )
        ax.set(
            xlabel=r"Effective exposure correlation, $\rho_{\mathrm{eff}}$",
            xlim=(
                float(np.min(np.asarray(species["rho_eff"], dtype=float))) - 0.03,
                float(np.max(np.asarray(species["rho_eff"], dtype=float))) + 0.03,
            ),
        )
        if ax is axes_arr[0]:
            ax.set_ylabel(r"Mean $\mathrm{CV}_{\mathrm{tot}}$")
            ax.legend(fontsize=8, frameon=False)
        _add_panel_label(ax, panel_label)

    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig5_persistence(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    sigma_target: float = 0.5,
) -> None:
    """Load production persistence outputs and write Figure 5."""
    df = _load_required_parquet(production_path, label="Figure 5 persistence")
    summary = summarize_fig5_persistence_production(df, sigma_target=sigma_target)
    make_production_fig5_persistence(
        summary,
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
    )


HIGH_RHO_THRESHOLD = 0.99


def _iter_groups(df: pd.DataFrame, keys: list[str]) -> Iterator[tuple[tuple[float, ...], pd.DataFrame]]:
    """Yield numeric group keys as floats with each group as a DataFrame."""
    for key, group in df.groupby(keys, observed=True):
        values = key if isinstance(key, tuple) else (key,)
        yield tuple(float(cast(float, value)) for value in values), pd.DataFrame(group)
BALANCED_TREATMENT_ID = "alignment-q000"
MATCHED_ALIGNED_TREATMENT_ID = "alignment-q1000"
CALIBRATION_SETTING = (0.3, 4, 0.4)


def _endpoint_ratio(cv_high: np.ndarray, cv_low: np.ndarray) -> tuple[float, float, float]:
    """Return a ratio of mean squared CV with a delta-method 95% interval on the log scale."""
    high = np.square(np.asarray(cv_high, dtype=float))
    low = np.square(np.asarray(cv_low, dtype=float))
    if high.size < 2 or low.size < 2:
        raise ValueError("Each endpoint needs at least two replicates.")
    mean_high = float(high.mean())
    mean_low = float(low.mean())
    if mean_high <= 0 or mean_low <= 0:
        raise ValueError("Endpoint mean squared CV must be positive.")
    ratio = mean_high / mean_low
    se_log = float(
        np.sqrt(
            high.var(ddof=1) / (high.size * mean_high**2)
            + low.var(ddof=1) / (low.size * mean_low**2)
        )
    )
    return ratio, float(ratio * np.exp(-1.96 * se_log)), float(ratio * np.exp(1.96 * se_log))


def _correlation_endpoints(block: pd.DataFrame, label: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    low = pd.DataFrame(block[np.isclose(block["rho_eff"], 0.0, atol=1e-12)])
    high = pd.DataFrame(block[block["rho_eff"] > HIGH_RHO_THRESHOLD])
    if low.empty or high.empty:
        raise ValueError(f"{label} needs rho=0 and near-perfect correlation endpoints.")
    return low, high


def summarize_endpoint_ratio_by_sigma(df: pd.DataFrame, *, slope_mode: str) -> pd.DataFrame:
    """Shared-to-independent ratio of mean squared CV for one slope mode at each sigma_env."""
    block = pd.DataFrame(df[df["slope_mode"].eq(slope_mode) & (df["sigma_env"] > 0)])
    records: list[dict[str, float | int]] = []
    for (sigma_env,), group in _iter_groups(block, ["sigma_env"]):
        low, high = _correlation_endpoints(group, f"sigma_env={sigma_env}")
        ratio, ci_low, ci_high = _endpoint_ratio(high["cv_total"].to_numpy(), low["cv_total"].to_numpy())
        endpoints = pd.concat([low, high])
        records.append(
            {
                "sigma_env": float(sigma_env),
                "cv2_ratio": ratio,
                "cv2_ratio_ci_low": ci_low,
                "cv2_ratio_ci_high": ci_high,
                "floor_replicate_max": float(endpoints["mean_extinction_freq"].max()),
                "replicates_per_endpoint": int(min(len(low), len(high))),
            }
        )
    return pd.DataFrame.from_records(records)


def summarize_boundary_by_sigma(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the weighted-boundary summary separately at each sigma_env."""
    if "sigma_env" not in df.columns:
        raise ValueError("Missing required column: sigma_env")
    blocks: list[pd.DataFrame] = []
    for (sigma_env,), group in _iter_groups(df, ["sigma_env"]):
        summary = summarize_fig4_weighted_boundary(group)
        replicate_max = {
            str(treatment_id): float(cast(float, value))
            for treatment_id, value in group.groupby("treatment_id", observed=True)["mean_extinction_freq"]
            .max()
            .items()
        }
        summary.insert(0, "sigma_env", sigma_env)
        summary["floor_replicate_max"] = [replicate_max[str(tid)] for tid in summary["treatment_id"]]
        blocks.append(summary)
    out = pd.concat(blocks, ignore_index=True)
    return out.sort_values(["sigma_env", "treatment_path", "treatment_level"]).reset_index(drop=True)


def summarize_sign_contrast_by_sigma(df: pd.DataFrame) -> pd.DataFrame:
    """Compare matched aligned with balanced mixed slopes directly at each sigma_env."""
    records: list[dict[str, float]] = []
    for (sigma_env,), group in _iter_groups(df, ["sigma_env"]):
        mixed_low, mixed_high = _correlation_endpoints(
            pd.DataFrame(group[group["treatment_id"].eq(BALANCED_TREATMENT_ID)]), "balanced mixed"
        )
        matched_low, matched_high = _correlation_endpoints(
            pd.DataFrame(group[group["treatment_id"].eq(MATCHED_ALIGNED_TREATMENT_ID)]),
            "matched aligned",
        )
        shared, shared_low, shared_high = _endpoint_ratio(
            matched_high["cv_total"].to_numpy(), mixed_high["cv_total"].to_numpy()
        )
        independent, ind_low, ind_high = _endpoint_ratio(
            matched_low["cv_total"].to_numpy(), mixed_low["cv_total"].to_numpy()
        )
        mixed_ratio, mixed_ci_low, mixed_ci_high = _endpoint_ratio(
            mixed_high["cv_total"].to_numpy(), mixed_low["cv_total"].to_numpy()
        )
        matched_ratio, matched_ci_low, matched_ci_high = _endpoint_ratio(
            matched_high["cv_total"].to_numpy(), matched_low["cv_total"].to_numpy()
        )
        records.append(
            {
                "sigma_env": sigma_env,
                "balanced_shared_over_independent": mixed_ratio,
                "balanced_ci_low": mixed_ci_low,
                "balanced_ci_high": mixed_ci_high,
                "matched_shared_over_independent": matched_ratio,
                "matched_ci_low": matched_ci_low,
                "matched_ci_high": matched_ci_high,
                "shared_matched_over_balanced": shared,
                "shared_matched_over_balanced_ci_low": shared_low,
                "shared_matched_over_balanced_ci_high": shared_high,
                "independent_matched_over_balanced": independent,
                "independent_matched_over_balanced_ci_low": ind_low,
                "independent_matched_over_balanced_ci_high": ind_high,
            }
        )
    return pd.DataFrame.from_records(records)


def summarize_mechanism_grids(df: pd.DataFrame, *, alpha_intra: float = 1.0) -> pd.DataFrame:
    """Balanced shared-to-independent ratios with the small-noise second-order prediction."""
    required = {"slope_mode", "alpha_inter", "n_species", "phi", "sigma_env", "rho_eff", "cv_total"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required mechanism columns: {', '.join(missing)}")
    if not bool(df["slope_mode"].eq("mixed").all()):
        raise ValueError("The mechanism summary applies to balanced mixed slopes only.")
    keys = ["alpha_inter", "n_species", "phi", "sigma_env"]
    records: list[dict[str, float | int | bool]] = []
    for (alpha_inter, n_species, phi, sigma_env), group in _iter_groups(df, keys):
        low, high = _correlation_endpoints(group, f"setting {alpha_inter}, {n_species}, {phi}")
        ratio, ci_low, ci_high = _endpoint_ratio(high["cv_total"].to_numpy(), low["cv_total"].to_numpy())
        slopes = slopes_for_mode("mixed", int(n_species))
        coefficient = balanced_small_noise_coefficient(
            response_slopes=slopes, alpha_intra=alpha_intra, alpha_inter=float(alpha_inter), phi=float(phi)
        )
        endpoints = pd.concat([low, high])
        floor_max = float(endpoints["mean_extinction_freq"].max())
        setting = (round(float(alpha_inter), 6), int(n_species), round(float(phi), 6))
        records.append(
            {
                "alpha_inter": float(alpha_inter),
                "n_species": int(n_species),
                "phi": float(phi),
                "sigma_env": float(sigma_env),
                "lambda_d": contrast_mode_eigenvalue(
                    r0=1.0, alpha_intra=alpha_intra, alpha_inter=float(alpha_inter), n_species=int(n_species)
                ),
                "small_noise_coefficient": coefficient,
                "predicted_ratio": coefficient * float(sigma_env) ** 2,
                "cv2_ratio": ratio,
                "cv2_ratio_ci_low": ci_low,
                "cv2_ratio_ci_high": ci_high,
                "floor_replicate_max": floor_max,
                "small_noise_eligible": bool(coefficient * 0.01 < 0.1),
                "calibration_repeat": bool(setting == CALIBRATION_SETTING),
                "floor_free_reversal": bool(floor_max == 0.0 and ci_low > 1.0),
                "n_steps": int(group["n_steps"].iloc[0]) if "n_steps" in group.columns else -1,
                "burn_in": int(group["burn_in"].iloc[0]) if "burn_in" in group.columns else -1,
                "replicates_per_endpoint": int(min(len(low), len(high))),
            }
        )
    return pd.DataFrame.from_records(records).sort_values(keys).reset_index(drop=True)


def _interpolated_crossing(alignment: np.ndarray, ratio: np.ndarray) -> tuple[float, float, float]:
    """Linear interpolation of the first crossing of ratio = 1 along increasing alignment."""
    order = np.argsort(alignment)
    x = np.asarray(alignment, dtype=float)[order]
    y = np.asarray(ratio, dtype=float)[order]
    for i in range(len(x) - 1):
        if (y[i] - 1.0) * (y[i + 1] - 1.0) <= 0 and y[i] != y[i + 1]:
            crossing = x[i] + (1.0 - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i])
            return float(crossing), float(x[i]), float(x[i + 1])
    return float("nan"), float("nan"), float("nan")


def summarize_boundary_crossings(boundary_by_sigma: pd.DataFrame) -> pd.DataFrame:
    """Interpolated A at which the ratio crosses one, with the bracketing tested compositions."""
    records: list[dict[str, float | str]] = []
    for (sigma_env,), group in _iter_groups(boundary_by_sigma, ["sigma_env"]):
        balanced = group[group["treatment_id"].eq(BALANCED_TREATMENT_ID)]
        paths = {
            "rotation": group[group["treatment_path"].eq("alignment")],
            "unequal_K": pd.concat([balanced, group[group["treatment_path"].eq("dominance")]]),
        }
        for path, rows in paths.items():
            crossing, lower, upper = _interpolated_crossing(
                rows["alignment_index"].to_numpy(), rows["cv2_ratio"].to_numpy()
            )
            records.append(
                {
                    "sigma_env": sigma_env,
                    "path": path,
                    "interpolated_crossing_A": crossing,
                    "bracket_lower_A": lower,
                    "bracket_upper_A": upper,
                }
            )
    return pd.DataFrame.from_records(records)


def make_production_fig6_amplitude_boundary(
    sign_summary: pd.DataFrame,
    boundary_by_sigma: pd.DataFrame,
    replication: pd.DataFrame,
    out_png: Path,
    *,
    onset_coefficient: float,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    replication_out: Path | None = None,
) -> None:
    """Write main Figure 2: shared-exposure benefit across fluctuation size."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        sign_summary.to_csv(summary_out, index=False)
    if replication_out is not None:
        replication.to_csv(replication_out, index=False)

    fig, axes = plt.subplots(2, 1, figsize=(6.4, 7.2), constrained_layout=True)
    ax = axes[0]
    rep = replication[replication["sigma_env"] <= boundary_by_sigma["sigma_env"].max() + 1e-9]
    ax.plot(rep["sigma_env"], rep["cv2_ratio"], "o", mfc="none", mec="0.6", ms=4.5, lw=0,
            label="balanced mixed, independent grid")
    series = [
        ("balanced", "#1f77b4", "o", "balanced mixed"),
        ("matched", "#d95f02", "s", "aligned, matched magnitude"),
    ]
    for key, color, marker, label in series:
        y = sign_summary[f"{key}_shared_over_independent"]
        yerr = np.vstack([y - sign_summary[f"{key}_ci_low"], sign_summary[f"{key}_ci_high"] - y])
        ax.errorbar(sign_summary["sigma_env"], y, yerr=yerr, color=color, marker=marker, lw=1.8,
                    ms=5.0, capsize=2.0, label=label)
    limits = boundary_by_sigma[boundary_by_sigma["sigma_env"].eq(boundary_by_sigma["sigma_env"].min())]
    for treatment_id, color in [(BALANCED_TREATMENT_ID, "#1f77b4"), (MATCHED_ALIGNED_TREATMENT_ID, "#d95f02")]:
        limit_rows = pd.DataFrame(limits[limits["treatment_id"] == treatment_id])
        limit = float(limit_rows["predicted_forcing_ratio"].iloc[0])
        ax.plot([0.0], [limit], marker=">", color=color, ms=8, clip_on=False, lw=0)
    sigma_grid = np.linspace(0.0, 0.6, 100)
    ax.plot(sigma_grid, onset_coefficient * sigma_grid**2, color="#1f77b4", ls="--", lw=1.1,
            label=rf"second-order onset, ${onset_coefficient:.2f}\,\sigma_{{\mathrm{{env}}}}^2$")
    ax.axhline(1.0, color="0.45", lw=0.9, ls=":")
    ax.set(xlabel=r"Environmental innovation SD, $\sigma_{\mathrm{env}}$",
           ylabel=r"Shared/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio", xlim=(0.0, 1.35), ylim=(0.0, 3.4))
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=8, frameon=False, loc="center right")

    ax = axes[1]
    rotation = pd.DataFrame(boundary_by_sigma[boundary_by_sigma["treatment_path"] == "alignment"])
    cmap = plt.get_cmap("plasma")
    shown = [0.1, 0.5, 1.3]
    for i, sigma_env in enumerate(shown):
        rows = pd.DataFrame(rotation[np.isclose(rotation["sigma_env"], sigma_env)]).sort_values("alignment_index")
        if rows.empty:
            continue
        color = cmap(0.1 + 0.75 * i / (len(shown) - 1))
        y = rows["cv2_ratio"]
        yerr = np.vstack([y - rows["cv2_ratio_ci_low"], rows["cv2_ratio_ci_high"] - y])
        ax.errorbar(rows["alignment_index"], y, yerr=yerr, color=color, lw=1.5, capsize=1.5, marker="none")
        clean = rows["floor_replicate_max"].eq(0.0)
        ax.plot(rows["alignment_index"][clean], y[clean], "o", color=color, ms=4.5,
                label=rf"$\sigma_{{\mathrm{{env}}}}={sigma_env:g}$")
        ax.plot(rows["alignment_index"][~clean], y[~clean], "o", mfc="white", mec=color, ms=4.5)
    rho_high = float(rotation["rho_high"].iloc[0])
    a_grid = np.linspace(0.0, 0.82, 50)
    ax.plot(a_grid, (1.0 - rho_high) + rho_high * 4.0 * a_grid, ":", color="0.3", lw=1.3, label="first-order benchmark")
    ax.axhline(1.0, color="0.45", lw=0.9, ls="--")
    ax.axvline(0.25, color="0.45", lw=0.9, ls="--")
    ax.set(xlabel=r"Abundance-weighted alignment, $A$",
           ylabel=r"Shared/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio")
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    for label, axis in zip(["A", "B"], axes):
        _add_panel_label(axis, label)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig6_amplitude_boundary(
    *,
    boundary_path: Path,
    core_path: Path,
    highsigma_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    replication_out: Path | None = None,
) -> None:
    """Load the boundary-by-sigma grid and the R1/R2 replication grids and write Figure 2."""
    boundary = _load_required_parquet(boundary_path, label="boundary-by-sigma")
    replication_frame = load_fig1_production_runs(core_path, highsigma_path)
    onset = balanced_small_noise_coefficient(
        response_slopes=slopes_for_mode("mixed", 4), alpha_intra=1.0, alpha_inter=0.3, phi=0.4
    )
    make_production_fig6_amplitude_boundary(
        summarize_sign_contrast_by_sigma(boundary),
        summarize_boundary_by_sigma(boundary),
        summarize_endpoint_ratio_by_sigma(replication_frame, slope_mode="mixed"),
        out_png,
        onset_coefficient=onset,
        out_pdf=out_pdf,
        summary_out=summary_out,
        replication_out=replication_out,
    )


def make_production_fig7_mechanism_reversal(
    mechanism: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write main Figure 3: prespecified small-noise prediction and balanced reversals."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        mechanism.to_csv(summary_out, index=False)
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 8.0), constrained_layout=True)
    alpha_colors = {0.1: "#1b9e77", 0.3: "#7570b3", 0.6: "#d95f02"}

    ax = axes[0]
    low_noise = mechanism[mechanism["sigma_env"] <= 0.2 + 1e-9]
    for (alpha, sigma_env), rows in _iter_groups(pd.DataFrame(low_noise), ["alpha_inter", "sigma_env"]):
        color = alpha_colors[round(alpha, 1)]
        marker = "o" if np.isclose(sigma_env, 0.1) else "s"
        eligible = rows["small_noise_eligible"].astype(bool)
        ax.loglog(rows["predicted_ratio"][eligible], rows["cv2_ratio"][eligible], marker, color=color,
                  ms=5, lw=0)
        ax.loglog(rows["predicted_ratio"][~eligible], rows["cv2_ratio"][~eligible], marker, mfc="white",
                  mec=color, ms=5, lw=0)
    calibration = low_noise[low_noise["calibration_repeat"].astype(bool)]
    ax.loglog(calibration["predicted_ratio"], calibration["cv2_ratio"], "o", mfc="none", mec="black",
              ms=10, lw=0, label="calibration setting (independent seeds)")
    for alpha, color in alpha_colors.items():
        ax.plot([], [], "o", color=color, label=rf"$\alpha_{{\mathrm{{inter}}}}={alpha:g}$")
    ax.plot([], [], "o", color="0.4", label=r"$\sigma_{\mathrm{env}}=0.1$")
    ax.plot([], [], "s", color="0.4", label=r"$\sigma_{\mathrm{env}}=0.2$")
    ax.plot([], [], "o", mfc="white", mec="0.4", label="outside small-noise regime")
    lims = np.array([3e-3, 4.0])
    ax.loglog(lims, lims, ":", color="0.3", lw=1.0)
    ax.set(xlim=tuple(lims), ylim=tuple(lims), xlabel="Ratio predicted before simulation",
           ylabel=r"Simulated shared/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio")
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2)

    ax = axes[1]
    coefficients = mechanism["small_noise_coefficient"].to_numpy(dtype=float)
    norm = Normalize(vmin=float(np.log10(coefficients.min())), vmax=float(np.log10(coefficients.max())))
    cmap = plt.get_cmap("viridis")
    for _, rows in _iter_groups(mechanism, ["alpha_inter", "n_species", "phi"]):
        rows = rows.sort_values("sigma_env")
        color = cmap(norm(np.log10(float(rows["small_noise_coefficient"].iloc[0]))))
        ax.plot(rows["sigma_env"], rows["cv2_ratio"], color=color, lw=1.0, alpha=0.85)
        clean = rows["floor_replicate_max"].eq(0.0)
        ax.plot(rows["sigma_env"][clean], rows["cv2_ratio"][clean], "o", color=color, ms=3.5)
        ax.plot(rows["sigma_env"][~clean], rows["cv2_ratio"][~clean], "o", mfc="white", mec=color, ms=3.5)
    reversals = mechanism[mechanism["floor_free_reversal"].astype(bool)]
    ax.plot(reversals["sigma_env"], reversals["cv2_ratio"], "o", mfc="none", mec="#c51b7d", mew=1.6, ms=9,
            lw=0, label="floor-free reversal (95% interval above one)")
    ax.axhline(1.0, color="0.45", lw=0.9, ls="--")
    ax.set(xscale="log", yscale="log", xlabel=r"Environmental innovation SD, $\sigma_{\mathrm{env}}$",
           ylabel=r"Shared/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio")
    ax.set_xticks([0.1, 0.2, 0.5, 1.0])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1"])
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar = fig.colorbar(scalar, ax=ax, pad=0.01)
    colorbar.set_label(r"$\log_{10}$ small-noise coefficient", fontsize=8.5)
    for label, axis in zip(["A", "B"], axes):
        _add_panel_label(axis, label)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig7_mechanism_reversal(
    *,
    mechanism_paths: Sequence[Path],
    longwindow_paths: Sequence[Path],
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    longwindow_out: Path | None = None,
) -> None:
    """Load the mechanism and long-window grids and write Figure 3 plus its summaries."""
    mechanism = pd.concat(
        [_load_required_parquet(path, label="sigma mechanism") for path in mechanism_paths], ignore_index=True
    )
    make_production_fig7_mechanism_reversal(
        summarize_mechanism_grids(mechanism), out_png, out_pdf=out_pdf, summary_out=summary_out
    )
    if longwindow_out is not None:
        longwindow = pd.concat(
            [_load_required_parquet(path, label="long-window reversal") for path in longwindow_paths],
            ignore_index=True,
        )
        summarize_mechanism_grids(longwindow).to_csv(longwindow_out, index=False)


def make_production_figS9_boundary_by_sigma(
    boundary_by_sigma: pd.DataFrame,
    crossings: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    crossings_out: Path | None = None,
) -> None:
    """Write Figure S9: both boundary paths at every sigma_env and interpolated crossings."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        boundary_by_sigma.to_csv(summary_out, index=False)
    if crossings_out is not None:
        crossings.to_csv(crossings_out, index=False)
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 10.0), constrained_layout=True)
    sigmas = sorted(boundary_by_sigma["sigma_env"].unique())
    cmap = plt.get_cmap("viridis")
    balanced = boundary_by_sigma[boundary_by_sigma["treatment_id"].eq(BALANCED_TREATMENT_ID)]
    panels = [
        (axes[0], boundary_by_sigma[boundary_by_sigma["treatment_path"].eq("alignment")], 0.82),
        (axes[1], pd.concat([balanced, boundary_by_sigma[boundary_by_sigma["treatment_path"].eq("dominance")]]), 0.27),
    ]
    rho_high = float(boundary_by_sigma["rho_high"].iloc[0])
    for ax, rows, a_max in panels:
        for i, sigma_env in enumerate(sigmas):
            color = cmap(i / max(len(sigmas) - 1, 1))
            block = rows[np.isclose(rows["sigma_env"], sigma_env)].sort_values("alignment_index")
            ax.plot(block["alignment_index"], block["cv2_ratio"], "-", color=color, lw=1.2,
                    label=rf"$\sigma_{{\mathrm{{env}}}}={sigma_env:g}$")
            clean = block["floor_replicate_max"].eq(0.0)
            ax.plot(block["alignment_index"][clean], block["cv2_ratio"][clean], "o", color=color, ms=3.5)
            ax.plot(block["alignment_index"][~clean], block["cv2_ratio"][~clean], "o", mfc="white", mec=color, ms=3.5)
        a_grid = np.linspace(0.0, a_max, 50)
        ax.plot(a_grid, (1.0 - rho_high) + rho_high * 4.0 * a_grid, ":", color="0.3", lw=1.2, label="first-order benchmark")
        ax.axhline(1.0, color="0.45", lw=0.9, ls="--")
        ax.axvline(0.25, color="0.45", lw=0.9, ls="--")
        ax.set(xlabel=r"Abundance-weighted alignment, $A$",
               ylabel=r"Shared/independent $\mathrm{CV}_{\mathrm{tot}}^2$ ratio")
        ax.tick_params(labelsize=8.5)
    axes[0].legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2)
    ax = axes[2]
    for path, marker, label in [("rotation", "o", "rotation path"), ("unequal_K", "s", "unequal-K path")]:
        rows = crossings[crossings["path"].eq(path)]
        ax.plot(rows["sigma_env"], rows["interpolated_crossing_A"], marker + "-", ms=5, label=label)
    ax.axhline(0.25, color="0.45", lw=0.9, ls="--")
    ax.set(xlabel=r"Environmental innovation SD, $\sigma_{\mathrm{env}}$",
           ylabel="A at which the ratio crosses one\n(linear interpolation)")
    ax.tick_params(labelsize=8.5)
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    for label, axis in zip(["A", "B", "C"], axes):
        _add_panel_label(axis, label)
    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_figS9_boundary_by_sigma(
    *,
    boundary_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
    crossings_out: Path | None = None,
) -> None:
    """Load the boundary-by-sigma grid and write Figure S9 with its summaries."""
    boundary = summarize_boundary_by_sigma(_load_required_parquet(boundary_path, label="boundary-by-sigma"))
    make_production_figS9_boundary_by_sigma(
        boundary,
        summarize_boundary_crossings(boundary),
        out_png,
        out_pdf=out_pdf,
        summary_out=summary_out,
        crossings_out=crossings_out,
    )
