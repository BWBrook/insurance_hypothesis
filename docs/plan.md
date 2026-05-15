# Project Plan (living document) – Insurance Effect Simulation

> Maintained by the AI agent. Reflects current understanding and near-term actions.

## 1. Working hypothesis (refined)

- Environmental variability tends to increase the temporal variability of individual species, but **biodiversity can buffer this variability at the community level** when species respond asynchronously to the same driver. When responses are strongly aligned, community variability more closely tracks the environment.
- **Stabilisation / insurance metrics** (all defined **relative**, not absolute):  
  - Community coefficient of variation (CV_total) compared to a single-species or aligned-response baseline under the same σ_env, ρ_env, S, and φ.  
  - CV_total relative to an approximate mean species CV, estimated from simulated species-level means and variances.  
  - Response synchrony indices (Loreau–de Mazancourt φ_LdM and mean pairwise growth-rate correlation), which serve as mechanistic indicators of (a)synchrony that covary with CV_total.
- **Asynchrony**: low or negative correlations among species’ environmentally driven growth rates; operationalised via φ_LdM and mean pairwise growth-rate correlations. Here **ρ_env is an imposed environmental correlation between species’ drivers**, not a synchrony metric by itself; realised synchrony emerges from ρ_env, slopes, and competition.

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

## 3. Experimental grid (completed)

- **Environmental variance (σ_env)**: {0, 0.2, 0.5, 1.0, 1.5} (reduced to {0,0.5,1.0} for φ sensitivity).
- **Imposed environmental correlation (ρ_env)**: {-0.5, 0, 0.5, 0.9, 1.0}; effective values stored as `rho_eff` when clipping is required for PD.
- **Species richness (S)**: {2, 4, 8} for mixed slopes; {4, 8} for positive and positive_matched slopes (S=2 subset at σ=0.5,1.0 for positive pilot).
- **Richness sweep for Figure 4**: additional mixed‑slope grid with S ∈ {2,3,4,5,6,7,8} on the full σ_env–ρ_env grid, stored as `data/sim/grid/run1_richness/summaries.parquet`.
- **AR(1) persistence (φ)**: 0.4 main; sensitivity {0, 0.7, 0.9, 0.95}.
- **Simulation length**: 600 steps (burn 300) for main/positive grids; 400 (burn 200) for φ sweeps.
- **Replicates per scenario**: mixed 150; positive 100; φ sweeps 80.
- **Outputs stored**: parquet summaries under `data/sim/grid/<run_name>/summaries.parquet`.

## 3.1 Production-scale grid extension (planned)

- **Compute target**: run production-scale CPU grids on `deep-server`, using WSL as the control plane and `tmux` for long jobs. Use login-shell remote commands (`ssh deep-server 'bash -lc "..."'`) so `uv` resolves from `~/.local/bin`.
- **Remote storage**: keep bulky run outputs, caches, and scratch material under `/data` on `deep-server`; keep scientific run definitions, summaries, interpretation notes, and reproducible code in this repository.
- **Replicate convention**: use **1000 replicates per scenario/slice** for final-paper production grids unless a run is explicitly a smoke test, pilot, or stress-test subset.
- **First production target**: high-resolution Figure 1 response surfaces for S=4 mixed vs positive slopes, `phi=0.4`, with denser `sigma_env`/`rho_env` values around the visible transition region and `rho_eff`-aware plotting.
- **Frozen first-batch spec**: `analysis/production_specs/fig1_s4_highres_v1.json` defines 570 scenarios (S=4; mixed and positive slopes; 19 `sigma_env` values from 0.0 to 2.0; 15 `rho_env` values from -0.3 to 1.0), 5700 shards, and 570000 expected replicate-summary rows.
- **Acceptance check**: compare high-resolution surfaces against the current coarse/interim grids before replacing display defaults or making manuscript claims depend on the new surfaces.

## 4. Response metrics

- Community mean, variance, and CV of total biomass (post burn-in).
- Loreau–de Mazancourt community synchrony index (φ_LdM) and average pairwise growth-rate correlations.
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

- Target: short theoretical ecology note (Ecology Letters–style).
- Sections: Introduction (insurance hypothesis framing); Methods (model, grid, metrics); Results (figures: variance vs σ_env by ρ and S); Discussion (conditions for stabilisation, limitations, robustness); Methods appendix with parameter tables.

## 8. Current status & next steps

- **Current phase**: post-review polishing and reproducibility QA (pre-submission handoff state).
- **Recently completed**:
  1) Full mixed and positive grids plus controls (`positive_matched`, `no_comp_*`, `mixed_narrow`) and φ sensitivity through 0.95.
  2) Numbered manuscript figure suite (`fig1_*` to `fig5_*`, `figS1_*` to `figS3_*`) and cached-data orchestration (`analysis/run_all.py`) with reproducible regeneration.
  3) Pylance/type-hint cleanup, `rho_eff` handling in summaries/plots, and test suite expansion (`uv run pytest` currently 8 tests).
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
- **Next steps if more work is requested**:
  1) Finish the ecologist-facing output walkthrough and collect figure/display/scientific sanity issues.
  2) Review the rebuilt production Figure 2 display and decide whether the faint `rho_eff` range bands should remain in the main panel.
  3) Re-review the manuscript Results text against the production Figure 1 and Figure 2 artefacts.
  4) Decide whether to extend production surfaces to S=2/S=8 for mixed-vs-aligned contrasts or instead prioritise the remaining manuscript/figure revision around the new Figure 1 and Figure 2 evidence.
  5) Optional robustness extension beyond equicorrelated Σ (block/gradient covariance structures) on reduced grids.
  6) Approval-gated work only for changes that would alter scientific metric definitions, output schemas, or the data-distribution strategy for fresh-clone reproducibility.

_This plan should be updated as design choices are made or adjusted._
