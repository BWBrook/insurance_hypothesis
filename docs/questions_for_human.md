# Questions for human (only when blocked or at major fork)

## Open questions

1. **Q-001 – Covariance structure robustness (future work)**  
   - Context: Current results use equicorrelated environmental innovations. Insurance signal is strong under mixed slopes and reversed under aligned slopes. The PI has indicated that, for this manuscript, equicorrelation is acceptable provided it is clearly acknowledged as a simplifying assumption.  
   - Question: For a potential follow-up or appendix, should we prioritise exploring (a) block-correlated Σ, (b) gradient-based Σ along the slope axis, or (c) empirically inspired covariance patterns, given limited additional compute?

2. **Q-006 – Final funding statement**
   - Context: The title page still contains a funding placeholder.
   - Question: What funding should be named, or should the statement say that the work received no specific funding?

3. **Q-007 – Final acknowledgements**
   - Context: The title page still contains an acknowledgements placeholder.
   - Question: Who, if anyone, should be acknowledged, or should this field be marked “None”?

4. **Q-008 – Permanent data/code archive**
   - Context: NSO requires a public, persistently identified archive after acceptance, and the submission statement should say where the materials will be deposited.
   - Question: Should the final package go to Dryad, Zenodo, or another named repository?

5. **Q-009 – AI-use disclosure**
   - Context: Current NSO guidance requires disclosure of LLM use for manuscript content, literature searches, code, or analysis.
   - Question: Does the drafted AI statement accurately describe the tools and purposes used in this project?

6. **Q-010 – Anonymous review-package delivery**
   - Context: The verified review zip is 72,617,256 bytes and must be classified as “Additional file for review but NOT for publication”.
   - Question: Should we try the direct ScholarOne upload first, or prepare an anonymous private-for-review repository link?

## Answered questions

1. **Q-002 – makedoc path resolution for external configs**  
   - Answer: Use absolute paths in external-path mode. Relative paths are not guaranteed to resolve relative to the external config location.
   - Action taken: `paper/settings/build.yaml` now uses absolute paths for manuscript sources, lint sources, author metadata, bibliography, and CSL.

2. **Q-003 – Preferred manuscript source contract for makedoc**  
   - Answer: `main.md` is convention only; any filename is acceptable if ordered correctly in `manuscript_sources`.
   - Action taken: Kept `paper/manuscript/text/draft_ms_v2.md` as primary manuscript source in build profiles.

3. **Q-004 – Lint policy for transition stage**  
   - Answer: Use reduced lint scope/profile during drafting, while preserving strict full-lint submission profile.
   - Action taken: Added `ih_draft` profile (scoped `lint_sources`) and `ih_submission` profile (full strict `lint_sources`) in `paper/settings/build.yaml`.

4. **Q-005 – Canonical bibliography filename in `paper/references/`**  
   - Answer: Use one canonical bibliography file only.
   - Action taken: Standardised on `paper/references/ih_references.yaml`; removed duplicate `paper/references/refs.yaml`; updated profile references accordingly.
