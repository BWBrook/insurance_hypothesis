### Table 1
Core model parameters and production simulation grids used for the main figures. The five main figures use production-scale runs with 1000 replicates per scenario; production-backed supplementary runs and remaining lower-replicate controls are listed separately in Tables S1-S3.

| Component | Setting | Values / role |
| --- | --- | --- |
| Community model | Discrete-time Ricker competition model | $N_i(t+1)=N_i(t)\exp\{r_0+b_i z_i(t)-[N_i(t)+\sum_j\alpha_{ij}N_j(t)]/K_i\}$ |
| Intrinsic growth | $r_0$ | 1.0 |
| Carrying capacity | $K_i$ | 100 for all species |
| Competition | $\alpha_{\mathrm{intra}}$, $\alpha_{\mathrm{inter}}$ | 1.0 and 0.3 in production grids; no-competition controls set $\alpha_{\mathrm{inter}}=0$ |
| Response slopes | Mixed | $b_i$ evenly spaced in $[-0.5,0.5]$ |
| Response slopes | Aligned positive | $b_i$ evenly spaced in $[0.1,1.0]$ |
| Environmental process | AR(1) driver | $z_t=\phi z_{t-1}+\epsilon_t$ with innovation SD $\sigma_{\mathrm{env}}$ |
| Driver correlation | Requested $\rho_{\mathrm{env}}$ and effective $\rho_{\mathrm{eff}}$ | Equicorrelated innovations; requested $\rho_{\mathrm{env}}$ is clipped to $\rho_{\mathrm{eff}}\in[-1/(S-1)+10^{-6},1-10^{-6}]$ when required for positive-definite covariance |
| Numerical safeguards | Abundance floor and exponent clipping | $N_{\min}=10^{-9}$; Ricker exponent clipped to $[-50,50]$ before exponentiation |
| Production effort | Steps / burn-in / replicates | 600 time steps, 300 burn-in, 1000 replicates per scenario |
| Figure 1 | Environmental-variance contrast | $S=4$ mixed and aligned-positive slopes, $\phi=0.4$, requested $\rho_{\mathrm{env}}=-0.3$ to 1.0, core $\sigma_{\mathrm{env}}=0$ to 2.0 plus a labelled stress extension to 4.0 |
| Figures 2 and 4 | Richness and CV-synchrony production grid | Mixed slopes, $S=2,\ldots,8$, $\phi=0.4$, $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1.0,1.5,2.0\}$, requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1.0\}$ |
| Figure 3 | Imposed-versus-realised synchrony grid | Mixed and aligned-positive slopes, $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, requested $\rho_{\mathrm{env}}=0$ to 1.0 in increments of 0.1 |
| Figure 5 | Persistence-sensitivity grid | Mixed slopes, $S\in\{2,4\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi\in\{0,0.7,0.9,0.95\}$, requested $\rho_{\mathrm{env}}\in\{-0.5,-0.25,0,0.25,0.5,0.75,0.9,1.0\}$ |

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
