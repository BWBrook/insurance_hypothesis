### Table 1
Core model parameters and simulation grids. Every scenario uses 1000 replicate trajectories of 600 steps, with 300 steps discarded as burn-in, except the long-window check of the Fig. 3 reversals (500 replicates of 6000 steps, 3000 discarded).

| Component | Setting | Values / role |
| --- | --- | --- |
| Community model | Discrete-time Ricker competition model | Symmetric density dependence with species-specific environmental term $b_i z_i(t)$; full update equation in Methods |
| Intrinsic growth | $r_0$ | 1.0 except Fig. 1C sensitivity: 0.25, 0.5, 1.0 and 1.5 |
| Density-dependence scale | $K_i$ | 100 except Fig. 1B abundance-weight path: constant-sum vectors from $(100,100,100,100)$ to $(67,89,111,133)$ |
| Competition | $\alpha_{\mathrm{intra}}$, $\alpha_{\mathrm{inter}}$ | 1.0 throughout; $\alpha_{\mathrm{inter}}=0.3$ except Fig. 3: 0.1, 0.3 and 0.6 |
| Response treatment | Mixed | $b_i$ evenly spaced in $[-0.5,0.5]$; slopes sum to zero |
| Response treatment | Matched aligned | $\lvert b_i^{\mathrm{mixed}}\rvert$: same magnitudes as mixed, all nonnegative; Fig. 1B also rotates continuously from the mixed to the matched aligned vector at constant norm |
| Response treatment | Steep aligned | $b_i$ evenly spaced in $[0.1,1.0]$; changes magnitude as well as direction |
| Environmental process | AR(1) exposure | $z_t=\phi z_{t-1}+\epsilon_t$ with innovation SD $\sigma_{\mathrm{env}}$ |
| Exposure correlation | Requested $\rho_{\mathrm{env}}$ and effective $\rho_{\mathrm{eff}}$ | Equicorrelated innovations; requested values outside the feasible interval are clipped at either boundary; bounds and affected treatments are given in Methods |
| Numerical safeguards | Abundance floor and exponent clipping | $N_{\min}=10^{-9}$; Ricker exponent clipped to $[-50,50]$ before exponentiation |
| Figure 1 | Sign contrast and weighted-balance boundary | Panel A: mixed versus matched aligned at $S=4,8$ and requested $\rho_{\mathrm{env}}=0$ to 1; panels B,C: $S=4$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}\in\{0,1\}$ |
| Figure 2 | Shared-exposure benefit across fluctuation size | Nine-treatment response rotation (mixed to matched aligned) and five-treatment unequal-$K_i$ path; $S=4$; $\phi=0.4$; $\sigma_{\mathrm{env}}\in\{0.1,0.2,0.3,0.5,0.7,1,1.3\}$; requested $\rho_{\mathrm{env}}\in\{0,1\}$ |
| Figure 3 | Prespecified second-order test and balanced-community reversals | Mixed slopes, equal $K$; $S\in\{2,4,8\}$; $\alpha_{\mathrm{inter}}\in\{0.1,0.3,0.6\}$; $\phi\in\{0,0.4,0.8\}$; $\sigma_{\mathrm{env}}\in\{0.1,0.2,0.5,1\}$; requested $\rho_{\mathrm{env}}\in\{0,1\}$; five reversal settings repeated in the long-window check |
| Supporting analyses | Realised synchrony, environmental-variance contrast, richness assembly sequence and fixed-innovation gradient | Grids and treatments given in the Supporting information |

### Table S1
Production run inventory for main and production-backed supplementary figures. Rows are replicate-level scenario summaries from validated, specification-defined runs. R1–R11 use 1000 replicates of 600 steps per scenario; R12–R16 use 500 replicates of 6000 steps. Short labels are used here and in Table S2; exact production IDs are listed below the table.

| Run | Design / figures | Grid | Effort |
| --- | --- | --- | --- |
| R1 | Fig. S6 core and Fig. 2 replication layer; mixed and steep aligned responses; $S=4$ | $\sigma_{\mathrm{env}}$: 0 to 2 (19 values); requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 570 scenarios; 570000 rows |
| R2 | Fig. S6 stress extension; mixed and steep aligned responses; $S=4$ | $\sigma_{\mathrm{env}}$: 2.25, 2.5, 2.75, 3, 3.5 and 4; requested $\rho_{\mathrm{env}}$: -0.3 to 1 (15 values); $\phi$: 0.4 | 180 scenarios; 180000 rows |
| R3 | Figs. S7, S1 and S2; mixed responses; $S=2$ to 8 | $\sigma_{\mathrm{env}}$: 0, 0.2, 0.5, 1, 1.5 and 2; requested $\rho_{\mathrm{env}}$: 0, 0.25, 0.5, 0.75 and 1; $\phi$: 0.4 | 210 scenarios; 210000 rows |
| R4 | Figs. S5 and S4; mixed and steep aligned responses; $S=2,4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R5 | Figs. 1A and S3; mixed, matched aligned and steep aligned responses; $S=4,8$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: 0 to 1 (11 values); $\phi$: 0.4 | 66 scenarios; 66000 rows |
| R6 | Fig. S8; mixed responses; $S=2,4$ | $\sigma_{\mathrm{env}}$: 0.5; requested $\rho_{\mathrm{env}}$: -0.5 to 1 (eight values); $\phi$: 0, 0.7, 0.9 and 0.95 | 64 scenarios; 64000 rows |
| R7 | Fig. 1B,C; weighted balance and $r_0$ boundary | $S=4$; $\sigma_{\mathrm{env}}=0.5$; requested $\rho_{\mathrm{env}}\in\{0,1\}$; 20 response, abundance-weight, or $r_0$ treatments | 40 scenarios; 40000 rows |
| R8 | Figs. 2 and S9; boundary across fluctuation size | $S=4$; $\sigma_{\mathrm{env}}$: 0.1, 0.2, 0.3, 0.5, 0.7, 1 and 1.3; requested $\rho_{\mathrm{env}}\in\{0,1\}$; 14 rotation and unequal-$K_i$ treatments | 196 scenarios; 196000 rows |
| R9–R11 | Fig. 3 and Table S4; balanced mixed slopes; $\alpha_{\mathrm{inter}}$ 0.1, 0.3 and 0.6 respectively | $S\in\{2,4,8\}$; $\phi\in\{0,0.4,0.8\}$; $\sigma_{\mathrm{env}}\in\{0.1,0.2,0.5,1\}$; requested $\rho_{\mathrm{env}}\in\{0,1\}$ | 72 scenarios; 72000 rows each |
| R12–R16 | Table S5; long-window check of the five balanced-community reversals | $S=8$; one reversal setting each; requested $\rho_{\mathrm{env}}\in\{0,1\}$; 6000 steps with 3000 burn-in | 2 scenarios; 1000 rows each |

Exact production run IDs:

- R1: `fig1-s4-highres-v1`
- R2: `fig1-s4-highsigma-v1`
- R3: `fig2-richness-mixed-v1`
- R4: `fig3-synchrony-v1`
- R5: `figs3-positive-matched-control-v1`
- R6: `fig5-persistence-mixed-v1`
- R7: `fig4-weighted-balance-r0-v1`
- R8: `boundary-by-sigma-v1`
- R9–R11: `sigma-mechanism-alpha010-v1`, `sigma-mechanism-alpha030-v1`, `sigma-mechanism-alpha060-v1`
- R12: `longwindow-reversal-a060-phi040-sig050-v1`
- R13: `longwindow-reversal-a030-phi000-sig100-v1`
- R14: `longwindow-reversal-a030-phi040-sig100-v1`
- R15: `longwindow-reversal-a060-phi000-sig100-v1`
- R16: `longwindow-reversal-a060-phi080-sig020-v1`

### Table S2
Production floor-occupancy summary. Values are post-burn-in frequencies of abundance at the numerical floor, with scenario means averaged over 1000 replicates. They are stress diagnostics rather than probabilities of irreversible biological extinction. Stress-region rows are retained for transparency but interpreted separately from the low-stress core inference regime.

| Production source | Maximum scenario-mean floor frequency | Maximum replicate floor frequency | Location of maximum scenario mean | Interpretation |
| --- | ---: | ---: | --- | --- |
| Fig. S6 core (R1) | 0.0189 | 0.0683 | steep aligned, $S=4$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Upper edge of the core Fig. S6 range; monitor as a stress edge |
| Fig. S6 high-$\sigma_{\mathrm{env}}$ extension (R2) | 0.1159 | 0.1942 | steep aligned, $S=4$, $\sigma_{\mathrm{env}}=4.0$, $\rho_{\mathrm{eff}}=-0.3$, $\phi=0.4$ | Explicit high-variance stress extension |
| Fig. S7 richness grid (R3) | 0.0014 | 0.0238 | mixed, $S=8$, $\sigma_{\mathrm{env}}=2.0$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.4$ | The assembly-sequence pattern is not driven by floor occupancy |
| Fig. S5 synchrony grid (R4) | 0.0000 | 0.0000 | all scenarios | Mechanism display is floor-free |
| Fig. 1A/S3 matched aligned control (R5) | 0.0000 | 0.0000 | all scenarios | Magnitude-matched sign control is floor-free |
| Fig. S8 persistence grid (R6) | 0.0492 | 0.3350 | mixed, $S=2$, $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}\approx1$, $\phi=0.95$ | Highest-persistence treatment is a stress case |
| Fig. 1 weighted-balance grid (R7) | 0.000016 | 0.0092 | abundance-weight path, $A=0.257$, $\rho_{\mathrm{eff}}\approx1$ | Negligible floor contact at the most uneven positive equilibrium; all other scenarios are floor-free |
| Fig. 2 boundary-by-$\sigma_{\mathrm{env}}$ grid (R8) | 0.0046 | 0.0483 | unequal-$K_i$ path, $A=0.257$, $\sigma_{\mathrm{env}}=1.3$, $\rho_{\mathrm{eff}}\approx1$ | Contact only in uneven unequal-$K_i$ treatments from $\sigma_{\mathrm{env}}=0.5$ and on the rotation path at 1.3; the balanced and matched aligned endpoints are floor-free |
| Fig. 3 mechanism grid, $\alpha_{\mathrm{inter}}=0.1$ (R9) | 0.0007 | 0.0250 | $S=8$, $\phi=0.8$, $\sigma_{\mathrm{env}}=1$, $\rho_{\mathrm{eff}}\approx1$ | Contact only at $\phi=0.8$, $\sigma_{\mathrm{env}}=1$ |
| Fig. 3 mechanism grid, $\alpha_{\mathrm{inter}}=0.3$ (R10) | 0.0105 | 0.0967 | $S=8$, $\phi=0.8$, $\sigma_{\mathrm{env}}=1$, $\rho_{\mathrm{eff}}\approx1$ | Contact at $\phi=0.8$ with $\sigma_{\mathrm{env}}\ge0.5$; all small-fluctuation test cells are floor-free |
| Fig. 3 mechanism grid, $\alpha_{\mathrm{inter}}=0.6$ (R11) | 0.0343 | 0.2017 | $S=2$, $\phi=0.8$, $\sigma_{\mathrm{env}}=1$, $\rho_{\mathrm{eff}}\approx1$ | Contact at $\sigma_{\mathrm{env}}\ge0.5$ in persistent settings; reversal cells counted only where floor-free |
| Fig. 3 long-window checks (R12–R16) | <0.00001 | 0.0003 | $S=8$, $\alpha_{\mathrm{inter}}=0.6$, $\phi=0.8$, $\sigma_{\mathrm{env}}=0.2$, $\rho_{\mathrm{eff}}\approx1$ | Four of five settings floor-free; one replicate touched the floor in the fifth |

### Table S3
Variance decomposition for selected mixed-response production scenarios from the Fig. S7 assembly grid at $\sigma_{\mathrm{env}}=0.5$. The aggregate covariance term is $\operatorname{Var}(N_{\mathrm{tot}})-\sum_i\operatorname{Var}(N_i)$, equivalent to $2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$. Full scenario-level values are written to `analysis/reports/variance_decomposition_fig2_mixed_summary.csv`.

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

### Table S4
Prespecified test of the second-order small-fluctuation prediction for perfectly balanced communities (mixed slopes, equal $K$, $r_0=1$). The coefficient $c=\sum_i b_i^2/[(1-\lambda_d^2)(1-\lambda_d\phi)^2]$ predicts the ratio of mean $\mathrm{CV}_{\mathrm{tot}}^2$ under near-perfect versus independent exposure as $c\,\sigma_{\mathrm{env}}^2$. Predictions were written before the simulations ran. The small-fluctuation regime contains settings with predicted ratio below 0.1 at $\sigma_{\mathrm{env}}=0.1$. Both recorded acceptance definitions (observed ratio within 20% of prediction; ratio of $R(0.2)$ to $R(0.1)$ between 3 and 5, applied to all 23 regime settings or only where the predicted $R(0.2)<0.2$) are met by all 23. The marked setting repeats the calibration case with independent seeds.

| $\alpha_{\mathrm{inter}}$ | $S$ | $\phi$ | $\lambda_d$ | $c$ | Predicted $R(0.1)$ | Simulated $R(0.1)$ | Simulated/predicted | $R(0.2)/R(0.1)$ | Small-fluctuation regime |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0.1 | 2 | 0 | 0.182 | 0.517 | 0.0052 | 0.0051 | 0.988 | 3.92 | yes |
| 0.1 | 2 | 0.4 | 0.182 | 0.601 | 0.0060 | 0.0060 | 1.005 | 3.86 | yes |
| 0.1 | 2 | 0.8 | 0.182 | 0.708 | 0.0071 | 0.0072 | 1.015 | 3.86 | yes |
| 0.1 | 4 | 0 | 0.308 | 0.614 | 0.0061 | 0.0061 | 0.992 | 3.96 | yes |
| 0.1 | 4 | 0.4 | 0.308 | 0.798 | 0.0080 | 0.0080 | 1.008 | 3.92 | yes |
| 0.1 | 4 | 0.8 | 0.308 | 1.080 | 0.0108 | 0.0109 | 1.010 | 3.88 | yes |
| 0.1 | 8 | 0 | 0.471 | 1.101 | 0.0110 | 0.0110 | 0.996 | 3.92 | yes |
| 0.1 | 8 | 0.4 | 0.471 | 1.671 | 0.0167 | 0.0165 | 0.988 | 3.94 | yes |
| 0.1 | 8 | 0.8 | 0.471 | 2.832 | 0.0283 | 0.0286 | 1.011 | 3.77 | yes |
| 0.3 | 2 | 0 | 0.462 | 0.635 | 0.0064 | 0.0064 | 1.014 | 3.88 | yes |
| 0.3 | 2 | 0.4 | 0.462 | 0.956 | 0.0096 | 0.0094 | 0.982 | 3.98 | yes |
| 0.3 | 2 | 0.8 | 0.462 | 1.597 | 0.0160 | 0.0162 | 1.011 | 3.89 | yes |
| 0.3 | 4 | 0 | 0.632 | 0.924 | 0.0092 | 0.0092 | 0.996 | 3.93 | yes |
| 0.3 | 4 | 0.4 | 0.632 | 1.655 | 0.0165 | 0.0165 | 1.000 | 3.82 | yes (calibration repeat) |
| 0.3 | 4 | 0.8 | 0.632 | 3.776 | 0.0378 | 0.0372 | 0.985 | 3.69 | yes |
| 0.3 | 8 | 0 | 0.774 | 2.140 | 0.0214 | 0.0214 | 1.002 | 3.86 | yes |
| 0.3 | 8 | 0.4 | 0.774 | 4.490 | 0.0449 | 0.0446 | 0.992 | 3.78 | yes |
| 0.3 | 8 | 0.8 | 0.774 | 14.766 | 0.1477 | 0.1431 | 0.969 | 3.38 | no |
| 0.6 | 2 | 0 | 0.750 | 1.143 | 0.0114 | 0.0114 | 0.997 | 3.84 | yes |
| 0.6 | 2 | 0.4 | 0.750 | 2.332 | 0.0233 | 0.0229 | 0.983 | 3.75 | yes |
| 0.6 | 2 | 0.8 | 0.750 | 7.143 | 0.0714 | 0.0706 | 0.989 | 3.50 | yes |
| 0.6 | 4 | 0 | 0.857 | 2.094 | 0.0209 | 0.0206 | 0.985 | 3.87 | yes |
| 0.6 | 4 | 0.4 | 0.857 | 4.849 | 0.0485 | 0.0468 | 0.965 | 3.70 | yes |
| 0.6 | 4 | 0.8 | 0.857 | 21.200 | 0.2120 | 0.1927 | 0.909 | 2.89 | no |
| 0.6 | 8 | 0 | 0.923 | 5.794 | 0.0579 | 0.0567 | 0.978 | 3.76 | yes |
| 0.6 | 8 | 0.4 | 0.923 | 14.563 | 0.1456 | 0.1413 | 0.970 | 3.36 | no |
| 0.6 | 8 | 0.8 | 0.923 | 84.709 | 0.8471 | 0.6710 | 0.792 | 2.18 | no |

### Table S5
Balanced-community reversals and their robustness checks. Each row is a setting in which the ratio of mean $\mathrm{CV}_{\mathrm{tot}}^2$ under near-perfect versus independent exposure exceeded one, with its 95% Monte Carlo interval and without production floor contact, in the Fig. 3 grids ($S=8$, mixed slopes, equal $K$, $r_0=1$). The long-window check repeated each setting with independent seeds, 500 replicates of 6000 steps and 3000 discarded. A separate guard diagnostic (200 full 600-step and 100 full 6000-step trajectories per exposure condition, independent seeds) recorded no exponent clipping and no floor contact in any of these settings; it describes guard activity in these parameter settings, not in every production replicate.

| $\alpha_{\mathrm{inter}}$ | $\phi$ | $\sigma_{\mathrm{env}}$ | $c$ | Ratio, 600 steps (95% interval) | Ratio, 6000 steps (95% interval) | Long-window maximum replicate floor frequency |
| ---: | ---: | ---: | ---: | --- | --- | ---: |
| 0.3 | 0 | 1 | 2.14 | 1.187 (1.168–1.207) | 1.187 (1.178–1.196) | 0.0000 |
| 0.3 | 0.4 | 1 | 4.49 | 1.548 (1.521–1.575) | 1.560 (1.547–1.572) | 0.0000 |
| 0.6 | 0 | 1 | 5.79 | 1.649 (1.612–1.687) | 1.654 (1.638–1.670) | 0.0000 |
| 0.6 | 0.4 | 0.5 | 14.56 | 1.458 (1.429–1.488) | 1.457 (1.444–1.470) | 0.0000 |
| 0.6 | 0.8 | 0.2 | 84.71 | 1.465 (1.430–1.501) | 1.453 (1.436–1.469) | 0.0003 |
