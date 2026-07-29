# AI-RAN TC Enhancement Phase 2 알고리즘 설계서

## Structured Review & Change Proposal Generation

## 0. 문서 정보

| 항목 | 내용 |
|---|---|
| 문서 목적 | Evidence Pack을 근거로 TC v1의 오류·누락·모호함을 체계적으로 탐지하고, Reviewer가 판단할 최소 변경 단위의 검토 제안서를 생성하는 알고리즘 정의 |
| 적용 단계 | Phase 2. Structured Review & Change Proposal |
| 입력 | TC v1, Evidence Pack, Gate 1 결과, Core/Domain Review Rule |
| 1차 출력 | 근거 기반 TC 검토 제안서(Review Queue) |
| 다음 단계 | Reviewer Decision Workflow → Phase 3 |
| 핵심 원칙 | Phase 2는 TC v1을 수정하거나 TC v2를 생성하지 않는다. 변경 제안만 만든다. |

---

## 1. Phase 2의 역할

Phase 2는 모든 TC에 동일한 검토 순서를 적용하여 검토 누락을 줄이고, 발견된 문제를 Reviewer가 한 건씩 판단할 수 있는 변경 제안으로 변환한다.

```text
TC v1 + Evidence Pack
→ 고정된 검토 관점 실행
→ 오류·누락·모호함 후보 생성
→ 중복·상충 후보 정리
→ 최소 변경 단위의 Change Proposal 생성
→ P1/P2/P3 우선순위 부여
→ 근거 상태 부여
→ Gate 2 검증
→ 근거 기반 TC 검토 제안서 출력
```

Phase 2가 지켜야 할 핵심 경계는 다음과 같다.

- `발견 내용`과 `변경 제안`을 분리한다.
- 한 Change ID에는 Reviewer가 독립적으로 승인·거절할 수 있는 변경 하나만 포함한다.
- Requirement 위반과 “추가하면 좋은 개선”을 같은 확실성으로 표현하지 않는다.
- Reviewer 승인 전 TC v1의 원문은 변경하지 않는다.
- Quality Score나 AI의 TC 전체 승인 판정은 핵심 출력에 포함하지 않는다.

---

## 2. 전체 블록 구조

| Block | 이름 | 핵심 행동 | 주요 출력 |
|---|---|---|---|
| 2-1 | Requirement & Verification Point Coverage | 요구사항과 검증 포인트 대응 여부 확인 | Coverage Gap |
| 2-2 | Scope, Target & Precondition Review | 대상·범위·실험 전제 확인 | Scope/Precondition Gap |
| 2-3 | Procedure Executability Review | 실제 수행 가능한 절차인지 확인 | Execution Gap |
| 2-4 | Observability & Pass/Fail Review | 결과 관찰 및 객관 판정 가능성 확인 | Observation/PF Gap |
| 2-5 | Scenario Coverage Review | Positive·Negative·Boundary·Abnormal·Failure·Recovery 검토 | Scenario Gap |
| 2-6 | Historical Risk & Consistency Review | 과거 문제 반영 및 TC/문서 모순 확인 | Risk/Conflict Gap |
| 2-7 | Gap Normalization & Deduplication | 발견 후보를 표준 형태로 정리·중복 제거 | Normalized Gap List |
| 2-8 | Atomic Change Proposal Generation | 최소 변경 단위의 수정안 생성 | Change Proposal Draft |
| 2-9 | Priority & Evidence Status Assignment | P1/P2/P3와 한글 근거 상태 부여 | Prioritized Proposal |
| 2-10 | Review Queue Generation | Reviewer용 검토 제안서 생성 | Review Proposal Document |
| Gate 2 | Proposal Integrity Gate | 제안의 완전성·안전성 검사 | READY_FOR_REVIEW / RETURN_FOR_REWORK / BLOCKED |

---

## 3. 공통 입력 계약

```yaml
phase2_input:
  tc_v1: object
  tc_metadata: object
  evidence_pack: object
  gate1_result:
    status: READY | READY_WITH_GAPS | BLOCKED
    restrictions: [string]
  core_review_rules:
    - requirement_coverage
    - scope_control
    - procedure_executability
    - observability
    - pass_fail_clarity
    - scenario_coverage
    - consistency
  domain_rules:
    domain_name: string
    rules: [object]
```

Gate 1이 `READY_WITH_GAPS`이면 Phase 2는 확인 가능한 관점만 수행하고, 제한 대상 관점에서는 `근거로 확인됨` 상태를 생성하지 않는다. Gate 1이 `BLOCKED`여도 문법·TC 내부 모순처럼 외부 근거 없이 확인 가능한 일부 검토는 수행할 수 있지만, Requirement 기반 수정은 제한한다.

---

## 4. 공통 Gap Record

각 검토 블록이 발견한 결과는 아래 구조로 통일한다.

```yaml
gap_id: GAP-0001
review_block: "2-4"
tc_location:
  section: "C. Pass/Fail Criteria"
  item_id: "P/F-02"
  original_text: string | null
gap_type: missing | incorrect | ambiguous | inconsistent | non_executable | non_observable | uncovered_scenario
finding: string
impact: string
linked_requirement_ids: [string]
evidence_ids: [string]
evidence_limitations: [string]
candidate_change: string | null
candidate_priority: P1 | P2 | P3 | unassigned
```

`finding`에는 현재 TC의 문제만 기록하고, 해결 문장은 `candidate_change`에 별도로 기록한다.

---

## 5. Block 2-1. Requirement & Verification Point Coverage

### 5.1 목적

관련 Requirement의 atomic behavior가 TC의 Purpose·Procedure·P/F에 실제로 연결되어 있는지 확인한다.

### 5.2 Input

- TC v1 및 TC Location Map
- Atomic Requirement List
- Requirement/Design Evidence
- Gate 1 제한사항

### 5.3 상세 수행 알고리즘

1. 각 Atomic Requirement에 고유 ID를 부여한다.
2. 각 Requirement에 대해 다음 세 연결을 찾는다.
   - `Intent Link`: Test Purpose 또는 Overview가 요구사항을 검증 대상으로 선언하는가?
   - `Action Link`: Procedure가 요구 동작을 유발하거나 관찰하는가?
   - `Oracle Link`: Expected Result/PF가 요구 동작의 성공·실패를 판정하는가?
3. 세 Link를 Requirement Coverage Matrix에 기록한다.
4. 단순히 FR ID만 Related Feature에 적힌 경우 Coverage로 인정하지 않는다.
5. 하나의 Procedure가 여러 Requirement를 검증하면 각 Requirement의 관측 결과가 분리되는지 확인한다.
6. 요구사항의 ON/OFF, Include/Exclude, Success/Failure처럼 서로 다른 behavior branch를 각각 독립 VP로 분해한다.

### 5.4 Coverage 판정

| 상태 | 조건 |
|---|---|
| COVERED | Intent·Action·Oracle이 모두 있고 서로 연결됨 |
| PARTIAL | 세 Link 중 하나 이상이 없거나 모호함 |
| MISSING | TC에서 해당 Requirement를 검증하는 행동과 판정 기준을 찾을 수 없음 |
| CONFLICT | TC 내용이 Requirement와 반대이거나 다른 값을 사용함 |
| UNKNOWN | Requirement 근거가 부족해 판단할 수 없음 |

### 5.5 Output Schema

```yaml
requirement_coverage_matrix:
  - atomic_requirement_id: FR-11-A
    intent_link: [TC-PURPOSE-01]
    action_link: [TC-STEP-03]
    oracle_link: [TC-PF-02]
    status: COVERED | PARTIAL | MISSING | CONFLICT | UNKNOWN
    evidence_ids: [EVD-0001]
    gap_id: GAP-0001 | null
```

### 5.6 Gap 생성 규칙

- FR과 직접 반대인 P/F 또는 동작은 `incorrect`이며 P1 후보이다.
- Requirement의 핵심 대상 또는 branch가 빠지면 `missing`이며 P1 후보이다.
- Oracle만 빠져 검증 결과를 판정할 수 없으면 Block 2-4와 연결한다.
- Requirement 자체가 불명확하면 변경 문장을 만들지 말고 `문서 간 충돌` 또는 `판단 근거 부족` 후보로 넘긴다.

### 5.7 COM 예시

```text
Requirement: Carrier Frequency별 Detection/Resolution ON/OFF 제어
TC v1: Detection ON 결과만 확인
판정: OFF branch와 Resolution branch가 누락되어 PARTIAL
발견 내용: "Carrier별 기능 제어 요구사항 중 Detection OFF와 Resolution ON/OFF 결과가 검증되지 않음"
```

---

## 6. Block 2-2. Scope, Target & Precondition Review

### 6.1 목적

TC가 누구에게, 어떤 환경과 상태에서, 어떤 데이터로 수행되는지 명확하며 Requirement의 적용 범위와 일치하는지 확인한다.

### 6.2 검토 영역

- Target rAPP/System/NE/Cell/Carrier/Cluster
- 포함·제외 대상
- Release 및 Feature Enable 상태
- Dependency Service
- CM/PM 데이터 준비 상태
- Test Data와 Configuration File
- Switch/Parameter 초기 상태
- 기간·수집 주기·실행 환경

### 6.3 상세 수행 알고리즘

1. Evidence Pack에서 필수 Scope와 Precondition을 추출한다.
2. TC Precondition과 Test Data를 항목별로 비교한다.
3. 포함 대상과 제외 대상이 모두 정의되었는지 확인한다.
4. Procedure에서 사용하는 모든 변수·파일·API·Parameter가 Precondition에 준비되어 있는지 확인한다.
5. Lab마다 달라지는 값은 정확한 숫자 대신 `변수명 + 허용 영역 + 선택 규칙 + 입력 위치`가 있는지 확인한다.
6. 문서가 고정한 Threshold/Default/API Enum은 정확한 값·단위·출처가 있는지 확인한다.
7. 서로 다른 Frequency, Switch 조합, Cell 유형을 비교해야 하면 Test Data가 이를 구분할 수 있는지 확인한다.

### 6.4 값 구체성 판정 예시

| TC 표현 | 판정 | 이유 |
|---|---|---|
| `NR cells are prepared` | 모호 | Target 수, Carrier 구성, 포함/제외 기준 불명확 |
| `서로 다른 Carrier Frequency의 NR Cell을 포함한 NE List 준비` | 기본 충족 | 필요한 데이터 영역이 정의됨 |
| `Cell ID는 Lab 환경에서 선택하되 NE List 포함 Cell과 제외 Cell을 각각 1개 이상 지정` | 실행 가능 | 값 자체가 아니라 선택 규칙과 역할이 명확 |
| `Th_DMacTputOp는 설계 기본값 2.5 사용` | 근거 필요 | 고정값은 정확한 출처 확인 필요 |

### 6.5 Output

```yaml
scope_precondition_review:
  required_items: [string]
  present_items: [string]
  missing_items: [string]
  ambiguous_items: [string]
  conflicting_items: [string]
  unresolved_runtime_values: [string]
  gaps: [GapRecord]
```

### 6.6 우선순위 후보

- Scope 누락으로 다른 Cell/Carrier에 동작할 수 있으면 P1 후보.
- 실행에 필요한 Dependency·데이터·초기 상태 부족은 P2 후보.
- 문장 구조 또는 용어 명확화는 P3 후보.

---

## 7. Block 2-3. Procedure Executability Review

### 7.1 목적

실험자가 TC만 읽고 준비된 환경에서 모호한 추론 없이 각 Step을 수행할 수 있는지 확인한다.

### 7.2 실행 가능성 체크 모델

각 Procedure Step을 다음 6개 필드로 정규화한다.

```text
Actor → Action → Target → Input/Command → Expected Immediate Response → Next State
```

### 7.3 상세 수행 알고리즘

1. 복합 문장을 atomic step으로 분해한다.
2. 각 Step의 Actor와 Target을 식별한다.
3. “실행한다”, “설정한다”, “확인한다”의 대상·방법·입력을 확인한다.
4. API/Command는 문서에 정의된 이름·Method·Parameter인지 검증한다.
5. Step n이 요구하는 상태가 Step n-1 또는 Precondition에서 만들어지는지 확인한다.
6. 결과 관찰만 가능한 내부 동작을 직접 제어 Step으로 작성하지 않았는지 확인한다.
7. 런타임에서 변경 불가능한 설정을 Procedure가 바꾸도록 지시하지 않았는지 확인한다.
8. 실패 시 정리·복구가 필요한 경우 Cleanup/Recovery Step 존재 여부를 확인한다.

### 7.4 Step 판정

| 상태 | 조건 |
|---|---|
| EXECUTABLE | Actor·Action·Target·Input이 명확하고 선행 상태 충족 |
| PARTIAL | 수행 가능하지만 Parameter/명령/대상이 일부 모호 |
| NON_EXECUTABLE | 존재하지 않는 API, 허용되지 않는 제어, 순서 오류 등으로 수행 불가 |
| UNKNOWN | 설계 근거 부족으로 실행 가능 여부 미확정 |

### 7.5 Output

```yaml
procedure_review:
  - step_id: TC-STEP-01
    normalized_step: string
    actor: string | unknown
    action: string
    target: string | unknown
    input_or_command: string | unknown
    required_pre_state: string | unknown
    produced_post_state: string | unknown
    status: EXECUTABLE | PARTIAL | NON_EXECUTABLE | UNKNOWN
    gaps: [GapRecord]
```

### 7.6 우선순위 후보

- 존재하지 않는 API 또는 잘못된 Parameter는 P1.
- 실행에 필요한 Command 상세·Test Data가 부족하면 P2.
- 한 문장에 여러 Step이 결합된 가독성 문제는 P3.

---

## 8. Block 2-4. Observability & Pass/Fail Review

### 8.1 목적

TC 수행 후 시스템 결과를 실제로 관측할 수 있고, 관측값을 기준으로 Pass와 Fail을 객관적으로 구분할 수 있는지 확인한다.

### 8.2 관측 대상 우선순위

가능한 관측 수단은 기능에 따라 다음 중 하나 이상이어야 한다.

- API Response 및 Error Code
- System/Application Log
- Detected/Resolved Cell List 또는 Output File
- KPI/PM/CM 변화
- State/Status 값
- Alarm/Event/Notification
- DB/Persistent Volume 결과
- 외부 시스템 동작 결과

### 8.3 Oracle 구조

각 Expected Result/PF는 다음 형태로 정규화한다.

```text
조건(Condition)
→ 관측 위치(Observation Point)
→ 관측 항목(Field/Metric/Log Pattern)
→ 기대값(Expected Value/State)
→ 허용 시간 또는 기간
→ Pass 판정
→ Fail 판정
```

### 8.4 상세 수행 알고리즘

1. 각 Procedure Step과 대응 Expected Result/PF를 연결한다.
2. “정상 동작”, “성공 확인”처럼 관측 항목이 없는 문장을 탐지한다.
3. 설계가 정의한 System Log, API Response, KPI, Output을 TC가 관측하는지 확인한다.
4. 고정 Threshold가 필요한 경우 값·단위·비교 연산자·기간을 확인한다.
5. Negative 조건에서는 “동작하지 않는다”를 증명할 관측 지점이 있는지 확인한다.
6. 시간 지연이 있는 알고리즘은 Observation Window 또는 Resolution Period가 정의되었는지 확인한다.
7. Pass만 있고 Fail 조건이 묵시적인 경우, 객관적인 Fail 조건을 생성할 수 있는지 확인한다.

### 8.5 좋은 P/F 구조 예시

```text
조건: Target carrier의 Detection Switch = OFF
관측 위치: COM execution result의 detected cell list와 system log
기대 결과: 해당 carrier의 Cell이 detected cell list에 포함되지 않고 Detection 수행 log가 생성되지 않음
Pass: 두 관측 결과가 모두 기대 결과와 일치
Fail: 해당 Cell이 결과 목록에 포함되거나 Detection 수행 log가 존재
```

### 8.6 Output

```yaml
observability_pf_review:
  - verification_point_id: VP-001
    procedure_step_ids: [TC-STEP-03]
    observation_points: [string]
    expected_value_or_state: string | unknown
    observation_window: string | unknown
    pass_condition: string | unknown
    fail_condition: string | unknown
    status: TESTABLE | PARTIAL | NON_TESTABLE | UNKNOWN
    gaps: [GapRecord]
```

### 8.7 우선순위 후보

- 잘못된 Expected Result 또는 FR과 반대인 P/F는 P1.
- 핵심 결과 Log·API Response·KPI가 없어 판정이 불가능하면 P2, 단 핵심 Requirement 검증 자체가 불가능하면 P1.
- 표현의 객관화·Step 연결 개선은 P3.

---

## 9. Block 2-5. Scenario Coverage Review

### 9.1 목적

단일 Happy Path에 머무르지 않고 Requirement·설계·과거 Issue가 요구하는 핵심 조건 조합과 비정상 동작을 검토한다.

### 9.2 Scenario 분류

| 분류 | 의미 | 대표 생성 기법 |
|---|---|---|
| Positive | 정상 입력·정상 Dependency에서 기대 동작 | Requirement branch |
| Negative | OFF, Invalid, Excluded Target 등 동작 거부/미수행 | 동등분할 |
| Boundary | Threshold·최소/최대·빈 목록·단일/다중 값 경계 | 경계값 분석 |
| Decision Combination | 여러 Switch/조건의 조합 | Decision Table |
| State Transition | ON→OFF, Retry, Restart, Recovery 등 상태 변화 | 상태 전이 |
| Abnormal | 상용 문제 가능성이 있는 비정상 환경/데이터 | Error Guessing + Issue Evidence |
| Failure | API/Dependency/Data 수집 실패 | Failure Injection 후보 |
| Recovery | 실패 제거 후 정상 복구, 재시도, 상태 정합성 | State/Recovery 검증 |

ISTQB 기반 기법은 Scenario를 체계적으로 찾는 도구이지, 제품 동작의 직접 근거가 아니다. 제품의 Expected Result는 반드시 Requirement/Design/Issue 근거와 연결하거나 `보완 제안`으로 표시한다.

### 9.3 상세 수행 알고리즘

1. Requirement와 설계에서 입력 변수·상태·대상 필터를 추출한다.
2. 각 변수의 유효·무효·경계 클래스를 정의한다.
3. Switch나 조건이 2개 이상이면 Decision Table을 만든다.
4. 모든 조합을 무조건 TC로 만들지 않고 결과 동작이 다른 조합을 우선한다.
5. 과거 Issue의 Trigger와 Failure Symptom을 Scenario 후보에 연결한다.
6. 현재 TC에 이미 존재하는 Scenario와 비교한다.
7. 누락 후보마다 필수성 근거와 예상 관측 결과의 존재 여부를 확인한다.

### 9.4 COM Decision Table 예시

| Detection | Resolution | 기대 검증 관점 |
|---|---|---|
| ON | ON | Detection 후 대상 Cell에 Resolution 수행 |
| ON | OFF | Detection은 수행되지만 Resolution Action은 수행되지 않음 |
| OFF | ON | Detection 미수행 시 Resolution 대상 생성 여부와 비정상 동작 방지 확인 |
| OFF | OFF | 두 기능 모두 미수행이며 결과·Log에 잘못된 Action이 없어야 함 |

실제 기대 동작은 FR/HLD/DLD의 정의로 확정한다. 위 표와 설계가 다르면 표를 적용하지 않고 문서 충돌 또는 보완 제안으로 남긴다.

### 9.5 Output

```yaml
scenario_coverage_matrix:
  - scenario_id: SCN-001
    scenario_type: positive | negative | boundary | decision | state | abnormal | failure | recovery
    input_class_or_condition: string
    expected_behavior: string | unknown
    required_by: requirement | design | issue | review_technique
    evidence_ids: [string]
    existing_tc_locations: [string]
    coverage_status: COVERED | PARTIAL | MISSING | UNKNOWN
    gap_id: GAP-0001 | null
```

### 9.6 우선순위 후보

- 안전성·상용 장애 또는 과거 Field Issue 재발 조건 누락은 P1.
- 필수 Negative·Abnormal·주요 상태 전환·ON/OFF 조합 누락은 P2.
- 근거는 약하지만 추가하면 좋은 확장 Scenario는 P3 또는 보완 제안.

---

## 10. Block 2-6. Historical Risk & Consistency Review

### 10.1 목적

과거 문제의 재발 위험이 현재 TC에 반영됐는지 확인하고, TC 내부 및 근거 문서 사이의 모순을 탐지한다.

### 10.2 Historical Risk 검토 알고리즘

1. Historical Risk Evidence마다 Trigger·Symptom·Fixed Behavior를 현재 TC와 비교한다.
2. 같은 Failure Condition을 재현하거나 방지 동작을 검증하는 Step/PF가 있는지 확인한다.
3. Fix 이후 Release에서 더 이상 적용되지 않는 Issue인지 확인한다.
4. 적용 여부가 불명확하면 자동 Scenario 추가 대신 사람 확인 질문을 만든다.

### 10.3 Consistency 검토 알고리즘

다음 쌍을 비교한다.

- Overview ↔ Purpose
- Purpose ↔ Procedure
- Precondition ↔ Procedure
- Procedure ↔ Expected Result/PF
- Related FR ↔ 실제 Procedure/PF
- Step 간 NE/Cell/Frequency/Parameter/State
- TC v1 ↔ Requirement/HLD/DLD/Algorithm
- HLD ↔ DLD ↔ Interface ↔ Algorithm

### 10.4 충돌 처리 규칙

- TC가 Strong Evidence와 직접 다르면 `확인된 오류` 후보로 생성한다.
- 두 Strong Evidence가 서로 다르면 AI가 선택하지 않고 `문서 간 충돌`로 생성한다.
- 단순 명칭 차이는 동일 대상임을 확인할 수 있을 때만 정규화한다.
- 수치·단위·Enum 차이는 사소한 표현 불일치로 낮추지 않는다.

### 10.5 Output

- `Historical Coverage Gap`
- `TC Internal Inconsistency`
- `TC-to-Evidence Conflict`
- `Evidence-to-Evidence Conflict`
- `Human Clarification Question`

---

## 11. Block 2-7. Gap Normalization & Deduplication

### 11.1 목적

여러 검토 블록에서 같은 문제를 중복 보고하지 않도록 Gap을 표준화하고 병합한다.

### 11.2 상세 수행 알고리즘

1. Gap을 `TC 위치 + 문제 유형 + 영향 받는 Requirement + 의미` 기준으로 군집화한다.
2. 같은 원인으로 Procedure와 PF가 함께 부족한 경우 Reviewer가 독립 판단해야 하는지 확인한다.
3. 하나의 변경으로 두 위치를 함께 수정해야만 일관성이 생기면 `linked_change_group`으로 묶되 Change ID는 분리할 수 있다.
4. 상충하는 변경 제안은 병합하지 않고 Conflict로 유지한다.
5. 단순 문법·표현 문제는 기능 Gap과 분리한다.

### 11.3 병합 예시

```text
Gap A: Procedure에 Resolution OFF Step 없음
Gap B: P/F에 Resolution OFF 결과 없음

처리:
- 실행 Step 추가와 P/F 추가는 서로 다른 TC 위치이므로 CHG 2개 생성 가능
- 단, 같은 Scenario를 구성하므로 linked_change_group = LCG-001 부여
```

### 11.4 Output

```yaml
normalized_gap_list:
  - gap_id: GAP-0001
    duplicate_gap_ids: [GAP-0007]
    linked_change_group: LCG-001 | null
    finding: string
    impact: string
    target_locations: [object]
    evidence_ids: [string]
```

---

## 12. Block 2-8. Atomic Change Proposal Generation

### 12.1 목적

각 Gap을 Reviewer가 독립적으로 승인·거절·수정할 수 있는 최소 변경 단위로 변환한다.

### 12.2 Atomic Change 규칙

1. 하나의 Change ID는 하나의 판단만 요구한다.
2. `발견 내용`에는 현재 문제를, `변경 제안`에는 목표 상태를 쓴다.
3. 가능하면 TC에 실제 반영할 문장 또는 Step 수준으로 제시한다.
4. 정확한 값이나 동작을 확정할 근거가 없으면 빈칸을 AI가 채우지 않는다.
5. 문서 충돌 항목의 변경 제안은 수정문이 아니라 `확인 요청 + 확정 후 반영 위치`가 된다.
6. 원래 TC 의도를 변경하거나 Scope를 확장하는 제안은 명확히 표시한다.
7. 삭제 제안은 Requirement 또는 잘못된 동작 근거가 명확한 경우에만 만든다.

### 12.3 Change Proposal Schema

```yaml
change_id: CHG-001
linked_change_group: LCG-001 | null
target:
  section: "C. Pass/Fail Criteria"
  item_id: "PF-02"
  original_text: string | null
change_operation: add | modify | delete | split | clarification_request
finding: string
proposed_change: string
reason: string
impact_if_not_changed: string
evidence_ids: [string]
priority: unassigned
evidence_status: unassigned
reviewer_action: pending
```

### 12.4 좋은 변경 제안 예시

```text
발견 내용:
Resolution Switch가 OFF일 때의 Expected Result가 없음.

변경 제안:
C. Pass/Fail Criteria에 다음 기준을 추가한다.
"Resolution Switch가 OFF인 Target Carrier에서는 Resolution Action이 수행되지 않고,
Resolution 결과 목록과 System Log에 해당 Action이 기록되지 않아야 한다."
```

### 12.5 나쁜 변경 제안 예시

```text
"Negative Scenario를 더 추가한다."
```

나쁜 예시는 대상 위치, 입력 조건, 관측 결과, 판정 기준이 없어 Reviewer가 무엇을 승인하는지 알 수 없다.

---

## 13. Block 2-9. Priority & Evidence Status Assignment

### 13.1 목적

Reviewer가 먼저 확인할 항목을 객관적 규칙으로 정렬하고, AI가 어느 수준까지 확정할 수 있는지 한글 상태로 표시한다.

### 13.2 우선순위 규칙

| 우선순위 | 명칭 | 적용 조건 |
|---|---|---|
| P1 | 필수 확인 | FR 직접 충돌, 잘못된 Expected Result/PF, 검증 Scope 누락, 실행 불가능 API/Parameter/절차, 안전성·상용 장애·Field Issue 관련 누락, Strong Evidence 간 충돌 |
| P2 | 주요 보완 | 필수 Negative/Abnormal Scenario 누락, 주요 ON/OFF 조합·상태 전환 누락, Log/KPI/API Response 부족, 주요 Precondition/Test Data 모호 |
| P3 | 개선 제안 | 표현 명확화, 절차 세분화, 선택적 확장 Scenario, 형식·용어·가독성 개선 |

AI는 중요해 보인다는 주관적 이유만으로 P1을 부여하지 않는다. 위 규칙 중 하나를 `priority_reason_code`로 기록해야 한다.

### 13.3 근거 상태 한글 정의

| 화면 표시 | 의미 | 생성 조건 | 허용되는 변경안 |
|---|---|---|---|
| 근거로 확인됨 | 문서 근거로 오류·누락이 명확 | Strong Evidence와 직접 비교 가능 | 구체적 수정문 제시 가능 |
| 보완 제안 | 검토 기법·Legacy TC·보조 근거상 유용하나 필수 여부는 사람 판단 | Supporting Evidence 또는 Coverage 기법 기반 | 제안문 제시, 자동 확정 금지 |
| 문서 간 충돌 | 동일 항목에 대해 근거 문서가 다름 | Strong/Supporting Evidence 간 상충 | 기준 문서 확인 요청 |
| 판단 근거 부족 | 필요한 문서나 위치를 찾지 못해 확정 불가 | Missing/Weak Evidence | 자료 요청 또는 확인 질문만 제시 |

내부 데이터에서는 영문 code를 사용할 수 있지만 Reviewer 화면에는 한글을 우선 표시한다.

```yaml
evidence_status_code: CONFIRMED | SUGGESTED | CONFLICT | EVIDENCE_MISSING
evidence_status_label_ko: 근거로 확인됨 | 보완 제안 | 문서 간 충돌 | 판단 근거 부족
```

### 13.4 우선순위 결정 의사코드

```text
function assign_priority(proposal):
    if direct_requirement_conflict(proposal): return P1
    if wrong_or_non_executable_core_behavior(proposal): return P1
    if commercial_or_safety_issue_gap(proposal): return P1
    if strong_evidence_conflict_requires_human(proposal): return P1

    if required_negative_or_abnormal_gap(proposal): return P2
    if major_state_or_switch_combination_gap(proposal): return P2
    if observation_or_precondition_gap(proposal): return P2

    return P3
```

### 13.5 정렬 규칙

```text
P1 → P2 → P3
동일 Priority 내에서는:
문서 간 충돌 → 근거로 확인됨 → 판단 근거 부족 → 보완 제안
그다음 TC Section 순서 → Change ID 순서
```

---

## 14. Block 2-10. Review Queue Generation

### 14.1 목적

Reviewer가 TC 전체를 다시 읽기 전에 중요한 문제와 변경안을 한 건씩 검토할 수 있는 1차 핵심 산출물을 생성한다.

### 14.2 최종 표 형식

| Change ID | 우선순위 | TC 위치 | 발견 내용 | 변경 제안 | 제안 이유 | 상세 근거 | 근거 상태 | Reviewer 결정 |
|---|---|---|---|---|---|---|---|---|
| CHG-001 | P1 필수 확인 | C. P/F 2번 | Resolution OFF 기대 결과가 없음 | 미동작 판정 기준과 관측 Log를 추가 | 주파수별 ON/OFF 요구사항을 판정할 수 없음 | FR-11 v2.0 §3.2 p.14 / HLD v2.1 §6.2 p.28 | 근거로 확인됨 | 결정 대기 |
| CHG-002 | P2 주요 보완 | B. Procedure | Invalid 입력 검증이 없음 | Invalid·Empty·Out-of-range 입력과 오류 응답 확인 Step 추가 | 비정상 입력 처리 범위가 검증되지 않음 | Interface Spec v1.4 §4.3 p.19 / 동등분할 관점 | 보완 제안 | 결정 대기 |
| CHG-003 | P1 필수 확인 | A. Precondition | HLD와 DLD의 대상 Cell 조건이 다름 | 기준 문서 확인 후 해당 조건 확정 | AI가 임의로 기준을 선택할 수 없음 | HLD v2.1 §5.1 p.25 / DLD v2.0 §4.2 p.41 | 문서 간 충돌 | 결정 대기 |

### 14.3 상세 근거 표시 규칙

각 Proposal에는 표의 축약 Citation 외에 아래 상세 Citation을 연결한다.

```yaml
citations:
  - evidence_id: EVD-0001
    document_title: "COM Functional Requirement"
    version: "2.0"
    section: "3.2 Frequency-based Control"
    pages: "14-15"
    source_excerpt: "..."
    relevance: "Resolution OFF 기대 동작을 직접 정의"
```

### 14.4 Reviewer 입력 선택지

Phase 2 출력 시 모든 항목의 기본 상태는 `결정 대기`이다.

- 승인
- 거절
- 수정 후 승인
- 보류

Phase 2는 선택지를 제공하지만 결정을 대신 입력하지 않는다.

### 14.5 보조 출력

Review Queue 외에 시스템 처리를 위해 다음 파일을 함께 생성할 수 있다.

```text
- review_proposal.md      # 사람이 읽는 검토 제안서
- review_proposal.json    # Change ID와 상태를 저장하는 구조화 데이터
- validation_matrix.json  # Requirement/Scenario/Observation 매트릭스
```

발표와 1차 화면의 핵심은 `review_proposal.md`의 Review Queue이다.

---

## 15. Gate 2. Proposal Integrity Gate

### 15.1 목적

근거가 없거나 서로 다른 변경이 섞인 제안이 Reviewer에게 노출되지 않도록 검증한다.

### 15.2 Gate 검사 항목

| Gate ID | 검사 질문 | 실패 시 처리 |
|---|---|---|
| G2-01 | 모든 Proposal에 고유 Change ID가 있는가? | 재생성 |
| G2-02 | TC 위치와 발견 내용이 구체적인가? | Block 2-7/2-8 재수행 |
| G2-03 | 발견 내용과 변경 제안이 분리되어 있는가? | 재작성 |
| G2-04 | 한 Proposal에 하나의 독립 판단만 있는가? | Atomic Change로 분할 |
| G2-05 | 제안 이유와 미변경 영향이 설명되는가? | 보완 |
| G2-06 | 상세 근거가 문서·Version·Section·Page/Line까지 연결되는가? | 상태를 제한하거나 보완 |
| G2-07 | P1/P2/P3가 규칙 코드로 설명되는가? | 우선순위 재판정 |
| G2-08 | 한글 근거 상태가 실제 Evidence Grade와 일치하는가? | 상태 재판정 |
| G2-09 | 문서 충돌/근거 부족 항목이 확정 수정문처럼 표현되지 않았는가? | clarification_request로 변경 |
| G2-10 | Reviewer 승인 전 TC v1이 보존되었는가? | Gate Fail |
| G2-11 | 중복 Proposal이 제거되었는가? | Block 2-7 재수행 |
| G2-12 | 거절된 Evidence가 근거로 사용되지 않았는가? | Gate Fail |

### 15.3 Gate 결과

| 결과 | 의미 | 다음 동작 |
|---|---|---|
| READY_FOR_REVIEW | Reviewer에게 표시할 수 있음 | 검토 제안서 출력 |
| RETURN_FOR_REWORK | 일부 Proposal 형식·근거·원자성 문제 | 관련 Block 재수행 |
| BLOCKED | TC/Requirement를 잘못 바꿀 위험이 큼 | Reviewer에게 자료 요청 또는 제한 결과 출력 |

### 15.4 출력 Schema

```yaml
gate2_result:
  status: READY_FOR_REVIEW | RETURN_FOR_REWORK | BLOCKED
  failed_checks: [G2-06]
  affected_change_ids: [CHG-004]
  required_action: "Citation Page 확인 후 다시 생성"
```

---

## 16. Phase 2 의사코드

```text
function run_phase2(tc_v1, evidence_pack, gate1, review_rules):
    coverage = review_requirement_and_vp_coverage(tc_v1, evidence_pack)
    scope = review_scope_target_precondition(tc_v1, evidence_pack)
    procedure = review_procedure_executability(tc_v1, evidence_pack)
    oracle = review_observability_and_pass_fail(tc_v1, evidence_pack)
    scenarios = review_scenario_coverage(tc_v1, evidence_pack, review_rules)
    risk_consistency = review_history_and_consistency(tc_v1, evidence_pack)

    raw_gaps = collect(
        coverage, scope, procedure,
        oracle, scenarios, risk_consistency
    )

    normalized_gaps = normalize_and_deduplicate(raw_gaps)
    proposals = []

    for gap in normalized_gaps:
        proposal = create_atomic_change_proposal(gap)
        proposal.priority = assign_priority_by_rule(proposal)
        proposal.evidence_status = assign_evidence_status(proposal)
        proposals.append(proposal)

    review_queue = sort_and_render_review_queue(proposals)
    gate2 = evaluate_proposal_integrity(review_queue, tc_v1, evidence_pack)

    if gate2 == RETURN_FOR_REWORK:
        return_to_affected_blocks(gate2.affected_change_ids)

    return review_queue, gate2
```

---

## 17. Phase 2 완료 조건

Phase 2는 다음 조건을 모두 만족하면 완료된다.

- 모든 Core Review Block이 실행되었거나 미실행 사유가 기록되었다.
- 발견 후보가 Gap Record로 정규화되었다.
- 중복 Gap이 제거되고 연관 변경이 연결되었다.
- 각 Change ID가 하나의 독립 변경을 나타낸다.
- P1/P2/P3가 고정 규칙에 따라 부여되었다.
- 근거 상태가 한글로 표시되었다.
- 상세 Citation이 제안별로 연결되었다.
- Gate 2가 `READY_FOR_REVIEW`이다.
- TC v1은 변경되지 않았다.
- TC v2는 아직 생성되지 않았다.

