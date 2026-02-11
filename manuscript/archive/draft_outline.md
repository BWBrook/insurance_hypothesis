# Draft outline

## Introduction
- Frame insurance hypothesis: environmental variability can stabilise aggregate biomass when species respond asynchronously; destabilises when responses synchronous.
- Contributions: fully simulated test across variance, synchrony, richness, and environmental persistence; explicit contrast between mixed vs aligned response slopes.

## Methods
- Model: stochastic Ricker with competition; equation and parameters (r0, K=100, α_intra=1, α_inter=0.3, floor).
- Environmental process: AR(1) with σ_env, ρ, φ; equicorrelated innovations; safeguards for PD covariance.
- Species responses: mixed slopes (-0.5..0.5) vs positive slopes (0.1..1.0).
- Grids: main mixed (σ_env 0–1.5, ρ -0.5–1.0, S 2/4/8, φ=0.4); positive slopes (same σ/ρ, S 4/8); φ sweeps (φ 0–0.95 on reduced grid S 2/4, σ 0/0.5/1.0).
- Metrics: CV of total biomass, φ_LdM synchrony, mean pairwise growth corr, extinction frequency. Burn-in 300/600 steps; reps 150 (mixed), 100 (positive), 80 (φ sweeps).
- Sanity/tests: non-negativity, equilibrium at σ=0, PD covariance, φ_LdM bound, extinction check.

## Results
- Mixed slopes: CV decreases with ρ and with richness; realised synchrony often negative even when imposed ρ>0.
- Positive slopes: CV and φ_LdM increase with ρ; richness reduces magnitude but not direction.
- Synchrony divergence: imposed vs realised scatter; delta_corr negative for mixed, positive for aligned.
- φ sensitivity: higher φ modestly increases CV but patterns persist to φ=0.95.
- Extinction minimal.
- Key figures: manuscript_panels.pdf + richness/persistence overlays.

## Discussion
- Mechanistic interpretation: response-direction heterogeneity turns environmental synchrony into compensatory dynamics; alignment removes insurance.
- Richness as amplifier of insurance under heterogeneity; limited buffering when responses aligned.
- Robustness to φ; limitations (equicorrelation assumption, static competition, no demographic stochasticity).
- Future work: alternative competition structures, trait distributions, non-equicorrelated drivers, inclusion of demographic noise.

## Reproducibility
- uv-managed Python env; entrypoints `analysis/run_full_grid.py`, `analysis/plot_grid.py`; data in `data/sim/grid/*`; tests via `uv run pytest`.
