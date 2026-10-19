# Supplementary Information

## Shared environments can destabilise communities with balanced opposing responses

This supplementary information file contains the linearised covariance derivation, the second-order calculation and its two prespecified tests, implementation checks, production run inventory, numerical stress summaries, a selected variance decomposition, and supplementary figures. It is anonymised for double-blind review.

## Linearised forcing and abundance variability

Let $\mathbf x_t=\mathbf N_t-\mathbf N^\ast$. To first order near a positive deterministic equilibrium, the unguarded recurrence is
\[
\mathbf x_{t+1}=J\mathbf x_t+D\mathbf z_t,\qquad
J=I-\operatorname{diag}(N_i^\ast/K_i)C_\alpha,\qquad
D=\operatorname{diag}(N_i^\ast b_i).
\]
This separates environmental input from its transmission through population feedback [@ives1999StabilityVariabilityCompetitive]. For equal $K_i$ and the symmetric competition matrix, $\mathbf 1^\mathsf{T}J=(1-r_0)\mathbf 1^\mathsf{T}$. Hence $X_t=\mathbf 1^\mathsf{T}\mathbf x_t$ follows $X_{t+1}=\lambda_cX_t+F_t$, where $\lambda_c=1-r_0$ and $F_t=\mathbf 1^\mathsf{T}D\mathbf z_t$.

Because $F_t$ is AR(1) with coefficient $\phi$, its stationary covariance with $X_t$ is
\[
\operatorname{Cov}(X_t,F_t)=\frac{\phi\operatorname{Var}(F)}{1-\lambda_c\phi}.
\]
Taking variances in the scalar abundance recurrence gives
\[
\operatorname{Var}(X)=\operatorname{Var}(F)
\frac{1+\lambda_c\phi}{(1-\lambda_c^2)(1-\lambda_c\phi)},
\]
provided the linearised equilibrium is stable and $|\phi|<1$. At fixed population parameters and $\phi$, the multiplier is independent of exposure correlation. Ratios of stationary total-abundance variances therefore equal ratios of forcing variances in the linearised equal-$K$ system. Dividing by the fixed squared equilibrium total gives the same ratio for the corresponding linear approximation to squared community CV. This does not make the ratio exact for finite nonlinear trajectories.

For unequal $K_i$, the same total-abundance projection generally does not close on a scalar recurrence. The equilibrium weights and $J$ both change along the abundance-weight path, so the forcing criterion alone need not give the stationary abundance-variance ratio. A full linear calculation can instead use the joint population–environment state with transition matrix
\[
M=\begin{pmatrix}J&D\\0&\phi I\end{pmatrix}
\]
and innovation covariance with $\Sigma$ in its environment block and zeros elsewhere. Its stationary covariance $P$ satisfies $P=MPM^\mathsf{T}+Q$. The upper-left block gives population covariance. Figure 1 retains the instantaneous forcing benchmark to show its agreement and departures from the nonlinear results.

Finally, the unguarded model constrains stationary means. Taking expectations of log growth at a positive stationary distribution with finite abundance and log-abundance expectations, and using $\mathbb E[\mathbf z]=0$, gives $C_\alpha\mathbb E[\mathbf N]=r_0\mathbf K$. Thus the stationary mean equals the deterministic equilibrium under these conditions. Finite trajectories and active numerical guards can break this correspondence; nonlinearity alone is not evidence of a shifted mean.

## Nonlinear contributions when first-order forcing cancels

For equal $K$, let $N_i=n+x_i$, where $n$ is the common equilibrium abundance, and define $u_i=b_i z_i-(C_\alpha\mathbf x)_i/K$. Expanding the unguarded Ricker update jointly in abundance and environmental departures gives
\[
x_i'=x_i+n u_i+x_i u_i+\tfrac12 n u_i^2+O(3).
\]
The aggregate second-order departure therefore receives both abundance–growth cross terms and quadratic growth terms. Since $x_i^{(1)\prime}=x_i^{(1)}+n u_i^{(1)}$ at first order, their sum can be written as
\[
X_{t+1}^{(2)}=\lambda_c X_t^{(2)}+
\frac{\lVert\mathbf x_{t+1}^{(1)}\rVert^2-\lVert\mathbf x_t^{(1)}\rVert^2}{2n}.
\]
Superscripts denote expansion order. Changes in the squared magnitude of species-level deviations can thus contribute to total-abundance variability even when their first-order sum cancels. The input has zero expectation under stationarity with finite second moments, but can have nonzero variance. This is a local route for nonlinear variability, not a quantitative decomposition of the simulated ratios or an explanation of their exact crossing. The numerical results use the full recurrence, not this truncated expansion.

### Leading-order residual of a perfectly balanced community

The identity becomes quantitative for a perfectly balanced community under shared exposure. Take equal $K$, $\alpha_{\mathrm{intra}}=1$, $r_0=1$ and slopes with $\sum_i b_i=0$, and let every species experience the same exposure $z_t$, an AR(1) process with coefficient $\phi$ and stationary variance $\sigma_z^2=\sigma_{\mathrm{env}}^2/(1-\phi^2)$. Because $\mathbf b$ is orthogonal to $\mathbf 1$, and every such vector is an eigenvector of the equal-$K$ Jacobian with eigenvalue $\lambda_d$, the first-order departures stay in the contrast subspace: $\mathbf x^{(1)}_t=n\,\mathbf b\,y_t$ with $y_{t+1}=\lambda_d y_t+z_t$, and $X^{(1)}_t=0$. Here $y$ is a stationary Gaussian AR(2) process with roots $\lambda_d$ and $\phi$. Substituting into the identity, with $\lambda_c=0$, gives
\[
X^{(2)}_{t+1}=\tfrac12 n\textstyle\sum_i b_i^2\,(y_{t+1}^2-y_t^2).
\]
For Gaussian $y$ with variance $v$ and lag-one autocorrelation $\rho_1$, $\operatorname{Var}(y_{t+1}^2-y_t^2)=4v^2(1-\rho_1^2)$. Dividing by the first-order variance of total abundance under independent exposures, $n^2\sum_i b_i^2\,\sigma_z^2$, gives the leading term of the shared-to-independent population-variance ratio, equivalently the ratio of population squared CVs at this order:
\[
R\approx c\,\sigma_{\mathrm{env}}^2,\qquad
c=\frac{\sum_i b_i^2}{(1-\lambda_d^2)(1-\lambda_d\phi)^2}.
\]
The ratio grows with the variance of per-capita environmental shocks, $\sigma_z^2\sum_i b_i^2$. It also grows as $\lambda_d$ approaches one, which happens with more species or stronger interspecific relative to intraspecific competition, and with environmental autocorrelation. For the focal community ($S=4$, $\alpha_{\mathrm{inter}}=0.3$, $\phi=0.4$), $c=1.65$. Applying the same calculation to the 300-step finite-window estimand changes $c$ by 0.8%.

The coefficient is a small-fluctuation result. It predicts the onset of the residual, not its magnitude once $R$ is no longer small: at $\sigma_{\mathrm{env}}=0.5$ it gives 0.41 against a simulated 0.32 in the focal community. For other values of $r_0$, the common mode has its own memory and the closed-form coefficient above no longer applies. Figure 1C reports those simulated sign contrasts without attributing their dependence on $r_0$ to any single dynamical feature. The calculation says nothing about aligned or partially balanced compositions, where first-order terms do not vanish.

### Finite observation window

For a stationary series with autocorrelation $q_h$, the expected sample variance over $L$ observations, with divisor $L-1$, is its population variance multiplied by
\[
B_L(q)=1-\frac{2}{L(L-1)}\sum_{h=1}^{L-1}(L-h)q_h.
\]
At $r_0=1$, the first-order independent-exposure total has autocorrelation $\phi^h$. Write $\eta_h$ for the autocorrelation of $y_t$. It satisfies $\eta_0=1$, $\eta_1=(\lambda_d+\phi)/(1+\lambda_d\phi)$ and
\[
\eta_h=(\lambda_d+\phi)\eta_{h-1}-\lambda_d\phi \eta_{h-2}\quad(h\ge2).
\]
Gaussian fourth moments give the autocorrelation of $\Delta y_t^2=y_{t+1}^2-y_t^2$ as
\[
q_h^{\Delta}=\frac{2\eta_h^2-\eta_{h-1}^2-\eta_{h+1}^2}{2(1-\eta_1^2)},\qquad \eta_{-h}=\eta_h.
\]
The leading coefficient for the ratio of mean sampled squared CVs is therefore $c_L=c\,B_L(q^{\Delta})/B_L(\phi^h)$. At the focal settings and $L=300$, the two factors are 1.003310 and 0.995565, giving $c_{300}=1.667519$. Random sample means affect higher-order terms. This calculation assumes stationarity, inactive guards and exactly shared exposure; the implemented correlation cap leaves a first-order ratio of $10^{-6}$.

### The second-order driver in simulated trajectories

The identity can be checked directly in long trajectories of the full recurrence. For two balanced communities ($S=4$, $\alpha_{\mathrm{inter}}=0.3$, $\phi=0.4$; $S=8$, $\alpha_{\mathrm{inter}}=0.6$, $\phi=0.4$), each at $\sigma_{\mathrm{env}}=0.1$ and 0.5, 20 trajectories of 3300 steps were simulated under each exposure condition with fixed seeds, and the first 300 steps were discarded. The total departure $X_{t+1}$ was compared with the driver $(\lVert\mathbf x_{t+1}\rVert^2-\lVert\mathbf x_t\rVert^2)/2n$, computed from the full simulated species departures rather than their first-order parts. Under shared exposure the mean correlations were 1.00 and 0.93 (range 0.91–0.94) in the four-species community, and 1.00 and 0.77 (0.74–0.80) in the eight-species community, at $\sigma_{\mathrm{env}}=0.1$ and 0.5 respectively. Mean regression slopes of $X_{t+1}$ on the driver were 0.99 at $\sigma_{\mathrm{env}}=0.1$, and 0.73 and 0.50 at 0.5, consistent with the leading-order over-prediction at larger fluctuations. The standard deviation of the driver under shared exposure exceeded that under independent exposure, trajectory by trajectory, by mean factors of 1.74 (1.63–1.82) and 2.12 (2.00–2.32) at $\sigma_{\mathrm{env}}=0.1$, and 1.33 (1.19–1.50) and 1.15 (0.96–1.44) at 0.5. At $\sigma_{\mathrm{env}}=0.1$, the independent-exposure total followed the uncancelled first-order input instead (mean correlations with the driver 0.11 and 0.26). The displayed trajectory in Fig. 3A, B uses a separate seed. Values are written to `fig7_mechanism_trajectory_summary.csv`.

## Prespecified test of the small-fluctuation prediction

Before simulating, the coefficient $c$ was computed for 27 perfectly balanced communities crossing $\alpha_{\mathrm{inter}}\in\{0.1,0.3,0.6\}$, $S\in\{2,4,8\}$ and $\phi\in\{0,0.4,0.8\}$ (Table S4). The predictions are retained, with their hash and timeline, in `analysis/prespecified/` of the reproducibility package. The specification files recorded the acceptance criteria before the first simulation shard was written. The criteria were posted to the project correspondence 18 seconds later, but that post omitted one eligibility restriction, so both versions were evaluated. Twenty-three settings fall in the small-fluctuation regime, with a predicted ratio at $\sigma_{\mathrm{env}}=0.1$ below 0.1. One of them repeats the calibration setting with independent seeds; the other 22 are new combinations. In all 23, the simulated ratio at $\sigma_{\mathrm{env}}=0.1$ lies within 4% of the prediction (simulated/predicted 0.965–1.015, across a 14-fold range of $c$). Doubling $\sigma_{\mathrm{env}}$ multiplied the ratio by 3.50–3.98, close to the predicted factor of four. Both recorded definitions are therefore met in every eligible setting. In the four settings outside the regime ($c$ from 14.6 to 84.7), the leading-order term over-predicts by 3–21%, as expected when $R$ is not small.

## Boundary across fluctuation sizes

The Fig. 1B rotation and unequal-$K_i$ paths were repeated at seven values of $\sigma_{\mathrm{env}}$ with independent seeds (Fig. S9). At $\sigma_{\mathrm{env}}=0.1$, the simulated ratios follow the first-order benchmark along the whole rotation path, generally within about 1%. As fluctuations grow, the curves flatten towards a ratio of one, and compositions near the first-order boundary change side. The rotation composition with $A=0.247$, just below the boundary, gives a ratio of 0.986 (95% Monte Carlo interval 0.978–0.995) at $\sigma_{\mathrm{env}}=0.1$ and 1.056 (1.034–1.077) at 0.7, with no retained floor contact at either. Interpolated crossings (Fig. S9C) summarise the same shift but are not estimated thresholds: the tested compositions are coarsely spaced, the unequal-$K_i$ path has floor contact in its most uneven treatments from $\sigma_{\mathrm{env}}=0.5$, and at $\sigma_{\mathrm{env}}=1.3$ the bracketing rotation-path points include an interval spanning one. The balanced and matched aligned endpoints are floor-free at every $\sigma_{\mathrm{env}}$. Under independent exposures the two treatments have the same forcing distribution; their simulated matched/balanced ratios range from 0.984 to 1.003. The shared-exposure comparison is computed directly from the matched and balanced endpoints' own mean squared CVs, without assuming identical simulated baselines.

## Balanced-community reversals and their robustness

In five of the 108 setting-by-$\sigma_{\mathrm{env}}$ cells of the Fig. 3 grids, the ratio exceeded one with its 95% Monte Carlo interval and without production floor contact (Table S5). In each of these, shared exposure made a community whose first-order environmental forcing cancels exactly more variable than independent exposure. All five involve eight species; they include the focal $\sigma_{\mathrm{env}}=0.5$ (with $\alpha_{\mathrm{inter}}=0.6$, $\phi=0.4$) and one setting at $\sigma_{\mathrm{env}}=0.2$, which lies outside the small-fluctuation regime.

An additional audit used Bonferroni-adjusted 95% familywise intervals across all 108 setting-by-amplitude comparisons. Replacing the pointwise normal critical value by $\Phi^{-1}[1-0.05/(2\times108)]=3.501318$ in the same log-ratio delta method gives lower bounds of 1.153, 1.501, 1.583, 1.407 and 1.403 in the order of Table S5. All five reversals therefore survive this multiplicity check.

Three checks address alternative explanations.

- **Trajectory length.** A long-window repeat (500 replicates of 6000 steps with 3000 discarded, independent seeds) reproduced every ratio, at 1.19–1.65 with all lower 95% bounds above 1.17. One replicate in one setting had mean floor occupancy of 0.00033, equivalent to eight species-time observations at the floor across the retained window.
- **Numerical guards.** A separate diagnostic of 200 full 600-step and 100 full 6000-step trajectories per exposure condition in each setting recorded no exponent clipping and no floor contact. The diagnostic seed stream is separate from production, but is reused across diagnostic conditions; the 600-step runs are prefixes of the corresponding 6000-step runs for their shared replicate indices. The check describes guard activity in these parameter settings, not in every production replicate.
- **Compensation itself.** Covariance accounting shows that compensation does not disappear. In the $\sigma_{\mathrm{env}}=0.5$ reversal, the aggregate covariance term remained strongly negative under shared exposure (−716, against summed species variances of 925), and mean $\phi_{\mathrm{LdM}}$ was 0.035. It was nevertheless less negative than under independent exposure (−879), whereas total variance rose from 144 to 210. In the focal four-species community, shared exposure did the opposite, strengthening the covariance term from −548 to −1053.

Compensating fluctuations therefore persist in the reversals, but sharing the environment makes them less effective than independent exposure.

Seeds are distinct among replicates within every scenario. Because production seeds are 32-bit values derived from the scenario and replicate indices, 18 seed values recur when the four new grids are pooled; none recurs within an analysed endpoint comparison.

## Prespecified test of ordering by the small-noise coefficient

After the mechanism grids had run, the floor-free ratios within each richness level were found to be nearly rank-ordered by $x=c\,\sigma_{\mathrm{env}}^2$: Spearman correlations were 1.000, 0.9996 and 0.999 for $S=2$, 4 and 8, over 31, 31 and 30 floor-free cells, with a few discordant pairs at nearly equal $x$. Because $\sigma_{\mathrm{env}}$ drives both $R$ and $x$, rank correlations overstate the evidence; the interpolation errors below are the stronger test. Because this pattern was observed rather than predicted, it was tested with two new grids (R17–R18; Table S6) using competition and autocorrelation values absent from the mechanism grids. The predictions and criteria were written to `analysis/prespecified/ordering_predictions_2026-10-19.json` (SHA-256 `0e12545fed0be9e14a4432e987ff06aa2372b8e7f27d61a6a314a99317d74d65`) at 00:28:17 UTC on 19 October 2026. They were posted to the project correspondence at 00:28:43, before the production manifests were created (00:28:49) and before any shard was simulated (00:28:57).

Each prediction interpolated $\log R$ linearly in $\log x$ between the floor-free mechanism-grid cells of the same richness, without extrapolation beyond their range of $x$. In leave-one-out interpolation within those reference cells, the largest error was 7.3% for $S=4$ and 4.2% for $S=8$; the 10% tolerance was set from these values. The criteria and results were:

- **C1, accuracy.** At least 90% of floor-free $S=4$ and 8 cells with a prediction within 10% of it. Result: 35 of 35, with a largest error of 4.6%. For comparison, the small-noise line $R=x$ came within 10% in 8 of these 35 cells, and interpolation in $\log\sigma_{\mathrm{env}}$ alone, using the geometric mean across the reference settings of the same richness, in 6.
- **C2, reversal calls.** Every floor-free $S=8$ cell whose prediction exceeded 1.05 or fell below 0.95 on the predicted side of one. Result: 17 of 17, comprising six predicted reversals, all with 95% intervals above one, and 11 predicted non-reversals, all with intervals below one. The line $R=x$ would have called 14 of the 17 correctly, and interpolation in $\sigma_{\mathrm{env}}$ alone 13. The one called cell with floor contact ($\alpha_{\mathrm{inter}}=0.2$, $\phi=0.6$, $\sigma_{\mathrm{env}}=1$) also fell on the predicted side.
- **C3, richness direction.** At least 80% of floor-free $S=12$ cells above the eight-species curve at the same $x$. Result: 14 of 15. The exception, at $\alpha_{\mathrm{inter}}=0.2$, $\phi=0.2$ and $\sigma_{\mathrm{env}}=0.2$, lies in the small-noise regime, where the ratios at different richness converge (0.1445 against 0.1447).

Thirteen floor-free test cells reversed with 95% intervals above one, six with eight species and seven with twelve, including both predicted eight-species reversals at $\alpha_{\mathrm{inter}}=0.2$. With Bonferroni-adjusted familywise intervals across the 60 test comparisons (critical value 3.342), the lower bounds range from 1.044 to 1.968. Pooling floor-free mechanism and test cells, the Spearman correlations between $x$ and $R$ are 0.999 for $S=4$ (50 cells), 0.9997 for $S=8$ (47 cells) and 1.00 for $S=12$ (15 cells). In eight-species communities, across both sets of grids, $R$ exceeded one in every floor-free cell with $x\ge1.67$ (the smallest, at $x=1.67$, was 1.004, interval 0.989–1.020) and had an interval below one in every cell with $x\le1.45$; the smallest $x$ with an interval above one was 1.85. No tested cell lies between 1.45 and 1.67. Floor-free brackets for the crossing are 1.29–1.83 for $S=12$, and above 2.26 for $S=4$, where the first ratio above one ($x=4.6$) has floor contact. The numerical-guard diagnostic was not extended to the new reversal settings; the floor-free criterion uses the retained production rows.

The coefficient does not account for the dependence on richness at fixed $x$, which appears from four species upward beyond the small-noise regime; below $x\approx0.5$ the two- and four-species curves cross back and forth within about 6%. The richness effect is relative. In the 15 floor-free $(\alpha_{\mathrm{inter}},\phi,\sigma_{\mathrm{env}})$ combinations of the test grids, mean squared CV under independent exposure fell with richness in every case, to 0.24–0.30 of its four-species value at twelve species, whereas under shared exposure the twelve-species value was 0.87–1.56 times the four-species value. In this assembly sequence, adding species also adds response slopes, lowers equilibrium abundance and moves $\lambda_d$ towards one. The test establishes the direction of the combined effect, not its cause. Seeds are distinct among all replicates of the two test grids.

## Implementation and numerical checks

All simulations and analyses were implemented in Python 3.12 in a uv-managed environment. NumPy provides numerical arrays and random-number generation, pandas and PyArrow handle tabular summaries and parquet I/O, and Matplotlib generates the figures. Versioned JSON specifications define every production grid; the same production runner creates deterministic replicate seeds, executes shards, combines outputs, and validates scenario counts and metadata. Automated tests check model limits, covariance construction, analytical diagnostics, production bookkeeping, and the complete summary-to-figure workflow.

Synchrony metrics are checked using toy examples with perfectly synchronous and perfectly asynchronous trajectories: the Loreau–de Mazancourt index $\phi_{\mathrm{LdM}}$ and mean pairwise realised log-growth correlations approach their expected extreme values, and $\phi_{\mathrm{LdM}}$ always lies in $[0,1]$ after clipping. Bookkeeping checks ensure that replicate simulation wrappers return arrays and data frames of the expected shapes and summary statistics.

The separate numerical-guard diagnostic uses 30 replicates per scenario with a fixed seed: mixed and steep aligned responses at $S=4$, $\phi=0.95$, $\sigma_{\mathrm{env}}=1$, and requested $\rho_{\mathrm{env}}=1$ over 400 steps; and steep aligned responses at $S=8$, $\phi=0.4$, $\sigma_{\mathrm{env}}=1.5$, and requested $\rho_{\mathrm{env}}=1$ over 600 steps. Guard activation is measured over each full trajectory, including its initial transient. These diagnostic frequencies are not the post-burn-in production floor frequencies in Table S2. A second block of the same script covers the five balanced-community reversal settings (Table S5) with its own seed and outputs, leaving the original three scenarios unchanged. The anonymous package includes the diagnostic script and its retained replicate-level and summary outputs.

## Species-level variability diagnostic

For each species, the temporal mean and variance are
\[
m_i = \mathbb{E}[N_i],\qquad v_i = \operatorname{Var}(N_i).
\]
An approximate mean species-level CV is then defined as
\[
\mathrm{CV}_{\mathrm{sp}} \approx
\frac{\sqrt{\frac{1}{S}\sum_{i=1}^S v_i}}{\frac{1}{S}\sum_{i=1}^S m_i},
\]
treating the mean of species variances and the mean of species means as proxies for a “typical” species.

## References
