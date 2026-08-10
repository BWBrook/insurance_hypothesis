# De-Identified Review Package

## Purpose and submission classification

The package supplies the minimum code, simulation specifications, compact
production summaries, and tests needed for double-anonymized peer review. It is
an **additional file for review but not for publication**, not Supporting
information. The distinction matters because NSO publishes Supporting
information as received, whereas the review package will be replaced by a
permanent public archive if the manuscript is accepted.

## Current artefacts

- Staging directory: `/home/bwbrook/papers/de_identified_repos/ih_package/`
- Upload candidate: `/home/bwbrook/papers/de_identified_repos/ih_package.zip`
- Rebuilt: 2026-07-24
- Archive size: 72,617,256 bytes (about 69.3 MiB)
- SHA-256:
  `f2cada4521af344fe156023740da4b1475e16cd8ef897dbe1e16d9c65dbbecea`
- Contents: 66 archive members, including six compact production-summary
  parquet files and seven runnable reproduction-test files.

Because the zip exceeds 50 MB, confirm that ScholarOne accepts it under
“Additional file for review but NOT for publication”. If not, use an anonymous
repository route, such as a private-for-review archive, rather than relabelling
the package as Supporting information.

## Included

- Anonymous `README.md` and `README_REVIEW.md` with setup and run instructions.
- Sanitized `pyproject.toml`, `uv.lock`, and `.python-version`.
- `src/python/insurance_sim/`.
- Runnable simulation and reproduction tests under `tests/python/`.
- Analysis scripts required to regenerate analysis-facing outputs.
- Sanitized versioned production specifications.
- Six compact production summaries under `data/sim/production/`.

## Excluded

- `.git/`, Git remotes, and local virtual environments.
- Manuscript, title-page, bibliography, and build sources.
- Project documentation, questions, logs, and submission-helper scripts.
- The repository-only submission-helper test, which depends on deliberately
  excluded packaging and DOCX-sanitization scripts.
- Remote-compute scratch outputs, tmux logs, shards, and bulky intermediates.

## Build command

Run from `/home/bwbrook/papers/insurance_hypothesis`:

```bash
uv run python scripts/build_deidentified_review_package.py --zip
```

The builder defaults to `~/papers/de_identified_repos/ih_package`. Set
`IH_REVIEW_PACKAGE_ROOT` only when deliberately staging elsewhere.

## Verified package workflow

The following commands were run from a newly built package on 2026-07-24:

```bash
uv sync --python 3.12 --frozen --dev
uv run pytest -q
uv run pyright
uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export
```

Results:

- 48 tests passed.
- Pyright reported zero errors and zero warnings.
- The analysis workflow completed and regenerated report outputs.
- The final archive was rebuilt after testing so it contains neither `.venv/`
  nor generated report files.
- Packaged simulator code, runnable tests, analysis scripts, production
  summaries, and `uv.lock` match the source repository byte-for-byte.
- Production specifications differ only in the deliberately sanitized execution
  host and remote-root fields; `pyproject.toml` differs only by replacing the
  author with `Anonymous`.
- Text files and parquet metadata/string fields contain none of the configured
  author, institution, repository, or local-path identity markers.
- The archive contains no Git metadata, manuscript material, author metadata,
  submission-helper scripts, or repository-only submission-helper test.
