# Production-result interpretation

These notes retain the decision-relevant reading of the validated production
evidence. Exploratory chronology and completed task lists are in Git history.

## Headline contrast: Figure 1

- Across the shared environmental grid, aligned positive responses are markedly
  more variable than mixed responses. Averaged over effective driver correlation,
  the aligned/mixed mean-CV ratio is about 3.0 at `sigma_env = 1`, 3.5 at 1.5,
  and 4.3 at 2.
- Mixed-response communities remain buffered until stronger forcing, but they
  also become highly variable in the stress extension. At `sigma_env = 4`, mean
  CV is about 4.39 for mixed slopes and 11.13 for aligned slopes.
- The relative contrast persists at the stress edge but narrows, while floor
  occupancy becomes scientifically non-negligible. Claims should foreground the
  core grid and label `sigma_env >= 3` as a stress regime.
- The simple effect of `rho_eff` is not monotone at every high-variance edge;
  the robust result is the response-regime contrast, not a universal monotonic
  correlation law.

## Richness sequence and variance decomposition: Figure 2

- In the implemented mixed-slope assembly sequence, mean community CV declines
  monotonically from `S = 2` to `S = 8` at every non-zero `sigma_env` after
  averaging over the shared non-negative `rho_eff` values.
- The `S = 2` to `S = 8` mean-CV ratio is roughly 2.2–2.8 across the production
  environmental-variance range.
- Floor occupancy is too small in this grid to explain the pattern.
- This is not an independent richness manipulation: slope composition, response
  balance, and abundance weighting change with `S`. The result supports a
  richness-associated buffering pattern for this deterministic assembly
  sequence, not a general causal richness coefficient.
- The exact decomposition
  `Var(sum N_i) = sum Var(N_i) + 2 sum Cov(N_i, N_j)` should be used to connect
  the aggregate pattern to abundance covariance without treating raw associations
  as mediation.

## Imposed versus realised synchrony: Figure 3

- At `sigma_env = 0.5`, mixed responses produce realised per-capita growth
  correlations far below imposed environmental correlation; aligned responses
  remain strongly positive and rise with `rho_eff`.
- Near `rho_eff = 1`, mixed-response mean growth correlations are approximately
  -0.81, -0.16, and 0.08 for `S = 2, 4, 8`, whereas aligned-response values are
  approximately 0.64, 0.81, and 0.86.
- This is direct evidence that common environmental orientation plus response
  sign structure can transform shared forcing into compensatory realised
  dynamics. Imposed driver correlation is not itself biological synchrony.

## Magnitude-matched sign control: Figure S3, to be promoted

- `positive_matched = abs(mixed)` preserves the mixed regime's slope magnitudes
  while aligning all response directions.
- Near `rho_eff = 1`, positive-matched community CV is about 0.184 versus 0.319
  for the steeper positive regime at `S = 4`, and 0.158 versus 0.316 at `S = 8`.
  Magnitude therefore affects absolute variability.
- Nevertheless, positive-matched realised growth correlations remain high
  (about 0.90 at `S = 4` and 0.84 at `S = 8`) and do not reproduce the weak or
  negative synchrony of mixed responses.
- This is the cleanest existing control for the central sign-structure mechanism
  and should move into the main evidential hierarchy.

## Persistence sensitivity: Figure 5

- At fixed innovation SD `sigma_env = 0.5`, increasing `phi` raises both temporal
  persistence and stationary environmental variance, strongly increasing
  community CV.
- At `rho_eff = 0.5`, mean CV rises from about 0.14 to 0.58 for `S = 2` and from
  0.07 to 0.35 for `S = 4` as `phi` moves from 0 to 0.95.
- The `S = 4` sequence remains less variable than `S = 2` throughout the shared
  grid, but this does not isolate a pure autocorrelation effect.
- Floor occupancy is negligible through `phi <= 0.7`, low at 0.9, and locally
  non-negligible at 0.95. High persistence is a stress test.

## Current Figure 4

- Raw production scenario means show strong positive association between CV and
  Loreau-de Mazancourt synchrony (Pearson `r` about 0.85) and a moderate
  association with realised pairwise growth correlation (about 0.57).
- The first association is partly mathematical because both quantities contain
  `Var(N_total)`. Both panels also mix richness, forcing magnitude, and imposed
  correlation.
- The plot is descriptive, not an independent-effect or mediation analysis. It
  is the lowest-value main display and is scheduled for replacement in Stage 3.

## Numerical boundaries

- Core production inference grids have negligible floor occupancy and no NaN or
  infinite summaries.
- High-variance and high-persistence extensions deliberately reach regions where
  the abundance floor participates in the dynamics. These are retained to show
  robustness boundaries, not to strengthen the core low-stress inference.
- Exponent clipping, floor occupancy, and abundance plausibility must be checked
  whenever the bounded sensitivity changes `r0`, response balance, or abundance
  weights.

## Questions Stage 3 must decide

1. Does the mixed-versus-aligned contrast persist away from the special
   `r0 = 1`/equal-abundance boundary?
2. How does controlled response imbalance change the abundance-weighted first-
   order covariance criterion and simulated aggregate variability?
3. Which diagnostic most compactly replaces current Figure 4 without opening a
   broad new modelling programme?
4. After these checks, what is the narrowest accurate statement of the mechanism
   and richness/persistence limitations?
