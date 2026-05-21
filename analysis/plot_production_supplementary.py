"""Build production-backed supplementary figures.

Usage:
  uv run python analysis/plot_production_supplementary.py
"""

from __future__ import annotations

from pathlib import Path

from insurance_sim.production_figures import (
    write_production_figs3_positive_matched_control,
    write_production_mixed_heatmap_supplement,
    write_production_species_cv_supplement,
)

REPORTS = Path("analysis/reports")
FIG2_PRODUCTION_RICHNESS = Path("data/sim/production/fig2_richness_mixed_v1/summaries.parquet")
FIG3_PRODUCTION_SYNCHRONY = Path("data/sim/production/fig3_synchrony_v1/summaries.parquet")
FIGS3_PRODUCTION_POS_MATCHED = Path("data/sim/production/figs3_positive_matched_control_v1/summaries.parquet")


def main() -> None:
    """Write supplementary figures S1-S4 from production summaries."""
    write_production_mixed_heatmap_supplement(
        production_path=FIG2_PRODUCTION_RICHNESS,
        metric="cv_total",
        metric_label=r"Mean $\mathrm{CV}_{\mathrm{tot}}$",
        out_png=REPORTS / "figS1_production_mixed_cv_total.png",
        out_pdf=REPORTS / "figS1_production_mixed_cv_total.pdf",
        summary_out=REPORTS / "figS1_production_mixed_cv_total_summary.csv",
    )
    write_production_mixed_heatmap_supplement(
        production_path=FIG2_PRODUCTION_RICHNESS,
        metric="phi_ldm",
        metric_label=r"Mean $\phi_{\mathrm{LdM}}$",
        out_png=REPORTS / "figS2_production_mixed_phi_ldm.png",
        out_pdf=REPORTS / "figS2_production_mixed_phi_ldm.pdf",
        summary_out=REPORTS / "figS2_production_mixed_phi_ldm_summary.csv",
    )
    write_production_figs3_positive_matched_control(
        production_path=FIGS3_PRODUCTION_POS_MATCHED,
        out_png=REPORTS / "figS3_positive_matched_control.png",
        out_pdf=REPORTS / "figS3_positive_matched_control.pdf",
        summary_out=REPORTS / "figS3_positive_matched_control_summary.csv",
    )
    write_production_species_cv_supplement(
        production_path=FIG3_PRODUCTION_SYNCHRONY,
        out_png=REPORTS / "figS4_production_species_cv_vs_rho.png",
        out_pdf=REPORTS / "figS4_production_species_cv_vs_rho.pdf",
        summary_out=REPORTS / "figS4_production_species_cv_vs_rho_summary.csv",
    )


if __name__ == "__main__":
    main()
