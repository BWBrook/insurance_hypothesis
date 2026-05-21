# De-Identified Review Package Plan

This is a deferred packaging plan. Do not build the package until the final code is locked for submission.

## Target Location

- Staging directory: `/home/bwbrook/papers/de_identified_repos/ih_package/`
- Expected final artefact: a zip file suitable for uploading as anonymous supplementary material.

## Purpose

Provide the minimum viable code/analysis package needed for double-blind review of the simulation workflow, without requiring GitHub access and without including identifying author information or manuscript-production material.

## Include

- `README_REVIEW.md` with anonymous setup and run instructions.
- `pyproject.toml` and `uv.lock`.
- `src/python/insurance_sim/`.
- `tests/python/`.
- Analysis scripts required to regenerate code-facing outputs from compact production summaries.
- `analysis/production_specs/`.
- Compact production summaries under `data/sim/production/`, if final package size remains practical.
- Minimal `.gitignore` and non-identifying metadata required for local execution.

## Exclude

- `.git/` and GitHub remotes.
- `paper/`, `manuscript/`, `csl/`, `references/`, `reports/`, and manuscript-build outputs.
- `docs/`, unless a short anonymous review README is generated specifically for the package.
- Logs or comments containing author names, affiliations, email addresses, ORCIDs, institutional paths, or GitHub repository URLs.
- Remote-compute scratch outputs, tmux logs, shard-level production artefacts, and other bulky non-minimal intermediates.

## Required Review Commands

The package should support, at minimum:

```bash
uv sync --frozen --dev
uv run pytest -q
uv run pyright
uv run python analysis/run_all.py --skip-guard-audit
```

If `analysis/run_all.py` still assumes a manuscript export path at packaging time, add a review-safe switch before building the zip so the package can regenerate analysis outputs without needing the manuscript tree.

## Pre-Zip Checks

- Search for identifying strings: `Barry`, `Brook`, `University`, `Tasmania`, `UTAS`, `utas`, `ORCID`, email addresses, and repository URLs.
- Run the review commands from inside the staged package directory, not the source repo.
- Confirm the zip contents with `zipinfo`.
- Confirm no hidden Git metadata or manuscript sources are present.

## Status

- Deferred until final code lock.
