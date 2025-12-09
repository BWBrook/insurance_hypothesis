# Project Plan (living document) – Insurance Effect Simulation

> This file is maintained by the AI agent. It should always reflect the current understanding of the project and the next concrete steps.

## 1. Working hypothesis

_Initial stub – the agent should overwrite this with its own wording and refinement._

- Starting point:
  - In multispecies communities with differing environmental responses, increased environmental variance may stabilise total community biomass when species respond asynchronously, but destabilise it when responses are synchronous.

The agent must:
- Clarify what “stabilise” means (e.g. reduced variance or coefficient of variation of total biomass).
- Clarify what “asynchronous responses” means (e.g. correlation structure of species’ environmental response).

## 2. Model design

_The agent should fill this in with specifics._

- Core model type (e.g. stochastic Ricker / Gompertz / LV).
- Environmental driver process (e.g. AR(1) with tunable variance).
- Species parameters:
  - number of species,
  - environmental optima / niches,
  - competition structure.

## 3. Experimental grid

_Describe the set of simulation scenarios._

- Axes to vary:
  - environmental variance,
  - synchrony / correlation among species responses,
  - number of species.
- Values or ranges for each axis.
- Number of replicates per scenario.
- Length of time series (burn-in + observed).

## 4. Response metrics

_List the main metrics to compute from simulations._

- For each scenario:
  - mean and variance (or CV) of total biomass,
  - species-level variances,
  - temporal β-diversity or turnover metrics (if used),
  - synchrony indices.

## 5. Sanity checks and validation

_This section should summarise the key sanity and validation strategies._

- Toy analytic cases (e.g. 2 species, simple environment) and expected behaviour.
- Numerical invariants (non-negativity, boundedness conditions, etc.).
- Cross-validation or alternative implementations (e.g. same model in two languages, or two independent implementations).

## 6. Result Review Cycle

_Short summary pointing to `docs/workflow.md`._

- Sequence of:
  - sanity checks,
  - interpretation notes,
  - iterations,
  - convergence criteria (when to stop iterating).

## 7. Manuscript plan

_Outline the eventual paper structure._

- Target journal type (theoretical ecology / ecology letters–style short communication, etc.).
- Draft section outlines:
  - Introduction,
  - Methods,
  - Results,
  - Discussion.

## 8. Current status and next steps

_The agent must keep this up to date._

- **Current phase**:
- **Recently completed**:
- **Immediate next steps** (ordered list of small, concrete tasks):
  1.
  2.
  3.

---

## Example template (dispose, use, modify as you see fit)

## Research question & scope
- Question: _[fill in]_
- System / focal taxa / region: _[fill in]_
- Hypotheses to test: _[bullet list]_ 

## Data sources
- Primary datasets (with URLs, versions, expected size):
  - _[fill in]_ 
- Supplementary covariates / metadata: _[fill in]_ 
- Access constraints / licenses: _[fill in]_ 

## Analysis plan (outline)
| Phase                    | Goal                                | Key actions | Owner | Status  |
| ------------------------ | ----------------------------------- | ----------- | ----- | ------- |
| 000_bootstrap            | Define question, scope, plan        | _[fill in]_ | Codex | pending |
| 010_data_acquisition     | Acquire & document data             | _[fill in]_ | Codex | pending |
| 020_exploratory_analysis | EDA & feature engineering           | _[fill in]_ | Codex | pending |
| 030_modelling            | Fit models, diagnostics, robustness | _[fill in]_ | Codex | pending |
| 040_reporting            | Figures, tables, manuscript draft   | _[fill in]_ | Codex | pending |
| 050_release              | Repro checks, packaging, archive    | _[fill in]_ | Codex | pending |

## Milestones & deliverables
- M1: _[e.g., cleaned dataset ready]_ — target date: _[date]_
- M2: _[e.g., preliminary figures]_ — target date: _[date]_
- M3: _[e.g., validated model results]_ — target date: _[date]_
- M4: _[e.g., manuscript draft]_ — target date: _[date]_

## Risks, assumptions, and contingencies
- Data availability risks: _[fill in]_ 
- Methodological risks: _[fill in]_ 
- Operational risks (compute, runtime): _[fill in]_ 
- Contingency ideas: _[fill in]_ 

## Next actions (short horizon)
- [ ] _[next concrete task]_ 
- [ ] _[next concrete task]_ 
- [ ] _[next concrete task]_ 

_Update this file whenever plans change; keep it succinct and current._

