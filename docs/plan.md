# Oikos final-revision plan

## Scientific objective

Test when environmental variability is buffered at the community level because
species respond asynchronously. The implemented stochastic Ricker model compares
mixed response directions with aligned responses under correlated AR(1)
environmental forcing.

The submission claim is relative and conditional: mixed response directions can
reduce temporal variability of total community abundance relative to aligned
responses under the examined design. Richness, persistence, and synchrony
patterns are supporting structure, not independent causal effects isolated by a
factorial experiment.

## Locked evidence base

Six validated production grids contain 1,156,000 replicate summaries in total:

| Grid | Rows | Primary use |
| --- | ---: | --- |
| `fig1_s4_highres_v1` | 570,000 | Core mixed-versus-aligned response surface |
| `fig1_s4_highsigma_v1` | 180,000 | Labelled high-variance stress extension |
| `fig2_richness_mixed_v1` | 210,000 | Richness display, current Figure 4, S1/S2, variance decomposition |
| `fig3_synchrony_v1` | 66,000 | Imposed-versus-realised synchrony and species-CV diagnostic |
| `fig5_persistence_mixed_v1` | 64,000 | Fixed-innovation persistence sensitivity |
| `figs3_positive_matched_control_v1` | 66,000 | Magnitude-matched response-sign control |

The present numerical summaries and display items are protected during structural
cleanup. New simulations in the scientific revision will be written to a new,
versioned spec and output directory.

## External-review response boundary

The 2026-08-09 external review found no fatal scientific or computational defect.
Its highest-value recommendations are accepted:

1. promote the magnitude-matched positive control in the evidential hierarchy;
2. express the first-order mechanism as an abundance-weighted covariance
   criterion, with its assumptions explicit;
3. clarify that environmental exposures share a common orientation;
4. test the special `r0 = 1`/equal-abundance boundary with a compact sensitivity;
5. replace the descriptive current Figure 4 with a more diagnostic display; and
6. narrow richness and fixed-innovation persistence claims to the implemented
   compound designs.

The revision will not automatically expand to fixed-stationary-variance AR(1)
experiments, alternative covariance structures, alternative density dependence,
or broad richness factorials. Those are deferred unless the bounded revision
fails to support an honest focused claim.

## Four-stage action plan

- [x] **Stage 1 — checkpoint the reviewed state.** Create a signed recovery
  commit; validate all six datasets; record hashes for the production summaries,
  locked displays, and external report; run the baseline test/type gate.
- [x] **Stage 2 — remove structural legacy without changing science.** Consolidate
  the runner and simulation recurrence; use specs as the only production-creation
  interface; remove superseded scripts, duplicate figure copies, historical
  ledgers, obsolete drafts, and redundant tests; verify numerical and rendered
  equivalence; commit; pause for PI review.
- [ ] **Stage 3 — bounded scientific revision.** Prespecify and run the smallest
  response-balance/abundance-weight/`r0` sensitivity that tests the reviewer's
  central boundary conditions. Promote the existing magnitude-matched control,
  replace Figure 4, and revise the manuscript's mechanism and claim hierarchy.
  Verify claim-specific invariants and pause for PI review.
- [ ] **Stage 4 — release and submission gate.** Run the full code/data/display
  checks, sequential manuscript profiles, identity sanitization, visual review,
  anonymous package rebuild, and submission checklist. Resolve only the remaining
  PI-supplied submission facts, then prepare the final handoff.

## Stage 2 acceptance criteria

- one spec-driven full-simulation route and one production-summary-to-display
  route remain;
- model and numerical-diagnostic simulation paths share one recurrence;
- all six production parquet SHA-256 values and validation row counts are
  unchanged;
- every regenerated numerical summary is identical to the Stage 1 baseline;
- PNG hashes and rasterized PDF pages are identical to the Stage 1 baseline;
- the reduced tests, type check, retained shell helpers, and anonymous package
  workflow pass; and
- the repository documents only current interfaces and unresolved decisions.

## Stopping rule

Each stage receives one focused implementation pass and one repair/verification
pass. Stop and return to the PI when its acceptance criteria are met. Further
polish, speculative generality, or repeated checks without new decision-relevant
evidence belongs to a later tranche, not the current one.
