"""Regenerate all manuscript figures and analysis summaries from production data."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

# Keep generated PDF metadata reproducible while allowing an explicit caller override.
os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

from insurance_sim.diagnostics import (
    select_variance_decomposition_rows,
    summarize_variance_decomposition,
)
from insurance_sim.production_figures import (
    write_production_fig1,
    write_production_fig2_richness,
    write_production_fig3_synchrony,
    write_production_fig4_weighted_boundary,
    write_production_fig5_persistence,
    write_production_figs3_positive_matched_control,
    write_production_mixed_heatmap_supplement,
    write_production_species_cv_supplement,
)


REPORTS = Path("analysis/reports")
PRODUCTION_INPUTS = {
    "fig1_core": Path("data/sim/production/fig1_s4_highres_v1/summaries.parquet"),
    "fig1_highsigma": Path("data/sim/production/fig1_s4_highsigma_v1/summaries.parquet"),
    "fig2_richness": Path("data/sim/production/fig2_richness_mixed_v1/summaries.parquet"),
    "fig3_synchrony": Path("data/sim/production/fig3_synchrony_v1/summaries.parquet"),
    "fig5_persistence": Path("data/sim/production/fig5_persistence_mixed_v1/summaries.parquet"),
    "figs3_positive_matched": Path(
        "data/sim/production/figs3_positive_matched_control_v1/summaries.parquet"
    ),
    "fig4_weighted_boundary": Path(
        "data/sim/production/fig4_weighted_balance_r0_v1/summaries.parquet"
    ),
}


def require_production_inputs() -> None:
    """Fail once, with the complete list of missing production summaries."""
    missing = [path for path in PRODUCTION_INPUTS.values() if not path.is_file()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(
            "Missing production summaries required to regenerate the paper:\n"
            f"{formatted}\n"
            "Retrieve the compact review data or rebuild the runs from "
            "analysis/production_specs/."
        )


def write_production_diagnostics(production_path: Path) -> None:
    """Write the production-derived diagnostic tables used by the manuscript."""
    df = pd.read_parquet(production_path)
    variance = summarize_variance_decomposition(df)
    variance.to_csv(REPORTS / "variance_decomposition_fig2_mixed_summary.csv", index=False)
    select_variance_decomposition_rows(variance).to_csv(
        REPORTS / "variance_decomposition_fig2_mixed_selected_summary.csv",
        index=False,
    )


def main() -> None:
    require_production_inputs()
    REPORTS.mkdir(parents=True, exist_ok=True)

    write_production_fig1(
        core_path=PRODUCTION_INPUTS["fig1_core"],
        highsigma_path=PRODUCTION_INPUTS["fig1_highsigma"],
        out_png=REPORTS / "fig1_panels.png",
        out_pdf=REPORTS / "fig1_panels.pdf",
        summary_out=REPORTS / "fig1_panels_summary.csv",
    )
    write_production_fig2_richness(
        production_path=PRODUCTION_INPUTS["fig2_richness"],
        out_png=REPORTS / "fig2_richness_scaling_mixed.png",
        out_pdf=REPORTS / "fig2_richness_scaling_mixed.pdf",
        summary_out=REPORTS / "fig2_richness_scaling_mixed_summary.csv",
    )
    write_production_fig3_synchrony(
        production_path=PRODUCTION_INPUTS["fig3_synchrony"],
        out_png=REPORTS / "fig3_imposed_vs_realised_panels.png",
        out_pdf=REPORTS / "fig3_imposed_vs_realised_panels.pdf",
        summary_out=REPORTS / "fig3_imposed_vs_realised_panels_summary.csv",
    )
    write_production_fig4_weighted_boundary(
        matched_path=PRODUCTION_INPUTS["figs3_positive_matched"],
        sensitivity_path=PRODUCTION_INPUTS["fig4_weighted_boundary"],
        out_png=REPORTS / "fig4_weighted_balance_boundary.png",
        out_pdf=REPORTS / "fig4_weighted_balance_boundary.pdf",
        summary_out=REPORTS / "fig4_weighted_balance_boundary_summary.csv",
    )
    write_production_fig5_persistence(
        production_path=PRODUCTION_INPUTS["fig5_persistence"],
        out_png=REPORTS / "fig5_phi_sensitivity_sigma0.5_extended.png",
        out_pdf=REPORTS / "fig5_phi_sensitivity_sigma0.5_extended.pdf",
        summary_out=REPORTS / "fig5_phi_sensitivity_sigma0.5_extended_summary.csv",
    )

    write_production_mixed_heatmap_supplement(
        production_path=PRODUCTION_INPUTS["fig2_richness"],
        metric="cv_total",
        metric_label=r"Mean $\mathrm{CV}_{\mathrm{tot}}$",
        out_png=REPORTS / "figS1_production_mixed_cv_total.png",
        out_pdf=REPORTS / "figS1_production_mixed_cv_total.pdf",
        summary_out=REPORTS / "figS1_production_mixed_cv_total_summary.csv",
    )
    write_production_mixed_heatmap_supplement(
        production_path=PRODUCTION_INPUTS["fig2_richness"],
        metric="phi_ldm",
        metric_label=r"Mean $\phi_{\mathrm{LdM}}$",
        out_png=REPORTS / "figS2_production_mixed_phi_ldm.png",
        out_pdf=REPORTS / "figS2_production_mixed_phi_ldm.pdf",
        summary_out=REPORTS / "figS2_production_mixed_phi_ldm_summary.csv",
    )
    write_production_figs3_positive_matched_control(
        production_path=PRODUCTION_INPUTS["figs3_positive_matched"],
        out_png=REPORTS / "figS3_positive_matched_control.png",
        out_pdf=REPORTS / "figS3_positive_matched_control.pdf",
        summary_out=REPORTS / "figS3_positive_matched_control_summary.csv",
    )
    write_production_species_cv_supplement(
        production_path=PRODUCTION_INPUTS["fig3_synchrony"],
        out_png=REPORTS / "figS4_production_species_cv_vs_rho.png",
        out_pdf=REPORTS / "figS4_production_species_cv_vs_rho.pdf",
        summary_out=REPORTS / "figS4_production_species_cv_vs_rho_summary.csv",
    )
    write_production_diagnostics(PRODUCTION_INPUTS["fig2_richness"])
    print("Regenerated manuscript figures and summaries in analysis/reports/.")


if __name__ == "__main__":
    main()
