# 270 Final Submission Chaperone Pass

Date: 2026-05-21

## Goal

Complete the last technical chaperone pass before Barry's human-scientist review of the Oikos submission package.

## Scope

- Oikos-oriented build profiles and generated outputs.
- Blinded main manuscript, anonymous supplementary information, unblinded title page, and cover letter.
- Figure captions, supplementary references, rendered PDF/DOCX metadata, and production-summary numerical claims.
- No new simulation science and no changes to numerical outputs or model definitions.

## Issues Found And Fixed

- No cover letter existed in the repo. Added `paper/manuscript/text/cover_letter.md` and a separate `ih_cover_letter` build profile.
- Build-facing figure files were rendering only one-line image alt text as captions. Expanded `figures_main.md`, `supplementary_figures.md`, and the combined draft `figures.md` to carry the full informative captions.
- One Introduction citation still contained a hard-coded `Wagg et al. 2022` string. Replaced it with the bibliography-backed `wagg2021DiversityAsynchronySoil` citation.
- Main-text references to specific supplementary items were softened to "Supporting information" to better align with Oikos guidance.
- Generated DOCX files retained invisible local-path metadata in image descriptions and custom bibliography/CSL properties. Added `scripts/sanitize_docx_identity.py` and sanitized the generated DOCX outputs.
- Parallel makedoc profile checks can race through shared build cache state. Final builds were rerun sequentially, and the checklist now records sequential builds as the safe path.

## Evidence

- `uv run pytest -q`: 45 passed.
- `uv run pyright`: 0 errors, 0 warnings, 0 informations.
- `git diff --check`: clean.
- makedoc `make check` passed sequentially for `ih_submission`, `ih_supplementary_info`, `ih_author_title_page`, and `ih_cover_letter`.
- makedoc `make validate-config` passed for the default config path.
- `uv run python analysis/run_all.py --skip-guard-audit` completed using production summaries and copied current figure artefacts to `paper/manuscript/figures/`.
- `uv run python scripts/sanitize_docx_identity.py --check` passed for the blinded main and anonymous supplementary DOCX outputs.
- Rendered PDF scans found no project-author identifiers in the blinded main or supplementary information.
- Numerical spot checks against production CSV/parquet outputs still match the manuscript claims for Figure 4 correlations, Figure 5 persistence values, scenario counts, replicate counts, and floor-occupancy summaries.

## Remaining Human Items

- Barry should review the scientific interpretation, stress-region caveats, and cover letter tone.
- Funding and acknowledgements remain placeholders on the unblinded title page.
- The de-identified review-code package remains intentionally deferred until final code lock.
