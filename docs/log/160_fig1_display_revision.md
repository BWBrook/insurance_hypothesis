# 160 Figure 1 Display Revision

Date: 2026-05-15

## What was attempted

- Revised the Figure 1 strategy after Barry noted the weak `rho_eff` effect and suggested dropping the mixed-slope heatmap from the main display.
- Added a reproducible production Figure 1 candidate generator:
  - `analysis/plot_production_fig1.py`
  - `src/python/insurance_sim/production_figures.py`
- Added focused tests:
  - `tests/python/test_production_figures.py`

## Display decision

- The main candidate now uses two panels:
  - Panel A: aligned positive-slope `CV_tot` surface across `sigma_env` and `rho_eff`.
  - Panel B: mixed versus aligned mean `CV_tot` across `sigma_env`, averaged over the `rho_eff` grid, with faint bands showing the range across `rho_eff` and a grey aligned-minus-mixed CV gap on a secondary axis.
- The mixed-slope heatmap is deliberately omitted from the main candidate because its message is mostly “buffered across the surface” and the `rho_eff` structure is weak.
- The high-sigma region is shaded as a stress extension rather than treated as part of the core low-stress response surface.

## Outputs

- `analysis/reports/fig1_production_candidate.png`
- `analysis/reports/fig1_production_candidate.pdf`
- `analysis/reports/fig1_production_candidate_summary.csv`

## Checks

- `uv run python analysis/plot_production_fig1.py` -> wrote PNG, PDF, and summary CSV.
- `uv run pytest tests/python/test_production_figures.py -q` -> 2 passed.
- `uv run pytest` -> 29 passed.
- `uv run pyright` -> 0 errors.
- `git diff --check` -> passed.

## Next

- Review the candidate visually with Barry.
- If accepted, promote this as the new Figure 1 basis and update the manuscript caption.
- Keep the full mixed-slope heatmap and floor/extinction surfaces as supplementary/diagnostic material.
