# AGENTS: Insurance hypothesis simulation and Oikos paper

This is a mature scientific repository in final revision. Treat the manuscript,
seven production summaries, numerical results, and accepted display suite as a
coherent research product—not as a greenfield software project.

## Working principle

**Rigour at the scientific decision boundary; proportional engineering
everywhere else.**

- Clarify or prespecify changes that could alter an estimand, mechanism,
  numerical result, display interpretation, or submission claim.
- Make routine implementation choices autonomously and use the smallest clear
  solution that answers the current research question.
- Stop when further work is unlikely to change a scientific or submission
  decision. “Could be more polished” is not sufficient reason to continue.
- Do not add compatibility layers, speculative abstractions, duplicate runners,
  or bookkeeping for its own sake. This is a private research repository with
  no public legacy API.

## Active product and workflow

The project tests whether mixed species responses to correlated environmental
variation can buffer temporal variability in total community abundance relative
to aligned responses.

There is one active computational path:

1. `analysis/production_specs/*.json` defines a production grid.
2. `analysis/production_grid.py` creates, runs, combines, and validates it.
3. Seven compact parquet summaries live under `data/sim/production/`.
4. `analysis/run_all.py` regenerates all canonical figures and derived tables in
   `analysis/reports/`.
5. `analysis/check_numerical_guards.py` is a separate release diagnostic.

Do not restore legacy exploratory grids, plotting wrappers, fallbacks, or copied
figure trees. If a new analysis is scientifically justified, add it to the
active spec-to-summary-to-display path.

## Protected scientific invariants

Unless a task explicitly changes the science, preserve:

- the discrete-time competitive stochastic Ricker recurrence and its update
  order;
- the AR(1) innovation interpretation of `sigma_env` and the distinction from
  stationary environmental SD;
- requested `rho_env` versus feasible `rho_eff` handling;
- deterministic per-replicate production seeding and scenario ordering;
- post-burn-in metric definitions, including `cv_total`, synchrony metrics,
  floor occupancy, and variance decomposition;
- the six validated baseline production summaries and the validated Figure 4
  boundary summary, including their row-level contents;
- accepted display rendering and paper-to-figure links, unless a display change
  is explicitly approved; and
- the separation of anonymous review material from author/editorial material.

When touching simulation or analysis code, verify the relevant invariant
directly. A passing type check is not evidence of scientific equivalence.

## Implementation conventions

- Python 3.12 with `uv`; use the checked-in `pyproject.toml` and `uv.lock`.
- Prefer existing NumPy, pandas, PyArrow, and Matplotlib capabilities.
- Keep model dynamics in `model.py`, production execution in `production.py`,
  display summaries/rendering in `production_figures.py`, and derived diagnostics
  in `diagnostics.py`.
- Use versioned JSON specs for production creation; fixed model constants must
  be explicit in each spec.
- Canonical generated displays belong only in `analysis/reports/`.
- Preserve dirty user work and use Git history as the archive for deleted
  scripts, reports, and drafts.

## Proportional verification

Routine gate:

```bash
uv sync --python 3.12 --frozen --dev
uv run --frozen pytest -q
uv run --frozen pyright
```

For figure-path changes, run `uv run --frozen python analysis/run_all.py` and
compare numerical summaries plus rendered displays with the protected baseline.

For simulation or production changes, additionally validate the affected spec,
scenario counts, seeds, output schema, row count, and claim-specific numerical
invariants. Run the numerical-guard diagnostic for release-relevant parameter
changes.

For manuscript or submission changes, use the sequential `makedoc` profiles in
`paper/settings/build.yaml`, sanitize anonymous DOCX outputs, inspect the PDF,
and rebuild the anonymous review package when relevant.

Do not create a new test for every branch or formatting detail. Protect distinct
scientific contracts, failure modes that would silently corrupt results, and one
complete active workflow.

## Planning and communication

At the start of resumed work, inspect:

```bash
git status --short
git log --oneline -n 10
```

Read `docs/plan.md` and the most relevant decision or manuscript source. Use
`docs/decisions.md` only for consequential choices; use `docs/plan.md` for the
current bounded tranche. Do not recreate chronological phase logs.

Ask the PI only about substantive scientific forks, irreversible actions, or
submission facts that cannot be inferred. Record genuine unresolved decisions
briefly in `docs/questions_for_human.md`. Otherwise, make the sensible choice and
report the evidence, residual uncertainty, and next highest-value step.
