# Biodiversity buffers environmental variability only when species responses diverge

## Abstract

Environmental variability is usually destabilising, yet the insurance hypothesis predicts that biodiversity can buffer ecosystem functioning when species respond asynchronously to fluctuating environments. Despite its influence, we lack simple dynamical demonstrations of when response diversity produces insurance and when it does not, particularly under correlated environmental drivers. Here I use a stochastic multispecies Ricker model to explore how species’ environmental response directions interact with shared environmental variation to shape community-level variability. Species compete symmetrically and differ only in the sign and magnitude of their response slopes to a single environmental axis. Environmental anomalies follow a multivariate autoregressive process with controllable variance, cross-species correlation in drivers, and temporal autocorrelation. I compare communities with mixed positive and negative response slopes to communities where all slopes are positive. For each scenario I quantify the coefficient of variation of total biomass and synchrony metrics based on abundance and per capita growth rates. When response slopes are mixed, realised synchrony in growth rates is much lower than the imposed correlation among environmental drivers and can become negative at low richness. In this regime, community-level variability declines with species richness and can even decrease as environmental correlation increases. When all slopes are positive, imposed environmental correlation yields strong realised synchrony; community-level variability increases with environmental correlation and remains high even at greater richness. These contrasts persist across environmental variances, competition strengths, and slope magnitudes, and mixed-slope insurance remains evident across a wide range of temporal autocorrelation. The results show that biodiversity buffers environmental variability only when it includes diversity in response directions that decouple driver covariance from realised synchrony. Richness alone is not enough: the stabilising effect of biodiversity depends critically on how species’ responses are arranged relative to the structure of environmental variation.

## Keywords

biodiversity; response diversity; ecosystem stability; species synchrony; environmental covariance; stochastic community dynamics; insurance hypothesis.

## Significance Statement

This manuscript addresses a central question in ecology: under what conditions does biodiversity stabilise ecosystem functioning in fluctuating environments? Oikos is an ideal outlet because it publishes theoretical and empirical work aimed at general ecological mechanisms, including biodiversity–stability, synchrony, and response diversity. This new study sits squarely in this space: it uses a deliberately simple stochastic community model to clarify how the structure of species’ environmental responses interacts with shared environmental variation to produce, or fail to produce, biodiversity “insurance”.
The simulation experiments build explicitly on classical insurance and portfolio theory, synchrony frameworks, and response diversity concepts developed in previous work, but moves beyond them in three ways. First, it cleanly separates imposed environmental correlation among species’ drivers from realised synchrony in population growth, and shows that the two can diverge sharply. Second, it makes response direction heterogeneity the central trait axis and demonstrates that biodiversity buffers environmental variability only when responses diverge in sign; aligned responses can instead amplify environmental shocks. Third, it systematically tests robustness across environmental variance, persistence, competition strength, and slope magnitude, providing a transparent dynamical testbed that complements recent empirical and statistical approaches to measuring response diversity. Because the results are expressed in terms of easily interpretable metrics (community variability, species level variability, and synchrony indices) and use a standard population dynamics framework, they are accessible to the broad ecology readership of Oikos and directly relevant to ongoing debates about biodiversity–stability relationships and the role of response diversity.

## Introduction

Environmental variability generally destabilises populations: as climatic and other drivers fluctuate, population abundances tend to vary more through time, increasing the risk of low-biomass episodes and local collapse [@ives2007StabilityDiversityEcosystems]. Against this backdrop, the insurance hypothesis proposes that biodiversity can buffer ecosystem functioning against environmental fluctuations, because different species respond differently in space and time, so that declines in some are offset by increases in others [@yachi1999BiodiversityEcosystemProductivity]. This idea, inspired by portfolio theory in economics, predicts that aggregate ecosystem properties such as total biomass or productivity should fluctuate less in more diverse communities than in species-poor systems subject to the same environmental variance [@loreau2021BiodiversityInsuranceConcept]. Over the last two decades, both experiments and syntheses have produced substantial evidence that biodiversity can stabilise ecosystem functioning ([@loreau2013BiodiversityEcosystemStability; @demazancourt2013PredictingEcosystemStability], Wagg et al. 2022), but they also reveal that the strength, and even the sign, of diversity–stability relationships depends strongly on the underlying mechanisms [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept].

A central theme in this work is synchrony among species’ fluctuations. When species respond similarly to environmental variation, community-level variability tends to scale with typical species-level variability; when responses are asynchronous or negatively correlated, aggregate variability can be much lower than the sum of its parts [@doak1998StatisticalInevitabilityStabilitydiversity; @loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability]. Formal measures such as the variance ratio, Loreau–de Mazancourt’s synchrony index $\phi_{\mathrm{LdM}}$, and related covariance-based metrics provide quantitative links between species-level variances, covariances, and community-level stability [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability; @thibaut2013UnderstandingDiversityStability; @demazancourt2013PredictingEcosystemStability]. At the same time, recent reviews have emphasised that “insurance” is conceptually slippery: it bundles together effects of biodiversity on both the mean and the variability of ecosystem properties, and different studies implicitly use different baselines when they claim that biodiversity “stabilises” functioning [@ives2007StabilityDiversityEcosystems; @loreau2021BiodiversityInsuranceConcept]. In particular, many formulations are vague about whether stabilisation is meant in an absolute sense (reduced community variance as environmental variance increases) or in a relative sense (community variance lower than an appropriate baseline under the same environmental forcing).

The notion of response diversity was introduced to capture the idea that what matters for insurance is not just the number of species but the diversity of their responses to environmental change [@elmqvist2003ResponseDiversityEcosystem]. In this view, species within a functional group may be redundant for mean functioning but differ in how they respond to fluctuations; such variation in response “slopes” and tolerances can, in principle, generate compensatory dynamics and enhance resilience [@mori2013ResponseDiversityDetermines]. Despite the conceptual appeal of response diversity, recent assessments suggest that both theoretical and empirical support for its stabilising role remain surprisingly thin [@ross2024LimitedTheoreticalEmpirical]. Empirical studies that explicitly quantify response diversity are still relatively rare and vary widely in how they define and measure it [@mori2013ResponseDiversityDetermines; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. On the theoretical side, most models either encode response differences implicitly via niche axes and competition coefficients, or assume a covariance structure for demographic rates without deriving it mechanistically from species’ environmental responses [@loreau2008SpeciesSynchronyIts; @thibaut2013UnderstandingDiversityStability; @shanafelt2015BiodiversityProductivitySpatial].

At the same time, a growing body of empirical work points to synchrony and covariance structure, rather than richness per se, as the primary determinants of temporal stability. Across a global compilation of plant communities, species synchrony explained more variation in community-level stability than species richness; richness had weak or inconsistent direct effects once synchrony was accounted for [@valencia2020SynchronyMattersMore]. Long-term grassland experiments and microbial mesocosms similarly show that diversity can stabilise functioning, but often via a mix of statistical averaging and modest compensatory dynamics, with the relative importance of asynchrony increasing over time ([@wagg2021DiversityAsynchronySoil; @zhao2022BiodiversityStabilizesPlant], Wagg et al. 2022). These studies typically treat synchrony as an empirical summary of observed covariances, not as a quantity that can be mechanistically predicted from traits and the structure of environmental drivers. As a result, we know that synchrony matters, but we often lack a clear mapping from environmental covariance and response diversity to realised synchrony, and then to community variability.

Recent developments have started to fill parts of this gap. Loreau and de Mazancourt [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability] derived how species synchrony should depend on shared environmental drivers, competition, and demographic noise in general stochastic models, while Thibaut and Connolly [@thibaut2013UnderstandingDiversityStability] unified portfolio and variance-ratio perspectives in a common framework. Loreau [@loreau2021BiodiversityInsuranceConcept] synthesised biological insurance theory, clarifying the parallel with economic portfolios and emphasising the need to separate effects on means and variances. On the empirical side, Polazzo et al. [@polazzo2024MeasuringResponseDiversity] and others have developed metrics to quantify response diversity and “response capacity” in communities exposed to multifarious environmental change. Yet even Ross and Sasaki [@ross2024LimitedTheoreticalEmpirical] conclude that we still lack simple dynamical testbeds that show under what conditions response diversity actually generates insurance, and when it fails, particularly under correlated environmental drivers and temporal autocorrelation.

This study takes a deliberately stylised approach to the problem. Stochastic multispecies communities are built under a symmetric Ricker model,chosen because it has a simple analytic equilibrium and is widely used for discrete-time population dynamic. This was subject to a single latent environmental axis that follows an AR(1) process with controllable innovation variance and temporal autocorrelation. Species differ only in the sign and magnitude of their environmental response slopes along this axis: in one regime, slopes are mixed (positive and negative), representing strong response diversity in direction; in the other, slopes are all positive, representing aligned responses along the same environmental gradient. Environmental drivers experienced by different species all have the same pairwise correlation $\rho_{\mathrm{env}}$, allowing the strength of imposed environmental correlation to be manipulated independently of species’ response directions. Within this framework, environmental variance, imposed driver correlation, species richness, and environmental autocorrelation are varied, and control simulations remove interspecific competition or narrow the range of slope magnitudes.

Insurance and stabilisation are defined explicitly in relative terms. The analysis quantifies (i) the coefficient of variation (CV) of total community biomass, (ii) an approximate mean species-level CV, and (iii) synchrony metrics (Loreau–de Mazancourt $\phi_{\mathrm{LdM}}$ and mean pairwise growth-rate correlations). Biodiversity is said to provide insurance when, for a given level of environmental variance and $\rho_{\mathrm{env}}$, communities with heterogeneous response directions and higher richness exhibit lower community CV and lower realised synchrony than baselines such as single-species or aligned-slope communities. By comparing imposed driver correlation to realised synchrony, the analysis asks how heterogeneity in response directions decouples environmental covariance from species covariances, and how that decoupling depends on richness, competition, and environmental persistence.

The aims are threefold. First, to clarify when and how response diversity turns shared environmental variation into compensatory dynamics that buffer aggregate biomass, versus when shared environment and aligned responses amplify fluctuations despite high richness. Second, to separate imposed environmental correlation from realised synchrony, and to quantify how species’ response directions modulate this relationship. Third, to assess the robustness of these insurance effects across key features of global change—environmental variance, temporal autocorrelation, and competition—using a model simple enough to maintain mechanistic transparency but rich enough to connect to contemporary biodiversity–stability and response-diversity debates [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept; @ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity]. In what follows, “insurance” is understood in this relative sense: reduced community variability and synchrony compared with appropriate baselines under the same environmental forcing. Species experience anomalies along the same environmental dimension, but not identical realisations (microhabitat/measurement/phenology differences), modelled as equicorrelated (z_i(t)).

## Methods 

### Community dynamics

We model a community of $S$ species using a discrete-time stochastic Ricker model with symmetric competition. Let $N_i(t)$ denote the abundance of species $i$ at time $t$. In the absence of environmental variation, per-capita growth follows
\[
N_i(t+1) = N_i(t)\exp\left[r_0 - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right],
\]
where $r_0$ is a shared intrinsic growth rate, $K_i$ is the carrying capacity of species $i$, $\alpha_{\mathrm{intra}}$ is intraspecific competition, and $\alpha_{\mathrm{inter}}$ is interspecific competition. We set $K_i = 100$ for all species, $\alpha_{\mathrm{intra}} = 1$, and $\alpha_{\mathrm{inter}} = 0.3$ unless otherwise stated. With these choices, the symmetric deterministic equilibrium is
\[
N_i^\ast = \frac{K_i}{\alpha_{\mathrm{intra}} + \alpha_{\mathrm{inter}}(S-1)}.
\]

Environmental variation enters as a linear response term $b_i z_i(t)$ in the per-capita growth rate:
\[
N_i(t+1) = N_i(t)\exp\left[r_0 + b_i z_i(t) - \frac{\alpha_{\mathrm{intra}} N_i(t) + \alpha_{\mathrm{inter}}\sum_{j \neq i} N_j(t)}{K_i}\right].
\]
Species differ only in their response slopes $b_i$, which encode both the direction and magnitude of their response to the environmental anomaly $z_i(t)$. Four slope regimes are considered:

* Mixed slopes: $b_i$ evenly spaced in $[-0.5, 0.5]$, giving both positive and negative responses.
* Positive slopes: $b_i$ evenly spaced in $[0.1, 1.0]$, giving aligned positive responses.
* Positive-matched (sign-structure control): aligned positive slopes with magnitudes matched to mixed slopes, $b_i = |b_i^{\mathrm{mixed}}|$.
* Mixed–narrow (sensitivity analysis): $b_i$ evenly spaced in $[-0.25, 0.25]$.

Abundances are floored at a small positive constant $N_{\min} = 10^{-9}$ to avoid numerical issues from extinction-driven zeros, and the exponent in the growth term is capped at $\pm 50$ to prevent overflow in $\exp(\cdot)$. Initial abundances are set to $K_i/2$ for all species.

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

For a given scenario, all species share the same $\phi$ and requested $\rho_{\mathrm{env}}$ but receive correlated environmental trajectories via the multivariate process (after clipping to $\rho_{\mathrm{eff}}$ where required). One environmental time series is generated per replicate and scenario.

### Simulation design

The main mixed-slope and positive-slope grids address the first two goals (when response diversity yields insurance and how imposed environmental correlation translates into realised synchrony). The $\phi$-sensitivity, no-competition, and slope-magnitude grids assess robustness to temporal autocorrelation, competition strength, and response magnitude.

A scenario is defined by a combination of slope regime, species richness $S$, innovation standard deviation $\sigma_{\mathrm{env}}$, imposed environmental correlation $\rho_{\mathrm{env}}$, temporal autocorrelation $\phi$, and competition strength $\alpha_{\mathrm{inter}}$. For each scenario, the model is run for $n_{\mathrm{steps}}$ time steps, discarding the first $n_{\mathrm{burn}}$ steps as burn-in.

The primary mixed-slope grid crosses $\sigma_{\mathrm{env}} \in \{0, 0.2, 0.5, 1.0, 1.5\}$ with $\rho_{\mathrm{env}} \in \{-0.5, 0, 0.5, 0.9, 1.0\}$ and $S \in \{2, 4, 8\}$, with $\phi = 0.4$, $n_{\mathrm{steps}} = 600$, and $n_{\mathrm{burn}} = 300$. For each combination of $(\sigma_{\mathrm{env}}, \rho_{\mathrm{env}}, S)$, 150 replicate time series are simulated.

The positive-slope grid (aligned responses) uses the same $(\sigma_{\mathrm{env}}, \rho_{\mathrm{env}})$ combinations, with $S \in \{4, 8\}$ (plus a small pilot subset for $S = 2$), $\phi = 0.4$, $n_{\mathrm{steps}} = 600$, and $n_{\mathrm{burn}} = 300$. For this grid, 100 replicates are simulated per scenario.

To isolate response sign structure from slope-magnitude differences, an additional positive-matched control grid is run with aligned positive slopes whose magnitudes match the mixed regime ($b_i = |b_i^{\mathrm{mixed}}|$). This grid uses the same $(\sigma_{\mathrm{env}}, \rho_{\mathrm{env}})$ combinations as the positive-slope grid, with $S \in \{4, 8\}$, $\phi = 0.4$, $n_{\mathrm{steps}} = 600$, $n_{\mathrm{burn}} = 300$, and 100 replicates per scenario.

To examine sensitivity to temporal autocorrelation, a production $\phi$-sensitivity grid is run for mixed slopes at $\sigma_{\mathrm{env}} = 0.5$, with $\rho_{\mathrm{env}} \in \{-0.5, -0.25, 0, 0.25, 0.5, 0.75, 0.9, 1.0\}$, $S \in \{2, 4\}$, and $\phi \in \{0, 0.7, 0.9, 0.95\}$. These runs use $n_{\mathrm{steps}} = 600$, $n_{\mathrm{burn}} = 300$, and 1000 replicates per scenario; the $\phi=0.4$ baseline is represented by the main mixed-slope grid.

No-competition controls set $\alpha_{\mathrm{inter}} = 0$ (with $\alpha_{\mathrm{intra}} = 1$) for both mixed and positive slopes. These controls use reduced grids with $\sigma_{\mathrm{env}} \in \{0, 0.5, 1.0\}$, $\rho_{\mathrm{env}} \in \{-0.5, 0, 0.5, 0.9, 1.0\}$, $S \in \{2, 4, 8\}$, and $\phi = 0.4$, with 80 replicates per scenario.

Finally, a slope-magnitude sensitivity analysis uses the mixed–narrow regime (slopes $b_i$ evenly spaced in $[-0.25, 0.25]$). This grid matches the reduced $(\sigma_{\mathrm{env}}, \rho_{\mathrm{env}}, S)$ combinations of the $\phi$-sensitivity grid at $\phi = 0.4$, again with 80 replicates per scenario.

For each run, a fixed base seed is used to generate independent random seeds for replicates, so that replicates within a scenario experience independent environmental realisations. Because the same base-seed scheme is used across scenario families, replicate indices are paired across comparable scenarios (e.g. mixed versus positive), reducing Monte Carlo comparison noise without changing within-scenario independence. Scenario-level summaries are stored in parquet format and subsequently aggregated into CSV files and figures by the analysis scripts.

### Metrics and insurance measures

All metrics are computed from post–burn-in time points. Let $T'$ be the number of retained time steps and define total community biomass
\[
N_{\mathrm{tot}}(t) = \sum_{i=1}^S N_i(t).
\]

**Community variability.** Community variability is measured by the coefficient of variation of total biomass,
\[
\mathrm{CV}_{\mathrm{tot}} = \frac{\sqrt{\operatorname{Var}(N_{\mathrm{tot}})}}{\mathbb{E}[N_{\mathrm{tot}}]},
\]
where empirical sample means and sample variances (with $\mathrm{ddof}=1$) are computed over the $T'$ retained time points.

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
A supplementary diagnostic of this metric versus imposed correlation is shown in Fig. S4.

**Synchrony indices.** Abundance-based community synchrony is quantified using the Loreau–de Mazancourt index,
\[
\phi_{\mathrm{LdM}} = \frac{\operatorname{Var}(N_{\mathrm{tot}})}{\left(\sum_{i=1}^S \sigma_i\right)^2},
\]
where $\sigma_i = \sqrt{v_i}$ is the standard deviation of species $i$. To avoid numerical overshoots, $\phi_{\mathrm{LdM}}$ is clipped to the interval $[0, 1]$.

To capture realised synchrony in growth responses, per-capita growth rates are computed as
\[
g_i(t) = \log\left(N_i(t+1) + N_{\min}\right) - \log\left(N_i(t) + N_{\min}\right),
\]
the correlation matrix of ${g_i(t)}$ across time is formed, and the mean of its off-diagonal elements is taken. This yields the **mean pairwise growth-rate correlation**, which can be negative when species exhibit compensatory dynamics.
When $\sigma_{\mathrm{env}} = 0$, growth-rate variance is zero and this correlation is undefined; such scenarios are excluded from correlation-based synchrony panels.

**Extinction frequency.** The extinction frequency for species $i$ is defined as
\[
e_i = \frac{1}{T'}\sum_{t=1}^{T'} \mathbf{1}\left[N_i(t) \leq N_{\min}\right],
\]
and the mean extinction frequency per scenario is
\[
\bar{e} = \frac{1}{S}\sum_{i=1}^S e_i.
\]

Scenario-level summaries are obtained by averaging replicate-level statistics for each unique combination of slope regime, $S$, $\sigma_{\mathrm{env}}$, $\rho_{\mathrm{env}}$, $\phi$, and $\alpha_{\mathrm{inter}}$.

“Insurance” is interpreted as relative stabilisation: for given $\sigma_{\mathrm{env}}$, $\rho_{\mathrm{env}}$, $S$, and $\phi$, biodiversity is said to provide insurance when communities with mixed response directions and higher richness show lower $\mathrm{CV}_{\mathrm{tot}}$ and lower realised synchrony (lower $\phi_{\mathrm{LdM}}$ and/or lower mean pairwise growth-rate correlation) than single-species or aligned-slope baselines.

### Monte Carlo uncertainty

Across the production grids used for the main figures, each scenario is represented by 1000 replicates. Monte Carlo uncertainty in $\mathrm{CV}_{\mathrm{tot}}$ is therefore small relative to the differences highlighted in the Results; for example, the mixed-versus-aligned difference in mean $\mathrm{CV}_{\mathrm{tot}}$ at $\sigma_{\mathrm{env}} = 0.5$, $\rho_{\mathrm{eff}} = 0.5$, and $S = 4$ is $\approx 0.18$, far larger than residual sampling variation in the scenario means. Lower-replicate exploratory and control grids are used only as robustness diagnostics, not as the primary source for the main production figures.

### Numerical and ecological checks

A suite of automated numerical and ecological checks is used to verify the simulations. For each richness $S$, the equicorrelation matrix with clamped $\rho_{\mathrm{env}}$ is confirmed to be positive definite and to admit a successful Cholesky decomposition. For long AR(1) runs, empirical stationary variances are compared with the analytic expression $\sigma_{\mathrm{env}}^2/(1 - \phi^2)$ and agree within tolerance. When $\sigma_{\mathrm{env}} = 0$, simulated abundances converge to the analytical symmetric equilibrium $N_i^\ast$. Under stochastic forcing, abundances remain above the numerical floor, ensuring non-negativity throughout.

Synchrony metrics are checked using toy examples with perfectly synchronous and perfectly asynchronous trajectories: the Loreau–de Mazancourt index $\phi_{\mathrm{LdM}}$ and mean pairwise growth-rate correlations approach their expected extreme values, and $\phi_{\mathrm{LdM}}$ always lies in $[0,1]$ after clipping. Bookkeeping checks ensure that replicate simulation wrappers return arrays and data frames of the expected shapes and summary statistics.
Numerical-guard diagnostics showed exponent clipping was rare (high-side clipping rates effectively zero and low-side clipping rates generally below $0.01$), while floor occupancy remained low in most scenarios but increased in high-persistence/high-variance stress-test corners (summary in `analysis/reports/numerical_guard_rates_summary.md`).

Extinction frequencies are monitored in scenario summaries and remain very low in the main inference grids. In the production richness grid for Figure 2, the maximum scenario-mean floor/extinction frequency is $\approx 0.0014$ even at $\sigma_{\mathrm{env}}=2.0$, confirming that the reported richness pattern is not driven by widespread numerical extinction.

## Results

### Insurance patterns under mixed vs aligned responses

In the mixed-slope regime, community variability is strongly buffered relative to aligned responses. Across the ($\sigma_{\mathrm{env}}, \rho_{\mathrm{eff}}, S$) grid, $\mathrm{CV}_{\mathrm{tot}}$ increases with $\sigma_{\mathrm{env}}$ but decreases with richness and—counterintuitively for many $\sigma_{\mathrm{env}}$ values—declines as $\rho_{\mathrm{eff}}$ increases. At S=4, production-scale simulations show that aligned positive responses become much more variable as $\sigma_{\mathrm{env}}$ increases, while mixed responses remain lower across the same forcing gradient (Fig. 1). For example, at $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ is $\approx 0.15$ for $S=2$, $\approx 0.08$ for $S=4$, and $\approx 0.06$ for $S=8$, illustrating a pronounced richness effect. Averaged over $\rho_{\mathrm{eff}}$, mean $\mathrm{CV}_{\mathrm{tot}}$ declines steeply from $S=2$ to $S=4$ and continues to fall towards $S=8$ across all $\sigma_{\mathrm{env}}$ values (Fig. 2).

In the positive-slope regime, community variability behaves very differently. Here $\mathrm{CV}_{\mathrm{tot}}$ increases with $\rho_{\mathrm{eff}}$ as well as $\sigma_{\mathrm{env}}$ (Fig. 1A), and realised growth synchrony is high and increases with $\rho_{\mathrm{eff}}$ (Fig. 3B). Richness still reduces variability through statistical averaging, but does not overturn the positive $\mathrm{CV}_{\mathrm{tot}}$–$\rho_{\mathrm{eff}}$ relationship: at $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{eff}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ for $S=4$ is $\approx 0.26$, substantially higher than in the corresponding mixed-slope scenario. Under high environmental forcing ($\sigma_{\mathrm{env}}\ge 1.0$) and strong driver correlation, positive-slope communities show very large $\mathrm{CV}_{\mathrm{tot}}$ (often approaching or exceeding 1), whereas mixed-slope communities under the same forcing remain far less variable (Fig. 1B).

### Imposed versus realised synchrony

The mixed and aligned regimes differ not only in $\mathrm{CV}_{\mathrm{tot}}$ but also in how imposed driver correlation translates into realised synchrony. At $\sigma_{\mathrm{env}}=0.5$, production-scale mixed-slope simulations show strong decoupling: mean pairwise correlations of per-capita growth rates fall well below $\rho_{\mathrm{eff}}$ as imposed correlation increases, becoming negative at high $\rho_{\mathrm{eff}}$ for low-richness communities (Fig. 3A). For example, at $\rho_{\mathrm{eff}}\approx 1$, mean growth-rate correlations are $\approx -0.81$ for $S=2$, $\approx -0.16$ for $S=4$, and remain low positive ($\approx 0.08$) for $S=8$ (Fig. 3A). This pattern is summarised by $\Delta\mathrm{corr}=\mathrm{corr}_{\mathrm{realised}}-\rho_{\mathrm{eff}}$, which decreases with $\rho_{\mathrm{eff}}$ and becomes strongly negative under high imposed correlation (Fig. 3C).

In the positive-slope regime, realised growth correlations increase with $\rho_{\mathrm{eff}}$ and remain strongly positive (Fig. 3B). At $\sigma_{\mathrm{env}}=0.5$, realised correlations track $\rho_{\mathrm{eff}}$ much more closely: $\Delta\mathrm{corr}$ is near zero at intermediate $\rho_{\mathrm{eff}}$ and becomes only modestly negative at the highest $\rho_{\mathrm{eff}}$ values (Fig. 3C). These results underscore that $\rho_{\mathrm{env}}$ is a driver parameter rather than a synchrony metric: response-direction heterogeneity determines whether shared environmental variation yields weak (or compensatory) versus strong realised synchrony.

### Synchrony–variability relationships

These synchrony patterns are closely linked to community variability. Across the production-scale mixed-slope scenario means, $\mathrm{CV}_{\mathrm{tot}}$ increases strongly with abundance-based synchrony $\phi_{\mathrm{LdM}}$ and, more broadly, with mean pairwise growth-rate correlation (Fig. 4A,B). Scenarios with low $\phi_{\mathrm{LdM}}$ and weakly positive or negative growth-rate correlations have the lowest $\mathrm{CV}_{\mathrm{tot}}$, especially at higher richness. Conversely, scenarios with elevated $\phi_{\mathrm{LdM}}$ and strongly positive growth correlations tend to show high $\mathrm{CV}_{\mathrm{tot}}$, even when $\sigma_{\mathrm{env}}$ is modest. Together, these patterns are consistent with stabilisation in mixed-slope communities being mediated by reduced realised synchrony, including compensatory growth dynamics.
Across the same scenarios, approximate species-level variability (Fig. S4) does not show a compensatory decline that could alone explain community-level buffering, supporting a synchrony-mediated interpretation.

In positive-slope communities, $\phi_{\mathrm{LdM}}$ is generally high and mean growth correlations track imposed driver correlation (Fig. 3B). Community $\mathrm{CV}_{\mathrm{tot}}$ is correspondingly high and more tightly controlled by $\sigma_{\mathrm{env}}$, consistent with shared environmental shocks being transmitted to all species in the same direction.

### Effects of environmental persistence

Increasing temporal autocorrelation $\phi$ inflates community variability in mixed-slope communities (Fig. 5). At fixed $\sigma_{\mathrm{env}}$ and $\rho_{\mathrm{env}}$, $\mathrm{CV}_{\mathrm{tot}}$ increases strongly with $\phi$: for $\sigma_{\mathrm{env}}=0.5$ and $\rho_{\mathrm{env}}=0.5$, $\mathrm{CV}_{\mathrm{tot}}$ rises from $\approx 0.14$ at $\phi=0$ to $\approx 0.58$ at $\phi=0.95$ for $S=2$, and from $\approx 0.07$ to $\approx 0.35$ for $S=4$. This sensitivity reflects the AR(1) structure: increasing $\phi$ at fixed $\sigma_{\mathrm{env}}$ increases environmental persistence and also increases stationary variance, with stationary standard deviation
\[
\sigma_{\mathrm{eff}}=\frac{\sigma_{\mathrm{env}}}{\sqrt{1-\phi^2}}.
\]

Despite this inflation, the qualitative insurance pattern within the mixed-slope regime persists across $\phi$: $\mathrm{CV}_{\mathrm{tot}}$ generally declines as $\rho_{\mathrm{env}}$ increases, and richer communities remain less variable than species-poor communities under the same forcing (Fig. 5). The decline with $\rho_{\mathrm{env}}$ weakens at the highest persistence ($\phi=0.95$) and can flatten at the most extreme $\rho_{\mathrm{env}}$ values, but the ordering by richness remains unchanged.

Floor/extinction frequencies remain essentially absent for $\phi \le 0.7$ and low for $\phi=0.9$ (maximum scenario mean $\bar{e}\approx 0.005$), but rise in the highest-persistence stress case ($\phi=0.95$; maximum scenario mean $\bar{e}\approx 0.049$). Thus the strongest $\phi=0.95$ inflation should be read as a high-persistence stress regime, while the qualitative richness ordering remains intact across the full persistence grid.

### Controls: competition strength and slope magnitudes

Control grids indicate that the insurance patterns do not depend on a particular competition strength or on extreme response slopes. Setting $\alpha_{\mathrm{inter}}=0$ shifts absolute variability but leaves the qualitative contrasts intact: mixed-slope communities still show declining $\mathrm{CV}_{\mathrm{tot}}$ with richness and a generally negative association between $\mathrm{CV}_{\mathrm{tot}}$ and $\rho_{\mathrm{env}}$, whereas positive-slope communities retain an increasing $\mathrm{CV}_{\mathrm{tot}}$–$\rho_{\mathrm{env}}$ relationship.

Narrowing mixed slopes to $b_i \in [-0.25, 0.25]$ reduces overall variability but preserves both the richness effect and the mixed–positive contrast. Communities with narrower mixed slopes continue to exhibit lower realised synchrony and lower $\mathrm{CV}_{\mathrm{tot}}$ than aligned positive-slope communities under the same environmental forcing. Together, these controls indicate that the key ingredient generating insurance in this model is heterogeneity in response direction under shared environmental drivers, rather than any tuned competition strength or unusually steep response slopes.

## Discussion

### Response-direction heterogeneity decouples driver correlation from realised synchrony

These simulations isolate a simple mechanism by which response diversity can, but need not, generate insurance: heterogeneity in response direction can decouple imposed correlation among environmental drivers ($\rho_{\mathrm{env}}$) from realised synchrony. With mixed response slopes, a shared environmental anomaly increases growth for some species while decreasing it for others, generating weak or negative covariances in per-capita growth rates. Mean pairwise growth-rate correlations therefore fall well below $\rho_{\mathrm{env}}$, abundance synchrony $\phi_{\mathrm{LdM}}$ remains low, and $\mathrm{CV}_{\mathrm{tot}}$ is reduced relative to aligned-slope baselines under the same $\sigma_{\mathrm{env}}$, $\rho_{\mathrm{env}}$, and $\phi$.

When response slopes are aligned and positive, imposed driver correlation and realised synchrony reinforce each other. Environmental anomalies push all species’ growth rates in the same direction, so increasing $\rho_{\mathrm{env}}$ yields high realised covariances and elevated $\phi_{\mathrm{LdM}}$. Community variability then rises with $\rho_{\mathrm{env}}$ and is only weakly offset by richness, consistent with stabilisation dominated by statistical averaging rather than compensatory dynamics in some empirical systems [@zhao2022BiodiversityStabilizesPlant].

Imposed driver correlation and realised synchrony are therefore not interchangeable. Treating $\rho_{\mathrm{env}}$ as a proxy for synchrony—an assumption that is often implicit in models and in interpretations of correlated environmental forcing—can misattribute mechanism [@thibaut2013UnderstandingDiversityStability; @loreau2008SpeciesSynchronyIts]. Under heterogeneous response directions, even strong driver correlation can yield near-zero or negative realised growth correlations; under aligned responses the same forcing produces tight positive synchrony. This emphasis on response-direction heterogeneity complements the synchrony framework of Loreau and de Mazancourt [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability] by identifying a concrete lever that controls how environmental covariance is translated into dynamical synchrony.

### Richness as an amplifier of insurance when responses differ

Species richness amplifies the insurance mechanism when response directions differ. In mixed-slope communities, increasing $S$ expands the range of response slopes represented, increasing the likelihood that some species respond positively while others respond negatively to the same environmental anomaly. This strengthens compensatory dynamics, reduces realised synchrony, and drives down $\mathrm{CV}_{\mathrm{tot}}$. In the simulations, $\mathrm{CV}_{\mathrm{tot}}$ declines sharply from $S=2$ to $S=4$ and continues to fall towards $S=8$, even under high $\sigma_{\mathrm{env}}$ and strong imposed driver correlation $\rho_{\mathrm{env}}$. By contrast, when slopes are aligned, richness still reduces variability through statistical averaging, but it cannot reverse the positive $\mathrm{CV}_{\mathrm{tot}}$–$\rho_{\mathrm{env}}$ relationship created by shared environmental forcing.

This pattern aligns with empirical and theoretical work suggesting that synchrony and covariance structure often explain more variation in community stability than richness per se [@valencia2020SynchronyMattersMore; @demazancourt2013PredictingEcosystemStability]. The model sharpens the conditions under which richness functions as “insurance”: strong buffering emerges only when additional species add response-direction diversity, rather than replicating the same response sign. This matches the intent of the response-diversity concept [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines] while making the mechanism explicit by linking response diversity to slopes in a dynamical model. It also highlights a failure mode: when responses are aligned in sign, increases in $\rho_{\mathrm{env}}$ can translate into higher realised synchrony and elevated $\mathrm{CV}_{\mathrm{tot}}$, even in richer communities.

### A mechanistic testbed for response diversity

Recent reviews have noted a mismatch between the prominence of response diversity as a concept and the limited number of dynamical tests that make its stabilising mechanism explicit [@mori2013ResponseDiversityDetermines; @ross2024LimitedTheoreticalEmpirical]. The simulations here provide a deliberately simple testbed: response diversity is represented by a distribution of linear response slopes (b_i) along a single environmental axis; species experience correlated environmental anomalies generated by a shared AR(1) process with adjustable variance, cross-species correlation $\rho_{\mathrm{env}}$, and temporal autocorrelation $\phi$; and the consequences are evaluated via emergent synchrony and $\mathrm{CV}_{\mathrm{tot}}$.

This structure reproduces a core expectation of response-diversity theory: under shared drivers, mixed response directions can generate compensatory dynamics, reduce realised synchrony, and stabilise aggregate biomass, with the effect strengthened by higher richness [@elmqvist2003ResponseDiversityEcosystem; @mori2013ResponseDiversityDetermines]. It also makes the failure mode explicit. When response directions are aligned, shared environmental variation acts as a common shock, synchrony remains high, and diversity contributes mainly through statistical averaging rather than compensation. In that regime, the patterns resemble empirical cases in which diversity stabilises functioning largely via averaging, with weaker evidence for compensatory dynamics [@zhao2022BiodiversityStabilizesPlant].

This contrast offers one mechanistic explanation for why empirical tests of response diversity can yield weak or inconsistent stabilising effects [@ross2024LimitedTheoreticalEmpirical]. Real communities likely experience multiple environmental axes simultaneously, some eliciting heterogeneous responses (favouring compensation) and others eliciting aligned responses (promoting synchrony). If response-diversity metrics aggregate across axes, stabilising and destabilising components may be conflated [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. More generally, inference depends on identifying which environmental drivers dominate temporal variability and how response slopes are distributed along those drivers [@polazzo2024MeasuringResponseDiversity].

The results also complement emerging empirical frameworks that estimate response diversity and “response capacity” from response surfaces under multifarious environmental change [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. Those approaches emphasise measurement in high-dimensional spaces; the present one-dimensional model trades realism for a clear mapping from the sign structure and dispersion of response slopes, together with driver covariance, to realised synchrony and stability.

### Insurance, environmental persistence, and effective variance

Environmental anomalies are modelled as an AR(1) process, with $\sigma_{\mathrm{env}}$ as the innovation standard deviation and $\phi$ controlling both temporal autocorrelation and the stationary variance of the environmental state [@loreau2008SpeciesSynchronyIts]. Varying $\phi$ at fixed $\sigma_{\mathrm{env}}$ therefore changes persistence and increases the effective magnitude of fluctuations, with stationary standard deviation
\[
\sigma_{\mathrm{eff}}=\frac{\sigma_{\mathrm{env}}}{\sqrt{1-\phi^2}}.
\]
As expected, increasing $\phi$ inflates $\mathrm{CV}_{\mathrm{tot}}$. Importantly, it does not erase the qualitative regime contrast: mixed response directions continue to yield lower realised synchrony and lower $\mathrm{CV}_{\mathrm{tot}}$ than aligned responses under comparable forcing, indicating that response-direction heterogeneity can buffer variability even when environmental fluctuations are persistent.

This joint dependence on $\phi$ and stationary variance connects to broader discussions of how autocorrelated environmental variation influences stability [@shanafelt2015BiodiversityProductivitySpatial; @loreau2021BiodiversityInsuranceConcept]. The analysis does not attempt to isolate “pure” persistence effects from variance inflation via rescaling; instead, it shows that the relative insurance benefit of response-direction heterogeneity is robust across a wide range of environmental persistence. For many applied contexts—where the primary concern is variability of aggregate output rather than attribution to variance versus autocorrelation—this robustness is arguably the more relevant result [@loreau2021BiodiversityInsuranceConcept].

### Robustness and scope of the model

Several features of the design suggest that the main patterns are not artefacts of a narrow parameter choice. The mixed–aligned contrast is evident across a broad range of environmental forcing, spanning innovation standard deviations up to $\sigma_{\mathrm{env}}\approx 1.5$, imposed driver correlations from moderately negative to near one ($\rho_{\mathrm{env}}$), and temporal autocorrelations up to $\phi=0.95$. The qualitative results also persist under control manipulations. Removing interspecific competition ($\alpha_{\mathrm{inter}}=0$) leaves both the mixed-versus-aligned contrast and the richness effect intact, indicating that competitive interactions are not required for response-direction heterogeneity to reduce realised synchrony. Narrowing the mixed-slope range reduces overall variability, as expected, but preserves the core ordering: mixed responses still yield lower synchrony and lower $\mathrm{CV}_{\mathrm{tot}}$ than aligned responses under the same environmental forcing.

A further safeguard is that the simulations satisfy numerical and ecological sanity checks. Environmental covariance matrices are positive definite, empirical AR(1) stationary variances match $\sigma_{\mathrm{env}}^2/(1-\phi^2)$ within tolerance, trajectories remain above the numerical floor under stochastic forcing, and synchrony metrics behave as expected in toy cases. Within the model’s assumptions, the mechanism emphasised here—shared environmental variation filtered through heterogeneous response directions—therefore appears robust.

This robustness is necessarily internal to a stylised framework. Species experience a single equicorrelated environmental axis; competition is symmetric; demographic stochasticity, spatial structure, and observation error are absent; and response heterogeneity is confined to a one-dimensional slope parameter. These simplifications are deliberate, because they reduce confounding and isolate the interaction between environmental covariance, response directions, and richness. They also limit direct transfer to real ecosystems, where multiple drivers, asymmetric interactions, and spatial heterogeneity can shape both synchrony and stability [@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial].

### Limitations and future directions

A first limitation is the assumption of an equicorrelated driver structure. Environmental covariance in nature is rarely so uniform: correlations can be block-structured, scale-dependent, spatially patterned, or shaped by teleconnections [@shanafelt2015BiodiversityProductivitySpatial; @loreau2021BiodiversityInsuranceConcept]. Such structures will change how often species experience effectively “opposite” conditions and therefore how easily response-direction heterogeneity can generate compensation. A natural extension is to replace the equicorrelation matrix with more realistic covariance models (e.g. block-correlated or spatially explicit matrices, or empirically estimated covariance), linking directly to spatial insurance and synchrony under global change [@loreau2003BiodiversitySpatialInsurance; @shanafelt2015BiodiversityProductivitySpatial; @valencia2020SynchronyMattersMore].

A second limitation is the focus on a single environmental axis with linear response slopes. Real communities face multidimensional environmental change, and response diversity then depends not only on variation in slopes for each driver but also on correlations among those response surfaces [@mori2013ResponseDiversityDetermines; @ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]. The present model is best interpreted as a limiting case in which one driver dominates. Extending the same slope-based mechanism to higher-dimensional environments—allowing different axes to have different covariance structures, with species aligned along some axes but mixed along others—would provide a more direct bridge between mechanistic prediction and empirical response-surface estimates [@polazzo2024MeasuringResponseDiversity].

A third limitation is the omission of demographic stochasticity, trophic structure, and eco-evolutionary feedbacks, all of which can reshape synchrony and stability [@ives2007StabilityDiversityEcosystems; @loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept]. Demographic noise can weaken the environment–growth coupling for rare species; trophic interactions can transmit or dampen environmental signals across levels; and evolutionary change could shift response slopes over time, potentially eroding or reinforcing response diversity. These extensions are important, but they do not negate the core point: even in a stripped-down setting, response-direction heterogeneity under shared environmental forcing can produce qualitatively different diversity–stability outcomes.

Finally, stability is measured here as temporal variability in total biomass. Other stability dimensions—resistance, resilience, recovery time, and responses to press perturbations—may behave differently under response diversity [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept]. Extending the analysis to alternative stability notions, or to multifunctional stability, would better match the multidimensional stability concepts used in empirical work [@sasaki2019SpeciesAsynchronyResponse; @wagg2021DiversityAsynchronySoil].

### Conclusion

Biodiversity insurance theory has matured to the point where the broad claim—that diversity can buffer ecosystem functioning against environmental variability—is no longer contentious [@loreau2013BiodiversityEcosystemStability; @loreau2021BiodiversityInsuranceConcept]. The sharper questions are mechanistic: when does biodiversity provide insurance, through which pathways, and how do those pathways depend on environmental covariance and response diversity [@ross2024LimitedTheoreticalEmpirical; @polazzo2024MeasuringResponseDiversity]? The simulations here provide a clear answer within a simple dynamical model. When species share environmental drivers but differ in response direction, biodiversity can decouple imposed driver correlation $\rho_{\mathrm{env}}$ from realised synchrony, generating compensatory dynamics and stabilising aggregate biomass relative to aligned-response baselines. When responses are aligned, the same environmental covariance acts as a common shock that elevates synchrony and increases community variability, with richness providing only modest buffering through statistical averaging.

The implication is straightforward: richness alone is insufficient. Stabilisation depends on how species’ response directions are arranged relative to the structure of environmental variation. Making that relationship explicit offers a route to reconciling divergent empirical results on richness, synchrony, and response diversity, and it suggests that future work should quantify not only species counts but also the alignment of response slopes with the covariance structure of the dominant environmental drivers.

## References

[To do in Zotero later]

---

Tables and their captions are given in `paper/manuscript/text/tables.md`
Figure captions are given in `paper/manuscript/text/figure_captions_v2.md`

---

## Reproducibility
- Environment: `pyproject.toml` managed with uv; run tests `uv run pytest`.
- Entry points: `analysis/run_full_grid.py`, `analysis/plot_grid.py`, and `analysis/run_all.py`; data under `data/sim/grid/`.
