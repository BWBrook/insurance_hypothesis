# Adversarial external review and detailed line-edit

**Target journal:** *Oikos*  
**Material reviewed:** anonymous manuscript, anonymous Supporting Information, display items, references, captions, reviewer brief, provenance records, and clean reproducibility repository  
**Review date:** 9 August 2026  
**Recommended disposition before submission:** **Major revision, then submit**  

---

## 1. Review boundary, anonymity, and archive integrity

I treated the package as a genuinely double-anonymized submission. The directory `03_editorial_materials_unblinded` was excluded before extraction; no file within it was extracted or read. This report therefore contains no information from the cover letter or author-information materials.

The supplied archive's SHA-256 digest matched the commissioned value exactly:

```text
de3c2c9c5354c79d8c2336d2162455e59e5c6c5b1f431099905107201ca8a385
```

The anonymous payload was internally coherent. The safe-tree checksum audit found no mismatches among the files reviewed, the manuscript-to-figure links resolved, the displayed results were consistent with the production summaries I inspected, and the source package was unusually well organized for external review.

I also attempted an independent execution audit. In the available review environment, 41 tests passed under Python 3.13. Seven workflow tests stopped before their scientific assertions because no Parquet engine (`pyarrow` or `fastparquet`) was installed. A frozen Python 3.12 environment could not be reconstructed because the isolated environment attempted to download the specified interpreter and had no network route. Static analysis could not be rerun because `pyright` was absent. These are environment limitations, not evidence of scientific test failures. The bundle's own provenance records report 48 passing tests, clean static analysis, a successful analysis workflow, anonymity and path scans, source-fidelity checks, 85 payload checksums, ZIP integrity, and extracted-tree comparison. I regard the computational package as strong, while distinguishing those reported checks from the subset independently rerun here.

---

## 2. Executive assessment

### Overall verdict

The manuscript contains a real, intelligible, and potentially valuable theoretical result: **positive correlation among commonly oriented environmental exposures can stabilize aggregate abundance when species' demographic responses are sufficiently balanced in sign, whereas the same exposure correlation destabilizes the aggregate when responses are aligned**. The strongest supplied control—identical response magnitudes with only the signs changed—supports this result. I found no fatal coding defect and no reason to doubt the existence of the mechanism.

The present manuscript nevertheless gives too much evidential weight to comparisons that do not isolate the advertised causes. In particular:

1. the headline mixed-sign versus aligned comparison changes response magnitude as well as sign;
2. the richness sequence changes response-coefficient variance, deterministic total abundance, and local dynamics as richness changes;
3. the temporal-persistence treatment holds innovation variance fixed, thereby increasing stationary environmental variance with autocorrelation;
4. the central mechanism is close to an algebraic consequence of the imposed covariance structure, but the manuscript does not yet exploit that fact to deliver a general theoretical criterion;
5. the ecological interpretation of “environmental synchrony” is not invariant unless the species-specific environmental variables share a fixed physical orientation; and
6. exact cancellation is obtained in an equal-abundance, symmetric community, whereas the real condition is **abundance-weighted response balance**.

These issues do not collapse the paper. They determine what the paper can presently claim and what is needed to make it a convincing *Oikos* contribution. The most important revision is conceptual rather than computational: promote the magnitude-matched control, derive the general covariance criterion, and make the nonlinear simulations a test of where that criterion survives or fails.

### Decision I would give in formal peer review

**Major revision**—or “reject with encouragement to resubmit” if the editorial system does not offer a major-revision route for a first decision. I would not recommend rejection on the ground that the core mechanism is false. I would resist acceptance because the current abstract, results hierarchy, richness language, and persistence language imply cleaner causal tests than were actually performed.

### Submission advice

The scientific core is a **GO**. The current submission form is a **HOLD**. A targeted revision should be sufficient; this does not require rebuilding the project from first principles.

---

## 3. What the paper contributes

The model separates two quantities that are often conflated:

- correlation among environmental exposures or drivers, and
- correlation among the demographic consequences of those exposures.

For species with oppositely signed response coefficients, positively correlated exposures can generate negatively correlated demographic forcing. Aggregate abundance can then be stabilized even though the raw environmental series are strongly positively correlated. Conversely, similarly signed responses transmit a common environmental mode into the community total.

The supplied simulations establish that this sign-dependent reversal persists in a nonlinear, density-regulated, multispecies Ricker system. The positive magnitude-matched treatment is especially persuasive because, under the symmetric Gaussian forcing used here, changing a coefficient from \(b_i\) to \(|b_i|\) preserves every species' marginal forcing distribution while altering only the cross-species covariance pattern. That is the clean causal comparison and should become the paper's centre of gravity.

The broader contribution could be considerably stronger than the current binary treatment suggests. In general, the decisive quantity is not “mixed signs” as such, but the projection of an abundance-weighted response vector onto the dominant environmental covariance modes. That formulation connects the paper directly to covariance, portfolio, response-diversity, and community-stability theory and yields a sharp, testable boundary condition.

---

## 4. Principal strengths

1. **The question is conceptually important.** Raw environmental covariance is routinely treated as a proxy for population synchrony; the paper shows why this can be wrong.

2. **The magnitude-matched control works.** The central reversal remains substantial when the response magnitudes are identical and only their signs differ. The mechanism is therefore not an artefact of the very broad positive-slope treatment.

3. **The model is transparent.** Equations, parameter grids, response sequences, initialization, burn-in, floors, clipping, metrics, seeds, and production outputs are all exposed.

4. **Driver correlation and realized growth synchrony are separated.** This is one of the manuscript's clearest conceptual choices and should be emphasized even more.

5. **Diagnostics are unusually candid.** The package records floor occupancy, stress-regime behaviour, and the stationary-variance consequence of changing temporal autocorrelation.

6. **The authors already recognize several limitations.** The richness-sequence caveat, the partially algebraic nature of the Loreau–de Mazancourt synchrony association, and the persistence/variance confounding are not hidden. The problem is chiefly that these caveats arrive later than the claims they qualify.

7. **The reproducibility package is close to exemplary.** It is clean, deterministic, tested, and reviewer-oriented. With a public archival DOI and a short data/code availability statement, it should satisfy the journal's reproducibility expectations well.

8. **The manuscript is within the likely *Oikos* format envelope.** The main text is about 5,981 words, the abstract is below 300 words, and the present combination of one table plus five main figures uses the journal's six-display-item allowance exactly.

---

## 5. Fatal-flaw screen

I found **no fatal flaw** in the sense of a coding error, impossible covariance construction, internally inconsistent result, or failed control that destroys the central mechanism.

There is, however, one interpretation condition that would become fatal if left ambiguous: the species-specific environmental variables must have a shared, ecologically fixed sign convention. If they are arbitrary latent axes that can each be reversed independently, “environmental correlation” and “response sign” are not separately identifiable. This is readily repaired by defining the variables as identically oriented exposures to the same physical quantity, or by reframing the theory directly in terms of demographic-shock covariance.

---

## 6. Major scientific issues

### Major issue 1 — The headline comparator confounds response sign with response magnitude

#### What the design currently does

The primary mixed-sign sequence is

\[
 b_i \in \operatorname{linspace}(-0.5,0.5,S),
\]

whereas the broad aligned sequence is

\[
 b_i \in \operatorname{linspace}(0.1,1.0,S).
\]

These treatments differ in at least four ways:

- coefficient signs;
- coefficient mean;
- coefficient root-mean-square magnitude;
- the strength of multiplicative-noise/Jensen effects.

For \(S=4\), for example,

\[
\operatorname{RMS}(b_{\mathrm{mixed}})=0.3727,
\qquad
\operatorname{RMS}(b_{\mathrm{positive}})=0.6442,
\]

so the broad positive treatment has about 73% greater marginal forcing scale. For \(S=8\), the corresponding RMS values are approximately 0.3273 and 0.6239, a roughly 91% difference. The reported contrast near 0.084 versus 0.263 in community CV therefore cannot be attributed to response-sign structure alone.

#### Why the paper nevertheless survives

The Supporting Information includes the correct control:

\[
 b_{\mathrm{positive\text{-}matched}}=|b_{\mathrm{mixed}}|.
\]

Under symmetric Gaussian exposure, \(b_i z_i\) and \(|b_i|z_i\) have the same marginal distribution for every species. The difference is in cross-species covariance. The supplied results show that the matched aligned treatment remains substantially more variable than the mixed-sign treatment—approximately 0.149 versus 0.085 for \(S=4\) and 0.120 versus 0.058 for \(S=8\) at the representative \(\rho=0.5\) setting. Those values should be checked against the final production table before insertion, but the qualitative and quantitative separation is unmistakable.

#### Required revision

- Make the positive magnitude-matched treatment the **primary comparator in the abstract, Results, Discussion, and main figures**.
- Move the present broad positive sequence to a sensitivity analysis explicitly labelled “greater aligned response amplitude.”
- Replace language such as “matched forcing” with either “magnitude-matched coefficients” or “parameter-matched forcing distributions.” The environmental realizations are not evidently paired across treatments.
- Ideally use common random numbers for the two sign treatments and report the distribution of paired within-realization differences. This is not needed for unbiased means, but it gives a cleaner causal contrast and tighter Monte Carlo precision.

#### Effect on the present claims

The central sign-reversal claim is **supported**. The current headline effect size is **inflated by a second treatment difference** and should not be used as the primary demonstration.

---

### Major issue 2 — The richness sequence is a compound assembly sequence, not an isolated richness manipulation

The sequence \(\operatorname{linspace}(-0.5,0.5,S)\) preserves the endpoints but not the distribution of response magnitudes. As \(S\) rises, more coefficients are inserted near zero and the mean squared response declines. Simultaneously, keeping \(K_i=100\) raises deterministic total equilibrium abundance.

For the symmetric deterministic model at \(z=0\),

\[
N_i^*=\frac{r_0K}{1+\alpha(S-1)},
\qquad
N_{\mathrm{tot}}^*=\frac{Sr_0K}{1+\alpha(S-1)}.
\]

With \(r_0=1\), \(K=100\), and \(\alpha=0.3\), the design changes as follows:

| \(S\) | RMS of mixed-sign \(b\) | \(N_{\mathrm{tot}}^*\) | contrast-mode eigenvalue \(\lambda_d\) |
|---:|---:|---:|---:|
| 2 | 0.5000 | 153.85 | 0.4615 |
| 3 | 0.4082 | 187.50 | 0.5625 |
| 4 | 0.3727 | 210.53 | 0.6316 |
| 5 | 0.3536 | 227.27 | 0.6818 |
| 6 | 0.3416 | 240.00 | 0.7200 |
| 7 | 0.3333 | 250.00 | 0.7500 |
| 8 | 0.3273 | 258.06 | 0.7742 |

Thus, from \(S=2\) to \(S=8\):

- the RMS environmental sensitivity falls by about 35%;
- deterministic total abundance rises by about 68%, increasing the denominator of community CV;
- the local persistence of contrast modes changes;
- odd-richness communities contain a completely insensitive \(b_i=0\) species; and
- species composition changes deterministically rather than being replicated from a common pool.

A decline in CV along this sequence is therefore not a clean estimate of a richness effect. The no-intercompetition control does not solve the problem: with \(\alpha=0\), total equilibrium is \(SK\), so its denominator change with richness is even more direct. That control establishes only that interspecific competition is not necessary for the observed sequence-level pattern.

#### Required minimum revision: choose one of two defensible paths

**Path A—retain the analysis but narrow the claim.** Call it a “prespecified deterministic assembly sequence” throughout. Report the changing RMS coefficient, equilibrium total, total mean, total variance, and CV. Do not infer that richness itself caused the decline.

**Path B—retain a causal richness claim by adding controls.** At minimum, rerun the richness grid with:

1. response vectors normalized to constant \(\sum_i b_i^2\) or constant RMS across \(S\);
2. \(K_i\) scaled so that deterministic total equilibrium is constant across \(S\); and
3. the two normalizations combined.

A still stronger design would draw replicated assemblages of each richness from a common response pool, with either nested additions or random subsets, and report the distribution across community composition. This separates richness from the particular species sequence.

#### Reporting needed regardless of path

Plot or tabulate \(E[N_{\mathrm{tot}}]\), \(\operatorname{SD}(N_{\mathrm{tot}})\), \(\operatorname{Var}(N_{\mathrm{tot}})\), and \(\operatorname{CV}(N_{\mathrm{tot}})\). A CV trend alone cannot reveal whether stabilization arises from covariance cancellation, a larger mean, a smaller forcing scale, or all three.

---

### Major issue 3 — The mechanism should be stated analytically, not left as a simulation pattern

Let \(a_i=w_i b_i\), where \(w_i\) is the first-order abundance or contribution weight of species \(i\). If the exposure vector has equal marginal variance \(\sigma_z^2\) and equicorrelation \(\rho\), then the instantaneous variance of aggregate environmental forcing is

\[
\operatorname{Var}\!\left(\sum_i a_i z_i\right)
=\sigma_z^2\left[(1-\rho)\sum_i a_i^2
+\rho\left(\sum_i a_i\right)^2\right].
\]

Differentiating with respect to \(\rho\) gives

\[
\frac{\partial \operatorname{Var}}{\partial \rho}
=\sigma_z^2\left[\left(\sum_i a_i\right)^2-\sum_i a_i^2\right].
\]

Therefore, increasing exposure correlation is stabilizing at first order only when

\[
\left(\sum_i a_i\right)^2 < \sum_i a_i^2.
\]

This is more precise than “mixed signs stabilize.” Mixed signs are neither necessary as a verbal category nor sufficient by themselves: what matters is enough **weighted cancellation**.

Define an alignment index

\[
A=\frac{(\mathbf 1^\top\mathbf a)^2}{S\,\mathbf a^\top\mathbf a},
\qquad 0\le A\le1.
\]

Then

\[
\operatorname{Var}(F)
=\sigma_z^2\|\mathbf a\|^2\left[(1-\rho)+\rho SA\right],
\]

and higher \(\rho\) is stabilizing exactly when \(A<1/S\). The perfectly balanced treatment has \(A=0\); an equal, aligned treatment has \(A=1\).

The same result has an eigenmode interpretation. An equicorrelation matrix has one common mode, proportional to \(\mathbf 1\), and \(S-1\) contrast modes. Increasing \(\rho\) puts more variance into the common mode and less into contrast modes. A balanced response vector is orthogonal to the common mode; an aligned vector projects strongly onto it.

#### Why this matters editorially

Without this derivation, a sceptical reviewer can characterize the paper as a numerical restatement of a covariance identity. With it, the paper becomes a general theory of when environmental covariance stabilizes or destabilizes aggregate abundance, and the nonlinear Ricker simulations test propagation beyond the first-order benchmark.

#### Required revision

- Put the covariance derivation in the main text, not only the SI.
- Use the abundance-weighted vector \(\mathbf a\), not unweighted signs, as the general quantity.
- Add a continuous alignment or imbalance gradient at fixed \(\|\mathbf a\|\), rather than relying only on two endpoints.
- Compare simulated community variability with the analytical forcing prediction and identify where density dependence, nonlinear means, floors, and temporal autocorrelation cause departures.
- For arbitrary environmental covariance \(\Sigma_z\), state the general form

  \[
  \operatorname{Var}(F)=\mathbf a^\top\Sigma_z\mathbf a.
  \]

  This immediately generalizes the result beyond equicorrelation.

---

### Major issue 4 — “Environmental synchrony” requires a shared orientation of the environmental axes

The model contains products \(b_i z_i\). If each \(z_i\) is an arbitrary species-specific latent environmental axis, one may transform

\[
z_i'=-z_i,\qquad b_i'=-b_i
\]

without changing the demographic forcing \(b_i z_i\). Yet that transformation reverses the signs of all correlations involving \(z_i\). Consequently, the separate labels “driver correlation” and “response sign” are coordinate-dependent unless the \(z_i\) variables share an externally fixed orientation.

#### Required clarification

The ecological interpretation is valid if, for example, \(z_i\) denotes a standardized temperature anomaly, moisture anomaly, or other identically oriented physical exposure measured for species \(i\) across sites, seasons, or microhabitats. It is not valid if each species has an independently defined latent “good-to-bad environment” axis.

State this condition explicitly in the model definition and Discussion. Prefer the phrase **cross-species correlation in commonly oriented environmental exposure** on first use. Thereafter, “exposure correlation” is a safer shorthand than generic “environmental synchrony.”

An invariant alternative is to frame the object of interest as the covariance of demographic shocks,

\[
\Sigma_u=D_b\Sigma_zD_b,
\]

where \(D_b=\operatorname{diag}(b_1,\ldots,b_S)\). The paper can then explain that positively correlated physical exposures yield negative demographic-shock covariance for species with opposite response signs.

---

### Major issue 5 — Equal abundance and perfect symmetry maximize cancellation

The main mixed-sign sequence satisfies \(\sum_i b_i=0\), and the symmetric model gives species equal deterministic abundance. In a real community, cancellation depends on

\[
\sum_i w_i b_i,
\]

not \(\sum_i b_i\), where \(w_i\) reflects abundance, biomass, contribution to the aggregate, and dynamical transfer. A rare species with a large negative coefficient will not offset a dominant species with a positive coefficient merely because the unweighted slopes sum to zero.

#### Required revision

At minimum:

- rewrite the general claim in terms of **abundance-weighted response balance**;
- add a sensitivity analysis with heterogeneous \(K_i\) or equilibrium abundances; and
- show the outcome across a gradient of weighted imbalance.

A useful compact experiment would retain the same coefficient norm while varying dominance, then plot community CV against the analytical alignment index \(A\). An optional stronger extension would use asymmetric competition matrices, but heterogeneous weights are more important than a large interaction-matrix exercise.

This issue also changes the empirical prediction. The paper should not ask merely whether a community contains positive and negative responders; it should ask whether the dominant contributors are balanced relative to the principal environmental modes.

---

### Major issue 6 — The persistence analysis changes persistence and stationary variance together

The environmental process is

\[
\mathbf z_t=\phi\mathbf z_{t-1}+\boldsymbol\varepsilon_t,
\qquad
\boldsymbol\varepsilon_t\sim\mathcal N(0,\sigma_\varepsilon^2 C_\rho).
\]

Holding \(\sigma_\varepsilon\) fixed gives

\[
\operatorname{Var}(z_i)=\frac{\sigma_\varepsilon^2}{1-\phi^2}.
\]

Thus, with \(\sigma_\varepsilon=0.5\):

| \(\phi\) | stationary variance multiplier | stationary SD |
|---:|---:|---:|
| 0.00 | 1.000 | 0.500 |
| 0.70 | 1.961 | 0.700 |
| 0.90 | 5.263 | 1.147 |
| 0.95 | 10.256 | 1.601 |

The \(\phi=0.95\) treatment therefore has more than three times the stationary environmental SD of \(\phi=0\), not merely greater persistence. The manuscript acknowledges this, and Figure 5 displays stationary variance, but the abstract and causal wording still need correction.

#### Required revision

Add a constant-stationary-variance treatment using

\[
\sigma_\varepsilon(\phi)=\sigma_{z,\mathrm{target}}\sqrt{1-\phi^2}.
\]

Then distinguish:

1. the effect of temporal persistence at fixed stationary variance; and
2. the compound effect of persistence plus rising stationary variance at fixed innovation variance.

If this control is not added, retitle the section and figure as a **fixed-innovation stress gradient** and remove claims that temporal persistence itself caused the result.

#### Finite-series concern

With 300 retained time steps and \(\phi=0.95\), the raw environmental series has a rough AR(1) effective sample size of only

\[
300\frac{1-0.95}{1+0.95}\approx7.7.
\]

Replicating many short series estimates the mean of a finite-window CV estimator precisely; it does not remove the estimator's short-series bias or instability. The supplied diagnostics also show appreciable floor contact in this regime. Use much longer retained series for \(\phi\ge0.9\), report trajectory-length sensitivity, or confine \(\phi=0.95\) to a clearly marked stress appendix.

---

### Major issue 7 — The fixed value \(r_0=1\) is dynamically special

At the symmetric deterministic equilibrium, the Jacobian's common-mode eigenvalue is

\[
\lambda_c=1-r_0.
\]

With \(r_0=1\), \(\lambda_c=0\): common-mode abundance perturbations are locally eliminated in one deterministic step. The contrast-mode eigenvalue is

\[
\lambda_d
=1-r_0\frac{1-\alpha}{1+\alpha(S-1)}.
\]

Thus the chosen growth rate is not a generic middle value; it makes the aggregate/common mode locally superstable. Because the paper is specifically about transmission of a common environmental mode into total abundance, this deserves direct sensitivity analysis.

#### Required revision

Run the clean magnitude-matched comparison over a modest range of deterministically stable \(r_0\), for example \(0.25,0.5,1.0,1.5\), and report when the sign effect is retained. A limited check under a compensatory density-dependence form such as Beverton–Holt would further show that the result is not peculiar to Ricker overcompensation, but the \(r_0\) gradient is the essential first step.

Do not allow this sensitivity exercise to expand into an indiscriminate parameter sweep. The purpose is to show that the central covariance criterion survives ordinary changes in dynamical memory.

---

## 7. Moderate scientific and analytical issues

### 7.1 The broad stress extension should not visually dominate the main result

The high-variance extension is useful for locating numerical and biological limits, but floor occupancy is no longer negligible. The package reports approximately 11.6% mean floor occupancy in the stress extension, with maxima around 19.4% in some replicate summaries; even the extreme edge of the core grid shows some floor contact. These are not ordinary stationary fluctuations around a positive equilibrium.

Move the most severe forcing levels to the SI or visually separate them from the inferential core. State a prespecified diagnostic threshold beyond which results are labelled floor-affected rather than “robust.”

### 7.2 The floor is numerical, not ecological extinction

Abundances at \(10^{-9}\) can subsequently rebound, so the floor is neither an absorbing extinction state nor a demographic rescue model. Avoid ecological language implying extinction or persistence of populations unless an absorbing boundary is added. Report floor occupancy as a numerical-regime diagnostic.

### 7.3 Loreau–de Mazancourt synchrony is partly algebraically coupled to community CV

Community CV and the Loreau–de Mazancourt synchrony metric share total-community variance in their construction. A strong association is therefore not independent mechanistic validation. The regression in Figure 4/Table S5 is descriptive and should be labelled as such. The near-zero incremental contribution of pairwise log-growth correlation also suggests that the panel is not carrying much explanatory information.

My preference is to move the current Figure 4 to the SI and replace it with either:

- the analytical forcing benchmark versus nonlinear simulation;
- a continuous response-balance gradient; or
- the controlled richness decomposition.

### 7.4 Clipping the synchrony metric needs a numerical-tolerance audit

Clipping the Loreau–de Mazancourt metric to \([0,1]\) is reasonable only for tiny floating-point overshoots. Preserve the raw value, assert that any excursion is within a declared tolerance, and report the maximum excursion. Do not silently clip structurally out-of-range values.

### 7.5 Log-growth calculation should be aligned with the abundance floor

If abundances are already bounded below by `floor`, computing `log(N + floor)` changes values near the boundary and creates a second, implicit offset. Prefer `log(N)` after the floor has been applied, or explain why the second offset is intentional. This is minor in the core regime but can matter in stress cases.

### 7.6 Monte Carlo uncertainty is not structural uncertainty

The very narrow uncertainty bands reflect many replicate simulations under a fixed model. They quantify Monte Carlo precision and the distribution of finite simulated trajectories, not uncertainty about model form, parameter relevance, community composition, or empirical effect size. Use “Monte Carlo interval” or “replicate quantile interval” precisely and state which one is plotted.

### 7.7 Clarify whether intervals describe replicate outcomes or means

A 95% interval across replicate-level CV values and a 95% confidence interval for the scenario mean answer different questions. Captions and methods should give the formula. For a theoretical paper, effect sizes and replicate distributions are usually more informative than significance-style intervals.

### 7.8 Equicorrelation is a useful special case, not a generic covariance architecture

The equicorrelated matrix makes the common/contrast decomposition transparent, but natural environmental covariance is heterogeneous. Once the main analytical result is written as \(\mathbf a^\top\Sigma_z\mathbf a\), add one small robustness example using a block, distance-decay, or empirical-like positive-definite covariance matrix. This can remain in the SI.

### 7.9 Competition sensitivity is too coarse

Comparing \(\alpha=0\) with \(\alpha=0.3\) shows that interspecific competition is not logically required. It does not establish insensitivity to competition strength. A short \(\alpha\) gradient would be more informative, especially because \(\alpha\) changes equilibrium abundance and contrast-mode memory.

### 7.10 The model tests aggregate abundance, not ecosystem functioning generally

Avoid moving without qualification from total abundance CV to “ecosystem stability,” “function,” or “ecosystem insurance.” The result may generalize to additive functions, but function-specific weights would enter \(a_i=w_i b_i\). State this rather than treating abundance and function as interchangeable.

### 7.11 The Gaussian linear-response model has no optimum or response curvature

A signed linear coefficient is the cleanest local model, but unbounded Gaussian forcing eventually generates unrealistically large favourable and adverse effects. Note that \(b_i\) should be interpreted as a local slope around an environmental reference state. A brief nonlinear-response sensitivity would be valuable but is secondary to the matched-sign and weighted-balance analyses.

### 7.12 Common random numbers would improve comparison efficiency

The deterministic seed architecture is excellent. For direct treatment contrasts, reuse the same innovation arrays across response-sign treatments. Report paired differences and their distribution. This will make the magnitude-matched result almost impossible to misread as Monte Carlo variation.

---

## 8. Claim-by-claim audit

| Claim or implied claim | Current status | Safe interpretation | Needed action |
|---|---|---|---|
| Mixed-sign responses reverse the effect of positive exposure correlation on aggregate CV | **Supported** | Strong in the symmetric model and retained under magnitude matching | Promote matched control; derive weighted criterion |
| The large 0.084-versus-0.263 contrast is caused by response sign | **Not isolated** | It combines sign, mean, RMS magnitude, and stochastic-mean effects | Demote broad positive treatment; do not headline this contrast |
| The mechanism is response diversity | **Partly supported, imprecisely named** | It is specifically abundance-weighted orientation/balance relative to environmental covariance modes | Define an alignment/balance index |
| Mixed signs are sufficient for stabilization as \(\rho\) rises | **False in general** | Stabilization requires \((\sum a_i)^2<\sum a_i^2\) | Replace binary verbal rule with the formal condition |
| Richness reduces community variability | **Not causally isolated** | CV declines along the chosen compound assembly sequence | Add RMS/total-abundance controls or narrow wording |
| The richness pattern persists without interspecific competition | **Supported descriptively** | Intercompetition is not necessary for that sequence-level pattern | Do not present as proof of a pure portfolio effect |
| Environmental persistence amplifies or modifies the mechanism | **Confounded** | Fixed innovation variance changes persistence and stationary variance together | Add constant-stationary-variance control |
| Realized growth synchrony mediates the effect | **Plausible and descriptively supported** | Signed coefficients transform exposure covariance into demographic-shock covariance | Avoid causal mediation language unless formally decomposed |
| Loreau–de Mazancourt synchrony independently validates the mechanism | **Weak** | Association is partly mathematical because the metrics share variance terms | Move regression to SI or describe as consistency check |
| Results are robust to severe environmental variability | **Only within diagnostic limits** | Strong forcing reaches a floor-affected regime | Mark stress cases; define exclusion/interpretation threshold |
| Results generalize to real communities | **Promising, not yet demonstrated** | Generality depends on shared exposure orientation and abundance-weighted balance | Add heterogeneous weights and clearer empirical scope |
| The mechanism is independent of model structure | **Not shown** | Demonstrated for one Ricker parameterization, with a no-competition control | Add \(r_0\) sensitivity; optional second density-dependence form |

---

## 9. Recommended analytical revision package

### Essential package for a defensible submission

1. **Promote the positive magnitude-matched comparator** to the primary analysis and main text.
2. **Add the analytical covariance/eigenmode derivation** and define an abundance-weighted alignment index.
3. **Run a continuous balance/imbalance gradient** at fixed response norm.
4. **Either control the richness analysis or relabel it as an assembly sequence.** The stronger option is constant RMS plus constant deterministic total abundance.
5. **Add a constant-stationary-variance autocorrelation control** and lengthen the high-\(\phi\) trajectories.
6. **Add a compact \(r_0\) sensitivity** and at least one unequal-abundance sensitivity.
7. **Rewrite the ecological interpretation** so that exposure variables have a shared physical orientation.
8. **Rebuild the figure hierarchy** around the clean mechanism and place stress/descriptive regressions in the SI.
9. **Add an anonymized data/code availability statement** with a review link and a public-release plan.

### Stronger, optional extensions

- one non-equicorrelated covariance example;
- an \(\alpha\) gradient rather than only \(0\) and \(0.3\);
- a compensatory density-dependence sensitivity;
- replicated communities sampled from a common species pool;
- paired common-random-number treatment contrasts;
- a local nonlinear response curve or saturating environmental effect.

These extensions would improve generality, but they should not obscure the paper's clean theoretical message.

---

## 10. Recommended main-text architecture

### Proposed conceptual sequence

1. **Problem:** environmental correlation alone does not determine aggregate stability.
2. **Theory:** derive \(\mathbf a^\top\Sigma_z\mathbf a\) and the equicorrelation balance criterion.
3. **Nonlinear test:** compare balanced mixed-sign and positive magnitude-matched treatments.
4. **Mechanistic diagnostic:** show imposed exposure correlation versus realized demographic-growth correlation.
5. **Boundary tests:** continuous imbalance and unequal abundance.
6. **Conditional extensions:** controlled richness and persistence, clearly distinguished from the core mechanism.
7. **Implications:** empirical measurement of exposure covariance, response slopes, and contribution weights.

### Proposed display-item allocation

The journal permits up to six main display items, and the manuscript currently uses all six. I recommend:

- **Table 1:** model quantities and parameterization, revised to distinguish innovation and stationary variance;
- **Figure 1:** conceptual/eigenmode schematic plus analytical variance prediction;
- **Figure 2:** nonlinear simulations using mixed versus positive magnitude-matched responses;
- **Figure 3:** imposed exposure correlation versus realized log-growth correlation;
- **Figure 4:** continuous weighted-balance gradient and/or unequal-abundance test;
- **Figure 5:** controlled richness decomposition or constant-stationary-variance persistence test.

Move the present wide-amplitude surface, severe stress extension, and synchrony regression to the SI. Promote current Figure S3 or its underlying data into the main text.

---

## 11. Figure-by-figure review

### Current Figure 1

**Strength:** It communicates that response structure interacts with exposure correlation and variability.

**Problems:** The main surface emphasizes the broad aligned treatment; the comparison is not magnitude-matched. The stress range visually dominates the core range, and averaging across \(\rho\) in another panel obscures the interaction that is the paper's subject.

**Revision:** Replace or redesign around the magnitude-matched contrast. Show analytic first-order predictions as thin lines and nonlinear simulation summaries as points/ribbons. Move high-\(\sigma\) stress levels to the SI.

### Current Figure 2

**Strength:** The monotone sequence is visually clear.

**Problem:** It invites a causal richness interpretation although coefficient RMS, total equilibrium abundance, community composition, and local dynamical modes all change with \(S\).

**Revision:** Either relabel it “assembly sequence” and add panels for mean, SD, and CV, or replace it with a four-design control: original, fixed RMS, fixed total equilibrium, and both fixed.

### Current Figure 3

**Strength:** This is one of the best figures. It clearly separates imposed exposure correlation from realized demographic synchrony.

**Revision:** Retain in the main text. State exactly whether the plotted realized metric is the replicate mean of pairwise correlations, a pooled correlation, or a scenario summary. Mark floor-affected stress cases separately.

### Current Figure 4

**Strength:** It summarizes relationships among metrics.

**Problems:** The Loreau–de Mazancourt metric shares variance terms with the response; the regression is descriptive; pairwise growth correlation contributes little additional explanatory information; and the panel does not establish mediation.

**Revision:** Move to the SI. Replace with the analytic-versus-simulated benchmark or the response-balance gradient.

### Current Figure 5

**Strength:** It transparently displays the growth of stationary variance with \(\phi\).

**Problem:** The headline can still be read as a persistence effect, although the treatment is compound and the \(\phi=0.95\) series is short in effective information and floor-affected.

**Revision:** Add a fixed-stationary-variance series, lengthen high-\(\phi\) trajectories, and present both parameterizations side by side. Otherwise move the panel to a stress appendix and narrow all causal wording.

### Current Figure S3

**Assessment:** This is the cleanest direct evidence for the paper's central causal claim.

**Revision:** Promote it to the main paper. The current evidential hierarchy is backwards: the least-confounded comparison should not be supplementary.

### Other SI displays

Keep diagnostic plots, no-competition results, numerical stress tests, and extended parameter grids in the SI, but make the main captions explicitly direct readers to the relevant diagnostic table. Each SI caption should identify the exact departure from the core design and state whether floors/clipping were encountered.

---

## 12. Table and caption edits

### Table 1

Revise parameter naming as follows:

- replace generic “environmental SD” with **innovation SD** \(\sigma_\varepsilon\);
- add stationary SD \(\sigma_z=\sigma_\varepsilon/\sqrt{1-\phi^2}\);
- define \(\rho\) as the pairwise correlation of identically oriented innovations/exposures;
- report the requested and effective \(\rho\) if values at 1 are numerically clipped;
- list the mean and RMS of each response-coefficient treatment;
- state that \(r_0=1\) gives \(\lambda_c=0\) at the symmetric equilibrium;
- distinguish core, sensitivity, and stress parameter ranges.

### Caption requirements

Every main and SI caption should be standalone and include:

- number of replicate trajectories;
- total, burn-in, and retained lengths;
- whether intervals are replicate quantiles or uncertainty intervals for a mean;
- parameters varied and held fixed;
- whether \(\sigma\) is innovation or stationary SD;
- exact response treatment, including whether magnitudes are matched;
- diagnostic status of floor-affected cases; and
- a definition of every abbreviation used in the panel.

Avoid captions that make causal claims stronger than the design. In particular, use “along the assembly sequence” rather than “with increasing richness” unless the controlled analysis is supplied.

---

## 13. Detailed line-edit of the main manuscript

Line numbers below refer to the supplied anonymous `main_text.md`. Because the scientific hierarchy should change, some edits are replacements rather than cosmetic copy-edits.

### Title and abstract

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 1 | The present title should identify the conditional reversal, not imply a generic insurance effect. | Prefer **“Response-sign balance determines whether correlated environments stabilize aggregate abundance”** or **“When correlated environmental exposure stabilizes communities: the role of response balance.”** |
| 5, sentence 1 | The opening treats environmental synchrony as though it normally maps directly to population synchrony. | Replace with: “Positive correlation among environmental exposures is often expected to synchronize populations and destabilize aggregate abundance, but that expectation assumes similarly oriented demographic responses.” |
| 5, model sentence | The environmental variables need a common sign convention. | Add “identically oriented” or a concrete example: “We simulated species-specific exposures to the same physically oriented environmental variable...” |
| 5, treatment description | “Heterogeneous” is too broad; the clean contrast is sign orientation at matched magnitudes. | Use “balanced mixed-sign responses” and “magnitude-matched aligned responses.” |
| 5, headline numbers | The broad positive treatment inflates the causal contrast. | Replace its numbers with the positive-matched result; retain the wide positive result only as a sensitivity sentence if space permits. |
| 5, richness sentence | The present wording implies a controlled richness effect. | Either delete from the abstract or write: “CV also declined along a prespecified assembly sequence, although that sequence changed response RMS and total equilibrium abundance with richness.” A stronger abstract may report the controlled rerun instead. |
| 5, persistence sentence | Temporal persistence and stationary variance are conflated. | Report only the constant-stationary-variance result after adding it; otherwise say “At fixed innovation variance, increasing autocorrelation produced a compound increase in persistence and stationary exposure variance.” |
| 5, final sentence | The conclusion is broader than the demonstrated condition. | End with: “Environmental correlation therefore predicts aggregate stability only when interpreted jointly with the abundance-weighted orientation of species' responses.” |

### Introduction

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 13–15 | The opening should begin with the variance identity for an aggregate rather than a broad claim about ecosystem stability. | Open: “Temporal variability of an aggregate depends on the variances of its components and their covariances. For community abundance, covariance can dominate the effect of individual population variability.” |
| 15 | “Stability” is used before the response variable is fixed. | Define at first use: “Here, stability means low temporal coefficient of variation in total community abundance.” |
| 17 | Driver synchrony and population synchrony are too easily conflated. | Add a two-sentence distinction between correlation of exposure series and correlation of demographic growth responses. |
| 17–19 | The conventional expectation is stated too categorically. | Use “often” or “under similarly signed responses,” and cite the relevant covariance/portfolio literature already in the bibliography. |
| 19 | “Response diversity” needs an operational definition. | Define it as variation in the slopes and signs of demographic responses to a commonly oriented exposure. State that this paper isolates response orientation. |
| 21 | Any claim that the sign interaction is “overlooked” or “unexplored” is vulnerable. | Soften to “has not been made explicit in this covariance form” unless a systematic literature search supports priority. Engage directly with Ives et al. (1999) and the existing response-diversity literature. |
| 21–23 | The gap is currently verbal. | Insert the general question: when does increasing off-diagonal environmental covariance raise versus lower \(\mathbf a^\top\Sigma_z\mathbf a\)? |
| 23 | The hypothesis should be quantitative. | State: “We predicted that increasing \(\rho\) would reduce aggregate forcing when \((\sum_i a_i)^2<\sum_i a_i^2\), but increase it when the inequality is reversed.” |
| 25 | The novelty risks sounding like the binary sign contrast itself. | Present novelty as testing the first-order covariance criterion in a nonlinear density-regulated system and mapping its breakdown. |
| 27 | Predictions mix clean and confounded analyses. | Separate **primary prediction** (matched sign orientation), **boundary prediction** (weighted imbalance), and **extensions** (assembly and temporal autocorrelation). |
| 29–31 | The paragraph previews richness and persistence as equivalent evidence. | Reorder so that matched-sign and realized-synchrony analyses come first; describe richness/persistence as conditional extensions. |

### Model and environmental process

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 35–39 | Model prose is clear but the aggregation target and census timing should be explicit. | State that \(N_{i,t}\) is abundance immediately before the annual update and that the response is the temporal CV of \(\sum_iN_{i,t}\). |
| 39, equation | Notation should distinguish innovation from state variance. | Write \(\boldsymbol\varepsilon_t\sim\mathcal N(0,\sigma_\varepsilon^2C_\rho)\), reserving \(\sigma_z\) for stationary exposure SD. |
| 41–43 | The AR(1) process needs its stationary covariance in the main methods. | Add \(\operatorname{Cov}(\mathbf z_t)=\sigma_\varepsilon^2C_\rho/(1-\phi^2)\). |
| 43 | Equicorrelation feasibility/clipping is implementation detail but should not be hidden. | State the positive-definite range and the small numerical offset used at \(\rho=1\). Report plotted labels as requested values and analysis values as effective values. |
| 45 | “Environmental correlation” is potentially coordinate-dependent. | Define \(z_i\) as an identically oriented physical exposure. Add a sentence that arbitrary species-specific latent axes would not permit separate interpretation of \(b_i\) and \(\rho\). |
| 45–47 | The response treatments are not equally scaled. | Give mean, RMS, and \(\sum b_i\) for each treatment. Identify `positive_matched` as the primary causal comparator and the broad positive range as an amplitude sensitivity. |
| 47 | Zero unweighted mean is presented as the relevant balance property. | Add: “In the symmetric baseline, equal equilibrium weights make \(\sum_i b_i=0\) equivalent to weighted balance; in heterogeneous communities the relevant condition is \(\sum_iw_ib_i\approx0\).” |
| 49 | The deterministic equilibrium is useful and currently underused. | Derive \(N_i^*=r_0K/[1+\alpha(S-1)]\) and report how total equilibrium changes across the richness sequence. |
| 51 | The choice \(r_0=1\) is not justified dynamically. | Explain that it gives \(\lambda_c=0\), then flag the planned \(r_0\) sensitivity. Do not call it merely a “standard” value. |
| 51–53 | Competition notation should distinguish intra- and interspecific coefficients. | Use \(\alpha_{ii}=1\) and \(\alpha_{ij}=\alpha\) or define the scalar convention once and consistently. |
| 53 | Initial abundance and burn-in are reported, but stationarity evidence is elsewhere. | Add a concise reference to convergence diagnostics and trajectory-length checks in the SI. |
| 55–57 | Floors and exponent clipping are described as safeguards without interpretation boundaries. | State that the floor is nonabsorbing, specify diagnostic summaries, and define stress cases with material floor occupancy as numerical boundary tests. |

### Simulation design and metrics

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 60–64 | Core, sensitivity, and stress grids are blended. | Divide into three labelled design tiers. The inferential core should exclude floor-affected extremes. |
| 64 | “Matched” may imply paired innovations. | State whether innovations are paired across treatments. If not, write “matched in parameter distribution” and consider rerunning with common random numbers. |
| 64–68 | Replication is excellent but the estimand is not explicit. | Define whether the scenario summary is mean replicate CV, median replicate CV, or CV calculated after pooling. |
| 68–72 | The community CV equation should make temporal averaging explicit. | Use \(\operatorname{CV}_T=\operatorname{SD}_t(N_{\mathrm{tot},t})/\operatorname{E}_t(N_{\mathrm{tot},t})\). |
| 72–76 | Species-level CV aggregation may be ambiguous. | State whether species CVs are averaged equally, abundance-weighted, or summarized another way. |
| 76–80 | The Loreau–de Mazancourt metric is clipped. | Define the raw estimator, numerical tolerance, and the exact clipping rule. Report maximum raw overshoot. |
| 80–84 | Log-growth correlation near the floor is sensitive to implementation. | Use \(\log N_{i,t+1}-\log N_{i,t}\) after flooring, or explain the additive offset. State how constant/near-constant series are handled. |
| 84–88 | Interval terminology is underspecified. | Give the exact interval: replicate 2.5–97.5% quantiles, percentile bootstrap of a mean, or \(\bar x\pm1.96\,SE\). |
| 88–92 | Regression language can imply inferential modelling. | Call the Figure 4 regression a descriptive cross-scenario association; do not interpret coefficients as independent mechanistic effects. |
| 92–96 | The magnitude-matched control appears as secondary. | Move it into the primary design subsection. |
| 96 | Richness is described as the manipulated factor. | Replace with “deterministic assembly sequence indexed by \(S\)” unless controlled reruns are added. |
| 96–99 | Temporal persistence is described without the variance consequence. | State in Methods, not only Discussion, that fixed \(\sigma_\varepsilon\) makes stationary variance depend on \(\phi\). |
| 99 | Reproducibility language is good but lacks journal-facing availability. | Add an anonymized archive link and identify the exact command that regenerates all tables and figures from a clean environment. |

### Results

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 103–107 | The Results should lead with the cleanest test. | Begin with the positive magnitude-matched comparison, not the wide positive treatment. |
| 107–111 | The current numerical headline combines sign and amplitude. | Use: “When response magnitudes were identical, changing only coefficient signs reversed the effect of exposure correlation...” Then report the matched values. |
| 111 | The broad aligned result remains useful. | Add one subordinate sentence: “Expanding the aligned coefficient range increased the contrast, as expected from its greater RMS sensitivity.” |
| 113–117 | The mechanism is described qualitatively. | Insert the first-order variance expression and state whether the nonlinear outcome follows its predicted sign across the core grid. |
| 117–121 | Any use of “always,” “regardless,” or “universally” is too strong. | Restrict claims to the examined stable, low-floor parameter domain. |
| 121–125 | Stress cases are folded into robustness. | Separate core results from floor-affected stress behaviour and report diagnostic occupancy alongside the effect. |
| 129–135 | “Increasing richness reduced CV” overstates causal identification. | Replace with: “Community CV declined monotonically along the prespecified assembly sequence from \(S=2\) to \(S=8\). Over the same sequence, response RMS declined and deterministic total abundance rose...” |
| 135–139 | The no-competition result is overinterpreted. | Write: “The sequence-level decline did not require interspecific competition,” not “confirming a portfolio effect” or equivalent. |
| 141–147 | Realized growth correlations are a strong mechanistic result. | Lead with the sign transformation: positive exposure correlations became negative demographic-growth correlations for opposite-sign pairs. |
| 147–153 | Figure 4 association risks circular interpretation. | Call it a metric-consistency analysis and move detailed regression statistics to the SI. |
| 153–159 | Loreau–de Mazancourt synchrony may be described as explanatory. | Replace “explained” with “was associated with,” noting the shared variance construction. |
| 159–165 | Severe environmental variation should not be called robust without qualification. | Report floor occupancy and say “the qualitative ordering persisted into a floor-affected stress regime.” |
| 165–171 | The autocorrelation result is phrased causally. | Start: “At fixed innovation SD, increasing \(\phi\) simultaneously increased temporal persistence and stationary exposure variance...” |
| 171–177 | The stationary-variance panel should be integrated into the prose. | Quantify the SD multiplier at \(\phi=0.95\) and avoid attributing the full CV change to persistence. |
| 177–183 | Short effective series and floor contact need a result-level warning. | Label \(\phi=0.95\) a stress endpoint unless longer-series results confirm it. |
| 183–185 | The Results summary bundles claims of unequal strength. | End with the matched-sign mechanism only; reserve richness and persistence qualifications for separate sentences. |

### Discussion

| Lines | Editorial diagnosis | Recommended edit |
|---:|---|---|
| 189–193 | The opening currently risks overstating a broad reversal of conventional wisdom. | Open with the conditional result: “The effect of correlated environmental exposure on aggregate stability changed sign with abundance-weighted response balance.” |
| 193–198 | The strongest causal evidence is not foregrounded. | State immediately that the reversal persisted when response magnitudes were identical. |
| 198–204 | Mechanism is verbal where a compact equation would be clearer. | Use the common/contrast eigenmode interpretation and the alignment index \(A\). |
| 204–210 | “Mixed signs” is treated as the operative condition. | Replace with the weighted inequality; explain that weakly mixed but strongly imbalanced responses can still be destabilized by higher \(\rho\). |
| 210–216 | The role of equal abundance is understated. | Add a paragraph on contribution weights and dominance. Make this a prediction, not merely a limitation. |
| 216–222 | Ecological examples may combine incomparable environmental axes. | Restrict examples to shared physical variables with a fixed orientation: temperature, rainfall, flow, salinity, or a consistently defined resource anomaly. |
| 222–228 | The coordinate-identifiability issue is absent. | Add the sign-flip argument in concise prose and state the invariant demographic-shock covariance formulation. |
| 228–234 | Richness language is too strong relative to the design. | Either discuss the new controlled analysis or call the existing result a property of one assembly rule. |
| 234–239 | Competition result may be used to infer general independence. | Say only that the mechanism does not require interspecific competition in this model; density feedback still controls propagation. |
| 245–251 | Limitations are candid but the slope-sequence caveat is buried. | Elevate it to the first limitation and connect it directly to the richness claim in the abstract/results. |
| 251–257 | Symmetry/equal abundance should be more prominent. | State that perfect cancellation is a best-case boundary and that weighted imbalance is expected in nature. |
| 257–263 | Fixed \(r_0\) is not discussed as a special dynamic choice. | Add the \(\lambda_c=1-r_0\) observation and summarize the sensitivity result. |
| 263–269 | Gaussian/linear response caveat is generic. | Explain that coefficients are local response slopes and that curvature can make response sign state-dependent. |
| 269–275 | Floor effects are described as technical only. | State that stress-regime conclusions are conditional once floor occupancy is material. |
| 275–281 | Persistence caveat arrives too late. | Move the fixed-innovation qualification into Methods and Results; here discuss what the fixed-stationary-variance control shows. |
| 281–287 | Empirical implications are too qualitative. | Specify the needed data: species contribution weights, exposure covariance on a common scale, response slopes, and population growth/abundance time series. |
| 287–293 | Generalization to ecosystem functions needs weighting. | State that for an additive function, function-specific contribution weights replace abundance weights in \(a_i=w_i b_i\). |
| 293–297 | The final paragraph should not end on generic “diversity is stabilizing” language. | Use the replacement conclusion below. |
| 301 | The AI declaration is too generic if it does not identify tools and uses. | Name each tool/model and describe its role—e.g. language editing, code assistance, or test generation—without implying that scientific responsibility was delegated. Ensure the same information is entered in the submission system. |

---

## 14. Replacement-ready text

### 14.1 Preferred revised title

> **Response-sign balance determines whether correlated environments stabilize aggregate abundance**

Alternative with a more conceptual tone:

> **When correlated environmental exposure becomes ecological insurance**

The first is safer and more informative for indexing.

### 14.2 Recommended abstract after the essential analyses are completed

> Positive correlation among environmental exposures is often expected to synchronize populations and destabilize aggregate abundance, but that expectation assumes similarly oriented demographic responses. We combined a first-order covariance analysis with a stochastic multispecies Ricker model to determine how correlation among identically oriented environmental exposures interacts with species' response coefficients. For an abundance-weighted response vector \(\mathbf a\) under equicorrelated exposure, aggregate forcing variance is proportional to \((1-\rho)\sum_i a_i^2+\rho(\sum_i a_i)^2\). Increasing exposure correlation is therefore stabilizing only when weighted response cancellation makes \((\sum_i a_i)^2<\sum_i a_i^2\). Nonlinear simulations supported this prediction. When coefficient magnitudes were held identical, increasing \(\rho\) lowered the temporal coefficient of variation of total abundance for balanced mixed-sign responses but raised it for aligned responses. The reversal weakened predictably as abundance weighting or response imbalance increased, demonstrating that mixed signs alone are insufficient. [Controlled richness result, if retained.] At fixed stationary environmental variance, [insert revised autocorrelation result], whereas fixed innovation variance produced the expected compound effect of persistence and rising stationary variance. The qualitative mechanism persisted across ordinary density-feedback settings but severe forcing produced floor-affected trajectories that marked its numerical boundary. Environmental correlation alone is therefore not a sufficient predictor of community stability: the decisive quantity is the projection of abundance-weighted demographic responses onto dominant environmental covariance modes. This framework clarifies when response diversity converts common environmental variation into aggregate insurance and identifies the measurements required for empirical tests.

The bracketed clauses should be completed only after the relevant controls. This version is approximately 250 words before those insertions and remains within the journal's 300-word limit.

### 14.3 Minimal-change abstract if no new richness or persistence controls are added

> Positive correlation among environmental exposures is often expected to synchronize populations and destabilize aggregate abundance, but that expectation assumes similarly oriented demographic responses. We used a stochastic multispecies Ricker model to examine how correlation among identically oriented species exposures interacts with response-sign structure. Increasing exposure correlation reduced the temporal coefficient of variation of total abundance when responses were balanced around zero, but increased it when responses were aligned. Crucially, this reversal persisted when response-coefficient magnitudes were identical between treatments, showing that it arose from cross-species covariance rather than unequal marginal forcing. The mechanism follows from a first-order covariance result: for effective response weights \(a_i\), aggregate forcing variance is proportional to \((1-\rho)\sum_i a_i^2+\rho(\sum_i a_i)^2\). Correlation is therefore stabilizing only when abundance-weighted responses cancel sufficiently. Community CV also declined along a prespecified assembly sequence, but this sequence simultaneously reduced response RMS and increased total equilibrium abundance and is not interpreted as an isolated richness effect. Likewise, increasing environmental autocorrelation at fixed innovation variance also increased stationary exposure variance and represents a compound stress treatment. The core sign-dependent reversal persisted across the low-floor parameter domain, whereas severe forcing identified numerical and biological limits. Raw environmental correlation is therefore insufficient to predict aggregate stability; it must be interpreted jointly with the orientation and contribution weighting of species' demographic responses.

This is scientifically safe with the current evidence, but the preferred route is to add the controls and retain a stronger abstract.

### 14.4 Recommended opening paragraph of the Introduction

> Temporal variability of an ecological aggregate depends on both the variability of its components and the covariance among them. For total community abundance, asynchronous population fluctuations can reduce aggregate variance even when individual populations remain variable, whereas synchronous fluctuations transmit population-level variability to the community total. Positive correlation among environmental exposures is therefore commonly expected to be destabilizing. That inference is incomplete, however, because environmental covariance acts through species-specific demographic responses. If species respond in opposite directions to the same physically oriented environmental anomaly, positively correlated exposure can generate compensatory demographic forcing rather than synchronous population growth.

### 14.5 Recommended hypothesis paragraph

> Let \(a_i=w_i b_i\) denote the product of species \(i\)'s contribution weight and its local demographic response coefficient. Under equal-variance, equicorrelated exposure, the first-order variance of aggregate environmental forcing is \(\sigma_z^2[(1-\rho)\sum_i a_i^2+\rho(\sum_i a_i)^2]\). We therefore predicted that increasing exposure correlation would stabilize aggregate abundance when \((\sum_i a_i)^2<\sum_i a_i^2\), but destabilize it when the inequality was reversed. We tested whether this covariance prediction survived nonlinear density regulation, temporal autocorrelation, unequal response balance, and changes in community assembly.

### 14.6 Recommended opening of the Discussion

> The stability consequence of correlated environmental exposure changed sign with abundance-weighted response balance. When response magnitudes were identical but signs were balanced, higher exposure correlation reduced variability in total abundance; when the same magnitudes were aligned, higher correlation increased aggregate variability. In covariance terms, positive correlation concentrates environmental variation in a common mode. Balanced response vectors are nearly orthogonal to that mode, whereas aligned vectors project strongly onto it. The nonlinear community model preserved this first-order prediction across the core parameter domain, while density feedback, response imbalance, and severe forcing determined its quantitative limits.

### 14.7 Recommended conclusion

> Environmental correlation alone cannot predict aggregate stability. What matters is the covariance of demographic forcing, equivalently the projection of an abundance- or function-weighted response vector onto the dominant modes of environmental variation. Balanced responses can convert a common environmental signal into compensatory population change, whereas aligned responses transmit that signal to the community total. This condition is narrower than the claim that mixed signs are universally stabilizing, but more general than the particular Ricker simulations studied here. It provides a direct empirical programme: measure commonly oriented exposures, estimate species' response slopes and contribution weights, and evaluate whether the resulting response vector aligns with or avoids dominant environmental covariance modes.

### 14.8 Recommended AI-use statement template

Do not fill this with generic language. Insert the actual tools and uses:

> Generative-AI tools were used for [language editing / code assistance / test generation / other specified task]. The tools and models were [exact names and versions, where available]. All model choices, analyses, source verification, interpretation, and final wording were checked and approved by the authors, who take full responsibility for the work. The same information was disclosed through the journal's submission system.

---

## 15. Reproducibility and code review

### What is already strong

- deterministic scenario construction and seeds;
- a clean Python package rather than a notebook-only workflow;
- a locked environment specification;
- explicit production specifications;
- unit and workflow tests;
- source-fidelity and figure-link checks;
- parameter and diagnostic outputs separated from display products;
- floor and clipping diagnostics;
- a complete anonymous reviewer bundle.

### Changes needed for publication

1. Add a manuscript section titled **Data and code availability**.
2. Deposit the exact accepted code, configuration, derived data, and figure-building inputs in a persistent public archive with a DOI. During double-anonymous review, use an anonymized private review link.
3. State the one-command rebuild procedure and expected outputs.
4. Record the Python version and the lockfile's package versions in the archive metadata.
5. Include a machine-readable citation file after de-anonymization.
6. Make clear which files are source data, generated intermediates, and final products.
7. Preserve the production archive checksum in the release notes.
8. Ensure no absolute user paths, Git metadata, author names, or repository remotes enter the anonymous archive.
9. Add tests for the analytical criterion and for the positive-matched treatment, not only numerical workflow completion.
10. Add assertions around raw synchrony bounds and report floor/clip thresholds.

### Independent execution note

The partial independent run does not reproduce the package's reported 48/48 test count because the review environment lacked a Parquet backend and could not download the locked Python interpreter. The 41 tests that did not require that backend passed. Nothing in the observed failures indicated a discrepancy in the demographic recurrence, covariance construction, metric calculations, or deterministic scenario logic. The final archive should nevertheless be tested in a clean, network-enabled container from the exact lockfile immediately before submission.

---

## 16. *Oikos* submission readiness

The official *Oikos* author guidance current at the review date indicates that a Research paper may use up to 7,000 words of main text, a 300-word abstract, and no more than six display items, excluding material specified by the journal. The manuscript appears compliant on those dimensions: approximately 5,981 main-text words, an abstract below 300 words, and six display items when Table 1 and Figures 1–5 are counted together.

The journal also requires a data/code availability statement and expects data and code needed to reproduce the results to be archived rather than offered merely “on request.” The package is technically close to satisfying this requirement but the manuscript needs the formal statement and an anonymized review link/public DOI plan.

The journal's AI policy requires transparent disclosure of relevant use. The present declaration should identify the actual tools/models and their roles, and the same information should be entered in the submission system.

Official guidance consulted:

- [Oikos author guidelines](https://www.oikosjournal.org/authors/author-guidelines)
- [Nordic Society Oikos AI ethics policy](https://www.oikosjournal.org/authors/ai-ethics-policy)

### Journal fit

The topic fits *Oikos*: it addresses a general ecological mechanism, community stability, environmental covariance, and response diversity. The main editorial risk is not scope but perceived novelty. A simulation-only binary contrast may be judged too close to a covariance tautology. The analytical balance criterion, eigenmode interpretation, and nonlinear boundary tests would convert that risk into a strength.

### Reference-list audit

Before submission:

- run a strict cited-versus-listed key audit;
- either cite or remove currently unused items, including the entries corresponding to Cottingham (2001), Gonzalez and colleagues (2009, 2020), and Ives et al. (1999), if they remain unused in the final source;
- manually verify the metadata and DOIs of the very recent 2025–2026 papers against publisher records;
- ensure every software/package citation has a version and archival identifier where appropriate; and
- conform capitalization, journal abbreviations, DOI format, and page/article-number style to the journal's reference output.

Ives et al. (1999) appears especially relevant to the theoretical positioning and is more likely to belong in the argument than in an unused-reference list.

---

## 17. Editorial style sheet

Apply these changes consistently throughout the main text, captions, and SI:

- Use **aggregate abundance variability** or **community-abundance CV** for the measured response; reserve “ecosystem stability” for explicitly broader claims.
- On first use, write **cross-species correlation in commonly oriented environmental exposure**; use **exposure correlation** thereafter.
- Use **balanced mixed-sign responses** rather than simply “heterogeneous responses.”
- Use **aligned responses** for same-sign coefficients; specify whether magnitudes are matched.
- Use **innovation SD** \(\sigma_\varepsilon\) and **stationary exposure SD** \(\sigma_z\), never the ambiguous “environmental SD” in the persistence section.
- Use **temporal autocorrelation** for \(\phi\); avoid “persistence” where it might be confused with species persistence or extinction.
- Reserve **insurance** for a demonstrated aggregate variance reduction arising through covariance, not any decline in CV.
- Replace “richness effect” with **assembly-sequence pattern** unless the controlled richness design is used.
- Replace “explains” with **is associated with** for the descriptive synchrony regression.
- Replace “robust” with a stated domain, such as **retained across the core low-floor parameter grid**.
- Report effect sizes before Monte Carlo precision; avoid significance-style rhetoric for deterministic simulation contrasts.
- Use one spelling convention consistently (`stabilization`/`stabilisation`, `modeling`/`modelling`). Either is acceptable if applied uniformly.
- Avoid intensifiers such as “strikingly,” “remarkably,” and “surprisingly” unless the analytical benchmark establishes genuine surprise.
- Define all symbols immediately after the equation in which they first appear.
- Use sentence case for panel descriptions and consistent `Fig.`/`Figure` style according to the journal template.

---

## 18. Suggested reviewer-facing summary after revision

> This study asks when positive correlation among environmental exposures stabilizes rather than destabilizes aggregate community abundance. Its central result is supported by a magnitude-matched sign control: balanced mixed-sign coefficients convert positively correlated exposure into compensatory demographic forcing, whereas aligned coefficients transmit the common environmental mode to total abundance. A first-order covariance derivation identifies the general boundary in terms of abundance-weighted response balance, and nonlinear simulations map departures caused by density feedback, imbalance, temporal structure, and severe forcing. Controlled analyses distinguish this mechanism from changes in total abundance and response variance along richness sequences. The code and production outputs are fully archived and reproducible.

That is the paper the current bundle is close to becoming.

---

## 19. Prioritized action list

### Must complete before submission

1. Rebase the main result on the positive magnitude-matched comparator.
2. Add the covariance/eigenmode derivation and weighted balance criterion.
3. Clarify the shared physical orientation of environmental exposures.
4. Control or narrow the richness claim.
5. Add the fixed-stationary-variance autocorrelation control or narrow the persistence claim.
6. Test \(r_0\) and unequal abundance/weights.
7. Replace Figure 4 in the main text and promote Figure S3.
8. Rewrite the abstract, Results hierarchy, Discussion opening, and conclusion.
9. Add data/code availability and exact AI-use declarations.
10. Run a clean frozen-environment rebuild and final bibliographic audit.

### Highly desirable

1. Pair environmental realizations across sign treatments.
2. Add a continuous response-alignment gradient.
3. Show mean, SD, variance, and CV in richness analyses.
4. Lengthen high-autocorrelation trajectories.
5. Add one non-equicorrelated covariance example.

### Not necessary for the core paper

- a large empirical case study;
- a full asymmetric food-web model;
- dozens of additional parameter sweeps;
- formal extinction dynamics;
- a wholesale rewrite of the reproducibility repository.

---

## 20. Final assessment

This is a better manuscript than the current hierarchy makes it appear. The decisive evidence is already present: the magnitude-matched sign control shows that the core mechanism survives adversarial scrutiny. The main weaknesses arise because cleaner evidence is relegated to the SI while less controlled extensions carry headline claims.

The revision should make the paper simultaneously **narrower in causal wording and broader in theory**. Narrower means no unqualified richness effect, no pure persistence claim under fixed innovation variance, no implication that any mixture of signs stabilizes, and no separation of response sign from environmental correlation without a shared exposure orientation. Broader means replacing the particular sign sequences with an abundance-weighted covariance criterion that applies to arbitrary community contributions and environmental covariance matrices.

With that change, the nonlinear simulations have a clear role: they show when a simple covariance prediction survives density regulation and where it breaks under imbalance, dynamical memory, and numerical stress. That would be a strong, transparent, and appropriately general *Oikos* paper.
