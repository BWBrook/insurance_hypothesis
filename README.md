# Insurance hypothesis simulation

This repository contains the simulation, analysis, and manuscript sources for a
theoretical ecology study of biodiversity insurance. Species follow a
competitive stochastic Ricker model and experience a correlated multivariate
AR(1) environment. The central comparison is between mixed response directions
and aligned responses: when species respond differently to the same forcing,
compensatory dynamics can reduce variability in total community abundance.

The active workflow is deliberately small:

1. versioned JSON specifications define production grids;
2. the production runner creates, shards, combines, and validates simulations;
3. seven compact production summaries regenerate every manuscript figure and
   derived table; and
4. a focused test suite protects the model, production bookkeeping, scientific
   summaries, and complete figure workflow.

There are no legacy fallbacks or compatibility entry points.

## Repository map

- `src/python/insurance_sim/model.py`: environment generator, Ricker simulator,
  and summary metrics.
- `src/python/insurance_sim/production.py`: deterministic production manifests,
  sharding, execution, combination, and validation.
- `src/python/insurance_sim/production_figures.py`: numerical summaries and
  plotting for the locked display suite.
- `src/python/insurance_sim/diagnostics.py`: variance decomposition, deterministic
  equilibrium, and abundance-weighted alignment diagnostics.
- `analysis/production_specs/`: the seven versioned production designs.
- `analysis/production_grid.py`: the sole full-simulation command-line entry
  point.
- `analysis/run_all.py`: the sole production-summary-to-display entry point.
- `analysis/check_numerical_guards.py`: a separate release check for clipping
  and floor occupancy in stress scenarios.
- `analysis/reports/`: canonical manuscript PNG, PDF, and CSV outputs.
- `paper/`: manuscript, Supporting Information, editorial materials,
  bibliography, Oikos style, and `makedoc` profiles.
- `tests/python/`: compact scientific and workflow checks.

## Environment and fast reproduction

Python 3.12 and [`uv`](https://docs.astral.sh/uv/) are required. From the
repository root:

```bash
uv sync --python 3.12 --frozen --dev
uv run --frozen pytest -q
uv run --frozen pyright
uv run --frozen python analysis/run_all.py
```

The last command reads these seven files:

| Production summary | Main use |
| --- | --- |
| `data/sim/production/fig1_s4_highres_v1/summaries.parquet` | Figure 3 core grid |
| `data/sim/production/fig1_s4_highsigma_v1/summaries.parquet` | Figure 3 stress extension |
| `data/sim/production/fig2_richness_mixed_v1/summaries.parquet` | Figures 4, S1, and S2; variance decomposition |
| `data/sim/production/fig3_synchrony_v1/summaries.parquet` | Figures 2 and S4 |
| `data/sim/production/fig5_persistence_mixed_v1/summaries.parquet` | Figure 5 |
| `data/sim/production/figs3_positive_matched_control_v1/summaries.parquet` | Figures 1A and S3 |
| `data/sim/production/fig4_weighted_balance_r0_v1/summaries.parquet` | Figure 1B,C weighted-balance boundary |

These parquet files contain replicate-level simulation summaries, not empirical
data. They are omitted from the ordinary Git checkout because of their size and
included in the reviewer-facing reproducibility package. If any are missing,
`analysis/run_all.py` reports the complete missing set and stops.

Canonical generated outputs are written only to `analysis/reports/`. Paper
sources reference that directory directly.

The manuscript figure order follows the revised evidential hierarchy; generated
filenames and production IDs remain stable. Figure 1 uses
`fig4_weighted_balance_boundary`, Figure 2 uses
`fig3_imposed_vs_realised_panels`, Figure 3 uses `fig1_panels`, Figure 4 uses
`fig2_richness_scaling_mixed`, and Figure 5 uses
`fig5_phi_sensitivity_sigma0.5_extended`. Each stem has PNG and PDF outputs.
The anonymous package README provides the same mapping.

## Model and experimental conventions

The population update is

```text
N_i(t+1) = N_i(t) exp[r0 + b_i z_i(t) -
                      {alpha_intra N_i(t) + alpha_inter sum_(j != i) N_j(t)} / K_i].
```

The production specifications make fixed constants explicit (normally `r0 = 1`,
`K = 100`, `alpha_intra = 1`, `alpha_inter = 0.3`, abundance floor `1e-9`, and
maximum exponent `50`) and record the Figure 1 vector-valued treatments in full.
Environmental innovations have standard deviation
`sigma_env`; with AR(1) persistence `phi`, stationary standard deviation is
`sigma_env / sqrt(1 - phi^2)`. The equicorrelation request `rho_env` is clipped
only when needed for positive definiteness, and the actual value is recorded as
`rho_eff`.

Response modes used by the paper are:

- `mixed`: slopes evenly spaced from -0.5 to 0.5;
- `positive`: aligned slopes from 0.1 to 1.0; and
- `positive_matched`: absolute values of the corresponding mixed slopes, which
  isolates response sign structure from slope magnitude.

The principal response is the temporal coefficient of variation of total
abundance (`cv_total`). Mechanistic summaries include Loreau-de Mazancourt
synchrony, mean pairwise realised per-capita growth correlation, and an exact
variance decomposition of total abundance.

## Full production recomputation

Each paper run is defined by one file under `analysis/production_specs/`. To
recompute a run, choose its spec and an output directory. For example:

```bash
SPEC=analysis/production_specs/fig1_s4_highres_v1.json
RUN_DIR=data/sim/production/fig1_s4_highres_v1

uv run --frozen python analysis/production_grid.py create \
  --spec "$SPEC" --output "$RUN_DIR/manifest.json"
uv run --frozen python analysis/production_grid.py run-pending \
  --manifest "$RUN_DIR/manifest.json" --jobs 8
uv run --frozen python analysis/production_grid.py combine \
  --manifest "$RUN_DIR/manifest.json" \
  --output "$RUN_DIR/summaries.parquet" \
  --validation-output "$RUN_DIR/validation.json"
uv run --frozen python analysis/production_grid.py validate \
  --manifest "$RUN_DIR/manifest.json" \
  --combined "$RUN_DIR/summaries.parquet"
```

The same runner supports `run-shard`, `pending`, and `list-shards`. Production
runs can be sharded across any suitable multi-core system without a second
simulation workflow.

After all seven summaries are present, regenerate the display suite with
`analysis/run_all.py`.

## Release checks

The routine code gate is:

```bash
uv run --frozen pytest -q
uv run --frozen pyright
uv run --frozen python analysis/run_all.py
```

Before a scientific release or submission, also run:

```bash
uv run --frozen python analysis/check_numerical_guards.py
```

Then validate the manuscript profiles using the external `makedoc` workflow
described in `paper/README_makedoc.md`, inspect the compiled PDF visually, and
build the anonymous code package:

```bash
uv run --frozen python scripts/build_deidentified_review_package.py --zip
```

Set `IH_REVIEW_PACKAGE_ROOT` when the package should be staged somewhere other
than `~/papers/de_identified_repos/`.

## Scientific and submission context

- `docs/plan.md` records the current revision tranche and stopping rule.
- `docs/decisions.md` records consequential scientific and release choices.
- `docs/interpretation_notes.md` gives the decision-relevant reading of the
  production results.
- `docs/oikos_external_review_and_line_edit_2026-08-09.md` is the preserved
  external review that motivates the final bounded revision.
- `docs/oikos_submission_checklist.md` is the live submission gate.
- `docs/questions_for_human.md` contains only unresolved PI decisions.

Historical scripts, exploratory outputs, progress ledgers, and superseded paper
drafts remain recoverable through Git history rather than being maintained as
active interfaces.
