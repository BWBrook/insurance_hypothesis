"""Build the anonymous code/data package for double-blind review.

The package is intentionally narrower than the working repository: it includes
only code, tests, environment files, production specs, and compact production
summaries needed to regenerate analysis outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE_ROOT = Path("~/papers/de_identified_repos")
DEFAULT_TARGET_NAME = "ih_package"

TEXT_IDENTITY_NEEDLES = [
    "Barry",
    "Brook",
    "University",
    "Tasmania",
    "UTAS",
    "utas",
    "ORCID",
    "github.com",
    "BWBrook",
    "bwbrook",
    "/home/",
    "/Users/",
    "/mnt/",
    "/private/var/folders/",
]


ANALYSIS_FILES = (
    "check_numerical_guards.py",
    "production_grid.py",
    "run_all.py",
)

GUARD_REPORT_FILES = (
    "numerical_guard_rates.csv",
    "numerical_guard_rates_summary.csv",
    "numerical_guard_rates_summary.md",
)

EXPECTED_REPORT_FILES = tuple(
    f"{stem}{suffix}"
    for stem in (
        "fig1_panels",
        "fig2_richness_scaling_mixed",
        "fig3_imposed_vs_realised_panels",
        "fig4_weighted_balance_boundary",
        "fig5_phi_sensitivity_sigma0.5_extended",
        "figS1_production_mixed_cv_total",
        "figS2_production_mixed_phi_ldm",
        "figS3_positive_matched_control",
        "figS4_production_species_cv_vs_rho",
    )
    for suffix in (".png", ".pdf", "_summary.csv")
) + (
    "variance_decomposition_fig2_mixed_summary.csv",
    "variance_decomposition_fig2_mixed_selected_summary.csv",
    *GUARD_REPORT_FILES,
)


README_TEXT = """# Insurance Hypothesis Simulation Review Package

This is an anonymous code and data package for peer review of a simulation study
on biodiversity insurance under environmental variability.

The package contains the minimum reproducibility materials needed to inspect
the reported simulation evidence, run the Python checks, and regenerate the
analysis-facing figure and table outputs:

- `src/python/insurance_sim/`: simulator, metrics, diagnostics, and plotting helpers.
- `analysis/`: orchestration and plotting scripts.
- `analysis/production_specs/`: versioned production-grid specifications.
- `data/sim/production/*/summaries.parquet`: compact production summaries.
- `analysis/reports/numerical_guard*`: the retained numerical-guard diagnostic.
- `tests/python/`: non-interactive tests.
- `pyproject.toml` and `uv.lock`: Python 3.12 environment specification.
- `.python-version`: uv/Python version hint for Python 3.12.

It intentionally excludes manuscript source files, title-page metadata,
references, documentation logs, Git metadata, remote-compute scratch files, and
other material not required for code review.

No empirical datasets are used. The parquet files are replicate-level
summaries of simulated trajectories, not field or observational data.

## Requirements

- Python 3.12
- `uv`

## Quick Start

From this package directory:

```bash
sha256sum -c SHA256SUMS.txt
uv sync --python 3.12 --frozen --dev
uv run --frozen pytest -q
uv run --frozen pyright
uv run --frozen python analysis/run_all.py
uv run --frozen python analysis/check_numerical_guards.py
sha256sum -c EXPECTED_OUTPUT_SHA256SUMS.txt
```

Run the first checksum command before generating outputs; it verifies the
contents supplied for review. `run_all.py` reads the included compact summaries
and writes nine PNGs, nine PDFs, nine figure-summary CSVs, and two variance-
decomposition CSVs under `analysis/reports/`. It does not rerun the production
simulations. Figure S2 masks zero-forcing synchrony as undefined because the
post-burn-in abundances are constant; those means and standard deviations are
missing in its display-summary CSV. The supplied replicate rows are preserved.

`check_numerical_guards.py` is a separate deterministic stress diagnostic. It
runs 30 replicates for each of three scenarios (90 trajectories in total) with
seed 12345 and overwrites the three included `numerical_guard*` files. These
full-trajectory checks are distinct from the post-burn-in floor frequencies in
the production summaries.

`EXPECTED_OUTPUT_SHA256SUMS.txt` records the reference hashes for all 32 outputs.
Byte-identical output is expected with the locked environment used to prepare
the package. On another operating system or numerical/graphics stack, compare
the numerical content and rendered figures if a byte hash differs.

## Validate the supplied production summaries

Each JSON specification defines its complete scenario grid, fixed model
constants, replicate count, shard size, and base seed. The following validation
creates manifests from those specs and checks every supplied row and scenario
without rerunning simulations:

```bash
mkdir -p validation
for spec in analysis/production_specs/*.json; do
  name=$(basename "$spec" .json)
  mkdir -p "validation/$name"
  uv run --frozen python analysis/production_grid.py create \\
    --spec "$spec" --output "validation/$name/manifest.json"
  uv run --frozen python analysis/production_grid.py validate \\
    --manifest "validation/$name/manifest.json" \\
    --combined "data/sim/production/$name/summaries.parquet"
done
```

The expected total is 1,196 scenarios and 1,196,000 replicate summaries across
the seven grids.

## Reconstruct the production inventory and floor summary

The following read-only aggregation reconstructs the row and scenario counts in
Table S1 and the maxima in Table S2. `mean_extinction_freq` is the recorded
post-burn-in numerical-floor frequency for each replicate.

```bash
uv run --frozen python - <<'PY'
from pathlib import Path
import pandas as pd

total_rows = 0
total_scenarios = 0
for path in sorted(Path("data/sim/production").glob("*/summaries.parquet")):
    data = pd.read_parquet(path)
    by_scenario = data.groupby("scenario_id", sort=False)["mean_extinction_freq"].mean()
    maximum_id = by_scenario.idxmax()
    location = data.loc[data["scenario_id"].eq(maximum_id)].iloc[0]
    rows = len(data)
    scenarios = data["scenario_id"].nunique()
    total_rows += rows
    total_scenarios += scenarios
    fields = {
        key: location[key]
        for key in ("slope_mode", "n_species", "sigma_env", "rho_eff", "phi")
    }
    print(
        path.parent.name,
        f"scenarios={scenarios}",
        f"rows={rows}",
        f"max_scenario_mean_floor={by_scenario.max():.9g}",
        f"max_replicate_floor={data['mean_extinction_freq'].max():.9g}",
        f"location={fields}",
    )
print(f"TOTAL scenarios={total_scenarios} rows={total_rows}")
PY
```

Table S3 is reconstructed directly by `analysis/run_all.py` as
`variance_decomposition_fig2_mixed_selected_summary.csv`; the full supporting
aggregation is written beside it.

## Full production regeneration

The compact summaries are supplied so that reviewing the evidence does not
require a large simulation run. A full regeneration is nevertheless available
from every spec. It is compute intensive and should be run on suitable compute:

```bash
mkdir -p full-runs
for spec in analysis/production_specs/*.json; do
  name=$(basename "$spec" .json)
  work="full-runs/$name"
  mkdir -p "$work"
  uv run --frozen python analysis/production_grid.py create \\
    --spec "$spec" --output "$work/manifest.json"
  uv run --frozen python analysis/production_grid.py run-pending \\
    --manifest "$work/manifest.json" --jobs 1
  uv run --frozen python analysis/production_grid.py combine \\
    --manifest "$work/manifest.json" \\
    --output "$work/summaries.parquet" \\
    --validation-output "$work/validation.json"
  uv run --frozen python analysis/production_grid.py validate \\
    --manifest "$work/manifest.json" --combined "$work/summaries.parquet"
done
```

## Manuscript figure mapping

The manuscript presents the matched-control evidence first. Generated filenames
retain their production identifiers; their numeric prefixes are not the current
manuscript figure numbers.

| Manuscript figure | Generated image in `analysis/reports/` |
| --- | --- |
| Figure 1: matched signs and weighted boundary | `fig4_weighted_balance_boundary.png` |
| Figure 2: realised synchrony | `fig3_imposed_vs_realised_panels.png` |
| Figure 3: environmental-variance contrast | `fig1_panels.png` |
| Figure 4: richness assembly sequence | `fig2_richness_scaling_mixed.png` |
| Figure 5: fixed-innovation persistence gradient | `fig5_phi_sensitivity_sigma0.5_extended.png` |

The four Supporting-information figures keep their S1–S4 numbering. Each image
also has a PDF version with the same filename stem.

The deterministic per-replicate seeds make results independent of shard order.
Exact parquet bytes can still depend on the Python and PyArrow environment;
validate row content and regenerated scientific outputs when comparing across
platforms.
"""


def review_package_root() -> Path:
    """Return the allowed local root for anonymous review packages."""
    root = os.environ.get("IH_REVIEW_PACKAGE_ROOT")
    return Path(root).expanduser() if root else DEFAULT_PACKAGE_ROOT.expanduser()


def default_target() -> Path:
    return review_package_root() / DEFAULT_TARGET_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the anonymous review package")
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target(),
        help="Staging directory to create",
    )
    parser.add_argument(
        "--zip",
        dest="make_zip",
        action="store_true",
        help="Also create a .zip archive next to the staging directory",
    )
    return parser.parse_args()


def ensure_safe_target(target: Path) -> None:
    resolved = target.expanduser().resolve()
    expected_parent = review_package_root().resolve()
    if resolved == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved.parents:
        raise ValueError(f"Refusing to build package inside source repository: {resolved}")
    if expected_parent not in resolved.parents:
        raise ValueError(f"Refusing unexpected package target outside {expected_parent}: {resolved}")


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def copy_review_tests(dst: Path) -> None:
    """Copy tests that can run inside the intentionally narrow review package."""
    shutil.copytree(
        REPO_ROOT / "tests/python",
        dst,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            "test_submission_helpers.py",
        ),
    )


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_sanitized_pyproject(target: Path) -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    text = text.replace('authors = [{name = "Barry W. Brook"}]', 'authors = [{name = "Anonymous"}]')
    (target / "pyproject.toml").write_text(text, encoding="utf-8")


def copy_production_summaries(target: Path) -> None:
    production_root = REPO_ROOT / "data/sim/production"
    if not production_root.exists():
        raise FileNotFoundError(f"Missing production summaries root: {production_root}")

    for summary in sorted(production_root.glob("*/summaries.parquet")):
        rel = summary.relative_to(REPO_ROOT)
        copy_file(summary, target / rel)


def copy_guard_reports(target: Path) -> None:
    """Copy the small retained evidence from the separate guard diagnostic."""
    for name in GUARD_REPORT_FILES:
        copy_file(
            REPO_ROOT / "analysis/reports" / name,
            target / "analysis/reports" / name,
        )


def write_review_files(target: Path) -> None:
    (target / "README.md").write_text(README_TEXT, encoding="utf-8")
    (target / ".python-version").write_text("3.12\n", encoding="utf-8")
    (target / ".gitignore").write_text(
        "\n".join(
            [
                ".venv/",
                "__pycache__/",
                "*.pyc",
                ".pytest_cache/",
                "analysis/reports/",
                "*.zip",
                "",
            ]
        ),
        encoding="utf-8",
    )


def scan_text_identity(target: Path) -> list[str]:
    hits: list[str] = []
    ignored_suffixes = {".parquet", ".png", ".pdf", ".docx", ".pyc", ".zip"}
    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() in ignored_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for needle in TEXT_IDENTITY_NEEDLES:
            if needle in text:
                hits.append(f"{path.relative_to(target)}: {needle}")
    return hits


def write_manifest(target: Path) -> None:
    files = sorted(
        str(path.relative_to(target))
        for path in target.rglob("*")
        if path.is_file() and ".venv" not in path.parts
    )
    (target / "REVIEW_PACKAGE_MANIFEST.txt").write_text("\n".join(files) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_package_checksums(target: Path) -> None:
    """Write checksums for supplied files, excluding the checksum file itself."""
    checksum_path = target / "SHA256SUMS.txt"
    files = sorted(
        path
        for path in target.rglob("*")
        if path.is_file() and path != checksum_path and ".venv" not in path.parts
    )
    lines = [f"{sha256(path)}  {path.relative_to(target)}" for path in files]
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_expected_output_checksums(target: Path) -> None:
    """Record reference hashes without copying the generated display suite."""
    lines = []
    for name in EXPECTED_REPORT_FILES:
        source = REPO_ROOT / "analysis/reports" / name
        if not source.is_file():
            raise FileNotFoundError(f"Missing canonical analysis output: {source}")
        lines.append(f"{sha256(source)}  analysis/reports/{name}")
    (target / "EXPECTED_OUTPUT_SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def make_zip(target: Path) -> Path:
    archive = target.with_suffix(".zip")
    if archive.exists():
        archive.unlink()
    base_name = str(target)
    zip_path = Path(shutil.make_archive(base_name, "zip", root_dir=target.parent, base_dir=target.name))
    return zip_path


def main() -> None:
    args = parse_args()
    target = args.target.expanduser()
    ensure_safe_target(target)

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    write_review_files(target)
    write_sanitized_pyproject(target)
    copy_file(REPO_ROOT / "uv.lock", target / "uv.lock")
    copy_tree(REPO_ROOT / "src/python/insurance_sim", target / "src/python/insurance_sim")
    copy_review_tests(target / "tests/python")
    target.joinpath("analysis").mkdir(exist_ok=True)
    for name in ANALYSIS_FILES:
        copy_file(REPO_ROOT / "analysis" / name, target / "analysis" / name)
    copy_tree(REPO_ROOT / "analysis/production_specs", target / "analysis/production_specs")
    copy_production_summaries(target)
    (target / "analysis/reports").mkdir(parents=True, exist_ok=True)
    copy_guard_reports(target)

    write_expected_output_checksums(target)
    write_manifest(target)
    write_package_checksums(target)
    hits = scan_text_identity(target)
    if hits:
        joined = "\n".join(hits)
        raise RuntimeError(f"Potential identifying text found in review package:\n{joined}")

    print(f"Wrote anonymous review package staging directory: {target}")
    if args.make_zip:
        print(f"Wrote anonymous review package archive: {make_zip(target)}")


if __name__ == "__main__":
    main()
