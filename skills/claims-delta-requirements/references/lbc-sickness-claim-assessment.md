# 3.3.3 LBC Sickness - Claim Assessment - Determine if full or partial approval (Signed Off)

| Field | Value |
|---|---|
| **Author** | Roshine Thomas |
| **User Story Summary** | Claim Registration – Determine if full or partial approval |
| **Epic** | UCS-1017 - Drop 4 LBC - Business Requirements Epic |
| **Feature** | Sickness Benefit Claim - Claim Registration - 3.3.3 Determine if full or partial approval |
| **Jira #** | UCS-1369 - Business Requirements - Dread Disease - Claim Registration - 3.3.3 Determine if full or partial approval |
| **Actor** | **Primary Actor (System):** SmartServe<br>**Human Roles (on breakouts):** Claims Specialist, Claims Consultant |

## Overview

When **contractual definitions are met**, SmartServe must determine if the claim qualifies for **full approval** or **partial approval** (based on the "partial capacity" field and supporting evidence). Unlike Dread Disease (lumpsum), Sickness allows **partial capacity** outcomes.

If the full/partial % is determined, the outcome feeds the successor step "Make claim outcome decision." The feature supports both automated and assisted decisions, with the option of a **LLM-generated summary** explaining how the coverage percentage was derived.

If the **partial %** cannot be determined, SmartServe triggers an **RFI loop** until sufficient information is received, then reevaluates.

## Trigger

- Entry from prior step: **"Contractual definitions met."**
- Reentry trigger: **"Receive Additional information"** event (after claimant provides missing details).

## Pre-conditions

- Contractual definitions step completed with **status = Met** or the case has just **resumed** from an RFI/Medical opinion with new documents recorded.
- Core fields present in claim record: **ICD10**, **sickleave start/end**, **claim event dates**, and **capacity indicators** (if captured on the form).

---

## Basic Flow (with reference to alternative flows)

### User Story

- **As a Claims Consultant**, I want the system to indicate whether **full** or **partial** approval applies and, if partial, whether the **claim form's partial capacity** has been correctly provided, so that I can finalize the outcome confidently or request more information.
- **As SmartServe**, I want to **detect partial vs full sick leave applicability** and **block progression** when partial capacity details are missing, sending an **RFI** and **resuming** automatically once information is received, so that the claim outcome is accurate and defensible.

### Acceptance Criteria

#### 1. Full vs Partial Applicability Check
- System evaluates available evidence and determines whether the life assured is on **full sick leave** or **partial capacity** is applicable.
- If **full** applies → proceed directly to *Make Claim Outcome Decision*.
- If **partial** applies → continue with AC2/3.

#### 2. Partial Capacity Field Presence
- When partial is applicable, system checks the **claim form's partial capacity field** (or equivalent capture) has been **selected/provided** and is **coherent** with medical documentation.
- If provided and coherent → proceed to *Make Claim Outcome Decision*.
- If **not provided** or **incoherent** → trigger RFI (AC3).

#### 3. RFI for Undetermined Partial %
- If **partial % cannot be determined**, system **autocreates an RFI** to the claimant/provider requesting the specific partial capacity details needed to make the decision.
- Case is **pended with SLA**, and **reminders/escalations** are sent until information is received.
- On receipt, the case **autoresumes** to reevaluate AC1/2.

#### 4. Medical Opinion Path (when Contractual Definitions were NOT met earlier, but condition/exclusion can be resolved)
- CC assesses whether **medical opinion is required** due to insufficient or conflicting medical information.
- When required, the case is **referred to the Medical Team**.
- **Medical Team provides decision/feedback**; the case returns to CC.
- If the **condition/exclusion is resolved**, proceed to *Make Claim Outcome Decision*.

#### 5. LLM-Assisted Summary
- System generates an **LLM summary** for assessor consumption highlighting: capacity cues from documentation, any contradictions, missing fields, and a recommendation on **full vs partial** readiness (advisory only; CC remains accountable).

#### 6. Audit & Traceability
- All determinations (full/partial), RFI requests/responses, and medical opinions are **timestamped** with user/system actor and stored in the claim record.

#### 7. No Silent Bypass
- The decision step **cannot be bypassed** if **partial** is indicated but **partial capacity details** are missing; the case must remain pended (or routed to Medical Team) until resolved.

---

## Successful Post Conditions

- Coverage percentage(s) determined and stored (per event).
- **Approval type resolved** (Full or Partial with %/hours/capacity) and posted to the case.
- Workflow proceeds to **"Make claim outcome decision"** without further fallouts for this step.
- Optional LLM summary generated and attached to the claim record.

## Dependencies

- Prior step: **Determine if doctor diagnosis is covered by contract** – must be completed successfully.
- Policy/Contract Service availability for benefit schedules, riders, versioning.
- Rules Engine availability for classification & calculation rules.
- LLM Summarization Service (optional, feature flagged).

## Business Acceptance Criteria

- If full/partial % approval criteria are met, system routes to "Make claim outcome decision" with no RFI.
- If partial % is not determined, then route to CC and to CS to request client for additional information.
- Reevaluation after additional information must resolve approval type or produce explicit fallout reason.
- All actions (determinable/indeterminable, RFI sent/received, timestamps) are persisted for audit (as per sample structure).
- Medical opinion referral path functions where evidence is insufficient, and the case **returns** with feedback to continue.

## Exception Handling

| Scenario | Handling |
|---|---|
| Missing or ambiguous partial capacity | RFI to claimant (via CS) |
| Conflicting information (e.g., form says partial; evidence suggests full) | Route to CC for clarification; loop back on receipt |
| Medical information insufficient | CC refers to Medical Team; if still inconclusive, CC may issue an additional targeted RFI |
| LLM service unavailable | Fall back to standard view of documents without summarization; step remains functional |

## Process Flow

LBC - Sickness Benefit(s): Living Benefit Claims Process To be_WIP

## Solution – Mock UI

*(To be provided)*

---

## Field Details - Data Attributes

Refer to Data Dictionary for data inputs – form wise data to be distributed across the tabs and pages in D365.

**DD Link:** SANLAM - Claims Modernization - Data Dictionary V1.0.xlsx

## Impacted Interfaces

| Interface | Role |
|---|---|
| Content Manager / Content Navigator | Used by Claims Specialist to manually search for FICA documents |
| SmartServe Workflow Engine | Routes the claim to the Claims Specialist step |
| Communications (D365 / KTA depending on the template) | Used to send RFI |
| Audit/Case store | Persistence of decisions and evidence pointers (per Sample file approach) |

## Specific Dev Tasks

- Implement **approval type resolver**: logic to classify Full vs Partial (driven by partial capacity field + evidence).
- Implement **conditional routing**:
  - If full/partial % determined → move to STP to make Claims Outcome decision.
  - If partial % NOT determined → route to CS to Request additional information.
- Implement **RFI loop handlers**: create request, send comms, await Receive Additional document submission, and reevaluate deterministically.
- Implement **continuation logic** after requesting for additional information.
- Integrate **communication trigger**:
  - When requesting additional information → trigger communication while continuing the workflow.
- Integrate **Medical Team referral** step and return handling.
- Integrate **LLM summary panel** in the assessor UI (readonly advisory).
- Persist **audit events** for all decisions and communications.

## Testing Considerations and Hot Spots

- **Test conditional routing logic:**
  - If full/partial % determined → move to STP to make Claims Outcome decision.
  - If partial % NOT determined → route to CS to Request additional information.
- **Test communication triggers:**
  - Communication must send to CC/CS requesting for additional information when partial % NOT determined.
  - Ensure workflow does not pause.
- **RFI path:** partial required but missing; ensure pend/SLA/reminders; autoresume on receipt.
- **Medical opinion path:** insufficient/contradictory documents; referral and return loop.
- **Edge cases:** capacity provided but inconsistent with medical notes; ensure block and correction.
- **LLM:** verify summary presence/quality does not alter decision rules; it must be advisory only.
- **Audit:** verify end-to-end entries for all routes.
- **Resilience:** behavior when comms or LLM are temporarily unavailable.

## Impacted Comms (CFD)

Communication to clients will be via:

- Email (primary)
- SMS
- WhatsApp (if feasible, though costly)

> The template/input/sample for Email, SMS and WhatsApp to be provided by Business.

## Calculations

- **No monetary calculation here.**
- The step records the **qualitative decision** (full vs partial).
- Any quantitative prorating is handled downstream during payment determination based on the finalized outcome.

## Security Considerations (Access & Routing)

- Only **authorized CC/CS** can trigger RFIs and finalize **full/partial** selection.
- **Medical Team** access restricted to clinical evidence and referral responses.
- All capacity-related data and medical documents are **sensitive** and must be protected in transit and at rest.
- Routing must ensure **return to the originating assessor** after medical feedback or RFI reception to maintain accountability.

## Relational Diagram

Not applicable.

## Context Documents

Not applicable.
