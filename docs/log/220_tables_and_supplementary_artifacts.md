# 220 Tables and Supplementary Artefacts

Date: 2026-05-19

## Goal

Replace the stale Table 1 placeholder with production-aligned model/run information, then sweep supplementary figures and supplementary tables against the accepted production Figure 1-5 story.

## Changes

- Replaced `paper/manuscript/text/tables.md` with:
  - Table 1: core model parameters and main production grids.
  - Table S1: production run inventory, scenario counts, and replicate-row counts.
  - Table S2: production floor-occupancy summary and stress-region interpretation.
  - Table S3: lower-replicate robustness/control grids.
- Added production-backed supplementary figure helpers in `src/python/insurance_sim/production_figures.py`.
- Added `analysis/plot_production_supplementary.py` as a thin entry point for regenerating production-backed supplementary Figures S1, S2, and S4.
- Rebuilt:
  - `analysis/reports/figS1_production_mixed_cv_total.png` and `.pdf`
  - `analysis/reports/figS1_production_mixed_cv_total_summary.csv`
  - `analysis/reports/figS2_production_mixed_phi_ldm.png` and `.pdf`
  - `analysis/reports/figS2_production_mixed_phi_ldm_summary.csv`
  - `analysis/reports/figS4_production_species_cv_vs_rho.png` and `.pdf`
  - `analysis/reports/figS4_production_species_cv_vs_rho_summary.csv`
- Removed superseded coarse-grid supplementary filenames for S1, S2, and S4.
- Updated `paper/manuscript/text/figures.md`, `paper/manuscript/text/figure_captions_v2.md`, and `README.md` to point to the production-backed supplementary artefacts.

## Interpretation

- Figures S1 and S2 now use the same validated `fig2-richness-mixed-v1` production grid as Figures 2 and 4.
- Figure S4 now uses the validated `fig3-synchrony-v1` production grid at `sigma_env=0.5`.
- Figure S3 was subsequently selected for a focused production refresh; see `docs/log/230_figS3_production_control.md`.

## Remaining Work

- Final manuscript build/lint pass completed after the Figure S3 production refresh; see `docs/log/230_figS3_production_control.md`.
- Figure S3 production refresh is complete; decide later only whether the remaining no-competition and mixed-narrow controls need production-scale reinforcement.
