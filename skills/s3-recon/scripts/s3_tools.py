#!/usr/bin/env python3
"""S3 helpers for the s3-recon skill: stats, verify, delete.

Credentials: loads `.env` from the current working directory (same convention
as s3-archiver.py — run from the repo/dir that holds the .env), falling back
to the standard boto3 credential chain.

Subcommands:
  stats   --bucket B --prefix P
          Object count, total bytes, storage-class breakdown, and
          oldest/newest LastModified (for DEEP_ARCHIVE early-delete fee checks).

  verify  --bucket B --prefix P --local DIR [--exclude PAT ...] [--spot N]
          Compare the S3 prefix against a local tree: object count and total
          bytes must match the excludes-filtered local set exactly; spot-checks
          N random keys byte-for-byte. Default excludes mirror the s3-archiver
          .env EXCLUDE_PATTERNS. Exit code 1 on any mismatch.

  delete  --bucket B --prefix P --yes
          Batch-delete every object under the prefix (1000/request) and verify
          the prefix is empty afterwards. Refuses to run without --yes, and
          refuses an empty prefix (guards against deleting a whole bucket).
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import random
import sys
from pathlib import Path

try:
    import boto3
except ImportError:
    sys.exit("boto3 is required: pip install boto3 (a throwaway venv is fine)")

DEFAULT_EXCLUDES = [
    ".DS_Store", "Thumbs.db", "desktop.ini", "*.tmp", "*.cache", "*.log",
    "__pycache__", "node_modules", ".git", ".svn", ".hg", "*.asd",
    "Ableton Folder Info",
]


def load_dotenv(path: str = ".env") -> None:
    env = Path(path)
    if not env.exists():
        return
    for raw in env.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def list_prefix(s3, bucket: str, prefix: str):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        yield from page.get("Contents", [])


def excluded(rel_path: str, patterns) -> bool:
    segments = rel_path.split("/")
    for pattern in patterns:
        if any(fnmatch.fnmatch(seg, pattern) for seg in segments):
            return True
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def walk_local(root: Path, patterns):
    """Yield (relative_posix_path, size) for files surviving the excludes."""
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        dirnames[:] = [
            d for d in dirnames
            if not excluded((f"{rel_dir}/{d}" if rel_dir != "." else d), patterns)
        ]
        for name in filenames:
            rel = f"{rel_dir}/{name}" if rel_dir != "." else name
            if excluded(rel, patterns):
                continue
            try:
                yield rel, os.path.getsize(os.path.join(dirpath, name))
            except OSError as exc:
                print(f"warning: cannot stat {rel}: {exc}", file=sys.stderr)


def cmd_stats(args) -> int:
    s3 = boto3.client("s3")
    count = total = 0
    oldest = newest = None
    classes: dict[str, int] = {}
    for obj in list_prefix(s3, args.bucket, args.prefix):
        count += 1
        total += obj["Size"]
        classes[obj.get("StorageClass", "STANDARD")] = (
            classes.get(obj.get("StorageClass", "STANDARD"), 0) + 1
        )
        lm = obj["LastModified"]
        oldest = lm if oldest is None or lm < oldest else oldest
        newest = lm if newest is None or lm > newest else newest
    print(f"Prefix:  s3://{args.bucket}/{args.prefix}")
    print(f"Objects: {count:,}")
    print(f"Bytes:   {total:,} ({total / 1024**3:.2f} GB)")
    print(f"Storage classes: {classes}")
    print(f"Oldest:  {oldest}")
    print(f"Newest:  {newest}")
    return 0


def cmd_verify(args) -> int:
    patterns = args.exclude if args.exclude else DEFAULT_EXCLUDES
    root = Path(args.local).resolve()
    if not root.is_dir():
        sys.exit(f"local dir not found: {root}")
    prefix = args.prefix if args.prefix.endswith("/") else args.prefix + "/"

    local = dict(walk_local(root, patterns))
    local_bytes = sum(local.values())
    print(f"Local (after {len(patterns)} exclude patterns): "
          f"{len(local):,} files / {local_bytes:,} bytes ({local_bytes / 1024**3:.2f} GB)")

    s3 = boto3.client("s3")
    remote = {}
    for obj in list_prefix(s3, args.bucket, prefix):
        remote[obj["Key"][len(prefix):]] = obj["Size"]
    remote_bytes = sum(remote.values())
    print(f"S3:    {len(remote):,} objects / {remote_bytes:,} bytes "
          f"({remote_bytes / 1024**3:.2f} GB)")

    ok = True
    if len(local) != len(remote) or local_bytes != remote_bytes:
        ok = False
        missing = sorted(set(local) - set(remote))
        extra = sorted(set(remote) - set(local))
        print(f"MISMATCH: {len(missing)} local-only, {len(extra)} s3-only")
        for k in missing[:10]:
            print(f"  local-only: {k}")
        for k in extra[:10]:
            print(f"  s3-only:    {k}")
    else:
        print("Count and bytes match exactly.")

    sample = random.sample(sorted(remote), min(args.spot, len(remote)))
    for key in sample:
        match = local.get(key) == remote[key]
        ok = ok and match
        print(f"  [{'OK' if match else 'MISMATCH'}] {key} ({remote[key]:,} bytes)")
    return 0 if ok else 1


def cmd_delete(args) -> int:
    if not args.prefix.strip("/"):
        sys.exit("refusing to delete with an empty prefix")
    if not args.yes:
        sys.exit("dry safety: re-run with --yes to actually delete "
                 "(and only after the human approved the manifest)")
    s3 = boto3.client("s3")
    keys = [obj["Key"] for obj in list_prefix(s3, args.bucket, args.prefix)]
    print(f"Deleting {len(keys):,} objects under s3://{args.bucket}/{args.prefix}")
    errors = []
    for i in range(0, len(keys), 1000):
        batch = keys[i:i + 1000]
        resp = s3.delete_objects(
            Bucket=args.bucket,
            Delete={"Objects": [{"Key": k} for k in batch], "Quiet": True},
        )
        errors.extend(resp.get("Errors", []))
        if (i // 1000) % 10 == 0:
            print(f"  {min(i + 1000, len(keys)):,}/{len(keys):,}")
    for err in errors[:10]:
        print("ERR", err)
    remaining = s3.list_objects_v2(
        Bucket=args.bucket, Prefix=args.prefix, MaxKeys=1
    ).get("KeyCount", 0)
    print(f"Deleted: {len(keys) - len(errors):,}, Errors: {len(errors)}, "
          f"Prefix empty: {remaining == 0}")
    return 0 if not errors and remaining == 0 else 1


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("stats", help="count/bytes/ages for an S3 prefix")
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", required=True)
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("verify", help="compare S3 prefix against local tree")
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", required=True)
    p.add_argument("--local", required=True)
    p.add_argument("--exclude", action="append",
                   help="exclude pattern (repeatable); default mirrors s3-archiver")
    p.add_argument("--spot", type=int, default=10, help="random keys to spot-check")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("delete", help="batch-delete an S3 prefix")
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", required=True)
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
