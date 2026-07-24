---
name: epic-to-feature
description: Decompose a planning-ready epic into 3-8 cohesive features with user value, technical scope, dependencies, sequencing, and open questions. Use when the user wants to break an epic into bounded capabilities before story refinement begins.
---

# Epic To Feature

## Overview

Use this skill once an epic has clear value, boundaries, and success criteria.

Read `references/epic-to-feature.md` before drafting the feature set.

## Workflow

1. Restate the epic context, boundaries, and linked evidence.
2. Identify the capability slices implied by the epic.
3. Draft 3-8 candidate features that collectively cover the epic.
4. Explain each feature's purpose and user or business value.
5. Capture technical scope, data needs, and major integration points.
6. Identify dependencies and sequencing across the feature set.
7. Surface assumptions, open questions, and unresolved decisions.
8. Validate coverage, overlap, and decomposability into stories.

## Output

Return a bounded feature set where each feature includes:

- title
- purpose and value
- technical scope and integration points
- dependencies and sequencing notes
- assumptions and open questions

## Notes

- Keep features cohesive and decomposable; avoid bundling unrelated outcomes.
- Stay above implementation-detail level.
- Use `TBD` explicitly when the epic inputs are incomplete.
