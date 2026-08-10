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
