# Oikos Submission Readiness Checklist

Current against the Oikos and NSO author guidance checked on 2026-08-10:

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

## Last full submission verification: 2026-08-10

- The main manuscript is anonymous and contains a specific AI-use statement
  before the References.
- The 230-word abstract states the principal numerical contrast. The
  Introduction begins on page 2 of the 28-page A4 submission PDF.
- The main PDF is double-spaced, single-column, continuously line-numbered, and
  contains all five cited main figures and Table 1.
- Main-text references to supplementary material use the generic term
  “Supporting information”.
- Main and Supporting-information PDF text and metadata contain no configured
  author, institution, ORCID, email, or local-path identity strings.
- Main and Supporting-information DOCX metadata were sanitized and rechecked.
- The duplicated italic title note was removed from the unblinded title page.
- All six makedoc profiles passed config validation, manuscript lint, reference
  audit, author-injection checks, and the current makedoc test suite.
- The submission golden contract passed against the actual PDF and DOCX: one
  table, five drawings, 28 PDF pages, and all 12 required text markers.
- The manuscript reference audit found 25 cited keys, zero unknown keys, and
  five unused non-fatal bibliography entries.
- All seven production summaries validate: 1,196,000 replicate rows across
  1,196 scenarios. The source repository has 39 passing tests and a clean
  Pyright result; the numerical guards pass with the high-variance and
  high-persistence edges retained as labelled stress regimes.
- Consecutive figure regenerations have identical PDF hashes. All 18 PNG and
  rasterized-PDF comparisons against the approved Stage 3 display suite pass.
- Every page of the main and Supporting-information PDF and Word renderings was
  visually inspected; no clipped table, equation, caption, line number, or
  display was found.
- The final de-identified review package was rebuilt with seven specs and seven
  compact summaries. From inside the package, 35 tests, Pyright, and the full
  nine-figure/11-summary workflow pass. The clean archive passes integrity,
  path, and identity scans (`SHA-256 c4184aa5528fd36258ae36b691abea193310e8bf36adcc49c4ffc76dd543a35a`).

## Important format choice

LibreOffice renders the generated DOCX main file with the Introduction on page
3, whereas the direct makedoc PDF begins it on page 2 and otherwise satisfies
the current initial-submission layout. Because NSO explicitly accepts PDF at
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
uv run --frozen python scripts/build_deidentified_review_package.py --zip
```
