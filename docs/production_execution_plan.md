# Production Execution Plan

Date: 2026-05-14

Purpose: move the project from a draft manuscript based on exploratory/interim simulations to a submission-ready Oikos manuscript built from production-scale simulations, high-quality display items, and explicit scientist-in-the-loop sanity checks.

## Operating Principles

- Treat WSL as the control plane; run production simulation work on `deep-server`.
- Run long jobs inside `tmux` so WSL shutdowns do not interrupt simulations.
- Use 1000 replicates per scenario/slice for final-paper production grids unless a run is explicitly labelled as a smoke test, pilot, or stress-test subset.
- Keep project-specific run definitions, code, summaries, interpretation notes, and manuscript-relevant artifacts in this repository.
- Put bulky scratch/output material under `/data` on `deep-server` during production runs.
- Preserve scientific semantics by default. Changes to RNG/seeding policy, metric definitions, schemas, or canonical outputs require explicit decision records and before/after checks.

## Phase 0: Planning Checkpoint

Goal: make the current transition explicit and avoid losing the rationale behind the production campaign.

Tasks:

- Record the `deep-server` operating model and 1000-replicate convention in `docs/plan.md`, `docs/decisions.md`, `docs/q_and_a_interpretation.md`, and `docs/log/`.
- Keep the current ecologist-facing notes and production-planning notes reviewable as one coherent checkpoint.
- Commit and push the planning checkpoint before production harness work, if Barry wants a clean repository boundary.

Exit criteria:

- Production target, replicate convention, and remote execution model are documented.
- No current planning changes are left ambiguous or only in chat.

## Phase 1: Finish Scientist-Facing Artifact Review

Goal: finish Barry's systematic review of the current outputs before freezing the production run spec.

Primary artifacts:

- `README.md`
- `analysis/reports/fig1_panels.png`
- `analysis/reports/fig3_imposed_vs_realised_panels.png`
- `analysis/reports/fig2_richness_scaling_mixed.png`
- `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`
- Supplementary figures and diagnostic tables as needed.

Tasks:

- Continue adding Barry's questions and responses to `docs/q_and_a_interpretation.md`.
- Convert figure-level concerns into concrete tasks in `docs/interpretation_notes.md`.
- Separate visual-display issues from scientific/model issues.
- Identify which questions require new production simulations and which require only plotting/manuscript changes.

Exit criteria:

- Current display artifacts have been reviewed from the ecologist-facing side.
- The production run spec is driven by known scientific/display needs rather than by generic desire for "nicer" figures.

## Phase 2: Freeze The Production Grid Spec

Goal: define exactly what will be run before compute starts.

Initial production target:

- High-resolution Figure 1 response surfaces.
- S=4 mixed vs positive slopes.
- `phi=0.4`.
- 1000 replicates per scenario/slice.
- Denser `sigma_env` around the visible transition region.
- `rho_eff`-aware plotting and summaries.

Likely follow-on targets:

- Extend high-resolution surfaces to S=2 and S=8 if the S=4 comparison confirms the story and display gains.
- Refresh richness scaling if Figure 2 depends on production-level smoothness.
- Refresh persistence sensitivity only if the artifact review identifies a need; keep high-phi runs clearly labelled as stress tests.
- Re-run or extend controls (`positive_matched`, `mixed_narrow`, no-competition) only where they protect a manuscript claim.

Tasks:

- Write the production grid specification in a machine-readable form before launch.
- Define run IDs, output directories, expected row counts, and acceptance checks.
- Decide how dense the `sigma_env` and `rho_env` grids should be after the artifact review.
- Decide which outputs are canonical manuscript inputs and which are diagnostics.

Exit criteria:

- A reviewer could reconstruct why each production grid exists.
- Expected outputs and success checks are known before execution.

Status, 2026-05-14:

- Complete for the first S=4 Figure 1 production batch.
- Machine-readable spec: `analysis/production_specs/fig1_s4_highres_v1.json`.
- Expected size: 570 scenarios, 5700 shards, 570000 replicate-summary rows.
- Execution defaults: 1000 replicates per scenario, 100 replicates per shard, `run-pending --jobs 48`.

## Phase 3: Build The Production Harness

Goal: make large runs reproducible, resumable, and easy to monitor.

Tasks:

- Add a production runner that can split work into scenario/slice shards.
- Keep each shard output atomic and self-describing with run metadata.
- Add a combine/validate step that checks schema, expected scenario counts, replicate counts, missing shards, duplicate rows, `rho_eff`, and numerical guards.
- Add focused tests for the shard manifest, tiny shard execution, combine step, and clear failure modes.
- Add remote helper scripts for:
  - syncing/updating the `deep-server` checkout,
  - running a tiny project-native smoke test,
  - launching production jobs under `tmux`,
  - monitoring progress,
  - retrieving compact summaries/artifacts.

Exit criteria:

- `uv run pytest` and `uv run pyright` pass locally.
- A tiny local production-harness smoke test completes and validates.
- The harness does not depend on an interactive WSL session after launch.

## Phase 4: Remote Smoke And Benchmark

Goal: prove the whole remote path before expensive simulations.

Tasks:

- Sync or fast-forward the `deep-server` checkout.
- Use login-shell remote commands so `uv` resolves correctly.
- Run `uv sync --dev`, `uv run pytest`, and `uv run pyright` on `deep-server`.
- Launch a tiny `tmux`-managed smoke run using the production harness.
- Benchmark a small but representative shard to estimate wall time and choose safe concurrency.
- Confirm outputs land under the intended `/data` path and can be retrieved or summarized.

Exit criteria:

- Remote tests pass.
- A `tmux` smoke job survives detachment and produces validated outputs.
- We have a credible runtime estimate for the first production batch.

Status, 2026-05-14:

- Complete for the initial S=4 production batch.
- Remote tests and a tiny tmux smoke passed in `docs/log/110_production_harness.md`.
- Two production-shaped benchmarks passed in `docs/log/120_remote_benchmark.md`.
- Recommended first-batch defaults: 100 replicates per shard, `run-pending --jobs 48`.

## Phase 5: Production Batch 1

Goal: generate the first high-resolution production surfaces without overcommitting to the full campaign.

Run:

- S=4 mixed slopes.
- S=4 positive slopes.
- `phi=0.4`.
- 1000 replicates per scenario/slice.
- High-resolution `sigma_env` and `rho_env` grid as frozen in Phase 2.

Tasks:

- Freeze the high-resolution `sigma_env` and `rho_env` values in a machine-readable grid specification.
- Launch under `tmux` on `deep-server`.
- Monitor logs and shard completion.
- Validate combined output.
- Generate comparison plots against the current coarse/interim Figure 1 surfaces.
- Record interpretation notes before replacing manuscript/display defaults.

Exit criteria:

- Production Batch 1 validates cleanly.
- The ecological story is unchanged or any change is understood and documented.
- A decision is made about whether to extend production runs to other richness levels and controls.

Status, 2026-05-14:

- Complete for raw simulation and validation.
- Run ID: `fig1-s4-highres-v1`.
- Remote output: `/data/codex/scratch/insurance_hypothesis/fig1-s4-highres-v1`.
- Validation: 570000 rows, 570 scenarios, 5700 shards, 1000 replicates per scenario.
- Initial interpretation is in `docs/interpretation_notes.md` and `docs/log/140_fig1_production_batch.md`.
- Remaining Phase 5 work is display and comparison: build manuscript-quality production Figure 1, compare against the coarse/interim Figure 1, and decide whether to extend production surfaces to other richness levels.

## Phase 6: Production Campaign Expansion

Goal: run only the additional production grids needed to support the final manuscript claims.

Candidate batches:

- Richness extension: S=2 and S=8 mixed/positive surfaces.
- Richness-scaling refresh for Figure 2.
- Mechanism/synchrony refresh for Figure 3 if plotting or grid density requires it.
- Persistence sensitivity refresh for Figure 5 only if needed.
- Controls required to defend interpretation, especially sign-structure and slope-magnitude controls.

Tasks:

- Treat each batch as a small campaign with a manifest, tmux job, validation, plot generation, and interpretation update.
- Avoid expanding into unnecessary parameter space just because compute is available.

Exit criteria:

- Every main-text claim rests on production-level outputs or explicitly labelled diagnostics.
- Supplementary materials cover the main robustness questions without becoming a data dump.

## Phase 7: Display Item Rebuild

Goal: turn validated production outputs into submission-quality figures.

Tasks:

- Rebuild main figures from production summaries.
- Improve heatmaps/surfaces without hiding discrete simulation design.
- Use shared scales where comparisons require them.
- Ensure `rho_eff` and clipping are labelled or footnoted where relevant.
- Generate high-resolution PNG/PDF/SVG outputs as appropriate.
- Update `analysis/reports/`, `paper/manuscript/figures/`, captions, and interpretation notes.

Exit criteria:

- Main and supplementary figures are internally consistent, readable, and traceable to production run IDs.
- Captions accurately describe plotted data and aggregation.

## Phase 8: Manuscript Finalisation For Oikos

Goal: produce a submission-ready manuscript package.

Tasks:

- Update Methods with final production grid, replicate counts, environment, and validation details.
- Update Results to match production figures.
- Revisit Discussion with particular attention to relative stabilisation, imposed vs realised synchrony, and stress-test limits.
- Verify current Oikos author/submission requirements before final formatting.
- Rebuild manuscript outputs and run final checks.

Exit criteria:

- Manuscript, figures, captions, references, and supplementary material are mutually consistent.
- The submission package is ready for final human read-through and Oikos upload.

## First Cab Off The Rank

The first implementation task is **Phase 3: build the production harness**, but only after the planning checkpoint is cleanly recorded. The current `analysis/run_full_grid.py` is a good exploratory runner, but it is scenario-sequential and not ideal for 64-core, 1000-replicate production campaigns. The production harness should come before any full simulation launch so we get resumability, shard validation, tmux-safe execution, and clean provenance from the beginning.
