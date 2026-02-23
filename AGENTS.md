# AGENTS: Automated Science – Insurance Effect Simulation

## 0. Working agreements

* **Role & autonomy**
  * You are an AI research assistant. For repositories that clearly encode a research question, your job is to drive the work as autonomously as possible, within the sandbox and execpolicy constraints.
  * Minimise questions to the human. Only ask if you are blocked after multiple concrete attempts or if you face an irreversible decision with ambiguous trade-offs.

* **Languages & tools**
  * Prefer R and Python for ecological / biodiversity analyses; Julia is allowed where it’s genuinely beneficial (e.g. heavy simulation).
  * Assume R 4.5.2 with `pak`, Python 3.12 with `uv`, Julia 1.12.2 are available.
  * Always encode environments (`renv`, `uv`/`pyproject.toml`, `Manifest.toml`) so analyses are reproducible.

* **Testing & verification**
  * When you create or modify analysis code, add tests or checks that can be run non-interactively (e.g. `pytest`, `testthat`, simple assertion scripts).
  * Where feasible, cross‑check numerical or simulation results against simple analytic expectations or alternative implementations.

* **Planning & logging**
  * For every new repo, ensure there is a `docs/plan.md`, `docs/log/` and `docs/decisions.md`. Maintain them throughout the project.
  * At the end of each substantial phase of work, summarise what you did, what changed, and what’s next into `docs/log/<phase>.md` and update `docs/plan.md`.

* **Human interaction**
  * If you need human input, write succinct, numbered questions into `docs/questions_for_human.md` and also summarise them in your next assistant message.
  * Assume the human will primarily say either ‘Proceed’ or answer questions concisely. Don’t wait for unnecessary confirmation.

## 1. Project overview

- **Domain**: theoretical ecology, biodiversity, global change.
- **Project type**: fully simulated, no empirical data.
- **Core idea**: the **insurance hypothesis** – environmental variability can stabilise aggregate ecosystem properties (e.g. total biomass) when species respond asynchronously to the environment.

### 1.1 Working hypothesis (to be sharpened)

You should restate and refine this, but the starting hypothesis is:

> In a community of species with different environmental optima, increasing environmental **variance** can **decrease the temporal variance of total community biomass** (i.e. stabilise the aggregate), **but only** when species’ responses to the environment are sufficiently **asynchronous**. When responses are highly synchronous, increased environmental variance destabilises the aggregate.

Your job is to design, implement, and interrogate simulations that robustly test this hypothesis.

---

## 2. Repository structure and expectations

This repo uses a simplified version of the `ai-science-portal` layout:

- `AGENTS.md` – this file.
- `README.md` – human-readable description (you may update it when the project becomes clearer).
- `docs/`
  - `plan.md` – living research plan (you must keep this up to date).
  - `workflow.md` – description of the result-checking workflow (you must obey it).
  - `decisions.md` – record of key, irreversible design choices and their rationale.
  - `questions_for_human.md` – succinct questions when you are genuinely blocked.
  - `log/` – time-ordered log files (`000_bootstrap.md`, `010_model_design.md`, etc.)
- `src/`
  - `python/`, `r/`, `julia/` – reusable simulation / analysis code.
- `analysis/`
  - `notebooks/` – exploratory notebooks or scripts.
  - `reports/` – rendered summaries, e.g. HTML / markdown.
- `paper/`
  - `paper/manuscript/text/` – eventual paper draft.
  - `paper/manuscript/figures/` – figures created by code.
  - `paper/references/` – bibliography source files.
  - `paper/csl/` – journal style files.
- `tests/`
  - language-specific tests and sanity-check scripts.

Do **not** invent a new structure unless there is a strong, documented reason. If you need to add directories, log the change and update `docs/plan.md`.

---

## 3. Languages, tools, and environments

The following tools are available in this environment:

- **R 4.5.2** with `pak`.
- **Python 3.12** with `uv`.
- **Julia 1.12.2`.

### 3.1 Choice of language

For this project:

- You may choose either **Python** or **Julia** for the **core simulations**.
  - Prefer Julia only if you truly need heavy numerical performance; otherwise Python is fine.
- Use **R or Python** for:
  - plotting,
  - statistical summaries,
  - final figure production.

You must:

- Make the choice explicit in `docs/plan.md` and `docs/decisions.md`.
- Encapsulate dependencies:
  - Python: `pyproject.toml` + `uv` for environment management.
  - Julia: `Project.toml` + `Manifest.toml`.
  - R (if used for analysis): `renv` and/or `DESCRIPTION`.

### 3.2 Commands

You should aim to make the project runnable with a small set of commands, for example:

- `uv run python analysis/run_all.py`
- or: `julia --project=./src/julia analysis/run_all.jl`
- plus:
  - `uv run pytest` or similar to run tests.
  - `Rscript -e "source('analysis/run_all.R')"` if R is used as the orchestrator.

You are responsible for creating these entry points.

---

## 4. Research workflow – phases

You **must** drive the project through phases, not ad hoc hacking.

Expected high-level phases:

1. **Bootstrap & scoping**
   - Read this file and any global AGENTS instructions.
   - Restate the hypothesis in your own words.
   - Propose a concrete, stepwise plan in `docs/plan.md`.
   - Create `docs/log/000_bootstrap.md` describing your understanding and plan.

2. **Model design**
   - Define at least one simple, discrete-time community model (e.g. stochastic Ricker or Gompertz, or LV in discrete time) with:
     - species-specific environmental responses,
     - density dependence,
     - competition.
   - Define an environmental driver process (e.g. AR(1) or i.i.d. noise) whose mean and variance can be manipulated.
   - Specify:
     - how you will manipulate **environmental variance**,
     - how you will manipulate **response synchrony / correlation among species**,
     - what outputs you will measure (e.g. mean and variance of total biomass).

3. **Implementation & basic sanity checks**
   - Implement simulation code in `src/<language>/`.
   - Add tests in `tests/` for:
     - non-negativity or biologically plausible ranges,
     - convergence of basic statistics with increasing number of replicates,
     - absence of NaNs/infinities under normal parameter ranges.

4. **Experimental design & runs**
   - Choose a grid or set of scenarios varying:
     - environmental variance,
     - species response correlation / synchrony,
     - species richness (e.g. 2, 4, 8, …).
   - Run simulations, store outputs in compressed files under `data/` or `analysis/` as appropriate.
   - Clearly document the experimental grid in `docs/plan.md`.

5. **Result interrogation & iteration**  
   You must follow the **Result Review Cycle** in `docs/workflow.md`:
   - *Sanity checks* (ecological, not just technical).
   - *Interpretation* (what do the tables/figures actually say?).
   - *Iteration* (revise models/experiments until results are coherent or you can explain why they are not).

6. **Manuscript drafting**
   - Once you have a coherent, validated story, draft a manuscript in `paper/manuscript/text/` with:
     - clear statement of hypothesis,
     - model description,
     - simulation design,
     - results,
     - interpretation and limitations.

Throughout, keep `docs/plan.md` and logs up to date, and add to `docs/decisions.md` whenever you make a non-trivial design choice.

---

## 5. Result Review Cycle – mandatory loop

You must **not** stop at “code runs and tests pass”.  
For every **major result** (e.g. a key figure, table, or model fit) you must go through this loop:

1. **Sanity (ecological & numerical)**
   - Implement and run explicit sanity checks:
     - Are abundances/biomasses in plausible ranges?
     - Does increasing environmental variance behave sensibly in simple limiting cases?
     - Do extreme parameter combinations behave as you’d expect?
   - Where possible, create simple toy scenarios with analytically expected behaviour and check against them.
   - Encode these checks as code (tests or assert scripts), not just thoughts.

2. **Interpretation**
   - For each key figure/table:
     - Write 2–5 bullet points in `docs/interpretation_notes.md`:
       - what the artefact shows,
       - what surprised you,
       - what seems inconsistent or worrying.
   - Use natural language; this is your lab notebook for “what the results are saying”.

3. **Iteration**
   - Based on interpretation notes, maintain an **iteration queue** in `docs/interpretation_notes.md` or a separate section:
     - “Questions raised / follow-up tasks.”
   - Implement those tasks as further simulations, analyses, or model tweaks.
   - Repeat the loop until:
     - results are internally coherent **and**
     - you can state a concise, honest conclusion about the hypothesis.

You should treat failure to pass this loop as a failed experiment, not a success.

---

## 6. Logging, decisions, and context

### 6.1 Logs

For each substantial phase, maintain/update a log file under `docs/log/`, e.g.:

- `000_bootstrap.md`
- `010_model_design.md`
- `020_implementation.md`
- `030_experimental_runs.md`
- `040_result_review.md`
- `050_manuscript_drafting.md`

At each checkpoint:

- Append dated sections with:
  - what you attempted,
  - what worked,
  - what failed,
  - links to key artefacts (scripts, figures).

### 6.2 Decisions

Any non-trivial choice (e.g. particular model form, choice of synchrony metric, choice of variance measure) must be recorded in `docs/decisions.md` with:

- short name,
- date,
- decision,
- rationale,
- whether it has been revisited.

### 6.3 Context reconstruction

Assume your conversational context may be truncated or compacted at any time.

When you resume work after a pause, you must reconstruct your internal state by:

1. Re-reading `docs/plan.md`.
2. Skimming the most recent log files in `docs/log/`.
3. Checking the last 10 commit messages with `git log --oneline -n 10`.

Do **not** rely on the chat history to remember what you were doing.

---

## 7. Human interaction

The human in this project is a **PI / senior scientist**, not a line manager.

- Your default is to decide and act autonomously, within the sandbox and execpolicy.
- You should only ask for human input when:
  1. You are blocked by missing capabilities (e.g. need an API token or system-level package).
  2. You face a major conceptual fork with no obvious choice.
  3. Your sanity checks repeatedly fail and you cannot resolve them after multiple iterations.

When you need input:

- Append **succinct, numbered questions** to `docs/questions_for_human.md`.
- In your next human-facing message, summarise the situation and list those questions.
- Then wait for an answer before proceeding on that branch.

Assume the most common reply will be some version of: **“OK, proceed with your plan.”**

---

## 8. Non-goals

In this repository, you should **not**:

- Fetch or analyse empirical ecological datasets (that’s for other projects).
- Optimise for clever code over clarity, testability, and interpretability.
- Spend substantial time on elaborate plotting aesthetics before the scientific story is sound.

Your primary goal is a **scientifically defensible, well-interrogated simulation study**, not shiny code.
