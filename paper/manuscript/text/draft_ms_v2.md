```{=latex}
\raggedright
```

# Abundance-weighted responses and nonlinear limits to community buffering under correlated environments

## Abstract

Biodiversity can buffer fluctuations in community abundance when species respond differently to environmental change, so that losses in some species are offset by gains in others. Opposing responses alone do not guarantee this compensation, because a species that contributes little to total abundance cannot offset a dominant one. Using a stochastic multispecies Ricker model of competing species, I asked when greater correlation among the environmental conditions that species experience reduces, rather than increases, the temporal variability of total abundance. A covariance argument gives a simple benchmark: correlation reduces the variance of the environmental forcing on total abundance when the sum of abundance-weighted response slopes is sufficiently small relative to their individual magnitudes. In four-species communities, reversing the signs of half the response slopes while holding every magnitude fixed turned buffering into amplification. At an exposure correlation of 0.5, the coefficient of variation of total abundance was 0.084 with mixed response directions and 0.149 with aligned directions. Relative to independent exposures, near-perfect correlation reduced the mean squared coefficient of variation to 0.32 of its baseline value for mixed responses and raised it 2.99-fold for aligned responses. Along continuous gradients of response balance and equilibrium abundance, the benchmark captured this transition but not its exact threshold or effect size. Mixed communities retained substantial variability where linear theory predicted almost none, and just below the predicted threshold the simulations showed weak amplification instead of weak buffering. The contrast between mixed and aligned responses held at every intrinsic growth rate tested. Empirical tests of the insurance hypothesis therefore need three quantities measured together on consistently oriented environmental axes: exposure covariance, species response slopes, and each species' contribution to the aggregate.

## Keywords

biodiversity; response diversity; ecosystem stability; species synchrony; environmental covariance; stochastic community dynamics; insurance hypothesis.

## Introduction

Environmental variability generally destabilises populations. As climatic and other drivers fluctuate, population abundances tend to vary more through time, and the risk of low-abundance episodes and local collapse rises [@ives2007StabilityDiversityEcosystems]. The insurance hypothesis makes a conditional prediction about this problem: biodiversity can buffer ecosystem functioning when different species respond differently in space or time, so that declines in some species are offset by increases in others [@yachi1999BiodiversityEcosystemProductivity]. By analogy with a diversified investment portfolio, aggregate ecosystem properties such as total biomass or productivity should then fluctuate less in diverse communities than in species-poor systems subject to the same environmental variance [@loreau2021BiodiversityInsuranceConcept]. Experiments and syntheses show that biodiversity can stabilise ecosystem functioning [@loreau2013BiodiversityEcosystemStability; @demazancourt2013PredictingEcosystemStability; @wagg2021DiversityAsynchronySoil], but they also show that the strength, and sometimes the sign, of diversity–stability relationships depends on the mechanism that generates covariances among species [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept].

Synchrony among species' fluctuations is the direct route from species-level responses to community-level variability. When species respond similarly to environmental variation, the community tends to fluctuate about as much as a typical species does; when their fluctuations are asynchronous or negatively correlated, aggregate variability can be much lower than the sum of its parts [@doak1998StatisticalInevitabilityStabilitydiversity; @loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability]. Formal measures such as the variance ratio, the Loreau–de Mazancourt synchrony index $\phi_{\mathrm{LdM}}$, and related covariance-based metrics express community stability in terms of species-level variances and covariances [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability; @demazancourt2013PredictingEcosystemStability]. The term "insurance" itself needs care, because it can refer to effects on mean functioning, on variability, or on both, and any claim of stabilisation depends on the comparison used [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept]. Here insurance means relative stabilisation: lower community variability than an appropriate baseline under the same forcing, not an absolute decline in variability as environmental variance increases.

Response diversity, the variation in how species respond to environmental change, is the component of biodiversity most relevant to this mechanism [@elmqvist2003ResponseDiversityEcosystem]. Species within a functional group may be redundant for mean functioning yet differ in their response slopes and tolerances, and those differences can generate compensation [@mori2013ResponseDiversityDetermines]. The stabilising role of response diversity nevertheless remains sparsely tested, and its definitions and metrics vary [@ross2024LimitedTheoreticalEmpirical; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. A recent expert survey found similar disagreement over definitions and stability dimensions, especially where biotic interactions combine with abiotic responses [@ross2026ExpertledPrioritiesResponse]. Empirical work increasingly treats response diversity as dynamic and context dependent, linking time-varying response diversity to ecosystem stability, biological traits to species' responses under multiple drivers, and the outcomes of pulse disturbances to species interactions [@hsieh2026QuantifyingEffectsResponse; @sasaki2026BiologicalTraitsPredict; @kunze2026SpeciesInteractionsDetermine].

Empirical studies point to synchrony and covariance structure, rather than richness alone, as the quantities most closely tied to temporal stability. Across a global compilation of plant communities, species synchrony explained more variation in community stability than richness did [@valencia2020SynchronyMattersMore]. Grassland and soil experiments show stabilisation through population or taxon asynchrony and overyielding [@hector2010GeneralStabilizingEffects; @wagg2021DiversityAsynchronySoil], whereas other plant experiments attribute stability to statistical averaging rather than compensatory dynamics [@zhao2022BiodiversityStabilizesPlant]. In an alpine grassland, nitrogen addition reduced stability first through increased synchrony and later through population variability and diversity loss [@song2026NitrogenAdditionReduces]. These studies treat synchrony as an observed summary of covariance, which on its own cannot show how environmental covariance and species response traits combine to produce it.

A two-species example shows how exposure correlation, response direction, and abundance combine. Suppose that one species grows faster in warm years and another in cool years. If the two experience largely independent temperature anomalies, perhaps because they occupy different microhabitats, their fluctuations only partly average out in the community total. If instead they experience the same anomalies, every warm year that favours one species penalises the other, and their fluctuations offset one another more completely. The same increase in shared exposure would synchronise two species that both grew faster in warm years. The offset also depends on abundance. If the warm-favoured species is far more abundant, the other can offset only a small part of its gains and losses. In larger communities, a sufficient imbalance can even make correlated exposure amplify the fluctuations of a community that still contains opposing responders.

Stochastic community theory already links environmental response covariance to the transmission of fluctuations through population feedback [@ives1999StabilityVariabilityCompetitive; @loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability]. Multispecies Ricker models have shown how environmental covariance, temporal colour, and community assembly jointly affect diversity–stability relationships [@fowler2013ColonizationCovarianceColour], and recent food-web modelling shows that response diversity can determine the sign of a richness–stability relationship [@danet2025ResponseDiversityMajor]. The importance of abundance weighting is also explicit in work on measuring response diversity [@ross2023HowMeasureResponse]. Here I combine these established ideas in a covariance benchmark that links exposure correlation, species response slopes, and species' contributions to total abundance. For the benchmark to be interpretable, the environmental axes must have a common physical orientation for every species; otherwise "exposure correlation" and "response sign" cannot be separated. I then test the benchmark in a nonlinear community model, using contrasts that preserve response magnitude. Buffering here means that correlated exposure reduces community variability, and amplification that it increases variability. The aim is to establish where the benchmark captures the transition between the two and where nonlinear dynamics shift its threshold or change the size of the effect.

The model is deliberately stylised. Communities of competing species follow a symmetric multispecies Ricker map, chosen for its transparent equilibrium and familiar discrete-time feedback. Each species experiences its own trajectory of the same physical exposure, for example a temperature anomaly whose positive direction is identical for every species. These trajectories come from a multivariate first-order autoregressive (AR(1)) process, in which the requested pairwise correlation $\rho_{\mathrm{env}}$ sets how similar the species' exposures are. Species differ in the sign and magnitude of their response slopes, that is, in whether their per-capita growth rates rise or fall with the exposure, and by how much. Insurance is measured as a lower temporal coefficient of variation (CV; standard deviation divided by mean) of total abundance under a specified matched comparison. Synchrony indices and variance decompositions help to diagnose the pathway to that outcome but are not alternative definitions of insurance.

In formal terms, I test the hypothesis that increasing positive cross-species correlation in commonly oriented exposure reduces aggregate variability when the abundance-weighted response vector is sufficiently orthogonal to the common environmental mode, and increases it when the weighted responses project strongly onto that mode. The common mode is the component of exposure that all species share. The analysis first derives a boundary for the variance of aggregate environmental forcing. It then tests how well that boundary predicts abundance variability, using magnitude-matched response signs, a continuous rotation of the response vector at fixed length, unequal equilibrium abundances, and a compact sensitivity analysis for intrinsic growth rate. Broader simulation grids show how the mechanism appears along a deterministic richness assembly sequence, across environmental innovation variance, and along a fixed-innovation gradient in which temporal autocorrelation and stationary variance rise together [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity].

## Methods

### Community dynamics

I model a community of $S$ species using a discrete-time stochastic Ricker model with symmetric competition, a standard description of density-dependent population growth. Let $N_i(t)$ denote the abundance of species $i$ at time $t$. In the absence of environmental variation, abundance follows
\[
N_i(t+1) = N_i(t)\exp\left[r_0 - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right],
\]
where $r_0$ is the intrinsic growth rate shared by all species, $K_i$ scales density dependence for species $i$, and $\alpha_{\mathrm{intra}}$ and $\alpha_{\mathrm{inter}}$ are the strengths of intraspecific and interspecific competition. Unless otherwise stated, I set $r_0=1$, $K_i = 100$ for all species, $\alpha_{\mathrm{intra}} = 1$, and $\alpha_{\mathrm{inter}} = 0.3$, so that each species is limited more strongly by its own abundance than by that of any single competitor. In this parameterisation an isolated species has equilibrium abundance $r_0K_i/\alpha_{\mathrm{intra}}$, and with equal $K_i=K$ the community equilibrium is
\[
N_i^\ast = \frac{r_0 K}{\alpha_{\mathrm{intra}} + \alpha_{\mathrm{inter}}(S-1)}.
\]
For heterogeneous $K_i$, the interior equilibrium, at which all species persist, instead solves $C_\alpha\mathbf N^\ast=r_0\mathbf K$, where $C_\alpha$ has $\alpha_{\mathrm{intra}}$ on its diagonal and $\alpha_{\mathrm{inter}}$ off the diagonal.

Environmental variation enters as a linear response term $b_i z_i(t)$ in the per-capita growth rate:
\[
N_i(t+1) = N_i(t)\exp\left[r_0 + b_i z_i(t) - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right].
\]
The response slope $b_i$ encodes both the direction and the magnitude of species $i$'s response to the environmental anomaly $z_i(t)$. A species with $b_i>0$ grows faster when the anomaly is positive, and one with $b_i<0$ grows more slowly. Three response treatments are used throughout:

* **Mixed** responses: $b_i$ evenly spaced in $[-0.5, 0.5]$. Positive and negative slopes occur in equal numbers, and odd-richness communities also contain one species with zero response. The slopes sum to zero, so this treatment is balanced in its unweighted responses.
* **Matched aligned** responses: the same slope magnitudes as the mixed treatment, all made nonnegative, $b_i = |b_i^{\mathrm{mixed}}|$. This treatment differs from the mixed treatment only in the signs of the responses.
* **Steep aligned** responses: $b_i$ evenly spaced in $[0.1, 1.0]$. All species respond positively, and the root-mean-square slope is greater than in the other two treatments, so this contrast changes response magnitude as well as direction.

These names are used throughout the text, tables, and figure captions; figure legends use shorter labels, which each caption identifies. All simulations start with each species at $K_i/2$. Two numerical safeguards keep the computation well defined: abundances are floored at a small positive constant $N_{\min} = 10^{-9}$ to avoid numerical problems at zero, and the exponent in the growth term is capped at $\pm 50$ to prevent overflow in $\exp(\cdot)$. How often each is triggered is reported with the numerical checks below.

### Environmental process

Environmental anomalies follow a multivariate AR(1) process
\[
\mathbf{z}_t = \phi\,\mathbf{z}_{t-1} + \boldsymbol{\varepsilon}_t,\qquad
\boldsymbol{\varepsilon}_t \sim \mathcal{N}(\mathbf{0}, \Sigma)
\]
where $\mathbf{z}_t$ is an $S$-dimensional vector of commonly oriented environmental exposures at time $t$, $\phi$ is the temporal autocorrelation, and $\Sigma$ is the covariance matrix of the innovation vector $\boldsymbol{\varepsilon}_t$. Each exposure thus retains a fraction $\phi$ of its previous value and receives a new random shock at every time step. All components use the same sign convention, so a positive $z_i$ denotes a higher value of the same physical variable, such as a warmer-than-average temperature, for every species. The trajectories themselves can still differ among sites, seasons, or microhabitats. The innovations are equicorrelated, so that every pair of species has the same correlation between their environmental shocks,
\[
\Sigma = \sigma_{\mathrm{env}}^2\,C(\rho_{\mathrm{env}})
\]
where $\sigma_{\mathrm{env}}$ is the innovation standard deviation, $\rho_{\mathrm{env}}$ is the requested cross-species correlation in exposure, and $C(\rho_{\mathrm{env}})$ is the equicorrelation matrix with ones on the diagonal and $\rho_{\mathrm{env}}$ off the diagonal. A value of $\rho_{\mathrm{env}}=0$ gives every species an independent exposure trajectory, and values approaching 1 expose all species to nearly identical fluctuations. For equicorrelated innovations, positive definiteness requires $\rho > -1/(S-1)$, and the matrix is singular at $\rho=1$. The implementation therefore uses the effective value
\[
\rho_{\mathrm{eff}} = \min\!\left(\max\!\left(\rho_{\mathrm{env}}, -\tfrac{1}{S-1} + \epsilon\right), 1 - \epsilon\right),
\]
with $\epsilon = 10^{-6}$. Simulations use $\rho_{\mathrm{eff}}$, and both the requested and the effective values are retained in the outputs. Requested correlations outside the feasible interval are clipped at the nearer boundary, which in the present grids affects the requested value of 1 and the $S=4$, requested $\rho_{\mathrm{env}}=-0.5$ treatment in Fig. 5. I refer to $\rho_{\mathrm{eff}}=1-10^{-6}$ as near-perfect correlation.

Under this convention, the stationary variance of each environmental component (for $|\phi| < 1$) is
\[
\operatorname{Var}(z_{i,t}) = \frac{\sigma_{\mathrm{env}}^2}{1 - \phi^2},
\]
so increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ increases environmental persistence and stationary variance together, a coupling that matters for the persistence gradient in Fig. 5. When $\sigma_{\mathrm{env}} = 0$, the process is constant and the community dynamics reduce to the deterministic Ricker model. Within a scenario, all species share $\phi$ and the requested $\rho_{\mathrm{env}}$. The environmental state starts at zero, one multivariate series is generated for each replicate of each scenario, and a burn-in period removes the transient that follows from these starting conditions.

### First-order covariance criterion

The benchmark concerns aggregate environmental forcing: the direct effect of the exposures on the community total within a single time step, before population feedback acts. It uses a first-order, or linear, approximation that is appropriate for small fluctuations around equilibrium. Let $w_i$ be the first-order contribution of species $i$ to the aggregate property of interest, and define the weighted response $a_i=w_i b_i$. For total abundance near a deterministic equilibrium, $w_i=N_i^\ast$, because a change $b_i z_i$ in per-capita growth changes abundance by approximately $N_i^\ast b_i z_i$; other ecosystem functions can have different contribution weights. If $F=\sum_i a_i z_i$ is the aggregate environmental forcing and $\Sigma_z$ is the stationary exposure covariance matrix, then
\[
\operatorname{Var}(F)=\mathbf a^\mathsf{T}\Sigma_z\mathbf a.
\]
This expression holds for any covariance structure. Under the equicorrelated design, write $\sigma_z^2=\sigma_{\mathrm{env}}^2/(1-\phi^2)$ for the stationary variance of each exposure. Then
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
In the expression for $\operatorname{Var}(F)$, the first term depends only on the sizes of the weighted responses and is the only term when exposures are independent, whereas the second depends on their sum and gains weight as exposures become more correlated. For non-zero environmental variance, increasing exposure correlation reduces aggregate forcing variance exactly when $(\sum_i a_i)^2<\sum_i a_i^2$, that is, when weighted responses of opposite sign cancel sufficiently in their sum. If the weighted responses sum to zero, perfect correlation removes the first-order forcing entirely. The alignment index
\[
A=\frac{(\mathbf 1^\mathsf{T}\mathbf a)^2}{S\,\mathbf a^\mathsf{T}\mathbf a}
\]
ranges from 0, when the weighted responses sum to zero, to 1, when they are all identical. It places the forcing-variance boundary at $A=1/S$. Increasing exposure correlation reduces the aggregate forcing variance of communities with $A<1/S$ and increases it for those with $A>1/S$.

The same result has a geometric reading that is useful later. An equicorrelation matrix has one common mode, the component of environmental variation shared by all species, and $S-1$ contrast modes, the components in which species' exposures differ. Increasing $\rho_{\mathrm{eff}}$ moves exposure variance out of the contrast modes and into the common mode. A balanced weighted response vector is nearly orthogonal to the common mode, so the aggregate gains little from that transfer while losing the contrast-mode variance to which it did respond. Aligned responses project onto the common mode and gain variance. Mixed signs alone do not guarantee cancellation, because unequal weights $w_i$ can unbalance the weighted responses even when the unweighted slopes sum to zero.

Forcing is only the input to abundance variability, which also depends on how population feedback damps or prolongs each environmental shock [@ives1999StabilityVariabilityCompetitive]. At the equal-$K$ equilibrium, the deterministic Jacobian has a common-mode eigenvalue $\lambda_c=1-r_0$, which governs fluctuations in total abundance, and a contrast-mode eigenvalue
\[
\lambda_d=1-r_0\frac{1-\alpha_{\mathrm{inter}}}{1+\alpha_{\mathrm{inter}}(S-1)}
\]
for $\alpha_{\mathrm{intra}}=1$, which governs fluctuations in the differences among species. Each eigenvalue gives the proportion of a small departure along its mode that carries over to the next time step, and a negative value means that the departure changes sign. At the default $r_0=1$, $S=4$ and $\alpha_{\mathrm{inter}}=0.3$, these are $\lambda_c=0$ and $\lambda_d\approx0.63$: the linearised total-abundance mode has no direct carryover from one step to the next, whereas differences among species decay slowly. Temporal memory can still enter total abundance through the autocorrelated forcing. For equal $K_i$, the linearised departure of total abundance from equilibrium, $X_t$, follows the common mode alone,
\[
X_{t+1}=\lambda_c X_t+F_t.
\]
Because all exposures share the same temporal autocorrelation, $F_t$ is itself an AR(1) process, and at a stable equilibrium
\[
\operatorname{Var}(X)=\operatorname{Var}(F)
\frac{1+\lambda_c\phi}{(1-\lambda_c^2)(1-\lambda_c\phi)}.
\]
The multiplier depends on $r_0$ and $\phi$ but not on exposure correlation, so it cancels when correlations are compared at fixed $r_0$ and $\phi$. In the linearised equal-$K$ model, the forcing criterion therefore gives the exact effect of exposure correlation on stationary total-abundance variance. Two features of the simulated communities can break this correspondence. With unequal $K_i$, the equilibrium weights and the feedback matrix both change, and total abundance no longer follows the scalar recurrence (Supporting information). In the full nonlinear model, products of abundance deviations and growth responses can also contribute to total abundance even when the first-order forcing cancels. A local second-order expansion in the Supporting information shows this route without attributing the whole of the observed departure to it. The simulations measure how much these two departures matter for temporal CV.

### Simulation design

A scenario is defined by a response treatment, species richness $S$, innovation standard deviation $\sigma_{\mathrm{env}}$, requested exposure correlation $\rho_{\mathrm{env}}$, temporal autocorrelation $\phi$, and the population parameters. Every production scenario uses 1000 replicate trajectories of 600 time steps, the first 300 of which are discarded as burn-in. The main model and simulation settings are summarised in Table 1.

The central experiment, the magnitude-matched sign contrast in Fig. 1A, compares mixed and matched aligned responses at $S\in\{4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}=0$ to 1 in increments of 0.1. Because the exposures are symmetric and Gaussian, reversing the sign of a slope leaves the distribution of that species' environmental forcing unchanged. The two treatments therefore have identical species-level forcing distributions and differ only in the covariance of forcing among species. The same production grid includes the steep aligned treatment, which is shown in the Supporting information.

The boundary test in Fig. 1B,C asks where, between these two endpoints, correlated exposure switches from buffering to amplification. It uses $S=4$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}\in\{0,1\}$, and follows two paths. The response-alignment path rotates the mixed vector continuously into the matched aligned vector,
\[
\mathbf b(q)=\cos(\pi q/2)\,\mathbf b_{\mathrm{mixed}}+\sin(\pi q/2)\,|\mathbf b_{\mathrm{mixed}}|,
\]
for nine equally spaced $q\in[0,1]$. Because the two endpoint vectors are orthogonal and have equal norm, the rotation holds $\lVert\mathbf b\rVert$ constant, changing the balance of the responses without changing their overall size. The abundance-weighting path instead retains $\mathbf b_{\mathrm{mixed}}$ and sets
\[
\mathbf K(d)=100(1-0.3d,\,1-0.1d,\,1+0.1d,\,1+0.3d)
\]
for $d\in\{0.25,0.5,0.75,1.0,1.1\}$, with $d=0$ supplied by the mixed endpoint. The $K_i$ always sum to 400, which holds deterministic total abundance constant under symmetric competition while the equilibrium weights become progressively less even, and every treatment retains a positive interior equilibrium. Because this path changes the dynamical feedback matrix as well as the equilibrium weights, it does not isolate weighting alone. Finally, $r_0=1$ gives the linearised common mode no direct carryover ($\lambda_c=0$), so Fig. 1C repeats the mixed and matched aligned endpoints at $r_0\in\{0.25,0.5,1.0,1.5\}$ to check that the sign contrast does not depend on this special case.

The remaining grids extend the analysis beyond the matched comparisons. The comparison of imposed and realised synchrony (Fig. 2) uses mixed and steep aligned responses at $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}$ from 0 to 1 in increments of 0.1. The broader environmental-variance contrast (Fig. 3) uses $S=4$ mixed and steep aligned communities with $\phi=0.4$; its core grid crosses 19 values of $\sigma_{\mathrm{env}}$ between 0 and 2 with 15 requested $\rho_{\mathrm{env}}$ values between -0.3 and 1.0. A high-variance extension adds $\sigma_{\mathrm{env}}\in\{2.25,2.5,2.75,3.0,3.5,4.0\}$ on the same requested-correlation grid, and values $\sigma_{\mathrm{env}}\ge3$ are marked as the highest-stress region in Fig. 3B.

Two further grids use mixed responses only. The richness assembly sequence (Fig. 4) uses $S\in\{2,3,4,5,6,7,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1.0,1.5,2.0\}$, non-negative requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1.0\}$, and $\phi=0.4$. Figure 4 averages scenario means over the shared effective-correlation values for each $S$ and $\sigma_{\mathrm{env}}$. Because the slope vector is regenerated as an evenly spaced sequence for each $S$, adding species changes response composition, root-mean-square slope, and deterministic total abundance together, so this grid does not identify a causal effect of richness alone. The fixed-innovation stress gradient (Fig. 5) uses $\sigma_{\mathrm{env}}=0.5$, $S\in\{2,4\}$, $\rho_{\mathrm{env}}\in\{-0.5,-0.25,0,0.25,0.5,0.75,0.9,1.0\}$, and $\phi\in\{0,0.7,0.9,0.95\}$, and deliberately changes temporal autocorrelation and stationary variance together.

Seeds for the random-number generator are derived deterministically by combining a fixed base seed with the scenario and replicate indices. They are distinct among replicates within each scenario, and environmental realisations are not paired across treatments. Simulations and analyses use Python 3.12, and the versioned specifications and software environment are supplied in the anonymous reproducibility package, where a single analysis workflow aggregates the replicate summaries into the submitted tables and figures. Implementation details and additional checks are given in the Supporting information.

### Metrics and insurance measures

All metrics are computed for each replicate from its post–burn-in time points, and scenario-level summaries average these replicate statistics for each unique treatment and environmental setting. Let $T'$ be the number of retained time steps and define total community abundance
\[
N_{\mathrm{tot}}(t) = \sum_{i=1}^S N_i(t).
\]

**Community variability.** Community variability is measured by the coefficient of variation of total abundance,
\[
\mathrm{CV}_{\mathrm{tot}} = \frac{\sqrt{\operatorname{Var}(N_{\mathrm{tot}})}}{\mathbb{E}[N_{\mathrm{tot}}]},
\]
where the sample mean and the sample variance (with divisor $T'-1$) are computed over the $T'$ retained time points.
For supplementary interpretation, total-abundance variance is also decomposed as
\[
\operatorname{Var}(N_{\mathrm{tot}})
=
\sum_i \operatorname{Var}(N_i)
+ 2\sum_{i<j}\operatorname{Cov}(N_i,N_j),
\]
using the full-replicate summaries to report mean total abundance, total variance, summed species variances, and the aggregate covariance term. A negative covariance term means that species' fluctuations partly offset one another.

For the endpoint-correlation tests in Fig. 1B,C, I compare squared community CV under near-perfect and independent exposures,
\[
R_{\mathrm{CV}^2}=
\frac{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}\approx1]}
{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}=0]}.
\]
Values of $R_{\mathrm{CV}^2}$ below 1 mean that near-perfect exposure correlation reduces community variability relative to independent exposures, and values above 1 mean that it increases variability. Squared CV is used because, with mean total abundance close to its equilibrium value, it is proportional to variance, which makes the ratio directly comparable with the first-order forcing benchmark for the same contrast, $(1-\rho_{\mathrm{eff}})+\rho_{\mathrm{eff}}SA$. At the near-perfect endpoint this benchmark equals $SA$ to within $10^{-6}$, so it predicts $R_{\mathrm{CV}^2}\approx0$ for a perfectly balanced community and $R_{\mathrm{CV}^2}=S$ for a perfectly aligned one.

**Synchrony indices.** Let $v_i$ be the temporal variance of species $i$'s abundance and $\sigma_i=\sqrt{v_i}$ its standard deviation. Abundance-based community synchrony is quantified using the Loreau–de Mazancourt index [@loreau2008SpeciesSynchronyIts],
\[
\phi_{\mathrm{LdM}} = \frac{\operatorname{Var}(N_{\mathrm{tot}})}{\left(\sum_{i=1}^S \sigma_i\right)^2}.
\]
The index equals 1 when all species fluctuate in perfect synchrony and falls towards 0 as their fluctuations cancel in the total; it is undefined when abundances are constant, as they are without environmental variation. In exact arithmetic $\phi_{\mathrm{LdM}}$ lies in $[0,1]$, and computed values are clipped to that interval to remove rounding overshoot.

To capture realised synchrony in population dynamics, per-capita log-growth rates are computed as
\[
g_i(t) = \log[N_i(t+1)+N_{\min}] - \log[N_i(t)+N_{\min}],
\]
where the implementation adds a further numerical offset $N_{\min}$ after flooring abundances. I correlate these growth rates across time for every pair of species and take the mean of the off-diagonal correlations. This mean pairwise realised per-capita log-growth correlation measures whether species actually grow in step, and it can be negative when their dynamics are compensatory. Unlike the first-order response term $b_i z_i(t)$, it includes density dependence, abundance feedbacks, floor effects where present, and the nonlinearities of the Ricker map. When $\sigma_{\mathrm{env}} = 0$, growth-rate variance is zero and the correlation is undefined, so such scenarios are excluded from the correlation-based synchrony panels.

**Floor occupancy.** For species $i$, floor occupancy, the fraction of retained time steps spent at the numerical floor, is
\[
e_i = \frac{1}{T'}\sum_{t=1}^{T'} \mathbf{1}\left[N_i(t) \leq N_{\min}\right],
\]
and the community mean floor occupancy is
\[
\bar{e} = \frac{1}{S}\sum_{i=1}^S e_i.
\]
Because $N_{\min}$ is a numerical device and floored populations can recover, $e_i$ is interpreted as contact with the floor, not as a probability of irreversible biological extinction.

**Interpretation.** Insurance is interpreted as relative stabilisation under matched environmental forcing. At fixed richness, lower $\mathrm{CV}_{\mathrm{tot}}$ for mixed than for aligned responses indicates compensatory insurance. Along the deterministic assembly sequence, lower $\mathrm{CV}_{\mathrm{tot}}$ at larger $S$ describes that particular sequence and is not an estimate of the effect of richness alone. Lower $\phi_{\mathrm{LdM}}$ or realised log-growth correlation helps to diagnose a compensatory pathway but is not part of the definition.

### Monte Carlo uncertainty

With 1000 replicates per scenario, Monte Carlo uncertainty in mean $\mathrm{CV}_{\mathrm{tot}}$ is small relative to the contrasts reported below. At $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, and $S=4$, for example, the mixed and matched aligned means are 0.084 and 0.149. The replicate standard deviation of $\mathrm{CV}_{\mathrm{tot}}$ in the mixed treatment is 0.0048, so the standard error of that mean is about 0.00015. Scenario means of $\mathrm{CV}_{\mathrm{tot}}$ are therefore reported to three decimal places. For the ratios in Fig. 1B,C, 95% Monte Carlo intervals are calculated on the log ratio by the delta method from the replicate-level distributions of $\mathrm{CV}_{\mathrm{tot}}^2$. These intervals describe simulation error within the model, not uncertainty about the model's structure.

### Numerical and ecological checks

Numerical checks verify the environmental covariance construction, the stationary environmental variance, and the deterministic limits of the model. For the boundary treatments, they confirm a positive deterministic equilibrium in every case, a constant response norm along the rotation, and constant deterministic total abundance along the $K_i$ path. Further metric and implementation checks are described in the Supporting information.

A separate numerical-guard diagnostic, with 30 replicates in each of three stress scenarios at $\sigma_{\mathrm{env}}=1.0$ or 1.5, found no high-side exponent clipping, and its scenario-mean low-side clipping fractions ranged from 0.00024 to 0.0070 over the full trajectories. These diagnostic rates are distinct from the post-burn-in floor frequencies of the production grids (Supporting information). Floor occupancy is very low in the main inference grids. In the richness grid for Fig. 4, for example, the maximum scenario mean is about 0.0014 even at $\sigma_{\mathrm{env}}=2.0$, so the richness pattern is not driven by repeated contact with the numerical floor. Occupancy rises in the explicitly labelled high-$\sigma_{\mathrm{env}}$ and high-$\phi$ extensions (Supporting information), so I treat those regions as numerical and ecological stress tests rather than as clean evidence about the mechanism.

## Results

### Reversing response signs alone reverses the effect of exposure correlation

Under independent exposures the mixed and matched aligned treatments are indistinguishable, but they diverge as $\rho_{\mathrm{eff}}$ rises (Fig. 1A). At $S=4$ and $\rho_{\mathrm{eff}}=0$, both have mean $\mathrm{CV}_{\mathrm{tot}}=0.106$, as expected, because with independent exposures the two treatments have identical forcing distributions. At $\rho_{\mathrm{eff}}=0.5$ the mixed and aligned means are 0.084 and 0.149, so the mixed community is little more than half as variable, and near $\rho_{\mathrm{eff}}=1$ the contrast widens to 0.059 versus 0.184. The corresponding $S=8$ values at $\rho_{\mathrm{eff}}=0.5$ are 0.059 and 0.120. Because every species' marginal forcing distribution is the same in both treatments, the separation can be attributed to the sign-dependent covariance of forcing among species rather than to slope magnitude.

### Weighted alignment captures the broad transition, with nonlinear departures

The continuous response rotation reproduces the transition from buffering to amplification predicted by the first-order criterion, and also shows where that criterion fails quantitatively (Fig. 1B). At the mixed endpoint ($A=0$), the linearised model predicts that near-perfect correlation should remove almost all of the variability present under independent exposures. The simulated ratio is instead 0.320 (95% Monte Carlo interval 0.315--0.325), so about a third of the independent-exposure mean squared CV remains even though the linear forcing cancels. At the matched aligned endpoint ($A=0.8$), the benchmark predicts 3.2 and the simulation gives 2.99 (2.97--3.02). Most ratios along the rotation lie closer to one than their benchmark values, but at the tested point nearest the boundary the simulated ratio and the benchmark fall on opposite sides of one (Fig. 1B, inset). The nonlinear crossing of $R_{\mathrm{CV}^2}=1$ is therefore displaced to lower alignment than the benchmark value $A=1/S=0.25$. It is bracketed by the tested points at $A=0.117$, where the ratio is 0.666, and $A=0.247$, where the benchmark predicts weak buffering (0.988) but the simulation shows weak amplification (1.043; 1.028--1.059). The criterion thus captures the broad transition and the contrast between endpoints, but not the exact nonlinear threshold or the size of the effect.

The unequal-$K_i$ path also crosses from buffering to amplification, although it keeps the mixed response vector unchanged and holds deterministic total abundance at 210.5. At $A=0.230$, $R_{\mathrm{CV}^2}=0.964$ (0.952--0.975); at $A=0.257$, it is 1.053 (1.041--1.065). All species keep a positive equilibrium along this path: the most uneven treatment has a minimum equilibrium abundance of 5.49 and a maximum scenario-mean floor occupancy of $1.6\times10^{-5}$, and all other boundary-test scenarios have zero floor occupancy. Thus mixed signs cease to stabilise the community along this path as equilibrium weights and population feedback change, and the two tested points on either side of one bracket the forcing boundary. At the upper point the benchmark predicts 1.030, so on this path it slightly underpredicts amplification.

The sign reversal also survives changes in intrinsic growth rate, which alter the local density-feedback dynamics (Fig. 1C). Across $r_0=0.25,0.5,1.0,$ and 1.5, $R_{\mathrm{CV}^2}$ for mixed responses is 0.663, 0.439, 0.320, and 0.323, respectively, and the corresponding matched aligned ratios are 2.77, 2.94, 2.99, and 2.97. Correlated exposure buffers mixed communities and amplifies aligned ones at every tested growth rate, so the result is not confined to $r_0=1$, where the linearised common mode has no direct abundance carryover.

### Response direction transforms exposure correlation into realised synchrony

At $\sigma_{\mathrm{env}}=0.5$, realised per-capita log-growth correlations in mixed communities fall well below $\rho_{\mathrm{eff}}$ as exposure correlation increases (Fig. 2A). Near $\rho_{\mathrm{eff}}=1$, mean realised correlations are approximately -0.81 for $S=2$, where the two species have exactly opposite slopes, -0.16 for $S=4$, and 0.08 for $S=8$. In the steep aligned treatment the same correlations remain strongly positive, at approximately 0.64, 0.81, and 0.86, respectively, and increase with $\rho_{\mathrm{eff}}$ (Fig. 2B). Plotted as a difference, $\mathrm{corr}_{\mathrm{realised}}-\rho_{\mathrm{eff}}$ becomes strongly negative for mixed responses (Fig. 2C). The matched aligned control gives the same contrast without any change in slope magnitude. Near $\rho_{\mathrm{eff}}=1$, realised growth correlation is -0.16 for mixed and 0.90 for matched aligned responses at $S=4$, and 0.08 and 0.84, respectively, at $S=8$ (Supporting information). Requested exposure correlation is a property of the forcing, not a proxy for biological synchrony.

### Environmental-variance, assembly-sequence, and persistence extensions

The steep aligned treatment extends the comparison across a wide range of environmental innovation SD (Fig. 3). Its larger slopes increase absolute variability, so it is not a sign-only control, but it shows where aligned communities enter severe boom–bust dynamics as $\sigma_{\mathrm{env}}$ increases. Mixed communities are less variable than steep aligned communities in every cell with non-zero $\sigma_{\mathrm{env}}$, including the high-$\sigma_{\mathrm{env}}$ extension, although at the highest forcing levels the dynamics are floor-affected stress cases rather than clean fluctuations around equilibrium.

Along the prespecified mixed-response assembly sequence, mean $\mathrm{CV}_{\mathrm{tot}}$ declines from $S=2$ to $S=8$ at every non-zero $\sigma_{\mathrm{env}}$ after averaging over the shared non-negative correlation grid (Fig. 4). At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, for example, mean CV is approximately 0.15, 0.08, and 0.06 for $S=2,4,$ and 8, and the $S=4$ and $S=8$ values agree with the independently simulated grid in Fig. 1A. The sequence also lowers root-mean-square response magnitude and raises mean total abundance as species are added, so the decline cannot be assigned to richness alone. In the variance decomposition, the aggregate covariance term is negative in the selected $S=2,4,$ and 8 scenarios, indicating compensation among species. Neither total variance nor the magnitude of the covariance term changes monotonically at every step, however (Supporting information).

Increasing $\phi$ at fixed innovation SD raises temporal autocorrelation and stationary variance together, so Fig. 5 describes a compound stress gradient. At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, mean $\mathrm{CV}_{\mathrm{tot}}$ rises from approximately 0.14 at $\phi=0$ to 0.58 at $\phi=0.95$ for $S=2$, and from 0.07 to 0.35 for $S=4$. The ordering of the assembly sequence persists, with four-species communities less variable than two-species communities at every tested $\phi$ and requested correlation, while the decline in CV with $\rho_{\mathrm{eff}}$ weakens, or reverses locally, at the most persistent edge. Floor occupancy is essentially absent for $\phi\le0.7$, reaches a maximum scenario mean of about 0.005 at $\phi=0.9$, and rises to 0.049 at $\phi=0.95$. The most persistent treatment is therefore a fixed-innovation stress case, not evidence for an isolated effect of temporal autocorrelation.

## Discussion

### Weighted cancellation and population feedback

Making the environments of different species more alike can either synchronise their fluctuations or stabilise their combined abundance. The outcome depends on how the community's weighted responses relate to the environmental modes that gain and lose variance. Under equicorrelation, higher $\rho_{\mathrm{eff}}$ concentrates variance in the common mode, the component of variation that all species share, and removes it from the contrast modes, the components in which species differ. Aggregate forcing variance falls when the abundance-weighted response vector has little projection onto the common mode, which is what the condition $(\sum_i a_i)^2<\sum_i a_i^2$, or $A<1/S$, expresses. Opposing response signs make such cancellation possible but do not guarantee it, because a negative responder that contributes little abundance or function cannot offset a dominant positive responder.

The simulations support the predicted contrast between mixed and aligned responses and measure how far nonlinear dynamics depart from the benchmark. Reversing the signs of otherwise identical slopes reverses the effect of exposure correlation, and both the response-rotation and the unequal-abundance paths cross from buffering to amplification near the benchmark boundary. Yet the benchmark predicts almost complete buffering for a perfectly balanced community, whereas the model retains about a third of its independent-exposure mean squared CV under near-perfect correlation. Just below the benchmark's threshold, the simulated effect has the opposite sign to the predicted one. Linear cancellation does not imply constant total abundance in the nonlinear model. Products of abundance deviations and growth responses, including quadratic terms from the Ricker update, can contribute to total abundance even when the first-order forcing cancels (Supporting information). This provides a route for the remaining variability, although the present comparisons do not separate these contributions or establish their individual effects on the threshold. The benchmark is thus a guide to the broad transition and the contrast between endpoints, but not to the size of the effect or the exact position of the threshold.

The matched aligned control separates response sign from the magnitude effect present in the steep aligned treatment, whose large absolute CV partly reflects its steeper slopes. Realised growth correlations (Fig. 2; Supporting information) then show the next step in the transmission of environmental fluctuations: the same positive exposure correlation produces compensatory or strongly synchronous population growth, depending on response orientation. These correlations are dynamical diagnostics, not formal estimates of mediation, and $\phi_{\mathrm{LdM}}$, which shares total-abundance variance with community CV, should likewise not be treated as independent confirmation [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability]. The sign contrast survives changes in intrinsic growth rate, with mixed and matched aligned treatments on opposite sides of $R_{\mathrm{CV}^2}=1$ across $r_0=0.25$--1.5. Because $r_0$ also alters equilibrium abundance and both the common and contrast population modes, however, the changing size of these ratios cannot be attributed to common-mode memory alone.

The physical orientation of exposure is part of the claim. Temperature, moisture, or another measured variable must have the same positive direction for every species, so that a positive anomaly means the same thing wherever it occurs. If each $z_i$ is instead an independently defined latent axis that can be reversed, exposure correlation and response sign become coordinate choices rather than separately identifiable ecological quantities. Reversing one species' axis changes the sign of its response slope and of its exposure correlations with every other species, while leaving its demographic shocks unchanged. The invariant object is then the demographic-shock covariance $D_b\Sigma_zD_b$, where $D_b=\operatorname{diag}(b_1,\ldots,b_S)$. This distinction matters when empirical response models use species-specific latent gradients.

### What should be measured in real communities?

Neither a count of species nor a tally of positive and negative responders reveals the weighted response vector. Along the unequal-$K_i$ path, the species list and every response sign stayed the same, yet mixed responses ceased to buffer the community once equilibrium abundances became sufficiently uneven. An empirical test therefore needs three linked quantities: covariance among commonly oriented exposures, species response slopes on those axes, and contributions to the aggregate property. For total abundance the natural initial weights are equilibrium or mean abundances, whereas for biomass, productivity, or multifunctionality they may differ. The forcing benchmark predicts buffering when the dominant contributors cancel along the environmental modes that gain variance; predicting how much buffering occurs also requires attention to population feedback.

This prediction sharpens the concept of response diversity [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines]. Empirical work already shows that synchrony can explain more variation in community stability than richness [@valencia2020SynchronyMattersMore] and that asynchrony or statistical averaging can dominate in different systems [@hector2010GeneralStabilizingEffects; @zhao2022BiodiversityStabilizesPlant; @wagg2021DiversityAsynchronySoil]. In Lake Geneva, time-varying response diversity also had context-dependent effects on phytoplankton and zooplankton biomass [@hsieh2026QuantifyingEffectsResponse]. The alignment criterion identifies one possible reason for such context dependence: the same list of response signs can have different consequences once abundance weights or environmental covariance change.

Real communities also face several environmental variables at once. A community can be balanced along one covariance mode and aligned along another, for instance compensating in its response to temperature while all species respond in the same direction to drought. A single unweighted response-diversity index can then combine stabilising and destabilising components [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. An aggregate linear response still has a forcing variance of the form $\mathbf a^\mathsf{T}\Sigma_z\mathbf a$, with the coefficients and covariance dimensions expanded to cover the relevant exposures, but estimating it requires response surfaces and function-specific weights [@polazzo2024MeasuringResponseDiversity; @sasaki2026BiologicalTraitsPredict].

### Richness and temporal structure are conditional extensions

The decline in CV from $S=2$ to $S=8$ is specific to the implemented assembly sequence. As species are added, intermediate slopes fill the fixed interval $[-0.5,0.5]$, odd-richness communities gain a zero-response species, root-mean-square slope decreases, and deterministic total abundance rises. Statistical averaging, covariance cancellation, changing forcing magnitude, and a larger CV denominator all move together. The result shows that this particular sequence becomes more stable, not that richness independently causes the decline, an interpretation consistent with theory and data that place covariance structure closer to community stability than richness itself [@demazancourt2013PredictingEcosystemStability; @valencia2020SynchronyMattersMore; @danet2025ResponseDiversityMajor].

Figure 5 has a similarly narrow interpretation. Holding innovation SD fixed while increasing $\phi$ raises temporal autocorrelation and stationary exposure variance together. Although the mixed-response assembly ordering survives that compound stress gradient, the design neither identifies a pure effect of temporal autocorrelation nor tests the matched sign contrast across $\phi$. The floor-affected $\phi=0.95$ edge is useful as a model boundary rather than as stronger evidence for the mechanism.

### Scope of the model

The analysis deliberately holds much of community structure fixed. Competition is symmetric, responses are linear in a single exposure, and demographic stochasticity, observation error, dispersal between populations, and trophic interactions are all absent. The $r_0$ sensitivity removes dependence on one special Ricker growth rate but does not establish invariance to other density-dependence functions or to asymmetric interaction matrices. These omitted processes and alternative structures can alter the dynamical weights that link environmental shocks to aggregate abundance [@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial].

Equicorrelation makes the common and contrast modes transparent. Spatially heterogeneous, block-correlated, or empirically estimated covariance matrices will have different eigenvectors, and their effects on aggregate forcing variance will depend on how the weighted response vector projects onto those modes [@loreau2003BiodiversitySpatialInsurance; @shanafelt2015BiodiversityProductivitySpatial]. The unequal-$K_i$ treatments show that changing species contributions and feedback together can move a community across the buffering boundary. The present simulations support the mechanism for one nonlinear community model and a limited set of departures from symmetry; they do not estimate how often, or how strongly, it operates in nature.

The numerical floor is a computational safeguard, not biological extinction; it is negligible in the matched-sign and weighted-boundary tests but becomes active in the high-variance and high-$\phi$ stress extensions. Finally, stability here means the temporal CV of total abundance. Resistance, resilience, recovery, and multifunctional stability are different properties and may respond differently to the same response structure [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept; @kunze2026SpeciesInteractionsDetermine].

### Conclusion

When species experience commonly oriented exposures, environmental correlation reduces aggregate forcing variance if their abundance-weighted responses cancel and increases it if those responses align. In the Ricker communities studied here, reversing response signs alone was enough to reverse the effect of exposure correlation on community variability. Continuous changes in response balance and in equilibrium abundances produced a broad transition from buffering to amplification near the forcing benchmark. The benchmark nevertheless has clear limits in the nonlinear model. A balanced community retained 0.32 of its independent-exposure mean squared CV, and near the rotation threshold the benchmark and the simulations disagreed about the direction of the effect. Empirical tests of insurance should therefore measure exposure covariance, species response slopes, and species' contributions to the aggregate together, and should use the covariance criterion alongside an assessment of the population feedbacks that transmit environmental fluctuations.

## Artificial intelligence statement

OpenAI Codex large language models assisted with model and code development, simulation and analysis workflows, literature searches, and drafting and editorial revision. Anthropic Claude assisted with literature checking, scientific review, and editorial revision. The author reviewed all AI-assisted material incorporated into the work and takes full responsibility for the final content.

## References
