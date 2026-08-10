### Table 1
Core model parameters and simulation grids. All main figures use 1000 replicates per scenario; full-replicate supplementary analyses and lower-replicate controls are listed in the Supporting information.

| Component | Setting | Values / role |
| --- | --- | --- |
| Community model | Discrete-time Ricker competition model | Symmetric density dependence with species-specific environmental term $b_i z_i(t)$; full update equation in Methods |
| Intrinsic growth | $r_0$ | 1.0 |
| Carrying capacity | $K_i$ | 100 for all species |
| Competition | $\alpha_{\mathrm{intra}}$, $\alpha_{\mathrm{inter}}$ | 1.0 and 0.3 in the main grids; no-competition controls set $\alpha_{\mathrm{inter}}=0$ |
| Response slopes | Mixed | $b_i$ evenly spaced in $[-0.5,0.5]$ |
| Response slopes | Aligned positive | $b_i$ evenly spaced in $[0.1,1.0]$ |
| Environmental process | AR(1) driver | $z_t=\phi z_{t-1}+\epsilon_t$ with innovation SD $\sigma_{\mathrm{env}}$ |
| Driver correlation | Requested $\rho_{\mathrm{env}}$ and effective $\rho_{\mathrm{eff}}$ | Equicorrelated innovations; feasibility limits are given in Methods |
| Numerical safeguards | Abundance floor and exponent clipping | $N_{\min}=10^{-9}$; Ricker exponent clipped to $[-50,50]$ before exponentiation |
| Simulation effort | Steps / burn-in / replicates | 600 time steps, 300 burn-in, 1000 replicates per scenario |
| Figure 1 | Environmental-variance contrast | $S=4$; mixed and aligned slopes; $\phi=0.4$; requested $\rho_{\mathrm{env}}=-0.3$ to 1; core $\sigma_{\mathrm{env}}=0$ to 2 plus extension to 4 ($\ge3$ highest stress) |
| Figures 2 and 4 | Richness and CV-synchrony grid | Mixed slopes; $S=2,\ldots,8$; $\phi=0.4$; $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1,1.5,2\}$; requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1\}$ |
| Figure 3 | Imposed-versus-realised synchrony | Mixed and aligned slopes; $S\in\{2,4,8\}$; $\sigma_{\mathrm{env}}=0.5$; $\phi=0.4$; requested $\rho_{\mathrm{env}}=0$ to 1 by 0.1 |
| Figure 5 | Persistence–stationary-variance grid | Mixed slopes; $S\in\{2,4\}$; $\sigma_{\mathrm{env}}=0.5$; $\phi\in\{0,0.7,0.9,0.95\}$; requested $\rho_{\mathrm{env}}=-0.5$ to 1 (eight values) |

### Table S1
Production run inventory for main and production-backed supplementary figures. Rows are replicate-level scenario summaries retrieved locally from validated `deep-server` runs. Short run labels are used here and in Table S2; exact production IDs are listed below the table.

| Run | Design / figures | Grid | Effort |
| --- | --- | --- | --- |
| R1 | Fig. 1 core; mixed and positive slopes; $S=4$ | $\sigma_{\mathrm{env}}$: 0 to 2 (19 values); requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 570 scenarios; 570000 rows |
| R2 | Fig. 1 stress extension; mixed and positive slopes; $S=4$ | $\sigma_{\mathrm{env}}$: 2.25, 2.5, 2.75, 3, 3.5 and 4; requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 180 scenarios; 180000 rows |
| R3 | Figs. 2, 4, S1 and S2; mixed slopes; $S=2$ to 8 | $\sigma_{\mathrm{env}}$: 0, 0.2, 0.5, 1, 1.5 and 2; requested $\rho_{\mathrm{env}}$: 0, 0.25, 0.5, 0.75 and 1; $\phi$: 0.4 | 210 scenarios; 210000 rows |
| R4 | Figs. 3 and S4; mixed and positive slopes; $S=2,4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R5 | Fig. S3; mixed, positive-matched and positive slopes; $S=4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R6 | Fig. 5; mixed slopes; $S=2,4$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: -0.5 to 1 (eight values); $\phi$: 0, 0.7, 0.9 and 0.95 | 64 scenarios; 64000 rows |

Exact production run IDs:

- R1: `fig1-s4-highres-v1`
- R2: `fig1-s4-highsigma-v1`
- R3: `fig2-richness-mixed-v1`
- R4: `fig3-synchrony-v1`
- R5: `figs3-positive-matched-control-v1`
- R6: `fig5-persistence-mixed-v1`

### Table S2
Production floor-occupancy summary. Values are post-burn-in frequencies of abundance at the numerical floor, with scenario means averaged over 1000 replicates. They are stress diagnostics rather than probabilities of irreversible biological extinction. Stress-region rows are retained for transparency but interpreted separately from the low-stress core inference regime.

| Production source | Maximum scenario-mean floor frequency | Maximum replicate floor frequency | Location of maximum scenario mean | Interpretation |
| --- | ---: | ---: | --- | --- |
| Figure 1 core (R1) | 0.0189 | 0.0683 | positive slopes, $S=4$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Upper edge of the core Figure 1 range; monitor as a stress edge |
| Figure 1 high-$\sigma_{\mathrm{env}}$ extension (R2) | 0.1159 | 0.1942 | positive slopes, $S=4$, $\sigma_{\mathrm{env}}=4.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Explicit high-variance stress extension |
| Figure 2/4 richness grid (R3) | 0.0014 | 0.0238 | mixed slopes, $S=8$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.4$ | Main richness and synchrony inferences are not driven by floor occupancy |
| Figure 3 synchrony grid (R4) | 0.0000 | 0.0000 | all scenarios | Mechanism display is floor-free |
| Figure S3 positive-matched control (R5) | 0.0000 | 0.0000 | all scenarios | Focused sign-structure control is floor-free |
| Figure 5 persistence grid (R6) | 0.0492 | 0.3350 | mixed slopes, $S=2$, $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.95$ | Highest-persistence treatment is a stress case |

### Table S3
Lower-replicate control and diagnostic grids retained as robustness checks. These are not the primary source for the main production figures; the positive-matched Figure S3 control has been refreshed as a 1000-replicate production run and is listed in Table S1.

| Diagnostic and question | Model variation | Grid and effort |
| --- | --- | --- |
| No-competition control: is interspecific competition required for the mixed-versus-aligned contrast? | Mixed and positive slopes with $\alpha_{\mathrm{inter}}=0$ | $S\in\{2,4,8\}$; $\sigma_{\mathrm{env}}\in\{0,0.5,1\}$; requested $\rho_{\mathrm{env}}\in\{-0.5,0,0.5,0.9,1\}$; $\phi=0.4$; 80 replicates |
| Mixed-narrow control: does the insurance pattern depend on unusually steep mixed slopes? | `mixed_narrow`, with $b_i$ evenly spaced in $[-0.25,0.25]$ | $S\in\{2,4,8\}$; $\sigma_{\mathrm{env}}\in\{0,0.5,1\}$; requested $\rho_{\mathrm{env}}\in\{-0.5,0,0.5,0.9,1\}$; $\phi=0.4$; 80 replicates |

### Table S4
Variance decomposition for selected mixed-slope production scenarios from the Figure 2/4 richness grid at $\sigma_{\mathrm{env}}=0.5$. The aggregate covariance term is $\operatorname{Var}(N_{\mathrm{tot}})-\sum_i\operatorname{Var}(N_i)$, equivalent to $2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$. Full scenario-level values are written to `analysis/reports/variance_decomposition_fig2_mixed_summary.csv`.

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

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### Table S5
Compact scenario-level association diagnostic for Figure 4. Models use non-deterministic mixed-slope scenario means from the Figure 2/4 production grid ($n=175$). Coefficients are standardised. Because $\mathrm{CV}_{\mathrm{tot}}$ and $\phi_{\mathrm{LdM}}$ both contain $\operatorname{Var}(N_{\mathrm{tot}})$, the diagnostic describes conditional association; it is not an independent mechanistic or mediation test.

| Model | Added synchrony metric(s) | $R^2$ | $\Delta R^2$ | Key standardised coefficient(s) |
| --- | --- | ---: | ---: | --- |
| Grid only | None | 0.857 | 0.000 | $\beta_{\sigma}=0.88$, $\beta_S=-0.28$ |
| + abundance synchrony | $\phi_{\mathrm{LdM}}$ | 0.904 | 0.047 | $\beta_{\phi_{\mathrm{LdM}}}=0.50$ |
| + log-growth synchrony | Mean pairwise realised log-growth correlation | 0.858 | 0.000 | $\beta_{\mathrm{corr}}=0.02$ |
| + both metrics | $\phi_{\mathrm{LdM}}$ and realised log-growth correlation | 0.912 | 0.055 | $\beta_{\phi_{\mathrm{LdM}}}=0.60$, $\beta_{\mathrm{corr}}=-0.18$ |
