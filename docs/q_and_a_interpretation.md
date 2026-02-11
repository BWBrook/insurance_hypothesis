# Ecologist Q and A Interpretation Log

This is a living notebook for the ecologist-facing walkthrough of the repository.
It captures:

- your interpretation questions,
- my technical and ecological responses,
- any actions we decide to take,
- and follow-up status.

The goal is to keep a transparent record of human-in-the-loop sanity checks as we review results and presentation.

## How to use this file

For each question, we add one entry with:

1. `Q-ID` (sequential, e.g. `QA-001`).
2. `Context` (what file/figure/result prompted the question).
3. `Question` (your exact or near-exact wording).
4. `Response` (my answer).
5. `Decision / Action` (what we agreed to do).
6. `Status` (`open`, `answered`, `actioned`, `deferred`).
7. `Links` (paths to figures/files/commits, if relevant).

## Session metadata

- Start date: 2026-02-11
- Mode: ecologist-facing human-testing pass with technical chaperoning
- Scope: interpretation, sanity checks, display clarity, reproducibility UX

## Q and A entries

### QA-001

- Context: kickoff of ecologist-facing review workflow.
- Question: How will we capture interpretation questions and responses as we go?
- Response: Use this file as a timestamped running log with explicit status and action fields so decisions are auditable.
- Decision / Action: create and maintain `docs/q_and_a_interpretation.md` throughout walkthrough.
- Status: actioned
- Links: `docs/q_and_a_interpretation.md`

### QA-002

- Context: Figure 1 caption check against `manuscript/text/figure_captions_v2.md` and current Figure 1 panel file.
- Question: Are Figure 1 caption and figure congruent, and can we move to numbered figure filenames?
- Response:
  - Mostly congruent for panels A, B, and D.
  - One mismatch identified in panel C: caption states "points = replicates, lines = scenario means", but the prior plotting code showed only means.
  - Renaming to numbered figure filenames is straightforward and improves manuscript/pipeline consistency.
- Decision / Action:
  - Update Figure 1 generator so panel C overlays replicate points and mean lines.
  - Rename Figure 1 output target to `fig1_panels.png` (and `.pdf`) in `analysis/run_all.py`.
  - Keep checking later figures in sequence and apply `figN_` naming pattern as we go.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig1_panels.png`, `manuscript/figures/fig1_panels.png`, `manuscript/text/figure_captions_v2.md`

## Open action queue

- Continue sequential caption-vs-figure congruence checks for Figures 2-5, applying `figN_` filename prefixes and updating generation paths.

## Deferred topics

- None yet.
