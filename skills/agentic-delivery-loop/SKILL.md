---
name: agentic-delivery-loop
description: Spec-first agentic delivery workflow for complex software features. Use when the user wants to turn an idea into a Codex goal, PRD/OpenSpec with grill-with-docs and prd-development; decompose work across backend/frontend/test/review agents or worktrees; integrate and validate the result; run Compound Engineering simplify-code; run the polish skill for UX finishing; and prepare to ship.
---

# Agentic Delivery Loop

Use this skill to run a feature from ambiguous idea to ship-ready change. Keep the orchestrator responsible for the spec, shared contracts, integration, and final judgment.

## Goal Integration

When Codex goals are enabled, use the goal as the live execution state for the loop. The goal does not replace the PRD, OpenSpec, or tests. The goal tracks progress and handoffs; the spec remains the contract.

Create or update a goal at the start of the loop with:

- Outcome: the user-visible change to ship.
- Current phase: discovery, specify, decompose, build/test, integrate, simplify, polish, or ship.
- Contract paths: PRD, OpenSpec change, issue, or design links.
- Acceptance criteria: the behaviors that must pass.
- Subgoals: backend, frontend, test, review, docs, or deployment lanes.
- Validation checks: commands, browser checks, screenshots, or manual verification.
- Open decisions: unresolved questions that block safe implementation.
- Ship checklist: docs, working memory, commit, PR, deploy, or release notes.

Update the goal at every phase boundary and after each worker handoff. Keep it concise: enough to resume orchestration without rereading the whole transcript.

## Skill Chain

Use these skills as the default chain when available:

1. Codex goal
   - Create or refine the goal before deep discovery.
   - Treat it as the orchestrator's durable state.
   - Keep PRD/OpenSpec paths and completion criteria linked from the goal.

2. `grill-with-docs`
   - Challenge the idea against existing domain language and documented decisions.
   - Ask one question at a time and wait for the user's answer.
   - Explore code/docs instead of asking when the answer can be discovered.
   - Update `CONTEXT.md` inline when domain terms crystallize.
   - Offer ADRs only for hard-to-reverse, surprising, real trade-off decisions.

3. `prd-development`
   - Convert the grilled understanding, repo context, and documented decisions into a PRD.
   - Include assumptions, evidence gaps, acceptance criteria, and open decisions.
   - If the repo uses OpenSpec, turn the approved PRD into an OpenSpec change before implementation.

4. `compound-engineering:ce-simplify-code`
   - Run after the integrated implementation is behaviorally correct and checks are green.
   - Simplify the joined diff, not isolated worker slices.

5. `polish`
   - Run only after functionality, tests, and simplification are complete.
   - Use real rendered UI/browser evidence for frontend work.

Fallback: if `grill-with-docs` is not available, compose `load-context` and `grill-me` before `prd-development`.

## Workflow

1. Discover
   - Create or update the Codex goal with the rough outcome and discovery phase.
   - Use `grill-with-docs` to clarify ambiguous ideas, one question at a time, against the repo's existing language and decisions.
   - Ask only the questions needed to remove delivery risk.
   - Capture constraints, non-goals, users, failure modes, and deployment assumptions.
   - Update the goal with resolved terms, unresolved decisions, and the next phase.

2. Specify
   - Use `prd-development` to produce a PRD from the discovery output.
   - Produce an OpenSpec change or equivalent repo-native spec when the repo expects one.
   - Include acceptance criteria, API contracts, state transitions, permissions, error states, loading/empty states, and test expectations.
   - Keep shared contracts small and owned by the orchestrator.
   - Wait for approval before broad implementation when the spec materially changes scope.
   - Update the goal with spec paths, accepted criteria, and implementation lanes.

3. Decompose
   - Split work by ownership boundaries, not by convenience.
   - Prefer separate agents or worktrees only when the slices are decoupled enough to avoid constant renegotiation.
   - Assign disjoint file ownership for code-writing agents.
   - Keep shared generated types, route constants, env schema, package files, and migrations under orchestrator control unless a single worker explicitly owns them.
   - Add subgoals for each worker lane and make the orchestrator owner of shared contracts.

4. Parallel Build And Test
   - Backend agent: server state, persistence, API/server actions, backend unit tests.
   - Frontend agent: UI, client state, forms, visual states, frontend unit tests.
   - Test agent: clean-context acceptance/API/e2e test design from the spec. It should not read the development transcript unless explicitly needed.
   - Optional review agents: security, data integrity, architecture, performance, or product critique when the change touches those risks.
   - If subagents are unavailable or not explicitly authorized, run the same roles sequentially in the main thread.
   - Update the goal as each lane completes, blocks, or changes the contract.

5. Integrate
   - Merge or apply worker outputs deliberately.
   - Resolve contract drift in favor of the approved spec, or update the spec if the implementation exposed a better contract.
   - Run typecheck, lint, unit tests, API tests, and e2e/browser tests appropriate to the blast radius.
   - Classify failures as implementation bug, test bug, environment issue, or spec ambiguity.
   - Update the goal with validation results and any remaining blockers.

6. Simplify
   - After the integrated change is green, use `compound-engineering:ce-simplify-code` on the joined diff.
   - Apply only behavior-preserving simplifications.
   - Rerun the checks that protect the simplified code path.
   - Update the goal with simplification results and rerun checks.

7. Polish UX
   - Use the `polish` skill after behavior is correct and code is simplified.
   - Verify real rendered screens, not just component code.
   - Check layout, responsive behavior, copy, loading/empty/error states, focus/keyboard behavior, and obvious accessibility issues.
   - Use browser verification or screenshots for user-facing UI changes.
   - Update the goal with browser evidence and remaining UX issues.

8. Ship
   - Update durable docs and working memory when repo state materially changes.
   - Run final review checks.
   - Prepare commit, PR, deployment, or release notes according to the user's request.
   - Mark the goal complete only when the ship checklist is satisfied or clearly explain what remains.

## Orchestrator Rules

- Keep the critical path local. Delegate bounded side work that can progress in parallel.
- Do not delegate the immediate blocker if the next main-thread step depends on its result.
- Do not let workers edit overlapping files unless explicitly coordinated.
- Do not accept worker output blindly. Synthesize findings, reject false positives, and own final integration.
- Prefer the repo's existing specs, docs, tests, and conventions over inventing a new process.
- Preserve server authority and product contracts when realtime or UI work is involved.
- Keep the Codex goal shorter than the spec. Store decisions and requirements in durable repo artifacts; store progress and handoffs in the goal.

## Test Agent Pattern

Give the test agent clean inputs:

```text
You did not implement this change. Read the spec and current diff only.
Design tests that would catch incorrect or incomplete implementations.
Prioritize externally observable behavior over implementation details.
Do not edit production code.
Return each test case with the behavior it proves.
```

Use the test agent in parallel for test design and independent test files. Use the orchestrator for final validation against the integrated branch.

## Worker Prompt Shape

```text
You are not alone in the codebase. Other agents may edit different files.
Own only: [paths/modules].
Implement against: [spec/contract path].
Do not edit shared contracts unless instructed.
Do not revert unrelated changes.
Return changed files, checks run, and any contract issues found.
```

## Worktree Pattern

Use separate worktrees when the feature has decoupled implementation lanes and merge risk is manageable:

```text
orchestrator: spec, shared contract, final integration
backend worker: API, persistence, server tests
frontend worker: UI, client state, browser-facing tests
test worker: acceptance/e2e tests from spec
```

Merge backend/runtime behavior before frontend integration when the frontend depends on implemented API behavior.

## Completion Bar

The loop is complete only when:

- The Codex goal is complete or has a clear residual blocker.
- The approved spec and implementation match.
- Relevant checks pass or failures are clearly explained.
- Simplification preserved behavior.
- User-facing UI has been rendered and inspected when applicable.
- Docs or working memory reflect material repo changes.
