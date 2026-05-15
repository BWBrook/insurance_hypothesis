# Figure captions (v2)

**Figure 1.** Environmental variability destabilises aligned responses more strongly than mixed responses. Production-scale S=4 simulations use 1000 replicates per scenario. **(A)** Heatmap of mean community variability ($\mathrm{CV}_{\mathrm{tot}}$) for aligned positive slopes across innovation SD $\sigma_{\mathrm{env}}$ and effective driver correlation $\rho_{\mathrm{eff}}$. **(B)** Mean $\mathrm{CV}_{\mathrm{tot}}$ across $\rho_{\mathrm{eff}}$ as $\sigma_{\mathrm{env}}$ increases, comparing mixed response directions, aligned response directions, and the aligned-minus-mixed gap. Faint bands show the range across $\rho_{\mathrm{eff}}$. The shaded high-$\sigma_{\mathrm{env}}$ region is treated as a stress extension rather than the core low-stress inference regime.

**Figure 2.** Richness effects on community variability under mixed response directions. Production-scale mixed-slope simulations show scenario means of $\mathrm{CV}_{\mathrm{tot}}$ as a function of species richness $S$, averaged over the shared non-negative imposed-correlation subset ($\rho_{\mathrm{eff}}\ge 0$) for each $\sigma_{\mathrm{env}}$; faint bands show the range across $\rho_{\mathrm{eff}}$. Over the examined richness range ($S=2$-8), $\mathrm{CV}_{\mathrm{tot}}$ declines strongly for all $\sigma_{\mathrm{env}}>0$, while the $\sigma_{\mathrm{env}}=0$ baseline remains near zero.

**Figure 3.** Imposed versus realised synchrony by slope regime at $\sigma_{\mathrm{env}}=0.5$. **(A)** Mixed slopes ($S=2,4,8$): realised growth correlations decline as imposed correlation increases and become negative for low richness at high imposed correlation. **(B)** Positive slopes ($S=4,8$): realised growth correlations increase with imposed correlation and remain strongly positive. Dashed lines indicate equality ($y=x$). **(C)** Difference metric $\Delta\mathrm{corr} = \mathrm{corr}_{\mathrm{realised}} - \rho_{\mathrm{eff}}$, shown as richness-averaged regime means. Mixed slopes become strongly negative at high imposed correlation, whereas positive slopes remain near zero to modestly negative.

**Figure 4.** Community variability versus synchrony metrics in mixed-slope communities. Scenario means (replicate-averaged) are shown by richness. **(A)** $\mathrm{CV}_{\mathrm{tot}}$ versus Loreau-de Mazancourt synchrony $\phi_{\mathrm{LdM}}$. **(B)** $\mathrm{CV}_{\mathrm{tot}}$ versus mean pairwise growth-rate correlation. Lower synchrony and weaker/negative growth correlations correspond to lower community variability.

**Figure 5.** Sensitivity of mixed-slope insurance patterns to environmental persistence. Community variability ($\mathrm{CV}_{\mathrm{tot}}$) versus imposed driver correlation ($\rho_{\mathrm{eff}}$ on x-axis) at $\sigma_{\mathrm{env}}=0.5$, shown for $S=2$ (left) and $S=4$ (right) across $\phi\in\{0,0.7,0.9,0.95\}$. Points show replicate values and lines show scenario means. Legend entries report $\phi$ with corresponding stationary environmental SD, $\sigma_{\mathrm{eff}}=\sigma_{\mathrm{env}}/\sqrt{1-\phi^2}$. Increasing $\phi$ inflates variability, but the mixed-slope richness contrast remains visible.

---

**Figure S1.** Main mixed-grid heatmap summary for community variability. Heatmaps of $\mathrm{CV}_{\mathrm{tot}}$ across imposed driver correlation ($\rho_{\mathrm{eff}}$; rows) and innovation SD ($\sigma_{\mathrm{env}}$; columns) for mixed slopes at $S=2,4,8$. A single shared colour scale and one colourbar are used across panels.

**Figure S2.** Main mixed-grid heatmap summary for realised community synchrony. Heatmaps of $\phi_{\mathrm{LdM}}$ across imposed driver correlation ($\rho_{\mathrm{eff}}$; rows) and innovation SD ($\sigma_{\mathrm{env}}$; columns) for mixed slopes at $S=2,4,8$. A shared colour scale and one colourbar are used across panels.

**Figure S3.** Positive-matched control (magnitude-matched aligned slopes). Comparison of mixed, positive-matched, and positive slope regimes for $\mathrm{CV}_{\mathrm{tot}}$ and mean pairwise growth-rate correlation as functions of imposed correlation ($\rho_{\mathrm{eff}}$), shown for $S=4$ and $S=8$. The positive-matched control isolates response sign structure from slope-magnitude differences: it shifts patterns toward mixed communities relative to positive slopes, but does not remove the mixed-vs-aligned contrast.

**Figure S4.** Approximate species-level CV diagnostic. Approximate $\mathrm{CV}_{\mathrm{sp}}$ (computed from `mean_species_var` and `mean_species_mean`) versus imposed correlation $\rho_{\mathrm{eff}}$ at $\sigma_{\mathrm{env}}=0.5$, shown for mixed and positive slope regimes at $S=4,8$. This panel documents species-level variability alongside community-level variability and synchrony metrics.

---

Figure assets are generated into `analysis/reports/` and copied to `paper/manuscript/figures/` by `analysis/run_all.py`.
