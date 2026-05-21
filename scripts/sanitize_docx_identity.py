"""Strip local-path image metadata from generated DOCX submission files."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
import zipfile
from pathlib import Path


IDENTITY_PATTERNS = (
    "/home/bwbrook",
    "bwbrook",
    "barry w. brook",
    "barry.brook",
    "university of tasmania",
    "utas.edu",
    "0000-0002-2491-1517",
    "github.com/bwbrook",
)


def _sanitize_xml(xml: str) -> str:
    # Pandoc records source image paths in cNvPr descr attributes. These are
    # invisible in Word but can leak local usernames in double-blind review.
    xml = re.sub(r'\sdescr="[^"]*"', "", xml)
    return re.sub(r"/home/bwbrook/[^<\"]*", "[local path removed]", xml)


def sanitize_docx(path: Path) -> bool:
    with zipfile.ZipFile(path, "r") as source:
        entries = {info.filename: (info, source.read(info.filename)) for info in source.infolist()}

    changed = False
    for name, (info, payload) in list(entries.items()):
        if name.endswith(".xml"):
            xml = payload.decode("utf-8", errors="ignore")
            sanitized = _sanitize_xml(xml)
            if sanitized != xml:
                entries[name] = (info, sanitized.encode("utf-8"))
                changed = True

    if not changed:
        return False

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", dir=str(path.parent)) as tmp:
        tmp_path = Path(tmp.name)

    try:
        with zipfile.ZipFile(tmp_path, "w") as target:
            for info, payload in entries.values():
                target.writestr(info, payload)
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
    return True


def docx_contains_identity(path: Path) -> list[str]:
    found: list[str] = []
    lowered: list[str] = []
    with zipfile.ZipFile(path, "r") as archive:
        for name in archive.namelist():
            if name.endswith(".xml"):
                lowered.append(archive.read(name).decode("utf-8", errors="ignore").lower())
    combined = "\n".join(lowered)
    for pattern in IDENTITY_PATTERNS:
        if pattern in combined:
            found.append(pattern)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", nargs="+", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if identity-bearing strings remain after sanitizing.",
    )
    args = parser.parse_args(argv)

    exit_code = 0
    for docx in args.docx:
        changed = sanitize_docx(docx)
        status = "sanitized" if changed else "unchanged"
        print(f"{docx}: {status}")
        if args.check:
            found = docx_contains_identity(docx)
            if found:
                print(f"{docx}: remaining identity strings: {', '.join(found)}", file=sys.stderr)
                exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
