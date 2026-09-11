# Abundance-weighted responses shape community buffering under correlated environments

## Abstract

Biodiversity can buffer community fluctuations when species respond differently to environmental change, but opposing responses need not compensate if some species contribute much more than others. I used stochastic multispecies Ricker simulations to test how response direction and abundance determine whether increasingly correlated environmental exposures buffer total abundance. A covariance analysis gives a simple benchmark: increasing correlation reduces aggregate forcing variance when the squared sum of abundance-weighted response slopes is smaller than their summed squares. In four-species communities, changing only response signs produced a clear contrast. At exposure correlation 0.5, balanced responses gave a coefficient of variation of total abundance of 0.084, compared with 0.149 for aligned responses of identical magnitude. Relative to independent exposures, near-perfect correlation reduced mean squared coefficients of variation to 0.32 times the baseline for balanced responses and increased them to 2.99 times the baseline for aligned responses. Continuous changes in response balance and equilibrium abundance produced transitions near the benchmark boundary, with a small but resolved departure in the nonlinear response experiment. The sign contrast persisted across the tested intrinsic growth rates. These results identify abundance-weighted response balance as an informative predictor of buffering in this model. Empirical assessment requires exposure covariance, species response slopes, and contributions to the aggregate property to be measured together on consistently oriented environmental axes.

## Keywords

biodiversity; response diversity; ecosystem stability; species synchrony; environmental covariance; stochastic community dynamics; insurance hypothesis.

## Introduction

Environmental variability generally destabilises populations: as climatic and other drivers fluctuate, population abundances tend to vary more through time, increasing the risk of low-abundance episodes and local collapse [@ives2007StabilityDiversityEcosystems]. The insurance hypothesis makes a conditional prediction about this problem: biodiversity can buffer ecosystem functioning when different species respond differently in space or time, so that declines in some species are offset by increases in others [@yachi1999BiodiversityEcosystemProductivity]. Borrowing from portfolio theory, the hypothesis predicts that aggregate ecosystem properties such as total biomass or productivity should fluctuate less in diverse communities than in species-poor systems subject to the same environmental variance [@loreau2021BiodiversityInsuranceConcept]. Experiments and syntheses show that biodiversity can stabilise ecosystem functioning [@loreau2013BiodiversityEcosystemStability; @demazancourt2013PredictingEcosystemStability; @wagg2021DiversityAsynchronySoil], but they also show that the strength, and sometimes the sign, of diversity–stability relationships depends on the mechanism generating species covariances [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept].

Synchrony among species’ fluctuations is the direct route from species-level responses to community-level variability. When species respond similarly to environmental variation, community-level variability tends to scale with typical species-level variability; when responses are asynchronous or negatively correlated, aggregate variability can be much lower than the sum of its parts [@doak1998StatisticalInevitabilityStabilitydiversity; @loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability]. Formal measures such as the variance ratio, Loreau–de Mazancourt’s synchrony index $\phi_{\mathrm{LdM}}$, and related covariance-based metrics link species-level variances and covariances to community-level stability [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability; @demazancourt2013PredictingEcosystemStability]. Insurance can refer to effects on mean functioning, effects on variability, or both; claims of stabilisation also depend on the comparison used [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept]. Here I use relative stabilisation: lower community variability than an appropriate baseline under the same forcing, not an absolute decline in variability as environmental variance increases.

Response diversity identifies the component of biodiversity most relevant to this mechanism: variation in how species respond to environmental change [@elmqvist2003ResponseDiversityEcosystem]. Species within a functional group may be redundant for mean functioning yet differ in response slopes and tolerances, generating compensation [@mori2013ResponseDiversityDetermines]. Its stabilising role remains sparsely tested, and definitions and metrics vary [@ross2024LimitedTheoreticalEmpirical; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. A recent expert survey found similar disagreement over definitions and stability dimensions, especially where biotic interactions combine with abiotic responses [@ross2026ExpertledPrioritiesResponse]. Empirical work increasingly treats response diversity as dynamic and context dependent, linking time-varying diversity to stability, biological traits to responses under multiple drivers, and pulse-disturbance outcomes to species interactions [@hsieh2026QuantifyingEffectsResponse; @sasaki2026BiologicalTraitsPredict; @kunze2026SpeciesInteractionsDetermine].

Stochastic community theory already links environmental response covariance to the transmission of fluctuations through population feedback [@ives1999StabilityVariabilityCompetitive; @loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability]. Multispecies Ricker models have also shown how environmental covariance, temporal colour, and community assembly jointly affect diversity–stability relationships [@fowler2013ColonizationCovarianceColour], while recent food-web modelling shows that response diversity can determine the sign of a richness–stability relationship [@danet2025ResponseDiversityMajor]. Here I express the covariance prediction in terms of commonly oriented exposures and abundance-weighted response slopes, then test how well it predicts nonlinear abundance variability using contrasts that preserve response magnitude. The aim is to identify when this explicit benchmark remains informative and where population dynamics produce departures from it.

Empirical studies likewise identify synchrony and covariance structure, rather than richness alone, as the quantities closest to temporal stability. Across a global compilation of plant communities, species synchrony explained more variation in community stability than richness [@valencia2020SynchronyMattersMore]. Grassland and soil experiments show stabilisation through population or taxon asynchrony and overyielding [@hector2010GeneralStabilizingEffects; @wagg2021DiversityAsynchronySoil], whereas other plant experiments identify statistical averaging rather than compensatory dynamics [@zhao2022BiodiversityStabilizesPlant]. In an alpine grassland, nitrogen addition reduced stability first through increased synchrony and later through population variability and diversity loss [@song2026NitrogenAdditionReduces]. These studies treat synchrony as an observed covariance summary; they do not by themselves explain how environmental covariance and response traits combine to produce it.

I examine this prediction with a deliberately stylised model. Stochastic multispecies communities follow a symmetric Ricker map, chosen for its transparent equilibrium and familiar discrete-time feedback. Each species receives a trajectory of the same physical exposure—for example, a temperature anomaly whose positive direction is identical for every species—from a multivariate first-order autoregressive (AR(1)) process. The requested pairwise correlation $\rho_{\mathrm{env}}$ controls the similarity of those trajectories. Species differ in the sign and magnitude of their response slopes. This shared orientation is essential: independently reversible latent environmental axes would not identify exposure correlation separately from response sign.

Insurance is defined here as a lower temporal coefficient of variation (CV) of total abundance under a specified matched comparison. At fixed richness, lower CV for balanced than aligned response slopes indicates compensatory insurance. A decline along the implemented richness sequence is reported as an assembly-sequence pattern because response composition and other design quantities also change with $S$. Loreau–de Mazancourt synchrony $\phi_{\mathrm{LdM}}$, realised per-capita log-growth correlation, and abundance variance decomposition are diagnostics of the pathway, not alternative definitions of insurance.

I test the hypothesis that increasing positive cross-species correlation in commonly oriented exposure reduces aggregate variability when the abundance-weighted response vector is sufficiently orthogonal to the common environmental mode, but increases variability when responses project strongly onto that mode. The analysis first derives a boundary for aggregate forcing variance, then tests its prediction for abundance variability with magnitude-matched signs, a continuous fixed-norm response rotation, unequal equilibrium abundances, and a compact $r_0$ sensitivity. Broader grids show how the mechanism appears along a deterministic richness assembly sequence, across environmental innovation variance, and along a fixed-innovation gradient in which temporal autocorrelation and stationary variance rise together [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity].

## Methods 

### Community dynamics

I model a community of $S$ species using a discrete-time stochastic Ricker model with symmetric competition. Let $N_i(t)$ denote the abundance of species $i$ at time $t$. In the absence of environmental variation, per-capita growth follows
\[
N_i(t+1) = N_i(t)\exp\left[r_0 - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right],
\]
where $r_0$ is a shared intrinsic growth rate, $K_i$ scales density dependence for species $i$, $\alpha_{\mathrm{intra}}$ is intraspecific competition, and $\alpha_{\mathrm{inter}}$ is interspecific competition. I set $r_0=1$, $K_i = 100$ for all species, $\alpha_{\mathrm{intra}} = 1$, and $\alpha_{\mathrm{inter}} = 0.3$ unless otherwise stated. In this parameterisation, an isolated species has equilibrium abundance $r_0K_i/\alpha_{\mathrm{intra}}$. With equal $K_i=K$, the community equilibrium is
\[
N_i^\ast = \frac{r_0 K}{\alpha_{\mathrm{intra}} + \alpha_{\mathrm{inter}}(S-1)}.
\]
For heterogeneous $K_i$, the interior equilibrium instead solves $C_\alpha\mathbf N^\ast=r_0\mathbf K$, where $C_\alpha$ has $\alpha_{\mathrm{intra}}$ on its diagonal and $\alpha_{\mathrm{inter}}$ off the diagonal.

Environmental variation enters as a linear response term $b_i z_i(t)$ in the per-capita growth rate:
\[
N_i(t+1) = N_i(t)\exp\left[r_0 + b_i z_i(t) - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right].
\]
Species differ in their response slopes $b_i$, which encode both the direction and magnitude of their response to the environmental anomaly $z_i(t)$. Three named regimes are used:

* Mixed slopes: $b_i$ evenly spaced in $[-0.5, 0.5]$, giving both positive and negative responses.
* Positive slopes: $b_i$ evenly spaced in $[0.1, 1.0]$, giving aligned positive responses.
* Positive-matched (sign-structure control): aligned positive slopes with magnitudes matched to mixed slopes, $b_i = |b_i^{\mathrm{mixed}}|$.

Abundances are floored at a small positive constant $N_{\min} = 10^{-9}$ to avoid numerical problems at zero, and the exponent in the growth term is capped at $\pm 50$ to prevent overflow in $\exp(\cdot)$. Initial abundances are set to $K_i/2$ for all species.

### Environmental process

Environmental anomalies are generated by a multivariate AR(1) process
\[
\mathbf{z}_t = \phi\,\mathbf{z}_{t-1} + \boldsymbol{\varepsilon}_t,\qquad
\boldsymbol{\varepsilon}_t \sim \mathcal{N}(\mathbf{0}, \Sigma)
\]
where $\mathbf{z}_t$ is an $S$-dimensional vector of commonly oriented environmental exposures at time $t$, $\phi$ is the temporal autocorrelation, and $\Sigma$ is the covariance matrix of the innovation vector $\boldsymbol{\varepsilon}_t$. Each component uses the same sign convention: a positive $z_i$ denotes a higher value of the same physical variable for every species, even though exposure trajectories can differ among sites, seasons, or microhabitats. An equicorrelated covariance structure is used,
\[
\Sigma = \sigma_{\mathrm{env}}^2\,C(\rho_{\mathrm{env}})
\]
where $\sigma_{\mathrm{env}}$ is the innovation standard deviation, $\rho_{\mathrm{env}}$ is the requested cross-species correlation in exposure, and $C(\rho_{\mathrm{env}})$ is the equicorrelation matrix with ones on the diagonal and $\rho_{\mathrm{env}}$ off-diagonal. For equicorrelated innovations, positive definiteness requires $\rho > -1/(S-1)$ and the matrix is singular at $\rho=1$. The implementation therefore uses the effective value
\[
\rho_{\mathrm{eff}} = \min\!\left(\max\!\left(\rho_{\mathrm{env}}, -\tfrac{1}{S-1} + \epsilon\right), 1 - \epsilon\right),
\]
with small $\epsilon$. Simulations are generated using $\rho_{\mathrm{eff}}$, while both requested and effective values are retained in outputs.

Under this convention, the stationary variance of each environmental component (for $|\phi| < 1$) is
\[
\operatorname{Var}(z_{i,t}) = \frac{\sigma_{\mathrm{env}}^2}{1 - \phi^2},
\]
so increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ simultaneously increases environmental persistence and the effective stationary variance. When $\sigma_{\mathrm{env}} = 0$, the process is constant and the community dynamics reduce to the deterministic Ricker model.

For a given scenario, all species share $\phi$ and the requested $\rho_{\mathrm{env}}$ but receive correlated trajectories from the multivariate process. The environmental state is initialised at zero; one multivariate series is generated per replicate and scenario, and burn-in removes the initial transient.

### First-order covariance criterion

Let $w_i$ be the first-order contribution of species $i$ to the aggregate and define $a_i=w_i b_i$. For total abundance near a deterministic equilibrium, $w_i=N_i^\ast$; other ecosystem functions can have different contribution weights. If $F=\sum_i a_i z_i$ is the aggregate environmental forcing and $\Sigma_z$ is the stationary exposure covariance matrix, then
\[
\operatorname{Var}(F)=\mathbf a^\mathsf{T}\Sigma_z\mathbf a.
\]
This expression applies to any covariance structure. Under the equicorrelated design, let $\sigma_z^2=\sigma_{\mathrm{env}}^2/(1-\phi^2)$. Then
\[
\operatorname{Var}(F)
=\sigma_z^2\left[(1-\rho_{\mathrm{eff}})\sum_i a_i^2
+\rho_{\mathrm{eff}}\left(\sum_i a_i\right)^2\right],
\]
and
\[
\frac{\partial\operatorname{Var}(F)}{\partial\rho_{\mathrm{eff}}}
=\sigma_z^2\left[\left(\sum_i a_i\right)^2-\sum_i a_i^2\right].
\]
For non-zero environmental variance, increasing exposure correlation reduces aggregate forcing variance exactly when $(\sum_i a_i)^2<\sum_i a_i^2$. The alignment index
\[
A=\frac{(\mathbf 1^\mathsf{T}\mathbf a)^2}{S\,\mathbf a^\mathsf{T}\mathbf a}
\]
places the forcing-variance boundary at $A=1/S$, with buffering when $A<1/S$. An equicorrelation matrix has one common mode parallel to $\mathbf 1$ and $S-1$ contrast modes. Increasing $\rho_{\mathrm{eff}}$ transfers exposure variance towards the common mode; a balanced weighted response vector is nearly orthogonal to that mode, whereas aligned responses project onto it. Mixed signs alone do not guarantee cancellation because unequal $w_i$ can change the weighted balance.

The link to abundance variability depends on population feedback [@ives1999StabilityVariabilityCompetitive]. For equal $K_i$, the linearised departure of total abundance from equilibrium, $X_t$, follows the common abundance mode,
\[
X_{t+1}=\lambda_c X_t+F_t,\qquad \lambda_c=1-r_0.
\]
All exposures share the same temporal autocorrelation, so $F_t$ is also AR(1). At a stable equilibrium,
\[
\operatorname{Var}(X)=\operatorname{Var}(F)
\frac{1+\lambda_c\phi}{(1-\lambda_c^2)(1-\lambda_c\phi)}.
\]
For fixed $r_0$ and $\phi$, this multiplier cancels when comparing exposure correlations. The forcing criterion therefore also gives the exact correlation effect on stationary total-abundance variance in the linearised equal-$K$ model. With unequal $K_i$, equilibrium weights and the feedback matrix both change, and total abundance generally no longer follows this scalar recurrence (Supporting information). The simulations test how well the forcing benchmark predicts temporal CV after these changes and nonlinear population feedback.

### Simulation design

A scenario is defined by a response treatment, species richness $S$, innovation standard deviation $\sigma_{\mathrm{env}}$, requested exposure correlation $\rho_{\mathrm{env}}$, temporal autocorrelation $\phi$, and the population parameters. Every production scenario uses 1000 replicate trajectories of 600 time steps, with the first 300 discarded as burn-in.

The main model and simulation settings are summarised in Table 1.

The magnitude-matched sign control in Fig. 1A compares mixed and positive-matched slopes at $S\in\{4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}=0$ to 1 in increments of 0.1. Under symmetric Gaussian exposure, mixed and positive-matched treatments have identical species-level forcing distributions; only their cross-species covariance differs. The same production grid includes a steeper positive-slope treatment, shown in the Supporting information.

The boundary test in Fig. 1B,C uses $S=4$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}\in\{0,1\}$. Its response-alignment path is
\[
\mathbf b(q)=\cos(\pi q/2)\,\mathbf b_{\mathrm{mixed}}+\sin(\pi q/2)\,|\mathbf b_{\mathrm{mixed}}|,
\]
for nine equally spaced $q\in[0,1]$. The two endpoint vectors are orthogonal and have equal norm, so this rotation holds $\lVert\mathbf b\rVert$ constant. A separate abundance-weighting path retains $\mathbf b_{\mathrm{mixed}}$ and sets
\[
\mathbf K(d)=100(1-0.3d,\,1-0.1d,\,1+0.1d,\,1+0.3d)
\]
for $d\in\{0.25,0.5,0.75,1.0,1.1\}$, with $d=0$ supplied by the balanced endpoint. The sum of $K_i$ is always 400, which holds deterministic total abundance constant under symmetric competition, while the equilibrium weights become progressively less even. All treatments retain a positive interior equilibrium. This path changes the dynamical feedback matrix as well as equilibrium abundance weights; it does not isolate weighting alone.

At the equal-$K$ equilibrium, the deterministic Jacobian has common-mode eigenvalue $\lambda_c=1-r_0$ and contrast-mode eigenvalue
\[
\lambda_d=1-r_0\frac{1-\alpha_{\mathrm{inter}}}{1+\alpha_{\mathrm{inter}}(S-1)}
\]
for $\alpha_{\mathrm{intra}}=1$. Because $r_0=1$ gives $\lambda_c=0$, Fig. 1C repeats the balanced and positive-matched endpoints at $r_0\in\{0.25,0.5,1.0,1.5\}$.

For the imposed-versus-realised synchrony mechanism (Fig. 2), simulations use mixed and positive slope regimes at $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}$ from 0 to 1 in increments of 0.1.

For the broader environmental-variance contrast (Fig. 3), simulations use $S=4$ mixed- and positive-slope communities with $\phi=0.4$, $n_{\mathrm{steps}}=600$, $n_{\mathrm{burn}}=300$, and 1000 replicates per scenario. The core grid crosses 19 values of $\sigma_{\mathrm{env}}$ between 0 and 2 with 15 requested $\rho_{\mathrm{env}}$ values between -0.3 and 1.0. A high-variance extension adds $\sigma_{\mathrm{env}}\in\{2.25,2.5,2.75,3.0,3.5,4.0\}$ on the same requested-correlation grid; values $\sigma_{\mathrm{env}}\ge3$ are marked as the highest-stress region in Fig. 3B.

For the richness assembly sequence (Fig. 4), a mixed-slope grid uses $S\in\{2,3,4,5,6,7,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1.0,1.5,2.0\}$, non-negative requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1.0\}$, and $\phi=0.4$. Figure 4 averages scenario means over the shared effective-correlation values for each $S$ and $\sigma_{\mathrm{env}}$. Because the slope vector is regenerated as an evenly spaced sequence for each $S$, this grid changes response composition, root-mean-square slope, and deterministic total abundance together; it does not identify a causal effect of richness alone.

To examine a fixed-innovation stress gradient (Fig. 5), mixed-slope simulations use $\sigma_{\mathrm{env}}=0.5$, $S\in\{2,4\}$, $\rho_{\mathrm{env}}\in\{-0.5,-0.25,0,0.25,0.5,0.75,0.9,1.0\}$, and $\phi\in\{0,0.7,0.9,0.95\}$. This design deliberately changes temporal autocorrelation and stationary variance together.

A fixed base seed is combined with scenario and replicate indices to generate deterministic seeds. Seeds are distinct among replicates within each scenario, and environmental realisations are not deliberately paired across treatments. Simulations and analyses use Python 3.12; versioned specifications and the software environment are supplied in the anonymous reproducibility package. Replicate summaries are aggregated into the submitted tables and figures by a single analysis workflow. Implementation details and additional checks are provided in the Supporting information.

### Metrics and insurance measures

All metrics are computed from post–burn-in time points. Let $T'$ be the number of retained time steps and define total community abundance
\[
N_{\mathrm{tot}}(t) = \sum_{i=1}^S N_i(t).
\]

**Community variability.** Community variability is measured by the coefficient of variation of total abundance,
\[
\mathrm{CV}_{\mathrm{tot}} = \frac{\sqrt{\operatorname{Var}(N_{\mathrm{tot}})}}{\mathbb{E}[N_{\mathrm{tot}}]},
\]
where empirical sample means and sample variances (with $\mathrm{ddof}=1$) are computed over the $T'$ retained time points.
For supplementary interpretation, total-abundance variance is also decomposed as
\[
\operatorname{Var}(N_{\mathrm{tot}})
=
\sum_i \operatorname{Var}(N_i)
+ 2\sum_{i<j}\operatorname{Cov}(N_i,N_j),
\]
using the full-replicate summaries to report mean total abundance, total variance, summed species variances, and the aggregate covariance term.

For the endpoint-correlation tests in Fig. 1B,C, I use
\[
R_{\mathrm{CV}^2}=
\frac{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}\approx1]}
{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}=0]}.
\]
Thus $R_{\mathrm{CV}^2}<1$ means that near-perfect exposure correlation reduces nonlinear community variability relative to independent exposures, whereas $R_{\mathrm{CV}^2}>1$ means that it increases variability. The first-order forcing benchmark for the same contrast is $(1-\rho_{\mathrm{eff}})+\rho_{\mathrm{eff}}SA$.

**Synchrony indices.** Abundance-based community synchrony is quantified using the Loreau–de Mazancourt index [@loreau2008SpeciesSynchronyIts],
\[
\phi_{\mathrm{LdM}} = \frac{\operatorname{Var}(N_{\mathrm{tot}})}{\left(\sum_{i=1}^S \sigma_i\right)^2},
\]
where $v_i$ is the temporal abundance variance and $\sigma_i = \sqrt{v_i}$ is the standard deviation of species $i$. To avoid numerical overshoots, $\phi_{\mathrm{LdM}}$ is clipped to the interval $[0, 1]$.

To capture realised synchrony in population dynamics, per-capita log-growth rates are computed as
\[
g_i(t) = \log\left(N_i(t+1) + N_{\min}\right) - \log\left(N_i(t) + N_{\min}\right),
\]
the correlation matrix of ${g_i(t)}$ across time is formed, and the mean of its off-diagonal elements is taken. This yields the **mean pairwise realised per-capita log-growth correlation**, which can be negative when species exhibit compensatory dynamics. Unlike the first-order $b_i z_i(t)$ response term above, this realised metric includes density dependence, abundance feedbacks, floor effects where present, and nonlinearities introduced by the Ricker map.
When $\sigma_{\mathrm{env}} = 0$, growth-rate variance is zero and this correlation is undefined; such scenarios are excluded from correlation-based synchrony panels.

**Floor occupancy.** For species $i$, floor occupancy is defined as
\[
e_i = \frac{1}{T'}\sum_{t=1}^{T'} \mathbf{1}\left[N_i(t) \leq N_{\min}\right],
\]
and the community mean floor occupancy is
\[
\bar{e} = \frac{1}{S}\sum_{i=1}^S e_i.
\]
Because $N_{\min}$ is a numerical floor and populations can subsequently recover, $e_i$ is interpreted as floor occupancy, not as a probability of irreversible biological extinction.

Scenario-level summaries are obtained by averaging replicate statistics for each unique treatment and environmental setting.

“Insurance” is interpreted as relative stabilisation under matched environmental forcing. At fixed richness, lower $\mathrm{CV}_{\mathrm{tot}}$ in balanced than aligned treatments indicates stronger compensatory insurance. Along the deterministic assembly sequence, lower $\mathrm{CV}_{\mathrm{tot}}$ at larger $S$ is an observed sequence-level pattern rather than an estimate of richness alone. Lower $\phi_{\mathrm{LdM}}$ or realised log-growth correlation diagnoses a compensatory pathway; it is not an additional criterion in the definition.

### Monte Carlo uncertainty

Each scenario is represented by 1000 replicates. Monte Carlo uncertainty in mean $\mathrm{CV}_{\mathrm{tot}}$ is small relative to the contrasts reported below. At $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, and $S=4$, for example, the mixed and magnitude-matched aligned means are 0.084 and 0.149. For ratios in Fig. 1B,C, 95% Monte Carlo intervals are calculated on the log ratio by the delta method from the replicate-level distributions of $\mathrm{CV}_{\mathrm{tot}}^2$.

### Numerical and ecological checks

Numerical checks verify the environmental covariance construction, stationary environmental variance, and deterministic model limits. The boundary treatments retain a positive deterministic equilibrium, hold response norm constant along the rotation, and hold deterministic total abundance constant along the $K_i$ path. The sign contrast across $r_0$ tests whether the result depends on the special common-mode dynamics at $r_0=1$. Additional metric and implementation checks are described in the Supporting information.

Numerical-guard diagnostics showed that high-side exponent clipping was effectively absent. Mean low-side clipping stayed below 0.01 in dedicated diagnostics at $\sigma_{\mathrm{env}}\leq1.5$ but reached 0.016–0.021 in 200-replicate checks of positive-slope $\sigma_{\mathrm{env}}=4$ stress cells. Floor occupancy was low in most scenarios but increased in the high-$\phi$ and high-variance regions (Supporting information). These extremes are therefore treated as stress tests rather than clean mechanistic evidence.

Floor occupancy remains very low in the main inference grids. In the richness grid for Figure 4, the maximum scenario mean is $\approx 0.0014$ even at $\sigma_{\mathrm{env}}=2.0$, confirming that the reported richness pattern is not driven by repeated contact with the numerical floor. Occupancy rises in the explicitly labelled high-$\sigma_{\mathrm{env}}$ and high-$\phi$ stress extensions, so those regions are interpreted as numerical and ecological stress tests rather than baseline scenarios.

## Results

### Magnitude-matched responses isolate the sign reversal

The mixed and positive-matched treatments are almost indistinguishable under independent exposures, then diverge as $\rho_{\mathrm{eff}}$ rises (Fig. 1A). At $S=4$ and $\rho_{\mathrm{eff}}=0$, their mean $\mathrm{CV}_{\mathrm{tot}}$ values are 0.1064 and 0.1064. At $\rho_{\mathrm{eff}}=0.5$, the balanced mixed treatment falls to 0.0840 while the same slope magnitudes aligned in one direction rise to 0.1489. Near $\rho_{\mathrm{eff}}=1$, the contrast widens to 0.0595 versus 0.1841. The corresponding $S=8$ values at $\rho_{\mathrm{eff}}=0.5$ are 0.0591 and 0.1198. Because the marginal forcing distribution of every species is preserved, this separation is attributable to the sign-dependent cross-species covariance rather than slope magnitude.

### Weighted alignment predicts the direction of correlation effects

The continuous response rotation captures the broad transition predicted by the first-order criterion (Fig. 1B). At the balanced endpoint ($A=0$), $R_{\mathrm{CV}^2}=0.320$ (95% Monte Carlo interval 0.315--0.325); at the magnitude-matched aligned endpoint ($A=0.8$), it is 2.992 (2.965--3.019). The nonlinear crossing is bracketed by the tested points at $A=0.117$ and $A=0.247$. At the latter point, the forcing benchmark predicts weak buffering, with a ratio of 0.988, whereas the nonlinear ratio is 1.043 (1.028--1.059), indicating weak amplification. This departure is small but resolved relative to Monte Carlo error: the criterion predicts the broad gradient, but not the exact nonlinear boundary.

The unequal-$K_i$ path also crosses from buffering to amplification while preserving the mixed response vector and deterministic total abundance. Along the $K_i$ path, the total equilibrium remains 210.53. At $A=0.230$, $R_{\mathrm{CV}^2}=0.964$ (0.952--0.975); at $A=0.257$, it is 1.053 (1.041--1.065). The most uneven treatment retains a positive minimum equilibrium abundance of 5.49, and its maximum scenario-mean floor occupancy is $1.6\times10^{-5}$; all other boundary-test scenarios have zero floor occupancy. Thus mixed signs cease to stabilise along this path as equilibrium weights and population feedback change, with the observed crossing near the forcing benchmark.

The sign reversal also survives changes in local density-feedback dynamics (Fig. 1C). Across $r_0=0.25,0.5,1.0,$ and 1.5, $R_{\mathrm{CV}^2}$ for balanced responses is 0.663, 0.439, 0.320, and 0.323, respectively. The corresponding magnitude-matched aligned ratios are 2.774, 2.942, 2.992, and 2.971. The result is therefore not confined to the common-mode superstable point at $r_0=1$.

### Response direction transforms exposure correlation into realised synchrony

At $\sigma_{\mathrm{env}}=0.5$, realised per-capita log-growth correlations in mixed communities fall well below $\rho_{\mathrm{eff}}$ as exposure correlation increases (Fig. 2A). Near $\rho_{\mathrm{eff}}=1$, mean realised correlations are approximately -0.81 for $S=2$, -0.16 for $S=4$, and 0.08 for $S=8$. In the broader positive-slope treatment they remain strongly positive—approximately 0.64, 0.81, and 0.86, respectively—and increase with $\rho_{\mathrm{eff}}$ (Fig. 2B). The difference $\mathrm{corr}_{\mathrm{realised}}-\rho_{\mathrm{eff}}$ consequently becomes strongly negative for mixed responses (Fig. 2C).

The magnitude-matched control gives the same mechanistic contrast without changing slope magnitudes. Near $\rho_{\mathrm{eff}}=1$, realised growth correlation is -0.16 for mixed slopes and 0.90 for positive-matched slopes at $S=4$; at $S=8$ the corresponding values are 0.08 and 0.84 (Supporting information). Requested exposure correlation is therefore a property of the forcing, not a proxy for biological synchrony.

### Environmental-variance, assembly-sequence, and persistence extensions

The broader positive-slope treatment maps the same contrast over environmental innovation SD. Its larger slopes increase absolute variability, so it is not a sign-only control, but it shows where aligned responses enter severe boom–bust dynamics as $\sigma_{\mathrm{env}}$ increases (Fig. 3). Mixed responses remain less variable across the shared grid. The relative contrast persists in the high-$\sigma_{\mathrm{env}}$ extension, although the highest forcing levels are floor-affected stress cases rather than clean equilibrium fluctuations.

Along the prespecified mixed-slope assembly sequence, mean $\mathrm{CV}_{\mathrm{tot}}$ declines from $S=2$ to $S=8$ at every non-zero $\sigma_{\mathrm{env}}$ after averaging over the shared non-negative correlation grid (Fig. 4). At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, for example, mean CV is approximately 0.15, 0.08, and 0.06 for $S=2,4,$ and 8. This sequence also lowers root-mean-square response magnitude and raises mean total abundance, so the decline cannot be assigned to richness alone. The variance decomposition shows negative aggregate covariance at the selected $S=2,4,$ and 8 scenarios, but total variance and covariance magnitude do not change monotonically at every step (Supporting information).

Increasing $\phi$ at fixed innovation SD creates a compound temporal-autocorrelation and stationary-variance gradient (Fig. 5). At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, mean $\mathrm{CV}_{\mathrm{tot}}$ rises from approximately 0.14 at $\phi=0$ to 0.58 at $\phi=0.95$ for $S=2$, and from 0.07 to 0.35 for $S=4$. The assembly-sequence ordering persists, while the decline in CV with $\rho_{\mathrm{eff}}$ weakens or reverses locally at the most persistent edge. Floor occupancy is essentially absent through $\phi\le0.7$, reaches a maximum scenario mean of about 0.005 at $\phi=0.9$, and rises to 0.049 at $\phi=0.95$. The final treatment is therefore a fixed-innovation stress case, not evidence for an isolated effect of temporal autocorrelation.

## Discussion

### Weighted cancellation and population feedback

Positive correlation in exposure can stabilise an aggregate because it changes which environmental mode carries the variance. Under equicorrelation, higher $\rho_{\mathrm{eff}}$ concentrates variance in the common mode and removes it from the contrast modes. Aggregate forcing variance is reduced when its abundance-weighted response vector has little projection onto that common mode. The condition $(\sum_i a_i)^2<\sum_i a_i^2$, or $A<1/S$, states this directly. Opposing response signs make cancellation possible, but they are not sufficient: a negative responder that contributes little abundance or function cannot offset a dominant positive responder.

The simulations support the predicted contrast between balanced and aligned responses, while identifying a limit near the transition. Aligning the signs of otherwise identical slopes reverses the effect of exposure correlation, and the response and unequal-abundance paths cross from buffering to amplification near $A=0.25$. The response path nevertheless shows amplification at the closest tested point below that threshold. The nonlinear boundary is therefore approximate. Balanced and aligned treatments also remain on opposite sides of $R_{\mathrm{CV}^2}=1$ across $r_0=0.25$--1.5. The equal-$K$ linearisation explains why the sign criterion is independent of the common-mode feedback multiplier at fixed $r_0$ and $\phi$; the simulations show that the endpoint reversal persists despite nonlinear departures.

The matched control separates response sign from the magnitude effect in the broader positive treatment. Its large absolute CV partly reflects steeper slopes, whereas the positive-matched treatment isolates covariance orientation. The controlled contrast isolates the sign-dependent transmission of a common exposure mode. Realised growth correlations in Fig. 2 and the Supporting information show the next step in that transmission: the same positive exposure correlation produces compensatory or strongly synchronous population growth depending on response orientation. These correlations are dynamical diagnostics, not formal mediation estimates. Likewise, $\phi_{\mathrm{LdM}}$ shares total-abundance variance with community CV and should not be treated as independent confirmation [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability].

The physical orientation of exposure is part of the claim. Temperature, moisture, or another measured variable must have the same positive direction for every species. If each $z_i$ is an independently defined latent axis that can be reversed, exposure correlation and response sign are coordinate choices rather than separately identifiable ecological quantities. In that case the invariant object is the demographic-shock covariance $D_b\Sigma_zD_b$, where $D_b=\operatorname{diag}(b_1,\ldots,b_S)$. This distinction matters when empirical response models use species-specific latent gradients.

### What should be measured in real communities?

Richness counts do not reveal the weighted response vector. An empirical test needs three linked quantities: covariance among commonly oriented exposures, species response slopes on those axes, and contributions to the aggregate property. For total abundance the natural initial weights are equilibrium or mean abundances; for biomass, productivity, or multifunctionality they may differ. The forcing benchmark predicts buffering when dominant contributors cancel along the environmental modes that gain variance; predicting abundance variability additionally requires attention to population feedback.

This prediction sharpens the response-diversity concept [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines]. Empirical work already shows that synchrony can explain more variation in community stability than richness [@valencia2020SynchronyMattersMore] and that asynchrony or statistical averaging can dominate in different systems [@hector2010GeneralStabilizingEffects; @zhao2022BiodiversityStabilizesPlant; @wagg2021DiversityAsynchronySoil]. Time-varying response diversity in Lake Geneva also had context-dependent effects on phytoplankton and zooplankton biomass [@hsieh2026QuantifyingEffectsResponse]. The alignment criterion identifies one reason for such context dependence: the same list of response signs can have different consequences after abundance weights or environmental covariance change.

Real communities also face several environmental variables. A community can be balanced along one covariance mode and aligned along another, so a single unweighted response-diversity index can combine stabilising and destabilising components [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. An aggregate linear response still has a forcing variance of the form $\mathbf a^\mathsf{T}\Sigma_z\mathbf a$, with coefficients and covariance dimensions expanded to cover the relevant exposures. Estimation then requires response surfaces and function-specific weights [@polazzo2024MeasuringResponseDiversity; @sasaki2026BiologicalTraitsPredict].

### Richness and temporal structure are conditional extensions

The decline in CV from $S=2$ to $S=8$ is specific to the implemented assembly sequence. Adding species fills the fixed interval $[-0.5,0.5]$ with intermediate slopes; odd-richness communities gain a zero-response species; root-mean-square slope decreases; and deterministic total abundance rises. Statistical averaging, covariance cancellation, changing forcing magnitude, and a larger CV denominator therefore move together. The result shows that this particular sequence becomes more stable, not that richness independently causes the decline. That interpretation is consistent with theory and data placing covariance structure closer to community stability than richness itself [@demazancourt2013PredictingEcosystemStability; @valencia2020SynchronyMattersMore; @danet2025ResponseDiversityMajor].

Figure 5 has a similarly narrow interpretation. Holding innovation SD fixed while increasing $\phi$ raises temporal autocorrelation and stationary exposure variance together. The mixed-slope assembly ordering survives that compound stress gradient, but the design does not identify a pure temporal-autocorrelation effect or test the matched sign contrast across $\phi$. The floor-affected $\phi=0.95$ edge is useful as a model boundary, not as stronger evidence for the mechanism.

### Scope of the model

The analysis deliberately holds much of community structure fixed. Competition is symmetric, responses are linear in one exposure, and demographic stochasticity, observation error, spatial population exchange, and trophic interactions are absent. The $r_0$ sensitivity removes dependence on one special Ricker growth rate, but it does not establish invariance to alternative density-dependence functions or asymmetric interaction matrices. Those processes can alter the dynamical weights linking environmental shocks to aggregate abundance [@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial].

Equicorrelation makes the common and contrast modes transparent. Spatially heterogeneous, block-correlated, or empirically estimated covariance matrices will have different eigenvectors. Their effects on aggregate forcing variance depend on projections of the weighted response vector onto those modes [@loreau2003BiodiversitySpatialInsurance; @shanafelt2015BiodiversityProductivitySpatial]. The unequal-$K_i$ treatments show that changing species contributions and feedback together can move the community across the buffering boundary. The present simulations support the mechanism for one nonlinear community model and a limited set of departures from symmetry; they do not estimate its frequency or magnitude in nature.

The numerical floor is also a computational safeguard, not biological extinction. It is negligible in the matched-sign and weighted-boundary tests, but participates in the high-variance and high-$\phi$ stress extensions. Finally, stability here means temporal CV of total abundance. Resistance, resilience, recovery, and multifunctional stability may respond differently to the same response structure [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept; @kunze2026SpeciesInteractionsDetermine].

### Conclusion

For commonly oriented exposures, environmental correlation can reduce aggregate forcing variance when abundance-weighted responses cancel and increase it when they align. In this Ricker model, the magnitude-matched control supports that sign reversal, while the continuous response and unequal-abundance paths locate nonlinear transitions near the forcing benchmark. The resolved departure near the response-alignment threshold shows why the criterion should guide, rather than substitute for, analysis of population dynamics. Empirical tests should therefore combine exposure covariance and species responses with their contributions to the aggregate and the feedbacks that transmit environmental fluctuations.

## Artificial intelligence statement

OpenAI Codex large language models assisted with model and code development, simulation and analysis workflows, literature searches, and drafting and editorial revision. The author reviewed all AI-assisted material incorporated into the work and takes full responsibility for the final content.

## References
