# Literature and claims audit: ordering integration

## Integration disposition, 19 October 2026

The parent integration applied all six claim corrections below and removed the
broad priority claim. Gouhier et al. (2010) is now cited in the Introduction;
Shibasaki et al. remains search context rather than an added citation. The
climate statement is restricted to heterogeneous changes in temperature
variance, the Adler comparison is a rough benchmark conditioned on competitive
pairs, and the remaining empirical and theoretical citations have the scope
specified in this review. The review below records the pre-correction findings.
It was performed independently using primary sources and Crossref; this file
preserves that review and the disposition, not a new systematic literature review.

## Scientific decision

The manuscript asks whether changing only exposure correlation, from independent
to near-perfectly shared, can increase temporal variability of total abundance in
a competitive community whose direct environmental responses are perfectly
balanced. The estimand is the shared-to-independent ratio of mean replicate
squared community CV, not the generic association between response diversity and
stability. The literature question is therefore whether the exact within-community
reversal, with opposing responses held fixed, has been reported previously.

**Recommendation: approve with changes.** Remove the broad “to my knowledge it
has not been reported” sentence. The exact design still appears distinct in this
bounded search, but prior work is close enough that an uncaveated novelty claim is
risky. Gouhier, Guichard and Gonzalez (2010) already showed that correlated
environmental noise can either stabilise or destabilise nonlinear food-web
metacommunities as noise strength and dispersal change, including disruption of
compensatory dynamics at strong noise. A 2026 preprint by Shibasaki et al. states
explicitly that response diversity can stabilise or destabilise community dynamics,
although it obtains that result by changing the fraction of identically responsive
sensitive versus insensitive species rather than by comparing shared and
independent exposure in a balanced opposing-response community.

Suggested connection in the Introduction or Discussion:

> Correlated environmental noise can also stabilise or destabilise nonlinear
> food-web metacommunities depending on noise strength and dispersal
> [@gouhier2010SynchronyStabilityFood]. Here I isolate a different contrast:
> shared versus independent exposure within the same perfectly balanced
> competitive community.

Primary source: [Gouhier et al. 2010](https://doi.org/10.1086/649579). The
[Shibasaki et al. 2026 preprint](https://doi.org/10.64898/2026.08.11.743952)
is useful novelty-search context but need not be added to the paper once the broad
novelty sentence is removed; its mechanism and estimand differ, and Kunze et al.
already support the more general point that response diversity alone does not
determine stability.

## Material claim and citation findings

### MAJOR — climate-variance wording exceeds Vasseur et al. (2014)

At lines 21 and 178, the manuscript turns a spatially heterogeneous projection
about temperature distributions into a general increase in “environmental
variability”, and line 21 additionally says extremes will become more frequent
and severe. Vasseur et al. analyse thermal performance curves and temperature
distributions; they report that projected changes in variance are spatially
heterogeneous and that changes in mean and standard deviation interact to explain
performance. They do not support a universal increase in environmental variance,
nor a general claim covering all environmental drivers.

Replace line 21 with:

> The question is practical as well as theoretical: projected temperature
> distributions can change in variance and skewness as well as mean, and those
> changes can materially alter species performance
> [@vasseur2014IncreasedTemperatureVariation].

Replace the start of the line-178 inference with:

> Projected changes in temperature variance are spatially heterogeneous, but
> where variance increases, communities that now gain stability from shared
> environments may gain less [@vasseur2014IncreasedTemperatureVariation].

Primary source: [Vasseur et al. 2014](https://doi.org/10.1098/rspb.2013.2612).

### MAJOR — Adler et al. is a rough benchmark, not direct parameter validation

Line 172 accurately recalls the reported mean four- to five-fold excess, but
“typical of plant communities” omits the study's conditioning and makes the
comparison sound more direct than it is. Adler et al. screened 39 studies of
terrestrial plant communities. The four- to five-fold mean applies to the 67% of
species pairs for which both estimated effects were negative. Their synthesis
concerns heterogeneous phenomenological interaction estimates, not the symmetric
Ricker coefficient $\alpha$.

A defensible replacement is:

> Values of $\alpha=0.45$–$0.6$ imply stronger relative interspecific
> competition than the mean four- to five-fold intraspecific excess reported for
> terrestrial plant species pairs in which both effects were competitive
> [@adler2018CompetitionCoexistencePlant], whereas $\alpha=0.2$ gives the same
> 5:1 coefficient ratio. This is only a rough ecological benchmark because the
> synthesis estimated phenomenological interaction effects rather than this
> model's symmetric $\alpha$.

Also replace “In this model they are not extreme” with the directly supported
claim “Within the tested grid, reversal was not confined to the largest
competition or autocorrelation values.” Adler et al. does not establish the
ecological plausibility of the manuscript's environmental-effect SDs.

Primary source: [Adler et al. 2018](https://doi.org/10.1111/ele.13098).

### MINOR — Vasseur and Yodzis (2004) supports coloured noise with qualifications

Line 172 says positive autocorrelation is common in environmental time series.
The cited survey found strong habitat and latitude structure: terrestrial series
tended towards white noise, whereas marine series tended towards red or brown
noise; most spectra also flattened at low frequencies. Use:

> Positive autocorrelation, which prolongs compositional departures, occurs in
> many environmental series, especially marine ones, although noise colour
> varies with habitat and latitude [@vasseur2004ColorEnvironmentalNoise].

Primary source: [Vasseur and Yodzis 2004](https://doi.org/10.1890/02-3122).

### MINOR — Houlahan et al. is one multi-community synthesis

Line 174 says “Empirical surveys find compensatory dynamics less often than
synchronous ones.” Houlahan et al. assessed community covariance in 41 natural
communities across taxa and spatial scales. Negative average covariance is a
necessary signature of strong compensation in their framing, but their analysis
does not identify every compensatory process. Use:

> In a synthesis of 41 natural communities, species tended to covary positively
> rather than negatively [@houlahan2007CompensatoryDynamicsAre]; the present
> results add that, where negative covariance does occur, it is not evidence that
> increasing exposure correlation stabilises the community.

Primary source: [Houlahan et al. 2007](https://doi.org/10.1073/pnas.0603798104).

### MINOR — Kunze et al. is related, not parallel in its estimand

Kunze et al. study resistance and recovery after pulse disturbances, using
Lotka–Volterra simulations and a meta-analysis, rather than temporal CV under
recurrent forcing. They found that mean response consistently predicted community
stability, while response dissimilarity and divergence were associated with
stability only without interspecific interactions. “Parallel conclusion” is a
little too strong. Use:

> A related result for pulse disturbances was that response-diversity metrics
> were associated with community stability only without interspecific
> interactions, whereas mean response remained predictive
> [@kunze2026SpeciesInteractionsDetermine]. Although the disturbance regime and
> stability metric differ, both results show that response diversity alone is
> insufficient.

Primary source: [Kunze et al. 2026](https://doi.org/10.1111/ele.70299).

### MINOR — Ruel and Ayres does not support “usually invoked”

Ruel and Ayres explain how Jensen's inequality predicts effects of environmental
variance on mean biological performance under nonlinear response functions. The
paper does not quantify how nonlinear averaging is “usually” invoked. Use:

> Ruel and Ayres used Jensen's inequality to show how environmental variance can
> shift mean biological performance under nonlinear response functions
> [@ruel1999JensensInequalityPredicts]; the second-order input here instead has
> zero temporal mean and transfers variability from community composition to the
> total.

Primary source: [Ruel and Ayres 1999](https://doi.org/10.1016/S0169-5347(99)01664-X).

## Bibliographic checks

The five entries added since `d6adc5c` are all cited in the manuscript and their
DOIs, titles, authors, journal, volume, issue and pages match Crossref and publisher
records:

- `houlahan2007CompensatoryDynamicsAre` — 10.1073/pnas.0603798104;
- `adler2018CompetitionCoexistencePlant` — 10.1111/ele.13098;
- `vasseur2004ColorEnvironmentalNoise` — 10.1890/02-3122;
- `vasseur2014IncreasedTemperatureVariation` — 10.1098/rspb.2013.2612; and
- `ruel1999JensensInequalityPredicts` — 10.1016/S0169-5347(99)01664-X.

The Kunze title-only edit is accurate. Wiley lists first publication on 31
December 2025 but cites the article as 2026, volume 29, issue 1, e70299, so the
repository's 2026 bibliographic year is appropriate. No newly added entry is
unused. The broader bibliography contains unused entries, but that predates and
falls outside this bounded audit.

Verified CSL-YAML for the recommended closest-prior-art citation:

```yaml
- id: gouhier2010SynchronyStabilityFood
  accessed:
    - year: 2026
      month: 10
      day: 19
  author:
    - family: Gouhier
      given: Tarik C.
    - family: Guichard
      given: Frédéric
    - family: Gonzalez
      given: Andrew
  citation-key: gouhier2010SynchronyStabilityFood
  container-title: The American Naturalist
  container-title-short: The American Naturalist
  DOI: 10.1086/649579
  ISSN: 0003-0147, 1537-5323
  issue: '2'
  issued:
    - year: 2010
      month: 2
  language: en
  page: E16–E34
  source: Crossref
  title: Synchrony and stability of food webs in metacommunities
  type: article-journal
  URL: https://doi.org/10.1086/649579
  volume: '175'
```

## Checks and limits

I compared `d6adc5c..d4352cf` for the manuscript and reference database, read the
claim-bearing passages in context, checked the five added references plus Kunze
against Crossref and publisher records, and read primary-source abstracts or full
text for all six. The novelty search used targeted combinations of shared/correlated
environment, compensation, balanced/opposing response, nonlinear dynamics,
Ricker, response diversity and destabilisation. It identified Gouhier et al.
(2010), Polazzo et al. (2025) and Shibasaki et al. (2026) as the closest conceptual
neighbours; Polazzo et al. experimentally supports the stabilising expectation for
balanced responses rather than the reported reversal.

This was deliberately not an exhaustive systematic review. The absence of an
exact match supports describing the comparison as distinct, but not claiming
priority. Literature cannot validate whether the simulated parameter combinations
occur in nature; the manuscript correctly states that the model does not estimate
their frequency.
