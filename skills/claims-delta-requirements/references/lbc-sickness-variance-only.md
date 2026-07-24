# 3.2.1 LBC Sickness (IS3/4/5) - Determine specific exclusion clauses - Variance only (Signed Off)

| Field | Value |
|---|---|
| **Author** | Roshine Thomas |
| **User Story Summary** | Claim Assessment - Determine specific exclusion clauses |
| **Epic** | UCS-1017 - Drop 4 - Sickness Benefit (IS3/4/5) - 3 Claim Assessment |
| **Feature** | Sickness Benefit (IS3/4/5) - Claim Assessment - 3.2.1 Determine specific exclusion clauses |
| **Jira #** | UCS-2057 - Business Requirements - Sickness Benefit (IS3/4/5) - Claim Assessment 3.2.1 Determine specific exclusion clauses |

## Overview

This step evaluates whether the illness reason is excluded under the applicable plan/benefit at the time of claim.

When compared to Sickness benefit (IS1/2), the variance of Sickness Benefit (IS3/4/5) is:

1. For Sickness Benefits **IS3, IS4, IS5**, an **additional executive signoff requirement** applies during exclusion assessment when **Sum Assured exceeds R500,000**.
2. There is a change from "**Date** of Premium position" → "**Check Premium position**" — i.e. it reflects an **assessment check**, not a date field.
3. When Contract required to determine which benefit can be claimed for and % claimable **(For rider benefits if applicable)**.
4. The Claims consultant must have the option (selection) to trigger contract validation for:
   - a.) If enquiry / opinion from Contract Validator required
   - b.) Or if full contract validation required.

## Trigger

The executive signoff rule is triggered **during exclusion assessment** when:
- The calculated **Sum Assured for the sickness benefit or applicable rider exceeds R500,000**.

## Basic Flow (with reference to alternative flows)

**As a Claims Consultant**, I want the system to **automatically detect and display applicable benefit-level exclusion clauses** (based on the claimant's condition and policy context), so that I can **quickly determine if the condition is excluded**, understand the **reason and source**, and **route/decide** appropriately without re-checking multiple systems.

When compared to Sickness Benefit (IS1/2), for Sickness Benefit (IS3/4/5), the following points under **UI Display on Claim Summary** have changed.

The **Claim Summary** shows:

- **Check the Premium position** (it reflects an assessment check, not a date field.)
- **Flag if Sum Assured > R500,000** (exec sign-off required)
- **Contract required to determine which benefit can be claimed for and % claimable** (For rider benefits if applicable).
- Claims consultant must have the option (selection) to trigger contract validation for:
  - a.) **If enquiry / opinion from Contract Validator required**
  - b.) **Or if full contract validation required.**

## Business Acceptance Criteria

- Claim Summary must **"Check Premium Position"** instead of a date field.
- The system must automatically **flag the claim when Sum Assured > R500,000**.
- Percentage claimable must be shown only where rider benefits apply (e.g. Impairment Income, Spouse/Child Protector).
- Claims consultant must have the option (selection) to **trigger contract validation** for:
  - a.) **If enquiry / opinion from Contract Validator required**
  - b.) **Or if full contract validation required.**

## Process Flow

LBC - Sickness Benefit(s) IS3 & IS4 & IS5: Living Benefit Claims Process To be_WIP - Claims Modernization - Dynamics 365 - SLS Confluence

## Solution – Mock UI

As in SmartServe System

## Field Details - Data Attributes

Refer to Data Dictionary for data inputs – form wise and Support document-wise.

**DD Link:** SANLAM - Claims Modernization - Data Dictionary V1.0.xlsx

---

## Specific Dev Tasks

- Clearly **flag rider benefits** in the Claims Summary. Make it visible when:
  - Spouse/Child Protector applies
  - Impairment Income is in play
  - Percentage logic applies only where the rider supports it.
- Implement logic to:
  - Evaluate **Sum Assured threshold (R500,000)** during exclusion assessment
  - Introduce:
    - **Executive signoff flag** for IS3/IS4/IS5 only
  - Ensure:
    - Claim routing supports **pause-and-resume behaviour** based on signoff outcome
    - Signoff decision is **stored and visible downstream**

## Testing Considerations

- IS3/IS4/IS5 with Sum Assured:
  - ≤ R500,000 → no executive signoff triggered
  - > R500,000 → executive signoff mandatory
- Verify:
  - Flag visibility on claim summary
  - Claim does not progress without signoff
  - Correct behaviour when multiple benefits or riders are present
