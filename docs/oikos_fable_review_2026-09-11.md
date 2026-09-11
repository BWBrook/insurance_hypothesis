# Fresh textual review for Oikos submission (Fable)

Reviewed 11 September 2026 at commit `ee75ab4`, after Astra's 10 September
assessment and the bounded revision it prompted. Scope: text only (clarity,
readability, scientific robustness of claims). No simulations were run, no
production outputs touched, no manuscript source edited. Numerical claims were
checked against `analysis/reports/*_summary.csv` and Fig. 1 as rendered.

**Verdict: not yet co-author ready. One more bounded text pass is needed.**
The evidence base is sound and the argument is honest. But the manuscript
describes the accuracy of its own analytical benchmark in words that its own
Figure 1B contradicts, and the Methods carry enough duplication and loose
terminology that an Oikos reviewer will spend effort on bookkeeping rather than
on the result. Both are fixable in prose. Neither needs a new run.

**Where I disagree with Astra.** Astra (docs/oikos_astra_review_2026-09-10.md,
§2) framed the benchmark problem as one near-boundary point (A = 0.247) where
the first-order criterion predicts weak buffering and the simulation shows weak
amplification, and called it "small but resolved". The revision adopted that
framing (draft_ms_v2.md lines 224, 250, 280; abstract line 5; cover letter;
significance statement). I think this understates the issue and points a
reviewer at the wrong number. See S1 below. I agree with Astra on the display
order, the antecedent literature, and the removal of the mean-shift explanation.

Line numbers refer to `paper/manuscript/text/draft_ms_v2.md`.

## Scientific robustness

### S1. The benchmark's quantitative failure is largest at A = 0, and the text does not say so

Figure 1B plots the first-order benchmark (1 - rho_eff) + rho_eff S A as a
dotted line running from 0 at A = 0 to 3.2 at A = 0.8. The simulated ratio
runs from 0.32 to 2.99. The departures are systematic across the whole path,
not confined to the boundary:

| Path | A | Benchmark | Simulated | Difference |
| --- | ---: | ---: | ---: | ---: |
| rotation | 0.000 | 0.000 | 0.320 | +0.32 |
| rotation | 0.117 | 0.469 | 0.666 | +0.20 |
| rotation | 0.247 | 0.988 | 1.043 | +0.06 |
| rotation | 0.400 | 1.600 | 1.489 | -0.11 |
| rotation | 0.800 | 3.200 | 2.992 | -0.21 |
| abundance | 0.022 | 0.089 | 0.375 | +0.29 |
| abundance | 0.230 | 0.919 | 0.964 | +0.05 |
| abundance | 0.257 | 1.030 | 1.053 | +0.02 |

(Source: `analysis/reports/fig4_weighted_balance_boundary_summary.csv`,
columns `predicted_forcing_ratio` and `cv2_ratio`.)

The benchmark predicts that perfect first-order cancellation removes
essentially all aggregate variance at rho_eff near 1. The simulation retains
about a third of the independent-exposure squared CV. That is the largest
disagreement in the figure, and it is the number a theoretician will look at
first. The current text (line 224) calls the criterion a predictor of "the
broad gradient, but not the exact nonlinear boundary", and the abstract speaks
of "a small but resolved departure in the nonlinear response experiment". A
reader who then looks at Fig. 1B will see a dotted line that misses the data
by 0.3 at the origin and conclude the text is selective.

The pattern has a simple explanation that the paper already has the machinery
for. The benchmark is a first-order (linear) result. Second-order terms in the
Ricker map transmit contrast-mode variance into total abundance even when the
linear projection cancels exactly. Under equicorrelation the contrast modes
lose variance as rho_eff rises but never vanish for the balanced vector's
nonlinear image, and they decay slowly (lambda_d = 0.63 at S = 4; see S3).
A residual that does not cancel would compress the ratio towards 1 from both
sides, which is what the table shows: positive departures below the boundary,
negative above. A check with a single rho-invariant additive residual fitted
at A = 0 reproduces the whole abundance-weight path to within 0.02 and the
rotation path below the boundary to within 0.05, but underpredicts the aligned
side (2.50 versus 2.99 at A = 0.8), so the residual itself grows when the
linear forcing is large. I report this as a diagnostic reading of existing
numbers, not as a result to add.

Recommended wording changes (no new analysis):

- Abstract, line 5: replace "with a small but resolved departure in the
  nonlinear response experiment" with a sentence that states the two facts a
  reader needs: the benchmark predicts the direction and ordering of the
  correlation effect, and it over-predicts the strength of buffering when
  first-order cancellation is complete. For example: "Nonlinear population
  dynamics retained about a third of the independent-exposure variability
  even when first-order cancellation was complete, so the benchmark predicts
  direction and ordering rather than magnitude."
- Results, line 224: lead with the A = 0 comparison (predicted near 0,
  observed 0.32), then the compression pattern, then the boundary point as
  the consequence of that pattern. Delete "small".
- Discussion, line 250: "The nonlinear boundary is therefore approximate"
  should become a statement of what the benchmark does and does not predict,
  with the second-order mechanism named in one sentence.
- Conclusion, line 280, cover letter, and significance statement: drop
  "small resolved departure at the closest tested point". It is the least
  informative departure in the figure.

This also changes the intellectual claim slightly and, I think, for the
better: the paper shows that a covariance criterion classifies exposure
correlation as buffering or amplifying, and simultaneously shows how much of
the nominal buffering nonlinear feedback takes back. That second half is
currently buried.

### S2. The Monte Carlo paragraph reports no uncertainty

Line 206 says Monte Carlo uncertainty is "small relative to the contrasts"
and then gives two means with no standard error, standard deviation, or
interval. The replicate standard deviation of CV_tot for the balanced S = 4,
sigma_env = 0.5, rho_eff = 0.5 cell is 0.0045
(`fig1_panels_summary.csv`, `cv_total_sd`), giving a standard error of the
mean of about 0.00014 over 1000 replicates. State that, or state the
replicate SD, in this paragraph. Without it the sentence is an assertion.

Related: Results line 220 reports CV to four significant figures (0.1064,
0.0840, 0.1489, 0.0595, 0.1841) while the abstract uses three. Use three
throughout unless a fourth is needed to separate two values. "0.1064 and
0.1064" should read "both 0.106", with the explanation that the two
treatments have identical marginal forcing distributions at rho_eff = 0, so
equality is expected, not a coincidence.

### S3. The contrast-mode eigenvalue is introduced and never used

Lines 132 to 136 derive lambda_d = 1 - r0 (1 - alpha_inter) / (1 +
alpha_inter (S - 1)) and then use only lambda_c to motivate the r0
sensitivity. Either delete lambda_d or put it to work in S1: at S = 4,
alpha_inter = 0.3, r0 = 1 it equals 0.63, so contrast-mode fluctuations have
substantial memory while the common mode has none. That asymmetry is why
contrast-mode variance is available to leak into the total through
nonlinearity, and why the balanced ratio rises to 0.66 at r0 = 0.25 (Fig. 1C)
as the common mode acquires memory too. One sentence would connect three
panels.

### S4. Four names for three response treatments

The manuscript uses "mixed", "balanced", "balanced mixed", "positive",
"positive slopes", "aligned", "aligned positive", "positive-matched",
"magnitude-matched aligned", "broader positive-slope treatment", and
"steeper positive-slope treatment". Table 1 uses "Aligned positive" and
"Magnitude-matched aligned"; Methods line 47 to 51 uses "Mixed", "Positive",
"Positive-matched"; Figure 1 legend uses "balanced mixed" and "aligned,
matched magnitude". A reviewer will lose track of which control is which.

Pick one name per treatment, define it once at line 47, and use it in Table 1,
every caption, and every legend. Suggested: **balanced** (signs mixed, sum
zero), **aligned-matched** (same magnitudes, all positive), **aligned-steep**
(slopes 0.1 to 1.0). Any consistent trio will do. This is the single
highest-value readability fix in the paper.

### S5. Duplicated passages

- The operational definition of insurance appears at line 25 and again,
  nearly verbatim, at line 202. Keep the Methods version and cut line 25 to
  one sentence.
- Floor occupancy is summarised twice in consecutive paragraphs (lines 212
  and 214) with overlapping content. Merge.
- The simulation size (1000 replicates, 600 steps, 300 burn-in) is stated at
  line 116, repeated in the Table 1 legend, and repeated again with symbols
  at line 140. State once.
- Line 252 says the control "isolates" in two consecutive sentences with the
  same object. Cut one.

### S6. Introduction paragraph order

Paragraph 4 (line 19) ends with "The aim is to identify when this explicit
benchmark remains informative and where population dynamics produce departures
from it." That sentence reads as the end of the Introduction. Paragraph 5
(line 21) then returns to empirical synchrony studies, followed by the model
description and hypothesis. Move paragraph 5 before paragraph 4, so the
sequence runs: insurance concept; synchrony as the pathway; response diversity;
what empirical studies show and do not explain; what theory already provides
and what this paper adds; the model; the hypothesis.

### S7. Title

"Abundance-weighted responses shape community buffering under correlated
environments" is accurate but "shape" carries no information. The paper has a
sharper claim: whether correlated environments buffer or amplify depends on
abundance-weighted response balance. A title that states the contingency
would serve a scanning reader better, for example "Abundance-weighted response
balance determines whether correlated environments buffer or amplify community
variability". This is a preference, not a defect; Astra proposed the current
title and Barry accepted it.

### S8. Points I checked and found sound

- All 25 cited references resolve. The five 2025 to 2026 entries (Danet 2025;
  Hsieh, Sasaki, Ross, Song 2026) resolve on Crossref with matching titles,
  journals and first authors; Kunze et al. 2026 was confirmed against the
  Wiley full-text page. No hallucinated references.
- The lambda_d formula, the equal-K equilibrium, the constant total of 210.53
  along the K path, the endpoint alignment indices (0 and 0.8), and the
  benchmark ratio formula are correct.
- The Loreau and de Mazancourt index is bounded in [0, 1] by construction, so
  the clipping at line 181 is a floating-point guard. Say "in exact
  arithmetic phi_LdM lies in [0,1]; clipping removes rounding overshoot" so a
  reader does not suspect the metric can exceed one.
- Abstract is 215 words, under the 300-word limit, with no unexplained
  abbreviations. Page 1 carries title and abstract; Introduction starts on
  page 2. Main text is anonymous.
- The unpaired-realisation design (line 146) is fine at 1000 replicates and
  is disclosed.

## Line-level edits

- Line 33: "per-capita growth follows" introduces an equation for abundance,
  not per-capita growth. Say "abundance follows".
- Line 47: "Three named regimes are used" then defines them as bullet points
  with inconsistent naming (see S4).
- Line 68: "with small epsilon" should give the value, 10^-6 (from
  `model.py`), because the near-1 endpoint is central to Fig. 1B.
- Line 78: "all species share phi and the requested rho_env but receive
  correlated trajectories" has a stray "but". The trajectories being
  correlated is the point, not a contrast.
- Line 179 to 181: v_i is used before it is defined; define v_i and sigma_i
  together.
- Line 185: N_i is already floored at N_min, so adding N_min inside the log
  is a second guard. Either say so or drop it from the displayed formula.
- Line 187: the bold phrase mid-paragraph is a stylistic outlier in the
  Methods. Use plain text.
- Line 228: "common-mode superstable point" is jargon. "the point at which
  the common mode has no memory (lambda_c = 0)" says the same thing.
- Line 232: "approximately -0.81 for S=2" is the perfectly opposed two-species
  case; say so, since it explains why the S = 2 value is so extreme.
- Line 240: the S = 4 value "approximately 0.08" and the Fig. 1 value 0.084
  are the same parameter cell from different grids. One clause noting the
  agreement would reassure a reviewer checking consistency.
- Line 284, AI statement: Oikos requires disclosure of LLM use. If any of
  this review is adopted, the statement must name Anthropic Claude as well as
  OpenAI Codex. As written it would be inaccurate after revision.
- Cover letter, paragraph 3: name Ross et al. 2026 explicitly when invoking
  the Oikos response-diversity agenda. It is the hook for the handling editor.
- Figure 1 caption: "the dotted line is the first-order forcing benchmark,
  which approximates the nonlinear transition" should be revised in line with
  S1: it predicts direction and ordering; it over-predicts buffering below
  the boundary and amplification above it.

## Compliance notes

Checked against the NSO author guidelines on 11 September 2026: abstract under
300 words with no references or unexplained abbreviations; anonymous main
text; Data Availability, Significance, AI-use, Conflict and Ethics statements
prepared. In-text citations must be chronological within parentheses; the
current source mixes orders (for example line 13 cites 2013, 2013, 2021, then
2007, 2021). Confirm the makedoc CSL sorts citations chronologically, or fix
by hand. No word limit is stated for Research papers.

## What this review did not do

No production or diagnostic code was run. No PDF was rebuilt; the 11 September
build in `build/oikos_submission_aug_2026/` was taken as current. Full text of
the Nature Communications and Oikos 2026 references was not retrieved
(paywalled); their metadata was verified through Crossref. The August external
review was read for structure only.

## Recommended next tranche

One coherent text pass, in this order: (1) rewrite the benchmark-accuracy
sentences per S1 in abstract, Results, Discussion, Conclusion, Figure 1
caption, cover letter and significance statement; (2) unify treatment names
per S4; (3) remove the duplications in S5 and reorder the Introduction per
S6; (4) add the Monte Carlo standard error and settle on three significant
figures; (5) update the AI statement. Then rebuild the six makedoc profiles
and the anonymous package. After that pass the manuscript is ready for
co-authors.

## Editorial pass applied (Fable, 11 September 2026, later the same day)

Barry asked for the recommendations above to be applied directly, for
Barry and Astra to check. All edits are uncommitted in the working tree;
`git diff` against `ee75ab4` shows them. No simulation, figure, or table
data changed. Files touched: the main text, the four caption/figure-block
files, the three table files, Supporting information (title only), title
page, cover letter, submission-form statements, and the golden contract.

What changed, by review item:

- **S1.** Abstract, Results, Discussion, Conclusion, Figure 1 caption, cover
  letter and significance statement now lead with the A = 0 comparison
  (benchmark near 0, simulated 0.32), describe the compression pattern, and
  state the second-order contrast-mode mechanism. The phrase "small but
  resolved departure" is gone everywhere.
- **S2.** Monte Carlo paragraph reports the replicate SD (0.0045) and SE
  (0.00014). CV values are given to three decimal places throughout.
- **S3.** lambda_d is now used: numerical values at the default parameters
  are given in Methods, and the Discussion uses the two eigenvalues to
  explain the residual and the r0 pattern in Fig. 1C.
- **S4.** Treatments are named **mixed**, **matched aligned** and **steep
  aligned** in text, Table 1, all captions and Table S1/S2, with one Methods
  sentence mapping these to the legend and production labels ("mixed",
  "positive matched", "aligned"/"aligned positive"). Rendered legends are
  unchanged.
- **S5.** Duplicated insurance definition, floor paragraphs and simulation
  size removed; "isolates" repetition removed.
- **S6.** Introduction reordered: empirical paragraph now precedes the
  theory-and-gap paragraph, and the gap paragraph names the two elements
  this paper makes explicit (common orientation; abundance weighting).
- **S7.** Title changed to "Abundance-weighted response balance determines
  whether environmental correlation buffers or amplifies community
  variability" in all five places it appears, and the golden contract's
  required-text fragments were updated to match. Revert with a single
  search-and-replace if Barry prefers the previous title.
- **Plain-language bridges** for the ecologist reader: one-sentence readings
  after the Var(F) derivative and the alignment index; common and contrast
  modes defined in words where first used in Methods and Discussion; CV
  defined at first use in the Introduction.
- **AI statement** now names Anthropic Claude alongside OpenAI Codex.
- **Compliance.** The CSL sorts parenthetical citations chronologically, so
  the citation-order item needs no manual fix. Abstract is 256 words.

Points for Astra and Barry to check in particular:

1. The mechanistic sentence in the Discussion attributing the residual to
   second-order transmission of contrast-mode variance through the convex
   exponential is my interpretation of the pattern, not a tested result. It
   is hedged in Methods ("can be transmitted") but stated more directly in
   the Discussion. If Astra's Lyapunov calculation or a quick second-order
   expansion contradicts it, soften or remove that sentence; the empirical
   statements about the 0.32 residual and the compression stand regardless.
2. The claim that weaker buffering at low r0 in Fig. 1C is "consistent with
   the same residual growing as the common mode acquires memory" is likewise
   an interpretation, and is hedged as such.
3. The title change is a preference call that Barry had previously settled
   the other way with Astra.
