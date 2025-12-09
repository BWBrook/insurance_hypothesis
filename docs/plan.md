# Project Plan (living document) – Insurance Effect Simulation

> Maintained by the AI agent. Reflects current understanding and near-term actions.

## 1. Working hypothesis (refined)

- Environmental variability can stabilise total community biomass (lower temporal variance or CV) when species respond asynchronously to environmental fluctuations, but the same variability destabilises biomass when responses are synchronous.
- **Stabilisation metric**: reduction in variance and coefficient of variation (CV) of total biomass relative to a low-variance baseline.
- **Asynchrony**: low or negative correlations among species’ environmentally driven growth rates; operationalised via the correlation (ρ) among species-specific environmental anomalies and the Loreau–de Mazancourt synchrony index.

## 2. Model design (planned)

- **Core model**: discrete-time stochastic Ricker with competition  
  `N_i(t+1) = N_i(t) * exp( r0 + b_i * z_i(t) - (N_i(t) + Σ_j α_ij N_j(t)) / K_i )`, truncated at a small floor to prevent negative values.
- **Environmental driver**: multivariate AR(1) process `z_t = φ z_{t-1} + ε_t`, with `ε_t ~ MVN(0, Σ)`; variance scaled by `σ_env^2`, synchrony controlled by off-diagonal correlation `ρ` in Σ. Initial φ planned at 0.4 to allow persistence without long memory.
- **Species differences**: slopes `b_i` arrayed along a gradient (e.g., linearly spaced from negative to positive) so species peak under different environmental anomalies; carrying capacities `K_i` near 100; intra- vs interspecific competition ratio set via `α_inter = c_comp * α_intra` with `c_comp ≈ 0.3`.
- **Numerical safeguards**: floor abundance at `1e-9`; cap exponent to avoid overflow; check for NaN/Inf each step.
- **Tooling choice**: core simulations in **Python 3.12** (uv-managed), with potential R/Python plotting later.

## 3. Experimental grid (initial)

- **Environmental variance (σ_env)**: {0, 0.2, 0.5, 1.0, 1.5}.
- **Response synchrony (ρ)**: {-0.5, 0, 0.5, 0.9, 1.0} via correlation matrix of ε_t.
- **Species richness (S)**: {2, 4, 8}; slope gradients rescaled for each S.
- **AR(1) persistence (φ)**: default 0.4; sensitivity check at 0 and 0.7 in a secondary sweep.
- **Simulation length**: 600 time steps; discard first 300 as burn-in.
- **Replicates per scenario**: 200 (adjust if runtime dictates); random seeds stored for reproducibility.
- **Outputs stored**: community time series summaries and per-scenario aggregate statistics saved under `data/sim/` as compressed parquet/feather.

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

- **Current phase**: 010_model_design (early experimentation).
- **Recently completed**: Full mixed-slope grid (reps=150), positive-slope subset run, covariance PD fix, synchrony metrics/tests, plotting and summary generation.
- **Immediate next steps** (ordered):
  1) Build combined panel figure (heatmaps + key line plots) for manuscript use; ensure assets saved in `analysis/reports/` and referenced.  
  2) Consider φ=0.9 sensitivity run on reduced grid if time permits; otherwise document current φ robustness.  
  3) Add a short findings-to-date summary section in `docs/interpretation_notes.md` and initiate Result Review Cycle checklist.  
  4) Add numerical sanity checks if panels suggest anomalies (e.g., enforce |phi_ldm| ≤ 1, monitor extinction under φ=0.9/σ_env high).  
  5) Begin sketching manuscript Methods/Results bullet points in `manuscript/text/` after panel figure complete.

_This plan should be updated as design choices are made or adjusted._
