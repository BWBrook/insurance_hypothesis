# Workflow – Result Review Cycle

This document specifies how the AI agent must interrogate its own results.  
The key idea: **code that runs is not enough**. Results must make ecological and mathematical sense.

## 1. When to use this workflow

The agent must apply this workflow whenever it:

- Implements or changes a simulation model or analysis pipeline.
- Produces a new **candidate main result**, such as:
  - a key figure,
  - a summary table,
  - a core statistic used to support/refute the hypothesis.

## 2. Step 1 – Sanity checks

### 2.1 Numerical sanity

For any new model or result, the agent must create and run **explicit checks**, such as:

- No `NaN`, `Inf`, or obviously divergent values under default parameter ranges.
- State variables (e.g. abundance, biomass) remain non-negative and within plausible bounds.
- Basic statistics converge reasonably as the number of simulation replicates increases.

These checks should be implemented as:

- Unit tests under `tests/`,
- or dedicated sanity-check scripts (e.g. `tests/sanity_*.py` or equivalent).

### 2.2 Ecological sanity

The agent must verify qualitatively sensible behaviour in:

- **Toy cases**:
  - small numbers of species (e.g. 2–3),
  - simple, low-variance environments,
  - straightforward parameter values.

Examples (to be instantiated by the agent):

- If all species have identical environmental responses, increasing variance should not magically create strong asynchrony.
- In the absence of environmental variation, the system should approach a predictable equilibrium or stationary distribution.

The agent must encode these expectations as tests where possible, not just prose.

## 3. Step 2 – Interpretation

For each candidate main result (e.g. figure or table), the agent must:

1. Save the artefact under:
   - `manuscript/figures/` (for figures), or
   - `analysis/reports/` (for exploratory output).
2. Add a section to `docs/interpretation_notes.md` with:
   - a short identifier (e.g. `FIG1_variance_vs_variability`),
   - a link or path to the artefact,
   - 2–5 bullet points describing:
     - what the result shows in plain language,
     - how it relates to the hypothesis,
     - any surprising or inconsistent patterns.

The agent should write these notes as if explaining the result to a human collaborator.

## 4. Step 3 – Iteration

Based on the interpretation notes, the agent must:

1. Maintain a list of **follow-up questions / tasks** directly under each result’s section in `docs/interpretation_notes.md`, for example:
   - “Check whether pattern holds with more species.”
   - “Test robustness to different synchrony metrics.”
   - “Re-run with longer time series to rule out transient effects.”

2. Convert these into concrete actions:
   - new simulation runs,
   - alternative analysis,
   - additional diagnostics.

3. When a follow-up is completed:
   - add a brief note under that item with what was done and what was learned,
   - if necessary, generate new artefacts and repeat the sanity + interpretation steps.

The agent should continue this cycle until:

- major contradictions are either resolved or clearly explained,
- and it can summarise the net conclusions in a short paragraph in `docs/interpretation_notes.md` under a “Summary” section.

## 5. Links to other documents

- `docs/plan.md` – must be updated to reflect any substantial change in model or experimental design.
- `docs/decisions.md` – must record major, irreversible modelling choices that arise from the iteration process.
- `docs/log/*.md` – should contain chronological notes about what was done and why.

The workflow in this document is **not optional**.  
If results appear “odd but interesting”, the correct response is **more iteration**, not acceptance without scrutiny.
