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
  5) Manuscript v2 (`manuscript/text/draft_ms_v2.md`) and captions (`manuscript/text/figure_captions_v2.md`) aligned to implemented model conventions (`rho_env` requested vs `rho_eff` effective; `sigma_env` innovation SD; `sigma_eff` stationary SD in φ analyses).
- **Next steps if more work is requested**:
  1) Keep manuscript text aligned with the corrected extinction/floor-occupancy interpretation as external edits continue.
  2) Optional robustness extension beyond equicorrelated Σ (block/gradient covariance structures) on reduced grids.
  3) Packaging/formatting tasks only (reference formatting, journal-specific figure/table assembly).

_This plan should be updated as design choices are made or adjusted._
