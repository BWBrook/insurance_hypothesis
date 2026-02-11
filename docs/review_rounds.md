# Review Rounds – PI handoff

## Plain-language summary
- **Question**: When does biodiversity buffer the destabilising effect of environmental variability on total community biomass (insurance effect), and when does it fail to do so?
- **Approach**: Simulated communities using a stochastic Ricker model with competition. Species’ environmental response slopes are either heterogeneous (mixed signs) or aligned (all positive). Environmental driver is multivariate AR(1) with controllable variance (σ_env), imposed environmental correlation among species’ drivers (ρ_env), and persistence (φ). We vary σ_env, ρ_env, richness (S), and φ.

## Main results
- Mixed slopes (heterogeneous responses): community CV decreases with both richness and higher imposed ρ because realised growth correlations become negative (compensatory dynamics). Example at σ=0.5, ρ=0.5: CV S=2 ≈0.15, S=4 ≈0.08, S=8 ≈0.06.
- Positive slopes (aligned responses): CV and φ_LdM increase with ρ; richness dampens magnitude but variability stays higher than mixed cases (σ=0.5, ρ=0.5, S=4 CV ≈0.26).
- Imposed vs realised synchrony: mixed slopes produce realised correlations below imposed (mean delta_corr ≈ -0.32), positive slopes above imposed (≈ +0.18).
- Environmental persistence: Increasing φ (0→0.95) inflates CV but does not reverse patterns; insurance signal persists, though very high φ (0.95) notably raises CV for low richness.
- Extinction/floor occupancy is very low in the main inference grids (`run1` max mean extinction frequency ~0.0033; `pos_full` max ~0.022), but high-persistence stress tests include non-negligible floor occupancy in a subset of low-richness/high-variance scenarios (`phi09_reduced` max ~0.24; `phi095_reduced` max ~0.43).

## Limitations / caveats
- Equicorrelated environmental covariance; no alternative correlation structures tested.
- Competition coefficients and slope distributions are fixed (not sampled); demographic stochasticity omitted.
- φ up to 0.95 tested; extreme near-random-walk (φ→1) not explored beyond 0.95.
- Figures derived from cached simulation outputs (parquet files in `data/sim/grid/`). Entry point can rerun but is slower.

## What to look at
- Figures: `analysis/reports/fig1_panels.pdf` (also copied to `manuscript/figures/`) plus `fig5_phi_sensitivity_sigma0.5_extended.png`.
- Manuscript draft: `manuscript/text/draft_ms_v2.md` (outline, parameter table, key numbers) and captions in `manuscript/text/figure_captions_v2.md`.
- Interpretation notes: `docs/interpretation_notes.md` for per-figure takeaways and follow-ups.

## Suggested PI focus / questions (Round 1)
- Is the equicorrelated AR(1) driver sufficient, or should we explore alternative covariance structures to test robustness of the insurance signal?
- Is the contrast between mixed vs aligned slopes framed clearly enough for publication, or should we include intermediate trait-structure scenarios?
- Are the current φ explorations (to 0.95) adequate, or should we push closer to φ→1 or add demographic noise?

---

## Round 2 – PI follow-up (accepted content)

- The PI confirms that, with the revised framing (relative insurance), added controls (no competition, mixed_narrow slopes), explicit σ_env/φ conventions, and synchrony/CV analyses, the **scientific content is in good shape**.
- Current replicate counts (150 mixed, 100 positive, 80 φ and controls) yield **very small Monte Carlo uncertainty** relative to effect sizes; no need to rerun simulations solely to increase replicates.
- Remaining work is classified as final polishing: small clarifications of Monte Carlo error in the manuscript, consistent notation (σ_env, σ_eff, ρ_env, φ_LdM), and standard reference/citation formatting.
- Exploration of non-equicorrelated environmental covariance structures is explicitly deferred to future robustness work; this is noted in Discussion and in `docs/questions_for_human.md`.

## Round 3 – Post-hiatus audit note (2026-02-11)

- Re-audit confirmed core conclusions and reproducibility pipeline still hold (`uv run pytest`, `uv run python analysis/run_all.py`).
- Corrected stale wording from earlier notes that implied negligible extinction across all φ sweeps.
- Final interpretation now distinguishes:
  - low floor occupancy in the main inference grids (`run1`, `pos_full`), and
  - non-negligible floor occupancy in subsets of high-persistence stress grids (`phi09_reduced`, `phi095_reduced`), primarily at low richness and high σ_env.

## Round 4 – Manuscript v2 alignment pass (2026-02-11)

- Updated manuscript artifact references to the active v2 files:
  - draft: `manuscript/text/draft_ms_v2.md`
  - captions: `manuscript/text/figure_captions_v2.md`
- Integrated key critique clarifications directly into v2 prose:
  - explicit `rho_env` (requested) vs `rho_eff` (effective),
  - explicit positive-matched slope control definition in Methods,
  - sample-variance wording aligned with implementation,
  - numerical-guard diagnostics and high-stress interpretation language.
- Added supplementary Figure S3 handling in pipeline output (`figS3_positive_matched_control.png`) to surface the magnitude-matched aligned-slope control used in robustness checks.
