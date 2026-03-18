# makedoc Readiness Check (paper/ structure)

Date: 2026-02-23  
Reference standard: `docs/makedoc_primer_for_agents.md`

## Scope

This check focuses on structural and mapping readiness after moving manuscript assets under `paper/`.

## Contract checklist

1. Repository paths use `paper/` hierarchy consistently: **PASS**
   - Active docs and pipeline paths now reference `paper/manuscript/...`, `paper/references/...`, and `paper/csl/...`.

2. Figure assets available for manuscript builds: **PASS**
   - Required files exist under `analysis/reports/` (Fig. 1-5, Fig. S1-S4).
   - `paper/manuscript/text/figures.md` now points directly to those tracked report artefacts for fresh-clone portability.

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
   - Uses config-relative manuscript paths, while still supporting external-path builds via an absolute `CONFIG=...` passed to `makedoc`.
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
make -C /Users/bwbrook/work/makedoc validate-config CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml
```

The original note predated the later macOS verification pass. Current validation on this Mac succeeded via the external `makedoc` repo (`validate-config`, `all`, `check`) rather than through `analysis/run_all.py`, which still requires cached full-grid parquet files.

Note: this check originally predated the local `makedoc` verification pass on macOS. Current validation should be done against the external `makedoc` repo with `make validate-config`.

## Integration status

Key integration questions Q-002 through Q-005 are resolved and recorded in `docs/questions_for_human.md`.
Only scientific-priority question Q-001 (future covariance-structure robustness direction) remains open.
