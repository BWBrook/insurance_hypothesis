# 250 Oikos Submission Readiness

## 2026-05-21

### Aim

Move from production-figure completion into an Oikos-oriented submission-readiness lane before Barry's full human-scientist pass.

### Actions

- Committed and pushed the production supplementary/reproducibility checkpoint as `ab3e9de`.
- Checked the Oikos author guidelines and treated the double-anonymised review requirement as a build-profile constraint.
- Rewrote the significance statement to remove journal-targeting language and keep it within the Oikos 1000-character limit.
- Removed source-note/reproducibility boilerplate from the manuscript body after the References heading.
- Split main figures/tables from supplementary figures/tables so the review manuscript and supplementary information can be emitted separately.
- Added a double-blind `ih_submission` profile with no injected author metadata.
- Added an anonymous `ih_supplementary_info` profile and an unblinded `ih_author_title_page` profile.
- Added `docs/oikos_submission_checklist.md` and `docs/deidentified_review_package_plan.md`.

### Current Interpretation

The remaining work is no longer mainly simulation production. The next high-value pass is submission hardening: build the blinded manuscript, title page, and supplementary information; scan for accidental identity leakage; then run a claim-by-claim consistency check against the production summaries.

### Deferred

- Do not build the de-identified review-code zip until final code lock.
- Do not refresh lower-replicate no-competition or mixed-narrow controls unless the final manuscript relies on them more heavily than intended.
