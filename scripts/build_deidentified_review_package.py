"""Build the anonymous code/data package for double-blind review.

The package is intentionally narrower than the working repository: it includes
only code, tests, environment files, production specs, and compact production
summaries needed to regenerate analysis outputs.
"""

from __future__ import annotations

import argparse
import json
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


README_TEXT = """# Insurance Hypothesis Simulation Review Package

This is an anonymous code and data package for peer review of a simulation study
on biodiversity insurance under environmental variability.

The package contains the minimum reproducibility materials needed to run the
Python simulation checks and regenerate analysis-facing figure/table outputs:

- `src/python/insurance_sim/`: simulator, metrics, diagnostics, and plotting helpers.
- `analysis/`: orchestration and plotting scripts.
- `analysis/production_specs/`: versioned production-grid specifications.
- `data/sim/production/*/summaries.parquet`: compact production summaries.
- `tests/python/`: non-interactive tests.
- `pyproject.toml` and `uv.lock`: Python 3.12 environment specification.
- `.python-version`: uv/Python version hint for Python 3.12.

It intentionally excludes manuscript source files, title-page metadata,
references, documentation logs, Git metadata, remote-compute scratch files, and
other material not required for code review.

## Requirements

- Python 3.12
- `uv`

## Quick Start

From this package directory:

```bash
uv sync --python 3.12 --frozen --dev
uv run pytest -q
uv run pyright
uv run python analysis/run_all.py --skip-guard-audit --skip-paper-export
```

The final command reads the included compact production summaries and writes
regenerated figures and CSV summaries under `analysis/reports/`.

## Notes

No empirical datasets are used. The included parquet files are simulation
summaries, not field or observational data.
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


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_sanitized_pyproject(target: Path) -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    text = text.replace('authors = [{name = "Barry W. Brook"}]', 'authors = [{name = "Anonymous"}]')
    (target / "pyproject.toml").write_text(text, encoding="utf-8")


def write_sanitized_specs(target: Path) -> None:
    out_dir = target / "analysis/production_specs"
    out_dir.mkdir(parents=True, exist_ok=True)
    for spec_path in sorted((REPO_ROOT / "analysis/production_specs").glob("*.json")):
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        execution = spec.get("execution")
        if isinstance(execution, dict):
            execution["host"] = "review-compute"
            execution["remote_root"] = "review-scratch"
        (out_dir / spec_path.name).write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")


def copy_production_summaries(target: Path) -> None:
    production_root = REPO_ROOT / "data/sim/production"
    if not production_root.exists():
        raise FileNotFoundError(f"Missing production summaries root: {production_root}")

    for summary in sorted(production_root.glob("*/summaries.parquet")):
        rel = summary.relative_to(REPO_ROOT)
        copy_file(summary, target / rel)


def write_review_files(target: Path) -> None:
    (target / "README.md").write_text(README_TEXT, encoding="utf-8")
    (target / "README_REVIEW.md").write_text(README_TEXT, encoding="utf-8")
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
    copy_tree(REPO_ROOT / "tests/python", target / "tests/python")
    target.joinpath("analysis").mkdir(exist_ok=True)
    for script in sorted((REPO_ROOT / "analysis").glob("*.py")):
        copy_file(script, target / "analysis" / script.name)
    write_sanitized_specs(target)
    copy_production_summaries(target)
    (target / "analysis/reports").mkdir(parents=True, exist_ok=True)

    write_manifest(target)
    hits = scan_text_identity(target)
    if hits:
        joined = "\n".join(hits)
        raise RuntimeError(f"Potential identifying text found in review package:\n{joined}")

    print(f"Wrote anonymous review package staging directory: {target}")
    if args.make_zip:
        print(f"Wrote anonymous review package archive: {make_zip(target)}")


if __name__ == "__main__":
    main()
