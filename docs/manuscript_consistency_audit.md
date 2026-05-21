# Manuscript Consistency Audit

Date: 2026-05-21

Scope: first numerical/prose consistency pass for the Oikos double-blind review manuscript after production-backed figures, tables, and supplementary artefacts were separated.

## Checks Passed

- Significance statement length: 872 characters including spaces after whitespace normalization, below the Oikos 1000-character limit.
- Blinded main PDF and anonymous supplementary PDF scan clean for the main author/institution strings: `Barry`, `Brook`, `University`, `Tasmania`, `UTAS`, `utas`, `ORCID`, `barry.brook`, and `github.com/BWBrook`.
- Blinded main DOCX and anonymous supplementary DOCX now pass `scripts/sanitize_docx_identity.py --check`; local build paths are stripped from invisible image/custom-property metadata.
- Figure caption labels no longer render as duplicated `Fig. 1. Figure 1...` captions.
- Build-facing main and supplementary figure sources now render full informative captions rather than one-line image alt text.
- Main-text references to supplementary detail now use "Supporting information" rather than specific supplementary figure/table labels.
- The stale `[To do in Zotero later]` placeholder no longer renders after the References heading.

## Numerical Spot Checks

All values below were recomputed from the current production summary CSV files under `analysis/reports/`.

| Manuscript claim | Current source value | Status |
| --- | ---: | --- |
| Mixed-vs-aligned difference in mean $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, $S=4$ | 0.1795 | Matches manuscript $\approx 0.18$ |
| Mixed $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, $S=4$ | 0.0839 | Matches manuscript $\approx 0.08$ |
| Positive $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, $S=4$ | 0.2635 | Matches manuscript $\approx 0.26$ |
| Fig. 2 richness means at $\sigma_{\mathrm{env}}=0.5$, $S=2,4,8$ | 0.1481, 0.0836, 0.0615 | Matches manuscript $\approx 0.15$, $\approx 0.08$, $\approx 0.06$ |
| Fig. 3 mixed growth correlations at $\rho_{\mathrm{eff}}\approx1$, $S=2,4,8$ | -0.8093, -0.1625, 0.0824 | Matches manuscript $\approx -0.81$, $\approx -0.16$, $\approx 0.08$ |
| Fig. 4 Pearson $r$ for $\mathrm{CV}_{\mathrm{tot}}$ versus $\phi_{\mathrm{LdM}}$ | 0.8548 | Matches manuscript $\approx 0.85$ |
| Fig. 4 Pearson $r$ for $\mathrm{CV}_{\mathrm{tot}}$ versus growth-rate correlation | 0.5677 | Matches manuscript $\approx 0.57$ |
| Fig. 5 $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, $S=2$, $\phi=0$ and 0.95 | 0.1367, 0.5813 | Matches manuscript $\approx 0.14$ and $\approx 0.58$ |
| Fig. 5 $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, $S=4$, $\phi=0$ and 0.95 | 0.0735, 0.3462 | Matches manuscript $\approx 0.07$ and $\approx 0.35$ |
| Maximum scenario-mean floor frequency in Fig. 2/4 production grid | 0.0014 | Matches manuscript/Table S2 |
| Maximum scenario-mean floor frequency at $\phi=0.9$ | 0.0052 | Matches manuscript $\approx 0.005$ |
| Maximum scenario-mean floor frequency at $\phi=0.95$ | 0.0492 | Matches manuscript/Table S2 |

## Prose Tightening Applied

- The abstract now distinguishes production-backed main contrasts from focused lower-replicate competition/slope-magnitude controls.
- The controls subsection now explicitly calls the no-competition and mixed-narrow grids lower-replicate controls.
- A hard-coded `Wagg et al. 2022` citation string was replaced with the bibliography-backed Wagg et al. 2021 reference.
- A separate editor-facing cover letter source and build profile were added.

## Remaining Review Risks

- Funding and acknowledgements remain Barry-only placeholders on the title page.
- The de-identified review-code package is planned but intentionally not yet built.
- No-competition and mixed-narrow controls remain lower-replicate diagnostics; do not elevate them to central evidence unless refreshed at production scale.
- makedoc submission profiles should be built sequentially, not in parallel, to avoid shared-cache races.
