# Insurance Hypothesis Simulation – Reproducible Pipeline

This repository contains the full simulation and analysis pipeline for a theoretical test of the **biodiversity insurance hypothesis**.  
In this project, multi‑species communities follow a stochastic Ricker model driven by a correlated AR(1) environmental process.  
We compare scenarios where species have **mixed response slopes** (some benefiting and some suffering from high environment) against **aligned positive slopes**, and quantify how richness and (a)synchrony modulate community‑level variability.

The repo is set up so that, starting from a clean checkout, you can:

- run the core simulations on the same grids used in the manuscript,
- regenerate all summary tables and figures,
- and rerun tests and sanity checks.

If you have already read the paper, this README is your practical guide to reproducing all results.

---

## 1. Repository layout

- `src/python/insurance_sim/`
  - Core simulator and metrics (`model.py`):
    - Discrete‑time stochastic Ricker dynamics with competition.
    - Multivariate AR(1) environment with innovation SD `σ_env`, equicorrelated covariance with imposed correlation `ρ_env`, and persistence `φ`.
    - Slope patterns:
      - `mixed`: species‑specific slopes evenly spaced in `[-0.5, 0.5]`.
      - `positive`: slopes in `[0.1, 1.0]`.
      - `mixed_narrow`: slopes in `[-0.25, 0.25]` (sensitivity).
    - Summary metrics: community CV (`CV_total`), approximate mean species CV, Loreau–de Mazancourt synchrony `φ_LdM`, mean pairwise growth‑rate correlation, extinction frequency.

- `analysis/`
  - `run_small_grid.py` – very small preview grid (2 species, few scenarios).
  - `run_full_grid.py` – generic grid runner used for all main and control experiments.
  - `plot_grid.py` – summarise a single `summaries.parquet` to CSV + heatmaps.
  - `plot_production_figS3.py` and `plot_production_supplementary.py` – rebuild production-backed supplementary figures from compact production summaries.
  - `run_all.py` – orchestration script that:
    - optionally reruns legacy exploratory fallback grids (`--rerun-data`),
    - reads production summaries under `data/sim/production/` when present,
    - uses cached exploratory outputs under `data/sim/grid/` only for optional diagnostics and legacy fallbacks,
    - regenerates summary CSVs and all manuscript‑level figures into `analysis/reports/`,
    - copies key panels into `paper/manuscript/figures/`.

- `data/sim/`
  - `preview/` – minimal preview run.
  - `grid/<run_name>/summaries.parquet` – cached scenario‑level summaries for each grid:
    - `run1` – main mixed‑slope grid.
    - `pos_full` – aligned positive slopes.
    - `phi0_reduced`, `phi07_reduced`, `phi09_reduced`, `phi095_reduced` – AR(1) persistence sensitivity.
    - `no_comp_mixed`, `no_comp_positive` – no‑competition controls (`α_inter = 0`).
    - `mixed_narrow` – reduced slope‑magnitude sensitivity.
    - `pos_subset` – early positive‑slope pilot (not used in final figures).

- `analysis/reports/`
  - Per‑grid CSV summaries and heatmaps (generated).
  - Combined panels:
    - `fig1_panels.png` / `.pdf` – Figure 1 main mixed vs positive contrast.
    - `fig3_imposed_vs_realised_panels.png` – Figure 3 imposed (`ρ_env`) vs realised synchrony.
    - `fig4_cv_vs_synchrony_mixed.png` – Figure 4 link between synchrony metrics and `CV_total`.
    - `fig5_phi_sensitivity_sigma0.5_extended.png` – Figure 5 φ‑sensitivity overlay.
    - `figS1_production_mixed_cv_total.png` – Supplementary Figure S1 production mixed-grid `CV Total` heatmaps.
    - `figS2_production_mixed_phi_ldm.png` – Supplementary Figure S2 production mixed-grid `φ_LdM` heatmaps.
    - `figS3_positive_matched_control.png` / `.pdf` – Supplementary Figure S3 production positive-matched control panel.
    - `figS4_production_species_cv_vs_rho.png` – Supplementary Figure S4 production species-level CV diagnostic.

- `paper/`
  - `paper/manuscript/text/draft_ms_v2.md` – full manuscript draft (Intro, Methods, Results, Discussion).
  - `paper/manuscript/text/figure_captions_v2.md` – captions aligned with figure filenames.
  - `paper/manuscript/text/figures.md` – makedoc figure blocks with stable `#fig-...` IDs.
  - `paper/manuscript/figures/` – figures copied from `analysis/reports/` by `run_all.py`.
  - `paper/references/ih_references.yaml` – canonical bibliography source (Zotero export and makedoc input).
  - `paper/csl/oikos.csl` – target journal CSL style.
  - `paper/settings/build.yaml` – makedoc external-path profiles (`ih_draft` scoped lint, `ih_submission` strict lint), using config-relative manuscript paths.

- `docs/`
  - `plan.md` – high‑level hypothesis, model description, experimental grid.
  - `interpretation_notes.md` – result summaries and follow‑up questions.
  - `decisions.md` – key modelling and implementation choices.
  - `log/*.md` – chronological logs of modelling and analysis phases.
  - `pi_review_round_*.md`, `review_rounds.md` – PI feedback and responses.

- `tests/`
  - `python/test_sim_basic.py` – unit/sanity tests for the simulator and environment generator.

---

## 2. Environment setup

This project uses **Python 3.12** with dependencies managed by **`uv`**.

1. Install `uv` (if not already available):

   ```bash
   pip install uv  # or follow the uv installation instructions for your platform
   ```

2. From the repository root, create/sync the environment:

   ```bash
   uv sync --dev
   ```

   This reads `pyproject.toml` and `uv.lock` and installs exact versions of the runtime and repo-local developer dependencies into a local environment.

3. Run the test suite to confirm everything is working:

   ```bash
   uv run pytest
   uv run pyright
   ```

   The tests cover:
   - basic AR(1) behaviour (stationary variance vs `σ_env` and `φ`),
   - non‑negativity and equilibrium under `σ_env = 0`,
   - synchrony metrics (φ_LdM, realised log-growth correlations) in toy cases,
   - bookkeeping in the replicate‑level simulator.

   Static type checks (`pyright`) help catch pandas/numpy interface mistakes early, especially in plotting and analysis orchestration scripts.

---

## 3. Fast reproduction: regenerate all figures from cached data

If you cloned the repository together with the `data/` directory (as in the archived project), you can reproduce all tables and figures **without rerunning the heavy simulations**.

The main Git repository does **not** currently track the bulky simulation data under `data/sim/`. For the final production figure suite, `analysis/run_all.py` now treats compact production summaries under `data/sim/production/` as the primary cache and uses the older `data/sim/grid/` summaries only for legacy fallbacks and per-grid diagnostic plots.

From the repository root:

```bash
uv run python analysis/run_all.py
```

For a code-only review package without the manuscript tree, use:

```bash
uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export
```

What this does:

- reads compact production `.parquet` summaries from `data/sim/production/<run_name>/summaries.parquet` for the production-backed main and supplementary figures;
- if the older exploratory caches are also present, reads `data/sim/grid/<run_name>/summaries.parquet` to regenerate legacy per-grid diagnostic heatmaps;
- if production summaries for a figure are missing, falls back to the corresponding cached exploratory grid and raises a targeted missing-data error if neither source is available;
- regenerates per‑grid summary CSVs and heatmaps into `analysis/reports/`;
- builds the combined panels (main manuscript figure, synchrony panels, φ‑sensitivity, CV vs synchrony scatter);
- copies key panels into `paper/manuscript/figures/`.

Typical runtime on a laptop or server is **well under a minute**, since no simulations are run.

For a **very small sanity preview** of the dynamics, you can also run:

```bash
uv run python analysis/run_small_grid.py
uv run python analysis/plot_grid.py \
  --input data/sim/preview/summaries.parquet \
  --out-prefix analysis/reports/preview
```

This generates a 2‑species, low‑replicate grid and corresponding plots.

---

## 4. Full recomputation: rerun all simulation grids

If you want to reproduce the simulations themselves (e.g. starting from a clone without `data/`), use `analysis/run_full_grid.py`.  
The commands below recreate each grid used for the manuscript, with the **same replicate counts and parameter sets**.

All commands should be executed from the repository root.

### 4.1 Main mixed‑slope grid (`run1`)

```bash
uv run python analysis/run_full_grid.py \
  --run-name run1 \
  --reps 150
```

- Slope mode: `mixed` (default, slopes in `[-0.5, 0.5]`).
- Grid:
  - `σ_env ∈ {0, 0.2, 0.5, 1.0, 1.5}`,
  - `ρ_env ∈ {-0.5, 0, 0.5, 0.9, 1.0}`,
  - `S ∈ {2, 4, 8}`,
  - `φ = 0.4`,
  - 600 time steps with 300 burn‑in.
- Output: `data/sim/grid/run1/summaries.parquet`.

This is the primary grid used for the mixed‑slope insurance results.

Note on negative correlations: with an equicorrelated innovation covariance, strongly negative `ρ_env` values become infeasible as richness increases (PD requires `ρ_env > -1/(S-1)`). The simulator therefore clips to the feasible bound when needed and records both the requested value (`rho_env`) and the effective value used (`rho_eff`, plus `rho_clipped`).

### 4.2 Positive‑slope grid (`pos_full`)

```bash
uv run python analysis/run_full_grid.py \
  --run-name pos_full \
  --slope-mode positive \
  --species-list 4,8 \
  --reps 100
```

- Slope mode: `positive` (slopes in `[0.1, 1.0]`).
- Grid:
  - `σ_env ∈ {0, 0.2, 0.5, 1.0, 1.5}`,
  - `ρ_env ∈ {-0.5, 0, 0.5, 0.9, 1.0}`,
  - `S ∈ {4, 8}`,
  - `φ = 0.4`,
  - 600 steps, 300 burn‑in.
- Output: `data/sim/grid/pos_full/summaries.parquet`.

This grid provides the aligned‑response contrast to the mixed‑slope scenarios.

### 4.2b Magnitude-matched aligned-slope control (`pos_matched`)

To separate “all slopes are positive” from “slopes are larger on average”, we also run an aligned-slope control where the **magnitude distribution is matched** to the mixed case (all slopes are `|b_i^{mixed}|`):

```bash
uv run python analysis/run_full_grid.py \
  --run-name pos_matched \
  --slope-mode positive_matched \
  --species-list 4,8 \
  --reps 100
```

Output: `data/sim/grid/pos_matched/summaries.parquet`.

### 4.3 Environmental persistence (φ) sensitivity grids

For φ‑sensitivity we use reduced grids with:
- `σ_env ∈ {0, 0.5, 1.0}`,
- `ρ_env ∈ {-0.5, 0, 0.5, 0.9, 1.0}`,
- `S ∈ {2, 4}`,
- `φ ∈ {0.0, 0.7, 0.9, 0.95}`,
- 400 steps with 200 burn‑in (passed explicitly; `run_full_grid.py` defaults are 600/300).

Run:

```bash
uv run python analysis/run_full_grid.py \
  --run-name phi0_reduced \
  --phi 0.0 \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4 \
  --steps 400 \
  --burn 200 \
  --reps 80

uv run python analysis/run_full_grid.py \
  --run-name phi07_reduced \
  --phi 0.7 \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4 \
  --steps 400 \
  --burn 200 \
  --reps 80

uv run python analysis/run_full_grid.py \
  --run-name phi09_reduced \
  --phi 0.9 \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4 \
  --steps 400 \
  --burn 200 \
  --reps 80

uv run python analysis/run_full_grid.py \
  --run-name phi095_reduced \
  --phi 0.95 \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4 \
  --steps 400 \
  --burn 200 \
  --reps 80
```

These runs underpin the φ‑sensitivity panels and the effective stationary SD (`σ_eff`) comparison in the manuscript.

### 4.4 No‑competition controls (`no_comp_mixed`, `no_comp_positive`)

To check whether the insurance patterns depend on interspecific competition, we repeat a reduced grid with `α_inter = 0`:

```bash
uv run python analysis/run_full_grid.py \
  --run-name no_comp_mixed \
  --alpha-inter 0.0 \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4,8 \
  --reps 80

uv run python analysis/run_full_grid.py \
  --run-name no_comp_positive \
  --alpha-inter 0.0 \
  --slope-mode positive \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4,8 \
  --reps 80
```

These grids are used qualitatively in the manuscript to demonstrate that mixed vs aligned response contrasts persist even without competition.

### 4.5 Slope‑magnitude sensitivity (`mixed_narrow`)

To test robustness to weaker response slopes, we run:

```bash
uv run python analysis/run_full_grid.py \
  --run-name mixed_narrow \
  --slope-mode mixed_narrow \
  --sigma-list 0,0.5,1.0 \
  --rho-list=-0.5,0,0.5,0.9,1.0 \
  --species-list 2,4,8 \
  --reps 80
```

This grid shows that insurance effects remain when mixed slopes are restricted to `[-0.25, 0.25]`.

### 4.6 Optional early pilot (`pos_subset`)

The early positive‑slope pilot is not used in the final manuscript figures but can be recreated as:

```bash
uv run python analysis/run_full_grid.py \
  --run-name pos_subset \
  --slope-mode positive \
  --sigma-list 0.5,1.0 \
  --rho-list=0,0.5,0.9 \
  --species-list 2 \
  --reps 50
```

### 4.7 Richness sweep for Figure 2 (`run1_richness`)

Figure 2 (richness scaling) uses an additional mixed‑slope grid that fills in all integer richness values `S=2…8` on the full σ_env–ρ_env grid:

```bash
uv run python analysis/run_full_grid.py \
  --run-name run1_richness \
  --species-list 2,3,4,5,6,7,8 \
  --reps 150
```

This produces `data/sim/grid/run1_richness/summaries.parquet`.  
`analysis/run_all.py` will automatically use this file for the richness‑scaling curve if it exists; otherwise it falls back to the main `run1` grid.

---

## 5. From simulations to figures

After rerunning any subset of grids above, regenerate all derived summaries and figures with:

```bash
uv run python analysis/run_all.py
```

You can also inspect or summarise an individual grid directly, for example:

```bash
uv run python analysis/plot_grid.py \
  --input data/sim/grid/run1/summaries.parquet \
  --out-prefix analysis/reports/run1
```

Key figures used in the manuscript will appear in:

- `analysis/reports/` – intermediate PNGs and CSVs,
- `paper/manuscript/figures/` – final panels referenced by `paper/manuscript/text/figure_captions_v2.md`.

Approximate runtimes on a modern laptop:

- `run1` (mixed grid, 150 reps): **~2–3 minutes**.
- `pos_full` (positive grid, 100 reps): **~1–2 minutes**.
- Each reduced grid (φ sensitivity, no‑competition, mixed_narrow): **<2 minutes**.
- `run_all.py` when using existing `.parquet` files: **<1 minute**.

Exact times will depend on hardware, but Monte Carlo uncertainty is small relative to the effect sizes reported in the manuscript.

---

## 6. How this maps to the manuscript

If you are reading this after the paper:

- **Main results**:
  - Mixed slopes vs aligned positive slopes (main grid vs `pos_full`).
  - Richness effects in CV_total and synchrony.
  - Imposed vs realised synchrony and their divergence.
  - φ‑sensitivity and effective environmental variance.
  - No‑competition and slope‑magnitude controls.
- **Model and experimental design** are described in detail in `paper/manuscript/text/draft_ms_v2.md` (Methods), with notation matched to the code:
  - imposed environmental correlation `ρ_env`,
  - innovation SD `σ_env` and effective stationary SD `σ_eff` for φ analyses,
  - realised synchrony `φ_LdM` and growth‑rate correlations.
- **Figures**: see `paper/manuscript/text/figure_captions_v2.md` for a mapping from figure labels to files in `paper/manuscript/figures/`.

For deeper scientific context and interpretation, consult:

- `docs/plan.md` – refined hypothesis and metric definitions.
- `docs/interpretation_notes.md` – per‑figure interpretation notes and robustness checks.
- `docs/decisions.md` – key modelling/implementation choices and their rationale.
- `docs/review_rounds.md`, `docs/pi_review_round_*.md` – PI review comments and how they were addressed.

---

## 7. Summary of reproduction steps

1. **Set up environment**
   - `uv sync`
   - `uv run pytest`
   - `uv run pyright`

2. **Fast path (cached data)**
   - `uv run python analysis/run_all.py`
   - Inspect figures in `analysis/reports/` and `paper/manuscript/figures/`.

3. **Full recomputation (optional)**
   - Run the grid commands in Section 4 (at minimum `run1` and `pos_full`, plus φ‑sensitivity if you want Fig. φ panels).
   - Rerun `uv run python analysis/run_all.py`.

Following these steps should exactly reproduce the tables and figures reported in the manuscript.

---

## 8. FAQ and troubleshooting

**Q1. I cloned the repo but there is no `data/` directory. What should I do?**  
- The fast path in Section 3 assumes cached `.parquet` files exist under `data/sim/grid/`.  
- If `data/` is missing, you simply need to rerun the grids you care about using `analysis/run_full_grid.py` (Section 4), then run:

  ```bash
  uv run python analysis/run_all.py
  ```

  At minimum, re‑create `run1` and `pos_full` for the main figures.

**Q2. I see a warning about `VIRTUAL_ENV` not matching `.venv` when using `uv`. Is this a problem?**  
- Example warning:

  > `VIRTUAL_ENV=... does not match the project environment path .venv and will be ignored`  

- This just means you already had another virtual environment active. `uv` will ignore it and use the project environment defined by `pyproject.toml` / `uv.lock`.  
- You can ignore the warning, or deactivate your global env (e.g. `deactivate`) before running `uv` commands.

**Q3. `uv run python analysis/run_all.py` fails because one of the `phi*_reduced` parquet files is missing.**  
- Each φ‑sensitivity dataset is expected at:
  - `data/sim/grid/phi0_reduced/summaries.parquet`
  - `data/sim/grid/phi07_reduced/summaries.parquet`
  - `data/sim/grid/phi09_reduced/summaries.parquet`
  - `data/sim/grid/phi095_reduced/summaries.parquet`
- If any are missing, rerun the corresponding grid using the commands in Section 4.3, then re‑run:

  ```bash
  uv run python analysis/run_all.py
  ```

**Q4. `pytest` fails after I modify the simulator or analysis code. How do I debug this?**  
- First ensure your environment is up to date:

  ```bash
  uv sync
  uv run pytest
  ```

- If tests still fail, check `tests/python/test_sim_basic.py` to see which expectations are violated (e.g. stationary variance under AR(1), non‑negativity, synchrony bounds).  
- The tests are intentionally small and fast; they are a good starting point for verifying any further changes you make.

**Q5. Simulations are running slowly on my machine. Can I down‑sample?**  
- For strict reproduction of the manuscript results you should use the replicate counts given in Section 4.  
- For experimentation or development, you can reduce `--reps`, shorten time series (`--steps` / `--burn`), or restrict σ/ρ/S lists (e.g. a single σ_env or a subset of ρ_env values).  
- Just be aware that Monte Carlo uncertainty will increase when you reduce replicate counts; the main manuscript grids were sized to make this uncertainty small relative to the effect sizes of interest.

**Q6. Pylance/VS Code reports type errors even though `pytest` passes. What should I run?**  
- Run:

  ```bash
  uv run pyright
  ```

- This uses the project-locked `pyright` version from `uv.lock`, so results are reproducible across machines.
- If `pyright` fails, address those issues before trusting regenerated figures; many static failures are pandas shape/type mismatches that can silently affect analysis scripts.
