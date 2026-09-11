# Oikos Submission Readiness Checklist

Current against the Oikos and NSO author guidance rechecked on 2026-09-11:

- <https://nso-journals.org/oikos-for-authors>
- <https://nso-journals.org/author-guidelines>

## Files and classification

Canonical generated files are in
`build/oikos_submission_aug_2026/` within this repository.

- `insurance_hypothesis_blinded_main.pdf`: anonymous main text for initial
  review. **Use this PDF as the main upload candidate.**
- `insurance_hypothesis_title_page.pdf`: unblinded title page.
- `insurance_hypothesis_supplementary_info.pdf`: anonymous Supporting
  information.
- `insurance_hypothesis_cover_letter.pdf`: editor-facing cover letter.
- `insurance_hypothesis_submission_form_statements.pdf`: source for
  copy-pasting required submission-system statements.
- `ih_package.zip`: anonymous code and simulated-data package, uploaded as
  **Additional file for review but NOT for publication**, not as Supporting
  information.

The current code/data archive is
`/home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-09-11/ih_package.zip`.
The dated archive preserves the previous release package.

## Current NSO requirements checked

- The main text must be anonymous, single-column, double-spaced, and have
  continuous page and line numbers.
- Page 1 contains the title and abstract; the Introduction begins on page 2.
- Initial main-text formats may be PDF, DOC, DOCX, RTF, or ODT.
- The abstract is no more than 300 words and contains no references.
- All figures and tables are numbered and cited in the text.
- Supporting information is a separate anonymous file. The main text refers to
  it only as “Supporting information”, without named subsections or specific
  item numbers.
- Data and custom code must be available at first submission, either through an
  anonymous repository link or as an “Additional file for review but NOT for
  publication”.
- The Data Availability, Significance, Conflict of Interest, Funding, and
  Acknowledgements material belongs in the submission system rather than the
  anonymous main file.
- Oikos asks authors to declare whether equity, diversity and inclusion
  considerations entered the conduct of the study; a simulation-appropriate
  statement is prepared with the other submission-form text.
- Use of LLM tools for literature search, content, code, or analysis must be
  disclosed in a specific AI-use statement at the end of the main text.

## Bounded revision verification: 2026-09-11

- The title is “Abundance-weighted responses shape community buffering under
  correlated environments”. The 215-word abstract leads with the biological
  comparison and states the numerical contrasts without unexplained notation.
- The central matched-control/boundary display is Figure 1. Existing rendered
  panels and numerical outputs are unchanged; all paper and package mappings
  follow the new order.
- An independent scientific audit approved the forcing-versus-abundance
  distinction, equal-`K` linear argument, unequal-`K` feedback qualification,
  resolved nonlinear departure, and removal of the unsupported mean-shift claim.
- All six sequential makedoc profiles passed their build checks, including
  manuscript lint, reference audit, and author-injection checks. The main
  reference audit found 27 cited keys, zero unknown keys, and four unused
  non-fatal bibliography entries.
- The main PDF is 28 pages, with its Introduction on page 2, continuous line
  numbers, five main figures, and one table. Its PDF/DOCX golden contract passes
  all 12 text markers, the table count, and the drawing count.
- Supporting information is 10 pages, including the added linear derivation
  and its reference. Every main and Supporting-information PDF page was visually
  checked, with full-size checks of the central equations and display. No
  clipping was found. Existing makedoc pagination includes a heading-only
  supplementary divider page; the main Table 1 and figure captions continue
  across page boundaries.
- Main and Supporting-information PDF text and metadata pass the configured
  identity scan and `qpdf --check`. Both DOCX files were sanitized and rechecked,
  and their build manifests refreshed. DOCX rendering was not repeated in this
  tranche; the PDF remains the initial-submission candidate.
- The repository passes 39 tests and Pyright. Regeneration left all 51 protected
  SHA-256 hashes identical, including model source, specs, seven production
  summaries, and canonical numerical/rendered reports.
- The rebuilt anonymous archive passes integrity, path, and identity checks.
  In a clean extraction, 35 tests, Pyright, and the nine-figure/11-table-summary
  workflow pass. All seven Parquet files match source hashes and contain
  1,196,000 rows; all 29 regenerated PNG/PDF/CSV files match byte-for-byte.
- Archive SHA-256:
  `405c1373cec236757ef825be776b7ef14300dc5e7826389314c28159a3f67f17`.
  Archive size: 75,469,545 bytes.
- Verification logs, protected hashes, renders, and the independent archive
  report are in `build/revision_checks_2026-09-11/`.

Full production validation and numerical guards last passed in the 2026-08-10
release gate. Those simulations/diagnostics were not rerun for this editorial
tranche; protected source, input, and output hashes establish the unchanged
computational evidence base.

## Important format choice

The 2026-08-10 LibreOffice rendering put the DOCX Introduction on page 3.
The revised DOCX has not been repaginated or visually rechecked in Word. The
current direct makedoc PDF begins the Introduction on page 2 and satisfies the
initial-submission layout. Because NSO explicitly accepts PDF at
initial submission, use the PDF main file unless the DOCX pagination is
deliberately reformatted first. The DOCX remains useful as an editable fallback
and will be required in clean and tracked forms at revision.

## Author confirmations still required

- Replace the funding placeholder with the correct funding statement or an
  explicit no-specific-funding statement.
- Replace the acknowledgements placeholder with final text or “None”.
- Confirm the current conflict-of-interest wording.
- Confirm that the AI-use statement accurately describes the tools and purposes
  used in the project.
- Name the intended permanent data/code repository in the Data Availability
  statement.
- Read the cover letter once in the author’s own voice.

## WSL build and verification commands

Run profiles sequentially because they share makedoc cache state:

```bash
MAKEDOC=/home/bwbrook/work/makedoc
CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml
BUILD=/home/bwbrook/papers/insurance_hypothesis/build/oikos_submission_aug_2026

make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_draft
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_submission
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_submission_form_statements
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_supplementary_info
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_author_title_page
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_cover_letter

uv run --frozen python scripts/sanitize_docx_identity.py --check \
  "$BUILD/insurance_hypothesis_blinded_main.docx" \
  "$BUILD/insurance_hypothesis_supplementary_info.docx"

make -C "$MAKEDOC" manifest CONFIG="$CONFIG" PROFILE=ih_submission
make -C "$MAKEDOC" manifest CONFIG="$CONFIG" PROFILE=ih_supplementary_info

uv run --frozen pytest -q
uv run --frozen pyright
uv run --frozen python scripts/build_deidentified_review_package.py \
  --target /home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-09-11/ih_package \
  --zip
```
