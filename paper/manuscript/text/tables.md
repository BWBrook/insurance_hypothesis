### Table 1
Model parameters and baseline values (or ranges) used in the stochastic multispecies Ricker simulations. Unless otherwise stated, parameters are held fixed across all scenarios.

| Parameter                                 | Value(s) / description                                                                                                                    |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| $r_0$                                     | $1.0$                                                                                                                                     |
| $K_i$                                     | $100$ for all species                                                                                                                     |
| $\alpha_{\mathrm{intra}}$                 | $1.0$                                                                                                                                     |
| $\alpha_{\mathrm{inter}}$                 | $0.3$ (set to $0$ in no-competition controls)                                                                                             |
| $b_i$ (mixed)                             | evenly spaced in $[-0.5, 0.5]$                                                                                                            |
| $b_i$ (positive)                          | evenly spaced in $[0.1, 1.0]$                                                                                                             |
| $b_i$ (positive-matched control)          | $                                                                                                                                         | b_i^{\mathrm{mixed}} | $ (all slopes non-negative; evaluated for $S \in \{4, 8\}$) |
| $b_i$ (mixed–narrow)                      | evenly spaced in $[-0.25, 0.25]$                                                                                                          |
| $\sigma_{\mathrm{env}}$                   | $0$–$1.5$ (specific values given in the scenario grids)                                                                                   |
| $\rho_{\mathrm{env}}$ (requested)         | $-0.5$ to $1.0$                                                                                                                           |
| $\rho_{\mathrm{eff}}$ (used in simulator) | $\rho_{\mathrm{eff}}=\mathrm{clip}\!\left(\rho_{\mathrm{env}},-1/(S-1)+10^{-6},\,1-10^{-6}\right)$ to ensure positive-definite covariance |
| $\phi$                                    | $0$–$0.95$                                                                                                                                |
| $N_{\min}$                                | $10^{-9}$ (abundance floor)                                                                                                               |
| Ricker exponent clipping                  | $x \in [-50, 50]$ before $\exp(x)$                                                                                                        |
| Steps / burn-in                           | $600 / 300$ (main and control grids); $400 / 200$ ($\phi$-sensitivity grids)                                                              |
| Replicates per scenario                   | 150 (mixed main and richness sweep), 100 (positive and positive-matched), 80 (reduced grids and control runs)                             |
