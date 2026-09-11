### Table S1
Production run inventory for main and production-backed supplementary figures. Rows are replicate-level scenario summaries from validated, specification-defined runs. Short labels are used here and in Table S2; exact production IDs are listed below the table.

| Run | Design / figures | Grid | Effort |
| --- | --- | --- | --- |
| R1 | Fig. 3 core; mixed and steep aligned responses; $S=4$ | $\sigma_{\mathrm{env}}$: 0 to 2 (19 values); requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 570 scenarios; 570000 rows |
| R2 | Fig. 3 stress extension; mixed and steep aligned responses; $S=4$ | $\sigma_{\mathrm{env}}$: 2.25, 2.5, 2.75, 3, 3.5 and 4; requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 180 scenarios; 180000 rows |
| R3 | Figs. 4, S1 and S2; mixed responses; $S=2$ to 8 | $\sigma_{\mathrm{env}}$: 0, 0.2, 0.5, 1, 1.5 and 2; requested $\rho_{\mathrm{env}}$: 0, 0.25, 0.5, 0.75 and 1; $\phi$: 0.4 | 210 scenarios; 210000 rows |
| R4 | Figs. 2 and S4; mixed and steep aligned responses; $S=2,4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R5 | Figs. 1A and S3; mixed, matched aligned and steep aligned responses; $S=4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R6 | Fig. 5; mixed responses; $S=2,4$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: -0.5 to 1 (eight values); $\phi$: 0, 0.7, 0.9 and 0.95 | 64 scenarios; 64000 rows |
| R7 | Fig. 1B,C; weighted balance and $r_0$ boundary | $S=4$; $\sigma_{\mathrm{env}}=0.5$; requested $\rho_{\mathrm{env}}\in\{0,1\}$; 20 response, abundance-weight, or $r_0$ treatments | 40 scenarios; 40000 rows |

Exact production run IDs:

- R1: `fig1-s4-highres-v1`
- R2: `fig1-s4-highsigma-v1`
- R3: `fig2-richness-mixed-v1`
- R4: `fig3-synchrony-v1`
- R5: `figs3-positive-matched-control-v1`
- R6: `fig5-persistence-mixed-v1`
- R7: `fig4-weighted-balance-r0-v1`

### Table S2
Production floor-occupancy summary. Values are post-burn-in frequencies of abundance at the numerical floor, with scenario means averaged over 1000 replicates. They are stress diagnostics rather than probabilities of irreversible biological extinction. Stress-region rows are retained for transparency but interpreted separately from the low-stress core inference regime.

| Production source | Maximum scenario-mean floor frequency | Maximum replicate floor frequency | Location of maximum scenario mean | Interpretation |
| --- | ---: | ---: | --- | --- |
| Fig. 3 core (R1) | 0.0189 | 0.0683 | steep aligned, $S=4$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Upper edge of the core Fig. 3 range; monitor as a stress edge |
| Fig. 3 high-$\sigma_{\mathrm{env}}$ extension (R2) | 0.1159 | 0.1942 | steep aligned, $S=4$, $\sigma_{\mathrm{env}}=4.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Explicit high-variance stress extension |
| Fig. 4 richness grid (R3) | 0.0014 | 0.0238 | mixed, $S=8$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.4$ | The assembly-sequence pattern is not driven by floor occupancy |
| Fig. 2 synchrony grid (R4) | 0.0000 | 0.0000 | all scenarios | Mechanism display is floor-free |
| Figure 1A/S3 matched aligned control (R5) | 0.0000 | 0.0000 | all scenarios | Magnitude-matched sign control is floor-free |
| Fig. 5 persistence grid (R6) | 0.0492 | 0.3350 | mixed, $S=2$, $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.95$ | Highest-persistence treatment is a stress case |
| Fig. 1 weighted-balance grid (R7) | 0.000016 | 0.0092 | abundance-weight path, $A=0.257$, $\rho_{\mathrm{eff}}\approx1$ | Negligible floor contact at the most uneven positive equilibrium; all other scenarios are floor-free |

### Table S3
Variance decomposition for selected mixed-response production scenarios from the Fig. 4 assembly grid at $\sigma_{\mathrm{env}}=0.5$. The aggregate covariance term is $\operatorname{Var}(N_{\mathrm{tot}})-\sum_i\operatorname{Var}(N_i)$, equivalent to $2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$. Full scenario-level values are written to `analysis/reports/variance_decomposition_fig2_mixed_summary.csv`.

| $S$ | $\rho_{\mathrm{eff}}$ | Mean total abundance | Total variance | Summed species variances | Aggregate covariance term | $\mathrm{CV}_{\mathrm{tot}}$ |
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
