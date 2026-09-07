# Insurance hypothesis manuscript builds (`makedoc`)

The manuscript sources and generated submission components are kept together in
this repository. `makedoc` remains the external rendering tool, but all six
profiles write to:

```text
/home/bwbrook/papers/insurance_hypothesis/build/oikos_submission_aug_2026
```

The portable path recorded in `settings/build.yaml` is
`../../build/oikos_submission_aug_2026`, resolved relative to that configuration
file. The generated `build/` tree is deliberately ignored by Git; source files
and build settings remain the reproducible record.

## WSL build workflow

Run profiles sequentially because they share `makedoc` cache state:

```bash
REPO=/home/bwbrook/papers/insurance_hypothesis
MAKEDOC=/home/bwbrook/work/makedoc
CONFIG="$REPO/paper/settings/build.yaml"

for PROFILE in \
  ih_draft \
  ih_submission \
  ih_submission_form_statements \
  ih_supplementary_info \
  ih_author_title_page \
  ih_cover_letter
do
  make -C "$MAKEDOC" check CONFIG="$CONFIG" PROFILE="$PROFILE"
done

uv run --project "$REPO" --frozen python \
  "$REPO/scripts/sanitize_docx_identity.py" --check \
  "$REPO/build/oikos_submission_aug_2026/insurance_hypothesis_blinded_main.docx" \
  "$REPO/build/oikos_submission_aug_2026/insurance_hypothesis_supplementary_info.docx"

make -C "$MAKEDOC" manifest CONFIG="$CONFIG" PROFILE=ih_submission
make -C "$MAKEDOC" manifest CONFIG="$CONFIG" PROFILE=ih_supplementary_info
```

The anonymous main manuscript and Supporting-information DOCX files must be
sanitized after each rebuild because Pandoc can embed local source paths in
otherwise invisible image metadata. Refresh their manifests afterwards so the
recorded hashes describe the sanitized upload candidates.

## Profiles

- `ih_draft`: complete unblinded working manuscript.
- `ih_submission`: anonymous, double-spaced main manuscript and golden-contract
  target.
- `ih_submission_form_statements`: submission-system statements.
- `ih_supplementary_info`: anonymous Supporting information.
- `ih_author_title_page`: unblinded title page and author statements.
- `ih_cover_letter`: editor-facing cover letter.

The canonical bibliography is `references/ih_references.yaml`; figure sources
are the accepted display suite in `../analysis/reports/`.
