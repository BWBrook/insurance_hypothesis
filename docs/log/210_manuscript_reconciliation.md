# 210 Manuscript Reconciliation Against Production Figures

Date: 2026-05-18

## Goal

Re-check the draft manuscript and figure captions after Barry accepted production Figures 1-5, before moving on to Table 1 and supplementary artefacts.

## Scope

- Main production figures: Figures 1-5 in `analysis/reports/` and `paper/manuscript/figures/`.
- Manuscript text: `paper/manuscript/text/draft_ms_v2.md`.
- Captions: `paper/manuscript/text/figure_captions_v2.md`.
- Living interpretation/project notes: `docs/plan.md`, `docs/interpretation_notes.md`, and `docs/q_and_a_interpretation.md`.

## Changes

- Updated the manuscript Methods so the five main figures are described as production-scale grids with 1000 replicates per scenario.
- Distinguished production grids from lower-replicate exploratory/control diagnostics.
- Tightened wording around requested `rho_env` and effective `rho_eff`, especially where Results and Discussion compare realised scenario outputs.
- Added stress-regime caveats for high-`sigma_env` and high-`phi` regions where floor occupancy is no longer negligible.
- Updated the Reproducibility note to point to production specs and compact production summaries, not only legacy exploratory grids.
- Recorded Figure 5 acceptance and the agreed next artefact order: Table 1, supplementary figures, supplementary tables, then final build/lint.

## Remaining Work

- Table 1 is still stale relative to the production grids and should be replaced next.
- Supplementary figures and supplementary tables still need a full sweep against the accepted main-figure story.
- A final manuscript build/lint pass should wait until Table 1 and supplementary artefacts are updated.
