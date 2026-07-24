# Claims Requirement Archetypes

Use this guide to choose the correct drafting pattern before producing output.

## Archetype 1: Claim-Step Requirement

Use when the requirement describes a step in claim intake, registration,
assessment, routing, or decisioning.

Primary reference:
- `lbc-sickness-claim-assessment.md`

Typical stable sections:
- metadata table
- overview
- trigger
- pre-conditions
- basic flow
- user story
- acceptance criteria
- post conditions
- dependencies
- business acceptance criteria
- exception handling
- impacted interfaces
- specific dev tasks
- testing considerations
- impacted comms
- calculations
- security

Typical delta fields:
- claim type or benefit
- step name
- decision criteria
- routing rules
- RFI or escalation logic
- claim-specific fields
- medical or contract-validation behavior
- threshold logic

## Archetype 2: Variance-Only Requirement

Use when the new requirement is mostly identical to an existing one and the team
only wants the differences called out.

Primary reference:
- `lbc-sickness-variance-only.md`

Typical stable sections:
- metadata
- overview
- trigger
- basic flow summary
- business acceptance criteria
- process flow
- field details
- dev tasks
- testing considerations

Typical delta fields:
- changed wording on claim summary or UI
- changed thresholds
- changed sign-off rules
- changed contract-validation paths
- rider-specific behavior

Output preference:
- keep unchanged baseline implied
- document only what differs from the named reference implementation

## Archetype 3: Report or Analytics Requirement

Use when the requirement is about operational reporting, SLA calculation,
exports, filters, metrics, or sample layouts.

Primary reference:
- `dc-sla-alert-report.md`

Typical stable sections:
- business context
- functional requirements
- technical requirements
- data requirements
- metrics and calculations
- business rules
- report layout
- acceptance criteria
- test scenarios
- integration and dependencies
- sample template or carved-out examples

Typical delta fields:
- claim type filters
- benefit-code groupings
- SLA rules
- aggregation logic
- event-code mappings
- report timing
- access roles
- export expectations

## Cross-Checks

For every archetype, verify:

1. Claim names, benefit names, and Jira references are internally consistent.
2. Section coverage matches the reference document rather than drifting into a
   new format.
3. The delta is explicit enough that reviewers can see what changed and why.
4. Testing hot spots line up with the changed logic, not just the entire
   inherited baseline.

## Baseline Selection Rule

Choose the baseline by benefit pattern before choosing the specific page:

- `dc-funeral`
  Use for death-claims work as the primary STP baseline.
- `lbc-lump-sum-dread`
  Use for living-benefit lump-sum work.
- `lbc-recurring-sickness`
  Use for living-benefit recurring-payment work.

Only fall back to a different baseline when the user can explain why the
standard baseline class does not fit.
