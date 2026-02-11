# 060 Manuscript V2 Alignment

Date: 2026-02-11

## What was attempted

- Audited `manuscript/text/draft_ms_v2.md` against current code outputs, figure files, and critique notes in `manuscript/text/colleague_critiques.md`.
- Checked consistency with current pipeline assets under `analysis/reports/` and `manuscript/figures/`.
- Implemented a full prose/notation cleanup pass and integrated previously requested critique fixes directly into Methods/Results language.

## What changed

1. Manuscript draft rewrite and cleanup (`manuscript/text/draft_ms_v2.md`)
- Removed formatting corruption artifacts (`*{`, `,,`, malformed inline equation fragments).
- Removed conversational placeholder text accidentally embedded in Methods.
- Clarified requested vs effective correlation (`rho_env` vs `rho_eff`) in the AR(1) environment section.
- Added explicit positive-matched slope regime (`positive_matched`) to slope definitions and simulation design.
- Aligned variance language with implementation (empirical/sample moments over retained time points).
- Updated Monte Carlo uncertainty paragraph with representative SE summaries from current replicate-level outputs.
- Added numerical-guard diagnostics wording with explicit stress-scenario interpretation.
- Reframed conclusions to avoid overgeneralising richness beyond the examined range.

2. Figure caption harmonisation (`manuscript/text/figure_captions_v2.md`)
- Standardised notation to `sigma_env`, `rho_env`/`rho_eff`, `phi_LdM`, `CV_tot`/"CV Total" wording.
- Added supplementary caption for positive-matched control as Figure S3.
- Ensured caption language is sign-robust for negative-correlation cases.

3. Figure pipeline update (`analysis/run_all.py`)
- Export positive-matched control with numbered supplementary filename: `figS3_positive_matched_control.png`.
- Copy Figure S3 into `manuscript/figures/` alongside existing numbered figure set.

4. Documentation sync (`README.md`, `docs/review_rounds.md`, `docs/plan.md`)
- Updated stale references from `draft.md` / `figure_captions.md` to `draft_ms_v2.md` / `figure_captions_v2.md`.
- Added Figure S3 to README figure inventory.
- Updated plan status to reflect numbered figure suite and manuscript v2 alignment state.

## Key checks completed

- Verified current figure inventory in `manuscript/figures/` and `analysis/reports/`.
- Cross-checked core quantitative claims (example CV values, synchrony contrasts, uncertainty magnitudes) from summary CSVs.
- Verified stress-test guard diagnostics from `analysis/reports/numerical_guard_rates.csv`.

## Remaining polishing items

- Optional: fill remaining `[REF]` placeholders once final citation library is frozen.
- Optional: tighten prose style further for target journal voice without changing technical content.

