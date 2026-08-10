from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str) -> ModuleType:
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_docx_sanitizer_strips_linux_and_macos_local_paths(tmp_path: Path) -> None:
    sanitizer = _load_script("sanitize_docx_identity")
    docx = tmp_path / "submission.docx"
    xml = (
        '<root><pic descr="/Users/bwbrook/papers/insurance_hypothesis/figure.png" />'
        "<custom>/Users/bwbrook/work/makedoc/dist/paper/out.docx</custom>"
        "<legacy>/home/bwbrook/work/makedoc/dist/paper/out.docx</legacy>"
        "<tmp>/private/var/folders/abc/build-cache</tmp></root>"
    )
    with zipfile.ZipFile(docx, "w") as archive:
        archive.writestr("word/document.xml", xml)

    assert sanitizer.sanitize_docx(docx) is True
    assert sanitizer.docx_contains_identity(docx) == []

    with zipfile.ZipFile(docx, "r") as archive:
        cleaned = archive.read("word/document.xml").decode("utf-8")
    assert "descr=" not in cleaned
    assert "/Users/bwbrook" not in cleaned
    assert "/home/bwbrook" not in cleaned
    assert "/private/var/folders" not in cleaned


def test_review_package_target_guard_uses_macos_home_root(tmp_path: Path, monkeypatch) -> None:
    builder = _load_script("build_deidentified_review_package")
    package_root = tmp_path / "papers" / "de_identified_repos"
    target = package_root / "ih_package"
    monkeypatch.setenv("IH_REVIEW_PACKAGE_ROOT", str(package_root))

    builder.ensure_safe_target(target)

    outside = tmp_path / "other" / "ih_package"
    try:
        builder.ensure_safe_target(outside)
    except ValueError as exc:
        assert "Refusing unexpected package target outside" in str(exc)
    else:
        raise AssertionError("Expected target outside review package root to be rejected.")

    try:
        builder.ensure_safe_target(REPO_ROOT / "nested_package")
    except ValueError as exc:
        assert "Refusing to build package inside source repository" in str(exc)
    else:
        raise AssertionError("Expected target inside source repository to be rejected.")


def test_review_package_copies_only_runnable_reproduction_tests(tmp_path: Path) -> None:
    builder = _load_script("build_deidentified_review_package")
    assert hasattr(builder, "copy_review_tests")

    destination = tmp_path / "tests" / "python"
    builder.copy_review_tests(destination)

    assert (destination / "test_sim_basic.py").is_file()
    assert not (destination / "test_submission_helpers.py").exists()
