# Feature Decomposition Process (Feature -> Stories)

This is the canonical end-to-end process for converting a feature into 3-8
developer-ready user stories. It is the primary module document for the
**story-refinement** workflow.

Supporting references (subordinate to this document):

- `user_story_format.md` — story card schema and examples
- `invest_criteria.md` — per-story quality gate (INVEST framework)
- `splitting_patterns.md` — systematic patterns for splitting oversized stories
- `feature_to_stories.txt` — legacy prompt template (retained for reference)

## Inputs

- **Feature ID and title**
- **Problem / goal description** — why this feature exists
- **Primary user value / outcome**
- **Technical scope and constraints**
- **Known dependencies** — internal and external
- **Domain glossary** — roles, key entities, business rules

## Outputs

The workflow produces a **story set** — a bounded collection of delivery-ready
stories for one selected feature. Each story includes:

- **Title** in "As a … I want … so that …" format
- **Scope and out-of-scope boundaries**
- **Acceptance criteria** — concrete, testable assertions covering happy path,
  edge cases, and failure behavior. Each criterion should be specific enough to
  support later conversion into acceptance tests or executable test scenarios
  (e.g. Playwright scripts) without ambiguity
- **File impact list** — frontend, backend, database, tests, configuration
- **Dependencies and open questions**
- **Bounded-scope notes** — why the story is focused and what remains out of scope

The story set as a whole includes:

- **Recommended implementation sequence** with rationale
- **Parallelization guidance** — what can be built concurrently
- **Integration points and cross-story testing needs**
- **Risks** (delivery and technical) with mitigation notes

### Output boundary

This workflow **stops at acceptance-criteria-ready stories**. It does not
generate executable test suites, Playwright scripts, or framework-specific test
code. However, the acceptance criteria shape is deliberately optimized so that
downstream acceptance-test design or automated test generation can consume the
output directly.

## Process

### Step 0: Clarity Gate

Do not decompose a vague feature into vague stories.

- If important details are missing, stop and ask questions first.
- If you have `core/ambiguity_analysis.md`, run it on the feature and address gaps before refinement.

### Step 1: Map User Workflows

Identify the distinct user journeys and roles involved.

- Separate happy paths from edge/failure paths.
- Note role-dependent behavior differences.
- Mark external handoffs (services, teams, vendors, integrations).

### Step 2: Establish Story Boundaries

Create candidate stories as vertical slices.

- Each story should be independently testable.
- Prefer user-visible value increments over layer splits (avoid "DB story", "API story", "UI story").
- Keep stories small enough to deliver as focused, independently reviewable slices.
- Target 3-8 stories per feature while keeping each story bounded in scope and explicit about what remains out of scope.

If a candidate story still feels large/unclear, move to Step 3.

### Step 3: Split Oversized Candidates

Apply splitting patterns systematically (see `splitting_patterns.md` for full
detail and examples):

- **By workflow steps** — multi-step journeys become one story per step.
- **By business rules** — many independent rules become one story per rule.
- **By happy/unhappy path** — deliver the success scenario first, then edge/error handling.
- **By parameters/data types** — broad variations become one story per type.
- **By complexity** — build simple first, optimize later.
- **Spike pattern** — unknowns/high risk get a spike, then first slice.

After splitting, ensure each story still delivers standalone value and is not
trivial or value-less. Do not split so far that the result stops being a meaningful standalone slice.

### Step 4: Write Story Cards

For each story, follow the story card schema (see `user_story_format.md` for
full schema and examples):

- **Title**: `As a [role] I want [capability] so that [benefit]`
- **Scope** and explicit **out-of-scope** boundaries
- **Acceptance criteria**: concrete, testable assertions using Given/When/Then
  or equivalent. Cover happy path, edge cases, failure behavior, validation
  rules, and security/access control where relevant. Write criteria that are
  specific enough for a tester to write test cases directly from them and for
  later automated test generation to consume without ambiguity.
- **Files that will need modification** (required): frontend, backend, database,
  tests, configuration — grouped by category, new files marked with (NEW)
- **Dependencies and open questions** (must be resolved before "Ready")
- **Bounded-scope notes** explaining why the story is focused enough to move forward

### Step 5: Quality Gate (INVEST-Style Readiness + Testability)

Validate each story against the INVEST-style readiness criteria (see `invest_criteria.md` for
the full framework):

- **Independent**: can be developed without waiting for other stories
- **Negotiable**: focuses on what/why, not prescriptive how
- **Valuable**: clear user benefit in the "so that" clause
- **Explicit**: scope, assumptions, and dependencies are clear enough to plan confidently
- **Small**: bounded to a focused slice without hidden coordination or bundled outcomes
- **Testable**: specific, measurable acceptance criteria

Additionally confirm:

- Acceptance criteria are objective (pass/fail is unambiguous).
- Error handling and validation rules are explicit.
- Permissions/security considerations are called out where relevant.
- Dependencies are explicit and minimized.
- The story is neither an epic in disguise nor a trivial slice.

If a story fails any check, rewrite or split it and re-validate.

### Step 6: Sequence, Integrate, and Summarize

Provide a story set summary:

- Recommended implementation order, with rationale.
- What can be parallelized.
- Integration points that require cross-story testing.
- Risks across the set (delivery/technical) and mitigation notes.

## Definition of Ready (Story Level)

A story is "Ready" when:

- Role/capability/value is explicit.
- Acceptance criteria cover happy path and important failure/edge behavior.
- File impact list is concrete and includes tests.
- Dependencies and open questions are explicit.
- The story passes INVEST and is right-sized.
