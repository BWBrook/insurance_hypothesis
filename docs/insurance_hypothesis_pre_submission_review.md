# Pre-submission review: insurance hypothesis manuscript for *Oikos*

## Overall verdict

I would not send this quite as-is, but I would be comfortable sending it after a focused tightening pass. The core idea is strong, the manuscript is readable, and the repository is much more defensible than the usual “simulation paper with scripts somewhere” submission. The production workflow has versioned simulation specs, shard validation, manifest checks, tests, figure-generation code, blinded submission profiles, and supporting tables documenting production runs and floor occupancy. That puts you well ahead of most pre-submission drafts.

The main vulnerability is not that the result is wrong. It is that a sharp reviewer could say: “Isn’t this just algebraically baked in by multiplying correlated environmental variables by slopes of opposite sign?” The answer is partly yes, and that should be embraced rather than hidden. The manuscript should make the analytical mechanism explicit, then position the simulations as the dynamical demonstration of how that covariance structure propagates into abundance synchrony, community CV, richness effects, floor behaviour and robustness. That single change would make the paper feel less like a simulation discovery and more like a clean mechanistic theory paper.

Oikos is a plausible target. Its current scope emphasises work that changes or substantially improves understanding of ecological mechanisms, processes or patterns, while giving low priority to incremental extensions of known results. The manuscript fits best if framed around the mechanism “environmental covariance is not realised synchrony; response-direction structure determines the translation between them”, rather than the broader, already familiar claim that biodiversity can stabilise ecosystem function. ([nso-journals.org](https://nso-journals.org/oikos-for-authors))

## The central scientific story is good, but sharpen the novelty

The title, abstract and Introduction are already close. The title is punchy and Oikos-compatible because NSO explicitly encourages titles that are concise, broadly comprehensible and, where possible, state the main result. ([nso-journals.org](https://nso-journals.org/author-guidelines)) My worry is the word “only”. In the aligned-positive regime, richness still gives statistical averaging, and the manuscript itself acknowledges that. A hostile reviewer could object that biodiversity can still buffer somewhat when responses do not diverge; what fails is strong compensatory insurance. I would either soften the title to “Biodiversity buffers environmental variability when species responses diverge” or keep the current title but be very precise in the Abstract and Discussion that “only” refers to compensatory insurance under the model’s definition, not to every possible richness-related reduction in CV.

The best conceptual contribution is the imposed-versus-realised synchrony separation. That is genuinely useful. The manuscript states this clearly in the Abstract and Significance Statement, and the Methods define the contrast between imposed environmental correlation, realised growth-rate correlation, abundance synchrony and community CV. fileciteturn8file0L3-L3 I would push that even harder. The insurance hypothesis literature already says asynchrony matters; your contribution is showing, in a stripped-down dynamical setting, that shared environmental forcing can either synchronise or desynchronise species depending on the sign structure of response slopes.

## Add one analytical paragraph: it will armour-plate the paper

At the moment, the model’s key mechanism is demonstrated numerically. It should also be shown analytically, at least as a first-order environmental-response argument. For the environmental response terms alone,

$$
\operatorname{Cov}(b_i z_i, b_j z_j)
=
b_i b_j\,\operatorname{Cov}(z_i,z_j)
=
b_i b_j\,\rho_{\mathrm{eff}}\frac{\sigma_{\mathrm{env}}^2}{1-\phi^2}.
$$

For non-zero slopes, the corresponding response-term correlation is essentially \(\operatorname{sign}(b_i b_j)\rho_{\mathrm{eff}}\). Thus, when all slopes are positive, positive environmental correlation produces positive covariance in growth forcing; when slopes have opposite signs, the same positive environmental correlation produces negative covariance in response forcing. In a symmetric community near equilibrium, the variance of the aggregate first-order environmental forcing is approximately

$$
\operatorname{Var}\left(\sum_i w_i b_i z_i\right)
=
\frac{\sigma_{\mathrm{env}}^2}{1-\phi^2}
\left[
\sum_i (w_i b_i)^2
+
2\rho_{\mathrm{eff}}\sum_{i<j} w_i b_i w_j b_j
\right],
$$

where \(w_i\) are abundance or biomass weights. For balanced mixed slopes and similar weights, the cross-terms can cancel aggregate forcing as \(\rho_{\mathrm{eff}}\) increases; for aligned slopes, they reinforce it. This is the mathematical spine of the paper. Add it in Methods or early Results, then show that the Ricker simulations preserve, dampen or distort this first-order expectation through density dependence and stochastic abundance dynamics.

This will also defuse the “obvious result” critique. You can say, in effect: yes, the sign of \(b_i b_j\) determines the environmental covariance term; the simulation contribution is to show how that first-order response structure maps into realised per-capita growth correlations, Loreau–de Mazancourt synchrony, community CV, richness scaling, persistence sensitivity and stress-regime behaviour.

## Fix a real inconsistency in the production seeding claim

The manuscript says that the same base-seed scheme pairs replicate indices across comparable scenario families, reducing Monte Carlo comparison noise. That is not true for the production runner as currently written. The production seed is generated from `[base_seed, scenario_index, replicate]`, so changing scenario index changes the random stream even when replicate number is the same. fileciteturn31file0L3-L3 This is not scientifically fatal, because 1000 replicates make Monte Carlo noise small, and independence across scenarios is perfectly defensible. But the current statement is false for the production analyses.

The easiest fix is textual: remove the claim about paired replicate indices and say that replicate streams are deterministically seeded and independent across scenarios. If you want common-random-number pairing, redesign the seed so directly comparable mixed/positive scenarios with the same \(S\), \(\sigma_{\mathrm{env}}\), \(\rho_{\mathrm{env}}\) and \(\phi\) share the environmental realisation, with slope mode excluded from the seed. That would be elegant, but unnecessary this close to submission unless you want the additional precision.

## Tighten the deterministic equilibrium statement

The Methods give the deterministic symmetric equilibrium as

$$
N_i^\ast = \frac{K_i}{\alpha_{\mathrm{intra}}+\alpha_{\mathrm{inter}}(S-1)}.
$$

That is only true because \(r_0=1\). The model equation is

$$
N_i(t+1)=N_i(t)\exp\left[r_0 - \frac{\alpha_{\mathrm{intra}}N_i+\alpha_{\mathrm{inter}}\sum_{j\ne i}N_j}{K_i}\right],
$$

so the general equilibrium is

$$
N_i^\ast =
\frac{r_0 K_i}{\alpha_{\mathrm{intra}}+\alpha_{\mathrm{inter}}(S-1)}.
$$

The code and table set \(r_0=1.0\), so the numerical work is fine. fileciteturn56file0L3-L3 But the Methods should explicitly state \(r_0=1\), or give the general expression and then note the simplification.

A related issue is Table 1’s model equation. It currently writes the competition term as \([N_i(t)+\sum_j\alpha_{ij}N_j(t)]/K_i\), which is less clear than the manuscript equation and could be read as double-counting \(N_i\). fileciteturn56file0L3-L3 I would replace the table equation with the exact manuscript equation, or simply refer to the equation in Methods rather than restating it in compressed form.

## Be more exact about richness and response diversity

The Results and Discussion say that increasing \(S\) “expands the range of response slopes represented”. Under the implemented mixed regime, the range is fixed at \([-0.5,0.5]\); increasing \(S\) fills that same range more densely. The code uses `np.linspace(-0.5, 0.5, n_species)` for mixed slopes, and analogous fixed ranges for the other regimes. fileciteturn6file0L3-L3 This is a small sentence-level issue but an important conceptual one, because richness and response-diversity sampling are deliberately coupled in the design.

I would rewrite those passages along these lines: “Increasing richness does not widen the imposed slope range; it increases the number of species sampling that range, thereby increasing the number of compensatory pairings and reducing the relative contribution of any one species’ fluctuations to total biomass.” Also note that odd-richness mixed communities include a zero-slope species. That is not a problem, but it is a neutral response rather than a divergent response direction.

There is also no single-species production baseline in the main grids; the production richness grid starts at \(S=2\). fileciteturn34file0L3-L3 The Methods currently define insurance partly relative to “single-species or aligned-slope communities”. Either add an \(S=1\) baseline or change this to “species-poor or aligned-slope communities”. I would not add new \(S=1\) runs unless needed; the textual fix is enough.

## Positive-matched control: use it more strategically

The positive-matched control is one of the most important defences against a reviewer saying that the mixed-versus-positive contrast is confounded by slope magnitude. The production spec explicitly describes it as a 1000-replicate comparison among mixed, positive-matched and aligned-positive regimes at \(S=4\) and \(S=8\). fileciteturn37file0L3-L3 The supplementary caption says the positive-matched control sits well below the fully aligned-positive regime for community variability, while realised growth correlations remain closer to aligned responses than to mixed responses. fileciteturn45file0L3-L3

That is a nuanced and valuable result. It says slope magnitude affects the amplitude of variability, while sign structure controls the synchrony mechanism. I would bring one sentence from Figure S3 into the main Results, because otherwise the Abstract’s “not driven solely by competition strength or slope magnitude” claim feels under-supported in the main narrative. The safest phrasing is: “The magnitude-matched aligned control reduced absolute CV relative to the wider positive-slope regime, but retained high realised growth synchrony, indicating that slope magnitude affects fluctuation amplitude whereas response sign structure governs the compensatory mechanism.”

## Strengthen the CV interpretation with a variance decomposition

The paper uses total-biomass CV as the central stability metric. That is reasonable, but richness changes mean total biomass in this model because the deterministic total equilibrium is \(S K/[1+0.3(S-1)]\) when \(r_0=1\). CV can decline because the numerator falls, because the denominator rises, or both. The manuscript partly handles this by reporting approximate species-level CV, but I would still add a small supplement decomposing the community variance:

$$
\operatorname{Var}(N_{\mathrm{tot}})
=
\sum_i \operatorname{Var}(N_i)
+
2\sum_{i<j}\operatorname{Cov}(N_i,N_j).
$$

A supplementary table or panel showing mean total biomass, total variance, summed species variances and summed covariance terms would materially improve the inferential clarity. It would connect directly to the theory cited in the Introduction and would show whether mixed-slope insurance is primarily covariance reduction, denominator inflation, or both. This is especially important because the insurance literature distinguishes effects of biodiversity on means from effects on variability, and your own manuscript foregrounds that distinction. fileciteturn53file0L3-L3

## Treat Figure 4 as association, not mediation, unless you add a model

Figure 4 is useful, but the current wording “consistent with stabilisation being mediated by reduced realised synchrony” is slightly stronger than the analysis. Across scenario means, CV, richness, \(\sigma_{\mathrm{env}}\), \(\rho_{\mathrm{eff}}\), \(\phi_{\mathrm{LdM}}\) and growth-rate correlation are all co-varying by design. A Pearson correlation of CV with synchrony is informative, but it is not a mediation analysis. fileciteturn10file0L3-L3

Either soften to “associated with” and “consistent with a synchrony-mediated interpretation”, or add a compact regression/partial-correlation diagnostic such as

$$
\mathrm{CV}_{\mathrm{tot}}
\sim
\sigma_{\mathrm{env}} + S + \rho_{\mathrm{eff}} + \phi_{\mathrm{LdM}},
$$

or the same with growth-rate correlation. You do not need to over-model a simulation grid, but a partial diagnostic would stop a reviewer from saying that Figure 4 merely rediscovers the plotted variables’ common dependence on the experimental grid.

## Clarify what “growth-rate correlation” actually measures

The code computes mean pairwise growth-rate correlation from post-burn-in changes in log abundance, not from the direct environmental forcing term \(b_i z_i(t)\). fileciteturn6file0L3-L3 That is a defensible realised-dynamics measure, but it includes density dependence, abundance feedbacks, floor effects where present, and any nonlinearities introduced by the Ricker map. I would explicitly call it “realised per-capita log-growth correlation” rather than “growth response synchrony” in places where ambiguity matters.

This also argues for adding the analytical environmental-response correlation described above, or a supplementary panel showing the correlation of \(b_i z_i(t)\) before density dependence. Then Figure 3 becomes more compelling: direct response covariance gives the expectation; realised log-growth correlations show how the full model modifies it.

## Environmental autocorrelation: either add a variance-standardised sensitivity or narrow the claim

The manuscript is admirably honest that increasing \(\phi\) at fixed innovation SD increases both persistence and stationary environmental variance. fileciteturn10file0L3-L3 Figure 5’s production spec also states that it keeps \(\sigma_{\mathrm{env}}=0.5\) and varies \(\phi\). fileciteturn36file0L3-L3 That is acceptable if described as a combined persistence-plus-stationary-variance stress test. But if you want to claim robustness specifically to autocorrelation, a reviewer may reasonably ask for a variance-standardised version in which the innovation SD is scaled as \(\sigma_{\mathrm{innov}}=\sigma_{\mathrm{target}}\sqrt{1-\phi^2}\), holding stationary variance constant.

I would not necessarily add another main figure. A short supplementary check with \(S=2,4\), mixed slopes, \(\rho_{\mathrm{env}}\in\{0,0.5,1\}\), and fixed stationary SD would be enough. If you do not add it, soften the Results and Abstract from “persist across temporal autocorrelation” to “persist across a persistence–variance stress gradient generated by increasing AR(1) autocorrelation at fixed innovation variance.”

## Figures: strong enough, but Figure 1 should be more comparative

Based on the captions and plotting code, Figure 1’s current design is slightly asymmetric: panel A is a heatmap only for aligned positive responses, while the mixed response surface is mostly relegated to Supporting information. The code comment even says the full mixed-slope heatmap is better suited to supplementary diagnostics because its rho-axis structure is weak relative to the sigma effect. fileciteturn18file0L3-L3 That may be visually efficient, but it undersells the central contrast. If the main claim is mixed versus aligned, I would strongly consider making Figure 1 a three-panel display: mixed heatmap, aligned heatmap, and aligned-minus-mixed difference heatmap, or mixed/positive heatmaps plus a difference curve. The current panel B averaged over \(\rho_{\mathrm{eff}}\) hides the counterintuitive “CV can decline as environmental correlation increases” message.

Figure 3 is probably the strongest main display: it directly shows imposed driver correlation versus realised growth correlation under mixed and aligned slopes, with the \(\Delta\) panel making the decoupling visible. fileciteturn42file0L3-L3 Figure 2 is clear but should be interpreted explicitly as richness conditional on adding more samples from the same mixed response range, not a generic richness effect. Figure 5 is useful but should be labelled as the persistence/stationary-variance stress gradient, not pure autocorrelation.

Also attend to NSO figure formatting: their guidelines prefer vector formats such as PDF/EPS/TIFF, require clear common sans-serif fonts, and specify lower-case panel labels in parentheses, e.g. “(a), (b), (c)”. ([nso-journals.org](https://nso-journals.org/author-guidelines)) The code and captions currently use bold uppercase panel letters. That will not derail review, but changing now avoids production-stage friction. The colour palettes in the plotting code look mostly sensible, but the journal explicitly asks for colour-blind-safe figures and alternative visual encodings where possible. ([nso-journals.org](https://nso-journals.org/author-guidelines))

## Reproducibility: the production scaffold is strong, but the review package must be unambiguous

The production workflow is a strength. The JSON specs declare purpose, rationale, manifest parameters, expected scenario counts, shard counts and row counts. For example, the Figure 1 high-resolution spec declares 570 scenarios, 5700 shards and 570,000 expected rows, with 1000 replicates per scenario. fileciteturn32file0L3-L3 The production validator then checks required columns, expected rows, duplicate scenario/replicate pairs, finite result columns, scenario parameter consistency, effective \(\rho\) and clipping status. fileciteturn31file0L3-L3 The tests also check basic model behaviour, effective-\(\rho\) clipping, deterministic synchrony extremes, AR(1) variance behaviour and the ability of `run_all.py` to use production summaries without legacy cached grids. fileciteturn24file0L3-L3 fileciteturn25file0L3-L3

The weak point is documentation ambiguity. The README and workflow still mix older exploratory `data/sim/grid` caches with final production summaries. The generic `run_full_grid.py` defaults to 200 replicates and is not the production pathway used for the main figures. fileciteturn15file0L3-L3 The final review package should open with a brutally simple reviewer route: “To reproduce submitted figures without rerunning simulations, install with `uv sync --dev`, ensure the six production parquet summaries listed in Table S1 are present, then run `uv run python analysis/run_all.py`.” Then give a separate “full rerun” route through the production specs. The current blinded data statement says a de-identified package is planned and will include code, tests, production specs and compact production summaries. fileciteturn41file0L3-L3 That is exactly what Oikos/NSO expects, but it needs to be real at submission, not aspirational.

NSO requires all data, metadata, custom code and bespoke software necessary for full replication at first submission; the material need not be public at that stage, but it must be available to reviewers, and identity should be concealed if archived. ([nso-journals.org](https://nso-journals.org/author-guidelines)) A private GitHub repository under `BWBrook` is not double-anonymous. Upload an anonymised zip as “additional file for review but not for publication”, or use an archive option that supports blinded review. The repo already has a blinded submission profile, a title-page profile and an unblinded cover letter, which is good. fileciteturn40file0L3-L3

One small code consistency fix: legacy `run_full_grid.py` does not add `alpha_inter` to the output frame, whereas production outputs do and the manuscript says scenario-level summaries include \(\alpha_{\mathrm{inter}}\). Add `df["alpha_inter"] = args.alpha_inter` before appending. This will prevent confusion if anyone inspects the lower-replicate no-competition controls through the legacy path.

## Submission-format issues

The main text file currently includes a Significance Statement in `draft_ms_v2.md`. NSO says the significance statement should not be included in the main text file; it should be entered in the submission form. ([nso-journals.org](https://nso-journals.org/author-guidelines)) Your build system appears to separate the formal submission profile from the drafting profile, but make sure the final uploaded main text excludes the Significance Statement unless Oikos specifically asks otherwise for this article type. Similarly, NSO says the Data Availability Statement, Conflict of Interest Statement, Funding Statement and Acknowledgements should not be included in the main text file but entered in the submission system or provided separately as required. ([nso-journals.org](https://nso-journals.org/author-guidelines)) ([nso-journals.org](https://nso-journals.org/author-guidelines))

The blinded submission statements are good in substance. They say no empirical datasets were used, all results are simulation-generated, and a de-identified reproducibility package will be supplied. fileciteturn41file0L3-L3 For the title page, fill in funding and acknowledgements before submission; placeholders such as “[To be confirmed before submission]” should not survive into the editor-facing package. fileciteturn47file0L3-L3 The cover letter is well pitched to Oikos, but I would soften “richness buffers environmental variability only when species differ in response direction” to “strong compensatory insurance emerges only when…” to avoid the “but statistical averaging still buffers” objection. fileciteturn48file0L3-L3

## Prose and readability

The manuscript walks the tightrope well. It is tight without being cryptic, and it mostly avoids the deadening over-abstraction common in biodiversity–stability theory. The Introduction is strong but slightly overburdened with recent empirical examples. Oikos research papers should aim at a wide ecological readership. ([nso-journals.org](https://nso-journals.org/oikos-for-authors)) I would trim the Introduction by about 10–15%, mainly by compressing the paragraph that lists recent response-diversity and synchrony studies. The reader needs the state of the art, but the paper’s force comes from the model, not from demonstrating exhaustive coverage.

The reference file looks unusually well curated, including DOI-backed entries for the 2026 papers that the Introduction invokes. fileciteturn54file0L3-L3 fileciteturn55file0L3-L3 I would still do a final DOI/status audit, especially for the 2025–2026 material, because reviewers notice when very recent citations are preprints, in press, or not yet in final form. The NSO author guidelines also ask authors to cite essential sources, preferably original research rather than relying heavily on reviews. ([nso-journals.org](https://nso-journals.org/author-guidelines)) The balance is broadly fine, but the Introduction can lose a few review-style citations without weakening the argument.

## What I would change before submission, in order

First, add the analytical covariance argument for \(b_i z_i\) and, ideally, a small direct-response synchrony supplement. This is the highest-value scientific improvement.

Second, correct the production seeding statement. Either remove the common-random-number claim or change the production seeding scheme and rerun the relevant comparisons.

Third, fix the equilibrium expression and the Table 1 Ricker equation. These are small but highly visible mathematical details.

Fourth, revise the richness language: increasing \(S\) fills a fixed response-slope range; it does not expand the range. Make clear that the richness effect is conditional on richer communities sampling more response directions under your design.

Fifth, bring the positive-matched control into the main Results in one sentence, because it is your best defence against slope-magnitude confounding.

Sixth, add a variance/covariance or mean/variance decomposition supplement for total biomass CV. This will make the insurance interpretation much harder to attack.

Seventh, decide whether to add a variance-standardised \(\phi\) sensitivity. If not, consistently describe Figure 5 as a persistence-plus-stationary-variance stress gradient.

Eighth, consider redesigning Figure 1 to show mixed and aligned response surfaces side by side, or at least add a difference heatmap. The current main display does not fully expose the central contrast.

Ninth, prepare the anonymised review package now, with production parquet summaries included and the legacy/production distinction made explicit. NSO will expect the data and code necessary for full replication at first submission. ([nso-journals.org](https://nso-journals.org/author-guidelines))

## Bottom line

This is a strong submission candidate. The paper has a clear mechanistic claim, a tractable model, a sensible Oikos pitch, and a reproducibility scaffold that will reassure reviewers if packaged cleanly. The most likely reviewer criticisms are predictable and fixable: the mechanism is partly algebraic, richness and response diversity are coupled by design, positive-slope magnitude differs from mixed-slope magnitude, CV needs mean/variance decomposition, and autocorrelation is confounded with stationary variance. Address those pre-emptively, and the manuscript will feel
