# Claims Delta Brief Example - LBC Sickness IS3/4/5 Exclusion Assessment

This worked example shows how to express a claims requirement as a delta against
an established baseline instead of drafting the entire document from scratch.

## 1. Request Summary

- Requirement title: 3.2.1 LBC Sickness (IS3/4/5) - Determine specific exclusion clauses
- Requirement archetype: variance-only requirement
- Claim domain / product: Living Benefit Claims
- Claim type / benefit / action: Sickness Benefit (IS3/4/5) exclusion assessment
- Jira / tracking reference: UCS-2057

## 2. Closest Reference Artifact

- Baseline class: `lbc-recurring-sickness`
- Reference document path or identifier: Sickness Benefit (IS1/2) exclusion assessment baseline
- Why this is the closest reference:
  - same assessment step
  - same core exclusion-clause determination logic
  - same broad UI and workflow shape
- Which sections should be preserved unchanged:
  - overall section ordering
  - exclusion-assessment baseline behavior
  - process-flow reference style
  - field-details and testing section shape

## 3. Delta to Apply

### Business Logic Changes
- Add executive signoff requirement for IS3/4/5 when Sum Assured exceeds R500,000.
- Distinguish rider-benefit cases where contract is required to determine which
  benefit can be claimed and what percentage is claimable.

### Workflow / Routing Changes
- Claims consultant must be able to trigger contract validation in two modes:
  - enquiry / opinion from Contract Validator
  - full contract validation
- Claim must support pause-and-resume behavior around executive signoff outcome.

### Data / Field Changes
- Replace "Date of Premium position" with "Check Premium position".
- Display and evaluate Sum Assured threshold of R500,000.
- Show percentage-claimable details only where rider benefits apply.

### UI / Output Changes
- Claim Summary must display:
  - Check Premium position
  - signoff flag when Sum Assured > R500,000
  - rider-benefit contract requirement
  - contract-validation selection options

### Dependency / Integration Changes
- Depend on contract-validation capability for rider-benefit determination.
- Ensure downstream routing can persist executive signoff result.

### Security / Access Changes
- No net-new security model stated; preserve baseline access assumptions unless
  signoff approval roles need explicit naming later.

## 4. Unchanged Baseline Assumptions

- Core exclusion-clause assessment logic remains the same as the IS1/2
  baseline.
- Baseline section structure and tone remain acceptable.
- Existing process flow and SmartServe UI context remain valid unless directly
  contradicted by the delta above.

## 5. Testing Hot Spots Introduced by the Delta

- Verify Sum Assured threshold behavior at and above R500,000.
- Verify claim cannot progress when executive signoff is required but not
  completed.
- Verify rider-benefit visibility and percentage handling.
- Verify both contract-validation options are available and route correctly.
- Verify copied baseline wording does not retain IS1/2-specific terminology.

## 6. Known Gaps / Questions

- Which role performs executive signoff and how is the decision recorded?
- Is the R500,000 threshold configurable or hard-coded?
- Should the contract-validation options appear for all claims or only when
  rider-benefit indicators are present?

## 7. Output Preference

- Produce: variance-only document
- Sections that must be rewritten:
  - Overview
  - Trigger
  - Basic Flow summary
  - Business Acceptance Criteria
  - Specific Dev Tasks
  - Testing Considerations
- Sections safe to carry forward with minimal edits:
  - Process Flow
  - Solution / Mock UI
  - Field Details shell

## 8. Reviewer Checks

- Verify all copied identifiers say IS3/4/5, not IS1/2.
- Verify R500,000 threshold appears consistently in overview, business
  acceptance criteria, dev tasks, and testing.
- Verify contract-validation options are expressed identically across UI,
  workflow, and testing sections.
