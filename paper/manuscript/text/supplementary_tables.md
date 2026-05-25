### Table S1
Production run inventory for main and production-backed supplementary figures. Rows are replicate-level scenario summaries retrieved locally from validated `deep-server` runs.

| Run ID | Figures supported | Slope modes | $S$ | $\sigma_{\mathrm{env}}$ | Requested $\rho_{\mathrm{env}}$ | $\phi$ | Scenarios | Replicate rows |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: |
| `fig1-s4-highres-v1` | Fig. 1 core | mixed, positive | 4 | 0.0-2.0, 19 values | -0.3 to 1.0, 15 values | 0.4 | 570 | 570000 |
| `fig1-s4-highsigma-v1` | Fig. 1 stress extension | mixed, positive | 4 | 2.25, 2.5, 2.75, 3.0, 3.5, 4.0 | -0.3 to 1.0, 15 values | 0.4 | 180 | 180000 |
| `fig2-richness-mixed-v1` | Figs. 2, 4, S1, S2 | mixed | 2-8 | 0.0, 0.2, 0.5, 1.0, 1.5, 2.0 | 0.0, 0.25, 0.5, 0.75, 1.0 | 0.4 | 210 | 210000 |
| `fig3-synchrony-v1` | Figs. 3, S4 | mixed, positive | 2, 4, 8 | 0.5 | 0.0-1.0, 11 values | 0.4 | 66 | 66000 |
| `figs3-positive-matched-control-v1` | Fig. S3 | mixed, positive_matched, positive | 4, 8 | 0.5 | 0.0-1.0, 11 values | 0.4 | 66 | 66000 |
| `fig5-persistence-mixed-v1` | Fig. 5 | mixed | 2, 4 | 0.5 | -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 0.9, 1.0 | 0, 0.7, 0.9, 0.95 | 64 | 64000 |

### Table S2
Production floor-occupancy summary. Values are mean extinction/floor frequencies computed from post-burn-in time points, with scenario means averaged over 1000 replicates. Stress-region rows are retained for transparency but interpreted separately from the low-stress core inference regime.

| Production source | Maximum scenario-mean floor frequency | Maximum replicate floor frequency | Location of maximum scenario mean | Interpretation |
| --- | ---: | ---: | --- | --- |
| Figure 1 core (`fig1-s4-highres-v1`) | 0.0189 | 0.0683 | positive slopes, $S=4$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Upper edge of the core Figure 1 range; monitor as a stress edge |
| Figure 1 high-$\sigma_{\mathrm{env}}$ extension (`fig1-s4-highsigma-v1`) | 0.1159 | 0.1942 | positive slopes, $S=4$, $\sigma_{\mathrm{env}}=4.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Explicit high-variance stress extension |
| Figure 2/4 richness grid (`fig2-richness-mixed-v1`) | 0.0014 | 0.0238 | mixed slopes, $S=8$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.4$ | Main richness and synchrony inferences are not driven by floor occupancy |
| Figure 3 synchrony grid (`fig3-synchrony-v1`) | 0.0000 | 0.0000 | all scenarios | Mechanism display is floor-free |
| Figure S3 positive-matched control (`figs3-positive-matched-control-v1`) | 0.0000 | 0.0000 | all scenarios | Focused sign-structure control is floor-free |
| Figure 5 persistence grid (`fig5-persistence-mixed-v1`) | 0.0492 | 0.3350 | mixed slopes, $S=2$, $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.95$ | Highest-persistence treatment is a stress case |

### Table S3
Lower-replicate control and diagnostic grids retained as robustness checks. These are not the primary source for the main production figures; the positive-matched Figure S3 control has been refreshed as a 1000-replicate production run and is listed in Table S1.

| Diagnostic grid | Purpose | Slope modes / interaction setting | Grid scope | Replicates | Artefact / use |
| --- | --- | --- | --- | ---: | --- |
| No-competition controls | Tests whether interspecific competition is required for the mixed-versus-aligned contrast | Mixed and positive slopes with $\alpha_{\mathrm{inter}}=0$ | $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.5,1.0\}$, requested $\rho_{\mathrm{env}}\in\{-0.5,0,0.5,0.9,1.0\}$, $\phi=0.4$ | 80 | Robustness diagnostic summarised in Methods/Discussion |
| Mixed-narrow slope control | Tests whether the insurance pattern depends on unusually steep mixed slopes | `mixed_narrow`, with $b_i$ evenly spaced in $[-0.25,0.25]$ | $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.5,1.0\}$, requested $\rho_{\mathrm{env}}\in\{-0.5,0,0.5,0.9,1.0\}$, $\phi=0.4$ | 80 | Robustness diagnostic summarised in Methods/Discussion |

### Table S4
Variance decomposition for selected mixed-slope production scenarios from the Figure 2/4 richness grid at $\sigma_{\mathrm{env}}=0.5$. The aggregate covariance term is $\operatorname{Var}(N_{\mathrm{tot}})-\sum_i\operatorname{Var}(N_i)$, equivalent to $2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$. Full scenario-level values are written to `analysis/reports/variance_decomposition_fig2_mixed_summary.csv`.

| $S$ | $\rho_{\mathrm{eff}}$ | Mean total biomass | Total variance | Summed species variances | Aggregate covariance term | $\mathrm{CV}_{\mathrm{tot}}$ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.00 | 153.86 | 945.68 | 1272.36 | -326.68 | 0.200 |
| 2 | 0.50 | 153.92 | 549.71 | 1447.90 | -898.19 | 0.152 |
| 2 | 1.00 | 153.85 | 186.61 | 1603.31 | -1416.70 | 0.088 |
| 4 | 0.00 | 210.58 | 505.17 | 1059.81 | -554.64 | 0.107 |
| 4 | 0.50 | 210.56 | 313.50 | 1139.63 | -826.14 | 0.084 |
| 4 | 1.00 | 210.52 | 159.76 | 1209.19 | -1049.43 | 0.060 |
| 8 | 0.00 | 258.07 | 308.60 | 1078.59 | -769.99 | 0.068 |
| 8 | 0.50 | 258.06 | 232.55 | 1118.80 | -886.25 | 0.059 |
| 8 | 1.00 | 258.07 | 240.83 | 1126.80 | -885.97 | 0.060 |

### Table S5
Compact scenario-level association diagnostic for Figure 4. Models use non-deterministic mixed-slope scenario means from the Figure 2/4 production grid ($n=175$). Coefficients are standardised; the diagnostic is intended to check whether synchrony remains informative after accounting for the experimental grid, not to claim formal mediation.

| Model | Predictors added to $\sigma_{\mathrm{env}}$, $S$, $\rho_{\mathrm{eff}}$ | $R^2$ | $\Delta R^2$ vs grid-only model | Key standardised coefficient |
| --- | --- | ---: | ---: | --- |
| Grid covariates | None | 0.857 | 0.000 | $\beta_{\sigma}=0.88$, $\beta_S=-0.28$ |
| Grid + abundance synchrony | $\phi_{\mathrm{LdM}}$ | 0.904 | 0.047 | $\beta_{\phi_{\mathrm{LdM}}}=0.50$ |
| Grid + realised log-growth synchrony | Mean pairwise realised log-growth correlation | 0.858 | 0.000 | $\beta_{\mathrm{corr}}=0.02$ |
| Grid + both synchrony metrics | $\phi_{\mathrm{LdM}}$ and realised log-growth correlation | 0.912 | 0.055 | $\beta_{\phi_{\mathrm{LdM}}}=0.60$, $\beta_{\mathrm{corr}}=-0.18$ |
