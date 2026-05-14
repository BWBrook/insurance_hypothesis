# 100 Deep Server Production Planning

Date: 2026-05-14

## What was attempted

- Reviewed `/home/bwbrook/work/nectar` as the control-plane reference for using `deep-server`, Nectar, Alien WSL, and `kunanyi`.
- Focused on the guidance relevant to the insurance-hypothesis production grids:
  - `README.md`
  - `docs/workflows/compute-resource-selection.md`
  - `docs/machines/deep-server.md`
  - `docs/workflows/project-integration.md`
  - `docs/workflows/smoke-tests.md`
  - `docs/workflows/data-placement.md`
  - `docs/workflows/wsl-control-plane.md`
- Ran the Nectar repo's lightweight checks from WSL:
  - `scripts/validate-repo.sh`
  - `scripts/check-access.sh deep-server`
  - `scripts/deep-server/inventory.sh`

## What worked

- The Nectar repo validated cleanly.
- `deep-server` SSH access passed through the repo's standard check.
- Inventory confirmed that `deep-server` is appropriate for the next production grids:
  - 64 logical CPUs from 2 x Intel Xeon E5-2683 v4 sockets
  - 125 GiB RAM, with about 123 GiB available during the scout
  - `/data` mounted with about 4.5 TiB available
  - Docker available
  - passwordless sudo enabled
  - no visible scheduler environment, so treat it as a standalone multicore host

## Notes

- The Nectar inventory script reports `uv=missing` because it probes a non-login shell. A login shell sees `uv` at `~/.local/bin/uv`, so remote project commands should use:

```bash
ssh deep-server 'bash -lc "cd /path/to/repo && uv run ..."'
```

- For heavy production grids, use WSL as the control plane, `deep-server` as the execution host, and `tmux` for long jobs.
- Keep bulky generated outputs and scratch material under `/data` on `deep-server`; keep scientific run definitions and interpretation records in this project repo.
- Barry set the production preference to 1000 replicates per scenario/slice for final-paper grids, replacing the earlier 300-500 exploratory suggestion.

## Next

- Finish the ecologist-facing output walkthrough before finalising the full production grid design.
- Before launching simulations, sync/update the remote `deep-server` checkout and run a project-native smoke test.
- First planned production run: high-resolution Figure 1 surfaces for S=4 mixed vs positive slopes, `phi=0.4`, 1000 replicates per scenario/slice, denser `sigma_env`/`rho_env`, and `rho_eff`-aware plotting.
