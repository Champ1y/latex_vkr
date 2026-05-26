#!/usr/bin/env python3
"""Replace wrong U+037E extraction mapping for semicolon glyphs in a PDF."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: fix_pdf_semicolon.py PDF", file=sys.stderr)
        return 2

    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    if shutil.which("mutool") is None:
        print("mutool is required to patch the PDF ToUnicode map", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="pdf-semicolon-") as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        unpacked = tmpdir / "unpacked.pdf"
        patched_unpacked = tmpdir / "patched-unpacked.pdf"
        patched = tmpdir / "patched.pdf"

        subprocess.run(
            ["mutool", "clean", "-d", str(pdf_path), str(unpacked)],
            check=True,
        )

        data = unpacked.read_bytes()
        patched_data = data.replace(b"<037E>", b"<003B>")
        patched_unpacked.write_bytes(patched_data)

        subprocess.run(
            ["mutool", "clean", "-gggg", "-z", "-f", "-i", str(patched_unpacked), str(patched)],
            check=True,
        )

        shutil.copyfile(patched, pdf_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
