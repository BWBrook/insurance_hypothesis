# 290 Oikos Submission Composition

## 2026-05-25

### What I attempted

- Re-checked the live Oikos and NSO author guidance after the independent pre-submission review flagged that the main manuscript still carried submission-system statements.
- Compared the guidance against the current makedoc profiles and source files.

### What changed

- Removed the Significance Statement from the blinded main manuscript source.
- Removed the data/code availability, ethics, conflict, funding, and acknowledgement statements from the blinded main manuscript build profile.
- Added `paper/manuscript/text/submission_form_statements.md` as a separate support file for ScholarOne copy-paste/upload fields.
- Added the `ih_submission_form_statements` makedoc profile.
- Updated `docs/oikos_submission_checklist.md` to point to the current NSO URLs and the corrected build composition.

### Rationale

- The live NSO author guidelines say the data availability statement should not be included in the main text file.
- The Oikos guidance says authors should be ready to provide data availability, significance, conflict, ethics, funding, and acknowledgement statements through the submission workflow.
- Keeping these statements outside the blinded main manuscript reduces double-blind leakage risk and directly addresses the independent reviewer's submission-composition critique.

### Next

- Validate the new makedoc profile and re-check the blinded main manuscript for statement leakage.
- Then build the de-identified review-code package, because NSO requires data and custom code needed for replication at first submission.

## 2026-05-25 Review-package harness

### What changed

- Added a review-safe `analysis/run_all.py --skip-paper-export` switch so the code-only package can regenerate figures and CSV summaries without creating a `paper/` tree.
- Added `scripts/build_deidentified_review_package.py`, which stages a minimal anonymous package under `/home/bwbrook/papers/de_identified_repos/ih_package/` and can write the corresponding zip archive.
- The package builder copies only code, tests, versioned production specs, compact production summaries, `pyproject.toml`, and `uv.lock`, while sanitising author metadata and excluding manuscript/documentation artefacts.

### Next

- Run the package builder.
- Validate the staged package with `uv sync --python 3.12 --frozen --dev`, `uv run pytest -q`, `uv run pyright`, and `uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export`.

### Validation completed

- Built `/home/bwbrook/papers/de_identified_repos/ih_package/` and `/home/bwbrook/papers/de_identified_repos/ih_package.zip`.
- Validated the staged package from its own directory:
  - `uv sync --python 3.12 --frozen --dev`
  - `uv run pytest -q` -> 48 passed
  - `uv run pyright` -> 0 errors
  - `uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export`
- Rebuilt the staging directory and zip after validation so the final package remains minimal and does not contain `.venv`, `__pycache__`, generated reports, manuscript files, docs, references, Git metadata, or local identity strings.
