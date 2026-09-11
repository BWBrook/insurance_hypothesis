# Active scientific and release decisions

This file records consequential choices that still govern the paper. Historical
implementation detail is recoverable through Git history.

## Scientific design

### Competitive stochastic Ricker model

- **Decision:** Use a discrete-time Ricker model with shared `r0 = 1`, `K = 100`,
  intraspecific competition `1`, and interspecific competition `0.3`.
- **Reason:** It is the smallest density-regulated community model that exposes
  environmental response covariance while retaining interpretable dynamics.
- **Status:** active; sensitivity at other `r0` values is part of the bounded
  final revision, not a replacement of the core design.

### AR(1) forcing and correlation

- **Decision:** `sigma_env` is the innovation SD of a multivariate AR(1) process;
  `phi` controls persistence, so stationary SD is
  `sigma_env / sqrt(1 - phi^2)`. Innovations use an equicorrelation request
  `rho_env`; infeasible negative requests are clipped to a positive-definite
  value recorded as `rho_eff`.
- **Reason:** This separates the implemented inputs from realised growth
  synchrony and makes feasibility transparent.
- **Status:** active. Figure 5 is a fixed-innovation compound persistence–variance
  sensitivity, not an isolated autocorrelation effect.

### Response regimes

- **Decision:** Compare `mixed` slopes in `[-0.5, 0.5]`, `positive` slopes in
  `[0.1, 1]`, and `positive_matched = abs(mixed)`.
- **Reason:** Mixed versus positive tests the headline contrast; positive-matched
  isolates response sign structure from slope magnitude.
- **Status:** active. The positive-matched control is the primary sign-structure
  comparison in the revised evidential hierarchy.

### Outcomes and mechanism

- **Decision:** Use temporal CV of total abundance as the main response. Treat
  Loreau-de Mazancourt synchrony, realised per-capita growth correlations, and
  the exact abundance variance decomposition as mechanistic diagnostics.
- **Reason:** These quantities distinguish aggregate stability from species-level
  variability and imposed environmental correlation.
- **Status:** active. The manuscript states the analytical mechanism as an
  abundance-weighted covariance criterion and limits it to its first-order scope.

### Bounded weighted-balance sensitivity

- **Decision:** Add one `S = 4` endpoint-correlation grid that combines a
  fixed-norm response-alignment path, a constant-total-equilibrium carrying-
  capacity path, and the clean matched-sign endpoints at
  `r0 = 0.25, 0.5, 1.0, 1.5`.
- **Reason:** This is the smallest design that tests the external review's three
  consequential boundary conditions: continuous response balance, unequal
  abundance weights, and the dynamically special `r0 = 1` setting.
- **Status:** completed with 1000 replicates per scenario. Both controlled paths
  crossed the nonlinear ratio of one near the first-order boundary, and the
  matched-sign reversal persisted at every tested `r0`. The analytical
  benchmark uses `a_i = N_i* b_i` and the alignment index
  `A = (sum a_i)^2 / (S sum a_i^2)`.

### Richness and persistence claims

- **Decision:** Describe richness as an ordered assembly sequence in which slope
  composition and other quantities covary with `S`; describe `phi` sensitivity at
  fixed innovation variance.
- **Reason:** The production grids do not independently randomize response
  balance across richness or hold stationary environmental variance fixed.
- **Status:** active; claims must remain calibrated to these compound designs.

### Stress regions

- **Decision:** Retain high-`sigma_env` and high-`phi` runs as labelled stress
  extensions and report floor occupancy explicitly.
- **Reason:** They reveal where the qualitative contrast persists while the model
  enters boom–bust/floor-influenced dynamics; they should not be presented as the
  same low-extinction regime as the core inference.
- **Status:** active.

## Reproducibility architecture

### Production specifications and seeds

- **Decision:** Versioned JSON specs are the only production-creation interface.
  All fixed model constants are explicit. Production uses 1000 replicates per
  scenario and deterministic seeds derived from the base seed, scenario index,
  and replicate index.
- **Reason:** A spec is a compact auditable design record; deterministic
  per-replicate seeds make sharding and reruns order-independent.
- **Status:** active.

### Single active analysis path

- **Decision:** `analysis/production_grid.py` is the full-run entry point and
  `analysis/run_all.py` is the only figure/table regeneration entry point. The
  current production summaries are mandatory inputs; canonical outputs live only in
  `analysis/reports/`.
- **Reason:** The previous collection of wrappers, fallbacks, exploratory caches,
  and copied figure trees obscured provenance without adding current capability.
- **Status:** active from the 2026-08-10 structural cleanup.

### Proportional test boundary

- **Decision:** Test distinct scientific contracts, deterministic production
  bookkeeping, numerical summary functions, failure on missing inputs, and one
  complete display workflow. Do not separately test every plotting wrapper or
  obsolete interface.
- **Reason:** This protects inferential validity while keeping a private
  scientific repository fast to change and easy to understand.
- **Status:** active.

### Reproducible display metadata

- **Decision:** `analysis/run_all.py` sets a stable default
  `SOURCE_DATE_EPOCH` before importing the plotting stack, while allowing an
  explicit caller override.
- **Reason:** Canonical PDF content was reproducible, but Matplotlib's embedded
  creation timestamp changed the file hash on every release run.
- **Status:** active. Consecutive full regenerations now produce identical PDF
  hashes, and raster comparison confirmed no rendered change.

## Manuscript and submission

### Evidence and display hierarchy

- **Decision:** Production-backed results are the paper's evidence base. Replace
  the descriptive CV-synchrony association in Figure 1 with the matched-sign,
  weighted-balance, and `r0` boundary test. Retain the fuller three-regime
  positive-matched diagnostic in the Supporting information.
- **Reason:** Display changes should follow scientific decisions, not code
  tidying.
- **Status:** approved by the PI at the Stage 3 boundary; the revised display and
  calibrated claims are current.

### Bounded conceptual and editorial revision

- **Decision:** On 2026-09-11 the PI approved the fresh review's bounded revision.
  State the abundance-weighted criterion as exact for forcing variance and for
  correlation ratios in the stable linearised equal-`K` model, while describing
  nonlinear abundance-CV transitions as approximate. Report the resolved
  departure at `A=0.247` and acknowledge that unequal `K` changes feedback as well
  as equilibrium weights. Remove the unsupported mean-shift explanation.
- **Reason:** These qualifications match the existing evidence and prior
  covariance/population-feedback theory without changing the model or results.
- **Display decision:** Promote the accepted matched-sign/weighted-boundary
  display to Figure 1; realised synchrony is Figure 2, environmental variance
  Figure 3, richness Figure 4, and persistence Figure 5. Retain rendered panels,
  production IDs, and generated filenames. Paper and package mappings identify
  their manuscript roles explicitly.
- **Status:** implemented and independently reviewed; manuscript builds, identity
  checks, protected-output comparisons, and clean-package verification passed
  on 2026-09-11.

### Oikos build composition

- **Decision:** Keep anonymous main manuscript, anonymous Supporting Information,
  submission-form statements, unblinded title page, and cover letter as separate
  `makedoc` profiles. Use the compliant A4 anonymous PDF as the initial main-text
  upload; keep DOCX as an editable fallback. Write every profile to the
  repo-local `build/oikos_submission_aug_2026/` directory rather than
  `makedoc/dist/`.
- **Reason:** This matches double-blind review needs and avoids accidental identity
  disclosure or unsuitable DOCX pagination, while keeping manuscript sources and
  their generated submission components together.
- **Status:** active.

### Anonymous reproducibility package

- **Decision:** Build an allowlisted code/data package containing the active
  simulator, production runner, figure workflow, tests, all current compact summaries,
  specs, and locked environment. Exclude manuscript/internal history and
  repository-only submission tests.
- **Reason:** Reviewers need complete reproducibility evidence without author
  identity or internal project context.
- **Status:** active. The 2026-09-11 package contains all seven production specs
  and summaries and passes its reviewer-facing test, type, and display workflow
  from inside the package.

### Final-review response boundary

- **Decision:** Address the external review with a bounded response-balance,
  abundance-weight, and `r0` tranche plus calibrated prose. Defer broader model
  extensions unless this focused test changes the decision.
- **Reason:** The review found no fatal defect; expanding every defensible
  sensitivity would diffuse a tight paper without proportionate inferential gain.
- **Status:** active.
