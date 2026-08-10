# 320 Fresh-model manuscript and artefact review

Date: 2026-07-10

## Scope

- Re-read the main manuscript, legends, tables, supplementary information, cover letter, title page, submission statements, code-facing model definitions, production summaries, and canonical bibliography.
- Applied the `audit-ai-writing` workflow first, then performed a separate scientific consistency and readability pass.
- Used this repository's `paper/references/ih_references.yaml`; no files or references from the concurrently active `rc-dates` paper were used.

## Writing and framing changes

- Reworked dense or formulaic passages into more direct scientific prose while retaining a single-author voice and the manuscript's compact structure.
- Reframed environmental forcing as correlated species-specific exposures rather than identical signals, and separated the operational definition of insurance from synchrony metrics used as mechanistic diagnostics.
- Revised the title to avoid implying that aligned communities receive no statistical-averaging benefit from richness.
- Tightened the cover letter around the paper's specific contribution to the response-diversity agenda and made the rendered letter fit on one page.

## Scientific consistency changes

- Standardised the simulated state variable and response metric as population and total abundance. The implementation sums unweighted abundances, so model-specific references to total biomass were inaccurate.
- Corrected the richness interpretation: total abundance increases with richness and covariance terms are negative in the selected decomposition, but total variance and covariance magnitude are not monotonic at every richness step.
- Qualified the deterministic richness sequence as denser sampling of a fixed slope range, not a pure richness manipulation at fixed response composition.
- Corrected Figure 3C text to report positive aligned-slope $\Delta\mathrm{corr}$ at low imposed correlation, values near zero in the middle, and modestly negative values only at the high end.
- Qualified the mixed-narrow control: its CV contrast is consistent, whereas the synchrony ordering reverses in some most-negative-correlation boundary scenarios.
- Restricted the temporal-persistence interpretation to the mixed-slope communities actually simulated and described Figure 4 as a raw/conditional association rather than an independent mediation test.
- Clarified that floor occupancy is a numerical stress diagnostic, not irreversible biological extinction.

## Literature and display items

- Cross-checked recent claims against the canonical bibliography and corrected the interpretation of the 2026 nitrogen-addition study.
- Updated the former Ross response-diversity preprint record to its 2026 Oikos publication (`10.1002/oik.11358`) and added the DOI to the Zotero import list.
- Kept accepted figure designs unchanged, but made captions more self-contained and corrected Figure 3's sign description.
- Removed the near-blank Table 1 overflow page, reorganised over-wide supplementary tables around compact run labels, retained exact production run IDs as copyable text, and placed Table S5 intact on one page.

## Verification

- `uv run pytest -q`: 50 passed.
- `uv run pyright`: 0 errors, warnings, or information messages.
- makedoc checks passed for all six profiles: `ih_submission`, `ih_supplementary_info`, `ih_submission_form_statements`, `ih_cover_letter`, `ih_author_title_page`, and `ih_draft`.
- Main-manuscript reference audit: 30 bibliography keys, 26 cited, 0 unknown, 4 unused.
- Blinded main, supplementary, and submission-statement DOCX files passed identity sanitising and `--check` verification.
- Rendered PDFs were inspected at full-page resolution. The blinded main is 34 pages, the supplement is 12 pages, and the cover letter is one page.

## Remaining author decisions

- Confirm funding and acknowledgement text, title-page metadata, cover-letter voice, and the permanent archive/DOI destination.
- The makedoc `captions_page` mode inserts a standalone `Supplementary Information` divider before supplementary figure pages. It contains no missing content and is an upstream pagination convention rather than a manuscript-source defect.
