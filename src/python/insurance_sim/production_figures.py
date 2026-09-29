"""Production-scale figure helpers for the insurance-hypothesis manuscript."""

from __future__ import annotations

from collections.abc import Sequence
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .diagnostics import (
    deterministic_equilibrium,
    equicorrelated_forcing_ratio,
    weighted_alignment_index,
)


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
