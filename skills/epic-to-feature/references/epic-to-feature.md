# Epic to Feature Decomposition Module

This module translates one planning-ready epic into a bounded set of features
that can later be decomposed into delivery-ready stories.

Use it to create planning-ready artifacts for:
- breaking an epic into 3-8 cohesive feature capabilities
- making feature boundaries, dependencies, and sequencing explicit
- surfacing assumptions and open questions before story decomposition starts

---

## When to Use

Run this module after:
- vision-to-epic decomposition is complete
- the selected epic has clear scope boundaries, value, and success metrics

Do this before:
- feature-to-story decomposition
- detailed backlog slicing
- delivery-ready story refinement

---

## Inputs Required

Collect these inputs before drafting module output:

- selected epic from the vision-to-epic artifact
- epic title, problem addressed, and user/business value
- epic scope boundaries (in scope / out of scope)
- epic dependencies, success metrics, and acceptance criteria
- primary stories, linked requirements, or roadmap references (if available)
- glossary terms, architectural constraints, and delivery constraints (if available)

If inputs are incomplete, mark assumptions and unknowns explicitly as `TBD`.

---

## Module Tasks

Complete these tasks in order.

1. Restate the epic context
- Capture the selected epic ID, title, source artifact, and any linked evidence.
- Pull the epic goal, boundaries, and success signals into one working view.

2. Identify the capability slices implied by the epic
- List the main user workflows, system capabilities, or operational needs the
  epic must cover.
- Separate distinct capabilities from implementation details.

3. Draft candidate features
- Propose 3-8 features that collectively achieve the epic goal.
- Keep each feature cohesive, action-oriented, and decomposable into stories.
- Prefer feature boundaries that stay focused and avoid bundling multiple unrelated outcomes.

4. Define each feature's purpose and user value
- Explain what the feature does and why it exists.
- Tie each feature back to the epic goal and end-user or business outcome.

5. Define technical scope and integration points
- Capture the high-level components, data needs, and major integration points.
- Keep scope concrete enough for planning, but avoid implementation-level design.

6. Identify dependencies and sequencing
- Note dependencies between features and on external systems or prior epics.
- Make sequence constraints explicit where one feature enables another.

7. Surface assumptions and open questions
- Record what is assumed to already exist.
- Separate confirmed scope from decisions that still need product, BA, or
  technical validation.

8. Add optional system links
- Include Jira or delivery-system links when available; otherwise use `TBD`.

9. Validate coverage and overlap
- Confirm the feature set fully covers the epic without major gaps.
- Merge, split, or tighten features if boundaries are fuzzy or overlapping.

10. Write decomposition summary and sequencing guidance
- Explain how the feature set achieves the epic goal.
- Summarize key risks, unresolved questions, and recommended sequencing.

11. Run final quality checks
- Every feature has a clear purpose, user value, and bounded scope.
- Dependencies, assumptions, and open questions are explicit.
- The feature set is ready to feed feature-to-story decomposition.

---

## Output Template

Use this template when delivering module output.

```markdown
# Epic to Feature Decomposition

## Sources
- Epic source: [path/link]
- Additional evidence: [path/link]

## Epic Input
- Epic ID: [E#]
- Epic Title: [title]
- Epic goal: [what outcome this epic must deliver]
- Problem addressed: [pain or gap]
- User and business value: [why the epic matters]

## Constraints and Context
- In scope:
  - [item 1]
  - [item 2]
- Out of scope:
  - [item 1]
  - [item 2]
- Dependencies:
  - [dependency 1]
  - [dependency 2]
- Success metrics:
  - [metric 1]
  - [metric 2]
- Related stories or references:
  - [path/link or `TBD`]

## Feature Set

### Feature F-1: [Title]
- Description:
  [2-4 sentences explaining what the feature does, why it is needed, and how
  it contributes to the epic.]
- User value:
  [specific value to the user or business]
- Technical scope:
  - [component / integration / data need]
  - [component / integration / data need]
- Dependencies:
  - [feature dependency, external system, or sequence note]
- Assumptions:
  - [assumption 1]
- Open questions:
  - [question 1]
- Jira link: [optional URL or `TBD`]

### Feature F-2: [Title]
- Description:
  [...]
- User value:
  [...]
- Technical scope:
  - [...]
- Dependencies:
  - [...]
- Assumptions:
  - [...]
- Open questions:
  - [...]
- Jira link: [optional URL or `TBD`]

[Repeat for all features]

## Decomposition Summary
- Coverage:
  [how the feature set collectively achieves the epic goal]
- Overlap / gap notes:
  [resolved overlaps and remaining concerns]
- Risks:
  - [risk 1]
  - [risk 2]
- Recommended sequencing:
  - Now: [features]
  - Next: [features]
  - Later / follow-on: [features]

## Assumptions and Open Questions
- [item 1]
- [item 2]
```

---

## Quality Bar (Definition of Done)

This module is complete when:
- 3-8 features are defined for the selected epic
- each feature has clear purpose, user value, and bounded scope
- technical scope stays high-level and planning-oriented
- dependencies and sequencing constraints are explicit
- assumptions and open questions are surfaced, not hidden
- optional Jira or delivery links are captured when available (or marked `TBD`)
- the feature set can feed feature-to-story decomposition without major overlap ambiguity

If these conditions are not met, iterate before moving into feature-to-story decomposition.
