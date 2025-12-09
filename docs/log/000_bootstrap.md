# 000_bootstrap log

- Date/time (UTC): _[fill in]_ 
- Context: _[current understanding of question and scope]_ 
- Actions taken:
  - _[step]_ 
- Key findings/decisions (link to `docs/decisions.md`):
  - _[item]_ 
- Files touched / artefacts created: _[paths]_ 
- Next steps (also update `docs/plan.md`):
  - _[item]_ 

Keep entries chronological; append rather than overwrite.

---

# Example:

# Log 000 – Bootstrap and scoping

> Maintained by the AI agent. This file records the initial understanding and plan.

## 1. Timestamp and environment

- **First created**: _TO BE FILLED BY AGENT (UTC timestamp)_
- **Agent**: Codex CLI with GPT-5.1-codex-max
- **Languages considered**: Python 3.12, Julia 1.12.2, R 4.5.2

## 2. Initial understanding of the project

_The agent should summarise in its own words:_

- The research hypothesis.
- The meaning of “stabilisation” and “asynchrony”.
- Why simulations are appropriate.

## 3. Proposed model framework

_The agent should outline here the model(s) it intends to use, before implementing them._

- Candidate model type(s).
- Environmental process.
- How species differences and correlations will be represented.

## 4. Proposed experimental grid

_Initial sketch of the parameter space to explore._

- Environmental variance levels.
- Synchrony / correlation scenarios.
- Species richness levels.
- Number of replicates and time steps.

## 5. Planned validation strategy

_Summary – details will go into `docs/plan.md` and `docs/workflow.md`._

- Toy scenarios and expected behaviour.
- Numerical sanity checks.
- Cross-checks or alternative implementations.

## 6. Immediate next actions

_The agent should list 3–7 specific tasks._

Examples (to overwrite):

1. Restate and refine hypothesis and definitions in `docs/plan.md`.
2. Decide on language (Python vs Julia) and record decision in `docs/decisions.md`.
3. Implement a minimal version of the chosen model with a two-species toy case.
4. Add first numerical and ecological sanity tests for the toy case.
5. Run initial simulations for a small subset of scenarios and generate a preliminary figure.
