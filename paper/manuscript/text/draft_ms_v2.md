# Biodiversity buffers correlated environmental variability through divergent species responses

## Abstract

Environmental variability is usually destabilising, yet biodiversity can buffer aggregate ecosystem properties when species respond asynchronously. Correlated forcing is a difficult case: response diversity must convert shared variation into compensatory rather than synchronous dynamics. I used a symmetric stochastic multispecies Ricker model in which species differed only in their signed responses to correlated autoregressive environmental anomalies. Across complementary simulation grids, I contrasted slopes balanced across positive and negative values with aligned positive slopes and a magnitude-matched control, while evaluating environmental variance, cross-species driver correlation, richness, temporal persistence, competition, and slope magnitude. Insurance was measured as lower variation in total abundance under matched forcing, with abundance and realised per-capita log-growth synchrony as mechanistic diagnostics. Balanced mixed slopes drove realised log-growth synchrony well below the imposed driver correlation and sometimes below zero. At an environmental innovation standard deviation of 0.5, effective driver correlation of 0.5, and richness of four species, the mean coefficient of variation of total abundance was 0.084 with mixed slopes and 0.263 with aligned slopes. Along the mixed-slope assembly sequence, variability declined with richness and often with increasing driver correlation; aligned communities showed the opposite correlation response and remained more variable at greater richness. Removing interspecific competition and narrowing response slopes did not reverse the central contrast. In this model, correlated forcing generated strong compensatory insurance when balanced opposing sensitivities converted shared anomalies into opposing growth responses. Richness alone was insufficient: stabilisation depended on which responses were added and how they aligned with environmental covariance.

## Keywords

biodiversity; response diversity; ecosystem stability; species synchrony; environmental covariance; stochastic community dynamics; insurance hypothesis.

## Introduction

Environmental variability generally destabilises populations: as climatic and other drivers fluctuate, population abundances tend to vary more through time, increasing the risk of low-abundance episodes and local collapse [@ives2007StabilityDiversityEcosystems]. The insurance hypothesis makes a conditional prediction about this problem: biodiversity can buffer ecosystem functioning when different species respond differently in space or time, so that declines in some species are offset by increases in others [@yachi1999BiodiversityEcosystemProductivity]. Borrowing from portfolio theory, the hypothesis predicts that aggregate ecosystem properties such as total biomass or productivity should fluctuate less in diverse communities than in species-poor systems subject to the same environmental variance [@loreau2021BiodiversityInsuranceConcept]. Experiments and syntheses show that biodiversity can stabilise ecosystem functioning [@loreau2013BiodiversityEcosystemStability; @demazancourt2013PredictingEcosystemStability; @wagg2021DiversityAsynchronySoil], but they also show that the strength, and sometimes the sign, of diversity–stability relationships depends on the mechanism generating species covariances [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept].

Synchrony among species’ fluctuations is the direct route from species-level responses to community-level variability. When species respond similarly to environmental variation, community-level variability tends to scale with typical species-level variability; when responses are asynchronous or negatively correlated, aggregate variability can be much lower than the sum of its parts [@doak1998StatisticalInevitabilityStabilitydiversity; @loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability]. Formal measures such as the variance ratio, Loreau–de Mazancourt’s synchrony index $\phi_{\mathrm{LdM}}$, and related covariance-based metrics link species-level variances and covariances to community-level stability [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability; @demazancourt2013PredictingEcosystemStability]. Insurance can refer to effects on mean functioning, effects on variability, or both; claims of stabilisation also depend on the comparison used [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept]. Here I use relative stabilisation: lower community variability than an appropriate baseline under the same forcing, not an absolute decline in variability as environmental variance increases.

Response diversity identifies the component of biodiversity most relevant to this mechanism: variation in how species respond to environmental change [@elmqvist2003ResponseDiversityEcosystem]. Species within a functional group may be redundant for mean functioning yet differ in response slopes and tolerances, generating compensation [@mori2013ResponseDiversityDetermines]. Its stabilising role remains sparsely tested, and definitions and metrics vary [@ross2024LimitedTheoreticalEmpirical; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. A recent expert survey found similar disagreement over definitions and stability dimensions, especially where biotic interactions combine with abiotic responses [@ross2026ExpertledPrioritiesResponse]. Empirical work increasingly treats response diversity as dynamic and context dependent, linking time-varying diversity to stability, biological traits to responses under multiple drivers, and pulse-disturbance outcomes to species interactions [@hsieh2026QuantifyingEffectsResponse; @sasaki2026BiologicalTraitsPredict; @kunze2026SpeciesInteractionsDetermine].

General stochastic theory links synchrony to shared environmental drivers, competition, demographic noise, and species covariance structure [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability], while recent food-web modelling shows that response diversity can determine the sign of the richness–stability relationship [@danet2025ResponseDiversityMajor]. Other models often encode response differences implicitly through niche axes and competition coefficients or prescribe covariance among demographic rates without mapping environmental exposures through response traits to realised synchrony [@shanafelt2015BiodiversityProductivitySpatial]. The unresolved gap is therefore narrower than a lack of dynamical theory: few models isolate how signed response slopes and covariance among environmental exposures combine to generate species covariances.

Empirical studies likewise identify synchrony and covariance structure, rather than richness alone, as the quantities closest to temporal stability. Across a global compilation of plant communities, species synchrony explained more variation in community stability than richness [@valencia2020SynchronyMattersMore]. Grassland and soil experiments show stabilisation through population or taxon asynchrony and overyielding [@hector2010GeneralStabilizingEffects; @wagg2021DiversityAsynchronySoil], whereas other plant experiments identify statistical averaging rather than compensatory dynamics [@zhao2022BiodiversityStabilizesPlant]. In an alpine grassland, nitrogen addition reduced stability first through increased synchrony and later through population variability and diversity loss [@song2026NitrogenAdditionReduces]. These studies treat synchrony as an observed covariance summary; they do not by themselves explain how environmental covariance and response traits combine to produce it.

The remaining task is to connect these elements transparently: when do response differences produce insurance, when do they fail, and how do correlated exposure and environmental persistence modify the outcome [@loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @ross2026ExpertledPrioritiesResponse]?

I use a deliberately stylised model to isolate this mechanism. Stochastic multispecies communities follow a symmetric Ricker model, chosen for its simple analytic equilibrium and familiar discrete-time dynamics. Each species experiences the same type of environmental variable, but through a species-specific trajectory drawn from a multivariate AR(1) process. The requested pairwise correlation $\rho_{\mathrm{env}}$ controls how similar those exposures are. Species differ only in the sign and magnitude of their response slopes: mixed positive and negative slopes represent divergence in response direction, whereas all-positive slopes represent aligned responses. I vary innovation variance, imposed driver correlation, richness, and temporal autocorrelation; control simulations alter competition and slope magnitudes.

Insurance and stabilisation are defined in relative terms. The analysis quantifies (i) the coefficient of variation (CV) of total community abundance, (ii) an approximate species-level CV, and (iii) Loreau–de Mazancourt synchrony $\phi_{\mathrm{LdM}}$ and mean pairwise realised per-capita log-growth correlation. Within a slope regime, lower community CV at greater richness indicates stronger insurance relative to a lower-richness community under matched environmental forcing. At fixed richness, lower community CV in mixed- than aligned-response communities indicates stronger compensatory insurance. The synchrony metrics diagnose whether that reduction is associated with compensatory dynamics; they are not part of the definition of insurance itself. Comparing imposed driver correlation with realised synchrony then shows how response directions alter the translation from environmental covariance to species covariances.

The analysis asks three questions. When does response diversity turn correlated environmental variation into compensatory dynamics rather than amplify fluctuations? How do species’ response directions alter the mapping from imposed environmental correlation to realised synchrony? Do the resulting insurance patterns persist across environmental variance, a combined persistence–stationary-variance gradient, and competition controls? The model retains nonlinear population feedbacks while keeping the covariance mechanism visible [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity]. Nearly unit $\rho_{\mathrm{env}}$ gives species almost identical trajectories; lower correlations can represent spatial or phenological differences in exposure to the same environmental variable.

## Methods 

### Community dynamics

I model a community of $S$ species using a discrete-time stochastic Ricker model with symmetric competition. Let $N_i(t)$ denote the abundance of species $i$ at time $t$. In the absence of environmental variation, per-capita growth follows
\[
N_i(t+1) = N_i(t)\exp\left[r_0 - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right],
\]
where $r_0$ is a shared intrinsic growth rate, $K_i$ is the carrying capacity of species $i$, $\alpha_{\mathrm{intra}}$ is intraspecific competition, and $\alpha_{\mathrm{inter}}$ is interspecific competition. I set $r_0=1$, $K_i = 100$ for all species, $\alpha_{\mathrm{intra}} = 1$, and $\alpha_{\mathrm{inter}} = 0.3$ unless otherwise stated. In the general symmetric case the deterministic equilibrium is
\[
N_i^\ast = \frac{r_0 K_i}{\alpha_{\mathrm{intra}} + \alpha_{\mathrm{inter}}(S-1)},
\]
which reduces to $K_i/[\alpha_{\mathrm{intra}} + \alpha_{\mathrm{inter}}(S-1)]$ for the value $r_0=1$ used in the main simulations.

Environmental variation enters as a linear response term $b_i z_i(t)$ in the per-capita growth rate:
\[
N_i(t+1) = N_i(t)\exp\left[r_0 + b_i z_i(t) - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right].
\]
Species differ only in their response slopes $b_i$, which encode both the direction and magnitude of their response to the environmental anomaly $z_i(t)$. Four slope regimes are considered:

* Mixed slopes: $b_i$ evenly spaced in $[-0.5, 0.5]$, giving both positive and negative responses.
* Positive slopes: $b_i$ evenly spaced in $[0.1, 1.0]$, giving aligned positive responses.
* Positive-matched (sign-structure control): aligned positive slopes with magnitudes matched to mixed slopes, $b_i = |b_i^{\mathrm{mixed}}|$.
* Mixed–narrow (sensitivity analysis): $b_i$ evenly spaced in $[-0.25, 0.25]$.

Abundances are floored at a small positive constant $N_{\min} = 10^{-9}$ to avoid numerical problems at zero, and the exponent in the growth term is capped at $\pm 50$ to prevent overflow in $\exp(\cdot)$. Initial abundances are set to $K_i/2$ for all species.

### Environmental process

Environmental anomalies are generated by a multivariate AR(1) process
\[
\mathbf{z}_t = \phi\,\mathbf{z}_{t-1} + \boldsymbol{\varepsilon}_t,\qquad
\boldsymbol{\varepsilon}_t \sim \mathcal{N}(\mathbf{0}, \Sigma)
\]
where $\mathbf{z}_t$ is an $S$-dimensional vector of environmental anomalies at time $t$, $\phi$ is the temporal autocorrelation, and $\Sigma$ is the covariance matrix of the innovation vector $\boldsymbol{\varepsilon}_t$. An equicorrelated covariance structure is used,
\[
\Sigma = \sigma_{\mathrm{env}}^2\,C(\rho_{\mathrm{env}})
\]
where $\sigma_{\mathrm{env}}$ is the innovation standard deviation, $\rho_{\mathrm{env}}$ is the imposed environmental correlation between species’ drivers, and $C(\rho_{\mathrm{env}})$ is the equicorrelation matrix with ones on the diagonal and $\rho_{\mathrm{env}}$ off-diagonal. For equicorrelated innovations, positive definiteness requires $\rho > -1/(S-1)$ and the matrix is singular at $\rho=1$. The implementation therefore treats $\rho_{\mathrm{env}}$ as a requested value and uses an effective value
\[
\rho_{\mathrm{eff}} = \min\!\left(\max\!\left(\rho_{\mathrm{env}}, -\tfrac{1}{S-1} + \epsilon\right), 1 - \epsilon\right),
\]
with small $\epsilon$. Simulations are generated using $\rho_{\mathrm{eff}}$, while both requested and effective values are retained in outputs.

Under this convention, the stationary variance of each environmental component (for $|\phi| < 1$) is
\[
\operatorname{Var}(z_{i,t}) = \frac{\sigma_{\mathrm{env}}^2}{1 - \phi^2},
\]
so increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ simultaneously increases environmental persistence and the effective stationary variance. When $\sigma_{\mathrm{env}} = 0$, the process is constant and the community dynamics reduce to the deterministic Ricker model.

For a given scenario, all species share the same $\phi$ and requested $\rho_{\mathrm{env}}$ but receive correlated environmental trajectories via the multivariate process (after clipping to $\rho_{\mathrm{eff}}$ where required). The environmental state is initialised at zero, and one multivariate time series is generated per replicate and scenario; the burn-in removes transients associated with that initial state.

The immediate covariance mechanism follows from the linear environmental response terms. Ignoring density dependence and abundance feedbacks for the moment,
\[
\operatorname{Cov}(b_i z_i, b_j z_j)
= b_i b_j\,\operatorname{Cov}(z_i,z_j)
= b_i b_j\,\rho_{\mathrm{eff}}\frac{\sigma_{\mathrm{env}}^2}{1-\phi^2}.
\]
For non-zero slopes, the corresponding response-term correlation is therefore $\operatorname{sign}(b_i b_j)\rho_{\mathrm{eff}}$: positively aligned slopes convert positive driver correlation into positive covariance in growth forcing, whereas opposite-signed slopes convert the same driver correlation into negative covariance. Near a symmetric equilibrium, the variance of the abundance-weighted first-order aggregate forcing is approximately
\[
\operatorname{Var}\!\left(\sum_i w_i b_i z_i\right)
=
\frac{\sigma_{\mathrm{env}}^2}{1-\phi^2}
\left[
\sum_i (w_i b_i)^2
+ 2\rho_{\mathrm{eff}}\sum_{i<j} w_i b_i w_j b_j
\right],
\]
where $w_i$ are abundance weights. For balanced mixed slopes and similar weights, cross-terms can cancel aggregate forcing as $\rho_{\mathrm{eff}}$ increases; for aligned slopes, they reinforce it. The simulations below ask how this first-order covariance structure is propagated, dampened, or distorted by nonlinear Ricker dynamics, competition, abundance weighting, richness, and numerical floor effects.

### Implementation environment

All simulations and analyses were implemented in Python 3.12 in a uv-managed environment. NumPy provides numerical arrays and random-number generation; pandas and PyArrow handle tabular summaries and parquet I/O; SciPy supplies numerical and statistical utilities; and Matplotlib generates the figures. Standard-library modules manage command-line orchestration and parallel execution. I used `pytest` for automated tests and `pyright` for static checking.

### Simulation design

A scenario is defined by a combination of slope regime, species richness $S$, innovation standard deviation $\sigma_{\mathrm{env}}$, imposed environmental correlation $\rho_{\mathrm{env}}$, temporal autocorrelation $\phi$, and competition strength $\alpha_{\mathrm{inter}}$. For each scenario, the model is run for $n_{\mathrm{steps}}$ time steps, discarding the first $n_{\mathrm{burn}}$ steps as burn-in.

The main model and simulation settings are summarised in Table 1.

For the main environmental-variance contrast (Fig. 1), simulations use $S=4$ mixed- and positive-slope communities with $\phi=0.4$, $n_{\mathrm{steps}}=600$, $n_{\mathrm{burn}}=300$, and 1000 replicates per scenario. The core grid crosses 19 values of $\sigma_{\mathrm{env}}$ between 0 and 2 with 15 requested $\rho_{\mathrm{env}}$ values between -0.3 and 1.0. A high-variance extension adds $\sigma_{\mathrm{env}}\in\{2.25,2.5,2.75,3.0,3.5,4.0\}$ on the same requested-correlation grid; values $\sigma_{\mathrm{env}}\ge3$ are marked as the highest-stress region in Fig. 1B.

For the richness and synchrony analyses (Figs. 2 and 4), a mixed-slope grid uses $S\in\{2,3,4,5,6,7,8\}$, $\sigma_{\mathrm{env}}\in\{0,0.2,0.5,1.0,1.5,2.0\}$, non-negative requested $\rho_{\mathrm{env}}\in\{0,0.25,0.5,0.75,1.0\}$, $\phi=0.4$, 600 steps, 300 burn-in, and 1000 replicates per scenario. Figure 2 averages scenario means over the non-negative effective-correlation grid for each richness and $\sigma_{\mathrm{env}}$, whereas Figure 4 uses the same simulation output to relate community variability to realised synchrony metrics after excluding the deterministic $\sigma_{\mathrm{env}}=0$ baseline.

For the imposed-versus-realised synchrony mechanism (Fig. 3), simulations use mixed and positive slope regimes at $S\in\{2,4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, non-negative requested $\rho_{\mathrm{env}}$ values from 0 to 1 in increments of 0.1, 600 steps, 300 burn-in, and 1000 replicates per scenario.

To examine the combined effects of environmental persistence and stationary variance, a $\phi$-sensitivity grid is run for mixed slopes at $\sigma_{\mathrm{env}} = 0.5$, with $\rho_{\mathrm{env}} \in \{-0.5, -0.25, 0, 0.25, 0.5, 0.75, 0.9, 1.0\}$, $S \in \{2, 4\}$, and $\phi \in \{0, 0.7, 0.9, 0.95\}$. These runs use $n_{\mathrm{steps}} = 600$, $n_{\mathrm{burn}} = 300$, and 1000 replicates per scenario.

To isolate response sign structure from slope-magnitude differences, an additional full-replicate control uses aligned positive slopes whose magnitudes match the mixed regime ($b_i = |b_i^{\mathrm{mixed}}|$). This positive-matched control uses $S \in \{4,8\}$, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, requested $\rho_{\mathrm{env}}=0$ to 1 in increments of 0.1, $n_{\mathrm{steps}}=600$, $n_{\mathrm{burn}}=300$, and 1000 replicates per scenario.

No-competition controls set $\alpha_{\mathrm{inter}} = 0$ (with $\alpha_{\mathrm{intra}} = 1$) for both mixed and positive slopes. These controls use reduced grids with $\sigma_{\mathrm{env}} \in \{0, 0.5, 1.0\}$, $\rho_{\mathrm{env}} \in \{-0.5, 0, 0.5, 0.9, 1.0\}$, $S \in \{2, 4, 8\}$, and $\phi = 0.4$, with 80 replicates per scenario.

Finally, a slope-magnitude sensitivity analysis uses the mixed–narrow regime (slopes $b_i$ evenly spaced in $[-0.25, 0.25]$). This grid matches the reduced $(\sigma_{\mathrm{env}}, \rho_{\mathrm{env}}, S)$ combinations of the no-competition controls at $\phi = 0.4$, again with 80 replicates per scenario.

In the 1000-replicate grids, a fixed base seed is combined with scenario and replicate indices to generate deterministic seeds. Seeds are distinct among replicates within each scenario, and environmental realisations are not deliberately paired across slope regimes. Scenario-level summaries are stored in parquet format and subsequently aggregated into CSV files and figures by the analysis scripts.

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

**Approximate mean species CV.** For each species, the temporal mean and variance are
\[
m_i = \mathbb{E}[N_i],\qquad v_i = \operatorname{Var}(N_i).
\]
An approximate mean species-level CV is then defined as
\[
\mathrm{CV}_{\mathrm{sp}} \approx
\frac{\sqrt{\frac{1}{S}\sum_{i=1}^S v_i}}{\frac{1}{S}\sum_{i=1}^S m_i},
\]
treating the mean of species variances and the mean of species means as proxies for a “typical” species.
Additional diagnostics are provided in the Supporting information.

**Synchrony indices.** Abundance-based community synchrony is quantified using the Loreau–de Mazancourt index [@loreau2008SpeciesSynchronyIts],
\[
\phi_{\mathrm{LdM}} = \frac{\operatorname{Var}(N_{\mathrm{tot}})}{\left(\sum_{i=1}^S \sigma_i\right)^2},
\]
where $\sigma_i = \sqrt{v_i}$ is the standard deviation of species $i$. To avoid numerical overshoots, $\phi_{\mathrm{LdM}}$ is clipped to the interval $[0, 1]$.

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

Scenario-level summaries are obtained by averaging replicate-level statistics for each unique combination of slope regime, $S$, $\sigma_{\mathrm{env}}$, requested $\rho_{\mathrm{env}}$, effective $\rho_{\mathrm{eff}}$, $\phi$, and $\alpha_{\mathrm{inter}}$.

“Insurance” is interpreted as relative stabilisation under matched environmental forcing. Within a slope regime, lower $\mathrm{CV}_{\mathrm{tot}}$ at greater richness indicates stronger insurance relative to a lower-richness community. At fixed richness, lower $\mathrm{CV}_{\mathrm{tot}}$ in mixed- than aligned-response communities indicates stronger compensatory insurance. Lower $\phi_{\mathrm{LdM}}$ or realised log-growth correlation diagnoses a compensatory pathway; it is not an additional criterion in the definition.

### Monte Carlo uncertainty

Across the main and full-replicate supplementary grids, each scenario is represented by 1000 replicates. Monte Carlo uncertainty in mean $\mathrm{CV}_{\mathrm{tot}}$ is small relative to the contrasts reported below. At $\sigma_{\mathrm{env}} = 0.5$, $\rho_{\mathrm{eff}} = 0.5$, and $S = 4$, for example, the mixed and aligned means are 0.084 and 0.263, with Monte Carlo standard errors of 0.00014 and 0.00059. Lower-replicate exploratory and control grids are used only as robustness diagnostics, not as the primary source for the main figures.

### Numerical and ecological checks

A suite of automated numerical and ecological checks is used to verify the simulations. For each richness $S$, the equicorrelation matrix with clamped $\rho_{\mathrm{env}}$ is confirmed to be positive definite and to admit a successful Cholesky decomposition. For long AR(1) runs, empirical stationary variances are compared with the analytic expression $\sigma_{\mathrm{env}}^2/(1 - \phi^2)$ and agree within tolerance. When $\sigma_{\mathrm{env}} = 0$, simulated abundances converge to the analytical symmetric equilibrium $N_i^\ast$. Under stochastic forcing, abundances are non-negative by construction and floor occupancy is monitored explicitly rather than assumed absent.

Synchrony metrics are checked using toy examples with perfectly synchronous and perfectly asynchronous trajectories: the Loreau–de Mazancourt index $\phi_{\mathrm{LdM}}$ and mean pairwise realised log-growth correlations approach their expected extreme values, and $\phi_{\mathrm{LdM}}$ always lies in $[0,1]$ after clipping. Bookkeeping checks ensure that replicate simulation wrappers return arrays and data frames of the expected shapes and summary statistics.
Numerical-guard diagnostics showed that high-side exponent clipping was effectively absent. Mean low-side clipping stayed below 0.01 in dedicated diagnostics at $\sigma_{\mathrm{env}}\leq1.5$ but reached 0.016–0.021 in 200-replicate checks of positive-slope $\sigma_{\mathrm{env}}=4$ stress cells. Floor occupancy was low in most scenarios but increased in the high-persistence and high-variance regions (Supporting information). These extremes are therefore treated as stress tests rather than clean mechanistic evidence.

Floor occupancy remains very low in the main inference grids. In the richness grid for Figure 2, the maximum scenario mean is $\approx 0.0014$ even at $\sigma_{\mathrm{env}}=2.0$, confirming that the reported richness pattern is not driven by repeated contact with the numerical floor. Occupancy rises in the explicitly labelled high-$\sigma_{\mathrm{env}}$ and high-$\phi$ stress extensions, so those regions are interpreted as numerical and ecological stress tests rather than baseline scenarios.

## Results

### Insurance patterns under mixed vs aligned responses

In the mixed-slope regime, community variability is strongly buffered relative to aligned responses. Across the ($\sigma_{\mathrm{env}}, \rho_{\mathrm{eff}}, S$) grid, $\mathrm{CV}_{\mathrm{tot}}$ increases with $\sigma_{\mathrm{env}}$ but generally decreases along the richness assembly sequence and—counterintuitively for many $\sigma_{\mathrm{env}}$ values—declines as $\rho_{\mathrm{eff}}$ increases. At $S=4$, aligned positive responses become much more variable as $\sigma_{\mathrm{env}}$ increases, while mixed responses remain lower across the same forcing gradient (Fig. 1). For example, at $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ is $\approx 0.15$ for $S=2$, $\approx 0.08$ for $S=4$, and $\approx 0.06$ for $S=8$. Averaged over $\rho_{\mathrm{eff}}$, mean $\mathrm{CV}_{\mathrm{tot}}$ declines steeply from $S=2$ to $S=4$ and continues to fall towards $S=8$ at every non-zero $\sigma_{\mathrm{env}}$; the deterministic $\sigma_{\mathrm{env}}=0$ baseline remains near zero for all richness values (Fig. 2).

In the positive-slope regime, community variability behaves very differently. Here $\mathrm{CV}_{\mathrm{tot}}$ increases with $\rho_{\mathrm{eff}}$ as well as $\sigma_{\mathrm{env}}$ (Fig. 1A), and realised log-growth synchrony is high and increases with $\rho_{\mathrm{eff}}$ (Fig. 3B). Richness still reduces variability through statistical averaging, but does not overturn the positive $\mathrm{CV}_{\mathrm{tot}}$–$\rho_{\mathrm{eff}}$ relationship: at $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ for $S=4$ is $\approx 0.26$, substantially higher than in the corresponding mixed-slope scenario. Under high environmental forcing ($\sigma_{\mathrm{env}}\ge 1.0$) and strong driver correlation, positive-slope communities show very large $\mathrm{CV}_{\mathrm{tot}}$ (often approaching or exceeding 1), whereas mixed-slope communities under the same forcing remain far less variable (Fig. 1B).

### Imposed versus realised synchrony

The mixed and aligned regimes map imposed driver correlation to realised synchrony in opposite ways. At $\sigma_{\mathrm{env}}=0.5$, the full-replicate mixed-slope simulations show strong decoupling: mean pairwise realised per-capita log-growth correlations fall well below $\rho_{\mathrm{eff}}$ as imposed correlation increases, becoming negative at high $\rho_{\mathrm{eff}}$ for low-richness communities (Fig. 3A). At $\rho_{\mathrm{eff}}\approx 1$, for example, mean realised log-growth correlations are $\approx -0.81$ for $S=2$, $\approx -0.16$ for $S=4$, and remain low positive ($\approx 0.08$) for $S=8$ (Fig. 3A). The difference $\Delta\mathrm{corr}=\mathrm{corr}_{\mathrm{realised}}-\rho_{\mathrm{eff}}$ consequently becomes strongly negative under high imposed correlation (Fig. 3C).

In the positive-slope regime, realised log-growth correlations increase with $\rho_{\mathrm{eff}}$ and remain strongly positive (Fig. 3B). At $\sigma_{\mathrm{env}}=0.5$, realised correlations track $\rho_{\mathrm{eff}}$ much more closely: $\Delta\mathrm{corr}$ is positive at low $\rho_{\mathrm{eff}}$, near zero at intermediate values, and only modestly negative at the high end (Fig. 3C). Thus $\rho_{\mathrm{env}}$ is a driver parameter, not a synchrony metric. Response-direction heterogeneity determines whether shared environmental variation yields weak (or compensatory) versus strong realised synchrony.

### Synchrony–variability relationships

Across the mixed-slope scenario means, $\mathrm{CV}_{\mathrm{tot}}$ increases with abundance-based synchrony $\phi_{\mathrm{LdM}}$ (Pearson $r\approx0.85$) and with mean pairwise realised log-growth correlation ($r\approx0.57$; Fig. 4A,B). These raw associations do not carry the same evidential weight. Because $\phi_{\mathrm{LdM}}$ and $\mathrm{CV}_{\mathrm{tot}}$ both contain $\operatorname{Var}(N_{\mathrm{tot}})$, their relationship is partly mathematical. In the grid-adjusted diagnostic, adding $\phi_{\mathrm{LdM}}$ to $\sigma_{\mathrm{env}}$, $S$, and $\rho_{\mathrm{eff}}$ increases $R^2$ from 0.857 to 0.904, whereas adding realised log-growth correlation alone changes $R^2$ by only 0.0001 and gives a standardised coefficient of 0.02. Figure 4 is therefore descriptive evidence of covariation across the designed scenarios, not a mediation test.

The less coupled evidence points in the same mechanistic direction. Approximate species-level variability does not decline enough to explain community buffering by itself. Mean total abundance increases with richness, so the decline in community CV partly reflects a larger denominator. Negative aggregate covariance offsets summed species variances in every examined decomposition, but neither total variance nor covariance magnitude changes monotonically at every richness step (Supporting information).

In positive-slope communities, $\phi_{\mathrm{LdM}}$ is generally high and mean realised log-growth correlations track imposed driver correlation (Fig. 3B). Community $\mathrm{CV}_{\mathrm{tot}}$ is correspondingly high and more tightly controlled by $\sigma_{\mathrm{env}}$, consistent with shared environmental shocks being transmitted to all species in the same direction.

### Effects of environmental persistence

Increasing $\phi$ at fixed innovation standard deviation creates a combined persistence–stationary-variance stress gradient that inflates community variability in mixed-slope communities (Fig. 5). At fixed $\sigma_{\mathrm{env}}$ and $\rho_{\mathrm{eff}}$, $\mathrm{CV}_{\mathrm{tot}}$ increases strongly with $\phi$: for $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ rises from $\approx 0.14$ at $\phi=0$ to $\approx 0.58$ at $\phi=0.95$ for $S=2$, and from $\approx 0.07$ to $\approx 0.35$ for $S=4$. This sensitivity reflects the AR(1) structure: increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ increases environmental persistence and also increases stationary variance, with stationary standard deviation
\[
\sigma_{\mathrm{eff}}=\frac{\sigma_{\mathrm{env}}}{\sqrt{1-\phi^2}}.
\]

Despite this inflation, the qualitative insurance pattern within the mixed-slope regime persists across the $\phi$ stress gradient: $\mathrm{CV}_{\mathrm{tot}}$ generally declines as $\rho_{\mathrm{eff}}$ increases, and richer communities remain less variable than species-poor communities under the same forcing (Fig. 5). The decline with $\rho_{\mathrm{eff}}$ weakens at the highest persistence ($\phi=0.95$) and can flatten or reverse locally, but the ordering by richness remains unchanged.

Floor occupancy remains essentially absent for $\phi \le 0.7$ and low for $\phi=0.9$ (maximum scenario mean $\bar{e}\approx 0.005$), but rises in the highest-persistence stress case ($\phi=0.95$; maximum scenario mean $\bar{e}\approx 0.049$). Thus the strongest $\phi=0.95$ inflation should be read as a high-persistence/high-stationary-variance stress regime, while the qualitative richness ordering remains intact across the full grid.

### Controls: competition strength and slope magnitudes

The full-replicate positive-matched control isolates response sign structure from slope magnitude by using aligned positive slopes with magnitudes matched to the mixed regime. It reduces absolute $\mathrm{CV}_{\mathrm{tot}}$ relative to the wider positive-slope regime, but its realised log-growth correlation remains positive and rises strongly with $\rho_{\mathrm{eff}}$. Slope magnitude therefore affects fluctuation amplitude, whereas response sign structure controls whether stronger driver correlation produces reinforcing or compensatory growth.

Lower-replicate no-competition and mixed-narrow control grids indicate that the insurance patterns do not depend on a particular competition strength or on unusually steep mixed slopes. Setting $\alpha_{\mathrm{inter}}=0$ shifts absolute variability but leaves the qualitative contrasts intact: mixed-slope communities still show declining $\mathrm{CV}_{\mathrm{tot}}$ with richness and a generally negative association between $\mathrm{CV}_{\mathrm{tot}}$ and $\rho_{\mathrm{eff}}$, whereas positive-slope communities retain an increasing relationship between $\mathrm{CV}_{\mathrm{tot}}$ and $\rho_{\mathrm{eff}}$.

Narrowing mixed slopes to $b_i \in [-0.25, 0.25]$ reduces overall variability and preserves the richness effect and the mixed–positive CV contrast. Across the central and non-negative correlation range, narrower mixed slopes also show lower realised synchrony than aligned positive slopes. At requested $\rho_{\mathrm{env}}=-0.5$, however, the synchrony ordering reverses in some $S=4$ and $S=8$ scenarios even though community CV remains lower. Together, the controls support response-direction heterogeneity, rather than tuned competition strength or unusually steep mixed slopes, as the main source of compensatory insurance while showing that boundary conditions affect synchrony ordering.

## Discussion

### Response-direction heterogeneity decouples driver correlation from realised synchrony

These simulations isolate a simple mechanism by which response diversity can, but need not, generate insurance: heterogeneity in response direction can decouple imposed correlation among environmental drivers ($\rho_{\mathrm{env}}$, implemented as $\rho_{\mathrm{eff}}$ after feasibility clipping) from realised synchrony. With response slopes balanced across positive and negative values, correlated anomalies paired with opposite response signs generate weak or negative covariances in the direct environmental forcing term and in realised per-capita log-growth rates. Mean pairwise realised log-growth correlations therefore fall well below $\rho_{\mathrm{eff}}$, abundance synchrony $\phi_{\mathrm{LdM}}$ remains low, and $\mathrm{CV}_{\mathrm{tot}}$ is reduced relative to aligned-slope baselines under the same $\sigma_{\mathrm{env}}$, $\rho_{\mathrm{eff}}$, and $\phi$.

When response slopes are aligned and positive, imposed driver correlation and realised synchrony reinforce each other. Correlated anomalies tend to push species’ growth rates in the same direction, so increasing $\rho_{\mathrm{eff}}$ yields high realised covariances and elevated $\phi_{\mathrm{LdM}}$. Richness reduces community variability through averaging, but does not eliminate the high variability generated by strongly correlated forcing, consistent with stabilisation dominated by statistical averaging rather than compensatory dynamics in some empirical systems [@zhao2022BiodiversityStabilizesPlant].

Imposed driver correlation and realised synchrony are therefore not interchangeable. In models that use driver correlation as a proxy for synchrony, the mechanism can be misidentified. Under heterogeneous response directions, even strong driver correlation can yield near-zero or negative realised log-growth correlations; under aligned responses the same forcing produces tight positive synchrony. This result complements the synchrony framework of Loreau and de Mazancourt [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability] by identifying signed response slopes as one control on the translation from environmental covariance to dynamical synchrony.

No single synchrony panel establishes that mechanism. $\phi_{\mathrm{LdM}}$ is a variance-decomposition metric and shares total-abundance variance with community CV, while realised log-growth correlation is affected by density feedbacks and adds little explanatory power once the experimental grid is included. The inference instead rests on agreement among the analytical response-term covariance, the opposite realised-correlation patterns in Fig. 3, and the sign-structure and variance-decomposition controls in the Supporting information.

### Richness as an amplifier of insurance when responses differ

Species richness amplifies insurance when additional species fill gaps in the response distribution. In the implemented mixed-slope gradient, increasing $S$ does not widen the range $[-0.5,0.5]$; it adds intermediate response types. Odd-richness communities include a zero-slope species, and mean squared slope falls from 0.25 at $S=2$ to approximately 0.11 at $S=8$. This is therefore a deterministic community-assembly sequence, not a pure richness manipulation at fixed response composition. It tests whether denser sampling of a fixed response range strengthens insurance. Under that design, additional compensatory pairings, statistical averaging, and the declining contribution of any one species all reduce $\mathrm{CV}_{\mathrm{tot}}$. The deterministic increase in total abundance when $\alpha_{\mathrm{inter}}<\alpha_{\mathrm{intra}}$ also lowers CV. Aggregate covariance is negative throughout the examined decompositions, although total variance and covariance magnitude are not monotonic with every increment in richness (Supporting information). When slopes are aligned, richness still reduces variability through averaging, but it does not reverse the positive $\mathrm{CV}_{\mathrm{tot}}$–$\rho_{\mathrm{eff}}$ relationship created by shared environmental forcing.

This pattern is consistent with work in which synchrony and covariance structure explain more variation in community stability than richness per se [@valencia2020SynchronyMattersMore; @demazancourt2013PredictingEcosystemStability]. The compensatory component of insurance strengthens when added species extend response-direction diversity rather than repeat the same sign, as recent food-web theory also predicts [@danet2025ResponseDiversityMajor]. This ties the response-diversity concept [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines] to explicit slopes in a population model. It also exposes the alternative: with aligned responses, stronger driver correlation raises realised synchrony and $\mathrm{CV}_{\mathrm{tot}}$, even though averaging still gives richer communities some buffer.

### A mechanistic bridge to empirical response diversity

The value of this deliberately spare model is its explicit mapping from environmental covariance and signed response slopes to realised synchrony. Recent work in Lake Geneva found that time-varying response diversity within phytoplankton and zooplankton communities stabilised their respective biomasses, with context-dependent effects and biotic interactions playing a prominent role [@hsieh2026QuantifyingEffectsResponse]. That result and the present model make the same general point: response diversity cannot be represented by richness alone; its effect depends on how responses are distributed and how species interactions reshape them. The aligned-slope treatment makes the alternative explicit. When response directions align, the shared component of environmental variation becomes a common shock and diversity contributes mainly through statistical averaging, resembling empirical cases dominated by averaging [@zhao2022BiodiversityStabilizesPlant].

Real communities experience several environmental axes simultaneously and may align along some axes but diverge along others. Metrics that aggregate across axes can therefore conflate stabilising and destabilising components [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. Empirical response-surface frameworks address that high-dimensional problem; the present one-dimensional model instead provides a transparent limiting case in which response direction and environmental covariance can be traced directly to realised synchrony and stability [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity; @sasaki2026BiologicalTraitsPredict].

### Insurance, environmental persistence, and effective variance

Environmental anomalies are modelled as an AR(1) process, with $\sigma_{\mathrm{env}}$ as the innovation standard deviation and $\phi$ controlling temporal autocorrelation and the stationary variance of the environmental state. Varying $\phi$ at fixed $\sigma_{\mathrm{env}}$ therefore changes persistence and increases the effective magnitude of fluctuations, with stationary standard deviation
\[
\sigma_{\mathrm{eff}}=\frac{\sigma_{\mathrm{env}}}{\sqrt{1-\phi^2}}.
\]
As expected, increasing $\phi$ at fixed innovation variance inflates $\mathrm{CV}_{\mathrm{tot}}$. Within the mixed-slope regime, it does not erase the richness ordering or the tendency for $\mathrm{CV}_{\mathrm{tot}}$ to decline with $\rho_{\mathrm{eff}}$. Because the persistence grid contains no aligned-slope treatment, it does not test whether the mixed–aligned contrast itself is invariant to $\phi$.

The analysis does not isolate a pure persistence effect by rescaling innovations to constant stationary variance. It asks the narrower question supported by Fig. 5: whether the mixed-slope richness and correlation orderings survive a gradient in which persistence and stationary variance rise together. They do, except that the decline with $\rho_{\mathrm{eff}}$ flattens or reverses locally at the most persistent, floor-affected edge.

### Robustness and scope of the model

The main patterns persist across the expanded environmental-forcing grid and the simplified control models. At $\phi=0.4$, the mixed–aligned contrast spans core innovation standard deviations up to $\sigma_{\mathrm{env}}=2.0$, a high-variance extension to $\sigma_{\mathrm{env}}=4.0$, and effective driver correlations from moderately negative to near one. Within mixed-slope communities, the richness and correlation orderings persist along the $\phi$ stress gradient to 0.95. Removing interspecific competition ($\alpha_{\mathrm{inter}}=0$) leaves the mixed-versus-aligned contrast and richness pattern intact, so interspecific competition is not required for response-direction heterogeneity to reduce realised synchrony. Narrowing the mixed-slope range lowers overall variability but preserves the core ordering under matched forcing.

The numerical checks serve a different purpose. Environmental covariance matrices are positive definite, empirical AR(1) stationary variances match $\sigma_{\mathrm{env}}^2/(1-\phi^2)$ within tolerance, floor occupancy is negligible in the main low-stress inference grids and flagged in stress extensions, and synchrony metrics behave as expected in toy cases. Together with the controls, these checks show that covariance-matrix failure, floor occupancy in the main inference grids, and a single competition setting do not account for the mixed–aligned contrast.

This robustness is internal to a stylised framework. Species receive an equicorrelated vector of exposures to one environmental variable; competition is symmetric; demographic stochasticity, spatial structure, and observation error are absent; and response heterogeneity is confined to one slope per species. The mixed-slope vectors are also perfectly balanced around zero, so the simulations test a strong form of opposing response diversity; unbalanced mixtures may cancel shared forcing less completely. These choices isolate the interaction among environmental covariance, response direction, and community assembly. They also limit transfer to real ecosystems, where multiple drivers, asymmetric interactions, and spatial heterogeneity can alter synchrony and stability [@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial].

### Limitations and future directions

Equicorrelation is the clearest simplification. Environmental covariance can be spatially heterogeneous and scale-dependent [@loreau2003BiodiversitySpatialInsurance; @shanafelt2015BiodiversityProductivitySpatial]. Block-correlated, spatially explicit, or empirically estimated covariance matrices would change which pairs of species receive similar anomalies and therefore which signed responses compensate. Testing those structures would connect this mechanism more directly to spatial insurance and synchrony under global change.

The linear, one-variable response model is another strong restriction. Real communities face multidimensional environmental change, and response diversity then depends on variation in slopes for each driver and on correlations among response surfaces [@mori2013ResponseDiversityDetermines; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. The present model is a limiting case in which one driver dominates. A higher-dimensional version could allow species to align along some environmental axes and diverge along others, providing a direct bridge to empirical response-surface estimates [@polazzo2024MeasuringResponseDiversity; @sasaki2026BiologicalTraitsPredict].

The model also omits demographic stochasticity and trophic structure, both of which can reshape synchrony and stability [@ives2007StabilityDiversityEcosystems; @loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept]. Demographic noise can weaken environment–growth coupling for rare species, while trophic interactions can transmit or dampen environmental signals across levels. These processes could change the size or even the sign of the effects reported here. The present result should therefore be read as a conditional mechanism, not a universal prediction.

Finally, stability is measured here as temporal variability in total abundance. Other stability dimensions—resistance, resilience, recovery time, and responses to pulse or press perturbations—may behave differently under response diversity [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept; @kunze2026SpeciesInteractionsDetermine]. Extending the analysis to alternative stability notions, or to multifunctional stability, would better match the multidimensional stability concepts used in empirical work [@sasaki2019SpeciesAsynchronyResponse; @wagg2021DiversityAsynchronySoil].

### Conclusion

Biodiversity can buffer aggregate community properties against environmental variability, but the mechanistic question is more informative: when does insurance arise, through which pathway, and how does it depend on environmental covariance and response diversity [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2026ExpertledPrioritiesResponse]? In this model, strong compensatory insurance depends on response direction. When response slopes are balanced across opposing directions, biodiversity decouples driver correlation from realised synchrony and stabilises aggregate abundance relative to aligned-response baselines. When responses are aligned, the same covariance acts as a common shock; richness still provides some statistical averaging, but synchrony and community variability remain high.

Richness alone is therefore an incomplete predictor. Stabilisation depends on which response types are added and how their directions align with the covariance structure of the dominant environmental drivers. Differences in that alignment may help explain divergent empirical relationships among richness, synchrony, and stability.

## Artificial intelligence statement

OpenAI Codex large language models assisted with model and code development, simulation and analysis workflows, literature searches, and drafting and editorial revision. The author reviewed all AI-assisted material incorporated into the work and takes full responsibility for the final content.

## References
