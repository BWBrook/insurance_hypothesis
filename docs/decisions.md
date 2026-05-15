# Decisions

> The AI agent must record here any non-trivial, irreversible decision it makes.

For each entry, include:

- an identifier,
- date,
- decision,
- rationale,
- status (active / superseded).

---

## Decision log

### DEC-001 – Language choice

- **Date**: 2025-12-09
- **Decision**: Python 3.12 for core simulations.  
- **Rationale**: Python offers sufficient performance for the planned grid, strong ecosystem for testing/plotting (numpy/pandas/pytest), and uv makes reproducible environments straightforward; Julia not needed for anticipated scales.
- **Status**: active

### DEC-002 – Core model form

- **Date**: 2025-12-09
- **Decision**: Discrete-time stochastic Ricker model with intra/interspecific competition; per-capita growth modulated by species-specific slopes on a correlated multivariate AR(1) environmental driver.
- **Rationale**: Captures density dependence and competitive interactions while remaining simple and fast for large scenario grids; AR(1) allows tunable environmental variance and persistence aligned with hypothesis needs.
- **Status**: active

### DEC-003 – Synchrony metric

- **Date**: 2025-12-09
- **Decision**: Manipulate **imposed environmental correlation** via equicorrelated environmental innovations (parameter ρ_env); quantify **realised synchrony** using pairwise growth-rate correlations and the Loreau–de Mazancourt community synchrony index in analyses.
- **Rationale**: Separates the driver parameter (ρ_env) from emergent synchrony and uses established ecological indices for realised synchrony and its link to variance.
- **Status**: active

### DEC-004 – Persistence range and stability safeguards

- **Date**: 2025-12-09
- **Decision**: Environmental persistence φ explored over [0, 0.95]; σ_env interpreted as **innovation** standard deviation in the AR(1) process so that stationary variance is σ_env²/(1−φ²); covariance clipped to keep ρ_env < 1 for PD; φ_LdM clipped to [0,1] to avoid numerical overshoot.
- **Rationale**: Ensures numerical stability while probing high persistence; makes explicit that φ sweeps change both temporal autocorrelation and effective environmental variance, and prevents artefactual synchrony values outside theoretical bounds.
- **Status**: active

### DEC-005 – Requested vs effective correlation logging

- **Date**: 2025-12-12
- **Decision**: Keep the requested grid value as `rho_env` and always store the actual value used by the simulator as `rho_eff`, plus a `rho_clipped` flag when clipping occurs.
- **Rationale**: Equicorrelation has feasibility bounds that tighten with richness; explicit `rho_eff` avoids mislabeling infeasible negative-correlation scenarios and keeps cross-richness comparisons auditable.
- **Status**: active

### DEC-006 – Fixed φ-sensitivity run length convention

- **Date**: 2025-12-12
- **Decision**: Use 400 steps with 200 burn-in for φ-sensitivity grids, passed explicitly in runner commands; keep 600/300 for the main and positive full grids.
- **Rationale**: Resolves a documentation-vs-command mismatch and standardises reduced-grid persistence sweeps without changing the main-inference grid convention.
- **Status**: active

### DEC-007 – Sign-structure control with magnitude matching

- **Date**: 2025-12-12
- **Decision**: Add a `positive_matched` control slope mode where aligned slopes are matched to the absolute-value magnitude distribution of mixed slopes.
- **Rationale**: Separates the effect of slope sign structure from slope magnitude, directly addressing the “aligned responses also have larger |b_i|” confound.
- **Status**: active

### DEC-008 – Interpretation boundary for high-persistence stress runs

- **Date**: 2026-02-11
- **Decision**: Treat φ=0.9/0.95 reduced-grid results as stress tests when floor occupancy is elevated (especially low S and high σ_env), and avoid describing these scenarios as uniformly low-extinction.
- **Rationale**: Post-hiatus audit showed non-negligible floor occupancy in subsets of high-φ scenarios (`phi09_reduced` and `phi095_reduced`) despite low extinction rates in main inference grids; documentation must distinguish these regimes.
- **Status**: active

### DEC-009 – Keep CLI scripts thin and reusable analysis logic importable

- **Date**: 2026-03-07
- **Decision**: Move reusable reporting and figure-generation logic into importable Python modules under `src/python/insurance_sim/`, leaving `analysis/*.py` as thin CLI/orchestration entry points.
- **Rationale**: Reduces duplication (`rho_eff` handling, slope-mode definitions, reporting helpers), makes behavior easier to test under `pytest`, and keeps future refactors reviewable without changing the public CLI or scientific outputs.
- **Status**: active

### DEC-010 – Production-grid compute target and replicate convention

- **Date**: 2026-05-14
- **Decision**: Use `deep-server` as the default execution host for production-scale single-host simulation grids, and use 1000 replicates per scenario/slice for final-paper production grids unless a run is explicitly labelled as a smoke test, pilot, or stress-test subset.
- **Rationale**: The Nectar control-plane repo identifies `deep-server` as the best fit for durable CPU-heavy single-host jobs, with 64 logical CPUs, 125 GiB RAM, and large `/data` storage. A fixed 1000-replicate convention is easy to justify in the paper and reduces reviewer concern about Monte Carlo sampling uncertainty, even where diminishing returns would likely begin earlier.
- **Status**: active

### DEC-011 – Production-only shard seeding

- **Date**: 2026-05-14
- **Decision**: For production manifests, derive each replicate seed deterministically from `(base_seed, scenario_index, replicate)` using NumPy `SeedSequence`; keep the existing exploratory `analysis/run_full_grid.py` seeding behaviour unchanged.
- **Rationale**: Production runs must be shardable and resumable across many independent worker processes on `deep-server`. Per-replicate deterministic seeds let shards run in any order or be re-run independently without changing already-completed replicate identities, while preserving the older exploratory runner as a compatibility surface.
- **Status**: active

### DEC-012 – First-batch production shard size and concurrency

- **Date**: 2026-05-14
- **Decision**: Use 100 replicates per shard and launch the first production batch with `run-pending --jobs 48` on `deep-server`.
- **Rationale**: Remote benchmarks with S=4, 600/300-step, 1000-replicate-per-scenario workloads validated cleanly. A 48-worker benchmark processed 10000 replicate summaries across 10 scenarios in 6.85 seconds of `run-pending` wall time with low memory use. Forty-eight workers use most of the 64 logical CPUs while leaving conservative headroom for OS, SSH/tmux, and filesystem activity; `--jobs 56` remains a later option if the first full grid shows no contention.
- **Status**: active

### DEC-013 – First high-resolution Figure 1 production grid

- **Date**: 2026-05-14
- **Decision**: Use `analysis/production_specs/fig1_s4_highres_v1.json` as the first production batch: S=4, `phi=0.4`, mixed and positive slope modes, 19 `sigma_env` values from 0.0 to 2.0, 15 `rho_env` values from -0.3 to 1.0, and 1000 replicates per scenario.
- **Rationale**: This grid directly addresses the ecologist-facing concern that the interim Figure 1 surfaces were blocky and that visual change was compressed at high `sigma_env`. It densifies the displayed gradients without expanding to other richness levels or controls before the main S=4 story is rechecked.
- **Status**: active

### DEC-014 – Label high-sigma Figure 1 work as a stress extension

- **Date**: 2026-05-15
- **Decision**: Add `analysis/production_specs/fig1_s4_highsigma_v1.json` as a separate S=4 production extension from `sigma_env=2.25` to `4.0`, rather than expanding the core Figure 1 grid in place.
- **Rationale**: The first production surface indicates that the mixed-slope response is still buffered at `sigma_env=2.0`, while positive slopes are already entering a high-CV/high-floor edge. Extending to `sigma_env=3-4` is ecologically plausible for high-variability taxa such as many invertebrates, but should be explicitly treated as a high-variability stress regime until floor occupancy and nonlinear dynamics are inspected.
- **Status**: active

_(The agent should add more entries as needed.)_

---

# Example template (dispose, use, modify as you see fit):

| Date (UTC) | Decision            | Rationale / evidence | Status | Links                  |
| ---------- | ------------------- | -------------------- | ------ | ---------------------- |
| _[fill]_   | _[what was chosen]_ | _[why]_              | active | _[log entry / commit]_ |

Add new rows as decisions are made; do not delete old ones. Mark superseded items in **Status** (e.g., superseded, reverted) rather than removing them.
