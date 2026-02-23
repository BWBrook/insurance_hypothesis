# Methods & Results Notes (working draft)

## Model & simulation setup
- Discrete-time stochastic Ricker model with intra/inter-specific competition; per-capita growth `r0 + b_i * z_i(t) - (N_i + Σ_j α_ij N_j)/K_i`.
- Environmental driver: multivariate AR(1) with equicorrelated innovations (σ_env controls variance, ρ controls synchrony), persistence φ; safeguards for PD covariance and non-negativity.
- Slopes:
  - Mixed slopes default: linear -0.5..0.5 to induce opposing responses.
  - Positive slopes: 0.1..1.0 to enforce aligned responses.
- Parameters: K=100, α_inter=0.3 * α_intra; floor=1e-9. Time horizon 600 (burn 300) for main grid; replicates 150 (mixed), 100 (positive), 80 (φ sweeps).

## Experimental grids
- Main mixed grid: σ_env {0,0.2,0.5,1.0,1.5} × ρ {-0.5,0,0.5,0.9,1.0} × S {2,4,8}, φ=0.4.
- Positive-slope grid: same σ_env–ρ grid, S {4,8}, φ=0.4 (plus subset S=2 σ_env {0.5,1.0}).
- φ sensitivity grids (mixed slopes): φ ∈ {0,0.4,0.7,0.9,0.95} on reduced σ_env {0,0.5,1.0} × ρ {-0.5,0,0.5,0.9,1.0}, S {2,4}.

## Key results (high level)
- Mixed slopes: community CV decreases with richness and with higher ρ; realised growth correlations often negative even when ρ>0, enabling compensation. At σ=0.5, ρ=0.5: CV S=2 ≈0.15, S=4 ≈0.08, S=8 ≈0.06.
- Positive slopes: CV and φ_LdM increase with ρ; richness dampens magnitude but not direction (σ=0.5, ρ=0.5: CV S=4 ≈0.26, S=8 ≈0.24).
- Synchrony divergence: mixed slopes show mean (realised – imposed) corr ≈ -0.32; positive slopes ≈ +0.18; φ=0.9 still gives negative deltas for mixed slopes.
- φ effects: higher φ modestly raises CV but does not flip patterns; σ=0.5, ρ=0.5, S=2 CV rises 0.138→0.223 when φ 0→0.9.
- Extinctions negligible across grids (max mean extinction freq ~0.003).

## Figures (current)
- `analysis/reports/manuscript_panels.pdf` – combined panels (heatmaps mixed vs positive, CV lines, imposed vs realised synchrony, φ sensitivity).
- Additional singles in `analysis/reports/` (heatmaps, lines, scatter).

## Next drafting steps
- Write Methods: model equations, parameter table, grid design, metrics (CV, φ_LdM, growth correlations), simulation length/replicates, sanity checks.
- Write Results narrative: contrast mixed vs positive slopes; richness and σ_env effects; imposed vs realised synchrony; φ robustness; extinction check.
- Insert key numbers (CV values above) and refer to manuscript_panels.pdf for visuals.
