---
name: docx
description: "Convert Markdown documents (.md) into Word (.docx) using Pandoc. Use when a user asks for /docx, wants a Markdown-to-Word export, needs a styled DOCX via a reference template, or needs Markdown assets (images, includes) resolved into a DOCX deliverable."
---

# DOCX

Convert Markdown to `.docx` via Pandoc, with predictable defaults and a reusable script.

## Prerequisites
- `pandoc` installed and on `PATH`.
  - macOS: `brew install pandoc`
  - Ubuntu/Debian: `sudo apt-get install -y pandoc`

## Quick start
Convert a single Markdown file:
```bash
python3 /Users/carlo/.codex/skills/docx/scripts/md_to_docx.py path/to/input.md
```

Write to an explicit output path:
```bash
python3 /Users/carlo/.codex/skills/docx/scripts/md_to_docx.py path/to/input.md -o output/doc/my-doc.docx
```

Use a Word template for consistent styles (Pandoc reference doc):
```bash
python3 /Users/carlo/.codex/skills/docx/scripts/md_to_docx.py path/to/input.md --reference-doc path/to/reference.docx
```

Include a table of contents:
```bash
python3 /Users/carlo/.codex/skills/docx/scripts/md_to_docx.py path/to/input.md --toc
```

## Defaults and conventions
- Input format: `gfm` (GitHub-flavoured Markdown).
- Output default: `output/doc/<input-stem>.docx`.
- Resource resolution default: the input file’s directory is added to Pandoc’s `--resource-path` so relative image paths work when running from elsewhere.

## Passing Pandoc flags
For unusual cases, pass additional Pandoc arguments after `--`:
```bash
python3 /Users/carlo/.codex/skills/docx/scripts/md_to_docx.py input.md -- --number-sections
```

## Troubleshooting
- Missing images: add `--resource-path` entries for asset folders, or fix relative paths in Markdown.
- Styling doesn’t match expectations: supply a `--reference-doc` (a `.docx` whose styles you want to reuse).
- Markdown features not rendering (Mermaid/PlantUML/custom HTML): pre-render to images or simplify; Pandoc won’t magically execute embedded diagram languages for DOCX.

## Included script
- `scripts/md_to_docx.py`: wrapper around `pandoc` with sensible defaults for resource paths and output locations.
