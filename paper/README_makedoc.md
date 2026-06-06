# IH Paper Build Guide (`makedoc`)

This file explains how to build the Insurance Hypothesis manuscript from the external `makedoc` repository.

## Prerequisites

1. Run commands from the **makedoc repo root** (the repo that provides `make validate-config`, `make check`, and `make all`). On this Mac, that repo is at `/Users/bwbrook/work/makedoc`.
2. Ensure this manuscript repo exists at:

```bash
/Users/bwbrook/papers/insurance_hypothesis
```

3. Use this config:

```bash
CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml
```

The config contains the current manuscript/submission profiles:

- `ih_draft` (default): scoped lint for iterative drafting.
- `ih_submission`: strict full-lint gate for the double-blind main manuscript.
- `ih_submission_form_statements`: submission-system statements for copy-paste or separate upload.
- `ih_supplementary_info`: anonymous supplementary information.
- `ih_author_title_page`: unblinded title page and author statements.
- `ih_cover_letter`: editor-facing cover letter.

The config file itself is passed in via an absolute path, but the profile file references inside it are now **config-relative**.
This keeps the manuscript portable across macOS and Linux while still allowing external-path `makedoc` builds.

## Draft build workflow (fast iteration)

```bash
CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml

make validate-config CONFIG="$CONFIG"
make all CONFIG="$CONFIG"
```

Because `default_profile` is `ih_draft`, this path is suitable while manuscript text is still evolving.

## Strict submission gate (full lint)

To avoid editing tracked config files, create a temporary config that switches `default_profile` to `ih_submission`:

```bash
CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml
TMP_CONFIG=/tmp/ih_build_submission.yaml

python - <<'PY'
import yaml
from pathlib import Path

src = Path("/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml")
dst = Path("/tmp/ih_build_submission.yaml")

cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
cfg["default_profile"] = "ih_submission"
dst.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
print(f"Wrote {dst}")
PY

make validate-config CONFIG="$TMP_CONFIG"
make check CONFIG="$TMP_CONFIG"
make all CONFIG="$TMP_CONFIG"
```

## Notes

1. Canonical bibliography file is:
   - `/Users/bwbrook/papers/insurance_hypothesis/paper/references/ih_references.yaml`
2. Current known strict-lint blocker is manuscript citation syntax (`[REF]` placeholders and manual author-year formatting in `draft_ms_v2.md`).
3. Figure blocks are managed in:
   - `/Users/bwbrook/papers/insurance_hypothesis/paper/manuscript/text/figures.md`
