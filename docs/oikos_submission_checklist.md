# Oikos Submission Readiness Checklist

Current against the Oikos and NSO author guidance checked on 2026-07-24:

- <https://nso-journals.org/oikos-for-authors>
- <https://nso-journals.org/author-guidelines>

## Files and classification

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
- Use of LLM tools for literature search, content, code, or analysis must be
  disclosed in a specific AI-use statement at the end of the main text.

## Implemented and verified on 2026-07-24

- The main manuscript is anonymous and contains a specific AI-use statement
  before the References.
- The abstract remains below the 300-word limit and states the principal
  numerical contrast.
- The Introduction begins on page 2 of the 29-page A4 submission PDF.
- The main PDF is double-spaced, single-column, continuously line-numbered, and
  contains all five cited main figures and Table 1.
- Main-text references to supplementary material use the generic term
  “Supporting information”.
- Main and Supporting-information PDF text and metadata contain no configured
  author, institution, ORCID, email, or local-path identity strings.
- Main and Supporting-information DOCX metadata were sanitized and rechecked.
- The duplicated italic title note was removed from the unblinded title page.
- All six makedoc profiles passed config validation, manuscript lint, reference
  audit, author-injection tests, and the 61-test makedoc suite.
- The submission golden contract passed against the actual PDF and DOCX: one
  table, five drawings, 29 PDF pages, and all 12 required text markers.
- The manuscript reference audit found 26 cited keys, zero unknown keys, and
  four unused non-fatal bibliography entries.
- The source-repository test suite and Pyright pass.
- The de-identified review package was freshly rebuilt and verified from inside
  the package; see `docs/deidentified_review_package_plan.md`.

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
- Confirm whether ScholarOne accepts the 72,617,256-byte review zip; otherwise
  use an anonymous repository/private-for-review route.
- Read the cover letter once in the author’s own voice.

## WSL build and verification commands

Run profiles sequentially because they share makedoc cache state:

```bash
MAKEDOC=/home/bwbrook/work/makedoc
CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml

make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_draft
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_submission
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_submission_form_statements
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_supplementary_info
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_author_title_page
make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE=ih_cover_letter

uv run python scripts/sanitize_docx_identity.py --check \
  /home/bwbrook/work/makedoc/dist/paper/insurance_hypothesis_blinded_main.docx \
  /home/bwbrook/work/makedoc/dist/paper/insurance_hypothesis_supplementary_info.docx

uv run pytest -q
uv run pyright
uv run python scripts/build_deidentified_review_package.py --zip
```
