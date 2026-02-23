# Questions for human (only when blocked or at major fork)

## Open questions

1. **Q-001 – Covariance structure robustness (future work)**  
   - Context: Current results use equicorrelated environmental innovations. Insurance signal is strong under mixed slopes and reversed under aligned slopes. The PI has indicated that, for this manuscript, equicorrelation is acceptable provided it is clearly acknowledged as a simplifying assumption.  
   - Question: For a potential follow-up or appendix, should we prioritise exploring (a) block-correlated Σ, (b) gradient-based Σ along the slope axis, or (c) empirically inspired covariance patterns, given limited additional compute?

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
