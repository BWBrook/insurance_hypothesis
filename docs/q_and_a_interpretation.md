# Ecologist Q and A Interpretation Log

This is a living notebook for the ecologist-facing walkthrough of the repository.
It captures:

- your interpretation questions,
- my technical and ecological responses,
- any actions we decide to take,
- and follow-up status.

The goal is to keep a transparent record of human-in-the-loop sanity checks as we review results and presentation.

Path note: after the manuscript reorganisation, canonical manuscript paths are under `paper/manuscript/` and links in this log follow that structure.

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
- Latest restart: 2026-05-14
- Mode: ecologist-facing human-testing pass with technical chaperoning
- Scope: interpretation, sanity checks, display clarity, reproducibility UX
- Current focus: whole-repo ecologist-facing sanity pass outside `paper/`, following the recent hardening/refactor work

## Q and A entries

### QA-001

- Context: kickoff of ecologist-facing review workflow.
- Question: How will we capture interpretation questions and responses as we go?
- Response: Use this file as a timestamped running log with explicit status and action fields so decisions are auditable.
- Decision / Action: create and maintain `docs/q_and_a_interpretation.md` throughout walkthrough.
- Status: actioned
- Links: `docs/q_and_a_interpretation.md`

### QA-002

- Context: Figure 1 caption check against `paper/manuscript/text/figure_captions_v2.md` and current Figure 1 panel file.
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
- Links: `analysis/run_all.py`, `analysis/reports/fig1_panels.png`, `paper/manuscript/figures/fig1_panels.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-003

- Context: Figure 2 caption check against `paper/manuscript/text/figure_captions_v2.md` and `paper/manuscript/figures/cv_richness_scaling_mixed.png`.
- Question: Is the Figure 2 caption fully congruent with the richness-scaling figure, and can we rename to a numbered figure filename?
- Response:
  - Core pattern is congruent: for `sigma_env > 0`, `CV_tot` drops from `S=2` to `S=4` and continues declining toward `S=8`.
  - Caption-side caveat: it currently says this decline occurs for "all sigma values shown", but `sigma_env=0` is a flat zero baseline (no decline).
  - Methods-side caveat: the plotted mean is currently averaged over the shared non-negative subset (`rho_env >= 0`) for cross-richness comparability, not all requested `rho_env` values.
- Decision / Action:
  - Rename generated Figure 2 output to `fig2_richness_scaling_mixed.png`.
  - Keep current plotting logic unchanged for now (shared non-negative `rho_env` subset), and flag caption wording for refinement.
- Status: answered
- Links: `analysis/run_all.py`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-004

- Context: Figure 2 visual polish pass (legend readability).
- Question: If legend title already defines the symbol (e.g. `sigma_env`/`rho_env`), should legend entries still repeat `symbol = value`?
- Response: Repeating the symbol in each entry is redundant and visually busy. A cleaner convention is: symbol in legend title, numeric values in entries.
- Decision / Action:
  - Simplified Figure 2 legend entries from `sigma_env = value` to `value` while keeping legend title as `sigma_env`.
  - Regenerate and re-check Figure 2 for readability.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`

### QA-005

- Context: Figure 2 caption precision review.
- Question: Can we fix the imprecision in the Figure 2 caption to match what is actually plotted?
- Response:
  - Yes. The original wording overstated two points:
    - `sigma_env=0` is a flat near-zero baseline, not a declining richness trend.
    - The current figure averages over the shared non-negative `rho_env` subset (`rho_env >= 0`) for cross-richness comparability.
- Decision / Action:
  - Updated Figure 2 caption text in `paper/manuscript/text/figure_captions_v2.md` to state both details explicitly.
  - Continued numbered-figure transition by keeping legacy `manuscript_panels.*` assets deleted.
- Status: actioned
- Links: `paper/manuscript/text/figure_captions_v2.md`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/figures/fig2_richness_scaling_mixed.png`

### QA-006

- Context: Figure asset housekeeping after Figure 2 renaming.
- Question: Should legacy `cv_richness_scaling_mixed.png` be removed now that Figure 2 uses numbered filenames?
- Response: Yes. Keeping only current numbered assets reduces ambiguity and prevents accidental citation of stale files.
- Decision / Action:
  - Deleted `paper/manuscript/figures/cv_richness_scaling_mixed.png`.
  - Deleted `analysis/reports/cv_richness_scaling_mixed.png` for consistency.
- Status: actioned
- Links: `paper/manuscript/figures/fig2_richness_scaling_mixed.png`, `analysis/reports/fig2_richness_scaling_mixed.png`

### QA-007

- Context: Figure 3 caption-vs-plot congruence check for `imposed_vs_realised_panels.png`.
- Question: Does Figure 3 match the v2 caption, and are there any caption bugs to fix?
- Response:
  - Panels A and B are congruent with the caption and summary data.
  - Caption bug identified in Panel C wording: positive-slope deviations are not uniformly near-zero/negative; they are positive at low `rho_env` and become near-zero to modestly negative only at high `rho_env`.
  - Plot-side refinement: panel C previously drew species-level rows as a single connected path per slope mode; this was visually ambiguous.
- Decision / Action:
  - Renamed Figure 3 output to `fig3_imposed_vs_realised_panels.png`.
  - Updated panel C plotting to use richness-averaged regime means (one curve per slope mode) to match caption framing.
  - Updated Figure 3 caption text in `paper/manuscript/text/figure_captions_v2.md` to reflect the corrected positive-regime pattern.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig3_imposed_vs_realised_panels.png`, `paper/manuscript/figures/fig3_imposed_vs_realised_panels.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-008

- Context: Figure 4 caption-vs-plot congruence check for `cv_vs_synchrony_mixed.png`.
- Question: Does Figure 4 match the v2 caption, and is there any caption bug to fix?
- Response:
  - Caption is scientifically congruent with the plotted data and aggregation method (scenario means, post-burn-in, mixed-slope grid).
  - Association direction in both panels is generally positive (higher synchrony metrics tend to correspond to higher `CV_tot`), with expected spread at low richness.
- Decision / Action:
  - No caption wording change required at this step.
  - Rename Figure 4 output to `fig4_cv_vs_synchrony_mixed.png` and update references.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig4_cv_vs_synchrony_mixed.png`, `paper/manuscript/figures/fig4_cv_vs_synchrony_mixed.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-009

- Context: Figure 5 caption-vs-plot congruence check for `cv_phi_sensitivity_sigma0.5_extended.png`.
- Question: Does Figure 5 match the v2 caption, and if not, what should be fixed?
- Response:
  - Core pattern and caption claims are congruent (higher `phi` inflates `CV_tot`; richness effect and generally negative `CV_tot`–`rho_env` association in mixed slopes remain).
  - One mismatch identified: caption states "points show replicate values and lines show scenario means", while the prior plot had means only.
- Decision / Action:
  - Updated Figure 5 plotting to overlay faint replicate points plus mean lines.
  - Renamed Figure 5 output to `fig5_phi_sensitivity_sigma0.5_extended.png` and updated references.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-010

- Context: Figure 5 display polish after the main caption congruence fix.
- Question: Can we simplify and standardise Figure 5 annotations for readability?
- Response: Yes. The requested improvements increase cross-panel comparability and reduce legend clutter without changing data content.
- Decision / Action:
  - Changed y-axis label from `CV_total` to `CV Total`.
  - Changed panel titles to use Greek sigma notation (`σ_env = 0.5`).
  - Forced both panels to the same x-axis scale (`-0.5` to `1.0`) for visual comparability.
  - Simplified legend entries to compact numeric format (`phi (~sigma_eff)`) with a single legend title.
  - Kept only one legend (left panel) to avoid duplication.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`

### QA-011

- Context: Final Figure 5 title/layout polish.
- Question: Can the super-title carry the fixed-environment context and allow cleaner panel titles?
- Response: Yes. Moving the fixed `sigma_env` context to the super-title and leaving panel titles as richness-only improves readability and avoids repetition.
- Decision / Action:
  - Updated Figure 5 super-title to use Greek notation and include fixed `sigma_env=0.5` context.
  - Simplified panel titles to `S=2` and `S=4`.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`, `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`

### QA-012

- Context: Supplementary promotion and comparability polish for `run1_cv_total.png` and `run1_phi_ldm.png`.
- Question: Can these become Fig. S1/S2 with cleaner labels and fully shared colour scales within each figure?
- Response: Yes. This is a strong improvement for supplementary readability and cross-panel comparability.
- Decision / Action:
  - Converted mixed-grid heatmaps to supplementary filenames:
    - `figS1_run1_cv_total.png`
    - `figS2_run1_phi_ldm.png`
  - Updated heatmap generation to enforce shared colour limits across richness panels within each metric figure.
  - Replaced panel title text:
    - `cv_total` -> `CV Total`
    - `phi_ldm` -> `φ_LdM`
  - Simplified each figure to a single shared colourbar.
  - Added Figure S1 and Figure S2 captions to `paper/manuscript/text/figure_captions_v2.md`.
- Status: actioned
- Links: `analysis/run_all.py`, `analysis/reports/figS1_run1_cv_total.png`, `analysis/reports/figS2_run1_phi_ldm.png`, `paper/manuscript/figures/figS1_run1_cv_total.png`, `paper/manuscript/figures/figS2_run1_phi_ldm.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-013

- Context: restart of the ecologist-facing review after the 2026-03-07 repo hardening pass.
- Question: How should we run the new scientist-in-the-loop sanity-check phase, and where should the discussion be captured?
- Response:
  - Reuse this file as the canonical living log for your questions and my responses.
  - Keep the pass explicitly non-`paper/` for now, so we sanity-check the repo from the ecologist-facing side first: README claims, analysis outputs, interpretation notes, and reproducibility UX.
  - Work in a stable review order so we can tell whether issues come from scientific framing, code behavior, or presentation.
- Decision / Action:
  - Resume `docs/q_and_a_interpretation.md` as the active running log.
  - First-pass review order:
    1. `README.md` as the ecologist-facing entry point.
    2. `analysis/reports/fig1_panels.png` for the main mixed-vs-aligned contrast.
    3. `analysis/reports/fig3_imposed_vs_realised_panels.png` for mechanism/synchrony interpretation.
    4. `analysis/reports/fig2_richness_scaling_mixed.png` and `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png` for robustness/story checks.
  - Record each new question as `QA-014` onward.
- Status: actioned
- Links: `docs/q_and_a_interpretation.md`, `README.md`, `analysis/reports/fig1_panels.png`, `analysis/reports/fig3_imposed_vs_realised_panels.png`, `analysis/reports/fig2_richness_scaling_mixed.png`, `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`

### QA-014

- Context: first ecologist-facing read of `analysis/reports/fig1_panels.png`, especially the blocky heatmaps in panels A/B and the concentration of visual change at higher `sigma_env`.
- Question: Why did we run relatively few simulation iterations, and quite crude gradations in parameters like `rho_env` and `sigma_env`? In a full multi-core/RAM setting, would it make sense to smooth this out with more replicates and finer parameter gradations, at least to make the figures nicer?
- Response:
  - The current grid is best understood as an exploratory-to-interim production grid, not the final display-quality response surface. It was coarse enough to map the sign and broad shape of the effect across slope modes, richness, synchrony, persistence, and controls while keeping turnaround times manageable during model development.
  - More replicates and finer parameter gradations solve different problems. More replicates reduce Monte Carlo noise around each scenario mean. Finer `sigma_env`/`rho_env` values reduce the blocky heatmap appearance and reveal whether apparent thresholds or bends are smooth transitions.
  - The blockiness in panels A/B is mostly the 5 x 5 parameter grid being shown with `imshow`; it is not primarily a replicate-count problem. The cached summary feeding the mixed panel has 150 replicates per scenario, while the aligned-response panel has 100. Those are reasonable for detecting the main effect, but sparse for publication-quality surfaces.
  - The bunching of the visual signal at `sigma_env > 1` is scientifically important rather than just a plotting nuisance. It suggests the response is nonlinear across the chosen environmental-noise range. A denser grid should concentrate points between about `sigma_env = 0.5` and `1.5`, and possibly treat the highest `sigma_env` values as stress-test territory rather than the main ecological operating range.
  - `rho_env` has an additional complication: under the equicorrelated multivariate driver, negative correlations are constrained by species richness. For example, requested `rho_env = -0.5` must be clipped upward for S=4 and S=8. So simply adding many negative `rho_env` values will not necessarily add much information unless we also consider a different covariance design.
  - My recommendation is yes: now that the code and tests are more stable, a high-resolution production grid is worthwhile. But we should do it as a controlled extension, not just smooth the existing figure. First run a focused high-resolution S=4 grid for mixed and positive slopes, compare it against the coarse grid, then decide whether to scale up to S=2/4/8 and the supplementary/sensitivity figures.
- Decision / Action:
  - Add a follow-up task to design and run a high-resolution production grid for Figure 1 surfaces.
  - Candidate first pass: keep `phi=0.4`, steps/burn unchanged or modestly increased, use higher replicate counts, densify `sigma_env` around the visible transition, and use `rho_eff`-aware plotting.
  - Follow-up on 2026-05-14: production-scale runs should default to 1000 replicates per scenario/slice, superseding the earlier 300-500 exploratory suggestion.
  - Before changing manuscript/display defaults, compare coarse vs high-resolution surfaces to confirm the ecological story is unchanged.
- Status: answered
- Links: `analysis/reports/fig1_panels.png`, `analysis/reports/run1_summary.csv`, `analysis/reports/pos_full_summary.csv`, `analysis/run_full_grid.py`, `src/python/insurance_sim/reporting.py`

### QA-015

- Context: infrastructure scouting for future higher-resolution simulation grids on `deep-server`.
- Question: Is `deep-server` available and suitably configured for larger compute-heavy simulation jobs?
- Response:
  - SSH access works non-interactively via `deep-server`; `deep-server-relay` also works and the persistent reverse tunnel listener is active at `127.0.0.1:2222`.
  - Follow-up access check on 2026-05-05 confirmed both direct SSH forms now work: `ssh deep-server ...` and `ssh -o ControlMaster=no -o ControlPath=none deep-server ...`. The earlier odd direct-SSH behaviour was plausibly a stale control-master socket rather than a server-side fault.
  - Hardware is suitable for the next simulation round: 64 logical CPUs on dual Intel Xeon E5-2683 v4 sockets, 2 NUMA nodes, about 125 GiB RAM with about 123 GiB available during the scout, and about 808 GiB free on the root/home filesystem.
  - The machine was effectively idle during the scout: load averages were near zero, no user simulation jobs were evident, and no tmux sessions were active.
  - Tooling is adequate: Python 3.12.3, `uv 0.9.13` in a login shell, Git, tmux, rsync, taskset, numactl, gcc/g++, make, Julia 1.12.2, and R 4.5.3 are available.
  - A checkout already exists at `~/papers/insurance_hypothesis`; it is currently behind `origin/main` by 3 commits, so it should be fast-forwarded or resynced before any production run.
  - A small `uv run` import check succeeded on the remote checkout for numpy, pandas, pyarrow, and matplotlib. No large simulations were launched.
- Decision / Action:
  - Use `deep-server` as the default execution host for high-resolution production grids, with WSL as the control plane.
  - Use `tmux` for long jobs, and sync outputs back via Git/rsync depending on whether outputs are intended to be tracked.
  - Before starting new grids, update the remote checkout to current `origin/main` and rerun a lightweight environment/test check.
- Status: answered
- Links: `docs/q_and_a_interpretation.md`

### QA-016

- Context: review of `/home/bwbrook/work/nectar` before planning production-scale insurance-hypothesis simulations.
- Question: How should the Nectar/deep-server operating guidance shape the new production simulation work, and should final runs use 1000 replicates rather than 300-500?
- Response:
  - The Nectar control-plane repo confirms the right division of labour: WSL is a dashboard/orchestration host, while `deep-server` is the right default for this project because the proposed production grids are CPU-heavy, single-host, and do not need GPU or multi-node queueing.
  - The relevant Nectar guidance is: use `deep-server` for durable standalone multicore jobs, keep project-specific scientific run definitions in this repository, use `tmux` for long jobs, and put bulky clones/caches/outputs under `/data` when running on `deep-server`.
  - The repo's own checks passed on 2026-05-14: `scripts/validate-repo.sh`, `scripts/check-access.sh deep-server`, and `scripts/deep-server/inventory.sh`.
  - `deep-server` inventory confirms 64 logical CPUs, 125 GiB RAM, `/data` mounted with about 4.5 TiB available, Docker available, passwordless sudo enabled, and no scheduler environment. GPU compute should be ignored for this project.
  - The inventory script reports `uv=missing` because it probes a non-login shell, but `uv` is present in a login shell at `~/.local/bin/uv`; remote project commands should therefore use `ssh deep-server 'bash -lc "..."'`.
  - The 1000-replicate default is scientifically reasonable for the final paper. Even if precision gains diminish after a few hundred replicates, a fixed 1K per scenario is easy to justify and reduces reviewer concern about sampling uncertainty.
- Decision / Action:
  - Default production-scale insurance-hypothesis runs to 1000 replicates per scenario/slice unless a specific stress-test or smoke-test is intentionally smaller.
  - Use `deep-server` via login-shell SSH commands and `tmux` for long production jobs.
  - Stage heavy run outputs under `/data` on `deep-server`, while keeping run definitions, code, summaries, and interpretation in this project repo.
  - Before launching production grids, sync/update the remote `insurance_hypothesis` checkout and run a small project-native smoke test.
- Status: answered
- Links: `/home/bwbrook/work/nectar/README.md`, `/home/bwbrook/work/nectar/docs/workflows/compute-resource-selection.md`, `/home/bwbrook/work/nectar/docs/machines/deep-server.md`, `/home/bwbrook/work/nectar/docs/workflows/project-integration.md`, `/home/bwbrook/work/nectar/docs/workflows/smoke-tests.md`

### QA-017

- Context: deciding how to move from a draft manuscript based on low/interim simulations to a final Oikos-ready manuscript based on production-level simulations.
- Question: What is the first cab off the rank, or is this the right time to make a detailed phased execution plan?
- Response:
  - This is the right time for a detailed phased plan. The project is crossing from exploratory result-building into a production campaign, so compute, provenance, validation, and display-item rebuilds need to be planned together.
  - The first implementation task is not launching the full grid. The current `analysis/run_full_grid.py` is scenario-sequential and suited to exploratory runs; before 1000-replicate production grids, we need a shardable, resumable production harness that can run under `tmux` on `deep-server`, validate outputs, and preserve run provenance.
  - The execution plan should still leave room for Barry's ongoing artifact review, because that review determines which grids are scientifically necessary rather than merely computationally possible.
- Decision / Action:
  - Added `docs/production_execution_plan.md` as the staged roadmap from current draft to Oikos-ready manuscript.
  - Treat the first code-producing task as building and testing the production harness, after the current planning checkpoint is clean.
  - Keep the ecologist-facing walkthrough active in parallel so the production grid spec is driven by real interpretation/display needs.
- Status: answered
- Links: `docs/production_execution_plan.md`, `analysis/run_full_grid.py`, `docs/plan.md`

### QA-018

- Context: first scientific read of production quicklooks from `fig1-s4-highres-v1`, especially the fact that the current surface only extends to `sigma_env=2.0`.
- Question: My first pass on this result is that we need to push out further in the `sigma_env` magnitude. Interesting things are really only happening in Figure 1 at about `sigma_env > 1` for positive slopes and `sigma_env > 1.8` for mixed slopes. Should we go up to 3 or even 4? High variability regimes may be less common in many taxa but plausible for invertebrates, for instance?
- Response:
  - Yes, this is a sensible next scientific probe. The first production grid shows that `sigma_env=2.0` is not yet enough to reveal the full mixed-slope response surface, even though the positive aligned-slope surface is already entering a high-CV region.
  - Ecologically, extending to `sigma_env=3-4` is defensible as a high-variability or boom-bust regime, especially for short-lived taxa with strong environmental forcing. It should not be presented as the typical regime for all communities, but it is useful for stress-testing where the insurance effect bends, saturates, or breaks down.
  - Technically, `sigma_env` is the innovation standard deviation of the AR(1) environmental driver. With `phi=0.4`, the stationary environmental SD is about 1.09 times `sigma_env`, so `sigma_env=4` is a genuinely extreme forcing regime.
  - Interpretation should explicitly separate the core response-surface regime from the high-sigma extension, because high positive-slope scenarios may increasingly reflect floor occupancy and nonlinear Ricker/floor dynamics rather than clean low-extinction insurance dynamics.
- Decision / Action:
  - Add a labelled high-sigma extension spec for S=4 mixed and positive slopes, reusing the same 1000-replicate and 48-worker production defaults.
  - Extend beyond the existing grid with `sigma_env` values above 2.0 up to 4.0.
  - Validate and summarise extinction/floor occupancy before deciding whether the high-sigma region belongs in the main Figure 1 display, an inset, or supplementary stress-region panel.
- Follow-up result:
  - `fig1-s4-highsigma-v1` validated cleanly on `deep-server` with 180 scenarios, 1800 shards, and 180000 rows.
  - The extension confirms your read: mixed slopes become visibly dynamic above `sigma_env=2`, rising from mean CV ~0.78 at 2.0 to ~4.39 at 4.0; positive slopes rise from ~3.36 to ~11.13 over the same range.
  - The insurance contrast persists but narrows at the extreme end: positive/mixed mean-CV ratio is ~4.5 near `sigma_env=2.5`, ~4.0 at 3.0, and ~2.5 at 4.0.
  - Floor/extinction frequency also rises, especially for positive slopes: by `sigma_env=4.0`, mean floor frequency averaged across the `rho_env` grid is ~0.030 for mixed slopes and ~0.102 for positive slopes. This supports treating `sigma_env > 3` as a stress region unless further diagnostics justify otherwise.
- Status: actioned
- Links: `analysis/production_specs/fig1_s4_highres_v1.json`, `analysis/production_specs/fig1_s4_highsigma_v1.json`, `docs/log/140_fig1_production_batch.md`, `analysis/reports/production/fig1_s4_combined_highsigma_v1_mean_cv_by_sigma.png`

### QA-019

- Context: redesigning Figure 1 after the core and high-sigma S=4 production runs showed weak `rho_eff` structure relative to the strong `sigma_env` gradient and mixed-vs-positive contrast.
- Question: Given the weak effect of `rho_eff` on Figure 1, should we leave out the current mixed-slopes subplot and instead use the positive-slope surface as subplot A and a positive-vs-mixed divergence across `sigma_env` as subplot B? Or should we use a core surface plus stress-extension inset/split-axis approach?
- Response:
  - I agree that the mixed-slope heatmap is not earning main-panel space. Its ecological message is mostly “buffered across the surface,” and the `rho_eff` variation is secondary compared with the `sigma_env` gradient.
  - The best main-text candidate is therefore a two-panel figure:
    - Panel A: aligned positive-slope response surface, retaining `rho_eff` as context because this is the regime where synchronised responses should be most visibly destabilising.
    - Panel B: mixed versus aligned mean `CV_tot` across `sigma_env`, averaged over `rho_eff`, with the range across `rho_eff` shown as a faint band and the aligned-minus-mixed CV gap on the same primary y-axis.
  - The high-sigma region is shaded as a stress extension rather than being hidden or treated as the core regime. The full mixed-slope heatmap and floor/extinction surfaces should remain diagnostic or supplementary.
- Decision / Action:
  - Added `analysis/plot_production_fig1.py` and `src/python/insurance_sim/production_figures.py`.
  - Wrote a review-ready candidate to `analysis/reports/fig1_production_candidate.png` and `.pdf`.
  - Wrote the scenario-level summary to `analysis/reports/fig1_production_candidate_summary.csv`.
  - Added focused tests for the production Figure 1 summary/plotting helper.
  - Follow-up display refinement: moved the aligned-minus-mixed gap onto the primary Panel B y-axis, merged it into the upper-left legend below the mixed/aligned entries, and right-aligned the "stress extension" label within the shaded band at about y=5.
- Status: actioned
- Links: `analysis/plot_production_fig1.py`, `src/python/insurance_sim/production_figures.py`, `analysis/reports/fig1_production_candidate.png`, `analysis/reports/fig1_production_candidate.pdf`

### QA-020

- Context: Barry approved the revised production Figure 1 display and asked to proceed with both Figure 1 completion and production-run work on Figure 2.
- Question: What should be done next to complete Figure 1 and move Figure 2 onto production-scale evidence?
- Response:
  - Promote the accepted Figure 1 display to the canonical `fig1_panels` outputs and update the caption/manuscript references so they no longer describe the superseded four-panel interim figure.
  - Keep `analysis/run_all.py` compatible with fresh/interim checkouts by using production Figure 1/Figure 2 inputs when present and falling back to existing cached exploratory grids otherwise.
  - Freeze Figure 2 as a focused mixed-slope richness production grid: S=2..8, `sigma_env` up to 2.0, non-negative `rho_env`, `phi=0.4`, and 1000 replicates per scenario.
  - Launch the Figure 2 production grid on `deep-server` under `tmux`, retrieve compact outputs, rebuild the Figure 2 display, and record the ecological sanity check before relying on it in the manuscript.
- Actions:
  - Added `analysis/production_specs/fig2_richness_mixed_v1.json`.
  - Added production Figure 2 plotting hooks alongside the promoted Figure 1 production hooks.
  - Updated Figure 1 and Figure 2 manuscript captions to match the production display plan.
  - Launched `fig2-richness-mixed-v1` on `deep-server` under tmux; the run validated with 210000 rows across 210 scenarios.
  - Retrieved compact outputs and rebuilt `analysis/reports/fig2_richness_scaling_mixed.png` and `.pdf`.
- Status: actioned
- Links: `analysis/production_specs/fig2_richness_mixed_v1.json`, `analysis/plot_production_fig1.py`, `analysis/plot_production_fig2.py`, `analysis/run_all.py`, `analysis/reports/fig2_richness_scaling_mixed.png`, `paper/manuscript/text/figure_captions_v2.md`

### QA-021

- Context: Barry reviewed the rebuilt production Figure 2 and said the `rho_eff` range bands are visually striking and should remain.
- Question: What should be the next production-level reinforcement/improvement after Figures 1 and 2?
- Response:
  - Keep Figure 2 unchanged.
  - The next cab should be the mechanism display: refresh Figure 3, the imposed-vs-realised synchrony figure, with production-scale simulations.
  - Proposed production grid: `sigma_env=0.5`, `phi=0.4`, S=2,4,8, mixed and positive slope modes, non-negative `rho_env` grid from 0 to 1, and 1000 replicates per scenario.
  - Rationale: Figures 1 and 2 now establish the headline pattern and richness buffering; Figure 3 is the causal/mechanistic bridge showing how response direction decouples imposed environmental covariance from realised growth synchrony.
- Actions:
  - Added `analysis/production_specs/fig3_synchrony_v1.json`.
  - Added `analysis/plot_production_fig3.py` and production Figure 3 helpers.
  - Updated `analysis/run_all.py` to prefer production Figure 3 data when available.
  - Launched `fig3-synchrony-v1` on `deep-server` after the GlobalProtect VPN refresh restored SSH.
  - Retrieved compact outputs and rebuilt `analysis/reports/fig3_imposed_vs_realised_panels.png` and `.pdf`.
- Status: actioned
- Links: `analysis/production_specs/fig3_synchrony_v1.json`, `analysis/plot_production_fig3.py`, `analysis/reports/fig3_imposed_vs_realised_panels.png`, `src/python/insurance_sim/production_figures.py`

## Open action queue

- Run the new ecologist-facing walkthrough in this order:
  - `README.md`
  - `analysis/reports/fig1_panels.png`
  - `analysis/reports/fig3_imposed_vs_realised_panels.png`
  - `analysis/reports/fig2_richness_scaling_mixed.png`
  - `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`
- Figure-by-figure numbered-filename transition completed for Figures 1–5. Continue with any additional display polish requested during manuscript integration.
- Use canonical `fig1_panels` outputs for future Figure 1 review; older `fig1_production_candidate` references are historical only.
- Before launching production grids, fast-forward or resync `~/papers/insurance_hypothesis` on `deep-server`, confirm login-shell `uv`, and run a lightweight project-native smoke test there.

## Deferred topics

- None yet.
