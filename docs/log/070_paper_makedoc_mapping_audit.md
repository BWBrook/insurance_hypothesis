# 070 Paper Mapping and makedoc Audit

- Date/time (UTC): 2026-02-23
- Objective: complete post-restructure path rewrite and verify `paper/` readiness against `docs/makedoc_primer_for_agents.md`.

## Actions completed

1. Historical path rewrite and cleanup
- Rewrote repository references from legacy `manuscript/...` to `paper/manuscript/...` across active docs and runtime notes.
- Updated `AGENTS.md` structure block to reflect canonical `paper/` hierarchy.
- Updated `analysis/run_all.py` messaging/comments to reference `paper/manuscript/figures/`.
- Updated historical logs/review docs where path strings pointed to moved files.

2. Table and link sanity fixes
- Repaired malformed Table 1 row in `paper/manuscript/text/tables.md` (`positive-matched control` line now valid markdown math/text).
- Updated stale archive reference in `docs/log/010_model_design.md` to current archived file paths.

3. makedoc-facing scaffold added under `paper/`
- Added `paper/settings/build.yaml` (external-path profile targeting manuscript text, tables, figures, bibliography, CSL, and author metadata).
- Added `paper/manuscript/text/figures.md` with explicit figure blocks and stable IDs (`#fig-main-...`, `#fig-main-s...`).
- Wired bibliography input to `paper/references/ih_references.yaml` (canonical bibliography file).
- Updated `README.md` and `docs/plan.md` to document these new paths.

4. Primer alignment
- Updated `docs/makedoc_primer_for_agents.md` examples and contracts to use the `paper/`-prefixed layout used in this repository.

## Audit outcome (current state)

- `paper/` now contains the expected top-level components for makedoc integration:
  - manuscript text + figures + author metadata,
  - bibliography YAML,
  - CSL style,
  - build profile.
- Figure assets referenced in `paper/manuscript/text/figures.md` exist in `paper/manuscript/figures/`.
- YAML syntax check passed for:
  - `paper/settings/build.yaml`
  - `paper/references/ih_references.yaml`

## Remaining caveats for strict makedoc quality gates

- `paper/manuscript/text/draft_ms_v2.md` still contains manual author-year citations and several `[REF]` placeholders; strict `make check` linting is expected to fail until citation syntax is converted to Pandoc citekeys and placeholders are resolved.

## 2026-02-23 follow-up (after makedoc-agent answers)

- Confirmed policy: external-path builds should use absolute paths.
- Updated `paper/settings/build.yaml` accordingly and split profiles:
  - `ih_draft` (scoped lint for iterative drafting),
  - `ih_submission` (strict full lint for final gate).
- Confirmed `main.md` is convention only; retained `paper/manuscript/text/draft_ms_v2.md` as primary source.
- Standardised to a single canonical bibliography file: `paper/references/ih_references.yaml`; removed duplicate `paper/references/refs.yaml`.
