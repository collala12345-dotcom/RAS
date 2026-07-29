# 06. Quality Rubric (Review Perspectives for Human-in-the-loop Workflow)

## Purpose

Defines review perspectives for Phase 2 Gap detection and P1/P2/P3 priority classification.

**Important Changes from Previous Versions:**

- ❌ **Removed**: Quality Report generation
- ❌ **Removed**: Quality Score calculation
- ❌ **Removed**: AI Approval/Revise/Regenerate Recommendation
- ✅ **Reused**: Review perspectives for Phase 2 Gap detection
- ✅ **Reused**: Priority classification rules (P1/P2/P3)

---

## Review Perspectives (Reuse for Phase 2)

The following review perspectives are used in Phase 2 Block 2-1 through 2-6 to detect gaps.

### 1. Requirement Coverage (Phase 2 Block 2-1)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| RC-1 | Are all functional requirements reflected in TC? | Direct conflict with FR | Missing major requirement | Minor requirement gap |
| RC-2 | Are non-functional requirements (performance, reliability) reflected? | Performance threshold missing | Reliability scenario gap | Documentation gap |
| RC-3 | Are FR conditions/constraints specified in Precondition? | Missing critical dependency | Missing secondary dependency | Expression unclear |
| RC-4 | Is FR expected behavior reflected in Expected Result? | Wrong expected result | Missing expected result | Expression ambiguous |

**Priority Rules:**
- **P1**: Direct FR conflict, wrong expected behavior
- **P2**: Missing major requirement branch (e.g., OFF branch when ON exists)
- **P3**: Minor expression improvement

---

### 2. Scenario Coverage (Phase 2 Block 2-5)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| SC-1 | Is positive scenario (normal operation) included? | Happy path missing | - | - |
| SC-2 | Is negative scenario (error handling) included? | Critical negative missing | Secondary negative missing | Expression improvement |
| SC-3 | Is boundary scenario (threshold values) included? | Safety threshold missing | Non-critical boundary missing | Boundary value expression |
| SC-4 | Is exception scenario (error recovery) included? | Recovery scenario missing | Exception handling gap | Documentation gap |
| SC-5 | Is combination scenario (multi-condition) included? | Critical combination missing | Non-critical combination | Suggestion only |
| SC-6 | Is past issue-based scenario included? | Field issue recurrence risk | Lab fail history | General issue awareness |

**Scenario Types:**
- **Positive**: Normal input, normal dependency, expected behavior
- **Negative**: OFF, Invalid, Excluded Target, error injection
- **Boundary**: Threshold, min/max, empty/single/multiple values
- **Decision Combination**: Multiple switch/condition combinations
- **State Transition**: ON→OFF, Retry, Restart, Recovery
- **Abnormal**: Commercial issue potential, abnormal environment/data
- **Failure**: API/Dependency/Data collection failure
- **Recovery**: Post-failure normal recovery, retry, state consistency

**Priority Rules:**
- **P1**: Safety/commercial/field issue recurrence condition missing
- **P2**: Required negative/abnormal/major state transition missing
- **P3**: Optional extension scenario, readability improvement

---

### 3. Procedure Executability (Phase 2 Block 2-3)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| PC-1 | Are there missing steps in Test Procedure? | Critical step missing | Secondary step missing | Step order improvement |
| PC-2 | Is each step described with concrete actions? | Action unclear, not executable | Some steps vague | Expression improvement |
| PC-3 | Is step order logical? | Order prevents execution | Order confusing | Readability improvement |
| PC-4 | Are intermediate results specified per step? | No observable intermediate result | Some results missing | Expression improvement |
| PC-5 | Is procedure actually executable? | Non-existent API/command | Missing parameter/detail | Readability improvement |

**Priority Rules:**
- **P1**: Non-existent API, wrong parameter, unexecutable order
- **P2**: Missing command detail, test data for execution
- **P3**: Multi-step sentence separation, readability

---

### 4. Observability & Pass/Fail Clarity (Phase 2 Block 2-4)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| PF-1 | Are Pass/Fail criteria measurable? | No measurable criterion | Some criteria vague | Expression improvement |
| PF-2 | Are criteria avoiding abstract expressions ("verify")? | All criteria abstract | Some criteria abstract | Expression refinement |
| PF-3 | Are criteria automatable? | Not automatable | Partially automatable | Suggestion |
| PF-4 | Are criteria unambiguous? | Critical ambiguity | Minor ambiguity | Expression refinement |

**Good P/F Structure:**
```text
Condition → Observation Point → Field/Metric → Expected Value → Pass/Fail
```

**Priority Rules:**
- **P1**: Wrong expected result, no observation point for critical requirement
- **P2**: Missing log/API response/KPI for judgment
- **P3**: Expression objectification, step connection improvement

---

### 5. Scope, Target & Precondition (Phase 2 Block 2-2)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| SP-1 | Are target rAPP/System/NE/Cell/Carrier specified? | Target scope missing | Some targets unclear | Expression refinement |
| SP-2 | Are inclusion/exclusion targets defined? | Critical filter missing | Secondary filter gap | Expression improvement |
| SP-3 | Is Release/Feature Enable status specified? | Release mismatch | Feature status unclear | Documentation gap |
| SP-4 | Are dependency services specified? | Critical dependency missing | Secondary dependency gap | Documentation gap |
| SP-5 | Are CM/PM data preparation specified? | Data source missing | Collection period unclear | Expression improvement |
| SP-6 | Are Test Data/Configuration Files specified? | Critical data missing | File format unclear | Expression improvement |
| SP-7 | Are Switch/Parameter initial states specified? | Critical state missing | Secondary state gap | Expression improvement |

**Value Specificity Rules:**

| TC Expression | Judgment | Reason |
|--------------|----------|--------|
| `NR cells are prepared` | Ambiguous | Target count, carrier configuration, inclusion/exclusion criteria unclear |
| `NE List including NR Cells of different Carrier Frequency` | Basic | Required data area defined |
| `Select Cell ID from Lab environment, specify at least 1 included and 1 excluded Cell` | Executable | Selection rule and role defined, not value itself |
| `Th_DMacTputOp uses design default 2.5` | Evidence required | Fixed value needs exact source |

**Priority Rules:**
- **P1**: Scope omission allowing operation on different Cell/Carrier
- **P2**: Missing dependency/data/initial state for execution
- **P3**: Sentence structure or terminology clarification

---

### 6. Historical Risk & Consistency (Phase 2 Block 2-6)

| Check ID | Check Question | P1 Condition | P2 Condition | P3 Condition |
|----------|---------------|--------------|--------------|--------------|
| HR-1 | Are past issue triggers reflected? | Field issue recurrence condition | Lab fail history | General issue awareness |
| HR-2 | Are failure conditions reproducible? | Critical failure path | Secondary failure path | Documentation gap |
| HR-3 | Is TC internally consistent? | Internal contradiction | Inconsistent expression | Terminology variance |
| HR-4 | Is TC consistent with Evidence? | Direct conflict with Strong Evidence | Conflict with Supporting Evidence | Expression variance |
| HR-5 | Are Evidence documents consistent? | Strong vs Strong conflict | Strong vs Supporting conflict | Minor variance |

**Consistency Check Pairs:**
- Overview ↔ Purpose
- Purpose ↔ Procedure
- Precondition ↔ Procedure
- Procedure ↔ Expected Result/PF
- Related FR ↔ Actual Procedure/PF
- Step-to-step NE/Cell/Frequency/Parameter/State
- TC v1 ↔ Requirement/HLD/DLD/Algorithm
- HLD ↔ DLD ↔ Interface ↔ Algorithm

**Priority Rules:**
- **P1**: TC directly conflicts with Strong Evidence
- **P2**: Internal inconsistency, missing historical issue reflection
- **P3**: Terminology variance, expression refinement

---

## Evidence Status Assignment (Phase 2 Block 2-9)

| Status Code | Label (KO) | Meaning | Allowed Change Proposal |
|-------------|------------|---------|------------------------|
| `CONFIRMED` | 근거로 확인됨 | Direct evidence confirms issue | Specific modification text |
| `SUGGESTED` | 보완 제안 | Supporting evidence or test technique | Suggestion, auto-confirmation prohibited |
| `CONFLICT` | 문서 간 충돌 | Conflicting Strong/Supporting Evidence | Clarification request only |
| `INSUFFICIENT` | 판단 근거 부족 | Missing/Weak Evidence | Material request or question only |

**Evidence Grade Mapping:**

| Evidence Grade | Status Code | Meaning |
|----------------|-------------|---------|
| `strong` + direct match | `CONFIRMED` | Strong evidence directly confirms |
| `supporting` + technique | `SUGGESTED` | Supporting evidence or ISTQB technique |
| `strong` vs `strong` conflict | `CONFLICT` | Conflicting strong evidence |
| `strong` vs `supporting` conflict | `CONFLICT` | Conflicting evidence |
| `missing` / `weak` only | `INSUFFICIENT` | Insufficient evidence to confirm |

---

## Priority Assignment Rules (Phase 2 Block 2-9)

### P1 (Essential Confirmation)

Assign P1 when **any** of the following conditions are met:

1. **Direct Requirement Conflict**: TC directly contradicts FR/Requirement
2. **Wrong Expected Result**: Expected Result opposite to FR/Evidence
3. **Non-executable Core Behavior**: Non-existent API, wrong parameter, unexecutable procedure
4. **Non-observable Critical Result**: No observation point for critical requirement verification
5. **Safety/Commercial/Field Issue**: Missing safety-related or commercial issue recurrence condition
6. **Strong Evidence Conflict**: Strong vs Strong evidence conflict requiring human decision

**Priority Reason Codes for P1:**
- `DIRECT_REQUIREMENT_CONFLICT`
- `WRONG_EXPECTED_RESULT`
- `NON_EXECUTABLE_API`
- `MISSING_CRITICAL_OBSERVATION`
- `SAFETY_ISSUE_GAP`
- `STRONG_EVIDENCE_CONFLICT`

### P2 (Major Improvement)

Assign P2 when **any** of the following conditions are met:

1. **Required Negative/Abnormal Gap**: Missing required negative or abnormal scenario
2. **Major State/Switch Combination Gap**: Missing major ON/OFF combination or state transition
3. **Observation/Precondition Gap**: Missing log/KPI/API response or major precondition
4. **Historical Risk Gap**: Missing lab fail history or non-critical issue reflection
5. **Major Scope Gap**: Secondary target/dependency missing

**Priority Reason Codes for P2:**
- `MISSING_NEGATIVE_SCENARIO`
- `MISSING_STATE_TRANSITION`
- `MISSING_OBSERVATION_POINT`
- `MISSING_PRECONDITION`
- `HISTORICAL_RISK_GAP`

### P3 (Improvement Suggestion)

Assign P3 when **none** of P1/P2 conditions are met, but improvement is possible:

1. **Expression Clarification**: Ambiguous expression refinement
2. **Procedure Subdivision**: Multi-step sentence separation
3. **Optional Extension**: Optional extension scenario
4. **Format/Terminology**: Format, terminology, readability improvement

**Priority Reason Codes for P3:**
- `EXPRESSION_CLARIFICATION`
- `PROCEDURE_SUBDIVISION`
- `OPTIONAL_EXTENSION`
- `FORMAT_IMPROVEMENT`

---

## Prohibited Uses

The following uses are **NOT** allowed in this Human-in-the-loop Workflow:

- ❌ Quality Score calculation (weighted sum of check items)
- ❌ Quality Report generation as separate deliverable
- ❌ Risk Score / Risk Indicator calculation
- ❌ AI Approve/Revise/Regenerate recommendation
- ❌ Using this rubric to auto-approve or auto-reject proposals
- ❌ Using P1/P2/P3 as quality score components

**Note**: P1/P2/P3 indicates **review priority**, not quality score.

---

## Revision Policy

This document is revised when:

1. New review perspectives are added to Phase 2
2. Priority assignment rules change
3. Evidence status codes are modified
4. New priority reason codes are introduced

---

**Last Updated**: 2026-07-22  
**Version**: 3.0 (Human-in-the-loop Workflow - Review Perspectives Only)
