# Critique Resolution Matrix (Manuscript V2)

Date: 2026-02-11

## Colleague 1

| Item | Decision | Resolution |
| --- | --- | --- |
| Figure-caption congruence and panel labeling | Accepted | Implemented in numbered figure set and `manuscript/text/figure_captions_v2.md`; A/B/C/D panel references align with current figures. |
| Shared colour scale where needed | Accepted | Figure 1 A-B and supplementary heatmaps use shared scales as configured in plotting pipeline. |
| Avoid unsupported species-variance mechanism claim | Accepted | Manuscript wording kept synchrony-mediated and does not claim species-level variance constancy without evidence panel. |
| Numerical safeguard disclosure | Accepted | Methods now defines exponent/floor safeguards and reports diagnostic rates plus stress-test caveat. |
| Negative-correlation language robustness | Accepted | Results/captions use `Delta corr` and sign-robust wording instead of geometric above/below phrasing. |
| Richness overgeneralisation risk | Accepted | Claims bounded to examined richness range ($S=2$-8). |
| Foreground mechanism | Accepted | Discussion opens with imposed-vs-realised synchrony decoupling mechanism. |

## Colleague 2

| Item | Decision | Resolution |
| --- | --- | --- |
| Requested vs effective negative correlation mismatch | Accepted | Manuscript Methods explicitly defines `rho_env` (requested) and `rho_eff` (effective clipped), consistent with stored outputs and plotted axes. |
| Phi-sensitivity steps/burn mismatch | Accepted | Methods documents 400/200 for reduced phi sweeps; pipeline commands in README match. |
| Slope-magnitude confound in mixed vs positive contrast | Accepted | Positive-matched control integrated in Methods/Results and surfaced as supplementary Figure S3. |
| ddof/sample variance wording | Accepted | Metrics section now states empirical sample moments over retained time points. |
| Guard-hit diagnostics | Accepted | Numerical/eco checks section includes clipping/floor occupancy diagnostics and interpretation boundary. |

## Colleague 3

| Item | Decision | Resolution |
| --- | --- | --- |
| Explicit `rho_eff` equation and usage | Accepted | Added full clipping expression and implementation convention in Environmental process section. |
| Add positive-matched slope regime | Accepted | Added to slope regimes, simulation design, and control-results interpretation. |
| Add positive-matched grid details | Accepted | Included grid settings and replicate counts in Methods simulation design. |
| Explicit guard diagnostics and floor-based extinction definition | Accepted | Added guard diagnostics paragraph and explicit floor-occupancy extinction definition. |
| Clarify sample-variance convention | Accepted | Metrics section now explicitly uses empirical/sample moments. |

## Notes

- Remaining citation placeholders `[REF]` are intentional and confined to two spots where specific references should be selected during final bibliography styling.
- No new simulation experiments were introduced in this pass; all updates are consistency, documentation, and manuscript/reporting alignment.
