# Active scientific and release decisions

This file records consequential choices that still govern the paper. Historical
implementation detail is recoverable through Git history.

## Scientific design

### Competitive stochastic Ricker model

- **Decision:** Use a discrete-time Ricker model with shared `r0 = 1`, `K = 100`,
  intraspecific competition `1`, and interspecific competition `0.3`.
- **Reason:** It is the smallest density-regulated community model that exposes
  environmental response covariance while retaining interpretable dynamics.
- **Status:** active baseline. Growth-rate sensitivity and the October mechanism
  grids (`alpha_inter = 0.1, 0.3, 0.6`) extend it without changing the recurrence.

### AR(1) forcing and correlation

- **Decision:** `sigma_env` is the innovation SD of a multivariate AR(1) process;
  `phi` controls persistence, so stationary SD is
  `sigma_env / sqrt(1 - phi^2)`. Innovations use an equicorrelation request
  `rho_env`; infeasible requests at either boundary are clipped to a positive-definite
  value recorded as `rho_eff`.
- **Reason:** This separates the implemented inputs from realised growth
  synchrony and makes feasibility transparent.
- **Status:** active. Figure S8 is a fixed-innovation compound persistence–variance
  sensitivity, not an isolated autocorrelation effect.

### Response regimes

- **Decision:** Compare `mixed` slopes in `[-0.5, 0.5]`, `positive` slopes in
  `[0.1, 1]`, and `positive_matched = abs(mixed)`.
- **Reason:** Positive-matched isolates response sign structure from slope
  magnitude; the steep-positive comparison is a supplementary stress contrast.
- **Status:** active. The positive-matched control is the primary sign-structure
  comparison in the revised evidential hierarchy.

### Outcomes and mechanism

- **Decision:** Use temporal CV of total abundance as the main response. Treat
  Loreau-de Mazancourt synchrony, realised per-capita growth correlations, and
  the exact abundance variance decomposition as mechanistic diagnostics.
- **Reason:** These quantities distinguish aggregate stability from species-level
  variability and imposed environmental correlation.
- **Status:** active. The first-order covariance criterion and local second-order
  departure are distinguished from the full nonlinear simulation result.

### Shared-exposure reversal and local prediction, October 2026

- **Decision:** Make the conditional destabilising effect of shared exposure the
  central result. Retain the mixed-versus-aligned sign control as a separate
  estimand. Predict only the small-fluctuation onset with the derived coefficient.
- **Evidence:** All 23 eligible prospective settings meet both recorded criteria;
  all five identified reversals survive familywise adjustment and the specified
  longer-window check. Four longer-run settings remain floor-free, and one has
  rare retained floor contact. The separate guard runs find no activation.
- **Limits:** Neither negative covariance nor balanced slopes guarantees that
  increasing exposure correlation adds stability. The coefficient does not
  quantitatively explain the finite-noise reversal. Composition crossings are
  interpolated summaries, not precisely estimated thresholds. Compound richness,
  competition and persistence changes do not isolate a single causal driver.
- **Display decision:** Keep Figure 1; add amplitude/boundary Figure 2 and
  prediction/reversal Figure 3. Move former Figures 2–5 to S5–S8 and add S9 for
  the complete boundary paths. Keep every original generated filename and value.
- **Status:** integrated after independent derivation and raw-summary audits;
  correspondence discussion 89 preserves the prespecifications and disagreements.

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
  All fixed model constants are explicit. Main production grids use 1000
  replicates per scenario and longer-window checks use 500. Deterministic seeds
  derive from the base seed, scenario index and replicate index.
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
- **September display decision (superseded by the October hierarchy above):** Promote the accepted matched-sign/weighted-boundary
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

### Final author-read synthesis and scientific release boundary

- **Decision:** The PI approved Astra's check of Fable's editorial pass on
  2026-09-11. Keep the readability gains and balanced-endpoint emphasis while
  retaining the direction-reversal counterexample, qualifying nonlinear
  attribution, and matching all Methods descriptions to the implemented code.
- **Evidence:** The local second-order derivation passes an independent
  methodological check; existing production summaries establish the measured
  departures. No new numerical approximation is adopted as manuscript evidence.
- **Release boundary:** The working repository is the research record. Review
  and eventual public artifacts are generated from the minimal code/data path,
  with complete recipes, integrity references, and no workbook Git history.
  The public release will have its own versioned repository and Zenodo archive.
  The PI's full read and any subsequent corrections precede that release.
- **Diagnostic provenance:** Report the retained 30-replicate-per-scenario
  numerical-guard diagnostic rather than the historical 200-replicate sigma=4
  claim whose recipe is absent from the active package. Preserve all saved
  production and diagnostic evidence.

### Preprint and anonymous-review workflow

- **Decision:** The PI prefers a preprint before journal submission and approved
  retaining anonymous manuscript and code/data review files for Oikos. A public
  preprint URL will be disclosed separately to the editor when available.
- **Basis:** Oikos uses double-anonymous review and its publishing policy permits
  preprints before or during review. This arrangement preserves anonymous review
  files while accepting that author identity is discoverable from the preprint.
- **Boundary:** No preprint, public repository, or Zenodo deposit has been made
  in this tranche. The PI's full read and final metadata still precede release.

### Approved external-review display corrections, 19 September 2026

- **Decision:** Apply the four bounded corrections from the independent Astra
  review: undefined-synchrony masking, readable principal figures, precise
  novelty positioning and removal of the SI divider page.
- **Scientific boundary:** Zero-forcing Figure S2 synchrony is undefined for
  constant trajectories. Correct the display summary and mask those cells,
  preserving saved replicate rows. Other numerical summaries, all production
  specifications, seeds and model dynamics remain fixed. Changes to Figure 1
  and Figure 2 concern physical layout and type size only.
- **Verification boundary:** Compare regenerated summaries against the prior
  release; permit only the Figure S2 zero-forcing mean/SD missing-value change.
  Recheck affected figures at their submitted size and rebuild the anonymous
  package with updated expected-output hashes.
- **Deferred:** The review's longer-window calculations remain review evidence.
  No new production run, manuscript sensitivity result, seed migration or
  validator extension is part of this correction.
- **Build dependency:** Remove the SI divider in makedoc only for documents
  containing supplementary figures without main figures. Preserve the existing
  divider for combined documents and keep caption-page layout. This required a
  separately tested local patch to `/home/bwbrook/work/makedoc` at base `b613e71`;
  both repositories remain uncommitted pending the PI's read.
