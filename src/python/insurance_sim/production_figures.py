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

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.5), constrained_layout=True)

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
            xlabel=r"Effective driver correlation, $\rho_{\mathrm{eff}}$",
            ylabel="Realised mean growth correlation",
            xlim=(-0.02, 1.02),
            ylim=(-1.02, 1.02),
        )
        ax.legend(fontsize=8, frameon=False)
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
        xlabel=r"Effective driver correlation, $\rho_{\mathrm{eff}}$",
        ylabel=r"$\Delta$ growth correlation",
        xlim=(-0.02, 1.02),
    )
    ax.legend(fontsize=8, frameon=False)
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


def summarize_fig4_cv_synchrony_production(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mixed-slope production rows for the CV-vs-synchrony figure."""
    required = {
        "slope_mode",
        "sigma_env",
        "rho_eff",
        "n_species",
        "cv_total",
        "phi_ldm",
        "mean_pairwise_corr",
        "mean_extinction_freq",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required production columns: {', '.join(missing)}")

    mixed = pd.DataFrame(df[df["slope_mode"].eq("mixed")].copy())
    sigma_positive = np.asarray(mixed["sigma_env"], dtype=float) > 0
    mixed = pd.DataFrame(mixed.loc[sigma_positive, :].copy())
    rho_nonnegative = np.asarray(mixed["rho_eff"], dtype=float) >= -1e-12
    mixed = pd.DataFrame(mixed.loc[rho_nonnegative, :].copy())
    if mixed.empty:
        raise ValueError("No mixed-slope production rows with sigma_env > 0 were found.")

    summary = (
        mixed.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False, observed=True)
        .agg(
            cv_total_mean=("cv_total", "mean"),
            phi_ldm_mean=("phi_ldm", "mean"),
            pair_corr_mean=("mean_pairwise_corr", "mean"),
            extinction_mean=("mean_extinction_freq", "mean"),
            replicate_rows=("cv_total", "size"),
        )
        .reset_index(drop=True)
    )
    out = pd.DataFrame(summary)
    order = np.lexsort(
        (
            np.asarray(out["rho_eff"], dtype=float),
            np.asarray(out["sigma_env"], dtype=float),
            np.asarray(out["n_species"], dtype=int),
        )
    )
    return out.iloc[order].reset_index(drop=True)


def _sigma_size_values(summary: pd.DataFrame) -> np.ndarray:
    sigma = np.asarray(summary["sigma_env"], dtype=float)
    sigma_max = float(np.max(sigma))
    if sigma_max <= 0:
        return np.full_like(sigma, 42.0)
    return 30.0 + 75.0 * (sigma / sigma_max)


def make_production_fig4_cv_synchrony(
    summary: pd.DataFrame,
    out_png: Path,
    *,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Write production Figure 4: community variability versus synchrony."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(summary_out, index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True, sharey=True)
    sizes = _sigma_size_values(summary)
    richness = np.asarray(summary["n_species"], dtype=float)
    scatter_kwargs = {
        "c": richness,
        "cmap": "viridis",
        "vmin": float(np.min(richness)),
        "vmax": float(np.max(richness)),
        "s": sizes,
        "alpha": 0.78,
        "edgecolors": "white",
        "linewidths": 0.45,
    }

    axes[0].scatter(summary["phi_ldm_mean"], summary["cv_total_mean"], **scatter_kwargs)
    axes[0].set(
        xlabel=r"Loreau-de Mazancourt synchrony, $\phi_{\mathrm{LdM}}$",
        ylabel=r"Mean $\mathrm{CV}_{\mathrm{tot}}$",
    )

    points = axes[1].scatter(summary["pair_corr_mean"], summary["cv_total_mean"], **scatter_kwargs)
    axes[1].axvline(0, color="0.55", lw=0.9, ls=":")
    axes[1].set(
        xlabel="Mean pairwise growth correlation",
    )

    cbar = fig.colorbar(points, ax=axes, shrink=0.92, pad=0.015)
    cbar.set_label(r"Species richness, $S$")

    sigma_values = [0.2, 1.0, 2.0]
    sigma_max = float(np.max(np.asarray(summary["sigma_env"], dtype=float)))
    handles = [
        axes[1].scatter(
            [],
            [],
            s=30.0 + 75.0 * (value / sigma_max),
            facecolors="0.65",
            edgecolors="white",
            linewidths=0.45,
            label=f"{value:g}",
        )
        for value in sigma_values
        if value <= sigma_max + 1e-12
    ]
    if handles:
        axes[1].legend(
            handles=handles,
            title=r"$\sigma_{\mathrm{env}}$",
            fontsize=8,
            title_fontsize=9,
            frameon=False,
            loc="upper left",
        )

    for label, ax in zip(["A", "B"], axes):
        _add_panel_label(ax, label)

    fig.savefig(out_png, dpi=300)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


def write_production_fig4_cv_synchrony(
    *,
    production_path: Path,
    out_png: Path,
    out_pdf: Path | None = None,
    summary_out: Path | None = None,
) -> None:
    """Load production mixed-slope richness outputs and write Figure 4."""
    df = _load_required_parquet(production_path, label="Figure 4 CV-synchrony")
    summary = summarize_fig4_cv_synchrony_production(df)
    make_production_fig4_cv_synchrony(
        summary,
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
            xlabel=r"Effective driver correlation, $\rho_{\mathrm{eff}}$",
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
