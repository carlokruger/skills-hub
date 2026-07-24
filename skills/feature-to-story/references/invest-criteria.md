# INVEST Criteria

> **Supporting reference** for the story-refinement module.
> The primary workflow document is `feature_decomposition_process.md`.

This is the per-story quality gate used by the feature decomposition process.

Product Coach uses an INVEST-style readiness lens. The familiar acronym stays, but the check is interpreted for scope clarity and testability rather than effort prediction.

## The INVEST Framework

- **I**ndependent: Can be developed in any order, in parallel with other stories
- **N**egotiable: Not a contract; solution adaptable during development
- **V**aluable: Provides tangible value to end user
- **E**xplicit: Scope, assumptions, and dependencies are clear enough to plan confidently
- **S**mall: Bounded to a focused slice without bundled outcomes or hidden coordination
- **T**estable: Clear acceptance criteria for verification

## Detailed Breakdown

### Independent

**Definition**: Story can be developed without depending on other stories being completed first.

**Why it matters**:

- Enables parallel development
- Reduces blocking and waiting
- Allows flexible prioritization

**Good example**: "Display user profile picture"
**Bad example**: "Update profile picture" (depends on upload story)

**How to achieve**:

- Minimize dependencies between stories
- Use temporary data or mocks if needed
- Consider vertical slicing (complete features across all layers)

---

### Negotiable

**Definition**: Details of implementation can be discussed and adapted during development.

**Why it matters**:

- Encourages collaboration
- Allows for better solutions discovered during development
- Avoids waterfall-style rigid specs

**Good example**: "Allow users to filter search results" (HOW is flexible)
**Bad example**: "Add dropdown with 5 filter options at exact coordinates X,Y" (too prescriptive)

**How to achieve**:

- Focus on WHAT and WHY, not HOW
- Leave implementation details to developers
- Avoid over-specifying UI/UX details

---

### Valuable

**Definition**: Delivers clear, demonstrable value to end users or stakeholders.

**Why it matters**:

- Justifies development effort
- Enables prioritization based on business value
- Keeps team focused on outcomes

**Good example**: "As a customer, I want to save my cart so I can complete my purchase later"
**Bad example**: "As a developer, I want to refactor the database schema" (technical, no user value)

**How to achieve**:

- Write from user's perspective
- Include "so that" clause explaining the benefit
- Ask "what value does this provide?"

---

### Explicit

**Definition**: Scope, assumptions, dependencies, and open questions are clear enough that the team can plan and start work without guessing.

**Why it matters**:

- Surfaces missing information early
- Reduces hidden scope creep
- Makes sequencing and handoff quality stronger

**Good example**: "Add email validation to registration form"
**Bad example**: "Improve system performance" (too vague to plan safely)

**How to achieve**:

- Provide sufficient detail and context
- Clarify scope and acceptance criteria
- Surface assumptions and open questions explicitly

---

### Small

**Definition**: Focused enough to deliver as a single coherent slice without broad coordination or multiple unrelated outcomes.

**Why it matters**:

- Faster feedback cycles
- Reduces risk
- Enables continuous delivery
- Makes review and testing simpler

**Good example**: "Display validation error message when email format is invalid"
**Bad example**: "Build complete user authentication system" (months of work)

**How to achieve**:

- Split large stories using proven patterns
- Vertical slices preferred over horizontal
- Keep one primary outcome per story

---

### Testable

**Definition**: Clear acceptance criteria that can be verified/tested.

**Why it matters**:

- Defines "done"
- Enables automated testing
- Reduces ambiguity
- Facilitates QA process

**Good example**:

```
Given a user enters an invalid email format
When they submit the form
Then an error message "Invalid email format" is displayed
And the form is not submitted
```

**Bad example**: "System should handle errors gracefully" (what does "gracefully" mean?)

**How to achieve**:

- Write specific, measurable acceptance criteria
- Use Given/When/Then format for scenarios
- Include edge cases and error handling
- Avoid vague terms like "user-friendly", "fast", "gracefully"

---

## INVEST Validation Checklist

Before marking a story as "refined", verify:

- [ ] **Independent**: Story has minimal dependencies on other stories
- [ ] **Negotiable**: Focuses on WHAT/WHY, not prescriptive HOW
- [ ] **Valuable**: Clear user benefit stated in "so that" clause
- [ ] **Explicit**: Scope, assumptions, and dependencies are clear enough to start safely
- [ ] **Small**: Story is bounded to one focused slice
- [ ] **Testable**: Specific, measurable acceptance criteria provided

## When a Story Fails INVEST

If a story fails any INVEST criterion:

1. **Not Independent**: Identify dependencies, consider merging or splitting differently
2. **Not Negotiable**: Remove prescriptive implementation details
3. **Not Valuable**: Rewrite from user perspective, clarify benefit
4. **Not Explicit**: Add more detail, clarify scope, or surface assumptions and open questions
5. **Too Large**: Apply splitting patterns (see `splitting_patterns.md`)
6. **Not Testable**: Add specific acceptance criteria with measurable outcomes

## Common Anti-Patterns

### The "Epic Disguised as Story"

**Problem**: Story is actually 3+ weeks of work
**Solution**: Break down using splitting patterns

### The "Technical Task"

**Problem**: Story written for developers, not users
**Solution**: Reframe from user perspective with clear benefit

### The "Vague Value Proposition"

**Problem**: "So that... the system works better"
**Solution**: Specify concrete user benefit

### The "Design Document"

**Problem**: Prescriptive implementation details
**Solution**: Focus on what user needs, not how to build it

### The "Maybe Someday"

**Problem**: Unclear acceptance criteria, no definition of done
**Solution**: Write testable, specific acceptance criteria
