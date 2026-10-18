# Reproducibility release boundary

## Scientific target

The release must preserve the two related comparisons estimated by the paper.
The main shared-exposure estimand is

```text
R = mean_replicate(cv_total^2 | shared, near-perfect exposure)
    / mean_replicate(cv_total^2 | independent exposure).
```

The means are taken over replicate-level summaries before forming the ratio; it
is not a ratio of mean `cv_total` values. The mixed-versus-matched-aligned sign
contrast is reported separately. Monte Carlo uncertainty comes from
independently seeded simulated trajectories, with scenario as the treatment
unit and replicate as the Monte Carlo unit. The simulation process, complete
simulated abundance trajectories, sixteen versioned production grids, and
effective-correlation handling are fixed by the active code path.

## Current anonymous review package

The allowlisted package is sufficient for double-anonymous computational review.
It contains the model and analysis code, locked Python environment, 41
collected tests in a clean extraction, sixteen complete specs, and sixteen
compact production summaries. Fresh manifests generated from those specs can
validate all 1,618 scenarios and 1,613,000 replicate rows. The seven original
production summaries remain part of this protected set; the added grids are
`boundary_by_sigma_v1`, three `sigma_mechanism_alpha*_v1` grids, and five
`longwindow_reversal_*_v1` grids.

The full source checkout currently collects 45 routine tests; the archive
collects 41 because it excludes the repository-only submission-helper tests.

The saved summaries drive 12 manuscript figures (three main and nine
Supporting Information figures), 15 figure-summary CSVs, and two
variance-decomposition CSVs through `analysis/run_all.py`. The package's
expected-output checksum file contains those 41 outputs plus six retained
numerical-guard reports, for 47 expected outputs in total.

The separate numerical-guard script retains the original three prespecified
scenarios with 30 replicates each and seed 12345. Its new reversal block covers
five balanced-community settings at both exposure endpoints, with 200 full
600-step trajectories and 100 full 6000-step trajectories per condition, using
its own fixed seed. The two blocks produce six retained report files in total.
These are independent full-trajectory diagnostics, distinct from the
post-burn-in production floor frequencies: sampling the guard scenarios does
not certify every production replicate.

Tables S1 and S2 are embedded manuscript tables rather than files emitted by
`analysis/run_all.py`. Their row/scenario counts and floor-frequency maxima are
direct aggregations of the included parquet columns; the package README gives
the exact reconstruction. Table S3 is emitted by `analysis/run_all.py`. Table
S4 records the prespecified mechanism predictions and eligibility results from
`analysis/prespecified/` and the three mechanism grids. Table S5 records the
five long-window reversal checks and is backed by the retained long-window
summary emitted by `analysis/run_all.py`.

The package records two checksum layers: `SHA256SUMS.txt` verifies all files
supplied for review, while `EXPECTED_OUTPUT_SHA256SUMS.txt` records the 47
analysis and numerical-guard outputs expected from the locked release
environment. Exact byte equality across operating systems or different
numerical and graphics libraries is not guaranteed; scientific equivalence
then requires numerical and rendered-output comparison.

## Manuscript mapping

Generated filenames and production identifiers are stable even though the
manuscript order changed. The three main figures use
`fig4_weighted_balance_boundary` (Figure 1), `fig6_amplitude_boundary`
(Figure 2), and `fig7_mechanism_reversal` (Figure 3). The former main Figures
2--5 are now Figures S5--S8 and retain the stems
`fig3_imposed_vs_realised_panels`, `fig1_panels`,
`fig2_richness_scaling_mixed`, and `fig5_phi_sensitivity_sigma0.5_extended`,
respectively. Figures S1--S4 retain their existing stems, and the new Figure
S9 is `figS9_boundary_by_sigma_paths`. Each stem has PNG and PDF outputs under
`analysis/reports/`; the manuscript sources reference those canonical paths.

## Smallest eventual public archive

Use the anonymous package contents as the computational core. After final author
review and approval, the public version should add only:

- author metadata and the final data-and-code availability wording;
- a Barry-approved licence;
- `CITATION.cff` or equivalent machine-readable citation metadata;
- the accepted repository URL, release version/tag, and archived DOI; and
- a release note identifying the paper version and archive SHA-256.

Do not publish the anonymous archive as the permanent record. Prepare licence
and publication metadata proposals reversibly; final author review covers them
before the first public release. Manuscript source, editorial histories,
local/remote compute logs, Git internals, and intermediate shards are
unnecessary for the minimal computational archive unless the selected release
workflow makes one of them a required source input. The first public release
and any submission remain one-way actions requiring the PI's final author
review and approval.

The PI prefers a preprint before journal submission. The anonymous review
package and public record remain distinct; disclose a preprint URL to the editor
when one exists. No preprint or public archive has been released in this tranche.

## Public-release verification gate

At the frozen author-approved paper or preprint commit:

1. validate every saved parquet against a manifest freshly generated from each
   of the sixteen corresponding specs;
2. verify the supplied-file checksums, tests, and Pyright in a clean extraction;
3. run `analysis/run_all.py` and the separate numerical-guard diagnostic;
4. compare all 47 expected-output hashes, numerical summaries, and rendered
   figures with the frozen release references;
5. reconstruct Tables S1 and S2 from the parquet files and confirm agreement
   with that manuscript version; confirm the mechanism and long-window Table S4
   and S5 sources are the corresponding retained outputs;
6. scan archive paths, text, parquet metadata, and Git-excluded content for
   local paths or unintended private/editorial material; and
7. create the author-approved version/tag and DOI archive only after all prior
   checks pass.

The full production grids can also be regenerated from the specs and
deterministic seeds, but this is a compute-intensive validation tier rather than
a prerequisite for reviewing figures from the supplied summaries. When it is
run, compare semantic parquet contents as well as file hashes because Parquet
bytes can depend on the writer environment.
