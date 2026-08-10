# 330 – Final hard pre-submission review

**Date:** 2026-07-24

## Scope

Performed a final, source-backed review of the Oikos manuscript before author
sign-off. The pass covered:

- scientific claim/result alignment across all six production grids;
- full-manuscript structure, argument, style, and terminology;
- figures, tables, captions, references, title page, cover letter, and
  submission-form statements;
- current Oikos/NSO initial-submission requirements;
- generated PDF/DOCX rendering and anonymous metadata;
- the de-identified code/simulated-data package.

Three bounded independent reviews covered the editorial cold read, scientific
claims and simulation evidence, and submission/display package. Material
findings were then checked against source files and generated outputs in the
root review.

## Scientific evidence checked

- All six compact production summaries validate: 1,156,000 replicate rows in
  total.
- Five selected production rows were regenerated exactly from their recorded
  deterministic seeds.
- Mixed-slope community CV was lower than the aligned-positive CV in all 270
  matched core Figure 1 cells.
- The manuscript’s principal example was confirmed:
  `CV_tot = 0.08395` for mixed slopes versus `0.26345` for aligned positive
  slopes at `sigma_env = 0.5`, `rho_eff = 0.5`, and `S = 4`.
- The magnitude-matched sign control was confirmed at `S = 4`: the mixed and
  positive-matched regimes are nearly identical at `rho_eff = 0`, but diverge
  strongly as environmental correlation increases. Those cells are floor-free.
- Independent variance decomposition confirmed negative aggregate covariance
  for mixed slopes and positive aggregate covariance for the
  magnitude-matched aligned control.
- No-competition, narrower-slope, and persistence/stationary-variance controls
  preserve the central mixed-versus-aligned contrast.

No fatal scientific defect was found. The central result is supported, but the
review identified boundaries that now appear explicitly in the text:

- The richness sequence is not a pure richness manipulation. Slopes always
  span `[-0.5, 0.5]`, so mean squared slope declines from 0.25 at `S = 2` to
  about 0.11 at `S = 8`.
- Mixed slopes are perfectly balanced around zero. The evidence therefore
  supports balanced opposing sensitivities, not arbitrary response
  heterogeneity.
- Richness-averaged curves are monotone, but individual adjacent steps are not:
  30 of 150 absolute-variance steps and 6 of 150 CV steps increase.
- High-persistence curves contain local reversals. They do not overturn the
  overall contrast.
- High-side exponent clipping was absent. Low-side clipping was below 0.01 in
  dedicated checks through `sigma_env <= 1.5`, but reached 0.016–0.021 in
  independent 200-replicate positive-slope checks at `sigma_env = 4`; floor
  occupancy also rises there. Those cells are described as stress tests.
- There are 155 repeated 32-bit seed values across the 1,156,000-row combined
  archive, but none within a scenario. This is a minor cross-grid design
  limitation rather than evidence that the reported contrasts are paired.

## Manuscript and submission edits

The main editorial changes are in
`paper/manuscript/text/draft_ms_v2.md` and related submission sources:

- rewrote and tightened the abstract around the main numeric result;
- substantially shortened the Introduction and sharpened the theory gap;
- corrected the operational definition of insurance and clarified that driver
  correlation is not realised synchrony;
- replaced over-general richness language with “assembly sequence” language;
- added the balanced zero-sum slope limitation;
- corrected production-seed wording and removed internal workflow jargon;
- reported numerical-guard behaviour with measured clipping frequencies;
- narrowed high-persistence and stress-region claims;
- generalized all main-text supplementary citations to “Supporting
  information”;
- condensed the Discussion and conclusion to the supported model scope;
- added the current NSO-required AI-use statement;
- revised the significance and data/code statements;
- removed a duplicated italic title note from the unblinded title page;
- changed the blinded main build from 1.5 to double line spacing.

The AI-writing phrase scanner still labels the Markdown source “high surface
risk”, largely because it counts valid Markdown headings, equation scaffolding,
parallel experimental contrasts, and technical phrases. Its more diagnostic
metrics were low: two vocabulary hits in 5,998 words and no
sentence-opening-transition pattern. Independent manual cold reads did not find
a material generated-prose problem, so no phrase-swapping pass was performed.

Figures, numerical values, and simulation outputs were not regenerated or
altered during the editorial pass.

## Build and visual verification

Fresh sequential makedoc checks passed for:

- `ih_draft`
- `ih_submission`
- `ih_submission_form_statements`
- `ih_supplementary_info`
- `ih_author_title_page`
- `ih_cover_letter`

Each profile passed config validation, lint, author-injection checks, and the
61-test makedoc suite. The main reference audit found 30 bibliography keys, 26
cited keys, zero unknown keys, and four unused non-fatal keys.

The submission golden contract was corrected to count five main drawings and
to tolerate the line-number split in the two-line title. It then passed against
the actual PDF and DOCX: one table, five drawings, 29 PDF pages, and all 12
required text markers.

The direct anonymous submission PDF is 29 A4 pages, double-spaced,
single-column, and continuously line-numbered. It was visually inspected page
by page; the abstract fits on page 1, the Introduction begins on page 2, and all
tables, captions, and five main figures render without clipping. The nine-page
Supporting-information PDF and the title page, cover letter, and
submission-form statements were also visually inspected.

The anonymous main and Supporting-information PDF text/metadata and DOCX
metadata were scanned for author, institution, ORCID, email, repository, and
local-path markers; none were found after the DOCX sanitizer.

LibreOffice renders the generated main DOCX as 42 US-letter pages and starts the
Introduction on page 3. The direct PDF meets the NSO page-2 requirement, and PDF
is explicitly accepted for initial submission, so the PDF is the recommended
initial main-text upload. The DOCX remains an editable fallback.

## Review-package rebuild and defect repaired

The first package rebuild correctly stopped because
`test_submission_helpers.py` contains deliberate identity/path fixtures. That
repository-only test also depends on packaging and DOCX-sanitizer scripts that
are intentionally absent from the anonymous review package. A regression test
was added first, then the builder was corrected to copy only runnable
reproduction tests.

The clean package at
`/home/bwbrook/papers/de_identified_repos/ih_package.zip` was tested from inside
its staging directory:

- `uv sync --python 3.12 --frozen --dev`: passed;
- `uv run pytest -q`: 48 passed;
- `uv run pyright`: zero errors and zero warnings;
- `uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export`:
  completed and regenerated reports.

The final archive was rebuilt after testing to exclude `.venv/` and generated
reports. It has 66 members, six parquet summaries, seven packaged tests, and a
size of 72,617,256 bytes. SHA-256:

`f2cada4521af344fe156023740da4b1475e16cd8ef897dbe1e16d9c65dbbecea`

Included source, tests, analysis scripts, data summaries, and lockfile match the
repository byte-for-byte. The only deliberate transformations are author
anonymization in `pyproject.toml` and execution-host/root anonymization in the
production specifications. Text files and structured parquet metadata/string
fields passed the identity scan; forbidden Git, manuscript, author-metadata,
and submission-helper paths are absent.

## Remaining author decisions

The scientific/editorial package is ready for Barry’s Git-diff review. Actual
submission remains conditional on:

1. replacing the funding placeholder;
2. replacing the acknowledgements placeholder;
3. confirming the conflict statement;
4. confirming the AI-use statement;
5. naming the intended permanent archive;
6. selecting direct review-zip upload versus an anonymous repository route;
7. reading the cover letter once in the author’s own voice.

After any author edits, repeat the affected makedoc profiles, anonymous metadata
scan, visual page check, repository tests/type check, and final package
build/checksum.
