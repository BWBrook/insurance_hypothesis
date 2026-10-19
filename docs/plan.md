# Oikos final-revision plan

## Scientific objective

Test when environmental variability is buffered at the community level because
species respond asynchronously. The implemented stochastic Ricker model compares
mixed response directions with aligned responses under correlated AR(1)
environmental forcing.

The paper separates two relative comparisons: mixed versus matched aligned
responses, and shared versus independent exposure within a fixed community.
Opposing responses can retain their sign-only advantage while shared exposure
becomes destabilising. Richness, persistence and synchrony patterns support
this analysis without identifying isolated causal effects of those quantities.

## Current tranche: mechanism and predictive ordering, 19 October 2026

The PI requested substantial asynchronous reworking by Codex and Claude for a
broad ecology editor and a specialist reader. Discussion 89 records the
competing drafts, prespecifications, independent checks and handoffs. The
integrated 18 October manuscript is `d6adc5c`; Claude's new ordering analysis and
mechanism-led manuscript are `d5947b3` and `d4352cf`, respectively, on
`claude/oikos-editorial-checkpoint`.

The paper centres on **shared environments can destabilise communities with
balanced opposing responses**. It distinguishes the sign-only advantage of
mixed responses from the shared-to-independent ratio of mean replicate squared
CV within a community. Compensation can persist while this ratio exceeds one.
The mechanism is a second-order contribution from changes in squared species
departures; it is not an exact identity for the full nonlinear trajectory.

The active evidence now comprises 18 grids, 1,738 scenarios and 1,733,000
replicate summaries. The original seven production grids and their specifications
remain unchanged, as do the model recurrence, production seeding and retained
metrics. The main display suite has three figures: the original sign/balance
comparison, amplitude dependence with a visible reversal, and compositional
trajectories plus predictive ordering. Nine supplementary figures retain the
supporting gradients and full boundary paths.

- The local second-order formula meets both recorded acceptance definitions in
  all 23 eligible settings, including one independent-seed calibration repeat.
- Five original floor-free reversals survive Bonferroni adjustment across 108
  comparisons and independently seeded 6000-step repeats. Four longer-run
  settings remain floor-free; one replicate in the fifth has eight species-time
  floor observations. The separate guard diagnostic covers these five settings,
  with its reused seed stream and prefix dependence disclosed.
- Ordering by `x = c * sigma_env^2` was noticed after the mechanism grids ran.
  Predictions for new competition/autocorrelation values were then recorded
  before two new grids ran. This tests interpolation calibrated on previous
  simulations; it does not validate the leading-order formula at large noise.
  Reported criteria are 35/35 ratios within 10% (maximum error 4.6%), 17/17
  eight-species buffering/amplification calls correct, and 14/15 twelve-species
  values above the eight-species reference curve. All 13 floor-free reversals in
  the new test survive adjustment across 60 comparisons; the largest ratio is
  2.03. The full longer-window and guard tests were not extended to these new
  cases. A separate audit-only 200-replicate check of the largest reversal
  retained a ratio of 2.011 (1.985–2.037) over 3000 post-burn-in steps, without
  floor contact or clipping; it is not a new production result.
- Richness patterns describe relative stability in the specified assembly
  sequence, which also changes slopes, equilibrium abundance and feedback.
  Composition-boundary crossings remain descriptive interpolations.

The integration updates the cover letter and significance statement and corrects
exact versus approximate mechanism wording. Independent numerical and literature
reviews support the central result with those corrections. Closest prior work is
now acknowledged, the broad priority claim is removed, and empirical comparisons
are restricted to what their sources measured. Both new reviews are retained in
`docs/oikos_ordering_scientific_review_2026-10-19.md` and
`docs/oikos_ordering_literature_review_2026-10-19.md`; the earlier review remains
in `docs/oikos_october_scientific_review_2026-10-18.md`.

The checkout passes 46 tests and Pyright. All 89 protected computational files
are unchanged by this manuscript integration, and independent archive integrity,
checksums and canonical-file comparisons pass. Final document verification is
recorded in the submission checklist and
`build/ordering_integration_2026-10-19/`.

The current anonymous computational package is
`de_identified_repos/insurance_hypothesis_2026-10-19/ih_package.zip`, with
51 expected outputs. Its exact hash and replay evidence are recorded in
`docs/oikos_submission_checklist.md`. Manuscript-only edits do not alter its
computational contents. Funding and acknowledgements remain author placeholders;
the PI's full reading precedes first public release and submission.

## Completed checkpoint: external-review corrections and prose pass, September 2026

The PI approved the four bounded recommendations from the fresh Astra review
in `docs/oikos_astra_external_review_2026-09-18.md`:

1. mask undefined zero-forcing synchrony in the Figure S2 display summary;
2. make Figures 1 and 2 readable at their final physical size;
3. acknowledge existing abundance-weighting work and specify the integrated
   benchmark and nonlinear test as the contribution; and
4. remove the heading-only Supporting-information page.

The permitted display changes preserve all seven production datasets, seeds,
model dynamics, numerical estimands and nonzero-forcing summaries. The only
numerical display correction is missing values for undefined Figure S2 cells.
No production rerun is warranted. The external review's longer-window check is
retained as review evidence, without adding a new manuscript result or changing
the minimal scientific archive. Validator strengthening remains optional
maintenance outside this tranche.

All four corrections are complete. The repository passes 40 tests and Pyright;
canonical regeneration preserves all seven datasets/specs and every numerical
summary except the 15 undefined Figure S2 mean/SD cells. Figures 1 and 2 have
approximately 8 pt minimum text at submitted size. All six manuscript profiles,
PDF identity/structure checks, DOCX sanitization and refreshed manifests passed.
The final main PDF has 29 pages and Supporting information has 10, with every
page visually checked.

The rebuilt anonymous ZIP passes an independent clean extraction: 36 tests,
Pyright and all 32 expected-output hashes. Evidence is in
`build/review_corrections_2026-09-19/`; artifact locations and the exact archive
hash are in `docs/oikos_submission_checklist.md`.

Removing the SI divider required a small separate makedoc fix, with regression
checks for standalone and mixed figure documents. It is committed on branch
`claude/standalone-si-divider` of the makedoc repository (`4cd4809`).

A prose pass followed on 28 September at the PI's request. It revised the
main-text prose and figure captions for readability and for readers outside the
subfield, without changing equations, citations, claims or displays, and
corrected two roundings: the Fig. 1A value near perfect correlation and the
Monte Carlo SD example. All six profiles and the golden contract pass. The main
PDF has 31 pages with the Introduction on page 2, and the abstract has 277
words. Pre-pass copies and word diffs are in `build/prose_pass_2026-09-28/`.
Both tranches are committed on branch `claude/oikos-editorial-checkpoint`. The
next human step is the PI's editorial pass. Public release and submission await
that pass and the outstanding author declarations.

## Locked evidence base

Seven validated production grids contain 1,196,000 replicate summaries in
total:

| Grid | Rows | Primary use |
| --- | ---: | --- |
| `fig1_s4_highres_v1` | 570,000 | Core mixed-versus-aligned response surface |
| `fig1_s4_highsigma_v1` | 180,000 | Labelled high-variance stress extension |
| `fig2_richness_mixed_v1` | 210,000 | Richness display, S1/S2, variance decomposition |
| `fig3_synchrony_v1` | 66,000 | Imposed-versus-realised synchrony and species-CV diagnostic |
| `fig5_persistence_mixed_v1` | 64,000 | Fixed-innovation persistence sensitivity |
| `figs3_positive_matched_control_v1` | 66,000 | Magnitude-matched response-sign control |
| `fig4_weighted_balance_r0_v1` | 40,000 | Weighted-balance boundary and `r0` sensitivity |

The present numerical summaries and display items are protected. Any future
simulation analysis must use a new, versioned spec and output directory.

## External-review response boundary

The 2026-08-09 external review found no fatal scientific or computational defect.
Its highest-value recommendations are accepted:

1. promote the magnitude-matched positive control in the evidential hierarchy;
2. express the first-order mechanism as an abundance-weighted covariance
   criterion, with its assumptions explicit;
3. clarify that environmental exposures share a common orientation;
4. test the special `r0 = 1`/equal-abundance boundary with a compact sensitivity;
5. replace the former descriptive Figure 4 with a more diagnostic display; and
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
- [x] **Stage 3 — bounded scientific revision.** Prespecify and run the smallest
  response-balance/abundance-weight/`r0` sensitivity that tests the reviewer's
  central boundary conditions. Promote the existing magnitude-matched control,
  replace Figure 4, and revise the manuscript's mechanism and claim hierarchy.
  Verify claim-specific invariants and pause for PI review.
- [x] **Stage 4 — release and submission gate.** Run the full code/data/display
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

## Stage 3 prespecification

One new production grid, `fig4_weighted_balance_r0_v1`, will contain 40
scenarios and 40,000 replicate summaries. It is deliberately limited to
`S = 4`, innovation SD `sigma_env = 0.5`, `phi = 0.4`, requested exposure
correlations `rho_env = 0` and `1`, 600 steps, 300 burn-in steps, and 1000
replicates per scenario. All environmental axes have the same physical
orientation. The comparison quantity is the ratio of mean squared community CV
at effective correlation near one to that at zero.

The grid has three prespecified components:

1. **Response alignment:** rotate the balanced mixed vector continuously towards
   its magnitude-matched aligned counterpart at nine equally spaced positions,
   preserving its Euclidean norm exactly and keeping equal `K_i = 100` and
   `r0 = 1`.
2. **Abundance weighting:** keep the balanced mixed response vector and `r0 = 1`
   while varying carrying capacities along five positive skew levels. Their sum
   remains 400, so deterministic total abundance remains constant; the final
   level crosses the first-order alignment boundary while retaining a positive
   interior equilibrium.
3. **Dynamical memory:** repeat the balanced mixed and magnitude-matched aligned
   endpoints at `r0 = 0.25, 0.5, 1.0, 1.5`, with equal carrying capacities.

The first-order benchmark uses `a_i = N_i* b_i`, where `N_i*` is the positive
deterministic equilibrium, and

`A = (sum(a_i))^2 / (S sum(a_i^2))`.

For the equicorrelated exposure design, the predicted high/independent forcing-
variance ratio is `(1-rho_eff) + rho_eff S A`, and the predicted sign boundary is
`A = 1/S = 0.25`. The new Figure 4 will compare that benchmark with nonlinear
simulation, then show whether the matched-sign reversal persists across `r0`.

Stage 3 passes if the production output validates; response norms and scenario
metadata match the specification; every deterministic equilibrium is positive;
the abundance-weight path holds deterministic total abundance constant; the
balanced and aligned high/independent CV-squared ratios remain respectively
below and above one at every tested `r0`; the alignment-gradient reversal occurs
near the analytical boundary; and floor occupancy is absent or explicitly
reported. A failed scientific check changes the claim rather than being tuned
away with a broader sweep.

## Stage 3 outcome

The new grid completed all 40 scenarios and 40,000 replicate summaries, bringing
the active evidence base to seven production grids and 1,196,000 rows. All
prespecified checks passed. The response-vector norm varied by less than
$8\times10^{-13}$ along the rotation; all deterministic equilibria were positive;
and deterministic total abundance along the carrying-capacity path was constant
at 210.53 to numerical precision.

At the balanced endpoint, the high-correlation to independent-exposure ratio was
$R_{\mathrm{CV}^2}=0.320$ (95% Monte Carlo interval 0.315--0.325), whereas the
magnitude-matched aligned endpoint gave 2.992 (2.965--3.019). The response and
abundance-weight paths both crossed one near the analytical boundary
$A=1/S=0.25$. Balanced ratios remained below one and aligned ratios above one at
every tested $r_0$. Floor contact was absent except for negligible occupancy in
the most uneven abundance-weight treatment. Figure 4 and the manuscript now use
these results, and obsolete Figure 4 association outputs are retired.

## Stage 4 outcome

The final release gate passed on 2026-08-10. All seven production summaries
validated at 1,196 scenarios and 1,196,000 replicate rows; 39 repository tests,
Pyright, numerical guards, and the canonical display workflow passed. Consecutive
full display regenerations produced identical PDF hashes, and all PNG plus
rasterized-PDF comparisons matched the PI-approved Stage 3 suite.

All six manuscript profiles passed their current makedoc checks. The anonymous
main PDF is 28 pages with a 230-word abstract and the Introduction on page 2; its
golden contract, identity sanitization, and page-by-page PDF/DOCX inspection
passed, as did the 9-page Supporting information. A live check of the Oikos/NSO
guidance prompted one narrow compliance correction: the main text now refers to
the separate file only as “Supporting information”. A simulation-appropriate
equity, diversity and inclusion response was also added to the submission-form
statements.

The rebuilt anonymous package contains all seven specs and compact summaries.
From inside that package, 35 reviewer-facing tests, Pyright, and regeneration of
nine figures and 11 tabular summaries passed; the clean zip also passed archive,
path, and identity checks. The only remaining submission tasks are the
author-supplied facts recorded in `docs/questions_for_human.md`. An optional
anonymous cold-review bundle and cover note were also prepared for one final Pro
review without expanding the scientific scope.

## Stopping rule

Each stage receives one focused implementation pass and one repair/verification
pass. Stop and return to the PI when its acceptance criteria are met. Further
polish, speculative generality, or repeated checks without new decision-relevant
evidence belongs to a later tranche, not the current one.
