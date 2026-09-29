# Reproducibility release boundary

## Scientific target

The release must preserve the comparison estimated by the paper: replicate-
mean temporal community-abundance CV under mixed versus aligned environmental
responses, with Monte Carlo uncertainty across independently seeded simulated
trajectories. The simulation process, observation process (complete simulated
abundance trajectories), scenario as the treatment unit, replicate as the Monte
Carlo unit, and the seven production grids are already fixed by the code and
versioned specifications.

## Current anonymous review package

The allowlisted package is sufficient for double-anonymous computational review.
It contains the model and analysis code, locked Python environment, 36 runnable
tests, seven complete specs, and seven compact production summaries. Fresh
manifests generated from the specs validate all 1,196 scenarios and 1,196,000
replicate rows. The saved summaries drive all nine paper figures, nine figure-
summary CSVs, and two variance-decomposition CSVs.

The separate numerical-guard script runs three prespecified scenarios with 30
replicates each and seed 12345. Its replicate CSV, summary CSV, and Markdown
summary are included as retained evidence and can be regenerated independently.
It does not reproduce the retired exploratory 200-replicate, high-variance
checks because their executable recipe and outputs are absent from the active
repository.

Tables S1 and S2 are embedded manuscript tables rather than files emitted by
`analysis/run_all.py`. Their row/scenario counts and floor-frequency maxima are
direct aggregations of the included parquet columns; the anonymous README gives
the exact reconstruction. Table S3 is emitted by `analysis/run_all.py`.

The package now records two checksum layers: `SHA256SUMS.txt` verifies all files
supplied for review, while `EXPECTED_OUTPUT_SHA256SUMS.txt` records the 29
summary-to-display outputs and three numerical-guard outputs expected from the
locked release environment. Exact byte equality across operating systems or
different numerical and graphics libraries is not guaranteed; scientific
equivalence then requires numerical and rendered-output comparison.

## Smallest eventual public archive

Use the anonymous package contents as the computational core. After final author
review, the public version should add only:

- author metadata and the final data-and-code availability wording;
- a Barry-approved licence;
- `CITATION.cff` or equivalent machine-readable citation metadata;
- the accepted repository URL, release version/tag, and archived DOI; and
- a release note identifying the paper version and archive SHA-256.

Do not publish the anonymous archive as the permanent record. Do not choose the
licence, author list, citation text, repository host, version number, or DOI
before author approval. Manuscript source, editorial histories, local/remote
compute logs, Git internals, and intermediate shards are unnecessary for the
minimal computational archive unless the selected release workflow makes one of
them a required source input.

The PI prefers preprinting before journal submission. Oikos permits preprints
before or during review, so journal acceptance is not a prerequisite for the
public release. Keep the review ZIP and manuscript anonymous; disclose any
preprint URL to the editor separately. A public preprint makes author identity
discoverable even when the supplied review files are anonymous. Timing remains
subject to the PI's final read and release decision.

## Public-release verification gate

At the frozen author-approved paper or preprint commit:

1. validate every saved parquet against a manifest freshly generated from its
   corresponding spec;
2. verify the supplied-file checksums, tests, and Pyright in a clean extraction;
3. run `analysis/run_all.py` and the separate numerical-guard diagnostic;
4. compare the 32 generated-output hashes, numerical summaries, and rendered
   figures with the frozen release references;
5. reconstruct Tables S1 and S2 from the parquet files and confirm agreement
   with that manuscript version;
6. scan archive paths, text, parquet metadata, and Git-excluded content for
   local paths or unintended private/editorial material; and
7. create the author-approved version/tag and DOI archive only after all prior
   checks pass.

The full production grids can also be regenerated from the specs and
deterministic seeds, but this is a compute-intensive validation tier rather than
a prerequisite for reviewing figures from the supplied summaries. When it is
run, compare semantic parquet contents as well as file hashes because Parquet
bytes can depend on the writer environment.
