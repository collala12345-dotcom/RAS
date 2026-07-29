# AI-RAN TC Enhancement Phase 3 알고리즘 설계서

## Human-controlled Finalization

## 0. 문서 정보

| 항목 | 내용 |
|---|---|
| 문서 목적 | Reviewer의 변경별 결정을 검증하고, 승인된 변경만 TC v1에 통제 병합하여 TC v2와 변경 이력을 생성하는 알고리즘 정의 |
| 적용 단계 | Phase 3. Human-controlled Finalization |
| 입력 | TC v1, Phase 2 검토 제안서, Reviewer Decision Record |
| 최종 출력 | Enhanced TC v2, Change History |
| 핵심 원칙 | AI의 제안 정확성을 가정하지 않는다. Reviewer가 승인한 변경만 반영한다. |

---

## 1. Phase 3의 역할

Phase 3는 새로운 검토 의견을 만드는 단계가 아니다. Reviewer가 입력한 결정을 기계적으로 검증하고 승인 범위 안에서만 TC를 변경하는 단계이다.

```text
근거 기반 TC 검토 제안서
→ Reviewer가 Change ID별 결정 입력
→ 결정 Record 저장
→ 결정 완전성·유효성 검증
→ 승인 대상만 분류
→ 승인된 변경만 TC v1에 병합
→ TC v2 생성
→ 모든 결정과 실제 반영 결과를 Change History로 기록
```

이 단계에서 안정적인 것은 AI 판단 성능이 아니라 변경 프로세스이다.

- AI 제안이 틀릴 가능성을 허용한다.
- Reviewer는 변경별로 승인·거절·수정 후 승인·보류할 수 있다.
- 승인 전 원본 TC v1은 보존한다.
- 거절·보류·결정 대기 항목은 TC v2에 반영하지 않는다.
- 누가 어떤 제안을 어떤 문장으로 승인했는지 기록한다.

---

## 2. 전체 블록 구조

| Block | 이름 | 핵심 행동 | 주요 출력 |
|---|---|---|---|
| 3-1 | Reviewer Decision Collection | Change ID별 결정과 의견 수집 | Decision Record Draft |
| 3-2 | Decision Validation | 결정값·필수 입력·제안 존재 여부 검증 | Validated Decision Record |
| Gate 3 | Decision Readiness Gate | 병합 가능한 상태인지 판정 | READY_TO_MERGE / RETURN_TO_REVIEWER / BLOCKED |
| 3-3 | Approved Change Classification | 승인·수정 후 승인만 반영 대상으로 분류 | Merge Candidate List |
| 3-4 | Controlled Merge Planning & Application | 원본 위치 검증 후 승인 변경만 병합 | Patched TC Working Copy |
| 3-5 | TC v2 Generation & Integrity Check | 구조·의도·미승인 반영 여부 검증 | Enhanced TC v2 |
| 3-6 | Change History Generation | 결정과 실제 반영 결과 기록 | Change History |
| 3-7 | Final Output Packaging | 최종 파일과 상태 패키징 | Final Output Package |

---

## 3. Reviewer Decision Interface

### 3.1 MVP 입력 방식

Cline 기반 MVP에서는 별도 웹 UI보다 `Change ID 기반 대화 입력`을 사용한다.

```text
CHG-001: 승인

CHG-002: 수정 후 승인
최종 반영 내용:
Invalid value, empty value 및 허용 범위 외 값을 입력하고,
정의된 오류 응답과 System Log를 확인한다.

CHG-003: 거절
사유: 이번 Release 검증 범위에 포함되지 않음

CHG-004: 보류
사유: API 담당자에게 기준 Parameter 확인 필요
```

시스템은 자연어 입력을 곧바로 병합하지 않고, 먼저 구조화된 Decision Record로 변환한 뒤 Reviewer에게 요약 확인을 받을 수 있다.

### 3.2 향후 UI 확장 형태

```text
[승인] [거절] [수정 후 승인] [보류]

Reviewer 의견: __________________________
최종 반영 내용: _________________________
```

MVP와 UI 버전은 입력 방식만 다르며, 이후 Decision Validation과 Merge 알고리즘은 동일하게 사용한다.

---

## 4. 결정 상태 정의

| Reviewer 결정 | 의미 | 필수 추가 입력 | TC v2 반영 |
|---|---|---|---|
| 승인 | AI가 제안한 변경문을 그대로 수용 | 선택: 의견 | 반영 |
| 거절 | 제안을 수용하지 않음 | 권장: 거절 사유 | 미반영 |
| 수정 후 승인 | Reviewer가 고친 최종 문장으로 수용 | 필수: 최종 반영 내용 | 수정 문장으로 반영 |
| 보류 | 추가 자료·담당자 확인 후 결정 | 필수: 보류 사유 또는 확인 필요사항 | 이번 TC v2에 미반영 |
| 결정 대기 | 아직 Reviewer가 판단하지 않음 | 없음 | 병합 금지 |

`수정`이라는 상태만 단독으로 사용하지 않는다. 실제 반영할 최종 문장이 있어야 하므로 상태명은 `수정 후 승인`으로 고정한다.

---

## 5. 공통 입력 계약

```yaml
phase3_input:
  original_tc_v1:
    path: string
    checksum: string
    tc_id: string
  review_proposal:
    review_id: REVIEW-COM-001
    gate2_status: READY_FOR_REVIEW
    changes: [ChangeProposal]
  reviewer_decision_record:
    review_id: REVIEW-COM-001
    reviewer_id: string
    reviewed_at: datetime
    decisions: [Decision]
```

TC v1의 checksum 또는 동등한 무결성 식별자를 저장하여 Phase 2 이후 원본이 바뀌지 않았는지 확인한다. 원본이 달라졌다면 잘못된 위치에 변경을 적용할 수 있으므로 병합을 중단한다.

---

## 6. Block 3-1. Reviewer Decision Collection

### 6.1 목적

Reviewer의 자연어 결정을 Change ID별 구조화 데이터로 변환하고, 누락된 입력을 식별한다.

### 6.2 상세 수행 알고리즘

1. Reviewer 입력에서 Change ID를 추출한다.
2. 각 Change ID에 승인·거절·수정 후 승인·보류 중 하나를 매핑한다.
3. `수정 후 승인`의 최종 반영 문장을 별도 필드로 추출한다.
4. 거절·보류의 사유를 Reviewer Comment로 저장한다.
5. 한 Change ID에 두 결정이 입력되면 마지막 값을 임의 채택하지 않고 충돌로 표시한다.
6. 검토 제안서에 없는 Change ID는 Unknown Decision으로 분리한다.
7. Reviewer 입력을 AI가 의미적으로 확장하거나 재작성하지 않는다.

### 6.3 Decision Record Schema

```yaml
review_id: REVIEW-COM-001
proposal_version: "1.0"
original_tc_checksum: string
reviewer:
  reviewer_id: string
  reviewer_name: string | null
reviewed_at: "2026-07-21T11:00:00+09:00"
decisions:
  - change_id: CHG-001
    action_code: ACCEPT
    action_label_ko: 승인
    reviewer_comment: ""
    approved_text: null
  - change_id: CHG-002
    action_code: EDIT_AND_ACCEPT
    action_label_ko: 수정 후 승인
    reviewer_comment: "빈 값과 범위 외 값 포함"
    approved_text: "Invalid value, empty value 및 허용 범위 외 값을 입력하고 정의된 오류 응답과 System Log를 확인한다."
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

### 6.4 Output

- `Decision Record Draft`
- `Unparsed Input List`
- `Unknown Change ID List`
- `Missing Decision List`

---

## 7. Block 3-2. Decision Validation

### 7.1 목적

병합 전에 Reviewer 결정의 완전성·일관성·권한 범위를 검사한다.

### 7.2 상세 수행 알고리즘

1. Decision Record의 `review_id`가 Review Proposal과 같은지 확인한다.
2. 모든 Decision의 Change ID가 Proposal에 존재하는지 확인한다.
3. Change ID별 결정이 하나만 존재하는지 확인한다.
4. `수정 후 승인`에는 `approved_text`가 비어 있지 않은지 확인한다.
5. `승인`에는 Phase 2의 `proposed_change`가 존재하는지 확인한다.
6. `보류`에는 확인 필요사항 또는 사유가 있는지 확인한다.
7. 결정 대기 항목과 미입력 항목을 구분한다.
8. Reviewer가 입력한 수정문이 해당 Change ID의 Target Section 범위를 명백히 벗어나는지 탐지한다.
9. 수정문이 다른 Proposal까지 함께 승인하는 표현이면 Atomic Decision으로 다시 분리하도록 요청한다.
10. 원본 TC checksum이 Phase 2 기준과 같은지 확인한다.

### 7.3 결정 완전성 정책

최종 TC v2 생성을 위해 모든 Change ID는 다음 중 하나의 명시적 상태를 가져야 한다.

```text
승인 / 거절 / 수정 후 승인 / 보류
```

`결정 대기`는 명시적 결정이 아니므로 남아 있으면 Reviewer에게 다시 입력을 요청한다. `보류`는 명시적 결정이므로 병합에서는 제외하되 Workflow를 계속할 수 있다.

### 7.4 P1 보류 정책

P1 항목이 보류되어도 기술적으로 TC v2 Draft를 생성할 수 있지만, 최종 상태를 `FINAL`로 표시해서는 안 된다.

```text
P1 보류 존재
→ 승인 변경은 병합 가능
→ 출력 상태: REVIEW_INCOMPLETE_P1_HOLD
→ TC v2는 Draft로 표시
→ Change History 첫 부분에 P1 보류 경고 표시
```

P2/P3 보류는 미반영 상태와 사유를 Change History에 남기고 `FINAL_WITH_HOLDS`로 표시할 수 있다. 실제 조직 정책이 정해지면 이 규칙은 설정값으로 분리한다.

### 7.5 Output

```yaml
validated_decision_record:
  validation_status: VALID | INVALID | VALID_WITH_P1_HOLD
  accepted_ids: [CHG-001]
  edited_and_accepted_ids: [CHG-002]
  rejected_ids: [CHG-003]
  held_ids: [CHG-004]
  pending_ids: []
  validation_errors: []
  warnings:
    - "P1 CHG-004가 보류되어 최종 상태를 Draft로 제한"
```

---

## 8. Gate 3. Decision Readiness Gate

### 8.1 목적

Reviewer 입력이 안전하게 병합 가능한 상태인지 확인한다.

### 8.2 Gate 검사 항목

| Gate ID | 검사 질문 | 실패 시 처리 |
|---|---|---|
| G3-01 | Review ID와 Proposal Version이 일치하는가? | 병합 중단 |
| G3-02 | TC v1 checksum이 일치하는가? | 병합 중단, 재검토 필요 |
| G3-03 | 모든 Change ID가 실제 Proposal에 존재하는가? | Unknown ID 수정 요청 |
| G3-04 | Change ID별 결정이 하나뿐인가? | 충돌 해결 요청 |
| G3-05 | 결정 대기 항목이 없는가? | Reviewer 입력 요청 |
| G3-06 | 수정 후 승인 항목에 최종 반영 문장이 있는가? | Reviewer 입력 요청 |
| G3-07 | 승인 항목에 적용 가능한 제안 문장이 있는가? | Proposal 보완 요청 |
| G3-08 | 보류 항목에 사유 또는 확인 필요사항이 있는가? | 입력 보완 요청 |
| G3-09 | Reviewer 수정문이 Change ID의 범위를 초과하지 않는가? | 별도 Change로 분리 요청 |
| G3-10 | P1 보류가 경고와 Draft 상태로 처리되는가? | Gate Fail |

### 8.3 Gate 결과

| 결과 | 의미 | 다음 동작 |
|---|---|---|
| READY_TO_MERGE | 승인 범위가 명확하고 병합 가능 | Block 3-3 진행 |
| READY_TO_MERGE_WITH_WARNING | P1 보류 등 경고가 있으나 Draft 병합 가능 | 제한 상태로 진행 |
| RETURN_TO_REVIEWER | 결정·최종 문장·사유가 부족 | Reviewer 입력 보완 |
| BLOCKED | TC 원본/Proposal Version 불일치 등 안전 병합 불가 | 재검토 또는 Proposal 재생성 |

---

## 9. Block 3-3. Approved Change Classification

### 9.1 목적

Reviewer 결정을 반영 대상과 미반영 대상으로 분리하고, 실제 적용 문장을 확정한다.

### 9.2 분류 규칙

| 결정 | Merge Candidate | 적용 문장 |
|---|---|---|
| 승인 | 포함 | Phase 2 `proposed_change` |
| 수정 후 승인 | 포함 | Reviewer `approved_text` |
| 거절 | 제외 | 없음 |
| 보류 | 제외 | 없음 |
| 결정 대기 | 오류 | 병합 금지 |

### 9.3 상세 수행 알고리즘

1. 승인 항목의 Proposed Change를 원문 그대로 가져온다.
2. 수정 후 승인 항목은 Approved Text만 가져오며 AI 제안문과 자동 혼합하지 않는다.
3. 거절·보류 항목은 별도 Excluded List로 이동한다.
4. 같은 Target Section에 여러 승인 변경이 있으면 충돌 여부를 검사한다.
5. `linked_change_group`이 있는 변경은 적용 순서와 상호 의존성을 확인한다.
6. 삭제·대규모 대체 변경은 Reviewer 승인 여부와 Target 범위를 한 번 더 확인한다.

### 9.4 Output Schema

```yaml
merge_candidates:
  - change_id: CHG-001
    target_section: "C. Pass/Fail Criteria"
    target_item_id: "PF-02"
    operation: add
    final_approved_text: string
    decision_source: proposal | reviewer_edited
    apply_order: 1
excluded_changes:
  - change_id: CHG-003
    decision: 거절
    reason: string
```

---

## 10. Block 3-4. Controlled Merge Planning & Application

### 10.1 목적

TC v1의 구조와 의도를 보존하면서 승인된 최소 변경만 정확한 위치에 적용한다.

### 10.2 불변 조건

- 원본 TC v1 파일을 덮어쓰지 않는다.
- 승인되지 않은 문장은 추가·수정·삭제하지 않는다.
- TC Template의 Section 순서를 임의 변경하지 않는다.
- Reviewer의 Approved Text를 의미가 달라지도록 재작성하지 않는다.
- 병합 중 새 Gap을 발견하더라도 Phase 3에서 새 변경안을 자동 생성하지 않는다.

### 10.3 Merge Plan 생성

각 변경에 대해 실제 적용 전에 다음 계획을 만든다.

```yaml
merge_plan_item:
  change_id: CHG-001
  target_anchor:
    section: "C. Pass/Fail Criteria"
    item_id: "PF-02"
    original_text_hash: string | null
  operation: add | modify | delete | split
  before_text: string | null
  after_text: string
  apply_order: integer
  dependency_change_ids: [string]
```

### 10.4 Target 위치 검증

1. Section과 Item ID를 우선 사용한다.
2. Item ID가 없으면 원문 Anchor와 Section 조합을 사용한다.
3. 같은 원문이 여러 번 등장하면 자동 적용하지 않고 Ambiguous Target으로 중단한다.
4. 원문 Hash가 달라졌다면 TC v1 변경 가능성이 있으므로 병합하지 않는다.
5. 추가 위치가 모호하면 Reviewer 또는 Proposal 생성 단계로 되돌린다.

### 10.5 Operation별 적용 규칙

| Operation | 적용 규칙 |
|---|---|
| add | 승인된 문장을 지정 위치 전/후에 추가 |
| modify | 정확히 일치하는 Before Text만 After Text로 교체 |
| delete | 승인된 Target Text만 삭제, 주변 문장 보존 |
| split | 기존 복합 Step을 승인된 여러 Step으로 치환 |
| clarification_request | 병합 대상이 아니므로 제외 |

### 10.6 같은 위치의 복수 변경

- 서로 다른 문장을 추가하는 경우 승인 순서대로 적용한다.
- 같은 원문을 서로 다른 내용으로 수정하면 Merge Conflict로 중단한다.
- 한 변경이 삭제하고 다른 변경이 같은 항목을 수정하면 Merge Conflict이다.
- 상호 의존 Change 중 일부만 승인되면 결과가 불완전한지 확인하고 경고 또는 중단한다.

### 10.7 Output

- `Merge Plan`
- `Patched TC Working Copy`
- `Merge Conflict List`
- `Applied Change ID List`

---

## 11. Block 3-5. TC v2 Generation & Integrity Check

### 11.1 목적

Patched Working Copy가 승인 범위를 정확히 반영하는지 검사하고 Enhanced TC v2로 확정한다.

### 11.2 검증 항목

1. TC v1의 TC ID·제목·원래 검증 의도가 보존되는가?
2. 승인/수정 후 승인된 모든 Change ID가 반영되었는가?
3. 거절·보류 항목이 반영되지 않았는가?
4. AI가 병합 과정에서 추가한 미승인 문장이 없는가?
5. Section 구조와 번호가 유효한가?
6. Procedure Step과 P/F 참조가 병합 후 깨지지 않았는가?
7. 동일 내용을 중복 추가하지 않았는가?
8. Merge Conflict가 남아 있지 않은가?

### 11.3 무결성 비교

TC v1과 TC v2의 Diff를 생성하고, 모든 Diff 구간이 Applied Change ID 중 하나에 연결되는지 검사한다.

```text
모든 Diff Line
→ 정확히 하나 이상의 승인 Change ID에 연결
→ 연결되지 않은 Diff가 있으면 Integrity Fail
```

### 11.4 출력 상태

| 상태 | 조건 |
|---|---|
| FINAL | 모든 결정 완료, P1 보류 없음, 무결성 검사 통과 |
| FINAL_WITH_HOLDS | P2/P3 보류 존재, P1 보류 없음, 무결성 검사 통과 |
| REVIEW_INCOMPLETE_P1_HOLD | P1 보류 존재, 무결성 검사는 통과했으나 Draft만 허용 |
| MERGE_BLOCKED | Target 충돌·원본 불일치·미승인 Diff 존재 |

### 11.5 Output Header 예시

```yaml
tc_v2_metadata:
  source_tc_id: TC-COM-001
  source_version: v1
  output_version: v2
  review_id: REVIEW-COM-001
  finalization_status: FINAL_WITH_HOLDS
  applied_change_ids: [CHG-001, CHG-002]
  excluded_change_ids: [CHG-003, CHG-004]
```

### 11.6 Output

- `Enhanced TC v2`
- `TC v1 ↔ TC v2 Diff Map`
- `Integrity Check Result`

---

## 12. Block 3-6. Change History Generation

### 12.1 목적

모든 Change Proposal의 결정, Reviewer 의견, 실제 적용 문장, 미반영 사유를 추적 가능하게 기록한다.

### 12.2 Change History 필드

| 필드 | 의미 |
|---|---|
| Change ID | Phase 2에서 생성된 변경 식별자 |
| 우선순위 | P1/P2/P3 |
| TC 위치 | 변경 대상 Section/Item |
| 발견 내용 | TC v1에서 발견된 문제 |
| AI 변경 제안 | Phase 2 원래 제안 |
| 근거 상태 | 근거로 확인됨/보완 제안/문서 간 충돌/판단 근거 부족 |
| 상세 근거 | 문서·Version·Section·Page/Line |
| Reviewer 결정 | 승인/거절/수정 후 승인/보류 |
| Reviewer 의견 | 거절·보류·수정 이유 |
| 최종 반영 내용 | 실제 TC v2에 들어간 문장 |
| 반영 여부 | Applied/Not Applied |
| 미반영 사유 | 거절·보류·오류 등 |
| 검토자/시각 | 책임 추적 정보 |

### 12.3 Change History 표 예시

| Change ID | 우선순위 | Reviewer 결정 | 실제 반영 내용 | 반영 여부 | 사유/의견 |
|---|---|---|---|---|---|
| CHG-001 | P1 | 승인 | Resolution OFF 미동작 P/F 기준 | Applied | 제안대로 반영 |
| CHG-002 | P2 | 수정 후 승인 | Invalid·Empty·Out-of-range 및 오류 Log 확인 | Applied | Reviewer 문장으로 대체 |
| CHG-003 | P3 | 거절 | - | Not Applied | 이번 Release Scope 아님 |
| CHG-004 | P1 | 보류 | - | Not Applied | API 담당자 확인 필요 |

### 12.4 완전성 규칙

- Review Proposal의 모든 Change ID가 Change History에 정확히 한 번 등장해야 한다.
- Applied 항목은 TC v2 Diff와 연결되어야 한다.
- Not Applied 항목은 TC v2 Diff에 등장해서는 안 된다.
- 문서 간 충돌·판단 근거 부족 제안이 승인된 경우, Reviewer가 확정한 최종 근거 또는 문장을 기록해야 한다.

### 12.5 Output

- `Change History Markdown`
- `Change History JSON/YAML`

---

## 13. Block 3-7. Final Output Packaging

### 13.1 목적

최종 산출물을 고정된 구조로 제공하고 원본·제안·결정·결과의 연결을 보존한다.

### 13.2 사용자용 핵심 산출물

```text
1. Enhanced TC v2
   - 승인 및 수정 후 승인된 변경만 반영

2. Change History
   - 모든 제안의 결정과 실제 반영 결과 기록
```

### 13.3 시스템 보존 파일

사용자 화면에서는 두 핵심 산출물을 우선 보여주되 재현성과 감사 추적을 위해 다음 구조화 파일을 보존한다.

```text
- original_tc_v1.md
- review_proposal.md
- reviewer_decisions.yaml
- enhanced_tc_v2.md
- change_history.md
- diff_map.json
- finalization_manifest.yaml
```

### 13.4 Finalization Manifest

```yaml
finalization_manifest:
  review_id: REVIEW-COM-001
  source_tc_checksum: string
  proposal_version: "1.0"
  reviewer_id: string
  finalization_status: FINAL | FINAL_WITH_HOLDS | REVIEW_INCOMPLETE_P1_HOLD
  proposal_count: 4
  accepted_count: 1
  edited_and_accepted_count: 1
  rejected_count: 1
  held_count: 1
  applied_change_ids: [CHG-001, CHG-002]
  output_tc_v2_path: string
  change_history_path: string
```

### 13.5 최종 경고 표시

다음 조건은 최종 결과 첫 부분에 경고로 표시한다.

- P1 보류
- 문서 간 충돌이 해결되지 않은 채 보류
- 판단 근거 부족으로 미확정된 핵심 Parameter/API
- 일부 승인 변경의 Merge 실패
- Target Release가 확인되지 않음

---

## 14. Phase 3 의사코드

```text
function run_phase3(tc_v1, review_proposal, reviewer_input):
    decision_draft = parse_reviewer_decisions(reviewer_input)
    validated = validate_decisions(
        decision_draft,
        review_proposal,
        tc_v1.checksum
    )

    gate3 = evaluate_decision_readiness(validated)

    if gate3 == RETURN_TO_REVIEWER:
        return missing_or_invalid_decision_request(validated)

    if gate3 == BLOCKED:
        stop_without_modifying_tc_v1()

    merge_candidates, excluded = classify_decisions(validated)
    merge_plan = build_merge_plan(tc_v1, merge_candidates)

    if has_target_conflict(merge_plan):
        return MERGE_BLOCKED

    working_copy = copy_without_overwriting(tc_v1)
    patched = apply_only_approved_changes(working_copy, merge_plan)

    diff_map = build_diff_map(tc_v1, patched, merge_candidates)
    integrity = verify_every_diff_is_approved(diff_map)

    if integrity.failed:
        discard_working_result_and_return_blocked()

    tc_v2 = finalize_tc_v2(patched, validated.warnings)
    history = build_complete_change_history(
        review_proposal,
        validated,
        diff_map
    )

    return package(tc_v2, history, validated, diff_map)
```

---

## 15. 실패 및 복구 규칙

| 실패 상황 | 처리 | 원본 TC v1 영향 |
|---|---|---|
| 알 수 없는 Change ID | Reviewer 입력 수정 요청 | 없음 |
| 수정 후 승인 문장 누락 | 해당 결정 보완 요청 | 없음 |
| TC v1 checksum 불일치 | Proposal 재검토 또는 재생성 | 없음 |
| Target Anchor 중복 | 자동 병합 중단 | 없음 |
| 같은 위치의 승인 변경 충돌 | Reviewer에게 병합 방식 요청 | 없음 |
| 미승인 Diff 탐지 | Working Copy 폐기, 병합 실패 기록 | 없음 |
| Change History 누락 | 최종 패키징 금지 | 없음 |

모든 실패는 원본 TC v1을 보존한 상태에서 처리한다.

---

## 16. Phase 3 완료 조건

Phase 3는 다음 조건을 모두 만족하면 완료된다.

- 모든 Change ID가 승인·거절·수정 후 승인·보류 중 하나로 결정되었다.
- `수정 후 승인` 항목에 Reviewer 최종 문장이 존재한다.
- Gate 3가 병합 가능 상태이다.
- 승인/수정 후 승인 항목만 Merge Candidate에 포함되었다.
- 원본 TC v1이 변경되지 않았다.
- TC v1↔v2의 모든 Diff가 승인 Change ID에 연결된다.
- 거절·보류 항목은 TC v2에 반영되지 않았다.
- Review Proposal의 모든 Change ID가 Change History에 기록되었다.
- P1 보류가 있으면 결과가 Draft/Review Incomplete로 표시되었다.
- Enhanced TC v2와 Change History가 최종 출력으로 생성되었다.

---

## 17. 최종 흐름 요약

```text
Phase 2 검토 제안서
→ Reviewer Decision 입력
→ Decision Record 구조화
→ Gate 3 결정 검증
→ 승인·수정 후 승인만 분류
→ 승인 범위 기반 Merge Plan
→ TC v1 복사본에 통제 병합
→ 미승인 Diff 검사
→ Enhanced TC v2 생성
→ 전체 결정 Change History 생성
```

Phase 3의 최종 정의는 다음과 같다.

> AI가 TC를 임의로 다시 작성하는 단계가 아니라, Reviewer가 변경별로 통제한 결정을 검증하고 승인된 내용만 추적 가능하게 반영하는 단계이다.

