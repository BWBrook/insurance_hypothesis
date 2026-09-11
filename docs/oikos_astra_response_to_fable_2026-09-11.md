# Astra's check of Fable's editorial revision

Reviewed 11 September 2026 against commit `ee75ab4` and Fable's uncommitted
manuscript changes. This is a review of those changes, not an applied revision.
Line references below describe that working-tree version. Fable's report and
correspondence thread 14, messages 43–49, were read as context.

## Recommendation

**APPROVE WITH CHANGES.** Keep the editorial improvements and the stronger
account of the balanced endpoint. Correct the claim about predicting direction,
reduce the mechanistic attribution to what the evidence establishes, and repair
two Methods statements that no longer match the code. No new simulations are
needed to resolve these issues.

Fable is right that my previous revision gave too little prominence to the
quantitative failure at complete first-order cancellation. At the balanced
endpoint, retaining 0.320 of the independent-exposure mean squared CV is a
substantial departure from the near-zero linear benchmark. I accept that
criticism and would keep the endpoint comparison in the abstract and Results.

I disagree that the point at `A = 0.247` is the least informative departure.
It answers a different question: can the benchmark get the *direction* wrong?
It can. The two observations belong together. Replacing the previous emphasis
with an unqualified claim that the criterion classifies direction exchanges one
problem for another.

The treatment names, empirical-to-theoretical Introduction sequence, added
Monte Carlo uncertainty, and explanations immediately after equations all
improve the manuscript for its intended audiences. Preserve them.

## Findings requiring correction

### 1. MAJOR — direction and universal compression are overstated

Locations: main text lines 5, 217–223, 245 and 275; Figure 1 caption in
`figures_main.md:1` and its copies; cover letter line 7; significance statement
line 7. The title also deserves reconsideration in this light.

The existing `analysis/reports/fig4_weighted_balance_boundary_summary.csv`
contains the following comparisons. These are readings of existing results,
not new analyses or fitted predictions.

| Treatment | Alignment A | Forcing benchmark | Nonlinear ratio | What it establishes |
| --- | ---: | ---: | ---: | --- |
| Balanced endpoint | 0 | 0.000001 | 0.319819 | Large magnitude departure despite the correct buffering direction |
| Response rotation | 0.246927 | 0.987707 | 1.043172 | Opposite directions; simulated interval 1.027978–1.058591 excludes one |
| Unequal K endpoint | 0.257497 | 1.029989 | 1.052860 | Amplification is underpredicted, not overpredicted |

Thus “predicts the direction and ordering”, “classifier of direction”, and
“over-predicts buffering below the boundary and amplification above it” need
qualification. Most rotation ratios are closer to one than their benchmarks,
but the near-boundary rotation point is not. The final unequal-K point is also
farther from one, even though the benchmark has the correct sign there.

The unequal-K crossing is bracketed by `A = 0.229638` and `0.257497`; this
interval contains `0.25`. The data therefore do not establish the new wording
“close to, but not at, the forcing benchmark” for that path. Say “brackets the
forcing boundary”. The resolved displacement belongs to the rotation path.

Use “captures the broad transition and endpoint contrast, but not the exact
nonlinear threshold or effect size”. Keep the measured ratio defined as the
**ratio of mean squared CV**, not an unspecified fraction of variability or a
fraction of CV itself. A ratio of 0.32 in squared CV does not mean a ratio of
0.32 in CV.

### 2. MAJOR — a plausible nonlinear route has become an established explanation

Locations: main text lines 109, 118, 223 and especially 245.

The second-order route is locally valid and can be exhibited algebraically. It does
not establish the numerical residual, universal compression, the threshold
shift, or the attribution of the r0 pattern to common-mode memory alone.

For equal K, write `N_i = n + x_i`, where n is the common equilibrium abundance,
and let `u_i = b_i z_i - (C_alpha x)_i/K`. The local expansion of the implemented
unguarded recurrence is

\[
x_i' = x_i+n u_i+x_i u_i+\tfrac12 n u_i^2+O(3).
\]

Consequently, for total departure X and first-order forcing F,

\[
X' = \lambda_c X+F+
\sum_i x_i u_i+\tfrac12 n\sum_i u_i^2+O(3).
\]

The convex exponential contributes the positive square term, but the
abundance–growth cross term is not sign-definite. Their time covariances and
feedback matter for stationary variance. A convexity argument alone cannot
establish the claimed explanation. At the equilibrium itself, balanced slopes
and a common nonzero exposure already give a nonzero quadratic aggregate term;
persistent contrast-mode memory is not a necessary condition for this route.

The independent methodological check makes the route more explicit. For
first-order departures `x^(1)` and aggregate second-order departure `X^(2)`,
the two quadratic terms combine as

\[
X_{t+1}^{(2)}=\lambda_c X_t^{(2)}+
\frac{\|\mathbf x_{t+1}^{(1)}\|^2-\|\mathbf x_t^{(1)}\|^2}{2n}.
\]

Changes in the squared magnitude of contrast fluctuations can therefore drive
aggregate fluctuations. The input has zero mean under stationarity, but can
have nonzero variance. This supports the route Fable proposes without making
convexity alone, a positive constant residual, or a shifted stationary mean
its explanation.

The new statement “the common mode ... has no memory at r0 = 1, so the linear
calculation is exact for it” is particularly misleading. The closure is exact
**within the linearised model**, for all stable r0 in the equal-K setting. It
does not make the nonlinear total-abundance dynamics exact at r0 = 1. Also,
zero direct abundance carryover does not remove the temporal memory in the
AR(1) forcing.

Changing r0 changes both eigenvalues, equilibrium abundance, and the size of
environmental shocks relative to population growth. At S = 4, changing r0
from 1 to 0.25 changes `(lambda_c, lambda_d)` from approximately `(0, 0.632)`
to `(0.75, 0.908)`, while equilibrium total abundance falls from 210.526 to
52.632. Figure 1C does not isolate common-mode memory. Retain the robust result
that the mixed/aligned sign contrast survives, and describe the attribution
of its magnitude as unresolved.

Fable's review also describes a common additive-residual diagnostic. Even as a
heuristic, an identical residual H added to high- and low-correlation variances
gives `R = (p L + H)/(L + H)`, where p is the benchmark ratio. For positive L,
`R = 1` if and only if `p = 1`. Such a construction can compress ratios towards
one, but cannot shift the crossing or reverse the sign. This is another reason
not to turn that diagnostic into the explanation of the boundary departure.

### 3. MAJOR — the realised-growth equation no longer describes the saved metric

Location: main text lines 182–185; implementation:
`src/python/insurance_sim/model.py:343`.

Fable removed the additive floor from the displayed log-growth equation.
The production code still computes `diff(log(obs + floor))`, not
`diff(log(obs))`. Already flooring abundances does not make these expressions
identical. For a transition from N_min to 2 N_min they give `log(3/2)` and
`log(2)`, respectively. The difference is negligible far above the floor but
material at the stress boundary.

Restore

\[
g_i(t)=\log[N_i(t+1)+N_{\min}]-\log[N_i(t)+N_{\min}],
\]

and explain that this includes an additional numerical offset after abundance
flooring. Preserve the code and existing metrics. Despite the handoff's
“equations are unchanged” description, this equation was changed.

### 4. MAJOR — lower-bound correlation clipping is incorrectly ruled out

Locations: main text line 70; `tables_main.md:14` and the copy in `tables.md`.

The new text says requested and effective correlation differ only at requested
correlation one. Figure 5 includes S = 4 and requested correlation -0.5. The
existing `effective_rho` implementation clips that to
`-1/3 + 10^-6 = -0.333332333...`. This is specified by the unchanged formula
at main-text line 68 and the active production spec.

Replace the sentence with: “Requested correlations outside the feasible
interval are clipped at either boundary. In the present grids this affects
the requested value of one and the S = 4, requested rho = -0.5 treatment in
Figure 5.” Keep epsilon explicitly stated. Table 1 can simply refer to the
feasibility bounds in Methods.

### 5. MINOR — precise treatment definitions need small repairs

Locations: main text lines 47–51; treatment rows in Table 1.

- Odd richness occurs in Figure 4. Mixed slopes then include one zero-response
  species, with equal numbers of positive and negative responders among the
  remainder. “Half the species ... and half ...” is not true for those cases.
- Absolute values produce nonnegative slopes; zero remains zero. “Nonnegative”
  is a safe general definition of the matched aligned treatment, although its
  current even-richness production comparisons do have strictly positive slopes.
- The steep aligned treatment has greater overall response magnitude, not a
  larger absolute slope for every corresponding species. At S = 4 the first
  steep aligned slope is 0.1, versus magnitude 0.5 in the mixed treatment.
- Keep the caption-specific legend mappings. The generic mapping in Methods
  should not imply that every use of “aligned” denotes the steep treatment:
  Figure 1's “aligned, matched magnitude” denotes the matched treatment.

## Suggested synthesis for the manuscript

These are proposed replacements, not applied edits.

**Abstract: replace the final benchmark-accuracy passage with:**

> The benchmark captured the broad transition but not its exact threshold or
> effect size. At balanced responses, mean squared CV remained 0.32 of its
> independent-exposure value despite near-complete cancellation in the linear
> benchmark. Near the response-alignment threshold, the simulation showed weak
> amplification where the benchmark predicted weak buffering.

Define CV at its first occurrence if using this wording. Remove the earlier
duplicate occurrence of the 0.32 result, or combine these sentences with the
endpoint comparison, to keep the abstract concise. Preserve the matched-sign
contrast and the empirical quantities to measure.

**Results heading:** “Weighted alignment captures the broad transition, with
nonlinear departures”. Lead with the balanced endpoint, retain the aligned
endpoint and the sign-reversal point, and describe compression as a broad
rotation pattern with the stated exceptions. Keep causal interpretation out
of the final r0 Results sentence.

**Discussion: replace the mechanistic explanation beginning “The explanation
lies...” with:**

> Linear cancellation does not imply constant total abundance in the nonlinear
> model. Products of abundance deviations and growth responses, including
> quadratic terms from the Ricker update, can contribute to total abundance
> even when the first-order forcing cancels. This provides a route for the
> remaining variability, but the present comparisons do not separate these
> contributions or establish their individual effects on the threshold.
> Changing intrinsic growth rate also changes equilibrium abundance and both
> common and contrast population modes. The persistence of the mixed/aligned
> sign contrast across these changes is therefore the supported result; its
> changing magnitude is not attributable to common-mode memory alone.

**Figure 1 caption: replace the claim after the benchmark formula with:**

> The benchmark provides the linear comparison; nonlinear ratios depart from
> both its magnitude and, near the rotation threshold, its predicted direction.

Propagate that qualification to the Conclusion, cover letter and significance
statement. Keep the two empirical observations distinct. Avoid the Conclusion's
new “how much stability diversity will buy” metaphor.

**Title:** Fable's wish for a more informative title is reasonable, but
“determines whether” is too categorical for the nonlinear claim. One possible
synthesis is “Abundance-weighted responses and nonlinear limits to buffering
under correlated environments”. This remains a PI preference after the body
claims are corrected.

**AI statement:** naming both providers is appropriate. More precise attribution
would retain Codex's existing description of computational assistance and
describe Claude's contribution separately as literature checking, scientific
review and editorial revision. Final wording remains the author's declaration.

## Verification and handoff

Parent checks were limited to source/diff inspection, arithmetic on existing
CSV values and equations, the existing correlation-clipping helper, SHA-256
comparisons, caption/table-copy comparisons, and read-only inspection of the
current PDF and DOCX files. An independent methodological specialist checked
the second-order expansion and also evaluated a small unfitted
stationary-Gaussian approximation. Only the checked algebra is used here; the
exploratory numerical approximation is not adopted as manuscript evidence.
No simulation, production regeneration, numerical guard run, manuscript
rebuild, or new fitted model was performed.

- All 51 files in the preceding protected baseline retain identical hashes.
- The new Monte Carlo values are correct: replicate SD 0.004474884 and
  SE 0.000141508 for the stated mixed-treatment cell in
  `analysis/reports/fig1_panels_summary.csv`.
- The nine combined figure blocks match the five main plus four supplementary
  blocks; main and supplementary tables match their combined source copies.
- The abstract has 256 whitespace-delimited words. The existing main PDF has
  29 pages and begins the Introduction on page 2; Supporting information has
  10 pages. Both PDFs pass the configured text/metadata identity-pattern check.
- Both current anonymous DOCX files still contain identifying local-path
  metadata (`/home/bwbrook`), as Fable's handoff warned. They require the
  existing sanitizer after the final rebuild.
- Reference metadata and the full page-by-page layout were not re-audited in
  this pass. Earlier successful code tests remain evidence for the unchanged
  computation, not validation of the newly edited prose.

The next coherent action is to apply the bounded corrections above, keep
Fable's successful editorial work, then run all six sequential manuscript
profiles, the golden contract, identity sanitization and refreshed manifests,
and inspect the final PDFs. The anonymous computational archive does not
contain the manuscript and its builder/data are unchanged; its content need
only be rebuilt if its README or included files change. Confirm the existing
archive remains the intended submission artifact. No scientific expansion is
justified by this review.

## Approved implementation status

The PI approved and the final author-read revision implemented these corrections
on 2026-09-11. The final title adds “community” to the proposed title above.
The 240-word abstract, 29-page main PDF, 11-page Supporting information,
one-page cover letter, all six profile checks, identity sanitation, independent
mechanism approval, and clean minimal-package verification are recorded in
`docs/oikos_submission_checklist.md`. The verification section above describes
the earlier review-only snapshot, not the final artifacts. All 51 protected
hashes remain unchanged; no full production grid was rerun.
