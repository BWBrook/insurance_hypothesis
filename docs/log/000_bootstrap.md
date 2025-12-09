# Log 000 – Bootstrap and scoping

## 1. Timestamp and environment

- **Created**: 2025-12-09 01:04 UTC
- **Agent**: Codex CLI (GPT-5.1-codex-max)
- **Languages available**: Python 3.12, Julia 1.12.2, R 4.5.2

## 2. Initial understanding of the project

- Goal: test the insurance hypothesis via simulations—whether environmental variability stabilises total community biomass when species responses are asynchronous, and destabilises it when responses are synchronous.
- Stabilisation ≡ reduced temporal variance/CV of total biomass compared to a low-variance baseline.
- Asynchrony operationalised as low/negative correlations among species’ environmentally driven growth rates (tunable via correlated environmental anomalies), summarised by synchrony indices.
- Simulations are appropriate because the study is theoretical, with no empirical data, and we need controlled manipulation of variance and synchrony.

## 3. Proposed model framework

- Discrete-time stochastic Ricker with density dependence and competition. Per-capita growth rate modulated by species-specific slopes `b_i` times an environmental anomaly `z_i(t)`.
- Environmental driver: multivariate AR(1) with adjustable variance `σ_env` and inter-species correlation `ρ` to control synchrony; covariance matrix `Σ = σ_env^2[(1-ρ)I + ρ11^T]`.
- Species differences: `b_i` arrayed along a gradient (negative to positive) so species respond differently to the same environmental distribution; carrying capacities near 100; interspecific competition scaled by `α_inter = c_comp * α_intra`.

## 4. Proposed experimental grid

- σ_env ∈ {0, 0.2, 0.5, 1.0, 1.5}; ρ ∈ {-0.5, 0, 0.5, 0.9, 1.0}; species richness S ∈ {2, 4, 8}.
- AR(1) persistence φ default 0.4, with sensitivity runs at 0 and 0.7.
- 600 time steps with 300 burn-in; 200 replicates per scenario (adjustable if runtime heavy).
- Outputs: per-scenario summary stats and seeds saved under `data/sim/`.

## 5. Planned validation strategy

- Deterministic baseline (σ_env = 0) should converge near equilibrium K_i with no extinctions.
- Perfect synchrony (ρ = 1) should yield community CV ≈ species CV (minimal insurance effect).
- Negative/low synchrony should reduce community variance relative to species-level variance, with stronger effect at higher richness.
- Numerical checks: non-negativity, no NaN/Inf, stable trajectories under default params; convergence of summary stats as replicates increase.
- Cross-check a two-species toy case against an independent vectorised calculation at σ_env = 0.

## 6. Immediate next actions

1. Stand up Python/uv environment and record language decision in `docs/decisions.md`.
2. Implement correlated AR(1) generator and Ricker simulation in `src/python/insurance_sim/model.py`.
3. Add pytest sanity tests (`tests/test_sim_basic.py`) for σ_env = 0 equilibrium, non-negativity, and array shapes.
4. Build a tiny runner `analysis/run_small_grid.py` to exercise one subset of the grid and write preview outputs.
5. Start `docs/log/010_model_design.md` once model code exists; prepare first interpretation note after preview run.

---

### 2025-12-09 (UTC) – Actions taken

- Created Python packaging scaffold (`pyproject.toml`) with core deps: numpy, pandas, scipy, pyarrow; dev dep: pytest.
- Implemented core simulation utilities in `src/python/insurance_sim/model.py`: equicorrelated AR(1) environment, stochastic Ricker with competition, per-replicate summaries, and helper config dataclass.
- Added initial pytest sanity checks in `tests/python/test_sim_basic.py` (covariance PD, deterministic equilibrium under σ_env=0, non-negativity, replicate shapes).
- Added preview runner `analysis/run_small_grid.py` to execute a minimal grid (S=2; σ_env ∈ {0,0.5}; ρ ∈ {0,0.5}) and write parquet summaries under `data/sim/preview/`.
