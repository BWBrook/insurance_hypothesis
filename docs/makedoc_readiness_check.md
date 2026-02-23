# makedoc Readiness Check (paper/ structure)

Date: 2026-02-23  
Reference standard: `docs/makedoc_primer_for_agents.md`

## Scope

This check focuses on structural and mapping readiness after moving manuscript assets under `paper/`.

## Contract checklist

1. Repository paths use `paper/` hierarchy consistently: **PASS**
   - Active docs and pipeline paths now reference `paper/manuscript/...`, `paper/references/...`, and `paper/csl/...`.

2. Figure assets available under canonical figure directory: **PASS**
   - Required files exist under `paper/manuscript/figures/` (Fig. 1-5, Fig. S1-S4).
   - `analysis/run_all.py` copies to `paper/manuscript/figures/` successfully.

3. makedoc figure source file with explicit IDs: **PASS**
   - Added `paper/manuscript/text/figures.md`.
   - IDs follow required pattern (`#fig-main-*`, `#fig-main-s*`).

4. Bibliography YAML at expected path: **PASS**
   - Canonical bibliography file is `paper/references/ih_references.yaml`.
   - Build profiles now point directly to this canonical file (no duplicate bibliography files).

5. CSL file at expected location: **PASS**
   - `paper/csl/oikos.csl` present and referenced by build profile.

6. Author metadata file present: **PASS**
   - `paper/manuscript/authors.yaml` present.

7. Build profile file present: **PASS**
   - Added `paper/settings/build.yaml`.
   - Uses absolute paths for external-path reliability.
   - Includes two profiles:
     - `ih_draft`: scoped lint for iterative drafting.
     - `ih_submission`: strict lint for submission gating.
   - YAML syntax checks clean for build and bibliography files.

8. Body manuscript source file naming convention (`main.md`): **PASS**
   - Current body source is `paper/manuscript/text/draft_ms_v2.md`.
   - Confirmed acceptable by makedoc guidance as long as it is included in `manuscript_sources`.

9. Citation lint readiness (`@citekey` only, no `[REF]` placeholders): **WARN (known, expected at this stage)**
   - `paper/manuscript/text/draft_ms_v2.md` still includes manual author-year citations and `[REF]` placeholders.
   - Strict `makedoc` lint (`make check`) is expected to fail until citation syntax conversion/finalisation.

## Validation commands run in this repo

```bash
uv run pytest
uv run python analysis/run_all.py
```

Both commands completed successfully; figure copy targets now resolve to `paper/manuscript/figures/`.

Note: `makedoc`/`make validate-config` is not available in this repo runtime, so config validation here is limited to YAML parsing and path-existence checks.

## Integration status

Key integration questions Q-002 through Q-005 are resolved and recorded in `docs/questions_for_human.md`.
Only scientific-priority question Q-001 (future covariance-structure robustness direction) remains open.
