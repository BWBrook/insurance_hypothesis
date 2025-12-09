# AI Science Portal Template

A minimal harness for running autonomous, Codex-driven "automated science" projects in ecology, biodiversity, conservation, palaeontology, and global change. Each clone becomes a project-specific working repo; the human sets the question and high-level scope, Codex executes the work end-to-end.

## How to start a new project
1) Create/clone this template into a fresh repo and set the remote to the project repo.
2) Edit `AGENTS.md` fields under **Research field & scope** (System, Key idea).
3) Kick off the run with a bootstrap prompt similar to:
   - "You are an autonomous research assistant. Read AGENTS.md and global instructions, restate the research question and your high-level plan in your own words, then create docs/plan.md and docs/log/000_bootstrap.md. Do not ask me questions yet; propose a full plan first."
4) Let Codex proceed. The human should mainly respond "Proceed" unless specific questions are asked.

### Fast path: instantiate from GitHub template
If this repo is marked as a template (it is), you can create a fresh project repo and clone it locally in one step:

```bash
gh repo create <new-repo-name> --private --template BWBrook/ai-science-portal --clone
```

If you prefer not to mark the new repo private, switch `--private` to `--public` or `--internal`.

## Externalised memory (must stay current)
- `docs/plan.md`: single source of truth for current plan, milestones, and next actions.
- `docs/log/<phase>.md`: chronological narrative per phase (000 bootstrap, 010 data acquisition, 020 exploratory analysis, etc.).
- `docs/decisions.md`: irreversible choices with rationale and links to evidence.
- `docs/questions_for_human.md`: numbered, concise questions when Codex is blocked.
- Git history: small, meaningful commits with descriptive messages.

When resuming after a break, Codex should re-read `docs/plan.md`, the latest `docs/log/` entries, `docs/decisions.md`, and the last ~10 commits before acting—do not rely on chat history.

## Suggested workflow phases
- 000_bootstrap → define question, hypotheses, data candidates, and full plan.
- 010_data_acquisition → download, document sources/checksums in `data/README.md`, and build reproducible ingestion scripts.
- 020_exploratory_analysis → EDA, feature engineering, preliminary figures.
- 030_modelling → fit models per hypotheses, diagnostics, robustness checks.
- 040_reporting → finalize figures/tables, draft manuscript, reproducibility checks.
Adjust or add phases as needed; keep numbering monotonic.

## Data management
- `data/raw/`: immutable downloads; never hand-edit. Record source URLs, access dates, versions, and checksums in `data/README.md`.
- `data/processed/`: outputs from scripts only; scripts must be re-runnable.
- Avoid committing large/binary data unless essential; prefer scripted downloads.

## Environments & tooling
- R 4.5.2 with `pak`; capture deps with `renv`. Prefer R for domain-standard stats.
- Python 3.12 with `uv`; encode deps in `pyproject.toml`. Good for data plumbing and ML.
- Julia 1.12.2 only when clearly beneficial (e.g., heavy simulation).
- Add runnable entrypoints (e.g., `analysis/run_all.R` or `analysis/run_all.py`) and tests (`tests/`).

## Human interaction protocol
Codex should only stop for the human when blocked, facing a major conceptual fork, or detecting violated assumptions. In those cases:
1) Append numbered questions to `docs/questions_for_human.md` (with minimal context and options).
2) Summarize the blocking issue in the assistant message.
3) Wait. Human replies succinctly or edits the questions file, then says "Proceed".

## Commit discipline
- Commit after coherent steps (e.g., data ingestion script, EDA notebook, model implementation).
- Reference related log sections or decisions in commit messages when helpful.
- Keep CI-style commands reproducible locally (no hidden steps).

## Repo map (quick reminder)
- `docs/plan.md` – canonical plan
- `docs/log/` – phase journals
- `docs/decisions.md` – irreversible choices
- `docs/questions_for_human.md` – questions parking lot
- `data/raw/`, `data/processed/` – inputs/outputs
- `src/` – reusable code
- `analysis/` – notebooks, reports
- `manuscript/` – text and figures
- `tests/` – automated checks

Stay concise, automate everything, and prefer actions over questions.
