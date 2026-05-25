# Oikos Submission Readiness Checklist

This checklist captures the current submission-facing interpretation of the Oikos and NSO author guidelines checked on 2026-05-25.

Sources:

- <https://nso-journals.org/oikos-for-authors>
- <https://nso-journals.org/author-guidelines>

## Current Build Profiles

- `ih_draft`: internal author-aware draft profile.
- `ih_submission`: double-blind main manuscript profile for review, with author metadata omitted.
- `ih_submission_form_statements`: separate statements profile for submission-system fields and editor/upload support.
- `ih_supplementary_info`: anonymous supplementary information profile.
- `ih_author_title_page`: separate unblinded title page and author-statement profile.
- `ih_cover_letter`: separate editor-facing cover letter profile.

## Oikos-Facing Requirements

- Initial submission can use PDF, DOC, DOCX, RTF, or ODT; PDF plus DOCX fallback is therefore acceptable for review.
- Double-anonymised review requires author names, affiliations, acknowledgements, and contribution statements to be removed from the main text file.
- A separate title page should contain title, author names, affiliations, email addresses, corresponding author details, and ORCID information.
- The main manuscript should include line numbers and page numbers.
- Oikos asks authors to be ready to provide statements on data availability, significance, conflict of interest, ethics, funding, and acknowledgements through the submission workflow.
- NSO explicitly says the data availability statement should not be included in the main text file; for consistency and double-blind hygiene, the submission-support profile keeps all required statements outside the main review manuscript.
- Supplementary material should also be anonymised for review.
- Data archiving is required; for this simulation study, the review route is a de-identified reproducibility package supplied as supplementary material, followed by a permanent public archive with DOI if accepted.

## Implemented Now

- The significance statement has been rewritten as concise, journal-neutral submission-form text.
- The submission profile no longer injects author metadata into the main manuscript.
- The submission profile no longer includes the significance statement, data/code availability statement, conflict statement, ethics statement, funding statement, or acknowledgements in the blinded main manuscript.
- A separate `ih_submission_form_statements` profile carries these statements for copy-paste or separate upload as needed.
- Main figures/tables and supplementary figures/tables are split into separate source files so the review manuscript and supplementary information can be built separately.
- A separate title-page source carries the unblinded author metadata and placeholders for Barry-only submission details.
- A separate cover-letter source has been drafted for Barry's editorial pass.

## Barry-Only Confirmations Before Final Submission

- Confirm final funding text.
- Confirm conflict-of-interest wording.
- Confirm whether acknowledgements are absent or should be supplied after review.
- Confirm final data/code archive destination and whether the review package should later be mirrored to Dryad, Zenodo, OSF, or another permanent archive.
- Review and finalise the cover-letter text for tone, author voice, and any ScholarOne-specific fields.

## Local Build Commands

Run from `/home/bwbrook/work/makedoc`, sequentially rather than in parallel because the profiles share build cache state:

```bash
make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_submission
make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_submission_form_statements
make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_supplementary_info
make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_author_title_page
make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_cover_letter
```

After building DOCX files, run the local metadata sanitizer from `/home/bwbrook/papers/insurance_hypothesis`:

```bash
uv run python scripts/sanitize_docx_identity.py --check \
  /home/bwbrook/work/makedoc/dist/paper/insurance_hypothesis_blinded_main.docx \
  /home/bwbrook/work/makedoc/dist/paper/insurance_hypothesis_supplementary_info.docx
```

Run from `/home/bwbrook/papers/insurance_hypothesis`:

```bash
uv run pytest -q
uv run pyright
uv run python analysis/run_all.py --skip-guard-audit
```
