### Table 1
Core model parameters and production simulation grids used for the main figures. The five main figures use production-scale runs with 1000 replicates per scenario; production-backed supplementary runs and remaining lower-replicate controls are listed separately in the Supporting information.

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
