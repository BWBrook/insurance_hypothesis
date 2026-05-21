# Oikos Submission Readiness Checklist

This checklist captures the current submission-facing interpretation of the Oikos author guidelines checked on 2026-05-21.

Source: <https://www.oikosjournal.org/authors/author-guidelines>

## Current Build Profiles

- `ih_draft`: internal author-aware draft profile.
- `ih_submission`: double-blind main manuscript profile for review, with author metadata omitted.
- `ih_supplementary_info`: anonymous supplementary information profile.
- `ih_author_title_page`: separate unblinded title page and author-statement profile.

## Oikos-Facing Requirements

- Initial submission can use PDF, DOC, DOCX, RTF, or ODT; PDF plus DOCX fallback is therefore acceptable for review.
- Double-anonymised review requires author names, affiliations, acknowledgements, and contribution statements to be removed from the main text file.
- A separate title page should contain title, author names, affiliations, email addresses, corresponding author details, and ORCID information.
- The main manuscript should include line numbers and page numbers.
- A significance statement should appear below the abstract and be no more than 1000 characters including spaces.
- Required statements include data/code availability, conflict of interest, ethics where relevant, funding, and author contributions.
- Supplementary material should also be anonymised for review.
- Data archiving is required; for this simulation study, the review route is a de-identified reproducibility package supplied as supplementary material, followed by a permanent public archive with DOI if accepted.

## Implemented Now

- The significance statement has been rewritten as a concise, journal-neutral statement below the abstract.
- The submission profile no longer injects author metadata into the main manuscript.
- Main figures/tables and supplementary figures/tables are split into separate source files so the review manuscript and supplementary information can be built separately.
- Anonymous statements are included in the blinded main manuscript.
- A separate title-page source carries the unblinded author metadata and placeholders for Barry-only submission details.

## Barry-Only Confirmations Before Final Submission

- Confirm final funding text.
- Confirm conflict-of-interest wording.
- Confirm whether acknowledgements are absent or should be supplied after review.
- Confirm final data/code archive destination and whether the review package should later be mirrored to Dryad, Zenodo, OSF, or another permanent archive.
- Confirm article type and any cover-letter text in the Oikos submission system.

## Local Build Commands

Run from `/home/bwbrook/work/makedoc`:

```bash
make all CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_submission
make all CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_supplementary_info
make all CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml PROFILE=ih_author_title_page
```

Run from `/home/bwbrook/papers/insurance_hypothesis`:

```bash
uv run pytest -q
uv run pyright
uv run python analysis/run_all.py --skip-guard-audit
```
