"""End-to-end runner for the insurance hypothesis simulations and figures.

Default behaviour (no flags):
- Uses existing simulation outputs under data/sim/grid/ (run1, pos_full, phi0/07/09/095_reduced).
- Regenerates summary tables and figures into analysis/reports/.
- Copies key panels into paper/manuscript/figures/.

Optional: rerun simulations with `--rerun-data`, which will rerun a smaller set
of grids with the same configurations used in the paper. This is slower
(several minutes).
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import pandas as pd

from insurance_sim.figures import (
    ensure_reports,
    make_cv_vs_synchrony,
    make_panel,
    make_phi_overlay,
    make_positive_matched_control,
    make_richness_scaling,
    make_species_cv_diagnostic,
    make_synchrony_panels,
)
from insurance_sim.reporting import (
    DEFAULT_DATA_RUNS,
    copy_existing_files,
    load_summary,
    remove_existing_files,
    summarize_numerical_guard_csv,
    validate_phi_run_lengths,
    write_guard_summary_markdown,
)
from insurance_sim.production_figures import (
    write_production_fig1,
    write_production_fig2_richness,
    write_production_fig3_synchrony,
    write_production_fig4_cv_synchrony,
)

REPORTS = Path("analysis/reports")
FIG_DIR = Path("paper/manuscript/figures")
DATA_RUNS = DEFAULT_DATA_RUNS
FIG1_PRODUCTION_CORE = Path("data/sim/production/fig1_s4_highres_v1/summaries.parquet")
FIG1_PRODUCTION_HIGHSIGMA = Path("data/sim/production/fig1_s4_highsigma_v1/summaries.parquet")
FIG2_PRODUCTION_RICHNESS = Path("data/sim/production/fig2_richness_mixed_v1/summaries.parquet")
FIG3_PRODUCTION_SYNCHRONY = Path("data/sim/production/fig3_synchrony_v1/summaries.parquet")


def run_command(cmd: list[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def rerun_data() -> None:
    for name, spec in DATA_RUNS.items():
        args = ["python", "analysis/run_full_grid.py", "--run-name", name, *spec.args]
        run_command(["uv", "run"] + args)


def summarize_numerical_guards() -> None:
    """Run and summarise numerical-guard diagnostics for manuscript transparency."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    run_command(["uv", "run", "python", "analysis/check_numerical_guards.py"])

    in_path = REPORTS / "numerical_guard_rates.csv"
    if not in_path.exists():
        print(f"Warning: missing expected guard diagnostics file: {in_path}")
        return

    summary = summarize_numerical_guard_csv(in_path)
    out_csv = REPORTS / "numerical_guard_rates_summary.csv"
    summary.to_csv(out_csv, index=False)
    write_guard_summary_markdown(summary, REPORTS / "numerical_guard_rates_summary.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simulations and regenerate figures")
    parser.add_argument("--rerun-data", action="store_true", help="Rerun simulations instead of using cached parquet files")
    parser.add_argument(
        "--skip-guard-audit",
        action="store_true",
        help="Skip numerical-guard diagnostics refresh (enabled by default).",
    )
    args = parser.parse_args()

    if args.rerun_data:
        rerun_data()

    if not args.skip_guard_audit:
        summarize_numerical_guards()

    # Load summaries
    summary_mixed = load_summary(DATA_RUNS["run1"].path)
    summary_pos = load_summary(DATA_RUNS["pos_full"].path)
    summary_pos_matched = load_summary(DATA_RUNS["pos_matched"].path) if DATA_RUNS["pos_matched"].path.exists() else None
    phi_runs = {
        key: load_summary(spec.path)
        for key, spec in DATA_RUNS.items()
        if key.startswith("phi")
    }
    validate_phi_run_lengths(phi_runs)

    # Per-run summary figs
    ensure_reports(summary_mixed, REPORTS / "run1")
    ensure_reports(summary_pos, REPORTS / "pos_full")
    if summary_pos_matched is not None:
        ensure_reports(summary_pos_matched, REPORTS / "pos_matched")
    for key, df in phi_runs.items():
        ensure_reports(df, REPORTS / key)

    # Panels
    panel_path = REPORTS / "fig1_panels.png"
    panel_pdf_path = panel_path.with_suffix(".pdf")
    if FIG1_PRODUCTION_CORE.exists() and FIG1_PRODUCTION_HIGHSIGMA.exists():
        write_production_fig1(
            core_path=FIG1_PRODUCTION_CORE,
            highsigma_path=FIG1_PRODUCTION_HIGHSIGMA,
            out_png=panel_path,
            out_pdf=panel_pdf_path,
            summary_out=REPORTS / "fig1_panels_summary.csv",
        )
    else:
        make_panel(summary_mixed, summary_pos, panel_path)

    sync_panel_path = REPORTS / "fig3_imposed_vs_realised_panels.png"
    sync_panel_pdf_path = sync_panel_path.with_suffix(".pdf")
    if FIG3_PRODUCTION_SYNCHRONY.exists():
        write_production_fig3_synchrony(
            production_path=FIG3_PRODUCTION_SYNCHRONY,
            out_png=sync_panel_path,
            out_pdf=sync_panel_pdf_path,
            summary_out=REPORTS / "fig3_imposed_vs_realised_panels_summary.csv",
        )
    else:
        make_synchrony_panels(summary_mixed, summary_pos, sync_panel_path)

    phi_overlay_path = REPORTS / "fig5_phi_sensitivity_sigma0.5_extended.png"
    make_phi_overlay(phi_runs, phi_overlay_path)

    cv_sync_path = REPORTS / "fig4_cv_vs_synchrony_mixed.png"
    cv_sync_pdf_path = cv_sync_path.with_suffix(".pdf")
    if FIG2_PRODUCTION_RICHNESS.exists():
        write_production_fig4_cv_synchrony(
            production_path=FIG2_PRODUCTION_RICHNESS,
            out_png=cv_sync_path,
            out_pdf=cv_sync_pdf_path,
            summary_out=REPORTS / "fig4_cv_vs_synchrony_mixed_summary.csv",
        )
    else:
        make_cv_vs_synchrony(summary_mixed, cv_sync_path)

    # Richness scaling curve (prefer dedicated richness sweep if available)
    richness_path = Path("data/sim/grid/run1_richness/summaries.parquet")
    if richness_path.exists():
        richness_df = pd.read_parquet(richness_path)
    else:
        richness_df = summary_mixed
    richness_fig_path = REPORTS / "fig2_richness_scaling_mixed.png"
    richness_fig_pdf_path = richness_fig_path.with_suffix(".pdf")
    if FIG2_PRODUCTION_RICHNESS.exists():
        write_production_fig2_richness(
            production_path=FIG2_PRODUCTION_RICHNESS,
            out_png=richness_fig_path,
            out_pdf=richness_fig_pdf_path,
            summary_out=REPORTS / "fig2_richness_scaling_mixed_summary.csv",
        )
    else:
        make_richness_scaling(richness_df, richness_fig_path)

    species_cv_path = REPORTS / "figS4_species_cv_vs_rho.png"
    make_species_cv_diagnostic(
        summary_mixed,
        summary_pos,
        species_cv_path,
        summary_out_path=REPORTS / "figS4_species_cv_vs_rho_summary.csv",
    )

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

    # Copy key panels to paper/manuscript/figures
    figure_paths = [
        panel_path,
        panel_pdf_path,
        sync_panel_path,
        sync_panel_pdf_path,
        cv_sync_path,
        cv_sync_pdf_path,
        phi_overlay_path,
        supp_cv_path,
        supp_phi_path,
        species_cv_path,
        richness_fig_path,
        richness_fig_pdf_path,
    ]
    if matched_path is not None:
        figure_paths.append(matched_path)
    copy_existing_files(figure_paths, FIG_DIR)

    # Remove stale supplementary filenames after transition to figS* names.
    remove_existing_files(
        [
            FIG_DIR / "run1_cv_total.png",
            FIG_DIR / "run1_phi_ldm.png",
            REPORTS / "positive_matched_control.png",
            FIG_DIR / "positive_matched_control.png",
        ]
    )

    print("Run complete. Figures in analysis/reports and paper/manuscript/figures.")


if __name__ == "__main__":
    main()
