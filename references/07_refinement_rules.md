# 07. Refinement Rules (Evidence-Based Minimal Change for Human-in-the-loop Workflow)

## Purpose

Defines rules for Phase 2 change proposal generation and Phase 3 controlled merge.

**Important Changes from Previous Versions:**

- ❌ **Removed**: Auto-apply changes to TC v2 in Phase 2
- ❌ **Removed**: AI-generated TC v2 without Reviewer decision
- ✅ **Reused**: Evidence-based minimal change principles for Phase 2 proposals
- ✅ **Reused**: Controlled merge rules for Phase 3

---

## Core Principles

### 1. Evidence-Based Change (Phase 2 Block 2-8)

**Rule**: Every change proposal must have supporting evidence.

```yaml
# Valid Change Proposal
change_id: CHG-001
finding: "Resolution OFF expected result missing"
proposed_text: "Resolution Switch 가 OFF 인 Target Carrier 에서는..."
evidence_refs: [EVD-0001, EVD-0005]  # Required
evidence_status: CONFIRMED  # Required

# Invalid (prohibited)
change_id: CHG-XXX
finding: "This should be improved"
proposed_text: "Better wording here"
evidence_refs: []  # ❌ Not allowed
evidence_status: SUGGESTED  # Must have at least supporting evidence
```

**Evidence Types:**
- `CONFIRMED`: Direct requirement/design evidence
- `SUGGESTED`: Supporting evidence or test technique (ISTQB)
- `CONFLICT`: Conflicting evidence requires human decision
- `INSUFFICIENT`: Cannot propose specific change, only question

### 2. Minimal Change Unit (Phase 2 Block 2-8)

**Rule**: One Change ID = One independent change.

```yaml
# Valid (Atomic)
change_id: CHG-001
operation: ADD
target: "C. Pass/Fail Criteria, PF-02"
proposed_text: "Resolution OFF 미동작 판정 기준"

change_id: CHG-002
operation: ADD
target: "C. Pass/Fail Criteria, PF-03"
proposed_text: "Detection OFF 미동작 판정 기준"

# Invalid (Combined - Do NOT do this)
change_id: CHG-XXX
operation: ADD
target: "C. Pass/Fail Criteria"
proposed_text: "Resolution OFF AND Detection OFF 판정 기준 추가"  # ❌ Two changes in one
```

**Atomic Change Test:**
- Can Reviewer approve this change independently? → Yes = Atomic
- Can Reviewer reject part of this change? → Yes = Split into multiple changes

### 3. Original Text Preservation (Phase 3 Block 3-4)

**Rule**: Preserve TC v1 intent and structure.

```yaml
# Valid (Minimal modification)
original: "NR Cell 대상 Overshooting 검증"
proposed: "NR Cell 대상 Overshooting Detection 검증"  # Added specific function name

# Invalid (Rewrite - Do NOT do this)
original: "NR Cell 대상 Overshooting 검증"
proposed: "이 TC 는 NR Cell 의 Overshooting 문제를 탐지하는지 확인한다. 또한..."  # Complete rewrite
```

**Preservation Rules:**
- Do not change TC ID, title, or core intent
- Do not restructure sections unless explicitly approved
- Do not add new scenarios beyond approved changes
- Do not remove existing content unless explicitly approved

### 4. Unsupported Change Prohibition (Phase 2 Block 2-8)

**Rule**: Do not propose changes without evidence.

```yaml
# Valid (Evidence-supported)
finding: "FR-11 §3.2 requires per-frequency control, but TC tests single frequency only"
proposed_text: "Add Frequency 2 test scenario"
evidence_refs: [EVD-0001]  # FR-11 reference

# Invalid (Unsupported - Do NOT do this)
finding: "This TC seems incomplete"
proposed_text: "Add more test scenarios for better coverage"  # ❌ No specific evidence
```

**Prohibited Changes:**
- Changes based on "seems incomplete" without specific evidence
- Changes based on "would be nice to have" without requirement basis
- Changes that expand TC scope beyond original intent
- Changes that add new features not in original requirement

---

## Phase 2 Change Proposal Generation Rules

### Block 2-1: Requirement & Verification Point Coverage

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| FR direct conflict | MODIFY | Strong requirement evidence |
| Missing requirement branch | ADD | Strong requirement evidence |
| Wrong expected result | MODIFY | Strong requirement/design evidence |
| Missing verification point | ADD | Strong/design evidence |

**Do NOT generate proposal when:**
- Requirement evidence is `INSUFFICIENT` → Generate clarification request instead
- Evidence is `CONFLICT` → Generate conflict report, not specific change

### Block 2-2: Scope, Target & Precondition

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| Missing critical target | ADD | Design/Interface evidence |
| Wrong target scope | MODIFY | Design/Interface evidence |
| Missing dependency | ADD | Design evidence |
| Missing test data | ADD | Procedure/Design evidence |

**Value Specificity Rules:**

| Value Type | Required Specificity | Evidence |
|------------|---------------------|----------|
| Fixed threshold | Exact value + unit + source | Algorithm/Design document |
| Lab-specific value (Cell ID, IP) | Selection rule + allowed range | Test environment guide |
| Boundary value | Boundary + just below/at/just above | Requirement/Algorithm |
| API Enum/Switch | Allowed values + invalid value rules | Interface Spec |

### Block 2-3: Procedure Executability

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| Non-existent API | MODIFY | Interface Spec evidence |
| Wrong parameter | MODIFY | Interface Spec evidence |
| Missing step | ADD | Design/Procedure flow evidence |
| Step order issue | MODIFY | Design/Sequence evidence |

**Do NOT generate proposal when:**
- API/parameter evidence is `INSUFFICIENT` → Generate clarification request
- Design evidence conflicts → Generate conflict report

### Block 2-4: Observability & Pass/Fail

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| No observation point | ADD | Design/Interface evidence |
| Wrong expected result | MODIFY | Requirement/Design evidence |
| Missing P/F criterion | ADD | Requirement evidence |
| Ambiguous criterion | MODIFY | Requirement/Design evidence |

**Good P/F Structure:**
```text
Condition → Observation Point → Field/Metric → Expected Value → Pass/Fail
```

### Block 2-5: Scenario Coverage

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| Missing negative scenario | ADD | Requirement/Design evidence |
| Missing boundary scenario | ADD | Requirement/Algorithm evidence |
| Missing state transition | ADD | Design/State machine evidence |
| Missing historical issue scenario | ADD | Issue/Bug report evidence |

**ISTQB Techniques as Evidence:**
- Equivalence Partitioning → Supports negative scenario proposal
- Boundary Value Analysis → Supports boundary scenario proposal
- State Transition Testing → Supports state transition proposal
- Error Guessing → Supports abnormal scenario proposal (with caution)

**Note**: ISTQB techniques are `SUGGESTED` evidence, not `CONFIRMED`. Product behavior must be confirmed by requirement/design.

### Block 2-6: Historical Risk & Consistency

**Generate Change Proposal when:**

| Condition | Operation | Evidence Required |
|-----------|-----------|-------------------|
| TC conflicts with Strong Evidence | MODIFY | Strong evidence |
| Missing historical issue reflection | ADD | Issue/Bug report |
| Internal TC inconsistency | MODIFY | TC internal consistency |
| Evidence document conflict | REPORT | Both conflicting documents |

**Do NOT generate proposal when:**
- Evidence documents conflict (`CONFLICT`) → Generate conflict report
- Historical issue applicability unclear → Generate clarification request

---

## Phase 3 Controlled Merge Rules

### Block 3-3: Approved Change Classification

**Classification Rules:**

| Reviewer Decision | Merge Candidate | Apply Text |
|-------------------|-----------------|------------|
| `ACCEPT` | Include | Phase 2 `proposed_text` |
| `EDIT_AND_ACCEPT` | Include | Reviewer `approved_text` |
| `REJECT` | Exclude | N/A |
| `HOLD` | Exclude | N/A |
| `WAITING` | Error | N/A (Gate 3 failure) |

### Block 3-4: Controlled Merge Planning

**Target Location Verification:**

1. Use Section + Item ID as primary anchor
2. Use original text hash as secondary anchor
3. If multiple matches found → `AMBIGUOUS_TARGET`, stop merge
4. If original text changed → `ANCHOR_DRIFT`, stop merge

**Operation Application Rules:**

| Operation | Rule |
|-----------|------|
| `ADD` | Insert approved text before/after specified position |
| `MODIFY` | Replace exactly matching `before_text` with `after_text` |
| `DELETE` | Remove exactly matching target text only |
| `SPLIT` | Replace composite step with multiple approved steps |

**Same Position Multiple Changes:**

- Different additions → Apply in approval order
- Same text, different modifications → `MERGE_CONFLICT`, stop
- One delete, one modify same item → `MERGE_CONFLICT`, stop

### Block 3-5: TC v2 Generation & Integrity Check

**Verification Items:**

1. TC v1 ID/title/original intent preserved?
2. All `ACCEPT`/`EDIT_AND_ACCEPT` changes applied?
3. All `REJECT`/`HOLD` changes NOT applied?
4. No unapproved modifications by AI during merge?
5. Section structure and numbering valid?
6. Procedure step and P/F references not broken after merge?
7. No duplicate additions of same content?
8. No remaining merge conflicts?

**Integrity Check:**

```text
All Diff Lines
→ Must connect to exactly one or more approved Change ID
→ If any Diff without connection → Integrity Fail
```

**Output Status:**

| Status | Condition |
|--------|-----------|
| `FINAL` | All decisions complete, no P1 hold, integrity pass |
| `FINAL_WITH_HOLDS` | P2/P3 holds exist, no P1 hold, integrity pass |
| `REVIEW_INCOMPLETE_P1_HOLD` | P1 hold exists, draft only |
| `MERGE_BLOCKED` | Target conflict, original mismatch, unapproved diff |

---

## Change Proposal Schema (Phase 2 Output)

```yaml
change_id: CHG-001
review_block_id: "2-4"  # Block that generated this proposal
priority: P1 | P2 | P3
priority_reason_code: DIRECT_REQUIREMENT_CONFLICT | WRONG_EXPECTED_RESULT | ...
operation: ADD | MODIFY | DELETE | SPLIT | CLARIFICATION_REQUEST
tc_location:
  section: "C. Pass/Fail Criteria"
  item_id: "PF-02"
  original_text_hash: "sha256:..." | null
issue_type: missing | incorrect | ambiguous | inconsistent | non_executable | non_observable
finding: "Resolution OFF 일 때 기대 결과가 없음"
impact: "주파수별 ON/OFF 요구사항을 판정할 수 없음"
before_text: null | string
proposed_text: "Resolution Switch 가 OFF 인 Target Carrier 에서는..."
rationale: "FR-11 v2.0 §3.2 에서 Carrier 별 제어를 요구함"
related_requirement_ids: ["FR-11"]
evidence_refs: ["EVD-0001", "EVD-0005"]
evidence_status: CONFIRMED | SUGGESTED | CONFLICT | INSUFFICIENT
evidence_status_label_ko: "근거로 확인됨"
limitations: []
dependency_change_ids: []  # For linked changes
reviewer_decision: WAITING | ACCEPT | EDIT_AND_ACCEPT | REJECT | HOLD
```

---

## Prohibited Actions

### Phase 2 Prohibited Actions

- ❌ Generate TC v2 before Reviewer decision
- ❌ Auto-apply changes without Reviewer approval
- ❌ Generate Quality Report / Quality Score
- ❌ Generate AI approval/rejection recommendation
- ❌ Propose changes without evidence references
- ❌ Combine multiple independent changes into one Change ID
- ❌ Rewrite TC original text beyond proposed change scope
- ❌ Use ISTQB technique as `CONFIRMED` evidence (always `SUGGESTED`)

### Phase 3 Prohibited Actions

- ❌ Apply `REJECT` or `HOLD` changes
- ❌ Apply changes with `WAITING` decision
- ❌ Apply `EDIT_AND_ACCEPT` without `approved_text`
- ❌ Modify TC v1 original file (always copy first)
- ❌ Create new changes not in Review Queue
- ❌ Modify Reviewer's `approved_text`
- ❌ Merge when anchor drift detected
- ❌ Generate TC v2 with unapproved diffs

---

## Revision Policy

This document is revised when:

1. New change proposal rules are added to Phase 2
2. Controlled merge rules change in Phase 3
3. Evidence status codes are modified
4. New priority reason codes are introduced
5. Change proposal schema changes

---

**Last Updated**: 2026-07-22  
**Version**: 3.0 (Human-in-the-loop Workflow)
