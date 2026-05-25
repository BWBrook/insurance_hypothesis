"""Figure-generation helpers for insurance hypothesis analyses."""

from __future__ import annotations

from pathlib import Path

from matplotlib.image import AxesImage
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .reporting import add_species_cv, ensure_effective_rho, sort_by_rho_eff


def make_species_cv_diagnostic(
    summary_mixed: pd.DataFrame,
    summary_pos: pd.DataFrame,
    out_path: Path,
    *,
    summary_out_path: Path | None = None,
    sigma_target: float = 0.5,
) -> None:
    """Supplementary diagnostic: approximate species-level CV vs imposed correlation."""
    summary_mixed = add_species_cv(ensure_effective_rho(summary_mixed))
    summary_pos = add_species_cv(ensure_effective_rho(summary_pos))
    if "cv_sp" not in summary_mixed.columns or "cv_sp" not in summary_pos.columns:
        print("Warning: missing species-level variance summaries; skipping cv_sp diagnostic figure.")
        return

    fig, ax = plt.subplots(figsize=(8, 4.8))
    summary_rows: list[pd.DataFrame] = []

    for s, marker in [(4, "o"), (8, "s")]:
        m_rep = summary_mixed[
            (summary_mixed["sigma_env"] == sigma_target) & (summary_mixed["n_species"] == s)
        ].copy()
        p_rep = summary_pos[
            (summary_pos["sigma_env"] == sigma_target) & (summary_pos["n_species"] == s)
        ].copy()

        m_mean = (
            m_rep.groupby("rho_eff", as_index=False, observed=True)
            .agg(cv_sp=("cv_sp", "mean"))
        )
        p_mean = (
            p_rep.groupby("rho_eff", as_index=False, observed=True)
            .agg(cv_sp=("cv_sp", "mean"))
        )
        m_mean = sort_by_rho_eff(pd.DataFrame(m_mean))
        p_mean = sort_by_rho_eff(pd.DataFrame(p_mean))

        m_line = ax.plot(
            m_mean["rho_eff"],
            m_mean["cv_sp"],
            marker=marker,
            label=f"mixed S={s}",
        )[0]
        p_line = ax.plot(
            p_mean["rho_eff"],
            p_mean["cv_sp"],
            marker=marker,
            ls="--",
            label=f"positive S={s}",
        )[0]
        ax.scatter(
            m_rep["rho_eff"],
            m_rep["cv_sp"],
            s=10,
            alpha=0.15,
            color=m_line.get_color(),
            marker=marker,
            edgecolors="none",
            label="_nolegend_",
        )
        ax.scatter(
            p_rep["rho_eff"],
            p_rep["cv_sp"],
            s=10,
            alpha=0.15,
            color=p_line.get_color(),
            marker=marker,
            edgecolors="none",
            label="_nolegend_",
        )

        m_out = m_mean.copy()
        m_out["slope_mode"] = "mixed"
        m_out["n_species"] = s
        m_out["sigma_env"] = sigma_target
        p_out = p_mean.copy()
        p_out["slope_mode"] = "positive"
        p_out["n_species"] = s
        p_out["sigma_env"] = sigma_target
        summary_rows.extend([m_out, p_out])

    ax.set(
        title=rf"Approx. species-level CV vs $\rho_{{\mathrm{{env}}}}$ ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel=r"Approx. $\mathrm{CV}_{\mathrm{sp}}$",
    )
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

    if summary_rows and summary_out_path is not None:
        pd.concat(summary_rows, ignore_index=True).to_csv(summary_out_path, index=False)


def ensure_reports(summary_df: pd.DataFrame, out_prefix: Path) -> None:
    """Write per-run heatmaps and summary CSV for a cached summary frame."""
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    summary_df = ensure_effective_rho(summary_df)
    metric_labels = {
        "cv_total": r"$\mathrm{CV}_{\mathrm{tot}}$",
        "phi_ldm": r"$\phi_{\mathrm{LdM}}$",
    }
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
        fig, axes = plt.subplots(1, len(richness), figsize=(4 * len(richness), 4), constrained_layout=True)
        axes_list = [axes] if len(richness) == 1 else list(np.ravel(axes))
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

    summary_df.to_csv(out_prefix.with_name(out_prefix.name + "_summary.csv"), index=False)


def make_panel(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    """Create the main mixed-vs-positive comparison panel."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    summary_mixed = ensure_effective_rho(summary_mixed)
    summary_pos = ensure_effective_rho(summary_pos)

    table = summary_mixed[summary_mixed["n_species"] == 4].pivot_table(
        index="rho_eff", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    table_pos = summary_pos[summary_pos["n_species"] == 4].pivot_table(
        index="rho_eff", columns="sigma_env", values="cv_total", aggfunc="mean"
    )
    vmin_shared = float(np.nanmin([np.nanmin(table.values), np.nanmin(table_pos.values)]))
    vmax_shared = float(np.nanmax([np.nanmax(table.values), np.nanmax(table_pos.values)]))

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

    ax = axes[1, 1]
    mixed_sync = summary_mixed[summary_mixed["sigma_env"] > 0].copy()
    pos_sync = summary_pos[summary_pos["sigma_env"] > 0].copy()
    mixed_scatter = (
        mixed_sync.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False)["mean_pairwise_corr"]
        .mean()
        .dropna()
    )
    pos_scatter = (
        pos_sync.groupby(["n_species", "sigma_env", "rho_eff"], as_index=False)["mean_pairwise_corr"]
        .mean()
        .dropna()
    )
    ax.scatter(mixed_scatter["rho_eff"], mixed_scatter["mean_pairwise_corr"], s=20, alpha=0.5, label="mixed")
    ax.scatter(pos_scatter["rho_eff"], pos_scatter["mean_pairwise_corr"], s=20, alpha=0.5, label="positive")
    ax.axline((0, 0), (1, 1), color="k", linestyle="--", linewidth=0.8, label="y=x")
    ax.set(
        title="Imposed vs realised synchrony",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Realised log-growth corr",
    )
    ax.legend()

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
    if out_path.suffix.lower() == ".png":
        fig.savefig(out_path.with_suffix(".pdf"))
    plt.close(fig)


def make_synchrony_panels(summary_mixed: pd.DataFrame, summary_pos: pd.DataFrame, out_path: Path) -> None:
    """Panels separating imposed vs realised synchrony by slope mode and delta."""
    sigma_target = 0.5
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)
    summary_mixed = ensure_effective_rho(summary_mixed)
    summary_pos = ensure_effective_rho(summary_pos)

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
        ylabel="Realised log-growth corr",
    )
    ax.legend(fontsize=8)

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
        ylabel="Realised log-growth corr",
    )
    ax.legend(fontsize=8)

    ax = axes[2]
    for label, df_mean, marker in [("mixed", mixed_mean, "o"), ("positive", pos_mean, "s")]:
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
        title="Realised - imposed correlation",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Delta log-growth corr",
    )
    ax.legend(fontsize=8)

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
    summary_mixed = ensure_effective_rho(summary_mixed)
    sigma_positive = np.asarray(summary_mixed["sigma_env"], dtype=float) > 0
    summary_mixed = summary_mixed.loc[sigma_positive, :].copy()
    grp = (
        summary_mixed.groupby(["n_species", "sigma_env", "rho_eff"])[
            ["cv_total", "phi_ldm", "mean_pairwise_corr"]
        ]
        .mean()
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    ax = axes[0]
    for s, sub in grp.groupby("n_species"):
        ax.scatter(sub["phi_ldm"], sub["cv_total"], s=25, alpha=0.6, label=f"S={s}")
    ax.set_xlabel(r"Synchrony $\phi_{\mathrm{LdM}}$")
    ax.set_ylabel(r"$\mathrm{CV}_{\mathrm{tot}}$")
    ax.set_title(r"$\mathrm{CV}_{\mathrm{tot}}$ vs $\phi_{\mathrm{LdM}}$ (mixed slopes)")
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.9))

    ax = axes[1]
    for s, sub in grp.groupby("n_species"):
        ax.scatter(sub["mean_pairwise_corr"], sub["cv_total"], s=25, alpha=0.6, label=f"S={s}")
    ax.set_xlabel("Mean pairwise realised log-growth corr")
    ax.set_title(r"$\mathrm{CV}_{\mathrm{tot}}$ vs realised log-growth corr (mixed slopes)")

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
    """Overlay CV-vs-rho curves across phi values for reduced grids."""
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
    """Plot mean community CV vs richness for mixed slopes."""
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
    """Control plot: aligned slopes with matched magnitudes vs mixed slopes."""
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
        title=rf"Realised log-growth corr vs $\rho_{{\mathrm{{env}}}}$ ($\sigma_{{\mathrm{{env}}}}={sigma_target}$)",
        xlabel=r"$\rho_{\mathrm{env}}$",
        ylabel="Realised log-growth corr",
    )
    ax.legend(fontsize=8, ncol=2)

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
