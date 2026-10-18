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
