#!/usr/bin/env python3
"""
Convert Markdown (.md) to Word (.docx) using Pandoc.

Designed to be used by the /docx skill.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _build_pandoc_command(
    *,
    input_md: Path,
    output_docx: Path,
    reference_doc: Path | None,
    toc: bool,
    resource_paths: list[Path],
    extra_args: list[str],
) -> list[str]:
    cmd: list[str] = [
        "pandoc",
        str(input_md),
        "--from",
        "gfm",
        "--to",
        "docx",
        "--output",
        str(output_docx),
    ]

    if toc:
        cmd.append("--toc")

    if reference_doc is not None:
        cmd.extend(["--reference-doc", str(reference_doc)])

    if resource_paths:
        cmd.extend(["--resource-path", os.pathsep.join(str(p) for p in resource_paths)])

    if extra_args:
        cmd.extend(extra_args)

    return cmd


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to DOCX using Pandoc.",
    )
    parser.add_argument("input", type=Path, help="Input Markdown file (.md)")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output DOCX path. Default: output/doc/<input-stem>.docx",
    )
    parser.add_argument(
        "--reference-doc",
        type=Path,
        help="Optional reference DOCX to control styles (Pandoc --reference-doc).",
    )
    parser.add_argument(
        "--toc",
        action="store_true",
        help="Include a table of contents (Pandoc --toc).",
    )
    parser.add_argument(
        "--resource-path",
        action="append",
        type=Path,
        default=[],
        help=(
            "Additional resource path(s) for images/includes. Repeatable. "
            "Defaults to the input Markdown's folder."
        ),
    )
    parser.add_argument(
        "--",
        dest="extra_args",
        nargs=argparse.REMAINDER,
        help="Pass through additional arguments to pandoc after `--`.",
    )

    args = parser.parse_args(argv)

    input_md: Path = args.input
    if input_md.suffix.lower() not in {".md", ".markdown"}:
        print(f"[docx] Expected a Markdown file, got: {input_md}", file=sys.stderr)
        return 2
    if not input_md.exists():
        print(f"[docx] Input file not found: {input_md}", file=sys.stderr)
        return 2

    output_docx: Path
    if args.output:
        output_docx = args.output
    else:
        output_docx = Path("output") / "doc" / f"{input_md.stem}.docx"

    output_docx.parent.mkdir(parents=True, exist_ok=True)

    reference_doc: Path | None = args.reference_doc
    if reference_doc is not None and not reference_doc.exists():
        print(f"[docx] Reference DOCX not found: {reference_doc}", file=sys.stderr)
        return 2

    if shutil.which("pandoc") is None:
        print("[docx] pandoc not found on PATH.", file=sys.stderr)
        print("       Install it (e.g. `brew install pandoc`) and re-run.", file=sys.stderr)
        return 127

    resource_paths: list[Path] = [input_md.parent]
    for p in args.resource_path:
        resource_paths.append(p)

    extra_args: list[str] = []
    if args.extra_args:
        extra_args = [item for item in args.extra_args if item != "--"]

    cmd = _build_pandoc_command(
        input_md=input_md,
        output_docx=output_docx,
        reference_doc=reference_doc,
        toc=bool(args.toc),
        resource_paths=resource_paths,
        extra_args=extra_args,
    )

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"[docx] pandoc failed (exit {exc.returncode}).", file=sys.stderr)
        return exc.returncode

    print(f"[docx] Wrote: {output_docx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
