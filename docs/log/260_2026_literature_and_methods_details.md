# 260 2026 Literature and Methods Details

Date: 2026-05-21

## Goal

Address two pre-Barry-pass notes:

- Add a brief Methods sentence about Python 3.12 and the main analysis imports used for the simulation experiments.
- Refresh the manuscript against 2026 literature published since the December 2025 literature scan, verify DOIs, and provide a one-DOI-per-line import helper for Zotero.

## Literature Scan

Targeted searches focused on response diversity, biodiversity-stability, synchrony, and insurance-hypothesis terms for 2026 publications. Four additions were selected because they directly support the manuscript's response-diversity/synchrony frame:

- Hsieh et al. 2026, Nature Communications: dynamic response diversity and ecosystem stability.
- Sasaki et al. 2026, Nature Communications: biological traits and time-varying species responses to multiple global-change drivers.
- Kunze et al. 2026, Ecology Letters: response diversity, species interactions, and community stability under pulse disturbances.
- Song et al. 2026, Oecologia: synchrony and population variability as mechanisms reducing grassland stability under nitrogen enrichment.

Broader 2026 biodiversity-stability papers were not added when they did not directly sharpen the response-diversity, realised-synchrony, or mechanistic environmental-response framing.

## Changes

- Added the four references to `paper/references/ih_references.yaml`.
- Added `paper/references/ih_2026_doi_import.txt` as a plain one-DOI-per-line Zotero import helper.
- Cited the 2026 response-diversity and response-trait papers in the Introduction.
- Added the 2026 synchrony/stability paper to the empirical synchrony paragraph.
- Added a Methods subsection documenting Python 3.12 and the main analysis stack (`numpy`, `pandas`, `pyarrow`, `scipy`, `matplotlib`, standard-library orchestration tools, `pytest`, and `pyright`).

## Validation

- Parsed `paper/references/ih_references.yaml` successfully and confirmed all four new citekeys are present.
- Ran makedoc `make check` for `ih_submission`, `ih_supplementary_info`, and `ih_author_title_page`; all passed with reference audits clean of unknown keys.
- Confirmed the blinded main manuscript PDF contains the new 2026 citations and the Python 3.12 implementation sentence.
- Re-scanned the blinded main manuscript PDF for author-identifying strings after the bibliography update; no project-author identifiers were found.
- Ran `uv run pytest -q`: 45 passed.
- Ran `uv run pyright`: 0 errors, 0 warnings, 0 informations.
- Ran `git diff --check`: clean.
