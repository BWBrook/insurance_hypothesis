# Title (placeholder)
Insurance effects in simulated communities: when biodiversity buffers environmental variance, and when it does not

## Introduction
Environmental variability typically destabilises populations, increasing their temporal variance. However, theory predicts an **insurance effect** of biodiversity: if species respond asynchronously to the same environmental fluctuations, their individual deviations can cancel, stabilising aggregate biomass **relative to what would be expected from a single species or a fully synchronous community**. Here we probe this mechanism in fully simulated communities, contrasting heterogeneous response slopes (mixed signs) with aligned slopes (all positive).

We define insurance operationally as **reduced community variability and synchrony relative to appropriate baselines**. Quantitatively, we track (i) the coefficient of variation of total biomass (CV_total), (ii) an approximate mean species CV estimated from simulated species-level means and variances, and (iii) response synchrony indices: the Loreau–de Mazancourt synchrony φ_LdM and mean pairwise growth-rate correlations. Insurance is present when CV_total is lower than for a single species or aligned-response community under the same environmental variance and driver correlation, and when synchrony metrics indicate reduced or negative co-fluctuations.

We manipulate environmental variance (σ_env), **imposed environmental correlation among species’ drivers (ρ_env)**, species richness (S), and temporal autocorrelation (φ) to map where biodiversity provides buffering and where it does not.

## Methods
- **Community dynamics**: discrete-time stochastic Ricker with intra/inter-specific competition, per-capita growth `r0 + b_i z_i(t) - (N_i + Σ_j α_ij N_j)/K_i`; abundance floored at 1e-9.
- **Environment**: multivariate AR(1) with equicorrelated innovations; **σ_env is the innovation standard deviation**, so the stationary variance of the environmental process is σ_env² / (1−φ²). The parameter ρ_env controls the imposed environmental correlation between species’ drivers. Covariance is clipped to remain PD; σ_env=0 gives deterministic baseline.
- **Responses**: mixed slopes (linear -0.5..0.5) versus positive slopes (0.1..1.0). Fixed parameters: r0=1, K=100, α_intra=1, α_inter=0.3.
- **Design**:
  - Mixed grid: σ_env {0,0.2,0.5,1.0,1.5} × ρ {-0.5,0,0.5,0.9,1.0} × S {2,4,8}, φ=0.4, 600 steps (300 burn), 150 reps.
  - Positive grid: same σ_env–ρ with S {4,8} (+ small S=2 subset at σ=0.5,1.0), 100 reps.
  - φ sweeps (mixed): φ ∈ {0,0.4,0.7,0.9,0.95} on σ_env {0,0.5,1.0} × ρ {-0.5,0,0.5,0.9,1.0}, S {2,4}, 80 reps.
- **Metrics**: CV of total biomass (CV_total); an approximate mean species CV computed from simulated species-level means and variances; Loreau–de Mazancourt synchrony φ_LdM (clipped [0,1]); mean pairwise growth correlation; extinction frequency. Plots via matplotlib; outputs parquet.
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
In the mixed-slope regime, community variability is strongly buffered relative to single-species behaviour and to aligned responses. Across the σ_env–ρ_env–S grid, community CV (CV_total) falls with increasing richness and, for most σ_env, declines as ρ_env increases (Figure 1A–C). At σ_env=0.5 and ρ_env=0.5, CV_total is ≈0.15 for S=2, ≈0.08 for S=4, and ≈0.06 for S=8, illustrating a pronounced richness effect. By contrast, in the positive-slope regime, CV_total and φ_LdM both increase with ρ_env (Figure 1B–C), and richness, while reducing the magnitude of CV_total, cannot reverse this trend: at σ_env=0.5 and ρ_env=0.5, S=4 has CV_total ≈0.26, substantially higher than the mixed-slope case.

The simulations reveal a clear separation between imposed environmental correlation and realised response synchrony. Under mixed slopes, realised mean growth correlations are systematically lower than ρ_env, and often become negative at high ρ_env (Figures 1D, 2A); the average difference (realised − ρ_env) is negative across scenarios. Under positive slopes, realised correlations are higher than ρ_env (Figures 1D, 2B), with positive deltas (Figure 2C). This demonstrates that ρ_env is a driver parameter, while actual synchrony is emergent and strongly controlled by response directions.

These synchrony differences translate directly into differences in community variability. For the mixed-slope grid, CV_total decreases as φ_LdM decreases and as mean pairwise growth correlations become less positive or negative (Figure 3). Aggregated across scenarios, lower φ_LdM and lower realised correlations are associated with lower CV_total, especially at higher richness (S=4,8). In positive-slope grids, CV_total remains high at comparable φ_LdM values, consistent with the idea that aligned responses transmit environmental variance more directly into community variance.

Environmental persistence φ amplifies variability but does not overturn the insurance patterns. When φ is increased from 0 to 0.95 at fixed innovation SD σ_env, the stationary variance of the environmental process increases, and CV_total rises (Figure 5). At σ_env=0.5 and ρ_env=0.5, CV_total for S=2 increases from ≈0.14 (φ=0) to ≈0.58 (φ=0.95), and for S=4 from ≈0.07 to ≈0.35. Nonetheless, mixed-slope communities with higher richness retain substantially lower CV_total than positive-slope communities under the same σ_env, ρ_env, and φ. Extinction frequencies remain negligible across all scenarios (maximum mean extinction frequency ~0.003), indicating that patterns are not driven by numerical collapse.

Control runs confirm that these patterns are not artefacts of a specific competition strength or slope magnitude. Setting α_inter=0 (no interspecific competition) on a reduced grid yields qualitatively identical contrasts: mixed slopes still show CV_total decreasing with richness and ρ_env, whereas positive slopes retain an increasing CV_total–ρ_env relationship, only rescaled in magnitude. Narrowing mixed slopes to −0.25…0.25 lowers overall CV_total but preserves both the richness effect and the mixed-vs-positive contrast, demonstrating that insurance does not rely on extreme response heterogeneity.

## Discussion
The simulations support a mechanistic picture in which response-direction heterogeneity turns shared environmental variation into compensatory growth. When species have mixed environmental slopes, imposed driver correlation (ρ_env) does not translate into synchronous responses: realised growth correlations drop below ρ_env and can even become negative, leading to reduced φ_LdM and lower CV_total. In contrast, when slopes are all positive, imposed driver correlation is reinforced by aligned responses, generating high φ_LdM and high CV_total.

Species richness strengthens this insurance effect. Adding species amplifies the potential for compensatory dynamics when responses differ, driving CV_total down as S increases in mixed-slope communities. When responses align, richness still decreases CV_total via averaging, but cannot reverse the positive relationship between ρ_env and CV_total. In that sense, richness provides insurance only when coupled with response heterogeneity.

Robustness checks indicate that these conclusions are not artefacts of particular parameter choices. Insurance patterns persist across σ_env up to 1.5, ρ_env up to 1.0, and φ up to 0.95, and they survive removal of interspecific competition (α_inter=0) and a narrowing of mixed-slope magnitudes. These controls suggest that the qualitative results are driven primarily by the combination of shared drivers and heterogeneous response directions, rather than by specific interaction strengths or extreme trait values.

Several limitations remain. The environmental drivers are equicorrelated; alternative covariance structures (e.g. block correlations or empirical patterns) could reveal additional regimes. Competition is symmetric and static, and demographic stochasticity is absent. Slopes are constructed deterministically along a single environmental axis rather than sampled from a richer trait distribution. Future work could relax these assumptions, explore more realistic environmental covariance, and examine how demographic noise interacts with response heterogeneity to shape insurance.

## Figures
- Main panels: `analysis/reports/manuscript_panels.pdf` (heatmaps mixed/positive, CV lines, imposed vs realised synchrony, φ sensitivity).
- Supplementary overlays: `cv_richness_scaling_mixed.png`, `cv_phi_sensitivity_sigma0.5_extended.png`.

## Reproducibility
- Environment: `pyproject.toml` managed with uv; run tests `uv run pytest`.
- Entry points: `analysis/run_full_grid.py`, `analysis/plot_grid.py`, and `analysis/run_all.py`; data under `data/sim/grid/`.
