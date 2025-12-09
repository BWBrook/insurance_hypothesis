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
- **Decision**: Manipulate synchrony via equicorrelated environmental innovations (parameter ρ); quantify realised synchrony using pairwise growth-rate correlations and the Loreau–de Mazancourt community synchrony index in analyses.
- **Rationale**: Directly links the experimental control parameter (ρ) to both imposed and realised synchrony, with established ecological index for interpretation.
- **Status**: active

### DEC-004 – Persistence range and stability safeguards

- **Date**: 2025-12-09
- **Decision**: Environmental persistence φ explored over [0, 0.95]; covariance clipped to keep ρ < 1 for PD; φ_LdM clipped to [0,1] to avoid numerical overshoot.
- **Rationale**: Ensures numerical stability while probing high persistence; prevents artefactual synchrony values outside theoretical bounds.
- **Status**: active

_(The agent should add more entries as needed.)_

---

# Example template (dispose, use, modify as you see fit):

| Date (UTC) | Decision            | Rationale / evidence | Status | Links                  |
| ---------- | ------------------- | -------------------- | ------ | ---------------------- |
| _[fill]_   | _[what was chosen]_ | _[why]_              | active | _[log entry / commit]_ |

Add new rows as decisions are made; do not delete old ones. Mark superseded items in **Status** (e.g., superseded, reverted) rather than removing them.
