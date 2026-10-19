# Oikos Submission Readiness Checklist

Current against the Oikos and NSO author guidance rechecked on 2026-10-18:

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
`/home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-10-19/ih_package.zip`.
The September and 18 October archives remain available as earlier checkpoints.

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

## Mechanism and ordering-test revision: 2026-10-19

- New evidence: a prespecified out-of-sample test of ordering by the small-noise
  coefficient (`analysis/prespecified/ordering_predictions_2026-10-19.json`,
  SHA-256 `0e12545f…d74d65`; grids `ordering_test_alpha{020,045}_v1`, 120
  scenarios, 120,000 rows). All three criteria passed (35/35, 17/17, 14/15);
  13 further floor-free reversals, including two at alpha 0.2 and a doubling of
  mean squared CV at twelve species. Single- and 20-trajectory diagnostics show
  total abundance following the second-order driver.
- Main Fig. 2A now adds balanced two- and eight-species curves at the default
  competition and autocorrelation; the eight-species curve crosses one. Main
  Fig. 3 is redrawn: A–B mechanism trajectory, C ratio against c·sigma² for all
  168 setting-by-amplitude cells. New Table S6; Tables 1, S1 and S2 extended.
- The abstract has 261 words. The main PDF has 26 pages with the Introduction
  on page 2; the Supporting information has 24 pages. Five verified references
  were added (Adler et al. 2018, Houlahan et al. 2007, Ruel and Ayres 1999,
  Vasseur and Yodzis 2004, Vasseur et al. 2014), and four existing bibliography
  entries are now cited (Doak et al. 1998, Thibaut and Connolly 2013, Valencia
  et al. 2020, Kunze et al. 2026). The integration also adds Gouhier et al.
  (2010) as close prior work and removes the broad priority claim.
- An independent scientific audit of the new claims (separate agent, raw-row
  recomputation) returned SUPPORTED WITH CORRECTIONS; all corrections were
  applied: the ordering test is described as testing x = c·sigma² as a
  calibrated axis, not the leading-order formula; level-versus-change wording
  of the identity; the S = 8 threshold statement; Bonferroni over 60 test
  comparisons; the relative nature of the richness effect; ensemble rather than
  single-trajectory driver statistics.
- The source checkout passes 46 tests and Pyright. All outputs other than the
  Fig. 2 and Fig. 3 images are byte-identical to the 18 October outputs; four
  summary CSVs are new; regeneration is byte-stable.
- All six sequential document profiles pass; the golden contract passes; both
  anonymous DOCX files are sanitized and manifests refreshed; both anonymous
  PDFs pass `qpdf --check` and text/metadata identity scans.
- Anonymous computational archive:
  `~/papers/de_identified_repos/insurance_hypothesis_2026-10-19/ih_package.zip`,
  SHA-256 `a32b9f511f18a2f67cc92839ac3b6b72223d287aac08e5557a3b7b39c7c74796`,
  113,402,635 bytes, 99 entries. Claude's clean-extraction replay passes the supplied
  checksums, 42 tests, Pyright, `run_all.py`, the guard diagnostic, all 51
  expected-output hashes and validation of all 18 grids (1,738 scenarios,
  1,733,000 rows). The archive now exceeds 100 MB; confirm the portal limit or
  host it as an anonymous repository link.

- Codex's independent integration audit reconstructs all 60 test comparisons,
  the 35/35, 17/17 and 14/15 decisions, both coarse prediction benchmarks,
  and the familywise intervals. The maximum prediction error is 4.631%; the
  largest ratio is 2.030 (95% interval 1.993–2.068). The calibrated predictor is
  distinguished from the uncalibrated formula, the twelve-species directional
  comparison from the four/eight-species numerical predictions, and the
  second-order relation from the full nonlinear trajectory. The independent
  science and literature reviews are retained in
  `docs/oikos_ordering_scientific_review_2026-10-19.md` and
  `docs/oikos_ordering_literature_review_2026-10-19.md`.
- An audit-only independently seeded repeat of the largest new reversal used
  200 replicates per endpoint and 6000 steps, retaining the last 3000. Its ratio
  is 2.011 (1.985–2.037), with no floor contact or clipping. This targeted check
  is not a new production grid, does not alter the manuscript's reported
  result, and does not extend the full longer-window/guard check to all thirteen
  new cases.
- The final integration passes the 46-test/Pyright gate and preserves all 89
  audited computational files: 18 summaries, 18 specifications, 51 outputs, and
  the model/production modules. Independent ZIP checks pass CRC and all 67
  supplied-file checksums; 60 included science/data files match the checkout.
  The 51-output manifest and the archive hash above are unchanged. The complete
  clean-extraction replay was not repeated by Codex.
- The cover letter and significance statement reflect the new result; the AI
  statement includes the verified Sonnet review-agent identifier. Final build
  logs, source checks, independent calculations and page renders are in
  `build/ordering_integration_2026-10-19/`.
- All 26 main and 24 SI pages, the one-page cover letter and two-page title page
  were visually inspected. No clipping or missing display labels remain; normal
  caption continuations are retained in the review layout. The golden contract
  passes all 10 markers, one table and three drawings; its title markers follow
  the actual line break so line numbering cannot interrupt a matched phrase.
  Both anonymous DOCX files are sanitized, their manifests refreshed, and both
  PDFs pass structure and text/metadata identity checks. Word/LibreOffice DOCX
  pagination was not rechecked; PDF remains the initial-submission candidate.

## Earlier checkpoint: scientific and editorial revision, 2026-10-18

- The title is “Shared environments can destabilise communities with balanced
  opposing responses”. The abstract has 236 words. The main PDF has 21 pages,
  with the Introduction on page 2, three figures and one design table.
- The paper now distinguishes the benefit of opposing response signs from the
  effect of sharing environmental exposure. Five balanced-response settings
  show amplification; all survive the 108-comparison multiplicity correction
  and independently seeded longer runs. The local second-order prediction
  passes both recorded acceptance definitions in all 23 eligible settings.
- An independent scientific audit reconstructs the headline results, checks the
  finite-window calculation, and exactly replays 26 stored seeds across eight
  production sources. No major scientific concern remains. The audit and its
  limits are retained in `docs/oikos_october_scientific_review_2026-10-18.md`.
- The source checkout passes 45 tests and Pyright. Canonical display regeneration
  passes and preserves all 46 protected hashes: the original seven production
  summaries, seven specifications and 32 outputs. The model recurrence and
  production execution are unchanged.
- All six sequential document profiles pass. The main PDF/DOCX golden contract
  passes its 10 text markers, one table and three drawings. Both anonymous DOCX
  files are sanitized and their manifests refreshed. PDF remains the submission
  candidate; Word/LibreOffice pagination was not rechecked.
- Every page of the 21-page main PDF and 21-page Supporting information was
  visually checked, along with the cover letter and title page. Crowded SI
  headers, a long identifier and a list-parsing defect were corrected and the
  affected pages rechecked. Both anonymous PDFs pass `qpdf --check` and text/
  metadata identity scans.
- The bibliography prints all authors as required by the current NSO guidance.
  The disclosure names the verified AI model identifiers and describes their
  scientific, computational, review and writing roles explicitly.
- The anonymous archive contains 16 production summaries and specifications,
  1,618 scenarios and 1,613,000 replicate rows. Claude's clean-extraction replay
  passes 41 tests, Pyright, manifest validation and all 47 expected-output hashes.
  The integration audit independently checked supplied-file checksums, ZIP
  integrity and the new production inputs. Manuscript-only changes do not alter
  this computational package.
- Checkpoint archive SHA-256:
  `48fee560383f8c8a732a64a2441419995375e9362a0c9f25cd85ec6279e0e209`.
  Size: 104,808,799 bytes; 91 ZIP entries. Confirm the portal's limit for this
  review-only code/data upload at submission.
- Build logs, source comparisons, independent calculations and page renders are
  in `build/editorial_integration_2026-10-18/`. The checks below dated September
  describe earlier checkpoints and do not supersede this October inventory.

## Earlier checkpoint: external-review corrections, 2026-09-19

- The title is “Abundance-weighted responses and nonlinear limits to community
  buffering under correlated environments”. The abstract remains 240 words.
- The Introduction explicitly acknowledges Ross et al. (2023) on abundance
  weighting and locates the contribution in the integrated covariance benchmark
  and its nonlinear tests. The existing numerical claims and derivations remain.
- Figures 1 and 2 now use vertically stacked panels, with the smallest labels
  approximately 8 pt at their final PDF size. Figure 1B includes a magnified
  near-threshold inset using the same data and uncertainty intervals.
- Figure S2 masks 15 zero-forcing synchrony cells in pale grey. Their display
  means and SDs are missing in the CSV; all 75 nonzero-forcing cells and every
  other numerical summary are exactly unchanged. The caption and package README
  explain the undefined values. Saved replicate rows are preserved.
- All six sequential makedoc profiles passed their checks. The main PDF has
  29 pages, with the Introduction on page 2, continuous line numbers, five
  figures and one table. The PDF/DOCX golden contract passes all 12 text markers,
  the table count and the drawing count. The cover letter remains one page.
- Supporting information has 10 pages. The heading-only supplementary divider
  is removed; captions remain separate from the four correctly labelled figures.
  Every main and Supporting-information PDF page and the cover letter were
  visually checked. No clipping was found. Existing table and caption
  continuations across page boundaries remain.
- Main and Supporting-information PDF text and metadata pass the configured
  identity scan and `qpdf --check`. Both DOCX files were sanitized and rechecked,
  and their build manifests refreshed. Word/LibreOffice DOCX rendering was not
  repeated; the PDF remains the initial-submission candidate.
- The repository passes 40 tests and Pyright. All seven production Parquets,
  seven specifications and model/production/diagnostic modules retain their
  baseline hashes. Only the approved figure renderer and seven report files
  changed within the protected comparison. Pyright excludes generated `build/`
  scratch material and `.venv/`.
- The rebuilt anonymous archive passes integrity, path, text and metadata
  identity checks, and all 38 supplied-file checksums. A clean frozen extraction
  passes 36 tests and Pyright. All seven Parquets byte-match the canonical and
  previously verified anonymous data; their exhaustive metadata/string-column
  identity scan was reused on that basis.
- All 29 regenerated figure/table outputs match the current canonical files
  byte-for-byte; the three retained numerical-guard outputs also match, making
  32 expected-output hashes. Production and guard simulations were not rerun.
- Archive SHA-256:
  `7fd3b50e30c576ff4d7f02849c8b859a38ea1a3a70576a198b45fc836b9576f7`.
  Archive size: 75,477,793 bytes; 39 files, without workbook history or editorial
  material. Confirm the portal's limit for this review-only upload at submission.
- Verification logs, final renders, baseline comparison and independent package
  report are in `build/review_corrections_2026-09-19/`; final page images are in
  its `rendered_final/` directory. The independent Astra review remains in
  `docs/oikos_astra_external_review_2026-09-18.md`.

### Manuscript build dependency

The SI layout fix also changes the local makedoc checkout at
`/home/bwbrook/work/makedoc` (base commit `b613e71`):
`scripts/prepare_markdown_sources.py` emits the supplementary divider only when
both main and supplementary figures occur in the document. Standalone SI
profiles retain their original caption-page layout without that divider.
The two placement modes and mixed-document behavior have regression coverage;
`test-author-injection`, `test-figure-modes`, `check` (38 tests), and
`check-fixture` passed. The implementation, test, README and agent primer changes
are committed on branch `claude/standalone-si-divider` of that repository
(`4cd4809`). Rebuilding this exact SI layout elsewhere requires that commit. No makedoc change is needed to run the anonymous
scientific archive.

## Earlier checkpoint: prose pass, 2026-09-28

- The main-text prose and figure captions were revised for readability and for
  readers outside the subfield. All 24 display equations and every citation are
  unchanged, and no display, estimand or claim changed. Two roundings were
  corrected: the Fig. 1A mixed value near perfect correlation now reads 0.059,
  and the Monte Carlo SD example (0.0048; SE 0.00015) now comes from the same
  grid as its means.
- The abstract has 277 words and fits on page 1 with the keywords; the
  Introduction begins on page 2. The main PDF has 31 pages and Supporting
  information has 10.
- All six sequential makedoc profiles passed, and the PDF/DOCX golden contract
  passes all 12 text markers, the table count and the drawing count. Both
  anonymous DOCX files were sanitized and their manifests refreshed. Both
  anonymous PDFs pass `qpdf --check` and a text and metadata identity scan. The
  repository passes 40 tests and Pyright.
- The anonymous archive contains no manuscript text and was not rebuilt; the
  archive hash above still applies.
- Pre-pass copies and word diffs are in `build/prose_pass_2026-09-28/`.

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
  --target /home/bwbrook/papers/de_identified_repos/insurance_hypothesis_2026-10-19/ih_package \
  --zip
```
