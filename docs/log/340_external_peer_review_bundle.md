# 340 – External peer-review dress-rehearsal bundle

## 2026-08-09

### Purpose

Assemble a self-contained source-component dossier for a critical external
reviewer who has no prior knowledge of the project, before the actual journal
submission.

### Bundle composition

- Anonymous main manuscript text, Table 1, bibliography/CSL, main captions,
  and Figures 1-5 in PNG and PDF formats.
- Anonymous Supporting Information overview, Tables S1-S5, supplementary
  captions, and Figures S1-S4 in PNG and PDF formats.
- A clearly separated unblinded editorial directory containing the title page,
  author metadata, cover letter, and submission-form statements.
- A freshly rebuilt anonymous reviewer reproducibility repository containing
  simulator/analysis source, production specifications, six compact production
  summary files, environment locks, and runnable tests.
- A reviewer brief, structured response template, provenance record, build
  metadata, consolidated captions, and a SHA-256 manifest.

Internal plans, logs, earlier reviews, Git metadata, remote scratch material,
and assembled manuscript PDF/DOCX outputs were excluded so that the exercise
remains a cold review. Individual figure PDFs were retained as display items.

### Verification

The anonymous reproducibility repository was rebuilt from the live working
tree and checked in isolation before its clean copy was packaged:

- `uv sync --python 3.12 --frozen --dev`: passed.
- `uv run pytest -q`: 48 passed.
- `uv run pyright`: no errors or warnings.
- `uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export`:
  completed from the included compact production summaries.

Final-bundle checks confirmed:

- all non-rewritten manuscript, Supporting Information, editorial, reference,
  display, and build components match their current source files byte-for-byte;
- the only manuscript-component rewrites are local figure links that now
  resolve within the bundle;
- all 18 display files match the current locked sources;
- no author identity or local-machine path markers occur outside the explicitly
  unblinded editorial directory;
- no Git repository, virtual environment, compiled cache, or assembled
  manuscript file is included;
- all 85 payload-file hashes in `MANIFEST.sha256` verify;
- the ZIP passes `unzip -t`, contains no absolute/traversal paths, and its
  extracted 86-file tree is byte-identical to the staging tree.

### Delivered archive

- Path: `/mnt/c/Temp/insurance_hypothesis_external_peer_review_2026-08-09.zip`
- Size: 75,057,987 bytes (71.6 MiB)
- SHA-256: `de3c2c9c5354c79d8c2336d2162455e59e5c6c5b1f431099905107201ca8a385`

### Next step

Obtain the independent review, then triage findings at the scientific and
editorial decision boundary. Do not reopen settled implementation or display
polish unless the review supplies material new evidence.
