# Title (placeholder)
Insurance effects in simulated communities: when environmental variance stabilises biomass, and when it does not

## Introduction
Environmental variability can destabilise populations, but theory predicts an **insurance effect**: when species respond asynchronously, fluctuations cancel and community biomass stabilises. We probe this mechanism in fully simulated communities, contrasting heterogeneous response slopes (mixed signs) with aligned slopes (all positive). We manipulate environmental variance (σ_env), imposed driver synchrony (ρ), species richness (S), and temporal autocorrelation (φ) to map where insurance holds or fails.

## Methods
- **Community dynamics**: discrete-time stochastic Ricker with intra/inter-specific competition, per-capita growth `r0 + b_i z_i(t) - (N_i + Σ_j α_ij N_j)/K_i`; abundance floored at 1e-9.
- **Environment**: multivariate AR(1) with variance σ_env² and equicorrelation ρ; persistence φ. Covariance clipped to remain PD; σ_env=0 gives deterministic baseline.
- **Responses**: mixed slopes (linear -0.5..0.5) versus positive slopes (0.1..1.0). Fixed parameters: r0=1, K=100, α_intra=1, α_inter=0.3.
- **Design**:
  - Mixed grid: σ_env {0,0.2,0.5,1.0,1.5} × ρ {-0.5,0,0.5,0.9,1.0} × S {2,4,8}, φ=0.4, 600 steps (300 burn), 150 reps.
  - Positive grid: same σ_env–ρ with S {4,8} (+ small S=2 subset at σ=0.5,1.0), 100 reps.
  - φ sweeps (mixed): φ ∈ {0,0.4,0.7,0.9,0.95} on σ_env {0,0.5,1.0} × ρ {-0.5,0,0.5,0.9,1.0}, S {2,4}, 80 reps.
- **Metrics**: CV of total biomass; Loreau–de Mazancourt synchrony φ_LdM (clipped [0,1]); mean pairwise growth correlation; extinction frequency. Plots via matplotlib; outputs parquet.
- **Sanity/tests**: PD covariance; σ_env=0 equilibrium; non-negativity; φ_LdM bound; synchrony edge cases. Automated with `uv run pytest`.

### Parameter summary
| Parameter | Value(s) |
| --- | --- |
| r0 | 1.0 |
| K_i | 100 |
| α_intra | 1.0 |
| α_inter | 0.3 |
| b_i (mixed) | linspace(-0.5, 0.5) |
| b_i (positive) | linspace(0.1, 1.0) |
| σ_env | 0–1.5 (see grids) |
| ρ | -0.5 to 1.0 |
| φ | 0–0.95 |
| steps / burn | 600 / 300 (main), 400 / 200 (reduced) |
| reps | 150 (mixed), 100 (positive), 80 (φ sweeps) |

## Results
- **Insurance with heterogeneous responses**: In mixed slopes, CV falls with richness and with higher ρ because realised growth correlations become negative even when drivers are synchronous. At σ=0.5, ρ=0.5: CV S=2 ≈0.15, S=4 ≈0.08, S=8 ≈0.06.
- **Loss of insurance with aligned responses**: Positive slopes show CV and φ_LdM rising with ρ; richness damps magnitude but CV remains above mixed cases (σ=0.5, ρ=0.5, S=4 CV ≈0.26).
- **Imposed vs realised synchrony**: Mixed slopes yield realised correlations below imposed (mean delta_corr ≈ -0.32); positive slopes above imposed (≈ +0.18). Panel D in `manuscript_panels.pdf`.
- **Environmental persistence**: Raising φ from 0→0.95 inflates CV but not qualitative patterns; σ=0.5, ρ=0.5 CV S=2 moves 0.138→0.585, S=4 moves 0.074→0.354. Insurance signal persists, especially with higher richness.
- **Extinctions**: negligible (max mean extinction freq ~0.003) across all grids.

## Discussion
- **Mechanism**: Response-direction heterogeneity turns shared environmental variation into compensatory growth, decoupling imposed driver synchrony from realised synchrony; aligned responses transmit driver covariance directly to community variance.
- **Role of richness**: More species amplify compensation when responses differ; when responses align, richness only dilutes variance, not reverse its sign.
- **Robustness**: Patterns persist across σ_env to 1.5, ρ to 1.0, and φ to 0.95; insurance conclusions are not artefacts of a particular temporal structure.
- **Limitations/future work**: Equicorrelated drivers and static competition; no demographic stochasticity; deterministic slope sets. Future: alternative covariance structures, stochastic competition, demographic noise, broader trait distributions.

## Figures
- Main panels: `analysis/reports/manuscript_panels.pdf` (heatmaps mixed/positive, CV lines, imposed vs realised synchrony, φ sensitivity).
- Supplementary overlays: `cv_richness_scaling_mixed.png`, `cv_phi_sensitivity_sigma0.5_extended.png`.

## Reproducibility
- Environment: `pyproject.toml` managed with uv; run tests `uv run pytest`.
- Entry points: `analysis/run_full_grid.py`, `analysis/plot_grid.py`; data under `data/sim/grid/`.
