# 08. Output Format (Human-in-the-loop Workflow)

## Purpose

Defines the output formats for each phase of the Human-in-the-loop TC Review Workflow.

---

## Phase 1 Output: Evidence Pack

### Evidence Pack Schema

```yaml
evidence_pack:
  pack_id: EPK-0001
  generated_at: "2026-07-22T13:00:00+09:00"
  tc_metadata:
    tc_id: TC-COM-001
    title: NR Cell Overshooting Detection/Resolution Verification
    target_rapp: COM
    feature_name: Overshooting Control
    related_requirement_ids: ["FR-11"]
  tc_v1_checksum: "sha256:abc123..."
  
  # Evidence by type
  requirement_evidence: [EvidenceRecord]
  design_evidence: [EvidenceRecord]
  algorithm_kpi_parameter_evidence: [EvidenceRecord]
  standard_evidence: [EvidenceRecord]
  legacy_tc_evidence: [EvidenceRecord]
  historical_risk_evidence: [EvidenceRecord]
  common_pattern_evidence: [EvidenceRecord]
  
  # Conflict and missing
  conflict_groups:
    - conflict_group_id: CFG-0001
      evidence_ids: [EVD-0003, EVD-0011]
      conflict_summary: "HLD and DLD define different target cell conditions"
      required_human_question: "Which document is the baseline for this Release?"
  missing_evidence:
    - missing_id: MIS-0001
      required_for: "API parameter validation"
      attempted_queries: ["COM Interface Spec API endpoint", "COM parameter definition"]
      effect_on_phase2: "Cannot confirm API parameter correctness"
  
  # Audit trail
  retrieval_audit:
    queries_executed: 45
    rejected_count: 12
    index_version: "2026-07-20"

gate1_result:
  status: READY | READY_WITH_GAPS | BLOCKED
  passed_checks: [G1-01, G1-02, G1-03]
  failed_checks: [G1-04]
  restrictions:
    - "Cannot confirm API parameter correctness without Interface Spec"
  human_input_required:
    - "Target Release Interface Spec required"
```

### Evidence Record Schema

```yaml
evidence_id: EVD-0001
source_type: requirement | design | interface | algorithm | kpi_parameter | standard | legacy_tc | issue | test_result | cross_rapp
document_title: "COM Functional Requirement"
document_version: "2.0"
release_scope: "SVR26A"
source_path: "data/raw/feature_specs/FR-11_COM_v2.0.md"
section_title: "3.2 Frequency-based Control"
section_number: "3.2"
page_start: 14 | unknown
page_end: 15 | unknown
line_start: 45 | unknown
line_end: 52 | unknown
source_excerpt: "The system shall control Overshooting Detection per Carrier Frequency..."
normalized_statement: "Carrier Frequency별 Detection ON/OFF 제어 요구사항"
related_requirement_ids: ["FR-11"]
related_tc_locations: ["TC-COM-001", "TC-COM-005"]
related_feature: "FGR-CC3101"
applicability:
  target_rapp_match: true
  feature_match: true
  release_match: true
  scope_match: true
relevance_reason: "Direct requirement for Carrier-based control verification"
evidence_grade: strong | supporting | weak | rejected | missing
allowed_usage:
  - validate_requirement
  - validate_design
  - validate_parameter
  - suggest_scenario
  - support_explanation
  - human_review_only
conflict_group_id: CFG-0001 | null
  retrieval_query_id: Q-0012
  retrieval_score: 0.95
  ```

---

## 📄 Evidence Citation 형식 (P0 Critical)

**모든 증거 인용은 원본 파일 형식 (PPTX/DOCX) 으로 해야 합니다!**

### Citation 생성 규칙

AI 는 JSONL chunk 의 `metadata.source_file` 과 `metadata.page_number` 를 사용하여 citation 을 생성합니다:

```yaml
# JSONL chunk metadata 예시
source_path: "data\\raw\\algorithm_docs\\SVR26A_Patch_COM_overshooting_algorithm_design.md"
metadata:
  source_file: "SVR26A_Patch_COM_overshooting_algorithm_design.pptx"
  page_number: 12

# AI citation 생성
if metadata.source_file.endswith('.pptx'):
    citation = f"{metadata.source_file}, Slide {metadata.page_number}"
elif metadata.source_file.endswith('.docx'):
    citation = f"{metadata.source_file}, Page {metadata.page_number}"
elif metadata.source_file.endswith('.pdf'):
    citation = f"{metadata.source_file}, Page {page_number}"
else:
    citation = f"{metadata.source_file}, Line {start_line}-{end_line}"
```

### 올바른 Citation 형식

| 원본 파일 | Citation 형식 | 예시 |
|-----------|---------------|------|
| **PPTX** | `{filename}.pptx, Slide {page_number}` | `SVR26A_COM_overshooting.pptx, Slide 12` |
| **DOCX** | `{filename}.docx, Page {page_number}` | `TS28536.docx, Page 45` |
| **PDF** | `{filename}.pdf, Page {page_number}` | `TS28.331.pdf, Page 102` |
| **MD** (원본이 MD 인 경우) | `{filename}.md, Line {start_line}-{end_line}` | `algorithm_design.md, Line 45-52` |

### Evidence Record 에 적용

```yaml
# Evidence Record 예시 (Citation 포함)
evidence_id: EVD-0001
source_type: algorithm
document_title: "COM Overshooting Algorithm Design"
document_version: "1.0"
source_path: "data\\raw\\algorithm_docs\\SVR26A_Patch_COM_overshooting_algorithm_design.md"
section_title: "3.2 Detection Logic"
page_start: 12  # PPTX Slide 번호
line_start: 45  # MD 변환 파일의 줄 번호 (참고용)

# Citation 생성 결과
citation: "SVR26A_Patch_COM_overshooting_algorithm_design.pptx, Slide 12"
```

### ❌ 잘못된 Citation 예시

```markdown
# 변환된 MD 파일을 인용하지 마세요!

❌ `SVR26A_COM_overshooting_algorithm_design.md:45-52`
   → 원본은 PPTX 입니다! Slide 번호를 사용해야 합니다.

❌ `algorithm_docs 폴더의 어떤 파일`
   → 파일명을 명시하세요.

❌ `source_path 없음`
   → metadata.source_file 을 사용하세요.
```

### ✅ 올바른 Citation 예시

```markdown
# 원본 파일 형식으로 인용하세요!

✅ `SVR26A_Patch_COM_overshooting_algorithm_design.pptx, Slide 12`
   > "Overshooting Cell 은 계획된 coverage 보다 실제 coverage 가 너무 넓어..."

✅ `23288-k10.docx, Page 45`
   > "NE List contains cells of different carrier frequency."

✅ `TS28.331.pdf, Page 102`
   > "TA (Timing Advance) represents the distance between UE and gNB."
```

---

## Phase 2 Output: Review Queue

### Review Queue (Markdown Table Format)

```markdown
# Review Queue - TC-COM-001

**Review ID**: REVIEW-COM-001  
**Generated At**: 2026-07-22T14:00:00+09:00  
**TC v1 Checksum**: sha256:abc123...  
**Gate 1 Status**: READY  

## Summary

| Priority | Count |
|----------|-------|
| P1 필수 확인 | 2 |
| P2 주요 보완 | 1 |
| P3 개선 제안 | 1 |
| **Total** | **4** |

## Change Proposals

| Change ID | 우선순위 | TC 위치 | 발견 내용 | 변경 제안 | 제안 이유 | 상세 근거 | 근거 상태 | Reviewer 결정 |
|-----------|----------|---------|-----------|-----------|-----------|-----------|-----------|---------------|
| CHG-001 | P1 필수 확인 | C. Pass/Fail Criteria #2 | Resolution OFF 일 때 기대 결과가 없음 | "Resolution Switch 가 OFF 인 Target Carrier 에서는 Resolution Action 이 수행되지 않고, Resolution 결과 목록과 System Log 에 해당 Action 이 기록되지 않아야 한다." | 주파수별 ON/OFF 요구사항을 판정할 수 없음 | FR-11 v2.0 §3.2 p.14 / HLD v2.1 §6.2 p.28 | 근거로 확인됨 | WAITING |
| CHG-002 | P2 주요 보완 | B. Procedure Step 3 | Invalid 입력 검증이 없음 | "Invalid value, empty value 및 허용 범위 외 값을 입력하고, 정의된 오류 응답과 System Log 를 확인한다." | 비정상 입력 처리 범위가 검증되지 않음 | Interface Spec v1.4 §4.3 p.19 / 동등분할 관점 | 보완 제안 | WAITING |
| CHG-003 | P1 필수 확인 | A. Precondition | HLD 와 DLD 의 대상 Cell 조건이 다름 | 기준 문서 확인 후 해당 조건 확정 | AI 가 임의로 기준을 선택할 수 없음 | HLD v2.1 §5.1 p.25 / DLD v2.0 §4.2 p.41 | 문서 간 충돌 | WAITING |
| CHG-004 | P3 개선 제안 | Test Overview | Feature ID 표기 불일치 | "FGR-CC3101"로 통일 | 문서 간 일관성 필요 | FR-11 v2.0 표지 | 근거로 확인됨 | WAITING |

## Reviewer Decision Guide

각 Change ID 에 대해 아래 중 하나로 결정해 주세요:

- **승인**: 제안문을 그대로 수용
- **수정후승인**: Reviewer 가 고친 최종 문장으로 수용 (최종 반영 내용 필수)
- **거절**: 제안을 수용하지 않음 (사유 권장)
- **보류**: 추가 자료·확인 후 결정 (사유 필수)

### 입력 예시

```
CHG-001: 승인

CHG-002: 수정후승인
최종 반영 내용:
"Invalid value, empty value 및 허용 범위 외 값을 입력하고,
정의된 오류 응답과 System Log 를 확인한다."

CHG-003: 거절
사유: 이번 Release 검증 범위에 포함되지 않음

CHG-004: 보류
사유: API 담당자에게 기준 Parameter 확인 필요
```
```

### Review Queue JSON Schema

```json
{
  "review_id": "REVIEW-COM-001",
  "tc_id": "TC-COM-001",
  "tc_v1_path": "output/input_tc/TC-COM-001_v1.md",
  "tc_v1_checksum": "sha256:abc123...",
  "generated_at": "2026-07-22T14:00:00+09:00",
  "gate1_status": "READY",
  "proposal_count": {
    "p1": 2,
    "p2": 1,
    "p3": 1,
    "total": 4
  },
  "proposals": [
    {
      "change_id": "CHG-001",
      "review_block_id": "2-4",
      "priority": "P1",
      "priority_reason_code": "DIRECT_REQUIREMENT_CONFLICT",
      "operation": "ADD",
      "tc_location": {
        "section": "C. Pass/Fail Criteria",
        "item_id": "PF-02"
      },
      "issue_type": "missing",
      "finding": "Resolution OFF 일 때 기대 결과가 없음",
      "impact": "주파수별 ON/OFF 요구사항을 판정할 수 없음",
      "before_text": null,
      "proposed_text": "Resolution Switch 가 OFF 인 Target Carrier 에서는...",
      "rationale": "FR-11 v2.0 §3.2 에서 Carrier 별 제어를 요구함",
      "related_requirement_ids": ["FR-11"],
      "evidence_refs": ["EVD-0001", "EVD-0005"],
      "evidence_status": "CONFIRMED",
      "evidence_status_label_ko": "근거로 확인됨",
      "limitations": [],
      "dependency_change_ids": [],
      "reviewer_decision": "WAITING"
    }
  ]
}
```

### Evidence Status Codes

| Code | Label (KO) | Meaning |
|------|------------|---------|
| `CONFIRMED` | 근거로 확인됨 | Direct evidence confirms the issue |
| `SUGGESTED` | 보완 제안 | Supporting evidence or test technique suggests improvement |
| `CONFLICT` | 문서 간 충돌 | Conflicting evidence exists |
| `INSUFFICIENT` | 판단 근거 부족 | Insufficient evidence to confirm |

---

## Reviewer Decision Record

### Decision Record YAML Format

```yaml
review_id: REVIEW-COM-001
proposal_version: "1.0"
original_tc_checksum: "sha256:abc123..."
reviewer:
  reviewer_id: "user001"
  reviewer_name: "Kim, James"
reviewed_at: "2026-07-22T15:00:00+09:00"
decisions:
  - change_id: CHG-001
    action_code: ACCEPT
    action_label_ko: 승인
    reviewer_comment: "제안대로 반영"
    approved_text: null
  - change_id: CHG-002
    action_code: EDIT_AND_ACCEPT
    action_label_ko: 수정후승인
    reviewer_comment: "빈 값과 범위 외 값 포함"
    approved_text: "Invalid value, empty value 및 허용 범위 외 값을 입력하고, 정의된 오류 응답과 System Log 를 확인한다."
  - change_id: CHG-003
    action_code: REJECT
    action_label_ko: 거절
    reviewer_comment: "이번 Release 검증 범위가 아님"
    approved_text: null
  - change_id: CHG-004
    action_code: HOLD
    action_label_ko: 보류
    reviewer_comment: "API 담당자 확인 필요"
    approved_text: null
```

### Decision Action Codes

| Action Code | Label (KO) | Required Input | Reflected in TC v2 |
|-------------|------------|----------------|-------------------|
| `ACCEPT` | 승인 | Optional comment | Yes |
| `EDIT_AND_ACCEPT` | 수정후승인 | **approved_text required** | Yes (with approved_text) |
| `REJECT` | 거절 | Recommended reason | No |
| `HOLD` | 보류 | **reason required** | No |

---

## Phase 3 Output: TC v2 + Change History

### Enhanced TC v2 Header

```yaml
---
tc_id: TC-COM-001
version: v2
source_version: v1
review_id: REVIEW-COM-001
finalization_status: FINAL_WITH_HOLDS
applied_change_ids: [CHG-001, CHG-002]
excluded_change_ids: [CHG-003, CHG-004]
generated_at: "2026-07-22T16:00:00+09:00"
---
```

### Change History Format

```markdown
# Change History - TC-COM-001

**Review ID**: REVIEW-COM-001  
**Generated At**: 2026-07-22T16:00:00+09:00  

## Summary

| Decision | Count |
|----------|-------|
| 승인 | 1 |
| 수정후승인 | 1 |
| 거절 | 1 |
| 보류 | 1 |
| **Total** | **4** |

## Detailed Changes

| Change ID | 우선순위 | Reviewer 결정 | 실제 반영 내용 | 반영 여부 | 사유/의견 |
|-----------|----------|---------------|----------------|-----------|-----------|
| CHG-001 | P1 | 승인 | Resolution OFF 미동작 P/F 기준 추가 | Applied | 제안대로 반영 |
| CHG-002 | P2 | 수정후승인 | Invalid·Empty·Out-of-range 및 오류 Log 확인 | Applied | Reviewer 문장으로 대체 |
| CHG-003 | P3 | 거절 | - | Not Applied | 이번 Release Scope 아님 |
| CHG-004 | P3 | 보류 | - | Not Applied | API 담당자 확인 필요 |

## Evidence Traceability

### CHG-001
- **Evidence**: EVD-0001 (FR-11 v2.0 §3.2 p.14), EVD-0005 (HLD v2.1 §6.2 p.28)
- **TC v2 Location**: C. Pass/Fail Criteria, PF-02
- **Diff**: Lines 45-47 added

### CHG-002
- **Evidence**: EVD-0012 (Interface Spec v1.4 §4.3 p.19)
- **TC v2 Location**: B. Procedure, Step 3
- **Diff**: Lines 28-30 modified
```

### Finalization Manifest

```yaml
finalization_manifest:
  review_id: REVIEW-COM-001
  source_tc_checksum: "sha256:abc123..."
  proposal_version: "1.0"
  reviewer_id: "user001"
  finalization_status: FINAL | FINAL_WITH_HOLDS | REVIEW_INCOMPLETE_P1_HOLD | MERGE_BLOCKED
  proposal_count: 4
  accepted_count: 1
  edited_and_accepted_count: 1
  rejected_count: 1
  held_count: 1
  applied_change_ids: [CHG-001, CHG-002]
  excluded_change_ids: [CHG-003, CHG-004]
  output_tc_v2_path: "output/enhanced_tc/TC-COM-001_v2.md"
  change_history_path: "output/change_history/TC-COM-001_history.md"
  integrity_check:
    all_diffs_linked: true
    unapproved_diffs: 0
    anchor_drift_detected: false
```

---

## File Naming Convention

| Output Type | Filename Pattern | Example |
|-------------|------------------|---------|
| Evidence Pack | `evidence_pack_{tc_id}_{timestamp}.json` | `evidence_pack_TC-COM-001_20260722_130000.json` |
| Review Queue | `review_queue_{tc_id}_{timestamp}.md` | `review_queue_TC-COM-001_20260722_140000.md` |
| Decision Record | `reviewer_decisions_{review_id}.yaml` | `reviewer_decisions_REVIEW-COM-001.yaml` |
| Enhanced TC v2 | `{tc_id}_v2.md` | `TC-COM-001_v2.md` |
| Change History | `{tc_id}_change_history.md` | `TC-COM-001_change_history.md` |
| Finalization Manifest | `finalization_manifest_{review_id}.yaml` | `finalization_manifest_REVIEW-COM-001.yaml` |

---

## Prohibited Outputs

The following outputs are **NOT** generated in this Human-in-the-loop Workflow:

- ❌ Quality Report
- ❌ Quality Score
- ❌ Risk Score / Risk Indicator
- ❌ AI Approval/Rejection Recommendation
- ❌ Auto-apply results (without Reviewer decision)
- ❌ TC v2 before Reviewer decision

---

## Revision Policy

This document is revised when:

1. New output formats are required by the workflow
2. Schema fields are added or removed
3. File naming conventions change
4. New evidence types are introduced
