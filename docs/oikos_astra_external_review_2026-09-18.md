# Independent external review: insurance hypothesis manuscript and computational evidence

**Recommendation: APPROVE WITH CHANGES — a small, bounded revision; no new production simulations.**

The paper is scientifically sound for its stated, conditional claim. In the specified stochastic Ricker community, changing response signs while preserving their magnitudes changes how exposure correlation affects variability of total abundance. The weighted forcing criterion is correct, its connection to linearised abundance variance is properly qualified, and the retained simulations demonstrate both substantial residual variability and a small reversal of the criterion's predicted direction near its boundary. Attempts to explain these results by a seed error, mismatched treatments, incorrect aggregation, numerical floors, or the short estimation window did not succeed.

I found **no BLOCKER or MAJOR scientific or reproducibility defect**. One supplementary display does present an undefined quantity as a numerical result, and the principal figures are too small to read comfortably at their submitted size. Both deserve correction. A short clarification of the relationship to earlier abundance-weighted response-diversity work would also strengthen the submission. These changes do not require broadening the research programme.

**Contribution and confidence.** The contribution is an explicit connection between physically oriented exposures, weighted response cancellation, and the quantitative limits of a linear benchmark in a nonlinear community model. It is an informative theoretical demonstration, rather than a new discovery that response covariance matters for stability. Confidence is high in the central calculations, implementation, retained results and archive reproduction; moderate in the paper's incremental novelty clearing Oikos's editorial threshold. Computational solidity cannot resolve that editorial judgement.

## Scope, independence and provenance

Reviewed on 18 September 2026 at commit **`d0fc7e1c906f5726b57eff7c5b23da73e76528c9`**, with a clean working tree at the start. This is a full current-product review, not a commit-diff review.

Primary materials were the main manuscript (`paper/manuscript/text/draft_ms_v2.md`), Supporting information, figure/table sources, current anonymous main and Supporting-information PDFs, all five scientific Python modules, the seven production specifications and saved parquet summaries, analysis runners, tests, and the candidate anonymous archive. The PDFs have **29 and 11 pages**, respectively. I inspected the complete page layouts, the displayed equations, all five main figures and four supplementary figures, and their numerical generation paths.

Required `AGENTS.md` and `docs/plan.md` were read. The plan unavoidably exposed earlier revision themes, historical verdicts and claims of successful checks. Those assertions were not used as validation. Initial observations were recorded in `build/astra_external_review_2026-09-18/initial_findings.md` before opening code/data or examining earlier reviews. **No previous review memo, response, correspondence, personal memory, or parent's scientific conclusions was consulted at any stage.** No review was delegated further.

All calculations and extraction occurred in `build/astra_external_review_2026-09-18/`, apart from the normal temporary directory needed by one existing path-safety test. Canonical code, manuscript sources, data and figures were not edited. All 44 reviewed artefact hashes were rechecked at handoff and remained unchanged. No full production grid, remote computation, publication or correspondence was undertaken.

Key SHA-256 values:

| Reviewed artefact | SHA-256 |
| --- | --- |
| Main manuscript source | `3ee5f6a7b51af1bdc48acb174df13329d89693e10a89406de41e70fea5b89451` |
| Supporting-information source | `1e1002607c0197390b53ad94f4759e510f453262ab26b17adb85ebe81c1176f4` |
| Anonymous main PDF | `904d553282a5e3928838b04e716c01ee4aa003776b9ddb019607127ec648b1a8` |
| Supporting-information PDF | `ea1895da3dd582c9b0ff3f4bef5b2d577ccad5419beb539a7c6b00d9a7759d06` |
| `insurance_hypothesis_2026-09-11_final/ih_package.zip` | `818d45b668a170fcf8790722c2f6cb6f0d0ecc84835ef091c212a01f36b9114f` |

The complete 44-artefact inventory, including all seven parquets and retained analysis outputs, is in `build/astra_external_review_2026-09-18/reviewed_artifact_hashes.json`.

## Findings requiring a bounded response

### MINOR 1 — Figure S2 depicts undefined zero-noise synchrony as low synchrony

**Status: demonstrated display defect; no effect on the principal conclusions.**

**Evidence.** Figure S2, Supporting-information PDF p. 9, includes the `sigma_env = 0` column. Its CSV reports `phi_ldm = 0` for S = 2 and 8 and `0.008264462809917354` for S = 4, across all five correlation settings. Directly regenerated post-burn-in trajectories have exactly zero range for every species and for total abundance. Their reported species variances are nevertheless approximately 10^-26 because of floating-point mean/variance calculations. For S = 4 the total variance is approximately 8.10 × 10^-28. Dividing these numerical residuals produces the apparent synchrony value.

Relevant implementation: `src/python/insurance_sim/model.py:322–340` calculates synchrony whenever the computed denominator is positive; `src/python/insurance_sim/production_figures.py:159–180` retains zero-forcing rows and `:230–239` colours them. Evidence is retained in `build/astra_external_review_2026-09-18/deterministic_synchrony_defect.json` and `claim_checks.py`. Main-text Methods already recognise undefined growth correlation at zero forcing (`draft_ms_v2.md:189`), but the same issue is not handled for this abundance-synchrony display.

**Why it matters.** A constant community has no synchrony to estimate: the intended ratio is 0/0. The coloured column invites the interpretation that absence of environmental noise produces almost perfect compensatory asynchrony. That is a numerical artefact, even though no headline claim depends on it.

**Smallest remedy.** Mask zero-forcing cells as undefined in the Figure S2 summary/rendering path, and identify the mask in the caption. Preserve the frozen parquet rows; this correction requires display regeneration only. Add one meaningful test ensuring deterministic zero-variation cases are not presented as estimated synchrony. A broader redesign of the metrics or a production rerun is unnecessary.

### MINOR 2 — The main figure text is too small at the size actually submitted

**Status: demonstrated presentation problem.**

**Evidence.** Main PDF pp. 25–26 place three-panel Figures 1 and 2 at about six inches total width. Figure 1 originates at 13.6 inches wide (`production_figures.py:1093`) with 7.0–7.4 pt legends (`:1118, :1162, :1199`). Its 4080-pixel image is embedded at approximately 682 ppi: the effective legend size is about **3.1–3.3 pt**, and default 10 pt tick text becomes about 4.4 pt. Figure 2's 14.5-inch source and 8 pt legends similarly yield approximately **3.3 pt** legends. The source width instructions are `paper/manuscript/text/figures_main.md:1–3`. `pdfimages -list` confirms the physical scaling; it is not a low-resolution screenshot artefact.

The small nonlinear reversal near A = 0.247 is especially hard to inspect in Figure 1B at this scale. The manuscript supplies its numbers, so the result is recoverable, but its principal display should make the comparison easier to assess.

**Smallest remedy.** Adjust the figure layout and text sizes for the final physical width, or stack panels where necessary. Check the result at ordinary reading/printing scale. A modest enlargement or local annotation/inset around the boundary can make the stated departure visible; the data and numerical summaries need not change. At least 7–8 pt text at final size is a sensible readability target, not a claim about a mandatory journal rule.

### MINOR 3 — Make the incremental contribution explicit relative to existing abundance weighting

**Status: editorial/scientific positioning risk, not a demonstrated false result.**

**Evidence.** The novelty paragraph (`draft_ms_v2.md:25`) identifies contribution weights as one of two elements less often made explicit. Yet Ross et al. (2023), already cited elsewhere in the paper, explicitly discuss abundance weighting, evenness and dominant versus rare contributions in sections 4.3–4.4. Earlier stochastic-community theory already separates environmental input covariance from dynamical transmission. [Ross et al. 2023](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14087), [Ives et al. 1999](https://ives.labs.wisc.edu/pdf/Ives_et_al._1999.pdf).

**Why it matters.** A specialist reviewer could read the paragraph as claiming the weighting insight itself, then dismiss a sound analysis as rediscovery. The present wording is restrained enough that this is not a priority dispute or a reason to block the paper; it is a preventable objection to the paper's contribution.

**Smallest remedy.** Add a short, explicit acknowledgement of that existing weighting argument at the novelty paragraph, then identify the contribution as its integration with commonly oriented exposure covariance and the tested nonlinear departures from the benchmark. The current title and most of the Abstract already support this positioning. No new simulations or a broad literature rewrite are needed.

### NIT — Remove the heading-only Supporting-information page

The Supporting-information PDF p. 7 contains only “Supplementary Information”, between captions and figures. Table S3 also begins on p. 4 while its numerical body appears on p. 5. Neither loses content, but the redundant heading page should be removed when rebuilding the document. Inspect the supplementary build's generated section/page-break handling; the figure Markdown itself does not contain that repeated heading. This is a layout cleanup, not a scientific revision.

## Scientific assessment and attempted falsification

### Question, comparisons and ecological interpretation

The sign-matched experiment is the paper's strongest element. With symmetric Gaussian exposure, replacing b by |b| preserves each species' marginal stochastic forcing, including temporal autocorrelation. At zero cross-species correlation the joint forcing distributions are equivalent. At positive exposure correlation, they differ in the intended covariance structure. The independent-exposure negative control agrees with that prediction. This supports a within-model causal comparison of response signs, without claiming an independently estimated effect of richness.

The paper also correctly distinguishes three different comparisons: mixed versus matched aligned at a fixed correlation; near-perfect versus independent exposure within a treatment; and the compound assembly/persistence sequences. The use of a ratio of **means of squared replicate CVs** is explicit, and the implementation uses that estimand rather than a squared ratio of mean CVs.

I did not find an unacknowledged substitution of “insurance” for absolute stabilisation as noise rises. Mean functioning, temporal variability, recovery and biological persistence are distinguished. The abundance floor is explicitly reversible and not called extinction. The treatments do not establish effects of species richness alone, temporal autocorrelation alone, generic interaction matrices, or response diversity in nature; the Discussion says so. Those are honest scope limits, not mandatory extra experiments.

The ecological abstraction is substantial: symmetric competition, fixed log-growth slopes, one exposure dimension, identical temporal colour and no demographic or observation noise. These choices limit external generality but also permit an interpretable test. More realistic covariance or interaction structures would be separate research questions. Adding them indiscriminately would weaken the current paper's focus.

### Mathematics

The following claims survived independent derivation and numerical checks:

- The equilibrium solves C_alpha N* = r0 K, giving the stated equal-K formula.
- With a_i = N_i* b_i, equicorrelated forcing has variance proportional to `(1-rho) sum(a_i^2) + rho (sum(a_i))^2`; its derivative changes sign at A = 1/S. Mixed signs are neither sufficient for balance nor necessary for every weaker form of insurance.
- The equal-K Jacobian has the stated common and contrast eigenvalues. Summing the first-order system closes on a scalar recurrence for total abundance.
- Solving the full joint population–environment discrete Lyapunov equation independently agrees with the scalar AR(1) transfer formula to maximum absolute discrepancy **6.1 × 10^-13** across the equal-K boundary treatments. Thus the stationary linear variance ratio really is the forcing ratio under those assumptions.
- All 20 boundary treatments have positive equilibria and locally stable Jacobians. The largest population-Jacobian spectral radius is approximately 0.933. Response norm is preserved along the rotation to the precision of the supplied vectors, and the unequal-K path preserves deterministic total abundance.
- Unequal K breaks the scalar closure, as acknowledged. For example, at the most uneven endpoint the full linear abundance-variance ratio is approximately 1.008, whereas the instantaneous forcing benchmark is 1.030. This supports retaining the manuscript's explicit distinction; it does not invalidate that labelled benchmark.
- The second-order identity follows from `x'_1 = x_1 + n u_1`. An independent Taylor-residual check has the expected cubic scaling, and the quadratic identity holds to numerical precision. The manuscript correctly calls it a local route for residual variability, rather than a quantitative decomposition of the observed 0.32 ratio.
- Taking stationary expectations of unguarded log growth gives the stated stationary mean constraint, conditional on the required moments. The text does not incorrectly invoke generic Jensen effects to assert a changed stationary mean.

See `analytic_audit.py`, `analytic_checks.json` and `analytic_boundaries.csv` in the review scratch directory. These checks validate the statements actually made; they are not a global proof of stochastic stationarity for every stress-grid parameter.

### Results and statistical uncertainty

Independent aggregations of the retained rows recover the central numerical contrasts:

| Quantity | Recomputed result |
| --- | ---: |
| S = 4, rho = 0.5, mixed mean CV | 0.083988 |
| Same setting, matched aligned mean CV | 0.148858 |
| Balanced endpoint squared-CV ratio | 0.319819; 95% MC interval 0.314845–0.324871 |
| Matched aligned endpoint ratio | 2.992106; 2.965410–3.019042 |
| Rotation q = 0.375, A = 0.246927 | 1.043172; 1.027978–1.058591 |
| Unequal-K path d = 1.0 | 0.963556; 0.952146–0.975102 |
| Unequal-K path d = 1.1 | 1.052860; 1.040817–1.065041 |

All 20 boundary ratios and their delta-method intervals were recomputed independently and agree with the generated summary to numerical precision. The calculation appropriately uses replicate-level variation of CV squared and independent endpoint ensembles. These are Monte Carlo intervals for this finite simulation design; they do not represent uncertainty about ecological applicability or structural model choice. The paper labels them appropriately.

The quoted means, growth-correlation patterns, inventory, variance decomposition and floor maxima are supported. Independent datasets at identical parameters differ slightly, as expected. For example, the SD example 0.0045 in Methods comes from the core grid; the matched-control grid has SD 0.00480. This does not alter the small-uncertainty argument. The S = 4 matched-control endpoint mean is 0.059488, so the text's 0.060 is a coarse approximation rather than strict three-decimal rounding; it is immaterial to the contrast.

The growth-correlation plots are descriptive diagnostics. They do not prove mediation, and the text does not claim that they do. Comparisons across richness also inherit the mathematical richness dependence of possible mean pairwise correlations; the main mechanism rests on matched treatments at fixed richness, not that cross-richness gradient.

### Convergence, finite windows and numerical safeguards

The paper specifies 300 burn-in steps and 300 retained steps but offers little direct evidence that those choices are adequate (`draft_ms_v2.md:82, :126, :209–213`). This was my main initial scientific concern, particularly for a ratio only 4% above one.

I challenged it with a **review-only** independent vectorised implementation: 500 trajectories per endpoint, 6,600 steps, seven targeted treatments and both rho = 0 and 0.999999. The selected treatments were balanced and matched aligned, the near-boundary rotation, both unequal-K crossing points, and both r0 = 0.25 endpoints. The independent recurrence and covariance were first checked against the package. I compared the original 300-step window, a late 300-step window, and a late 3,600-step window after 3,000 burn-in steps.

| Treatment | Published-design ratio | Late 3,600-step diagnostic ratio, 95% MC interval |
| --- | ---: | ---: |
| Balanced, r0 = 1 | 0.320 | 0.3182, 0.3162–0.3202 |
| Matched aligned, r0 = 1 | 2.992 | 3.0029, 2.9919–3.0139 |
| Rotation q = 0.375 | 1.043 | 1.0358, 1.0295–1.0422 |
| Unequal K, d = 1.0 | 0.964 | 0.9595, 0.9548–0.9642 |
| Unequal K, d = 1.1 | 1.053 | 1.0463, 1.0412–1.0513 |
| Balanced, r0 = 0.25 | 0.663 | 0.6471, 0.6407–0.6537 |
| Matched aligned, r0 = 0.25 | 2.774 | 2.7758, 2.7573–2.7944 |

Every conclusion-relevant sign survives, including weak amplification at the point where the benchmark predicts 0.9877. The finite-window values are not identical to long-window values, especially at low r0; that is compatible with the paper's explicitly finite-window estimand. No replacement of production values is warranted. Retaining a brief account of this targeted sensitivity in the Supporting information would improve evidence transparency, if the PI adopts it as a labelled review diagnostic. It is not a reason to simulate the full grids again.

The test does not establish convergence at every high-sigma/high-phi stress combination. Those regions have guard activity and are explicitly not the clean mechanistic inference. Zero floor occupancy in the matched-sign grid and negligible occupancy at the most uneven boundary treatment were independently confirmed. The retained 90-trajectory guard diagnostic reproduces exactly, including no high-side clipping and low-side means from approximately 0.00024 to 0.0070. Its full-trajectory frequencies are correctly distinguished from production post-burn-in occupancy.

## Computational integrity and independent archive reproduction

The archive supports the paper independently of the private repository. It contains the model, runner, seven specifications, all seven compact datasets, diagnostics, tests, lockfile, figure-number mapping and checksums. Its exclusion of manuscript sources and editorial material is consistent with its stated purpose as a computational companion to the separately supplied review documents.

Executed checks:

| Check | Outcome and limit |
| --- | --- |
| ZIP CRC, traversal/symlink checks | Passed; extracted 58 entries into review scratch. |
| Supplied input checksums | All 38 listed files passed. |
| Fresh archive `uv sync --python 3.12 --frozen --dev` | Passed using Python 3.12.3 and locked dependencies. |
| Archive `uv run --frozen pytest -q` | 35 passed. |
| Archive `uv run --frozen pyright` | Zero errors/warnings; only a version-update notice. |
| Archive `analysis/run_all.py` and `analysis/check_numerical_guards.py` | Passed; all **32 expected output hashes** match. |
| Archive source/spec/test/lock comparison | All 22 checked files match the current checkout. |
| All seven dataset hashes | Identical between archive and canonical datasets. |
| Reconstructed manifests and saved-data validation | 1,196 scenarios; 1,196,000 rows; 1000 replicates per scenario. |
| Independent seed and metadata census | Every stored seed matches the specification; all rows have 600 steps and 300 burn-in steps. |
| Stratified trajectory spot reproduction | 42 rows, sampling first/middle/last scenarios and replicates 0/999 in every grid, reproduce all checked summary fields **bit-for-bit**. |
| Independent metric identities | CV squared equals variance/mean squared; summed species means agree with totals; finite/range and floor checks pass. |
| Canonical test suite | 38 passed initially; the remaining path-safety test passed when run with its normal external temporary directory. |
| Identity-string scan of supplied text/code | No author/workstation strings found in the targeted scan. This is not a guarantee against inference from scientific content. |

The canonical test exception was caused by my first command placing pytest's temporary directory *inside* the repository, while the package builder correctly refuses to create packages there. Re-running that one test with normal temporary-directory placement passed. This was a review-harness error, not a repository failure. Logs preserve both outcomes.

Seeding deserves precise wording. Seeds are unique **within each scenario**, as the manuscript says. Compressing SeedSequence outputs to 32 bits yields 165 excess repeated seeds across the full 1,196,000-row collection. These are across scenarios, not duplicate replicates within a scenario, and no deliberate treatment pairing is present. This scale of accidental sharing does not plausibly explain the effects or invalidate the scenario-wise Monte Carlo estimates. For future production designs, passing full SeedSequence state would avoid that unnecessary compression; changing the frozen seeds now is not warranted.

The tests cover deterministic limits, AR(1) variance, covariance feasibility, summary identities, seed/scenario bookkeeping and a complete miniature figure workflow. They are proportionate to this repository. They do not substitute for scientific claim checks: notably, the existing bounded-synchrony test does not catch the deterministic Figure S2 artefact.

One additional validation limitation was demonstrated in memory: `validate_combined_frame` accepts a row whose stored seed and burn-in metadata have been altered, because those values are not checked (`production.py:771–832`). The original data were separately verified in this review, so there is no current integrity finding. Extending that validator to check seeds, `n_steps`, `burn_in` and scenario indices would be a useful bounded maintenance task, with a corrupted-row regression test; it is not a reason to rerun or reject these data.

## Literature, novelty and Oikos suitability

The manuscript is accurate in acknowledging the existing theoretical foundation. Direct source checks support the cited distinctions, while also limiting how much novelty can be assigned to the individual ingredients:

| Primary source checked | Relevance to this review |
| --- | --- |
| [Ives, Gross & Klug 1999](https://ives.labs.wisc.edu/pdf/Ives_et_al._1999.pdf), full author-hosted paper | Environmental inputs are filtered through population interactions; a common aggregate mode and contrast modes already appear explicitly. The present paper correctly builds on that machinery. |
| [Loreau & de Mazancourt 2008](https://www.journals.uchicago.edu/doi/full/10.1086/589746), full publisher text | The synchrony definition and the distinction between growth synchrony and abundance synchrony are correctly represented. Their nonneutral model already contrasts environmental-response structures. |
| [Loreau & de Mazancourt 2013](https://onlinelibrary.wiley.com/doi/10.1111/ele.12073), relevant full-text theory sections | Linearisation, response covariance, feedback and total-biomass CV are established prior theory; covariance and synchrony summaries need not supply independent mechanistic evidence. The manuscript respects that distinction. |
| [Fowler & Ruokolainen 2013](https://www.sciencedirect.com/science/article/abs/pii/S0022519313000416), publisher abstract and model/results excerpts | Ricker communities, temporal colour, covariance structure and assembly-dependent stability are prior art. The manuscript acknowledges them and does not present its persistence/richness panels as isolated causal effects. Full repository PDF access was blocked. |
| [Ross et al. 2023](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14087), full methodological text | Response derivatives, direction versus magnitude and abundance weighting are explicitly discussed. This is the basis for the small positioning recommendation above. |
| [Danet et al. 2025](https://eprints.whiterose.ac.uk/id/eprint/234335/1/danet-et-al-2025-response-diversity-is-a-major-driver-of-temporal-stability-in-complex-food-webs.pdf), original paper | Broader food-web simulations already connect response diversity to the sign of richness–stability relationships. This paper's advantage is interpretability of its covariance contrast, not broader realism. |

Recent contextual citations were also checked against primary publisher/institutional sources: [Hsieh et al. 2026](https://www.nature.com/articles/s41467-026-70192-x.pdf), [Sasaki et al. 2026](https://www.nature.com/articles/s41467-026-70606-w), [Kunze et al. 2026](https://epic.awi.de/id/eprint/60659/), and [Ross et al. 2026](https://nsojournals.onlinelibrary.wiley.com/doi/10.1002/oik.11358). Their cited topics and broad characterisations are supported. This was a claim-targeted literature audit, not an exhaustive audit of every reference and DOI.

Oikos's current scope explicitly values research that changes or substantially improves understanding of ecological mechanisms. The topic and theoretical format fit. The residual editorial risk is that specialists may regard the elementary covariance boundary plus one model's nonlinear deviations as too incremental. My judgement is that the combined physical-axis interpretation, matched-sign control, weighting path and clearly delimited departures offer a credible contribution, provided the paper claims that contribution precisely. An additional large simulation grid would not automatically address novelty. [Oikos aims and article guidance](https://nso-journals.org/oikos-for-authors).

For community ecologists, the opening explanation, consistent definition of insurance and explicit comparisons are clear. Technical readers can reconstruct the argument from the equations and SI. The algebra is not excessively obscure, though three main figures devote substantial space to qualified extensions. Moving those extensions is an optional editorial choice, not required for validity. I would retain the current primary emphasis on Figure 1 and avoid promoting stress tests or descriptive richness patterns into broader claims.

## Prioritised revision and stopping point

1. **Correct Figure S2's zero-forcing synchrony cells.** Mask and label them as undefined, add one targeted test, regenerate the affected display and Supporting information, and update the archive's affected expected-output hashes.
2. **Make Figures 1 and 2 readable at final PDF size.** Inspect the rebuilt pages and preserve all underlying numerical values. Give the near-boundary comparison enough space to be assessed.
3. **Add the brief prior-work acknowledgement at the novelty paragraph.** Keep the contribution centred on the integrated benchmark and measured nonlinear limits.
4. **Remove the redundant SI heading page during the same build pass.** Optionally retain a short, explicitly labelled account of the successful convergence challenge. Validator strengthening is useful follow-up maintenance, not a submission dependency.

**No new production computation is necessary.** The targeted review calculations already resolve the only finite-window concern likely to change the scientific verdict. They should not replace the frozen production results or be retroactively called prespecified. There is no evidence-based reason here to add a richness factorial, a fixed-stationary-variance persistence experiment, an alternative community model, or a broad covariance survey before submission.

After the above small repairs and their affected-output checks, I would stop revising and support submission. Acceptance remains an editorial judgement about the size of the contribution; the current computational evidence is strong enough to withstand substantive review.

## Evidence retained and explicit limits

All review scripts, results, logs and rendered pages are under `build/astra_external_review_2026-09-18/`. Main evidence files are `saved_data_audit.json`, `claim_checks.log`, `analytic_checks.json`, `window_diagnostic_ratios.csv`, the archive checksum/test/type-check logs, and `reviewed_artifact_hashes.json`.

Full production trajectories were not regenerated, only 42 deterministic spot reproductions plus the targeted independent sensitivity. No global theorem of stochastic persistence, convergence of the highest-stress grids, other operating-system runtime, DOCX layout, journal portal behaviour or public archival release was certified. The archive's manuscript-build exclusion means it reproduces computational figures/tables, not the review PDFs themselves; its README states this boundary. Fowler's full paper was inaccessible through the attempted repository route; its publisher abstract and model excerpts were accessible. Earlier reviews were never consulted, including after initial findings were recorded.
