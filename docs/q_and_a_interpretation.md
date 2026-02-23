# Ecologist Q and A Interpretation Log

This is a living notebook for the ecologist-facing walkthrough of the repository.
It captures:

- your interpretation questions,
- my technical and ecological responses,
- any actions we decide to take,
- and follow-up status.

The goal is to keep a transparent record of human-in-the-loop sanity checks as we review results and presentation.

Path note: after the manuscript reorganisation, canonical manuscript paths are under `paper/manuscript/` and links in this log follow that structure.

## How to use this file

For each question, we add one entry with:

1. `Q-ID` (sequential, e.g. `QA-001`).
2. `Context` (what file/figure/result prompted the question).
3. `Question` (your exact or near-exact wording).
4. `Response` (my answer).
5. `Decision / Action` (what we agreed to do).
6. `Status` (`open`, `answered`, `actioned`, `deferred`).
7. `Links` (paths to figures/files/commits, if relevant).

## Session metadata

- Start date: 2026-02-11
- Mode: ecologist-facing human-testing pass with technical chaperoning
- Scope: interpretation, sanity checks, display clarity, reproducibility UX

## Q and A entries

### QA-001

- Context: kickoff of ecologist-facing review workflow.
- Question: How will we capture interpretation questions and responses as we go?
- Response: Use this file as a timestamped running log with explicit status and action fields so decisions are auditable.
- Decision / Action: create and maintain `docs/q_and_a_interpretation.md` throughout walkthrough.
- Status: actioned
- Links: `docs/q_and_a_interpretation.md`

### QA-002

- Context: Figure 1 caption check against `paper/manuscript/text/figure_captions_v2.md` and current Figure 1 panel file.
- Question: Are Figure 1 caption and figure congruent, and can we move to numbered figure filenames?
- Response:
  - Mostly congruent for panels A, B, and D.
  - One mismatch identified in panel C: caption states "points = replicates, lines = scenario means", but the prior plotting code showed only means.
  - Renaming to numbered figure filenames is straightforward and improves manuscript/pipeline consistency.
- Decision / Action:
  - Update Figure 1 generator so panel C overlays replicate points and mean lines.
  - Rename Figure 1 output target to `fig1_panels.png` (and `.pdf`) in `analysis/run_all.py`.
  - Keep checking later figures in sequence and apply `figN_` naming pattern as we go.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig1_panels.png`, `paper/manuscript/figures/fig1_panels.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-003

- Context: Figure 2 caption check against `paper/manuscript/text/figure_captions_v2.md` and `paper/manuscript/figures/cv_richness_scaling_mixed.png`.
- Question: Is the Figure 2 caption fully congruent with the richness-scaling figure, and can we rename to a numbered figure filename?
- Response:
  - Core pattern is congruent: for `sigma_env > 0`, `CV_tot` drops from `S=2` to `S=4` and continues declining toward `S=8`.
  - Caption-side caveat: it currently says this decline occurs for "all sigma values shown", but `sigma_env=0` is a flat zero baseline (no decline).
  - Methods-side caveat: the plotted mean is currently averaged over the shared non-negative subset (`rho_env >= 0`) for cross-richness comparability, not all requested `rho_env` values.
- Decision / Action:
  - Rename generated Figure 2 output to `fig2_richness_scaling_mixed.png`.
  - Keep current plotting logic unchanged for now (shared non-negative `rho_env` subset), and flag caption wording for refinement.
- Status: answered
- Links: `analysis/run_all.py`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-004

- Context: Figure 2 visual polish pass (legend readability).
- Question: If legend title already defines the symbol (e.g. `sigma_env`/`rho_env`), should legend entries still repeat `symbol = value`?
- Response: Repeating the symbol in each entry is redundant and visually busy. A cleaner convention is: symbol in legend title, numeric values in entries.
- Decision / Action:
  - Simplified Figure 2 legend entries from `sigma_env = value` to `value` while keeping legend title as `sigma_env`.
  - Regenerate and re-check Figure 2 for readability.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`

### QA-005

- Context: Figure 2 caption precision review.
- Question: Can we fix the imprecision in the Figure 2 caption to match what is actually plotted?
- Response:
  - Yes. The original wording overstated two points:
    - `sigma_env=0` is a flat near-zero baseline, not a declining richness trend.
    - The current figure averages over the shared non-negative `rho_env` subset (`rho_env >= 0`) for cross-richness comparability.
- Decision / Action:
  - Updated Figure 2 caption text in `paper/manuscript/text/figure_captions_v2.md` to state both details explicitly.
  - Continued numbered-figure transition by keeping legacy `manuscript_panels.*` assets deleted.
- Status: actioned
- Links: `paper/manuscript/text/figure_captions_v2.md`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`

### QA-006

- Context: Figure asset housekeeping after Figure 2 renaming.
- Question: Should legacy `cv_richness_scaling_mixed.png` be removed now that Figure 2 uses numbered filenames?
- Response: Yes. Keeping only current numbered assets reduces ambiguity and prevents accidental citation of stale files.
- Decision / Action:
  - Deleted `paper/manuscript/figures/cv_richness_scaling_mixed.png`.
  - Deleted `analysis/reports/cv_richness_scaling_mixed.png` for consistency.
- Status: actioned
- Links: `paper/manuscript/figures/fig2_richness_scaling_mixed.png`, `analysis/reports/fig2_richness_scaling_mixed.png`

### QA-007

- Context: Figure 3 caption-vs-plot congruence check for `imposed_vs_realised_panels.png`.
- Question: Does Figure 3 match the v2 caption, and are there any caption bugs to fix?
- Response:
  - Panels A and B are congruent with the caption and summary data.
  - Caption bug identified in Panel C wording: positive-slope deviations are not uniformly near-zero/negative; they are positive at low `rho_env` and become near-zero to modestly negative only at high `rho_env`.
  - Plot-side refinement: panel C previously drew species-level rows as a single connected path per slope mode; this was visually ambiguous.
- Decision / Action:
  - Renamed Figure 3 output to `fig3_imposed_vs_realised_panels.png`.
  - Updated panel C plotting to use richness-averaged regime means (one curve per slope mode) to match caption framing.
  - Updated Figure 3 caption text in `paper/manuscript/text/figure_captions_v2.md` to reflect the corrected positive-regime pattern.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig3_imposed_vs_realised_panels.png`, `paper/manuscript/figures/fig3_imposed_vs_realised_panels.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-008

- Context: Figure 4 caption-vs-plot congruence check for `cv_vs_synchrony_mixed.png`.
- Question: Does Figure 4 match the v2 caption, and is there any caption bug to fix?
- Response:
  - Caption is scientifically congruent with the plotted data and aggregation method (scenario means, post-burn-in, mixed-slope grid).
  - Association direction in both panels is generally positive (higher synchrony metrics tend to correspond to higher `CV_tot`), with expected spread at low richness.
- Decision / Action:
  - No caption wording change required at this step.
  - Rename Figure 4 output to `fig4_cv_vs_synchrony_mixed.png` and update references.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig4_cv_vs_synchrony_mixed.png`, `paper/manuscript/figures/fig4_cv_vs_synchrony_mixed.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-009

- Context: Figure 5 caption-vs-plot congruence check for `cv_phi_sensitivity_sigma0.5_extended.png`.
- Question: Does Figure 5 match the v2 caption, and if not, what should be fixed?
- Response:
  - Core pattern and caption claims are congruent (higher `phi` inflates `CV_tot`; richness effect and generally negative `CV_tot`–`rho_env` association in mixed slopes remain).
  - One mismatch identified: caption states "points show replicate values and lines show scenario means", while the prior plot had means only.
- Decision / Action:
  - Updated Figure 5 plotting to overlay faint replicate points plus mean lines.
  - Renamed Figure 5 output to `fig5_phi_sensitivity_sigma0.5_extended.png` and updated references.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-010

- Context: Figure 5 display polish after the main caption congruence fix.
- Question: Can we simplify and standardise Figure 5 annotations for readability?
- Response: Yes. The requested improvements increase cross-panel comparability and reduce legend clutter without changing data content.
- Decision / Action:
  - Changed y-axis label from `CV_total` to `CV Total`.
  - Changed panel titles to use Greek sigma notation (`σ_env = 0.5`).
  - Forced both panels to the same x-axis scale (`-0.5` to `1.0`) for visual comparability.
  - Simplified legend entries to compact numeric format (`phi (~sigma_eff)`) with a single legend title.
  - Kept only one legend (left panel) to avoid duplication.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`

### QA-011

- Context: Final Figure 5 title/layout polish.
- Question: Can the super-title carry the fixed-environment context and allow cleaner panel titles?
- Response: Yes. Moving the fixed `sigma_env` context to the super-title and leaving panel titles as richness-only improves readability and avoids repetition.
- Decision / Action:
  - Updated Figure 5 super-title to use Greek notation and include fixed `sigma_env=0.5` context.
  - Simplified panel titles to `S=2` and `S=4`.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`

### QA-012

- Context: Supplementary promotion and comparability polish for `run1_cv_total.png` and `run1_phi_ldm.png`.
- Question: Can these become Fig. S1/S2 with cleaner labels and fully shared colour scales within each figure?
- Response: Yes. This is a strong improvement for supplementary readability and cross-panel comparability.
- Decision / Action:
  - Converted mixed-grid heatmaps to supplementary filenames:
    - `figS1_run1_cv_total.png`
    - `figS2_run1_phi_ldm.png`
  - Updated heatmap generation to enforce shared colour limits across richness panels within each metric figure.
  - Replaced panel title text:
    - `cv_total` -> `CV Total`
    - `phi_ldm` -> `φ_LdM`
  - Simplified each figure to a single shared colourbar.
  - Added Figure S1 and Figure S2 captions to `paper/manuscript/text/figure_captions_v2.md`.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/figS1_run1_cv_total.png`, `analysis/reports/figS2_run1_phi_ldm.png`, `paper/manuscript/figures/figS1_run1_cv_total.png`, `paper/manuscript/figures/figS2_run1_phi_ldm.png`, `paper/manuscript/text/figure_captions_v2.md`

## Open action queue

- Figure-by-figure numbered-filename transition completed for Figures 1–5. Continue with any additional display polish requested during manuscript integration.

## Deferred topics

- None yet.
