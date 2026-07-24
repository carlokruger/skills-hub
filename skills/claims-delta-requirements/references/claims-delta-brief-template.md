# Claims Delta Brief Template

Use this brief when a new claims requirement should be drafted from an existing
signed-off reference rather than written from scratch.

## 1. Request Summary

- Requirement title:
- Requirement archetype:
  - claim-step requirement
  - variance-only requirement
  - report or analytics requirement
- Claim domain / product:
- Claim type / benefit / action:
- Jira / tracking reference:

## 2. Closest Reference Artifact

- Baseline class:
  - `dc-funeral`
  - `lbc-lump-sum-dread`
  - `lbc-recurring-sickness`
  - other: [explain]
- Reference document path or identifier:
- Why this is the closest reference:
- Which sections should be preserved unchanged:

## 3. Delta to Apply

### Business Logic Changes
- [changed rule]
- [changed rule]

### Workflow / Routing Changes
- [changed route, approval, signoff, pend, autoresume, escalation]

### Data / Field Changes
- [changed field, threshold, code, selector, calculation input]

### UI / Output Changes
- [changed wording, display field, report column, layout element]

### Dependency / Integration Changes
- [changed system, service, dependency, event code]

### Security / Access Changes
- [changed role, visibility, routing restriction]

## 4. Unchanged Baseline Assumptions

- [what should carry forward from the reference without rewriting]
- [what remains true]

## 5. Testing Hot Spots Introduced by the Delta

- [test focus area]
- [test focus area]

## 6. Known Gaps / Questions

- [open question]
- [open question]

## 7. Output Preference

- Produce:
  - full requirement document in reference format
  - variance-only document
- If full requirement:
  - sections that must be rewritten:
  - sections safe to carry forward with minimal edits:

## 8. Reviewer Checks

- Verify the selected baseline class matches the benefit pattern:
  - death claims -> funeral baseline
  - LBC lump sum -> dread disease baseline
  - LBC recurring -> sickness baseline
- Verify all copied identifiers match the new claim type/action.
- Verify no stale benefit names, Jira references, or thresholds remain.
- Verify the changed logic is reflected in acceptance criteria and testing.
