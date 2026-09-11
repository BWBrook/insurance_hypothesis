# Oikos Submission Readiness Checklist

Current against the Oikos and NSO author guidance rechecked on 2026-09-11:

- <https://nso-journals.org/oikos-for-authors>
- <https://nso-journals.org/author-guidelines>
- <https://www.oikosoffice.org/NSO-Publishing-Policies>

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
`/home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-09-11_final/ih_package.zip`.
The dated archive preserves the previous release package.

## Current NSO requirements checked

- The main text must be anonymous, single-column, double-spaced, and have
  continuous page and line numbers. Avoid right-margin justification and
  automatic hyphenation.
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

## Final author-read verification: 2026-09-11

- The title is “Abundance-weighted responses and nonlinear limits to community
  buffering under correlated environments”. The abstract is 240 words.
- The final synthesis retains Fable's readability improvements and reports both
  the substantial balanced-endpoint residual and the near-threshold direction
  reversal. An independent methodological audit approved the checked local
  second-order derivation and its limited interpretation. Growth-rate offsets,
  correlation clipping, and diagnostic provenance match the active code.
- All six sequential makedoc profiles passed their checks, including manuscript
  lint, reference audit, and author-injection checks. The cover letter is one
  page and uses the same calibrated claims as the manuscript.
- The main PDF is 29 pages, with the Introduction on page 2, continuous line
  numbers, five main figures, and one table. Its PDF/DOCX golden contract passes
  all 12 text markers, the table count, and the drawing count. The PDF uses
  ragged-right text without automatic hyphenation, as requested by NSO.
- Supporting information is 11 pages, including the linear and local
  second-order derivations. Every main and Supporting-information PDF page and
  the cover letter were visually checked. No clipping was found. Existing
  pagination includes a heading-only supplementary divider page; the main
  Table 1 and figure captions continue across page boundaries.
- Main and Supporting-information PDF text and metadata pass the configured
  identity scan and `qpdf --check`. Both DOCX files were sanitized and rechecked,
  and their build manifests refreshed. DOCX rendering was not repeated in this
  tranche; the PDF remains the initial-submission candidate.
- The repository passes 39 tests and Pyright. All 51 protected SHA-256 hashes
  remain identical, including model source, specs, seven production summaries,
  and canonical numerical/rendered reports.
- The rebuilt anonymous archive passes integrity, path, and identity checks,
  including Parquet metadata and string columns. A clean extraction passes
  35 tests and Pyright. All seven Parquet files validate against fresh manifests
  generated from their specs: 1,196 scenarios and 1,196,000 rows.
- All 29 regenerated figure/table outputs match byte-for-byte. The separate
  90-trajectory guard diagnostic reproduces all three retained outputs exactly.
  The README reconstruction of Tables S1 and S2 agrees with the manuscript;
  Table S3's generated output also matches. All supplied-file checksums pass.
- Archive SHA-256:
  `818d45b668a170fcf8790722c2f6cb6f0d0ecc84835ef091c212a01f36b9114f`.
  Archive size: 75,477,053 bytes; 39 files, without workbook history or editorial
  material. Confirm the portal's limit for this review-only upload at submission.
- Verification logs, renders, and the independent archive report are in
  `build/final_read_2026-09-11/`. The protected hash baseline is in
  `build/revision_checks_2026-09-11/protected_baseline.json`.

The full production simulations were not rerun for this tranche. Their saved
summaries and current spec-derived validation establish the production evidence
base; the small numerical-guard diagnostic was rerun independently as above.

## Preprint and public-release workflow

Oikos uses double-anonymous review and permits preprints before or during review.
The PI prefers a preprint before submission. Supply the anonymous main PDF and
code/data ZIP to Oikos and disclose the preprint URL separately to the editor
once available. The preprint makes author identity discoverable; anonymous
review files do not guarantee that reviewers cannot identify the author.

After the PI's full read and any final corrections, prepare the clean versioned
public repository and DOI-linked Zenodo package from the verified computational
core. Add the approved licence, author/citation metadata, version, repository
URL, and DOI. Journal acceptance is not a prerequisite. No preprint, public
repository, Zenodo deposit, or journal submission has been made in this tranche.
See `docs/reproducibility_release.md` for the precise archive boundary.

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
- Finalize the clean public repository URL, Zenodo metadata, licence, and
  release timing after the full manuscript read.
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
  --target /home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-09-11_final/ih_package \
  --zip
```
