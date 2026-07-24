---
name: feature-to-story
description: Convert a feature into 3-8 delivery-ready user stories with scope boundaries, acceptance criteria, file-impact guidance, sequencing, INVEST validation, and split patterns for oversized work. Use when the user asks for story refinement or wants a feature decomposed into implementable stories.
---

# Feature To Story

## Overview

Use this skill to create a bounded story set for one selected feature.

Read `references/feature-decomposition-process.md` first.
Use these supporting references as needed:

- `references/invest-criteria.md`
- `references/splitting-patterns.md`
- `references/user-story-format.md`

## Workflow

1. Confirm the feature goal, value, scope, and constraints.
2. If the feature is vague, run `$ambiguity-analysis` before decomposing it.
3. Map user workflows, roles, happy paths, and failure paths.
4. Establish candidate story boundaries as vertical slices.
5. Use the split patterns reference when a story is too large or mixed.
6. Validate each story against INVEST.
7. Write each story in the required format with explicit scope and
   out-of-scope notes.
8. Add concrete acceptance criteria, file-impact guidance, dependencies, and
   open questions.
9. Recommend implementation sequence, parallelization opportunities, and
   cross-story testing needs.

## Output

Return a story set where each story includes:

- user-story title
- scope and out-of-scope boundaries
- acceptance criteria
- likely file or layer impact
- dependencies and open questions
- bounded-scope notes

Also include:

- recommended sequence
- parallelization guidance
- integration risks and mitigation notes

## Notes

- Prefer user-visible slices over layer-by-layer decomposition.
- Keep the workflow output at acceptance-criteria-ready story level; do not
  generate executable tests here.
- Use the reference files instead of copying their content into the response.
