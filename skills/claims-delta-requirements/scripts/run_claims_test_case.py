#!/usr/bin/env python3
"""Run a claims automation pilot case from the test-run manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def default_manifest() -> Path:
    return repo_root() / "test-data" / "Claims" / "test-run" / "cases.json"


def load_manifest(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def find_case(manifest: dict, case_id: str) -> dict:
    for case in manifest["cases"]:
        if case["id"] == case_id:
            return case
    raise KeyError(case_id)


def output_path(case_id: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return repo_root() / "test-data" / "Claims" / "test-run" / "results" / f"{stamp}-{case_id}.md"


def run_case(case: dict) -> int:
    root = repo_root()
    reference = root / case["reference"]
    brief = root / case["brief"]
    output = output_path(case["id"])
    output.parent.mkdir(parents=True, exist_ok=True)

    generator = root / ".codex" / "skills" / "claims-delta-requirements" / "scripts" / "generate_claims_delta_draft.py"
    cmd = [
        sys.executable,
        str(generator),
        "--reference",
        str(reference),
        "--brief",
        str(brief),
        "--output",
        str(output),
    ]
    subprocess.run(cmd, check=True, cwd=root)

    print(f"case_id: {case['id']}")
    print(f"status: {case['status']}")
    print(f"baseline_class: {case['baseline_class']}")
    print(f"reference: {reference}")
    print(f"brief: {brief}")
    print(f"output: {output}")
    print(f"valid_pilot: {case.get('valid_pilot', False)}")
    if case.get("notes"):
        print("notes:")
        for item in case["notes"]:
            print(f"- {item}")
    if case.get("expected_review_focus"):
        print("expected_review_focus:")
        for item in case["expected_review_focus"]:
            print(f"- {item}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=default_manifest())
    parser.add_argument("--case", help="Case id to run. Defaults to manifest default_case.")
    parser.add_argument("--list", action="store_true", help="List available pilot cases.")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    if args.list:
        for case in manifest["cases"]:
            validity = "pilot" if case.get("valid_pilot", False) else "smoke"
            print(f"{case['id']}\t{case['status']}\t{validity}\t{case['baseline_class']}\t{case['description']}")
        return 0

    case_id = args.case or manifest["default_case"]
    case = find_case(manifest, case_id)
    return run_case(case)


if __name__ == "__main__":
    raise SystemExit(main())
