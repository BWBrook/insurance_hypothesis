# Final Pre-Barry Handoff

Date: 2026-05-21

## Verdict

The manuscript package is ready for Barry's human-scientist pass. The remaining work is judgement and submission polish, not more simulation production.

## Files To Read

Primary review files are in `/Users/bwbrook/work/makedoc/dist/paper/` on the Mac mini:

- `insurance_hypothesis_blinded_main.pdf` and `.docx`: double-blind main manuscript.
- `insurance_hypothesis_supplementary_info.pdf` and `.docx`: anonymous supplementary information.
- `insurance_hypothesis_cover_letter.pdf` and `.docx`: editor-facing cover letter draft.
- `insurance_hypothesis_title_page.pdf` and `.docx`: unblinded title page and author statements.

Repo source files to edit if changes are needed:

- `paper/manuscript/text/draft_ms_v2.md`
- `paper/manuscript/text/tables_main.md`
- `paper/manuscript/text/figures_main.md`
- `paper/manuscript/text/supplementary_information.md`
- `paper/manuscript/text/supplementary_tables.md`
- `paper/manuscript/text/supplementary_figures.md`
- `paper/manuscript/text/cover_letter.md`
- `paper/manuscript/text/title_page.md`

## Highest-Value Scientific Checks

- Does the main claim feel ecologically honest: biodiversity buffers variability only when species differ in response direction relative to the dominant environmental covariance structure?
- Are the $\sigma_{\mathrm{env}}$ and $\phi$ stress-region caveats strong enough, especially for high-variance and high-persistence regimes?
- Are the lower-replicate no-competition and mixed-narrow controls treated only as robustness diagnostics, not elevated as central evidence?
- Does the distinction between requested $\rho_{\mathrm{env}}$, effective $\rho_{\mathrm{eff}}$, and realised synchrony read clearly to an ecological modeller?
- Are the new 2026 references integrated in the right places without overclaiming their relevance?
- Do the figure captions now provide enough interpretation for a reviewer reading figures before the Results text?

## Barry-Only Submission Items

- Fill final funding text on the title page, or mark no specific funding if appropriate.
- Fill acknowledgements on the title page, or mark not applicable.
- Review the cover letter for author voice and any ScholarOne-specific fields.
- Confirm final article type wording in the submission system.
- Confirm whether the permanent accepted-version archive should be Dryad, Zenodo, OSF, institutional, or another DOI-bearing repository.
- After this human pass and any final code lock, build the de-identified reproducibility zip using `docs/deidentified_review_package_plan.md`; the default local staging root is `/Users/bwbrook/papers/de_identified_repos/`.

## Final Technical Notes

- Build makedoc profiles sequentially, not in parallel, because profile builds share cache state.
- After generating DOCX files, run `uv run python scripts/sanitize_docx_identity.py --check` on the blinded main and supplementary DOCX files to remove invisible local-path metadata.
- Rebuild the de-identified review-code package only once the final code/manuscript source is locked, so the upload artefact matches the submitted version.
