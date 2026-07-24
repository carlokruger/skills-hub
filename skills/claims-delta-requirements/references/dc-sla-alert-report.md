# 8.14 DC - SLA Calculations for Alerts (Signed Off)

## 1. Business Context

| Field | Value |
|---|---|
| **Author** | Satish Svn |
| **Jira #** | MCLCM-6938 |
| **Purpose** | Identify the outstanding cases in all the different statuses. Progress to be tracked 4x per day. Ref - New requirement - Refer sample provided in Sec (11) and actual report to be generated sample in Sec (12). |
| **Stakeholders** | Claims team |
| **Frequency** | Daily basis, including Saturdays — provided at 7h00, 10h00, 12h00, and 15h00 |
| **Delivery Format** | Excel / PDF |
| **Delivery List** | DC FLM, DC Ops |
| **Access Roles** | Death Claims Process Specialist - DC PSPEC<br>Death Claims Business Analyst - DC FLM<br>Death Claims Operational Manager - DC Ops |

---

## 2. Functional Requirements

| ID | Requirement |
|---|---|
| **FR-001** | Filter by claim type:<br>**FUNERAL** with benefits = DSF1, DSF3, DSF5, FSC2, FSC3<br>**DEATH RISK** with benefits = DS, DEC, DSC, DS50, DS80<br>**ACCIDENTAL DEATH** with benefits = ASC |
| **FR-002** | Number of Claims registered and statuses beyond Registered, excluding CLOSED (all active outstanding claims) during the last interval period: those handed over to other stakeholders, those not handed over, and total of both. |
| **FR-003** | The SLA applicable for the claim/benefit type:<br>Funeral — 2 days<br>DC Risk & Accidental Death — 5 days<br><br>**HANDOFFS** in a claim can be defined as a step in the claim process that cannot be handled by 1 singular person or system and is referred to another person or step in the life cycle of a claim. |
| **FR-004** | The SLA for Handoffs is a summation/average that includes the following SLA types:<br>• Funeral<br>• DC Risk and Accidental Death<br>• Gen *(not applicable for Drop 1 and 2)*<br>• Unclaimed Benefits *(not applicable for Drop 1 and 2)*<br>• General Claim Enquiry *(not applicable for Drop 1 and 2)*<br><br>Also includes:<br>• Forensic referral<br>• Medical decision<br>• Contract validation decision<br>• DC consultant<br>• Alternate flow<br>• Documents outstanding from Claimant<br>• Any Error |
| **FR-005** | The SLA for Others (Ready to work) is a summation/average that includes:<br>• Funeral Lifecycle<br>• Claim Intake<br>• Client Validation<br>• Claim Registration<br>• Claim Assessment<br>• Claim Authorization<br>• Claim Payment |
| **FR-006** | Number of Claims classified under the different types of SLAs under Handoffs and others (ready to work) and total of both. |
| **FR-007** | Number of Claims beyond the agreed SLA — handed over to other stakeholders, others (ready to work), and total of both. |
| **FR-008** | % of Claims **within** the agreed SLA — handed over to other stakeholders, others (ready to work), total of both, and average of percentage. |
| **FR-009** | % of Claims **beyond** the agreed SLA — handed over to other stakeholders, others (ready to work), total of both, and average of percentage. |
| **FR-010** | The entries to the report to be generated for the period range of selection by the user. |
| **FR-011** | Export report in Excel and PDF. |

### FR-004 Event Code Reference

**Gen** comprises of *(not applicable for Drop 1 and 2)*:

| Existing Event Code | Existing Event Description |
|---|---|
| 964 | Get Update on Outstanding Requirements |
| 966 | Complaint |
| 970 | Registration Error |
| 971 | Verify Documents / Certificates |
| 973 | DC Recon |
| 999 | Change Client Details |

**General Claim Enquiry** comprises of *(not applicable for Drop 1 and 2)*:

| Existing Event Code | Existing Event Description |
|---|---|
| 962 | Send Forms |
| 963 | Send Copy of Correspondence |
| 965 | NPN (No Policy Number) |
| 968 | General Claim Enquiry |
| 969 | Enquiry from Other Department |

---

## 3. Technical Requirements

| ID | Requirement |
|---|---|
| TR-001 | API endpoint for report generation with parameters |
| TR-002 | Integration with Claims DB |
| TR-003 | Role-based access control |
| TR-004 | Logging and audit trail for report access and generation |
| TR-004 | Select all claims that are processed and REGISTERED |

---

## 4. Data Requirements

### Death Claims Daily SLA - Handoffs Status

Type of Claim (applicable only for Funeral, Death Risk, Accidental Death benefit for this drop) which are routed to other internal or external stakeholders.

Attributes:
1. Total number of claims outstanding at the time of report generation
2. Applicable SLA (number of days)
3. Total number of claims beyond the agreed SLA at the time of report generation
4. % of Claims within the agreed SLA
5. % of Claims over the agreed SLA

### Death Claims Daily SLA - Other Status (Ready to Work)

Type of Claim (applicable only for Funeral, Death Risk, Accidental Death benefit for this drop) which are ready to be taken for work or other reasons.

Attributes:
1. Total number of claims outstanding at the time of report generation
2. Applicable SLA (number of days)
3. Total number of claims beyond the agreed SLA at the time of report generation
4. % of Claims within the agreed SLA
5. % of Claims over the agreed SLA

### Death Claims Daily SLA - Handoffs and Other Status

Total of each line item across the above 2 entities and average of percentage.

---

## 5. Metrics & Calculations

| Metric | Logic |
|---|---|
| Death Claims Daily SLA - Handoffs Status | % of Claims within the agreed SLA<br>% of Claims beyond the agreed SLA |
| Death Claims Daily SLA - Other Status (Ready to Work) | % of Claims within the agreed SLA<br>% of Claims beyond the agreed SLA |
| Death Claims Daily SLA - Combined Handoffs and Other Status | Total of the above 2 entities and average of percentage |

> **SLA** refers to Service Level Agreement for different steps in the life cycle of a claim.

---

## 6. Business Rules

| Rule ID | Description |
|---|---|
| BR-001 | Not applicable |

---

## 7. Report Layout

| Element | Detail |
|---|---|
| **Title** | 1. DEATH CLAIMS DAILY SLA - HANDOFF STATUS<br>2. DEATH CLAIMS DAILY SLA - Other Status (ready to work)<br>3. DEATH CLAIMS DAILY SLA - Combined Handoff and other status<br><br>STATUS DATE: dd-mm-yyyy xxhyy (time) |
| **Filters** | Claims status = Registered and statuses beyond Registered excluding CLOSED |
| **Columns** | Refer Data requirement for details |
| **Footer** | Notes, Contact info, Page # |

---

## 8. Acceptance Criteria

| ID | Criteria |
|---|---|
| AC-001 | Report includes only claims with all statuses from REGISTERED |
| AC-002 | Filters work as expected |
| AC-003 | Exported files match displayed data |
| AC-004 | Only authorized users can access the report |

---

## 9. Test Scenarios

| ID | Scenario | Expected Outcome |
|---|---|---|
| TS-001 | Generate report for all Claims for the period range provided | Registered and statuses beyond Registered excluding CLOSED |
| TS-002 | Apply filter for product = 'Funeral', 'Death Risk', 'Accidental Death' | Only Funeral, Death Risk and Accidental death claims shown |
| TS-003 | Apply filter for Benefits = DSF1, DSF3, DSF5, FSC2, FSC3, DS, DEC, DSC, DS50, DS80, ASC | Only Funeral, Death Risk and Accidental death claims shown |
| TS-004 | Export to Excel | File downloads correctly |
| TS-005 | Unauthorized access attempt | Access denied |
| TS-006 | Validate data against DB | Matches source data |

---

## 10. Integration & Dependencies

- Claims DB (Azure)
- Policy Admin System (Epsilon)
- Workflow Engine (D365)
- BI/Reporting Tool (Power BI)
- Authentication & Authorization Service

---

## 11. Sample Template / Report (reference only)

### Death Claims Daily SLA - Handoffs Status

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Funeral | 2 | 0 | 100.00% | 0.00% |
| Fund | 61 | 0 | 100.00% | 0.00% |
| Risk | 1,522 | 902 | **40.74%** | 59.26% |
| OMP | 0 | 0 | 100.00% | 0.00% |
| Registration Errors / complaints | 3 | 3 | **0.00%** | 100.00% |
| Unclaimed Benefits | 0 | 0 | 100.00% | 0.00% |
| Proof of Life | 0 | 0 | 100.00% | 0.00% |
| Enquiry on Previously Completed Claim | 779 | 534 | **31.45%** | 68.55% |
| **Global** | **2,367** | **1,439** | **39.21%** | **60.79%** |
| General Claim Enquiry | 452 | 356 | **21.24%** | 78.76% |

### Death Claims Daily SLA - All Other Status vs Follow up & Ready

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Funeral | 1,407 | 139 | 90.12% | 9.88% |
| Fund | 6,871 | 272 | 96.04% | 3.96% |
| Risk | 7,680 | 931 | **87.88%** | 12.12% |
| OMP | 45 | 1 | 97.78% | 2.22% |
| Registration Errors / complaints | 13 | 1 | 92.31% | 7.69% |
| Unclaimed Benefits | 0 | 0 | 100.00% | 0.00% |
| Proof of Life | 1 | 0 | 100.00% | 0.00% |
| Enquiry on Previously Completed Claim | 3 | 0 | 100.00% | 0.00% |
| **Global** | **16,020** | **1,344** | **91.61%** | **8.39%** |
| General Claim Enquiry | 0 | 0 | 100.00% | 0.00% |

### Death Claims Daily SLA - Handoff & Other Status Combined

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Funeral | 1,409 | 139 | 90.13% | 9.87% |
| Fund | 6,932 | 272 | 96.08% | 3.92% |
| Risk | 9,202 | 1,833 | **80.08%** | 19.92% |
| OMP | 45 | 1 | 97.78% | 2.22% |
| Registration Errors / complaints | 16 | 4 | **75.00%** | 25.00% |
| Unclaimed Benefits | 0 | 0 | 100.00% | 0.00% |
| Proof of Life | 1 | 0 | 100.00% | 0.00% |
| Enquiry on Previously Completed Claim | 782 | 534 | **31.71%** | 68.29% |
| **Global** | **18,387** | **2,783** | **84.86%** | **15.14%** |
| General Claim Enquiry | 452 | 356 | **21.24%** | 78.76% |

### All Status Summary

| Global | Total All Status | Handoff | Follow-up | Open | Ready | Wait |
|---|---|---|---|---|---|---|
| Funeral | 1,409 | 2 | 642 | 0 | 139 | 626 |
| Fund | 6,932 | 61 | 5,579 | 0 | 206 | 1,086 |
| Risk | 9,201 | 1,522 | 5,300 | 2 | 1,229 | 1,148 |
| OMP | 45 | 0 | 39 | 0 | 1 | 5 |
| Registration Errors / complaints | 16 | 3 | 3 | 0 | 0 | 10 |
| Unclaimed Benefits | 0 | 0 | 0 | 0 | 0 | 0 |
| Proof of Life | 1 | 0 | 0 | 0 | 1 | 0 |
| Enquiry on Previously Completed Claim | 782 | 779 | 1 | 0 | 0 | 2 |
| **Global** | **18,386** | **2,367** | **11,564** | **2** | **1,576** | **2,877** |
| General Claim Enquiry | 452 | 452 | 0 | 0 | 0 | 0 |

### Death Claims Daily - Alerts per SR Status

| Global | Total Alerts | Handoff | Follow-up | Open | Ready | Wait | In Pre Q | Odest (Handoff) | Odest (Other) | Over SLA | % on SLA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Funeral | 63 | 0 | 7 | 0 | 39 | 17 | 0 | | 20/01/2026 | 17 | 73.02% |
| Fund | 232 | 0 | 15 | 0 | 176 | 41 | 117 | | 09/01/2026 | 33 | 85.78% |
| Risk | 1,151 | 419 | 58 | 0 | 565 | 109 | 135 | 22/01/2026 | 05/01/2026 | 556 | 51.69% |
| OMP | 2 | 0 | 1 | 0 | 1 | 0 | 2 | | 13/01/2026 | 2 | 0.00% |
| Registration Errors / complaints | 1 | 0 | 1 | 0 | 0 | 0 | 0 | | 26/01/2026 | 1 | 0.00% |
| Unclaimed Benefits | 0 | 0 | 0 | 0 | 0 | 0 | 0 | | | 0 | 100.00% |
| Proof of Life | 0 | 0 | 0 | 0 | 0 | 0 | 0 | | | 0 | 100.00% |
| Enquiry on Previously Completed Claim | 108 | 108 | 0 | 0 | 0 | 0 | 0 | 22/01/2026 | | 19 | 82.41% |
| **Global** | **1,557** | **527** | **82** | **0** | **781** | **167** | **254** | **22/01/2026** | **05/01/2026** | **628** | **59.67%** |
| General Claim Enquiry | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 26/01/2026 | | 8 | 57.89% |

> **ALERTS** are when additional documents/enquiries are received on a claim at any step in the life cycle of a claim.

---

## 12. Carved-out Sample — Funeral Benefit Claims, Death Risk & Accidental Death

*(SLA days must also be included in the SLA report)*

*Updated based on SLA feature on 17 Oct 2025*

### Death Claims Daily SLA - Handoffs Status

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Forensic Referral | 3 | 0 | 100.00% | 0.0% |
| Medical Decision | 2 | 0 | 100.00% | 0.0% |
| Contract Validation Decision | 1 | 0 | 100.00% | 0.0% |
| DC Consultant | 4 | 0 | 100.00% | 0.0% |
| Alternate flow | 5 | 0 | 100.00% | 0.0% |
| Documents Outstanding from Claimant | 6 | 0 | 100.00% | 0.0% |
| Any Error | 2 | 0 | 100.00% | 0.0% |
| **Total Funeral SLA - Handoffs** | **23** | **0** | **100.00%** | **0.0%** |

### Death Claims Daily SLA - Others (Ready to Work)

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Funeral LifeCycle | 3 | 0 | 100.00% | 0.0% |
| Claim Intake | 2 | 0 | 100.00% | 0.0% |
| Client Validation | 1 | 0 | 100.00% | 0.0% |
| Claim Registration | 4 | 0 | 100.00% | 0.0% |
| Claim Assessment | 5 | 0 | 100.00% | 0.0% |
| Claim Authorisation | 6 | 0 | 100.00% | 0.0% |
| Claim Payment | 2 | 0 | 100.00% | 0.0% |
| **Total Funeral SLA - Handoffs** | **23** | **0** | **100.00%** | **0.0%** |

### Death Claims Daily SLA - Handoffs and Other Status

| Global | Total | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|
| Funeral | 46 | 0 | 100.0% | 0.0% |

### Death Claims Daily SLA - Handoffs Status (with SLA days)

| Global | Total | SLA (days) | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|---|
| Funeral | 25 | 2 | 0 | 100.00% | 0.00% |
| DC Risk & Accidental Death | 20 | 5 | 9 | **55.00%** | 45.00% |
| **Global** | **45** | | **9** | **80.00%** | **20.00%** |

### Death Claims Daily SLA - Other Status (Ready to Work) (with SLA days)

| Global | Total | SLA (days) | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|---|
| Funeral | 181 | 2 | 47 | **74.03%** | 25.97% |
| DC Risk & Accidental Death | 35 | 5 | 4 | **88.57%** | 11.43% |
| **Global** | **216** | | **51** | **76.39%** | **23.61%** |

### Death Claims Daily SLA - Handoff & Other Status Combined (with SLA days)

| Global | Total | SLA (days) | Over SLA | % on SLA | % Over SLA |
|---|---|---|---|---|---|
| Funeral | 206 | 2 | 47 | **77.18%** | 22.82% |
| DC Risk & Accidental Death | 55 | 5 | 13 | **76.36%** | 23.64% |
| **Global** | **261** | | **60** | **77.01%** | **22.99%** |
