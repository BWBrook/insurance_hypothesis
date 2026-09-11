```{=latex}
\raggedright
```

# Abundance-weighted responses and nonlinear limits to community buffering under correlated environments

## Abstract

Biodiversity can buffer fluctuations in community abundance when species respond differently to environmental change. Opposing responses do not guarantee such buffering, because a species that contributes little abundance cannot offset a dominant one. I used a stochastic multispecies Ricker model to ask when increasing correlation among the environmental conditions that species experience reduces, rather than increases, the temporal variability of total abundance. A covariance argument gives a simple benchmark: correlation reduces aggregate forcing variance when the sum of abundance-weighted response slopes is sufficiently small relative to their individual magnitudes. In four-species communities, reversing the signs of half the response slopes while holding every magnitude fixed changed the outcome qualitatively. At an exposure correlation of 0.5, the coefficient of variation of total abundance was 0.084 with mixed response directions and 0.149 with aligned directions. Near-perfect correlation reduced mean squared coefficients of variation to 0.32 of the independent-exposure baseline for mixed responses and raised them to 2.99 times the baseline for aligned responses. The benchmark captured the broad transition but not its exact threshold or effect size. The mixed community retained substantial variability despite near-complete first-order cancellation, while near the response-alignment threshold the simulation showed weak amplification where the benchmark predicted weak buffering. The sign contrast held across the tested intrinsic growth rates. Empirical tests of the insurance hypothesis therefore need three quantities measured together on consistently oriented environmental axes: exposure covariance, species response slopes, and each species' contribution to the aggregate.

## Keywords

biodiversity; response diversity; ecosystem stability; species synchrony; environmental covariance; stochastic community dynamics; insurance hypothesis.

## Introduction

Environmental variability generally destabilises populations: as climatic and other drivers fluctuate, population abundances tend to vary more through time, increasing the risk of low-abundance episodes and local collapse [@ives2007StabilityDiversityEcosystems]. The insurance hypothesis makes a conditional prediction about this problem: biodiversity can buffer ecosystem functioning when different species respond differently in space or time, so that declines in some species are offset by increases in others [@yachi1999BiodiversityEcosystemProductivity]. Borrowing from portfolio theory, the hypothesis predicts that aggregate ecosystem properties such as total biomass or productivity should fluctuate less in diverse communities than in species-poor systems subject to the same environmental variance [@loreau2021BiodiversityInsuranceConcept]. Experiments and syntheses show that biodiversity can stabilise ecosystem functioning [@loreau2013BiodiversityEcosystemStability; @demazancourt2013PredictingEcosystemStability; @wagg2021DiversityAsynchronySoil], but they also show that the strength, and sometimes the sign, of diversity–stability relationships depends on the mechanism generating species covariances [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept].

Synchrony among species' fluctuations is the direct route from species-level responses to community-level variability. When species respond similarly to environmental variation, community-level variability tends to scale with typical species-level variability; when responses are asynchronous or negatively correlated, aggregate variability can be much lower than the sum of its parts [@doak1998StatisticalInevitabilityStabilitydiversity; @loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability]. Formal measures such as the variance ratio, the Loreau–de Mazancourt synchrony index $\phi_{\mathrm{LdM}}$, and related covariance-based metrics link species-level variances and covariances to community-level stability [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability; @demazancourt2013PredictingEcosystemStability]. Insurance can refer to effects on mean functioning, effects on variability, or both, and claims of stabilisation depend on the comparison used [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept]. Here insurance means relative stabilisation: lower community variability than an appropriate baseline under the same forcing, not an absolute decline in variability as environmental variance increases.

Response diversity identifies the component of biodiversity most relevant to this mechanism: variation in how species respond to environmental change [@elmqvist2003ResponseDiversityEcosystem]. Species within a functional group may be redundant for mean functioning yet differ in response slopes and tolerances, generating compensation [@mori2013ResponseDiversityDetermines]. Its stabilising role remains sparsely tested, and definitions and metrics vary [@ross2024LimitedTheoreticalEmpirical; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. A recent expert survey found similar disagreement over definitions and stability dimensions, especially where biotic interactions combine with abiotic responses [@ross2026ExpertledPrioritiesResponse]. Empirical work increasingly treats response diversity as dynamic and context dependent, linking time-varying diversity to stability, biological traits to responses under multiple drivers, and pulse-disturbance outcomes to species interactions [@hsieh2026QuantifyingEffectsResponse; @sasaki2026BiologicalTraitsPredict; @kunze2026SpeciesInteractionsDetermine].

Empirical studies identify synchrony and covariance structure, rather than richness alone, as the quantities closest to temporal stability. Across a global compilation of plant communities, species synchrony explained more variation in community stability than richness [@valencia2020SynchronyMattersMore]. Grassland and soil experiments show stabilisation through population or taxon asynchrony and overyielding [@hector2010GeneralStabilizingEffects; @wagg2021DiversityAsynchronySoil], whereas other plant experiments identify statistical averaging rather than compensatory dynamics [@zhao2022BiodiversityStabilizesPlant]. In an alpine grassland, nitrogen addition reduced stability first through increased synchrony and later through population variability and diversity loss [@song2026NitrogenAdditionReduces]. These studies treat synchrony as an observed covariance summary. They do not by themselves explain how environmental covariance and species response traits combine to produce it.

Stochastic community theory already links environmental response covariance to the transmission of fluctuations through population feedback [@ives1999StabilityVariabilityCompetitive; @loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability]. Multispecies Ricker models have shown how environmental covariance, temporal colour, and community assembly jointly affect diversity–stability relationships [@fowler2013ColonizationCovarianceColour], and recent food-web modelling shows that response diversity can determine the sign of a richness–stability relationship [@danet2025ResponseDiversityMajor]. Two elements are less often made explicit. First, the environmental axes must have a common physical orientation for every species, otherwise "exposure correlation" and "response sign" cannot be separated. Second, what matters for an aggregate is not the list of response signs but the response slopes weighted by each species' contribution to that aggregate. Here I express the covariance prediction in those terms, then test how well it predicts the variability of total abundance in a nonlinear community model, using contrasts that preserve response magnitude. The aim is to identify when this explicit benchmark is informative and where population dynamics depart from it.

The model is deliberately stylised. Stochastic multispecies communities follow a symmetric Ricker map, chosen for its transparent equilibrium and familiar discrete-time feedback. Each species receives a trajectory of the same physical exposure—for example, a temperature anomaly whose positive direction is identical for every species—from a multivariate first-order autoregressive (AR(1)) process. The requested pairwise correlation $\rho_{\mathrm{env}}$ controls how similar those trajectories are. Species differ in the sign and magnitude of their response slopes. Insurance is measured as a lower temporal coefficient of variation (CV; standard deviation divided by mean) of total abundance under a specified matched comparison. Synchrony indices and variance decompositions are diagnostics of the pathway, not alternative definitions of insurance.

I test the hypothesis that increasing positive cross-species correlation in commonly oriented exposure reduces aggregate variability when the abundance-weighted response vector is sufficiently orthogonal to the common environmental mode, and increases it when responses project strongly onto that mode. The analysis first derives a boundary for aggregate forcing variance, then tests its prediction for abundance variability using magnitude-matched response signs, a continuous fixed-norm response rotation, unequal equilibrium abundances, and a compact sensitivity to intrinsic growth rate. Broader grids then show how the mechanism appears along a deterministic richness assembly sequence, across environmental innovation variance, and along a fixed-innovation gradient in which temporal autocorrelation and stationary variance rise together [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity].

## Methods 

### Community dynamics

I model a community of $S$ species using a discrete-time stochastic Ricker model with symmetric competition. Let $N_i(t)$ denote the abundance of species $i$ at time $t$. In the absence of environmental variation, abundance follows
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
The response slope $b_i$ encodes both the direction and the magnitude of species $i$'s response to the environmental anomaly $z_i(t)$. Three response treatments are used throughout, and I refer to them by the same names in text, tables and figures:

* **Mixed** responses: $b_i$ evenly spaced in $[-0.5, 0.5]$. Positive and negative slopes occur in equal numbers; odd-richness communities also contain one zero-response species. The slopes sum to zero, so this treatment is balanced in its unweighted responses.
* **Matched aligned** responses: the same slope magnitudes as the mixed treatment, all made nonnegative, $b_i = |b_i^{\mathrm{mixed}}|$. This treatment differs from the mixed treatment only in response sign.
* **Steep aligned** responses: $b_i$ evenly spaced in $[0.1, 1.0]$. All species respond positively, and root-mean-square slope is greater than in the other two treatments, so this contrast changes response magnitude as well as direction.

Existing figure legends label the matched aligned treatment "aligned, matched magnitude" in Figure 1 and "positive matched" in the Supporting information. The steep aligned treatment is labelled "aligned" or "aligned positive" in the other displays; captions identify each comparison.

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
where $\sigma_{\mathrm{env}}$ is the innovation standard deviation, $\rho_{\mathrm{env}}$ is the requested cross-species correlation in exposure, and $C(\rho_{\mathrm{env}})$ is the equicorrelation matrix with ones on the diagonal and $\rho_{\mathrm{env}}$ off the diagonal. For equicorrelated innovations, positive definiteness requires $\rho > -1/(S-1)$, and the matrix is singular at $\rho=1$. The implementation therefore uses the effective value
\[
\rho_{\mathrm{eff}} = \min\!\left(\max\!\left(\rho_{\mathrm{env}}, -\tfrac{1}{S-1} + \epsilon\right), 1 - \epsilon\right),
\]
with $\epsilon = 10^{-6}$. Simulations are generated using $\rho_{\mathrm{eff}}$, and both requested and effective values are retained in outputs. Requested correlations outside the feasible interval are clipped at either boundary. In the present grids this affects the requested value of 1 and the $S=4$, requested $\rho_{\mathrm{env}}=-0.5$ treatment in Figure 5. I write "near-perfect correlation" for $\rho_{\mathrm{eff}}=1-10^{-6}$.

Under this convention, the stationary variance of each environmental component (for $|\phi| < 1$) is
\[
\operatorname{Var}(z_{i,t}) = \frac{\sigma_{\mathrm{env}}^2}{1 - \phi^2},
\]
so increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ increases environmental persistence and stationary variance together. When $\sigma_{\mathrm{env}} = 0$, the process is constant and the community dynamics reduce to the deterministic Ricker model.

Within a scenario, all species share $\phi$ and the requested $\rho_{\mathrm{env}}$. The environmental state is initialised at zero; one multivariate series is generated per replicate and scenario, and burn-in removes the initial transient.

### First-order covariance criterion

Let $w_i$ be the first-order contribution of species $i$ to the aggregate property of interest, and define the weighted response $a_i=w_i b_i$. For total abundance near a deterministic equilibrium, $w_i=N_i^\ast$; other ecosystem functions can have different contribution weights. If $F=\sum_i a_i z_i$ is the aggregate environmental forcing and $\Sigma_z$ is the stationary exposure covariance matrix, then
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
In words: when exposures are independent, only the sizes of the weighted responses matter; as exposures become more correlated, their sum matters more. For non-zero environmental variance, increasing exposure correlation reduces aggregate forcing variance exactly when $(\sum_i a_i)^2<\sum_i a_i^2$. If the weighted responses sum to zero, perfect correlation removes the first-order forcing entirely. The alignment index
\[
A=\frac{(\mathbf 1^\mathsf{T}\mathbf a)^2}{S\,\mathbf a^\mathsf{T}\mathbf a}
\]
ranges from 0, when the weighted responses sum to zero, to 1, when they are all identical. It places the forcing-variance boundary at $A=1/S$, with buffering when $A<1/S$.

A geometric reading helps later. An equicorrelation matrix has one common mode, the component of environmental variation shared by all species, and $S-1$ contrast modes, the components in which species' exposures differ. Increasing $\rho_{\mathrm{eff}}$ transfers exposure variance from the contrast modes to the common mode. A balanced weighted response vector is nearly orthogonal to the common mode and so gains nothing from that transfer; aligned responses project onto it and gain variance. Mixed signs alone do not guarantee cancellation, because unequal $w_i$ can unbalance the weighted responses.

The link from forcing to abundance variability depends on population feedback [@ives1999StabilityVariabilityCompetitive]. At the equal-$K$ equilibrium, the deterministic Jacobian has a common-mode eigenvalue $\lambda_c=1-r_0$, governing fluctuations in total abundance, and a contrast-mode eigenvalue
\[
\lambda_d=1-r_0\frac{1-\alpha_{\mathrm{inter}}}{1+\alpha_{\mathrm{inter}}(S-1)}
\]
for $\alpha_{\mathrm{intra}}=1$, governing fluctuations in the differences among species. At the default $r_0=1$, $S=4$ and $\alpha_{\mathrm{inter}}=0.3$, these are $\lambda_c=0$ and $\lambda_d\approx0.63$: the linearised total-abundance mode has no direct carryover from one step to the next, whereas differences among species decay slowly. Temporal memory can still enter through the environmental forcing. For equal $K_i$, the linearised departure of total abundance from equilibrium, $X_t$, follows the common mode alone,
\[
X_{t+1}=\lambda_c X_t+F_t.
\]
All exposures share the same temporal autocorrelation, so $F_t$ is also AR(1). At a stable equilibrium,
\[
\operatorname{Var}(X)=\operatorname{Var}(F)
\frac{1+\lambda_c\phi}{(1-\lambda_c^2)(1-\lambda_c\phi)}.
\]
For fixed $r_0$ and $\phi$, this multiplier cancels when comparing exposure correlations. The forcing criterion therefore gives the exact correlation effect on stationary total-abundance variance in the linearised equal-$K$ model. Two things can break this correspondence. With unequal $K_i$, equilibrium weights and the feedback matrix both change, and total abundance no longer follows this scalar recurrence (Supporting information). In the full nonlinear model, products of abundance deviations and growth responses can contribute to total abundance even when the first-order forcing cancels. A local second-order expansion in the Supporting information shows this route without assigning it the full observed departure. The simulations test how much these two departures matter for temporal CV.

### Simulation design

A scenario is defined by a response treatment, species richness $S$, innovation standard deviation $\sigma_{\mathrm{env}}$, requested exposure correlation $\rho_{\mathrm{env}}$, temporal autocorrelation $\phi$, and the population parameters. Every production scenario uses 1000 replicate trajectories of 600 time steps, with the first 300 discarded as burn-in. The main model and simulation settings are summarised in Table 1.

The magnitude-matched sign contrast in Fig. 1A compares mixed and matched aligned responses at $S\in\{4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}=0$ to 1 in increments of 0.1. Under symmetric Gaussian exposure, the two treatments have identical species-level forcing distributions; only their cross-species covariance differs. The same production grid includes the steep aligned treatment, shown in the Supporting information.

The boundary test in Fig. 1B,C uses $S=4$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}\in\{0,1\}$. Its response-alignment path rotates the mixed vector continuously into the matched aligned vector,
\[
\mathbf b(q)=\cos(\pi q/2)\,\mathbf b_{\mathrm{mixed}}+\sin(\pi q/2)\,|\mathbf b_{\mathrm{mixed}}|,
\]
for nine equally spaced $q\in[0,1]$. The two endpoint vectors are orthogonal and have equal norm, so this rotation holds $\lVert\mathbf b\rVert$ constant. A separate abundance-weighting path retains $\mathbf b_{\mathrm{mixed}}$ and sets
\[
\mathbf K(d)=100(1-0.3d,\,1-0.1d,\,1+0.1d,\,1+0.3d)
\]
for $d\in\{0.25,0.5,0.75,1.0,1.1\}$, with $d=0$ supplied by the mixed endpoint. The sum of $K_i$ is always 400, which holds deterministic total abundance constant under symmetric competition, while the equilibrium weights become progressively less even. All treatments retain a positive interior equilibrium. This path changes the dynamical feedback matrix as well as the equilibrium weights; it does not isolate weighting alone. Because $r_0=1$ makes the common mode memoryless ($\lambda_c=0$), Fig. 1C repeats the mixed and matched aligned endpoints at $r_0\in\{0.25,0.5,1.0,1.5\}$.

For the imposed-versus-realised synchrony comparison (Fig. 2), simulations use mixed and steep aligned responses at $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested $\rho_{\mathrm{env}}$ from 0 to 1 in increments of 0.1.

For the broader environmental-variance contrast (Fig. 3), simulations use $S=4$ mixed and steep aligned communities with $\phi=0.4$. The core grid crosses 19 values of $\sigma_{\mathrm{env}}$ between 0 and 2 with 15 requested $\rho_{\mathrm{env}}$ values between -0.3 and 1.0. A high-variance extension adds $\sigma_{\mathrm{env}}\in\{2.25,2.5,2.75,3.0,3.5,4.0\}$ on the same requested-correlation grid; values $\sigma_{\mathrm{env}}\ge3$ are marked as the highest-stress region in Fig. 3B.

For the richness assembly sequence (Fig. 4), a mixed-response grid uses $S\in\{2,3,4,5,6,7,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1.0,1.5,2.0\}$, non-negative requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1.0\}$, and $\phi=0.4$. Figure 4 averages scenario means over the shared effective-correlation values for each $S$ and $\sigma_{\mathrm{env}}$. Because the slope vector is regenerated as an evenly spaced sequence for each $S$, this grid changes response composition, root-mean-square slope, and deterministic total abundance together; it does not identify a causal effect of richness alone.

To examine a fixed-innovation stress gradient (Fig. 5), mixed-response simulations use $\sigma_{\mathrm{env}}=0.5$, $S\in\{2,4\}$, $\rho_{\mathrm{env}}\in\{-0.5,-0.25,0,0.25,0.5,0.75,0.9,1.0\}$, and $\phi\in\{0,0.7,0.9,0.95\}$. This design deliberately changes temporal autocorrelation and stationary variance together.

A fixed base seed is combined with scenario and replicate indices to generate deterministic seeds. Seeds are distinct among replicates within each scenario, and environmental realisations are not paired across treatments. Simulations and analyses use Python 3.12; versioned specifications and the software environment are supplied in the anonymous reproducibility package. Replicate summaries are aggregated into the submitted tables and figures by a single analysis workflow. Implementation details and additional checks are provided in the Supporting information.

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
Thus $R_{\mathrm{CV}^2}<1$ means that near-perfect exposure correlation reduces community variability relative to independent exposures, and $R_{\mathrm{CV}^2}>1$ means that it increases variability. The first-order forcing benchmark for the same contrast is $(1-\rho_{\mathrm{eff}})+\rho_{\mathrm{eff}}SA$, which equals $SA$ to within $10^{-6}$ at the near-perfect endpoint. It predicts $R_{\mathrm{CV}^2}\approx0$ for a perfectly balanced community and $R_{\mathrm{CV}^2}=S$ for a perfectly aligned one.

**Synchrony indices.** Let $v_i$ be the temporal variance of species $i$'s abundance and $\sigma_i=\sqrt{v_i}$ its standard deviation. Abundance-based community synchrony is quantified using the Loreau–de Mazancourt index [@loreau2008SpeciesSynchronyIts],
\[
\phi_{\mathrm{LdM}} = \frac{\operatorname{Var}(N_{\mathrm{tot}})}{\left(\sum_{i=1}^S \sigma_i\right)^2}.
\]
In exact arithmetic $\phi_{\mathrm{LdM}}$ lies in $[0,1]$; computed values are clipped to that interval to remove rounding overshoot.

To capture realised synchrony in population dynamics, per-capita log-growth rates are computed as
\[
g_i(t) = \log[N_i(t+1)+N_{\min}] - \log[N_i(t)+N_{\min}],
\]
where the implementation adds a further numerical offset $N_{\min}$ after flooring abundances. The correlation matrix of $g_i(t)$ across time is formed, and the mean of its off-diagonal elements is taken. This mean pairwise realised per-capita log-growth correlation can be negative when species exhibit compensatory dynamics. Unlike the first-order $b_i z_i(t)$ response term above, this realised metric includes density dependence, abundance feedbacks, floor effects where present, and nonlinearities introduced by the Ricker map. When $\sigma_{\mathrm{env}} = 0$, growth-rate variance is zero and this correlation is undefined; such scenarios are excluded from correlation-based synchrony panels.

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

**Interpretation.** Insurance is interpreted as relative stabilisation under matched environmental forcing. At fixed richness, lower $\mathrm{CV}_{\mathrm{tot}}$ for mixed than for aligned responses indicates compensatory insurance. Along the deterministic assembly sequence, lower $\mathrm{CV}_{\mathrm{tot}}$ at larger $S$ is an observed sequence-level pattern rather than an estimate of the effect of richness alone. Lower $\phi_{\mathrm{LdM}}$ or realised log-growth correlation diagnoses a compensatory pathway; it is not an additional criterion in the definition.

### Monte Carlo uncertainty

Each scenario is represented by 1000 replicates. Monte Carlo uncertainty in mean $\mathrm{CV}_{\mathrm{tot}}$ is small relative to the contrasts reported below. At $\sigma_{\mathrm{env}}=0.5$, $\rho_{\mathrm{eff}}=0.5$, and $S=4$, for example, the mixed and matched aligned means are 0.084 and 0.149, and the replicate standard deviation of $\mathrm{CV}_{\mathrm{tot}}$ in the mixed treatment is 0.0045, giving a standard error of the mean of about 0.00014. Scenario means of $\mathrm{CV}_{\mathrm{tot}}$ are therefore reported to three decimal places. For ratios in Fig. 1B,C, 95% Monte Carlo intervals are calculated on the log ratio by the delta method from the replicate-level distributions of $\mathrm{CV}_{\mathrm{tot}}^2$.

### Numerical and ecological checks

Numerical checks verify the environmental covariance construction, stationary environmental variance, and deterministic model limits. The boundary treatments retain a positive deterministic equilibrium, hold response norm constant along the rotation, and hold deterministic total abundance constant along the $K_i$ path. The sign contrast across $r_0$ tests whether the result depends on the memoryless common mode at $r_0=1$. Additional metric and implementation checks are described in the Supporting information.

The retained numerical-guard diagnostic uses 30 replicates in each of three stress scenarios at $\sigma_{\mathrm{env}}=1.0$ or 1.5. No high-side exponent clipping occurred, and scenario-mean low-side clipping fractions ranged from 0.00024 to 0.0070 over the full trajectories. These diagnostic rates are distinct from the post-burn-in production floor frequencies (Supporting information). Floor occupancy was very low in the main inference grids: in the richness grid for Fig. 4, the maximum scenario mean is about 0.0014 even at $\sigma_{\mathrm{env}}=2.0$, so the reported richness pattern is not driven by repeated contact with the numerical floor. Occupancy rises in the explicitly labelled high-$\sigma_{\mathrm{env}}$ and high-$\phi$ extensions (Supporting information), so those regions are interpreted as numerical and ecological stress tests rather than as clean mechanistic evidence.

## Results

### Reversing response signs alone reverses the effect of exposure correlation

The mixed and matched aligned treatments are indistinguishable under independent exposures, then diverge as $\rho_{\mathrm{eff}}$ rises (Fig. 1A). At $S=4$ and $\rho_{\mathrm{eff}}=0$, both have mean $\mathrm{CV}_{\mathrm{tot}}=0.106$; this equality is expected, because the two treatments have identical marginal forcing distributions and differ only in cross-species covariance. At $\rho_{\mathrm{eff}}=0.5$, the mixed treatment falls to 0.084 while the same slope magnitudes aligned in one direction rise to 0.149. Near $\rho_{\mathrm{eff}}=1$, the contrast widens to 0.060 versus 0.184. The corresponding $S=8$ values at $\rho_{\mathrm{eff}}=0.5$ are 0.059 and 0.120. Because every species' marginal forcing distribution is preserved, this separation is attributable to the sign-dependent cross-species covariance rather than to slope magnitude.

### Weighted alignment captures the broad transition, with nonlinear departures

The continuous response rotation confirms the transition from buffering to amplification predicted by the first-order criterion, and also shows where that criterion fails quantitatively (Fig. 1B). At the mixed endpoint ($A=0$), the benchmark predicts a high-correlation to independent-exposure variance ratio near zero in the linearised model. The simulated ratio is 0.320 (95% Monte Carlo interval 0.315--0.325). About a third of the independent-exposure mean squared CV therefore remains when the linear forcing cancels. At the matched aligned endpoint ($A=0.8$), the benchmark predicts 3.2 and the simulation gives 2.99 (2.97--3.02). Most ratios along the rotation are closer to one than their benchmark values, but the nearest tested point below the forcing boundary crosses to the opposite side of one. The nonlinear crossing of $R_{\mathrm{CV}^2}=1$ is displaced to lower alignment than the benchmark value $A=1/S=0.25$: it is bracketed by the tested points at $A=0.117$ (ratio 0.666) and $A=0.247$, where the benchmark predicts weak buffering (0.988) but the simulation shows weak amplification (1.043; 1.028--1.059). The criterion captures the broad transition and endpoint contrast, but not the exact nonlinear threshold or effect size.

The unequal-$K_i$ path also crosses from buffering to amplification while preserving the mixed response vector and deterministic total abundance. Along the $K_i$ path, the total equilibrium remains 210.5. At $A=0.230$, $R_{\mathrm{CV}^2}=0.964$ (0.952--0.975); at $A=0.257$, it is 1.053 (1.041--1.065). The most uneven treatment retains a positive minimum equilibrium abundance of 5.49, and its maximum scenario-mean floor occupancy is $1.6\times10^{-5}$; all other boundary-test scenarios have zero floor occupancy. Thus mixed signs cease to stabilise along this path as equilibrium weights and population feedback change, with the tested points on either side of one bracketing the forcing boundary. At the upper point the benchmark predicts 1.030, so it slightly underpredicts amplification on this path.

The sign reversal survives changes in local density-feedback dynamics (Fig. 1C). Across $r_0=0.25,0.5,1.0,$ and 1.5, $R_{\mathrm{CV}^2}$ for mixed responses is 0.663, 0.439, 0.320, and 0.323, respectively; the corresponding matched aligned ratios are 2.77, 2.94, 2.99, and 2.97. The result is therefore not confined to $r_0=1$, where the linearised common mode has no direct abundance carryover.

### Response direction transforms exposure correlation into realised synchrony

At $\sigma_{\mathrm{env}}=0.5$, realised per-capita log-growth correlations in mixed communities fall well below $\rho_{\mathrm{eff}}$ as exposure correlation increases (Fig. 2A). Near $\rho_{\mathrm{eff}}=1$, mean realised correlations are approximately -0.81 for $S=2$, where the two species have exactly opposite slopes, -0.16 for $S=4$, and 0.08 for $S=8$. In the steep aligned treatment they remain strongly positive—approximately 0.64, 0.81, and 0.86, respectively—and increase with $\rho_{\mathrm{eff}}$ (Fig. 2B). The difference $\mathrm{corr}_{\mathrm{realised}}-\rho_{\mathrm{eff}}$ consequently becomes strongly negative for mixed responses (Fig. 2C).

The matched aligned control gives the same contrast without changing slope magnitudes. Near $\rho_{\mathrm{eff}}=1$, realised growth correlation is -0.16 for mixed and 0.90 for matched aligned responses at $S=4$; at $S=8$ the corresponding values are 0.08 and 0.84 (Supporting information). Requested exposure correlation is therefore a property of the forcing, not a proxy for biological synchrony.

### Environmental-variance, assembly-sequence, and persistence extensions

The steep aligned treatment maps the same contrast over environmental innovation SD. Its larger slopes increase absolute variability, so it is not a sign-only control, but it shows where aligned responses enter severe boom–bust dynamics as $\sigma_{\mathrm{env}}$ increases (Fig. 3). Mixed responses remain less variable across the shared grid. The relative contrast persists in the high-$\sigma_{\mathrm{env}}$ extension, although the highest forcing levels are floor-affected stress cases rather than clean equilibrium fluctuations.

Along the prespecified mixed-response assembly sequence, mean $\mathrm{CV}_{\mathrm{tot}}$ declines from $S=2$ to $S=8$ at every non-zero $\sigma_{\mathrm{env}}$ after averaging over the shared non-negative correlation grid (Fig. 4). At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, for example, mean CV is approximately 0.15, 0.08, and 0.06 for $S=2,4,$ and 8; the $S=4$ and $S=8$ values agree with the independently simulated grid in Fig. 1A. This sequence also lowers root-mean-square response magnitude and raises mean total abundance, so the decline cannot be assigned to richness alone. The variance decomposition shows negative aggregate covariance at the selected $S=2,4,$ and 8 scenarios, but total variance and covariance magnitude do not change monotonically at every step (Supporting information).

Increasing $\phi$ at fixed innovation SD creates a compound temporal-autocorrelation and stationary-variance gradient (Fig. 5). At $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, mean $\mathrm{CV}_{\mathrm{tot}}$ rises from approximately 0.14 at $\phi=0$ to 0.58 at $\phi=0.95$ for $S=2$, and from 0.07 to 0.35 for $S=4$. The assembly-sequence ordering persists, while the decline in CV with $\rho_{\mathrm{eff}}$ weakens or reverses locally at the most persistent edge. Floor occupancy is essentially absent through $\phi\le0.7$, reaches a maximum scenario mean of about 0.005 at $\phi=0.9$, and rises to 0.049 at $\phi=0.95$. The final treatment is therefore a fixed-innovation stress case, not evidence for an isolated effect of temporal autocorrelation.

## Discussion

### Weighted cancellation and population feedback

Positive correlation in exposure can stabilise an aggregate because it changes which environmental mode carries the variance. Under equicorrelation, higher $\rho_{\mathrm{eff}}$ concentrates variance in the common mode, the component of variation that all species share, and removes it from the contrast modes, the components in which species differ. Aggregate forcing variance is reduced when the abundance-weighted response vector has little projection onto that common mode. The condition $(\sum_i a_i)^2<\sum_i a_i^2$, or $A<1/S$, states this directly. Opposing response signs make cancellation possible, but they are not sufficient: a negative responder that contributes little abundance or function cannot offset a dominant positive responder.

The simulations support the predicted contrast between mixed and aligned responses and, at the same time, measure how much of the predicted buffering nonlinear dynamics take back. Reversing the signs of otherwise identical slopes reverses the effect of exposure correlation, and both the response-rotation and unequal-abundance paths cross from buffering to amplification near the benchmark boundary. But the benchmark predicts almost complete buffering for a perfectly balanced community, whereas the model retains about a third of its independent-exposure mean squared CV under near-perfect correlation. Linear cancellation does not imply constant total abundance in the nonlinear model. Products of abundance deviations and growth responses, including quadratic terms from the Ricker update, can contribute to total abundance even when the first-order forcing cancels (Supporting information). This provides a route for the remaining variability, but the present comparisons do not separate these contributions or establish their individual effects on the threshold. The criterion therefore captures the broad transition and endpoint contrast, with departures in both magnitude and, near the rotation threshold, direction.

Changing intrinsic growth rate also changes equilibrium abundance and both common and contrast population modes. Mixed and matched aligned treatments remain on opposite sides of $R_{\mathrm{CV}^2}=1$ across $r_0=0.25$--1.5. The persistence of that sign contrast is the supported result; its changing magnitude cannot be attributed to common-mode memory alone.

The matched aligned control separates response sign from the magnitude effect present in the steep aligned treatment, whose large absolute CV partly reflects steeper slopes. Realised growth correlations in Fig. 2 and the Supporting information show the next step in the transmission: the same positive exposure correlation produces compensatory or strongly synchronous population growth depending on response orientation. These correlations are dynamical diagnostics, not formal mediation estimates. Likewise, $\phi_{\mathrm{LdM}}$ shares total-abundance variance with community CV and should not be treated as independent confirmation [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability].

The physical orientation of exposure is part of the claim. Temperature, moisture, or another measured variable must have the same positive direction for every species. If each $z_i$ is an independently defined latent axis that can be reversed, exposure correlation and response sign are coordinate choices rather than separately identifiable ecological quantities. In that case the invariant object is the demographic-shock covariance $D_b\Sigma_zD_b$, where $D_b=\operatorname{diag}(b_1,\ldots,b_S)$. This distinction matters when empirical response models use species-specific latent gradients.

### What should be measured in real communities?

Richness counts do not reveal the weighted response vector. An empirical test needs three linked quantities: covariance among commonly oriented exposures, species response slopes on those axes, and contributions to the aggregate property. For total abundance the natural initial weights are equilibrium or mean abundances; for biomass, productivity, or multifunctionality they may differ. The forcing benchmark predicts buffering when dominant contributors cancel along the environmental modes that gain variance; predicting the size of that buffering additionally requires attention to population feedback.

This prediction sharpens the response-diversity concept [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines]. Empirical work already shows that synchrony can explain more variation in community stability than richness [@valencia2020SynchronyMattersMore] and that asynchrony or statistical averaging can dominate in different systems [@hector2010GeneralStabilizingEffects; @zhao2022BiodiversityStabilizesPlant; @wagg2021DiversityAsynchronySoil]. Time-varying response diversity in Lake Geneva also had context-dependent effects on phytoplankton and zooplankton biomass [@hsieh2026QuantifyingEffectsResponse]. The alignment criterion identifies one reason for such context dependence: the same list of response signs can have different consequences after abundance weights or environmental covariance change.

Real communities also face several environmental variables. A community can be balanced along one covariance mode and aligned along another, so a single unweighted response-diversity index can combine stabilising and destabilising components [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. An aggregate linear response still has a forcing variance of the form $\mathbf a^\mathsf{T}\Sigma_z\mathbf a$, with coefficients and covariance dimensions expanded to cover the relevant exposures. Estimation then requires response surfaces and function-specific weights [@polazzo2024MeasuringResponseDiversity; @sasaki2026BiologicalTraitsPredict].

### Richness and temporal structure are conditional extensions

The decline in CV from $S=2$ to $S=8$ is specific to the implemented assembly sequence. Adding species fills the fixed interval $[-0.5,0.5]$ with intermediate slopes; odd-richness communities gain a zero-response species; root-mean-square slope decreases; and deterministic total abundance rises. Statistical averaging, covariance cancellation, changing forcing magnitude, and a larger CV denominator therefore move together. The result shows that this particular sequence becomes more stable, not that richness independently causes the decline. That interpretation is consistent with theory and data placing covariance structure closer to community stability than richness itself [@demazancourt2013PredictingEcosystemStability; @valencia2020SynchronyMattersMore; @danet2025ResponseDiversityMajor].

Figure 5 has a similarly narrow interpretation. Holding innovation SD fixed while increasing $\phi$ raises temporal autocorrelation and stationary exposure variance together. The mixed-response assembly ordering survives that compound stress gradient, but the design does not identify a pure temporal-autocorrelation effect or test the matched sign contrast across $\phi$. The floor-affected $\phi=0.95$ edge is useful as a model boundary, not as stronger evidence for the mechanism.

### Scope of the model

The analysis deliberately holds much of community structure fixed. Competition is symmetric, responses are linear in one exposure, and demographic stochasticity, observation error, spatial population exchange, and trophic interactions are absent. The $r_0$ sensitivity removes dependence on one special Ricker growth rate, but it does not establish invariance to alternative density-dependence functions or asymmetric interaction matrices. Those processes can alter the dynamical weights linking environmental shocks to aggregate abundance [@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial].

Equicorrelation makes the common and contrast modes transparent. Spatially heterogeneous, block-correlated, or empirically estimated covariance matrices will have different eigenvectors. Their effects on aggregate forcing variance depend on projections of the weighted response vector onto those modes [@loreau2003BiodiversitySpatialInsurance; @shanafelt2015BiodiversityProductivitySpatial]. The unequal-$K_i$ treatments show that changing species contributions and feedback together can move the community across the buffering boundary. The present simulations support the mechanism for one nonlinear community model and a limited set of departures from symmetry; they do not estimate its frequency or magnitude in nature.

The numerical floor is a computational safeguard, not biological extinction. It is negligible in the matched-sign and weighted-boundary tests, but participates in the high-variance and high-$\phi$ stress extensions. Finally, stability here means temporal CV of total abundance. Resistance, resilience, recovery, and multifunctional stability may respond differently to the same response structure [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept; @kunze2026SpeciesInteractionsDetermine].

### Conclusion

For commonly oriented exposures, environmental correlation reduces aggregate forcing variance when abundance-weighted responses cancel and increases it when they align. In this Ricker model, reversing response signs alone reverses the effect of exposure correlation on community variability. Continuous changes in response balance and equilibrium abundances produce a broad transition from buffering to amplification near the forcing benchmark. The nonlinear departures matter: the balanced community retains 0.32 of the independent-exposure mean squared CV, while near the rotation threshold the benchmark and simulation predict opposite directions. Empirical tests of insurance should therefore measure exposure covariance, species response slopes, and species' contributions to the aggregate together, and use the covariance criterion alongside an assessment of the population feedbacks that transmit environmental fluctuations.

## Artificial intelligence statement

OpenAI Codex large language models assisted with model and code development, simulation and analysis workflows, literature searches, and drafting and editorial revision. Anthropic Claude assisted with literature checking, scientific review, and editorial revision. The author reviewed all AI-assisted material incorporated into the work and takes full responsibility for the final content.

## References
