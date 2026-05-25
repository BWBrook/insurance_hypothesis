# Project Plan (living document) – Insurance Effect Simulation

> Maintained by the AI agent. Reflects current understanding and near-term actions.

## 1. Working hypothesis (refined)

- Environmental variability tends to increase the temporal variability of individual species, but **biodiversity can buffer this variability at the community level** when species respond asynchronously to the same driver. When responses are strongly aligned, community variability more closely tracks the environment.
- **Stabilisation / insurance metrics** (all defined **relative**, not absolute):  
  - Community coefficient of variation (CV_total) compared to a species-poor or aligned-response baseline under the same σ_env, ρ_env, S, and φ.
  - CV_total relative to an approximate mean species CV, estimated from simulated species-level means and variances.  
  - Response synchrony indices (Loreau–de Mazancourt φ_LdM and mean pairwise realised per-capita log-growth correlation), which serve as mechanistic indicators of (a)synchrony that covary with CV_total.
  - Variance decomposition of total biomass into summed species variances and aggregate covariance terms for selected production scenarios.
- **Asynchrony**: low or negative correlations among species’ realised per-capita log-growth rates; operationalised via φ_LdM and mean pairwise realised log-growth correlations. Here **ρ_env is an imposed environmental correlation between species’ drivers**, not a synchrony metric by itself; realised synchrony emerges from ρ_env, slopes, and competition.

## 2. Model design (implemented)

- **Core model**: discrete-time stochastic Ricker with competition  
  `N_i(t+1) = N_i(t) * exp( r0 + b_i * z_i(t) - (N_i(t) + Σ_j α_ij N_j(t)) / K_i )`, truncated at a small floor to prevent negative values.
- **Environmental driver**: multivariate AR(1) process `z_t = φ z_{t-1} + ε_t`, with `ε_t ~ MVN(0, Σ)`; innovation variance scaled by `σ_env^2`, imposed environmental correlation controlled by off-diagonal `ρ_env` in Σ. Default φ=0.4; sensitivity runs at φ ∈ {0, 0.7, 0.9, 0.95}. When a requested `ρ_env` is infeasible for equicorrelation at given S, the simulator clips to the nearest feasible value and records effective `rho_eff`.
- **Species differences**: four slope modes are now used in the experiment suite:
  - mixed slopes linearly spaced -0.5..0.5 (heterogeneous responses),
  - all-positive slopes 0.1..1.0 (aligned responses),
  - mixed_narrow slopes -0.25..0.25 (magnitude sensitivity),
  - positive_matched slopes `|b_i(mixed)|` (sign-structure control with matched magnitudes).
  K_i=100; intra- vs interspecific competition ratio `α_inter = 0.3 * α_intra`.
- **Numerical safeguards**: floor abundance at `1e-9`; cap exponent; φ_LdM clipped to [0,1]; checks for NaN/Inf each step.
- **Tooling choice**: core simulations in **Python 3.12** (uv-managed); plotting with matplotlib.

## 3. Experimental grid (production state)

- **Compute target**: production-scale CPU grids run on `deep-server` under `tmux`, controlled from WSL. Bulky remote outputs and scratch material live under `/data` on `deep-server`; compact retrieved summaries live under `data/sim/production/` locally.
- **Replicate convention**: final-paper production grids use **1000 replicates per scenario** unless a run is explicitly labelled as a pilot, smoke test, or exploratory control.
- **Figure 1 production grid**: S=4 mixed and positive slopes, `phi=0.4`, 600 steps / 300 burn-in, 15 requested `rho_env` values from -0.3 to 1.0, 19 core `sigma_env` values from 0.0 to 2.0, plus a labelled high-variance stress extension to `sigma_env=4.0`.
- **Figures 2 and 4 production grid**: mixed slopes, S=2..8, `phi=0.4`, 600 steps / 300 burn-in, `sigma_env` in {0, 0.2, 0.5, 1.0, 1.5, 2.0}, and non-negative requested `rho_env` in {0, 0.25, 0.5, 0.75, 1.0}. Figure 2 uses richness means; Figure 4 reuses the same scenario means for CV-synchrony relationships.
- **Figure 3 production grid**: mixed and positive slopes, S in {2, 4, 8}, `sigma_env=0.5`, `phi=0.4`, requested `rho_env` from 0 to 1 in increments of 0.1, 600 steps / 300 burn-in.
- **Figure S3 production control**: mixed, positive_matched, and positive slopes, S in {4, 8}, `sigma_env=0.5`, `phi=0.4`, requested `rho_env` from 0 to 1 in increments of 0.1, 600 steps / 300 burn-in.
- **Figure 5 production grid**: mixed slopes, S in {2, 4}, `sigma_env=0.5`, `phi` in {0, 0.7, 0.9, 0.95}, requested `rho_env` in {-0.5, -0.25, 0, 0.25, 0.5, 0.75, 0.9, 1.0}, 600 steps / 300 burn-in.
- **Exploratory and control grids**: no-competition and mixed-narrow controls remain lower-replicate robustness diagnostics unless selected later for production refresh; the positive-matched sign-structure control is now production-backed for Figure S3.
- **Outputs stored**: versioned production specs under `analysis/production_specs/`; compact production parquet summaries under `data/sim/production/<run_name>/`; exploratory/control summaries under `data/sim/grid/<run_name>/`.

## 4. Response metrics

- Community mean, variance, and CV of total biomass (post burn-in).
- Loreau–de Mazancourt community synchrony index (φ_LdM) and average pairwise realised per-capita log-growth correlations.
- Variance decomposition: $\operatorname{Var}(N_{\mathrm{tot}})=\sum_i\operatorname{Var}(N_i)+2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$.
- Species-level extinction frequency and mean biomass.
- Stability ratio: variance at given σ_env, ρ relative to baseline σ_env = 0 case.
- Optional: temporal β-diversity/turnover (if informative).

## 5. Sanity checks & validation (to be encoded in tests)

- **Deterministic baseline**: with σ_env = 0, trajectories approach equilibrium near K_i; no extinctions under default parameters.
- **Perfect imposed correlation**: ρ_env = 1 should yield community CV close to species-level CV when responses are aligned (little insurance effect).
- **Negative/low imposed correlation**: lower ρ_env should reduce community CV under aligned responses.
- **Richness effect**: holding parameters constant, higher S with low realised synchrony should further reduce community variance.
- **High-φ stress behaviour**: at φ ≥ 0.9 with high σ_env and low S, monitor floor occupancy explicitly and treat these runs as stress tests rather than low-extinction baseline scenarios.
- **Numerical**: no NaN/Inf; abundances non-negative; statistics converge as replicates increase.
- Cross-check small toy case against an independent vectorised implementation or analytic approximation of equilibrium at σ_env = 0.

## 6. Result Review Cycle (pointer)

- Follow `docs/workflow.md`: for each key figure/table → run sanity checks → record interpretation bullets in `docs/interpretation_notes.md` → queue follow-ups → iterate until coherent.
- Production-scale execution is staged in `docs/production_execution_plan.md`.

## 7. Manuscript plan (outline)

- Target: concise theoretical ecology manuscript for Oikos.
- Sections: Introduction (insurance hypothesis framing); Methods (model, grid, metrics); Results (figures: variance vs σ_env by ρ and S); Discussion (conditions for stabilisation, limitations, robustness); Methods appendix with parameter tables.

## 8. Current status & next steps

- **Current phase**: post-review polishing and reproducibility QA (pre-submission handoff state).
- **Recently completed**:
  1) Full mixed and positive grids plus controls (`positive_matched`, `no_comp_*`, `mixed_narrow`) and φ sensitivity through 0.95.
  2) Numbered manuscript figure suite (`fig1_*` to `fig5_*`, `figS1_*` to `figS3_*`) and cached-data orchestration (`analysis/run_all.py`) with reproducible regeneration.
  3) Pylance/type-hint cleanup, `rho_eff` handling in summaries/plots, and test suite expansion.
  4) Post-hiatus audit identifying that high-φ stress grids have non-negligible floor occupancy in a subset of scenarios, with documentation corrected accordingly.
  5) Manuscript v2 (`paper/manuscript/text/draft_ms_v2.md`) and captions (`paper/manuscript/text/figure_captions_v2.md`) aligned to implemented model conventions (`rho_env` requested vs `rho_eff` effective; `sigma_env` innovation SD; `sigma_eff` stationary SD in φ analyses).
  6) `paper/` hierarchy harmonised for makedoc handoff (`paper/settings/build.yaml`, `paper/manuscript/text/figures.md`, `paper/references/ih_references.yaml`) with path mapping rewritten away from legacy `manuscript/` references.
  7) makedoc profile finalised with dual profiles (`ih_draft` scoped lint; `ih_submission` strict lint) and single canonical bibliography (`paper/references/ih_references.yaml`); manuscript file references are now config-relative for cross-platform portability.
  8) Environment bootstrap QA rerun on 2026-03-06: `uv sync --dev`, `uv run pytest`, `uv run pyright`, and the README preview workflow all verified after fixing preview-schema compatibility and pandas-stub typing issues.
  9) Repo hardening pass on 2026-03-07: added GitHub Actions CI, expanded test coverage to runner/schema/validation/scientific-invariant checks (`uv run pytest` now 23 tests), moved durable reporting/figure helpers into `src/python/insurance_sim/`, and tightened config validation without changing the documented CLI/output contract.
  10) Compute planning pass on 2026-05-14: reviewed `/home/bwbrook/work/nectar`, validated `deep-server` access/inventory with the control-plane scripts, and adopted `deep-server` plus 1000 replicates per scenario/slice as the default production-grid convention.
  11) Production harness Phase 3 implementation completed on 2026-05-14: added a manifest/shard/combine/validate runner, deterministic production-only per-replicate seeding, tests, and `deep-server` helper scripts for sync/check, tmux smoke launch, status, and artifact retrieval. Local tests/type checks passed, and a tiny tmux-managed remote smoke run completed on `deep-server`.
  12) Remote production benchmark completed on 2026-05-14: two S=4, 1000-replicate-per-scenario benchmark runs validated on `deep-server`; the wider 48-worker scout processed 10000 production-shaped replicate summaries across 10 scenarios in 6.85 seconds of `run-pending` wall time.
  13) First production grid spec frozen on 2026-05-14: `analysis/production_specs/fig1_s4_highres_v1.json` now defines the S=4 high-resolution Figure 1 batch, and `analysis/production_grid.py create-manifest-from-spec` can generate manifests directly from versioned JSON specs.
  14) First production batch completed on 2026-05-14: `fig1-s4-highres-v1` validated on `deep-server` with 570000 rows across 570 scenarios, then compact outputs were retrieved locally under `data/sim/production/fig1_s4_highres_v1/` and quicklook figures were generated under `analysis/reports/production/`.
  15) High-sigma extension completed on 2026-05-15: Barry's first read of the production surface indicated that the mixed-slope response likely needs `sigma_env > 2`; `fig1-s4-highsigma-v1` validated on `deep-server` with 180000 rows and shows the insurance contrast persists but narrows by `sigma_env=4.0`, while floor/extinction frequency rises enough to treat `sigma_env > 3` as a stress region.
  16) Figure 1 display candidate revised on 2026-05-15: added `analysis/plot_production_fig1.py` and `src/python/insurance_sim/production_figures.py` to build a two-panel production Figure 1 candidate that foregrounds the aligned-response surface and the mixed-vs-aligned divergence across `sigma_env`.
  17) Figure 1 promotion started on 2026-05-15: the accepted two-panel production display is now the canonical `fig1_panels` target, with `analysis/run_all.py` set to prefer production Figure 1 inputs when local compact production summaries are present.
  18) Figure 2 production spec frozen on 2026-05-15: `analysis/production_specs/fig2_richness_mixed_v1.json` defines a 210-scenario, 210000-row mixed-slope richness grid for S=2..8, non-negative `rho_env`, `sigma_env` up to 2.0, and 1000 replicates per scenario.
  19) Figure 2 production run completed on 2026-05-15: `fig2-richness-mixed-v1` validated on `deep-server` with 210000 rows across 210 scenarios and 2100 shards; compact outputs were retrieved locally and production Figure 2 was rebuilt under `analysis/reports/`.
  20) Figure 3 production spec frozen on 2026-05-18: `analysis/production_specs/fig3_synchrony_v1.json` defines a focused 66-scenario, 66000-row imposed-vs-realised synchrony grid at `sigma_env=0.5` for mixed and positive slopes, S=2/4/8, non-negative `rho_env`, and 1000 replicates per scenario.
  21) Figure 3 production run completed on 2026-05-18: `fig3-synchrony-v1` validated on `deep-server` with 66000 rows across 66 scenarios and 660 shards; compact outputs were retrieved locally and production Figure 3 was rebuilt under `analysis/reports/`.
  22) Figure 4 production rebuild completed on 2026-05-18: the validated `fig2-richness-mixed-v1` production grid is now used as the production source for CV-vs-synchrony scenario means, avoiding a redundant new run; production PNG/PDF and a scenario summary CSV were rebuilt under `analysis/reports/`.
  23) Submission-display polish started on 2026-05-18: production Figure 1-4 builders now omit embedded figure titles/suptitles so caption text, not PNG text, carries the short-title information.
  24) Figure 5 production run completed on 2026-05-18: `fig5-persistence-mixed-v1` validated on `deep-server` with 64000 rows across 64 scenarios and 640 shards; compact outputs were retrieved locally and production Figure 5 was rebuilt under `analysis/reports/`.
  25) Manuscript/caption reconciliation pass completed on 2026-05-18: Barry accepted Figure 5, and the draft Results/Methods/Discussion plus figure captions were checked against production Figures 1-5, with stale replicate-grid wording and requested-vs-effective correlation wording tightened.
  26) Table and supplementary artefact sweep completed on 2026-05-19: Table 1 was replaced with a production-aligned parameter/run-spec table, Tables S1-S3 were added, and supplementary Figures S1/S2/S4 were rebuilt from production outputs.
  27) Figure S3 production refresh completed on 2026-05-19: `figs3-positive-matched-control-v1` validated on `deep-server` with 66000 rows across 66 scenarios and 660 shards; compact outputs were retrieved locally and Figure S3 was rebuilt as a production-backed positive-matched sign-structure control.
  28) Post-refresh validation completed on 2026-05-19: `uv run pytest -q`, `uv run pyright`, `git diff --check`, makedoc `make validate-config`, and makedoc `make check` all passed.
  29) Cached-grid dependency wrinkle fixed on 2026-05-21: `analysis/run_all.py` can now regenerate the production-backed figure suite from `data/sim/production/` summaries without requiring untracked legacy `data/sim/grid/` caches; a regression test covers this production-only fast path.
  30) Oikos submission-readiness pass started on 2026-05-21: the current production checkpoint was committed and pushed, a double-blind `ih_submission` profile was added, the unblinded title page and anonymous supplementary information builds were separated, and the de-identified review-code package was documented as a deferred final-code-lock task.
  31) 2026 literature and Methods detail refresh completed on 2026-05-21: four relevant 2026 response-diversity/synchrony references were added with verified DOIs, a Zotero DOI import helper was created, and the Methods now explicitly names Python 3.12 plus the main analysis/import stack.
  32) Final pre-Barry submission chaperone pass started on 2026-05-21: a missing cover letter was drafted as a separate editor-facing profile, build-facing figure captions were expanded from one-line alt text to full informative captions, main-text references to supplementary details were softened to "Supporting information", and generated DOCX identity metadata is now sanitized after build.
  33) Independent pre-submission review response started on 2026-05-23: the first pass adds the analytical environmental-response covariance mechanism, corrects the deterministic equilibrium and production-seeding wording, revises richness and persistence-language caveats, brings the positive-matched control into the main Results, and adds production-derived variance-decomposition and Figure 4 association diagnostics.
  34) Oikos/NSO submission-composition check completed on 2026-05-25: live NSO guidance now confirms that data/code availability should not be in the main text file, so the blinded main profile contains only the anonymous article text, tables, and figures; required submission statements are held in a separate `ih_submission_form_statements` profile for ScholarOne support.
  35) De-identified review-code package built on 2026-05-25: `/home/bwbrook/papers/de_identified_repos/ih_package.zip` now contains a minimal anonymous Python/uv package with code, tests, production specs, and compact production summaries, validated from the staged package under Python 3.12.
- **Next steps if more work is requested**:
  1) Run one final submission artefact build/identity check after committing this package-hardening pass.
  2) Barry-only final pass: confirm funding text, acknowledgements, conflict statement, title-page metadata, cover-letter voice, and final archive destination.
  3) Approval-gated work only for changes that would alter scientific metric definitions, output schemas, new simulation scope, or the data-distribution strategy for fresh-clone reproducibility.

_This plan should be updated as design choices are made or adjusted._
