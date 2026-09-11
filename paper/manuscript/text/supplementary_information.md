# Supplementary Information

## Abundance-weighted responses and nonlinear limits to community buffering under correlated environments

This supplementary information file contains the linearised covariance derivation, implementation checks, production run inventory, numerical stress summaries, a selected variance decomposition, and supplementary figures. It is anonymised for double-blind review.

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

## Implementation and numerical checks

All simulations and analyses were implemented in Python 3.12 in a uv-managed environment. NumPy provides numerical arrays and random-number generation, pandas and PyArrow handle tabular summaries and parquet I/O, and Matplotlib generates the figures. Versioned JSON specifications define every production grid; the same production runner creates deterministic replicate seeds, executes shards, combines outputs, and validates scenario counts and metadata. Automated tests check model limits, covariance construction, analytical diagnostics, production bookkeeping, and the complete summary-to-figure workflow.

Synchrony metrics are checked using toy examples with perfectly synchronous and perfectly asynchronous trajectories: the Loreau–de Mazancourt index $\phi_{\mathrm{LdM}}$ and mean pairwise realised log-growth correlations approach their expected extreme values, and $\phi_{\mathrm{LdM}}$ always lies in $[0,1]$ after clipping. Bookkeeping checks ensure that replicate simulation wrappers return arrays and data frames of the expected shapes and summary statistics.

The separate numerical-guard diagnostic uses 30 replicates per scenario with a fixed seed: mixed and steep aligned responses at $S=4$, $\phi=0.95$, $\sigma_{\mathrm{env}}=1$, and requested $\rho_{\mathrm{env}}=1$ over 400 steps; and steep aligned responses at $S=8$, $\phi=0.4$, $\sigma_{\mathrm{env}}=1.5$, and requested $\rho_{\mathrm{env}}=1$ over 600 steps. Guard activation is measured over each full trajectory, including its initial transient. These diagnostic frequencies are not the post-burn-in production floor frequencies in Table S2. The anonymous package includes the diagnostic script and its retained replicate-level and summary outputs.

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
