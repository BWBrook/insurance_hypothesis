# 300 macOS submission compatibility pass

Date: 2026-05-28

## What was attempted

- Reviewed the WSL-to-Mac migration quirks identified during the repository orientation pass.
- Focused only on final-stage manuscript/build compatibility, not simulation code or new model runs.

## What changed

1. makedoc-facing runbooks
- Updated `docs/oikos_submission_checklist.md` to use `/Users/bwbrook/work/makedoc` and `/Users/bwbrook/papers/insurance_hypothesis`.
- Updated `docs/final_pre_barry_handoff.md` to point Barry's final review files at the Mac-side `makedoc/dist/paper/` directory.
- Updated `paper/README_makedoc.md` so it names the Mac `makedoc` path and the current full set of build profiles.

2. DOCX identity sanitising
- Extended `scripts/sanitize_docx_identity.py` to strip/check Mac local paths (`/Users/bwbrook/...`) and transient macOS build-cache paths (`/private/var/folders/...`) as well as WSL/Linux `/home/bwbrook/...` paths.

3. Review-package staging
- Changed `scripts/build_deidentified_review_package.py` to default to `~/papers/de_identified_repos/ih_package` instead of a Linux-only `/home/bwbrook/...` path.
- Added `IH_REVIEW_PACKAGE_ROOT` as an explicit override for unusual local staging roots while keeping the guard that refuses package builds inside the source repo.
- Updated `docs/deidentified_review_package_plan.md` to match the Mac default.

4. Remote helper clarity
- Left the `deep-server` helper defaults at `/home/bwbrook/papers/insurance_hypothesis`, but labelled them as intentional remote Linux checkout paths so they are not mistaken for local Mac paths.

## Validation

- Added non-simulation tests for the DOCX sanitizer and review-package target guard.
- `uv run pytest tests/python/test_submission_helpers.py -q` -> 2 passed.
- `uv run pyright` -> 0 errors.
- `git diff --check` -> passed.

## Notes

- No simulation model code, production specs, cached outputs, figures, or manuscript scientific claims were changed in this pass.
