# 350 – External review intake and triage

## 2026-08-09

### Source and integrity

The commissioned cold review was supplied at
`/mnt/c/Temp/Oikos_external_review_and_line_edit_2026-08-09.md` on the local
WSL laptop. It was copied unchanged to
`docs/oikos_external_review_and_line_edit_2026-08-09.md`.

- Size: 75,568 bytes; 910 lines.
- SHA-256 (source and repository copy):
  `42454eeb6891c494f773a0e4061a06794c2c39b30ca049bf56cace669b077483`.
- The reviewer excluded and did not open `03_editorial_materials_unblinded`.

### Root assessment

The report is scientifically strong and its major-revision-then-submit verdict
is accepted in substance. It found no fatal scientific or computational defect.
The highest-value finding is that the existing 1000-replicate
`positive_matched` treatment is the clean causal comparison: at zero exposure
correlation it is nearly identical to the mixed-sign treatment, but the two
diverge strongly as correlation rises. The current broad positive comparator
also changes coefficient RMS and should become an amplitude sensitivity rather
than the headline effect.

The proposed covariance criterion is correct for equal-variance,
equicorrelated *first-order aggregate environmental forcing*. The current main
text already contains the equivalent abundance-weighted variance expression,
so the revision should add its derivative, cancellation boundary, and
common/contrast-mode interpretation rather than present the idea as wholly
new. It must not be called a universal nonlinear stability criterion without
deriving the relevant dynamical transfer; outside the symmetric local model,
stationary abundance variance depends on the full linearized dynamics.

The report also identifies two consequential assumptions missed by earlier
passes:

- environmental axes need a shared physical orientation for response signs and
  exposure correlations to be separately interpretable; and
- `r0=1` gives a zero common-mode eigenvalue at the symmetric equilibrium,
  while equal abundance and zero-sum slopes maximize cancellation.

These justify one compact, prespecified sensitivity tranche spanning response
imbalance, unequal abundance/contribution weights, and a small stable `r0`
grid. A continuous balance display can replace the current descriptive Figure
4, while the existing positive-matched display should be promoted to the main
paper.

### Recommendations accepted without new simulation

- Tighten the title, abstract, Results hierarchy, Discussion opening, and
  conclusion around the magnitude-matched result and weighted cancellation.
- Define the environmental variables as commonly oriented physical exposures,
  or use demographic-shock covariance as the invariant formulation.
- Retain the existing richness analysis only as a prespecified compound
  assembly sequence. The manuscript already acknowledges its changing response
  RMS, total abundance, and composition, but the abstract, section title,
  captions, and insurance definition still need tightening.
- Keep the autocorrelation result explicitly described as a fixed-innovation,
  persistence–stationary-variance stress gradient. The current manuscript
  already makes this qualification; a fixed-stationary-variance rerun is not
  required unless a causal autocorrelation claim is retained.
- Cite the highly relevant Ives et al. (1999) item already present in the
  bibliography and remove other unused references unless needed after revision.

### Recommendations deferred or corrected

- Common random numbers would improve precision but are not required to rescue
  the existing 1000-replicate matched comparison; use them for any new direct
  contrasts rather than rerunning the old grid solely for pairing.
- Alternative covariance structures, a competition gradient, a second
  density-dependence model, a common-pool richness experiment, and nonlinear
  response curves are optional extensions rather than pre-submission gates.
- The report's statement that mixed signs are not necessary is too broad: under
  the equicorrelation derivative, opposite signs are necessary for a negative
  correlation effect, although they are not sufficient without adequate
  weighted cancellation.
- Oikos asks authors to have a data-archiving statement ready in the submission
  system and to provide data/code at first submission; it does not require that
  statement to be inserted into the anonymous initial main-text file. The
  existing separate submission-form statement and reviewer ZIP follow the
  current guidance.
- The existing AI statement already names OpenAI Codex and its roles. Greater
  specificity is worth considering, but exact model-version wording is an
  author confirmation rather than a scientific blocker.
- The reviewer environment's 41/48 partial test run reflects missing Parquet
  and Python tooling. The supplied package had already passed all 48 tests,
  Pyright, and the analysis workflow in the locked environment. Repeat those
  checks after substantive edits; a new repository overhaul is unnecessary.

### Proposed next tranche

Before implementation, prespecify a bounded scientific revision that combines:

1. a fixed-norm response-balance gradient;
2. an unequal-abundance or contribution-weight sensitivity; and
3. a small deterministically stable `r0` grid.

Then revise the theory and prose around the existing matched control, replace
only the main display whose evidential value is materially weakest, and run the
full submission QA once. Richness and temporal-autocorrelation expansions
remain optional unless the chosen final claims require causal identification.
