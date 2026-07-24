---
name: s3-recon
description: Consolidate duplicate copies of a content library into one canonical local folder and archive it to S3, deleting the redundant copies only after verified upload. Use whenever the user wants to merge/dedupe folders that exist in multiple places (local and/or S3), reconcile "which copy wins" across versions, prune unwanted formats, re-home an S3 prefix, or safely delete a folder that is "probably already backed up" — even if they don't say "recon" or "consolidate". Triggers include: duplicate sample packs/libraries, "merge these folders", "is everything in S3 before I delete this", freeing disk space on a full volume.
---

# S3 Recon: consolidate, archive, verify, delete

Take multiple partial/duplicate copies of a content library, produce one canonical local folder, upload it to S3, and delete the now-redundant copies — with a human-approved manifest gating every destructive step.

**Inputs to establish up front** (ask if not given):
- **Canonical folder** — the local path that will hold the merged result (usually the fullest existing copy).
- **Source(s)** — the other copies to merge in: local folders and/or existing S3 prefixes.
- **S3 destination** — bucket + key prefix for the canonical archive.
- **Prune rules** (optional) — formats/subfolders to strip (e.g. presets for DAWs the user doesn't use). Plain WAV/universal content always stays.

## Principles (apply to every phase)

- **Free operations first.** Listings, `find`, `du`, S3 `list_objects_v2` cost nothing. Build complete manifests from them before anything moves. A DEEP_ARCHIVE restore costs money and 12–48 hours — only consider it if the diff proves unique content exists.
- **Nothing is deleted without a manifest the human approved.** Each destructive phase produces a written manifest (a markdown file, kept as an asset) listing exactly what will be removed and why. Ambiguous cases get a recommendation, never a silent choice.
- **Deletes are two-stage.** During execution, "deleted" material moves to a staging trash on a roomy volume; the true `rm` happens only in the final phase, after the S3 upload is verified. Cross-volume moves are copy+delete, so they free space on the full volume immediately.
- **Verify with independent numbers.** After every mutation, count files/bytes and compare against the prediction from the manifest. After upload, list S3 independently (don't trust the uploader's own report) and compare count + bytes exactly.
- **Never stage on the volume you're trying to free.** Pick a staging path on a different disk with headroom, e.g. `/Volumes/coding/<effort>-staging/`.

## Phase 1 — Recon manifest (read-only)

Inventory the canonical folder and each source at the "item" level (a pack, album, project — the unit a human reasons about). For each item, decide which copy wins:

- **Newest version wins.** Parse versions from names, tolerating inconsistent encodings (`V1.71`, `V1_7`, `V1.5`).
- **Same version → fuller copy wins** (more files/bytes). The goal is "all the files".
- **Different host formats of the same title are different products** (e.g. Ableton vs Kontakt editions) — keep both.
- Watch for traps: trailing spaces in names, `(1)` duplicate files, "husk" folders holding only PDFs, extracted subsets of a fuller release, renamed products (same content, new title).

Write the manifest with sections: **COPY in** (source wins or source-only), **KEEP canonical / delete source dup**, **KEEP** (canonical-only), **DELETE from canonical** (superseded), **AMBIGUOUS** (numbered AMB-1…n, each with the evidence and a recommendation). End with predicted totals so execution can be verified later.

## Phase 2 — Prune manifest (read-only, optional)

If prune rules exist: census file extensions and folder names across all trees, identify unwanted-format material, then verify each hit **leaf-precisely** — prune the deepest folder that is purely unwanted, never a parent that also holds wanted content or a shared sample pool the wanted presets reference. Cover both levels: whole unwanted items AND format subfolders inside kept items. List every path with size/count; note wrapper dirs that become empty.

## Phase 3 — S3 diff (read-only, if content already exists in S3)

List the existing S3 prefix(es) (`scripts/s3_tools.py stats` / a full listing) and diff keys against the union of local copies. Classify anything S3-unique: is it real content or cache/derivative noise (`.asd`, thumbnails)? Recommend **restore** (only for substantive unique content) or **accept-loss**; the human ratifies.

## Phase 4 — Approval gate (HITL)

Present all manifests and every AMB recommendation to the human. Record their rulings and amendments in writing before executing anything. Do not proceed on silence.

## Phase 5 — Execute merge + prune

Script the approved manifest: copies in, prunes out (to staging trash, not `rm`), superseded canonical items to staging trash. Then verify: per-item file counts against manifest predictions, and total canonical count/size. Log the run. The old source folders stay untouched until Phase 7.

## Phase 6 — Upload and verify

This phase assumes the `s3-archiver` repo (`/Volumes/coding/dev/s3-archiver`); adapt if uploading by other means.

1. **Wire the folder in**: add the canonical path to `synch_folders.csv`. Add the *narrowest* entry that covers the content — a parent folder drags all its siblings into every future sync.
2. **Run scoped**: the archiver syncs every CSV row per run, and other rows may be stale. Run from the repo root (`.env` is cwd-relative) with a one-row CSV override:
   `SYNC_FOLDERS_FILE=/tmp/one-row.csv python3 s3-archiver.py`
   boto3 may be missing from system pythons — use a throwaway venv. For ~100 GB expect hours; run in background and poll the log's `Files uploaded:` lines.
3. **Baseline first**: the `.env` `EXCLUDE_PATTERNS` (`.asd`, `.DS_Store`, `Ableton Folder Info`, …) mean S3 will hold *fewer* objects than the raw local count. Before uploading, compute the filtered local count/bytes (mirror the excludes in `find`) — that is the number S3 must match.
4. **Verify independently**: `scripts/s3_tools.py verify --bucket B --prefix P --local DIR` — compares object count and total bytes against the excludes-filtered local tree, checks storage class, and spot-checks random keys byte-for-byte. Require an exact match and 0 uploader errors before declaring success.

## Phase 7 — Final deletions (HITL)

Present a final manifest: old local copies, old S3 prefix(es), staging trash — each with size, count, and the effect (space freed, storage cost saved). For old S3 objects in DEEP_ARCHIVE, check object ages (`s3_tools.py stats` prints the age range): deletion under 180 days incurs a pro-rated early-delete fee (~$0.001/GB-month remaining — state the estimate; it's usually cents). On approval:

- `rm -rf` the old local copies and staging.
- `scripts/s3_tools.py delete --bucket B --prefix P --yes` — batch-deletes and verifies the prefix is empty.
- Verify each path is gone and record freed space (local `df`, S3 GB, monthly cost).

## Record-keeping

Keep manifests, diff reports, and verification numbers as markdown files through the effort (e.g. in `.wayfinder/assets/` if run under a wayfinder map, else a scratch folder). Every resolution should state the numbers: predicted vs actual counts, bytes, error counts. Multi-day efforts fit naturally as a wayfinder map with one ticket per phase and the approval gates as HITL tickets.
