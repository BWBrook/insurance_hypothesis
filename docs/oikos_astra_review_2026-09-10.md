# Fresh submission assessment: Oikos

Reviewed 10 September 2026 at commit `b8f81a6`. This is a scientific and editorial
assessment of the current product, with proposed wording. It does not replace the
accepted manuscript, display suite, or scientific decisions.

**Recommendation: make a bounded conceptual and editorial revision before
submission. The matched-sign result is persuasive; the principal risks are the
novelty claim and the strength attributed to the analytical boundary. Further
production simulations are not justified by this review.**

## Ecological assessment

The useful result is easy to explain: species can experience increasingly similar
environmental conditions while their contributions to community abundance become
more compensatory. Whether that happens depends on which species respond in
opposite directions and how much they contribute. Species richness alone does not
identify that balance.

The strongest evidence preserves each species' response magnitude and changes
only its sign. At four species and exposure correlation 0.5, community CV is
0.0840 for balanced responses and 0.1489 for aligned responses: about 44% lower
variability. The independent-exposure control agrees between treatments. The
weighted-balance and growth-rate sensitivities make this more than an illustration
of perfect cancellation in one symmetric parameter setting.

The August revision has already addressed most of the former review's main
objections. The richness sequence, fixed-innovation autocorrelation gradient,
abundance floor, and distinction between imposed exposure and realised synchrony
are described candidly. Those issues should not trigger a new round of broad
simulation design. The remaining revision should make the contribution precise
and easier for an ecologist to follow.

## 1. State the new contribution against its closest predecessors

**Priority: resolve before submission.**

The abstract says the usual expectation “ignores” species contributions and
response orientation. The Introduction then says “What is missing is a usable
boundary” (`paper/manuscript/text/draft_ms_v2.md`, lines 5 and 19). These statements
invite a reviewer to challenge the history of the field before considering the
new results.

[Ives, Gross and Klug (1999)](https://ives.labs.wisc.edu/pdf/Ives_et_al._1999.pdf)
already separated environmental inputs from their amplification by community
dynamics, including a common abundance mode with eigenvalue `1-r`. That paper is
in the bibliography but is currently uncited.
[Fowler and Ruokolainen (2013)](https://doi.org/10.1016/j.jtbi.2013.01.016)
studied multispecies Ricker communities with environmental covariance, colour,
and assembly differences; it is absent from the bibliography. The latter
comparison was checked against the indexed author abstract, not an accessible
full text, so it establishes relevant overlap rather than equivalence of results.

The covariance quadratic form is established mathematics. The defensible
contribution is its explicit expression in terms of commonly oriented exposures,
abundance-weighted response slopes, and a controlled nonlinear test of where that
benchmark works and departs from the data. Do not imply that opposing responses
or covariance-mode arguments have only now been recognised.

**Proposed replacement for the gap claim:**

> Existing theory links community variability to environmental response
> covariance and to the filtering of those responses by population dynamics.
> Here I express the covariance prediction in terms of commonly oriented
> exposures and abundance-weighted response slopes, then test its accuracy in
> nonlinear communities using contrasts that preserve response magnitude.

Add the direct predecessors at this point and give the same account in the
significance statement and cover letter. Oikos currently prioritises work that
substantially improves understanding of ecological mechanisms; this is a reason
to sharpen the specific advance, not to claim a broader discovery.
[Oikos scope and article guidance](https://nso-journals.org/oikos-for-authors).

## 2. Separate the exact forcing criterion from approximate abundance prediction

**Priority: resolve before submission.**

The derivative of `Var(F)` with respect to equicorrelation is correct for the
fixed weighted response vector. It is a result about aggregate environmental
forcing. Transfer to stationary abundance variance also involves population
feedback; nonlinear temporal CV is a further step. The manuscript acknowledges
this distinction, but the title, abstract ending, Figure 4 caption opening,
and Discussion sometimes erase it (`draft_ms_v2.md`, lines 1, 5, 97–101,
254–256; `figures_main.md`, line 7).

The existing data already show why the distinction matters. The response-rotation
point nearest the benchmark boundary has:

| Quantity | Value |
| --- | ---: |
| Alignment index | 0.246927 |
| First-order threshold | 0.25 |
| Predicted forcing-variance ratio | 0.987707 |
| Nonlinear ratio of mean squared CV | 1.043172 |
| 95% Monte Carlo interval | 1.027978–1.058591 |

Thus the first-order benchmark predicts weak buffering at this point while the
simulated abundance statistic shows weak amplification. The difference is small
ecologically but resolved relative to Monte Carlo error. This is informative
model behaviour, not a failed simulation or an error to remove.

The current Results give both values but then say the shift occurs “without
changing the predicted ordering” (line 232). That may describe the broad gradient,
but it obscures the disagreement in classification at this particular point.
The tested sign crossing is bracketed by `A=0.117` and `A=0.247`; it is not a
precisely estimated nonlinear threshold. The unequal-abundance path more tightly
brackets its crossing at approximately 0.230–0.257.

**Proposed Results wording:**

> The first-order criterion captured the broad transition from buffering to
> amplification, but not its exact nonlinear boundary. At A=0.247, the forcing
> benchmark predicted a ratio of 0.988, whereas the simulated ratio of mean
> squared CV was 1.043 (95% Monte Carlo interval 1.028–1.059). This near-boundary
> disagreement shows that the forcing criterion is an approximate guide to
> nonlinear abundance variability.

The equal-abundance case permits a short analytical explanation of why the
aggregate follows a common dynamical mode. With unequal carrying-capacity
parameters, changing equilibrium abundance also changes the Jacobian; the
abundance-weight experiment is therefore not a manipulation of weights alone.
Say that explicitly. A general forcing-covariance identity does not by itself
establish a universal stationary abundance criterion for arbitrary community
dynamics.

A compact analytical bridge would strengthen this section. For equal `K`, let
`X_t` be the linearised departure of total abundance from equilibrium. Then
`X_(t+1) = lambda_c X_t + F_t`, with `lambda_c = 1-r0`. Because all exposures
have the same AR(1) coefficient, `F_t` is itself AR(1), giving

`Var(X) = Var(F) * (1 + lambda_c phi) / [(1-lambda_c^2)(1-lambda_c phi)]`.

For a stable equilibrium and fixed `r0` and `phi`, this multiplier cancels in the
correlation ratio. Thus the forcing benchmark is also the linear stationary
abundance-variance benchmark in the equal-`K` case, not merely a heuristic there.
For unequal `K`, the Jacobian is
`J = I - diag(N*/K) C_alpha`, and the aggregate generally does not close as this
scalar recurrence. A small deterministic Lyapunov calculation confirms the
distinction: at abundance-skew levels `d=1` and `1.1`, the linear stationary
ratios are approximately 0.89120 and 1.00817, whereas the instantaneous forcing
ratios are 0.91855 and 1.02999. Both still bracket a sign crossing on the same
tested interval. This explains a limitation of the benchmark without undermining
the observed local transition. These are diagnostic calculations, not new
production results or proposed changes to Figure 4's accepted benchmark line.

**Proposed title:**

> Abundance-weighted responses shape community buffering under correlated
> environments

## 3. Avoid an unsupported explanation based on shifts in mean abundance

**Priority: correct with the boundary wording.**

Line 232 attributes the shifted boundary partly to changes in mean abundance.
The boundary summary does not establish that mechanism. At the near-boundary
point, the two mean totals are 210.483 and 210.516, compared with a deterministic
total of 210.526. Across all boundary scenarios, mean totals differ from their
respective deterministic equilibria by at most approximately 0.21%.

There is also a useful exact constraint. Without the numerical guards, summing
the log-growth recurrence through time gives

`C_alpha mean(N) = K * [r0 + b * mean(z) - change(log(N))/T]`,

with multiplication on the right interpreted componentwise. For a positive
stationary process with the required finite expectations and zero-mean exposure,
this reduces to `C_alpha E[N] = r0 K`. Nonlinearity alone therefore does not
imply a shifted stationary mean in this model. Finite trajectories and guard
effects need separate treatment.

Use the empirical discrepancy to describe the limit of the approximation.
Do not assign it to a denominator mechanism that has not been isolated.
There is no need to add a new mean-response analysis simply to retain this clause.

## 4. Make the display sequence match the argument

**Priority: high-value presentation decision for the PI.**

The Results correctly begin with Figure 4, but the Methods, numbering, and
display sequence still begin with the older broad contrast. Figure 1 changes
slope magnitude as well as sign, and its colour scale is dominated by the
high-variance stress extension. Figure 4 provides the most direct evidence for
the present title and abstract.

The smallest revision is to promote the existing Figure 4 to Figure 1 and
renumber the remaining displays consistently, retaining every rendered panel and
all underlying values. Put the matched-control and boundary design paragraphs
first within Simulation design. Keep the Results centred on the matched sign
contrast and the two boundary paths before introducing broader extensions.

A shorter paper could move the richness and fixed-innovation displays to
Supporting information. That is optional and is not necessary to address the
scientific findings above. Do not redesign the accepted plotting suite or run
new grids solely to support a different narrative order.

The assembled main PDF is readable, but the three-panel central figure has small
legend text at its portrait-page size. It merits attention if layout changes are
approved; it is not currently clipped or corrupted.

## 5. Write the abstract for an ecological reader

**Priority: editorial revision alongside items 1–2.**

The current abstract packs the alignment formula, two variability statistics,
several parameter values, the rotation experiment, unequal abundances, and a
growth-rate sensitivity into 230 words. The ecological message competes with
the machinery. `CV`, `S`, and `r0` also appear without full definitions there;
current NSO guidance requires an abstract without unexplained abbreviations.
[NSO author guidelines](https://nso-journals.org/author-guidelines).

**Proposed abstract, for author review:**

> Biodiversity can buffer community fluctuations when species respond differently
> to environmental change, but opposing responses need not compensate if some
> species contribute much more than others. I used stochastic multispecies
> Ricker simulations to test how response direction and abundance determine
> whether increasingly correlated environmental exposures buffer total
> abundance. A covariance analysis gives a simple benchmark: increasing
> correlation reduces aggregate forcing variance when the squared sum of
> abundance-weighted response slopes is smaller than their summed squares.
> In four-species communities, changing only response signs produced a clear
> contrast. At exposure correlation 0.5, balanced responses gave a coefficient
> of variation of total abundance of 0.084, compared with 0.149 for aligned
> responses of identical magnitude. Relative to independent exposures,
> near-perfect correlation reduced mean squared coefficients of variation to
> 0.32 times the baseline for balanced responses and increased them to 2.99
> times the baseline for aligned responses. Continuous changes in response
> balance and equilibrium abundance produced transitions near the benchmark
> boundary, with a small but resolved departure in the nonlinear response
> experiment. The sign contrast persisted across the tested intrinsic growth
> rates. These results identify abundance-weighted response balance as an
> informative predictor of buffering in this model. Empirical assessment
> requires exposure covariance, species response slopes, and contributions
> to the aggregate property to be measured together on consistently oriented
> environmental axes.

In the main Methods, consider moving package inventories, wrapper shapes, and
toy-example test descriptions to Supporting information. Preserve equations,
sampling design, estimands, Monte Carlo intervals, and material guard behaviour
in the main paper. This is about keeping the ecological argument visible, not
reducing reproducibility.

## Verification and limits of this review

- Read the complete main manuscript, supporting tables and captions, editorial
  materials, current plan and decisions, and relevant model/diagnostic code and
  production summaries. An independent scientific auditor examined the central
  mechanism in parallel.
- Compared the central numerical claims directly with the saved Figure 4 CSV;
  no simulation rerun or modification of production data was needed.
- Independently evaluated the stationary covariance of the linearised model
  through an eight-state population/environment system and a discrete Lyapunov
  equation at the balanced and two near-boundary abundance treatments. This
  small deterministic calculation checks the analytical distinction above;
  it does not replace the nonlinear production evidence.
- Built the main and Supporting-information PDFs sequentially through the local
  `makedoc` using the repository profiles. They are 28 and 9 pages; the main
  Introduction begins on page 2.
- Main-manuscript lint and reference audit passed: 25 cited keys, zero unknown
  keys, five unused bibliography entries. This checks citation resolution, not
  literature completeness or claim support.
- Inspected rendered main pages 1, 6, and 27, Supporting-information page 2, and
  the original Figure 1 and Figure 4 images. No clipping or broken equations
  were observed in those samples. This was not a fresh page-by-page layout audit.
- Rebuilt the two anonymous DOCX files as manifest dependencies, sanitized them,
  checked for configured identity strings, and refreshed their manifests.
- Consulted current Oikos/NSO guidance. The prior review's assertion of a
  six-display-item research-paper allowance is not stated on the current pages;
  it should not constrain the revision as a confirmed current rule.
- The full production/test/release results remain the documented August gate;
  this review did not rerun that gate, regenerate figures, or rebuild the
  anonymous package. No manuscript or simulation source was changed.

## Recommended next tranche

Agree the narrower headline and the display promotion, then make one coherent
manuscript revision: explicit intellectual antecedents, exact-versus-approximate
boundary language, removal of the unsupported mean-shift explanation, a simpler
abstract, and consistent figure order. Retain the informative boundary departure.
The accepted data and simulation design can remain intact.

After that revision, run the sequential manuscript profiles, anonymous-output
checks, visual review of changed pages, and reviewer-package rebuild. Funding,
acknowledgements, archive choice, AI-use accuracy, and final declarations remain
the author-supplied submission facts in `docs/questions_for_human.md`. They are
separate from the scientific assessment above.
