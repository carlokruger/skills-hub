---
name: claims-delta-requirements
description: Draft or refine claims-project requirement documents by starting from the closest signed-off reference implementation, identifying only the delta for the new claim type, action, or report, and then filling the established format. Use when the user has similar claims requirements to replicate, wants variance-only output, or needs a new claims requirement aligned to existing signed-off examples.
---

# Claims Delta Requirements

## Overview

Use this skill for the claims project when the real task is not greenfield
authoring but controlled adaptation of an existing signed-off requirement.

Read `references/archetypes.md` first.
If available, start from a completed delta brief instead of freeform notes:

- `references/claims-delta-brief-template.md`
- `references/claims-delta-brief-example-lbc-is345-exclusion.md`

Then select the closest reference artifact:

- `references/lbc-sickness-claim-assessment.md`
- `references/lbc-sickness-variance-only.md`
- `references/dc-sla-alert-report.md`

Use `scripts/generate_claims_delta_draft.py` when you need a deterministic
first-pass draft from a reference artifact and a completed delta brief.

Default baseline classes:

- `dc-funeral` for death-claims baseline work
- `lbc-lump-sum-dread` for LBC lump-sum work
- `lbc-recurring-sickness` for LBC recurring-payment work

## Workflow

1. Classify the request into an archetype:
   - claim-step requirement
   - variance-only requirement
   - report or analytics requirement
2. Choose the baseline class before choosing the exact reference page:
   - death claims -> funeral baseline
   - LBC lump sum -> dread disease baseline
   - LBC recurring -> sickness baseline
3. Normalize the input into the delta-brief structure if the user did not
   already provide one.
4. Pick the closest signed-off reference artifact within that baseline class
   rather than drafting from a
   blank page.
5. Extract the stable structure that should be preserved.
6. Identify the true delta:
   - claim type or benefit
   - action or step name
   - changed decision logic
   - changed fields, thresholds, or routing
   - changed calculations, metrics, or report layout
   - changed dependencies, comms, or security
7. Preserve unchanged sections unless the delta explicitly affects them.
8. Rewrite the target sections from the delta brief first; use the reference as a structural scaffold, not as copy-forward source text.
9. Check carefully for copy-forward mistakes in names, Jira identifiers, claim
   types, benefit codes, and step labels.
10. Produce either:
   - a final requirement document in the established format
   - or a variance-only artifact if the user explicitly wants just the delta

## Script

Generate a first-pass draft:

```bash
python .codex/skills/claims-delta-requirements/scripts/generate_claims_delta_draft.py \
  --reference <reference.md> \
  --brief <claims-delta-brief.md> \
  --output <draft.md>
```

Then review the draft for copied identifiers, stale claim names, and whether
the delta propagated into acceptance and testing sections.

## PO Working Model

Follow the project's observed authoring model:

1. Read the process baseline.
2. Identify the specific process step.
3. Use the signed-off requirement for that step as the reference artifact.
4. Apply only the variance for the new benefit, claim type, or report.

Do not treat each page as an isolated requirement. The process and baseline
class determine the correct reference point.

## Output

When producing a full requirement, return:

- the established document structure for the chosen archetype
- claim-specific or report-specific content filled from the delta
- explicit assumptions and unresolved questions

When producing a variance-only artifact, return:

- reference artifact used
- unchanged assumptions carried forward
- changed fields and wording only
- implementation and testing hot spots caused by the delta

## Notes

- Treat the reference artifact as the baseline contract for tone, headings, and
  coverage depth.
- Prefer minimal edits over unnecessary rewriting.
- Always scan for stale copied values. The existing claims samples already show
  that this is an actual failure mode.
- If no close reference exists, say that explicitly and fall back to the
  nearest archetype rather than inventing a brand-new format.
