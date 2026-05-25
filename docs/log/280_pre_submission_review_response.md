# 280 Pre-submission Review Response

Date: 2026-05-23

## Goal

Address the highest-value points from the independent pre-submission review before Barry's final human-scientist pass, without changing production numerical outputs unless a new gap is discovered.

## Scope

- Main manuscript, cover letter, figure captions, main/supplementary tables, and supplementary information.
- Existing production summaries under `data/sim/production/`.
- Lightweight diagnostic code/tests for production-derived variance decomposition and Figure 4 association checks.
- No new `deep-server` simulation launches in this pass.

## Changes Made

- Added an explicit first-order environmental-response covariance argument showing how $b_i b_j$ maps driver covariance into reinforcing or compensatory growth forcing.
- Corrected the deterministic equilibrium expression to include $r_0$ and clarified the production simplification at $r_0=1$.
- Replaced the inaccurate common-random-number/paired-replicate wording with deterministic independent seeding across scenarios.
- Clarified that the growth-correlation metric is realised per-capita log-growth correlation, not the direct environmental forcing term.
- Revised richness wording: increasing $S$ fills the fixed mixed-slope range more densely rather than widening it, and odd-richness grids include a zero-slope species.
- Reframed Figure 5 as a persistence–stationary-variance stress gradient rather than a pure autocorrelation sensitivity.
- Brought the production positive-matched sign-structure control into the main Results.
- Added production-derived variance-decomposition and compact Figure 4 partial-association diagnostics under `analysis/reports/`.
- Added `alpha_inter` to legacy `analysis/run_full_grid.py` outputs for consistency with production summaries.

## Evidence So Far

- `uv run python analysis/summarize_production_diagnostics.py`: passed; wrote `analysis/reports/variance_decomposition_fig2_mixed_summary.csv`, `analysis/reports/variance_decomposition_fig2_mixed_selected_summary.csv`, and `analysis/reports/fig4_partial_association_summary.csv`.
- `uv run pytest tests/python/test_diagnostics.py tests/python/test_analysis_workflows.py -q`: 6 passed.
- `uv run pytest -q`: 47 passed.
- `uv run pyright`: 0 errors, 0 warnings, 0 informations.
- `git diff --check`: clean.
- `uv run python analysis/run_all.py --skip-guard-audit`: passed using production summaries only, regenerated figures, and copied manuscript figure assets.
- makedoc `make check` passed sequentially for `ih_submission`, `ih_supplementary_info`, `ih_author_title_page`, and `ih_cover_letter`.
- `uv run python scripts/sanitize_docx_identity.py --check ...`: passed for the rebuilt blinded main and anonymous supplementary DOCX outputs.
- PDF text scans found no project-author identifiers or title-page placeholders in the rebuilt blinded main or supplementary PDFs.
- Contact-sheet visual checks of the rebuilt blinded main and supplementary PDFs showed no obvious page-break or figure/table rendering failures.

## Remaining Follow-up

- Verify current Oikos/NSO submission-file instructions before making final file-composition changes.
- Decide whether Figure 1 warrants a comparative redesign after the strengthened analytical mechanism is reviewed.
- Build the de-identified review-code package after final code lock.
