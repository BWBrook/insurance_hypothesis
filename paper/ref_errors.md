# Reference Conversion Errors / Follow-up Items

Date: 2026-02-23
Source manuscript: `paper/manuscript/text/draft_ms_v2.md`
Bibliography checked: `paper/references/ih_references.yaml`

## Summary

- Manual author-year citations converted to Pandoc cite tokens where a clear bibliography match existed.
- Second-pass placeholder resolution completed: all `[REF]` markers in the manuscript body were replaced with best-match cite tokens.
- Distinct citekeys now used in manuscript: `19`.
- Unmatched citekeys introduced by conversion: `0`.
- Remaining unresolved citation-related items: `2` total (both are unmatched bibliography entries for one source).

## Missing / Unmatched bibliography entries

1. **`Wagg et al. 2022`**
   - Status: No disambiguated entry found in `paper/references/ih_references.yaml`.
   - Occurrences:
     - `paper/manuscript/text/draft_ms_v2.md:20`
     - `paper/manuscript/text/draft_ms_v2.md:26`
   - Notes:
     - Nearby citations in each sentence were converted to citekeys.
     - `Wagg et al. 2022` remains plain text until a matching bibliography record is added.

## Second-pass `[REF]` resolution notes

The following placeholders were resolved using best-match references from available titles/abstracts:

1. `paper/manuscript/text/draft_ms_v2.md:217`
   - Added: `[@thibaut2013UnderstandingDiversityStability; @loreau2008SpeciesSynchronyIts]`
2. `paper/manuscript/text/draft_ms_v2.md:231` (first)
   - Added: `[@ross2023HowMeasureResponse; @polazzo2024MeasuringResponseDiversity]`
3. `paper/manuscript/text/draft_ms_v2.md:231` (second)
   - Added: `[@polazzo2024MeasuringResponseDiversity]`
4. `paper/manuscript/text/draft_ms_v2.md:243`
   - Added: `[@loreau2021BiodiversityInsuranceConcept]`
5. `paper/manuscript/text/draft_ms_v2.md:251`
   - Added: `[@ives2007StabilityDiversityEcosystems; @shanafelt2015BiodiversityProductivitySpatial]`
6. `paper/manuscript/text/draft_ms_v2.md:255`
   - Added: `[@valencia2020SynchronyMattersMore]`

## Disambiguation notes

- No unresolved same-author same-year ambiguity remained after matching.
- For `2013` citations involving Loreau/de Mazancourt, the following were resolved distinctly:
  - `@loreau2013BiodiversityEcosystemStability` for “Loreau and de Mazancourt 2013”.
  - `@demazancourt2013PredictingEcosystemStability` for “de Mazancourt et al. 2013”.
