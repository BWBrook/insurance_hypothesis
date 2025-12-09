# Project Plan (living document) – Insurance Effect Simulation

> Maintained by the AI agent. Reflects current understanding and near-term actions.

## 1. Working hypothesis (refined)

- Environmental variability can stabilise total community biomass (lower temporal variance or CV) when species respond asynchronously to environmental fluctuations, but the same variability destabilises biomass when responses are synchronous.
- **Stabilisation metric**: reduction in variance and coefficient of variation (CV) of total biomass relative to a low-variance baseline.
- **Asynchrony**: low or negative correlations among species’ environmentally driven growth rates; operationalised via the correlation (ρ) among species-specific environmental anomalies and the Loreau–de Mazancourt synchrony index.

## 2. Model design (implemented)

- **Core model**: discrete-time stochastic Ricker with competition  
  `N_i(t+1) = N_i(t) * exp( r0 + b_i * z_i(t) - (N_i(t) + Σ_j α_ij N_j(t)) / K_i )`, truncated at a small floor to prevent negative values.
- **Environmental driver**: multivariate AR(1) process `z_t = φ z_{t-1} + ε_t`, with `ε_t ~ MVN(0, Σ)`; variance scaled by `σ_env^2`, synchrony controlled by off-diagonal correlation `ρ` in Σ. Default φ=0.4; sensitivity runs at φ ∈ {0, 0.7, 0.9, 0.95}. Covariance clipped to keep ρ<1 for PD.
- **Species differences**: two slope modes: mixed slopes linearly spaced -0.5..0.5 (heterogeneous responses) and all-positive slopes 0.1..1.0 (aligned responses). K_i=100; intra- vs interspecific competition ratio `α_inter = 0.3 * α_intra`.
- **Numerical safeguards**: floor abundance at `1e-9`; cap exponent; φ_LdM clipped to [0,1]; checks for NaN/Inf each step.
- **Tooling choice**: core simulations in **Python 3.12** (uv-managed); plotting with matplotlib.

## 3. Experimental grid (completed)

- **Environmental variance (σ_env)**: {0, 0.2, 0.5, 1.0, 1.5} (reduced to {0,0.5,1.0} for φ sensitivity).
- **Response synchrony (ρ)**: {-0.5, 0, 0.5, 0.9, 1.0}.
- **Species richness (S)**: {2, 4, 8} for mixed slopes; {4, 8} for positive slopes (S=2 subset at σ=0.5,1.0).
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
- **Perfect synchrony**: ρ = 1 should yield community CV close to species-level CV (little insurance effect).
- **Negative/low synchrony**: ρ ≤ 0 should reduce community CV relative to species-level CV.
- **Richness effect**: holding parameters constant, higher S with low ρ should further reduce community variance.
- **Numerical**: no NaN/Inf; abundances non-negative; statistics converge as replicates increase.
- Cross-check small toy case against an independent vectorised implementation or analytic approximation of equilibrium at σ_env = 0.

## 6. Result Review Cycle (pointer)

- Follow `docs/workflow.md`: for each key figure/table → run sanity checks → record interpretation bullets in `docs/interpretation_notes.md` → queue follow-ups → iterate until coherent.

## 7. Manuscript plan (outline)

- Target: short theoretical ecology note (Ecology Letters–style).
- Sections: Introduction (insurance hypothesis framing); Methods (model, grid, metrics); Results (figures: variance vs σ_env by ρ and S); Discussion (conditions for stabilisation, limitations, robustness); Methods appendix with parameter tables.

## 8. Current status & next steps

- **Current phase**: 010_model_design → transitioning to reporting.
- **Recently completed**: Full mixed and positive grids, φ sensitivity to 0.95, combined panels, manuscript scaffolding, φ_LdM bound tests.
- **Immediate next steps** (ordered):
  1) Finalise manuscript text (Methods/Results/Discussion) in `manuscript/text/draft.md` using current figures/captions.  
  2) Minor figure polish if needed; keep `analysis/reports/manuscript_panels.pdf` as bundle for reviewers.  
  3) Maintain sanity tests (φ_LdM bound) and rerun `uv run pytest` after edits.  
  4) Prep for external review: ensure README/docs point to key runs/figures; package zip when ready.  

_This plan should be updated as design choices are made or adjusted._
