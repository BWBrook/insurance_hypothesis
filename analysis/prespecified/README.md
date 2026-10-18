# Prespecified predictions

`sigma_mechanism_predictions_2026-10-18.json` is a byte-identical copy of the
second-order predictions written before any `sigma_mechanism_*` simulation ran.
The original is `build/fable_sigma_check_2026-10-18/prespecified_predictions.json`,
last modified 2026-10-18 03:35:31 UTC.

SHA-256: `10d840d777879c0a69128ef8ea182b257c285400d215ac2011b5076f957dfd6a`

For each combination of interspecific competition (`alpha_inter`), richness (`S`)
and environmental autocorrelation (`phi`), the file records the contrast-mode
eigenvalue `lambda_d` and the small-noise coefficient `kappa`. It also records the
predicted shared-to-independent ratio of mean squared CV for the balanced mixed
community at `sigma_env` 0.1 and 0.2, which is `kappa * sigma_env^2` at `r0 = 1`.
`insurance_sim.diagnostics.balanced_small_noise_coefficient` reproduces every
`kappa` value; the test suite checks this.

## Timeline, UTC, 18 October 2026

- 03:35:45: the acceptance criteria in the three `sigma_mechanism_alpha*_v1.json`
  specs were amended to the wording below, labelled "spec".
- 03:35:50: the first simulation shard was written. This was a timing shard for
  the alpha 0.6 grid.
- 03:36:08: the criteria were posted to correspondence discussion 89 (message
  1934), without the spec's extra eligibility restriction.

## The two recorded acceptance definitions

Both apply to the small-noise cells, where the predicted ratio at `sigma_env` 0.1
is below 0.1.

- **Posted (message 1934).** The observed ratio at `sigma_env` 0.1 lies within 20%
  of the prediction, and R(0.2)/R(0.1) lies between 3 and 5.
- **Spec.** The same, except that the scaling criterion applies only where the
  predicted R(0.2) is below 0.2.

Both definitions were evaluated. All 23 eligible cells pass under each. Of those
23, 22 are new parameter combinations. The `alpha_inter` 0.3, `S` 4, `phi` 0.4 cell
repeats the calibration setting with independent seeds.
