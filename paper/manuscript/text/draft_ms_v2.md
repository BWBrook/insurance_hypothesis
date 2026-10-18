```{=latex}
\raggedright
```

# Shared environments can destabilise communities with balanced opposing responses

## Abstract

Species that gain and lose under the same environmental fluctuation can compensate, suggesting that a shared environment should stabilise communities with balanced opposing responses. I tested this prediction in stochastic Ricker communities of competing species. Changing only response signs reversed the effect of exposure correlation: at the focal fluctuation size, near-perfect correlation reduced the mean squared coefficient of variation (CV) of total abundance to 0.32 of its independent-exposure value for balanced responses and raised it 2.99-fold for the same response magnitudes with aligned signs. The benefit of shared exposure declined as fluctuations grew, and sometimes reversed. In an eight-species community with stronger competition, shared exposure increased mean squared community CV by 46% despite perfectly balanced responses and no retained-window contact with the numerical floor. Species' fluctuations still partly offset one another; compensation persisted while correlation became destabilising. A second-order calculation explained the onset of incomplete cancellation: changes in the squared magnitude of opposing population departures contribute to variation in total abundance. Its predictions were within 4% of simulated ratios across 23 prespecified small-fluctuation combinations of richness, competition and environmental autocorrelation, but became inaccurate at larger fluctuations. Increasing fluctuation size also shifted the composition boundary between buffering and amplification towards less aligned responses. Balanced response diversity therefore does not guarantee that sharing an environment adds stability. In this model, the outcome depends on fluctuation size and population feedback as well as on the balance of species' contributions.

## Keywords

biodiversity; response diversity; ecosystem stability; compensatory dynamics; environmental covariance; nonlinear population dynamics; insurance hypothesis.

## Introduction

When a warm year favours one species and harms another, their changes can offset one another in the community total. This compensation is a central mechanism of biodiversity insurance: species with different environmental responses can stabilise aggregate abundance, biomass or productivity [@yachi1999BiodiversityEcosystemProductivity; @gonzalez2009CausesConsequencesCompensatory; @loreau2021BiodiversityInsuranceConcept]. Sharing an environmental fluctuation can strengthen that protection. The same warm year promotes one species and suppresses its opposite responder, whereas independent exposures need not produce gains and losses at the same time. If both species respond in the same direction, shared exposure instead makes their fluctuations reinforce one another. Whether a common environment stabilises a community therefore depends on the organisms that experience it.

The strength of compensation also depends on how much each species contributes. A rare cool-favoured species cannot fully offset a dominant warm-favoured one, even if their per-capita responses are equal and opposite. Stochastic community theory accounts for differences among species through response covariances and the feedbacks that transmit environmental shocks through population dynamics [@ives1999StabilityVariabilityCompetitive; @loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability]. Abundance weighting is also central to measuring response diversity [@ross2023HowMeasureResponse]. For small fluctuations around a stable equilibrium, these ideas give a clear prediction in a symmetric competitive community: shared exposure reduces total-abundance variability when opposing abundance-weighted responses cancel sufficiently, and perfect balance removes the shared environmental input from the linearised total.

How much of this protection survives when fluctuations are large? Population change depends on current abundance and density feedback, so cancellation of the direct environmental input need not produce cancellation of the resulting abundance changes. Even at a balanced equilibrium, multiplicative growth makes the gain under a favourable shock larger than the loss under an equally strong unfavourable shock. Away from equilibrium, the abundance of each responder and its subsequent density-dependent adjustment also matter. Existing theory explicitly recognises its small-perturbation assumption [@demazancourt2013PredictingEcosystemStability]. Here I ask how the benefit of shared exposure changes beyond that limit, and whether sharing an environment can make a perfectly balanced community more variable than independent exposure would.

Previous multispecies Ricker simulations have linked environmental covariance, temporal colour and community assembly to diversity–stability relationships [@fowler2013ColonizationCovarianceColour]. Work on response diversity likewise emphasises that stability depends on the responses and interactions of the constituent species [@mori2013ResponseDiversityDetermines; @ross2024LimitedTheoreticalEmpirical; @ross2026ExpertledPrioritiesResponse]. Testing the contribution of response direction requires a comparison that holds response magnitudes fixed. Testing the contribution of shared exposure requires a second comparison, between correlated and independent environments within the same community. These comparisons address different questions: opposing responses can remain advantageous relative to aligned responses even if environmental correlation no longer adds stability.

I use stochastic Ricker communities to connect these two comparisons to fluctuation size. A sign-only contrast first establishes how opposing responses alter the effect of exposure correlation. I then measure how that effect changes with environmental innovation variance and derive its leading departure from the small-fluctuation limit. Predictions made before additional simulations test the calculation across richness, competition and environmental autocorrelation. Continuous changes in response balance and equilibrium abundance locate the transition from buffering to amplification at different fluctuation sizes. The analysis asks when shared exposure adds stability, how nonlinear population dynamics limit that benefit, and whether the benefit can reverse even when responses remain balanced.

## Methods

### Community dynamics and environmental exposure

The abundance of species $i$ follows a competitive stochastic Ricker map,
\[
N_i(t+1)=N_i(t)\exp\left[r_0+b_i z_i(t)-\frac{N_i(t)+\alpha\sum_{j\ne i}N_j(t)}{K_i}\right].
\]
Here $r_0$ is intrinsic growth, $K_i$ scales density dependence, intraspecific competition is fixed at one, and $\alpha$ is interspecific competition. Defaults are $r_0=1$, $K_i=100$ and $\alpha=0.3$. An isolated species has equilibrium abundance $r_0K_i$; with equal $K_i=K$, the community equilibrium is $N_i^\ast=n=r_0K/[1+\alpha(S-1)]$. For unequal $K_i$, the interior equilibrium solves $C_\alpha\mathbf N^\ast=r_0\mathbf K$, where $C_\alpha$ has diagonal entries one and off-diagonal entries $\alpha$.

The response slope $b_i$ determines whether growth increases or decreases with exposure $z_i$, and by how much. **Mixed** responses are evenly spaced in $[-0.5,0.5]$, so they sum to zero; odd-richness communities also contain a zero slope. **Matched aligned** responses use the same magnitudes with nonnegative signs, $b_i=|b_i^{\mathrm{mixed}}|$. Reversing signs under symmetric Gaussian exposures preserves each species' marginal forcing distribution and changes only the covariance of forcing among species. A **steep aligned** treatment, with slopes evenly spaced in $[0.1,1.0]$, is retained in the Supporting information; it changes magnitude as well as direction and is not a sign-only control.

Exposures follow a multivariate AR(1) process,
\[
\mathbf z_t=\phi\mathbf z_{t-1}+\boldsymbol\varepsilon_t,
\qquad \boldsymbol\varepsilon_t\sim\mathcal N(\mathbf0,\sigma_{\mathrm{env}}^2C(\rho_{\mathrm{eff}})).
\]
The equicorrelation matrix $C$ has diagonal entries one and common off-diagonal correlation $\rho_{\mathrm{eff}}$. All exposures represent the same physically oriented variable: a positive anomaly means, for example, a warmer temperature for every species, although trajectories can differ among microhabitats. The innovation SD $\sigma_{\mathrm{env}}$ differs from the stationary exposure SD, $\sigma_z=\sigma_{\mathrm{env}}/\sqrt{1-\phi^2}$. Thus increasing $\phi$ at fixed innovation variance changes both persistence and stationary variance. Defaults use $\phi=0.4$.

For $S>1$, positive definiteness requires $-1/(S-1)<\rho<1$. Requested correlations are converted to
\[
\rho_{\mathrm{eff}}=\min\!\left(\max\!\left(\rho_{\mathrm{env}},-\frac1{S-1}+10^{-6}\right),1-10^{-6}\right).
\]
Both values are retained. I refer to $\rho_{\mathrm{eff}}=1-10^{-6}$ as near-perfect correlation; $\rho=0$ gives independent exposures. The lower bound also clips the requested $S=4$, $\rho_{\mathrm{env}}=-0.5$ treatment in the supplementary persistence gradient.

The main experiments use 1000 replicate trajectories per scenario, each of 600 time steps with the first 300 discarded. A robustness experiment uses longer trajectories, described below. Exposures start at zero and abundances at $K_i/2$. Seeds are deterministic functions of a grid's base seed, scenario and replicate indices; environmental realisations are not paired across treatments. An abundance floor of $N_{\min}=10^{-9}$ and exponent clipping to $[-50,50]$ prevent numerical failure. Floor contact and guard diagnostics are reported separately from ecological interpretation. Table 1 summarises the design; the complete grid inventory and floor occupancy are in the Supporting information.

### Stability comparisons and the linear benchmark

Community variability is the temporal coefficient of variation of total abundance, $N_{\mathrm{tot}}=\sum_i N_i$, computed separately for each retained trajectory using the sample mean and sample variance with divisor $L-1$, where $L=300$ in the main experiments and $L=3000$ in the longer runs. I compare mixed with matched aligned communities under the same environmental conditions to measure the sign-only advantage. To measure the additional effect of exposure correlation within a community, I use
\[
R=\frac{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}=1-10^{-6}]}{\mathbb E_{\mathrm{rep}}[\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}=0]}.
\]
This is a ratio of mean replicate squared CVs. Values below one indicate buffering by shared exposure; values above one indicate amplification. These terms describe a relative comparison, not an absolute decline in variability as environmental variance increases. Direct matched-to-mixed comparisons at shared exposure use their own mean squared CVs, rather than the quotient of two separately estimated values of $R$.

For small fluctuations, species $i$ contributes $a_i=N_i^\ast b_i$ to the aggregate environmental input $F=\sum_i a_i z_i$. Under equicorrelation,
\[
\operatorname{Var}(F)=\sigma_z^2\left[(1-\rho_{\mathrm{eff}})\sum_i a_i^2+\rho_{\mathrm{eff}}\left(\sum_i a_i\right)^2\right].
\]
The abundance-weighted alignment index
\[
A=\frac{(\sum_i a_i)^2}{S\sum_i a_i^2}
\]
ranges from zero for balanced weighted responses to one for identical weighted responses. Increasing exposure correlation reduces forcing variance when $A<1/S$ and increases it when $A>1/S$. Relative to independent exposure, the forcing-variance ratio is $(1-\rho_{\mathrm{eff}})+\rho_{\mathrm{eff}}SA$.

With equal $K_i$, total abundance near equilibrium follows a single linear mode, $X_{t+1}=\lambda_cX_t+F_t$, where $\lambda_c=1-r_0$. Because every exposure has the same temporal autocorrelation, the stationary variance multiplier from this feedback is independent of exposure correlation and cancels in the ratio. The forcing benchmark therefore also gives the ratio of stationary total-abundance variances in the linearised equal-$K$ model. With unequal $K_i$, both the weights and the feedback matrix change, so the forcing benchmark alone no longer determines abundance variability. Nonlinear dynamics can break the correspondence even with equal weights (Supporting information).

### A small-fluctuation prediction for balanced communities

Perfectly shared exposure and balanced slopes remove the first-order total-abundance response. They do not remove departures of individual populations from equilibrium. In the equal-$K$ model, these opposing departures persist through the contrast mode,
\[
\lambda_d=1-r_0\frac{1-\alpha}{1+\alpha(S-1)}.
\]
Writing first- and second-order abundance departures as $\mathbf x^{(1)}$ and $\mathbf x^{(2)}$, with $X^{(2)}=\sum_i x_i^{(2)}$, expansion of the full Ricker update gives
\[
X_{t+1}^{(2)}=\lambda_cX_t^{(2)}+
\frac{\lVert\mathbf x_{t+1}^{(1)}\rVert^2-\lVert\mathbf x_t^{(1)}\rVert^2}{2n}.
\]
The second term is a signed change in squared departure, with zero stationary mean and nonzero variance. It includes abundance–growth products as well as curvature of the exponential growth response; it is not a uniformly positive convexity correction.

For $r_0=1$, stationary Gaussian forcing and exact shared exposure, the resulting population-variance ratio has leading form
\[
R_{\mathrm{pop}}=c\sigma_{\mathrm{env}}^2+O(\sigma_{\mathrm{env}}^4),
\qquad
c=\frac{\sum_i b_i^2}{(1-\lambda_d^2)(1-\lambda_d\phi)^2}.
\]
This local prediction assumes a stable positive equilibrium and inactive numerical guards. It applies to the balanced shared-exposure endpoint, not to an arbitrary partially aligned community. For the focal four-species community, $c=1.65465$. The expected 300-step sample-variance correction gives a leading coefficient of 1.66752 for the sampled CV ratio, a difference of 0.78%; imperfect correlation also leaves approximately $10^{-6}$ of the first-order ratio. The full derivation and finite-window calculation are in the Supporting information.

### Simulation contrasts and prospective tests

The focal sign-only experiment compares mixed and matched aligned responses at $S=4$ and 8, $\sigma_{\mathrm{env}}=0.5$, $\phi=0.4$, and requested correlations from zero to one in increments of 0.1 (Fig. 1A). A composition experiment at $S=4$ follows two paths between buffering and amplification (Fig. 1B). The first rotates the mixed response vector into its matched aligned counterpart,
\[
\mathbf b(q)=\cos(\pi q/2)\,\mathbf b_{\mathrm{mixed}}+
\sin(\pi q/2)\,|\mathbf b_{\mathrm{mixed}}|,
\]
for nine equally spaced $q\in[0,1]$. The endpoint vectors are orthogonal and have equal norm, so the rotation holds overall response magnitude fixed. The second retains the mixed slopes and varies $\mathbf K(d)=100(1-0.3d,1-0.1d,1+0.1d,1+0.3d)$ for $d\in\{0.25,0.5,0.75,1,1.1\}$, using the balanced endpoint for $d=0$. Every treatment has a positive interior equilibrium, and the constant sum of $K_i$ holds deterministic total abundance constant. This path changes feedback as well as abundance weights. An endpoint sensitivity repeats the sign contrast at $r_0\in\{0.25,0.5,1,1.5\}$ (Fig. 1C).

To measure amplitude dependence, a new grid repeats the 14 composition treatments at $\sigma_{\mathrm{env}}\in\{0.1,0.2,0.3,0.5,0.7,1,1.3\}$, with independent and near-perfectly shared exposures (Fig. 2). The balanced and matched aligned endpoints supply the sign-only amplitude comparison. Older grids independently replicate the balanced amplitude curve and extend it into a floor-affected stress region. Boundary comparisons use the simulated treatment points and their uncertainty. Where crossings are linearly interpolated between adjacent treatments, they are descriptive summaries; the design does not resolve an exact continuous threshold.

The second-order prediction was derived from the focal setting before three additional grids crossed $\alpha\in\{0.1,0.3,0.6\}$, $S\in\{2,4,8\}$ and $\phi\in\{0,0.4,0.8\}$, with mixed responses, $r_0=1$, equal $K_i$, $\sigma_{\mathrm{env}}\in\{0.1,0.2,0.5,1\}$, and both correlation endpoints (Fig. 3). Predictions were calculated for all 27 parameter combinations before these simulations. One combination repeats the derivation setting with independent seeds; the other 26 extend it. The prespecified small-fluctuation subset comprises combinations with predicted $R<0.1$ at $\sigma_{\mathrm{env}}=0.1$. Success required the simulated ratio to lie within 20% of the prediction and the ratio $R(0.2)/R(0.1)$ to lie between three and five. The written spec restricted the latter criterion to predicted $R(0.2)<0.2$, whereas the contemporaneous discussion record did not; both versions are reported. Larger predicted departures test the limits of the approximation, and no floor-affected cell is discarded.

Supplementary grids retain the realised-synchrony comparison, the steep aligned stress extension, a deterministic richness assembly sequence and a fixed-innovation persistence gradient (Supporting information). Adding species in the assembly sequence changes slope composition, root-mean-square slope and equilibrium abundance together. Increasing $\phi$ at fixed innovation SD changes persistence and stationary variance together. Neither sequence identifies a pure effect of richness or environmental persistence.

Five balanced-response settings in which shared exposure increased variability without retained floor contact were then repeated with 6000 steps, 3000 burn-in and 500 independently seeded replicates per exposure condition. This follow-up was specified before the longer runs, with success defined as a ratio above one and a 95% Monte Carlo lower bound also above one in each of the five settings. The original parameter settings were retained without expansion.

### Uncertainty and diagnostic checks

Ninety-five per cent Monte Carlo intervals for $R$ use a log-ratio delta method applied to the replicate squared CV distributions. They quantify simulation error within the model, not uncertainty about its structure. An additional multiplicity check used Bonferroni-adjusted 95% familywise intervals across all 108 setting-by-amplitude comparisons in the mechanism grids. Means of CV and ratios of mean squared CV are kept distinct. Production summaries also retain the exact variance decomposition, $\operatorname{Var}(N_{\mathrm{tot}})=\sum_i\operatorname{Var}(N_i)+2\sum_{i<j}\operatorname{Cov}(N_i,N_j)$. A negative aggregate covariance indicates that population fluctuations partly offset one another; it is descriptive accounting, not an independent causal test.

Abundance synchrony and mean pairwise log-growth correlation provide further diagnostics in the Supporting information. The implementation defines log-growth using $\log[N_i(t+1)+N_{\min}]-\log[N_i(t)+N_{\min}]$, adding an offset after abundance flooring. Zero-forcing synchrony is undefined. Floor occupancy is the fraction of retained steps at $N_{\min}$, averaged over species; floored populations can recover, so this is not biological extinction. A separate guard diagnostic examines full trajectories, including burn-in, at all five balanced-reversal settings with 200 full 600-step and 100 full 6000-step trajectories per exposure condition, seeded separately from the production runs. Its coverage is distinct from the retained production summaries and from the earlier three-scenario stress diagnostic (Supporting information).

## Results

### Response signs determine whether shared exposure helps

Under independent exposures the mixed and matched aligned treatments have the same forcing distribution and nearly identical variability. At the focal $S=4$, $\sigma_{\mathrm{env}}=0.5$ setting, both have mean $\mathrm{CV}_{\mathrm{tot}}=0.106$. At exposure correlation 0.5 the mixed and matched aligned means separate to 0.084 and 0.149, and near perfect correlation they are 0.059 and 0.184 (Fig. 1A). The corresponding shared-to-independent squared-CV ratios are 0.320 (95% Monte Carlo interval 0.315–0.325) and 2.99 (2.97–3.02). Changing response signs alone therefore reverses the effect of exposure correlation.

The response rotation passes from buffering to amplification, but nonlinear dynamics displace the transition from its first-order benchmark (Fig. 1B). At the tested alignment $A=0.247$, the benchmark predicts weak buffering ($R=0.988$), whereas the simulation shows weak amplification ($R=1.043$, 1.028–1.059). The balanced endpoint retains substantial variability where the benchmark predicts almost none. Along the unequal-$K_i$ path, $R$ changes from 0.964 (0.952–0.975) at $A=0.230$ to 1.053 (1.041–1.065) at $A=0.257$. Here response signs are unchanged: altered abundance weights and feedback together remove the benefit of shared exposure. The benchmark at the upper point is 1.030, so nonlinear departures do not universally compress ratios towards one.

The sign contrast survives all four tested growth rates (Fig. 1C). At $r_0=0.25,0.5,1$ and 1.5, mixed-response ratios are 0.663, 0.439, 0.320 and 0.323; matched aligned ratios are 2.77, 2.94, 2.99 and 2.97. The result is therefore not confined to $r_0=1$, where the linearised total-abundance mode has no direct carryover from the previous step.

### Larger fluctuations weaken the benefit and change the composition boundary

In the matched amplitude grid, the balanced community's shared-to-independent ratio rises from approximately 0.017 at innovation SD 0.1 to 0.320 at 0.5 and 0.961 at 1.3 (Fig. 2A). The older independent-seed grid gives corresponding values of 0.0165, 0.3197 and 0.9371. The benefit of correlated exposure thus declines strongly as fluctuations grow. Matched aligned communities remain amplified, although their ratio falls from 3.19 to 2.31 across the same amplitude range. Directly comparing the two communities under shared exposure, aligned responses produce approximately 190 times the mean squared CV of balanced responses at SD 0.1 and 2.4 times at SD 1.3. Opposing signs retain an advantage even where the additional benefit of exposure correlation is small.

Amplitude also changes which compositions are buffered (Fig. 2B). At alignment $A=0.247$, the ratio rises from 0.986 (0.978–0.995) at SD 0.1 to 1.056 (1.034–1.077) at SD 0.7, with no retained floor contact at either amplitude. Thus the same composition switches from buffering to amplification as fluctuations grow. Linear interpolation of neighbouring simulated points places the rotation crossing near $A=0.250$ at SD 0.1 and $A=0.145$ at SD 1.3, but the upper-amplitude bracket spans a wide alignment interval, its lower point has an interval overlapping one, and both bracketing treatments have some floor contact. These interpolations summarise the curve shapes rather than resolve an exact or strictly monotonic threshold. The unequal-$K_i$ path shifts in the same direction, but its upper-amplitude comparisons include floor contact and are supporting evidence. On the rotation path, retained floor contact occurs only at SD 1.3, with very low frequencies; the treatment-specific rates are reported in the Supporting information.

### The nonlinear onset is predictable across community settings

Twenty-three of the 27 parameter combinations meet the prespecified small-fluctuation eligibility criterion, including the independent-seed repeat of the derivation setting. All 23 pass both versions of the acceptance criteria (Fig. 3A). At innovation SD 0.1, simulated ratios are 0.965–1.015 times the stationary second-order prediction, across coefficients $c$ from 0.52 to 7.14. Doubling innovation SD raises the ratio by factors of 3.50–3.98, close to the predicted quadratic scaling. Thus the calculation predicts the initial departure in 22 additional parameter combinations as well as reproducing the focal one.

The approximation becomes less accurate at larger departures. The four combinations outside the small-fluctuation subset have coefficients from 14.6 to 84.7; at SD 0.1, observed-to-predicted ratios range from 0.792 to 0.970. In the focal community at SD 0.5, the stationary prediction is 0.414 compared with the observed 0.320. The calculation predicts the onset of incomplete cancellation, not the nonlinear threshold or the full amplitude curve.

### Shared exposure can destabilise a perfectly balanced community

Five tested settings have balanced responses, no retained floor contact at either exposure endpoint, and a shared-to-independent ratio whose interval lies entirely above one (Fig. 3B). At $S=8$, $\alpha=0.6$, $\phi=0.4$ and innovation SD 0.5, the ratio is 1.458 (1.429–1.488): sharing the environment increases mean squared community CV by about 46%. Three other eight-species settings at SD 1.0 give ratios from 1.19 to 1.65. A fifth, at $\alpha=0.6$, $\phi=0.8$ and SD 0.2, gives 1.465 (1.430–1.501). All five Bonferroni-adjusted familywise intervals also remain above one.

All five reversals persisted in the longer trajectories, with ratios from 1.187 to 1.654 and every lower interval bound above 1.17. The SD 0.5 example gave 1.457 (1.444–1.470), almost unchanged from the original estimate. Four settings remained free of retained floor contact; in the fifth, one replicate had a floor frequency of 0.00033. The separate full-trajectory diagnostic observed no exponent clipping or floor events at either trajectory length in any of the five settings (Supporting information).

Compensatory fluctuations persist during this reversal. In the SD 0.5 example, the aggregate covariance contribution is approximately -879 under independent exposure and -716 under shared exposure, while mean total-abundance variance increases from 144 to 210. The covariance remains negative but offsets less of the summed species variance under shared exposure. The reversal therefore concerns the effect of environmental correlation on the whole community, not disappearance of all compensation. It occurs in the tested eight-species settings with larger small-fluctuation coefficients; the design does not isolate richness or contrast persistence as its sole cause.

## Discussion

A community can contain perfectly balanced opposing responders and still become more variable when its members share the same environmental fluctuations. This reversal is stronger than incomplete cancellation: environmental correlation changes from a source of buffering to a source of amplification without changing any response sign. The matched-sign control establishes why shared exposure can help, and the amplitude experiments show where that benefit weakens. The second-order calculation predicts the initial loss of buffering across a range of community settings. Together, these results connect an ecological stability comparison to a specific nonlinear contribution to population change.

The distinction between balanced responses and constant total abundance is central. Linearised direct effects cancel under shared exposure, but the populations depart from equilibrium in opposite directions. Changes in the squared magnitude of those departures then contribute to the total. This quadratic input can have either sign and has zero stationary mean. The one-step convexity of multiplicative growth suggests why cancellation may be incomplete, but abundance–growth products and density feedback are required to obtain the stationary result. The predictive test supports this local mechanism across richness, competition and environmental autocorrelation. Its increasing error outside the small-fluctuation regime also sets a clear limit: it does not quantitatively explain the reversal or determine its threshold.

The coefficient separates two ingredients of the leading departure: the combined response magnitude, $\sum_i b_i^2$, and the transmission of fluctuations through the contrast mode and environmental autocorrelation. At fixed response magnitude, $r_0=1$ and positive stable $\lambda_d$, longer-lived contrast departures increase the leading ratio. In the tested symmetric model, stronger competition and greater richness increase $\lambda_d$. Richness also changes the slope vector and equilibrium abundance, while changes in $r_0$ alter both common and contrast feedback. These compound paths cannot identify a pure causal effect of richness or memory at finite noise. They do show why response balance alone is inadequate: the same cancellation of direct forcing can accompany substantially different abundance variability.

Opposing responses nevertheless remain useful. Across the matched four-species amplitude series, balanced communities are less variable than aligned communities under shared exposure, even when sharing the environment provides little additional protection. The distinction is between the benefit of response direction and the benefit of environmental correlation within a community. Likewise, a negative aggregate covariance or low synchrony does not establish that increasing exposure correlation will stabilise the community. Negative covariance persists in the reversal settings because some population fluctuations still offset one another. Covariance-based synchrony metrics describe that accounting, but they do not isolate the process that generated it [@loreau2008SpeciesSynchronyIts; @loreau2013BiodiversityEcosystemStability].

The composition boundary makes the same limitation visible away from perfect balance. Increasing the alignment of responses changes correlated exposure from buffering to amplification, and increasing fluctuation size moves that transition towards less aligned compositions. Changing equilibrium abundances while retaining every response sign can also remove buffering. Because the unequal-$K_i$ path changes feedback as well as weights, its results should be interpreted jointly. For empirical work, a species list or an unweighted tally of response signs is insufficient. Responses must be weighted by contributions to the aggregate and interpreted alongside the environmental and population dynamics [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity].

The empirical prediction is conditional and testable. Where direct environmental responses nearly balance, the local model predicts that the relative benefit of shared exposure declines with the size of per-capita shocks, especially where compositional departures persist. Testing that prediction requires consistently oriented environmental measurements, species response functions, contribution weights and information about population feedback. The orientation matters: if each species has its own freely reversible latent environmental axis, response signs and exposure correlations cannot be interpreted separately. The invariant quantity is then the covariance of demographic shocks, $D_b\Sigma_zD_b$, where $D_b=\operatorname{diag}(b_i)$. With several physical drivers, a community may compensate along one axis and respond in the same direction along another; the full covariance and response structure must be retained [@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity].

These findings extend established theory within a deliberately restricted model. Earlier work already links abundance weighting, environmental covariance and dynamical feedback, and explicitly acknowledges the small-perturbation assumption [@ives1999StabilityVariabilityCompetitive; @demazancourt2013PredictingEcosystemStability]. Earlier Ricker simulations also show that environmental covariance and temporal colour interact with community assembly [@fowler2013ColonizationCovarianceColour]. Here the environmental response is linear in log growth, competition is symmetric, and exact response-magnitude controls separate sign effects. Demographic stochasticity, observation error, dispersal and trophic interactions are absent. Different density dependence, nonlinear environmental response curves and asymmetric interactions can alter the second-order contribution and its stability consequences. The derived coefficient and observed reversal should therefore be tested under those alternatives before being treated as general properties of biodiversity insurance.

The supplementary assembly and persistence gradients have a narrower role. Their changing slope compositions, equilibrium abundances and stationary environmental variances prevent isolated causal claims about richness or temporal colour. Their severe-forcing regions also contact the numerical floor. The main reversal persists across longer observation windows, and the numerical diagnostics support its interpretation as a property of the population dynamics. These checks do not estimate its frequency in natural communities. Stability here is temporal variability of total abundance; resistance, recovery and multifunctional stability are different properties [@ives2007StabilityDiversityEcosystems; @mori2013ResponseDiversityDetermines; @loreau2021BiodiversityInsuranceConcept].

Balanced response diversity can therefore coexist with a destabilising effect of shared environmental variation. Predicting the sign and size of that effect requires the scale of fluctuations and their transmission through population dynamics, as well as the covariance and balance of direct responses. The small-fluctuation calculation supplies a quantitative starting point; the nonlinear simulations show how far the resulting compensation can depart from it.

## Artificial intelligence statement

OpenAI Codex (GPT-6, with GPT-5.6 specialist agents) and Anthropic Claude (model identifiers `claude-fable-5-1` and `claude-opus-5-5`) contributed to mathematical derivation, model and software development, simulation design and execution, data analysis, literature searches and source checking, figure production, independent scientific audits, and manuscript drafting and revision. The systems exchanged and challenged analyses and drafts through a shared research correspondence. The human author contributed the research question, scientific framing, interpretation and critical review, and takes responsibility for the final content.

## References
