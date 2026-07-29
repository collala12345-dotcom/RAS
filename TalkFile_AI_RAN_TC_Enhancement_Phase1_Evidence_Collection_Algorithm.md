# AI-RAN TC Enhancement Phase 1 알고리즘 설계서

## Evidence Collection & Evidence Pack Generation

## 0. 문서 정보

| 항목 | 내용 |
|---|---|
| 문서 목적 | TC v1 검토에 필요한 근거를 수집·정규화·등급화하여 Evidence Pack을 생성하는 알고리즘 정의 |
| 적용 단계 | Phase 1. Evidence Collection |
| 입력 | Generated TC v1, 내부/외부 근거 문서 검색 DB, 실행 설정 |
| 출력 | Evidence Pack, Missing Evidence List, Conflict List, Gate 1 결과 |
| 다음 단계 | Phase 2. Structured Review & Change Proposal |
| 핵심 원칙 | Phase 1은 TC를 평가하거나 수정하지 않는다. 근거를 수집하고 사용 가능 상태로 정리한다. |

---

## 1. Phase 1의 역할

Phase 1은 TC v1의 내용을 읽고, Phase 2가 오류·누락·모호함을 판단할 때 사용할 근거를 준비하는 단계이다.

```text
TC v1 입력
→ TC 의도와 검증 대상 구조화
→ 문서 유형별 검색 Query 생성
→ FR/HLD/DLD/Algorithm/3GPP/Legacy TC/Issue 검색
→ 후보 근거의 관련성·출처·적용 범위 검증
→ Evidence Pack 생성
→ Gate 1 수행
```

이 단계에서는 다음 행동을 금지한다.

- TC v1 문장을 수정하지 않는다.
- 검색된 문장만으로 새로운 요구사항을 만들지 않는다.
- 다른 rAPP 또는 Legacy TC의 내용을 현재 TC의 필수 요구사항으로 단정하지 않는다.
- Page·Section·Version을 확인할 수 없는 근거를 확정 근거처럼 표시하지 않는다.
- 문서 간 충돌이 있을 때 AI가 임의로 우선 문서를 선택하지 않는다.

---

## 2. 전체 블록 구조

| 작업군 | Block | 이름 | 핵심 행동 | 주요 출력 |
|---|---|---|---|---|
| A. TC 이해 | 1-1 | TC Intake & Intent Understanding | TC 구조·의도·검색 단서 추출 | TC Metadata |
| B. 직접 근거 검색 | 1-2 | Requirement Matching | FR·Requirement 직접 매핑 | Requirement Evidence |
| B. 직접 근거 검색 | 1-3 | Design Behavior Retrieval | HLD·DLD·Interface 동작 검색 | Design Evidence |
| B. 직접 근거 검색 | 1-4 | Algorithm/KPI/Parameter Retrieval | 알고리즘·수치·데이터 조건 검색 | Algorithm/KPI Evidence |
| C. 보조·경험 근거 검색 | 1-5 | Standard/3GPP Retrieval | 표준 정의와 측정 개념 검색 | Standard Evidence |
| C. 보조·경험 근거 검색 | 1-6 | Legacy TC Retrieval | 기존 검증 패턴 검색 | Legacy TC Evidence |
| C. 보조·경험 근거 검색 | 1-7 | Issue/Bug/Test Result Retrieval | 과거 실패·상용 문제 검색 | Historical Risk Evidence |
| C. 보조·경험 근거 검색 | 1-8 | Cross-rAPP/Common Pattern Retrieval | 공통 검증 관점 탐색 | Common Pattern Evidence |
| D. 패키징 | 1-9 | Evidence Grading & Pack Generation | 중복 제거·등급화·충돌 표시 | Evidence Pack |
| Gate | Gate 1 | Evidence Readiness Gate | Phase 2 사용 가능성 판정 | READY / READY_WITH_GAPS / BLOCKED |

Phase 1의 블록은 기본적으로 순차 실행한다. 다만 1-5부터 1-8까지는 1-2~1-4의 핵심 검색 단서가 확보된 뒤 병렬 검색할 수 있다.

---

## 3. 공통 입출력 계약

### 3.1 필수 입력

```yaml
phase1_input:
  tc_v1_path: string
  tc_template_type: string | unknown
  target_release: string | unknown
  document_index_path: string
  allowed_doc_types:
    - requirement
    - hld_dld
    - interface
    - algorithm
    - kpi_parameter
    - standard_3gpp
    - legacy_tc
    - issue_bug
    - test_result
    - cross_rapp
  retrieval_config:
    top_k_per_query: integer
    max_query_variants: integer
    minimum_relevance_score: number
```

`target_release`가 입력되지 않은 경우 검색은 수행할 수 있지만, Release 일치 여부는 `unknown`으로 남긴다. Release가 다른 문서를 현재 설계 근거로 자동 채택해서는 안 된다.

### 3.2 공통 Evidence Record

모든 검색 결과는 최종적으로 아래 공통 구조로 정규화한다.

```yaml
evidence_id: EVD-0001
source_type: requirement | design | interface | algorithm | kpi_parameter | standard | legacy_tc | issue | test_result | cross_rapp
document_title: string
document_version: string | unknown
release_scope: string | unknown
source_path: string
section_title: string | unknown
section_number: string | unknown
page_start: integer | unknown
page_end: integer | unknown
line_start: integer | unknown
line_end: integer | unknown
source_excerpt: string
normalized_statement: string
related_requirement_ids: [string]
related_tc_locations: [string]
related_feature: string | unknown
applicability:
  target_rapp_match: true | false | unknown
  feature_match: true | false | unknown
  release_match: true | false | unknown
  scope_match: true | false | unknown
relevance_reason: string
evidence_grade: strong | supporting | weak | rejected | missing
allowed_usage:
  - validate_requirement
  - validate_design
  - validate_parameter
  - suggest_scenario
  - support_explanation
  - human_review_only
conflict_group_id: string | null
retrieval_query_id: string
retrieval_score: number | null
```

### 3.3 Citation 최소 요건

Reviewer에게 제시되는 근거는 가능한 경우 다음 순서를 모두 포함해야 한다.

```text
문서명 → 문서 버전 → Section 번호/제목 → Page 범위 → 관련 원문 또는 요약
```

문서가 Markdown처럼 Page 개념이 없는 경우에는 `Heading Path + Line 범위`를 사용한다. Page와 Line이 모두 없는 경우 출처는 불완전한 것으로 표시하며 `Strong Evidence`로 승격하지 않는다.

---

## 4. Block 1-1. TC Intake & Intent Understanding

### 4.1 목적

TC v1을 검색 가능한 구조로 변환하고, 이 TC가 무엇을 어떤 조건에서 어떤 결과로 검증하려는지 파악한다.

### 4.2 Input

- TC v1 원문
- 알려진 TC Template 구조
- 선택 입력: Target Release, rAPP 이름, FR ID

### 4.3 상세 수행 알고리즘

1. TC 문서의 Section을 식별한다.
   - Test Overview
   - Test Purpose
   - Dependency & Limitation
   - Related Feature
   - A. Precondition
   - B. Test Procedure
   - C. Pass/Fail Criteria
2. 문서에 없는 Section은 빈 값으로 생성하고 `missing_section`에 기록한다.
3. 제목·Purpose·Procedure·P/F에서 기능명과 동작 동사를 추출한다.
4. FR ID, API, Parameter, KPI, CM/PM, Switch, State, Frequency, NE/Cell, Log 키워드를 추출한다.
5. Procedure의 각 Step과 Expected Result를 분리한다.
6. TC의 검증 의도를 한 문장으로 정규화한다.
7. 명확히 알 수 없는 항목은 추측하지 않고 `unknown_or_ambiguous`에 기록한다.

### 4.4 추출 Schema

```yaml
tc_metadata:
  tc_id: string | unknown
  title: string
  target_rapp: string | unknown
  feature_name: string | unknown
  related_requirement_ids: [string]
  normalized_test_intent: string
  target_objects: [NE | cell | carrier | cluster | system | unknown]
  operations: [string]
  states_or_switches: [string]
  frequencies_or_carriers: [string]
  mentioned_apis: [string]
  mentioned_parameters: [string]
  mentioned_kpis: [string]
  mentioned_logs_or_outputs: [string]
  preconditions: [string]
  procedure_steps: [string]
  expected_results: [string]
  missing_sections: [string]
  unknown_or_ambiguous: [string]
```

### 4.5 판단 규칙

| 상태 | 조건 | 처리 |
|---|---|---|
| PASS | 기능 또는 FR, 검증 동작, 대상 중 최소 2개가 명확 | Block 1-2 진행 |
| PARTIAL | 목적은 파악되지만 FR·Scope·Expected Result 일부 불명확 | Fallback Query를 추가하고 진행 |
| FAIL | 기능과 검증 목적을 식별할 수 없음 | 제한 검색 후 Gate 1에서 BLOCKED 후보 |

### 4.6 Output

- `TC Metadata`
- `TC Location Map`
- `Initial Search Terms`
- `Ambiguity List`

### 4.7 COM 예시

```yaml
normalized_test_intent: "NE List 내 NR Cell을 대상으로 Carrier Frequency별 Overshooting Detection/Resolution ON/OFF 제어가 적용되는지 검증"
target_objects: [NE, cell, carrier]
states_or_switches: [detection_on_off, resolution_on_off]
mentioned_kpis: [Th_DMacTputOp]
unknown_or_ambiguous:
  - "API 명령의 정확한 endpoint와 parameter"
  - "결과 확인에 필요한 system log 위치"
```

---

## 5. Block 1-2. Requirement Matching

### 5.1 목적

TC v1과 직접 연결되는 FR·Requirement·Feature Description을 식별하여 검토 기준선을 만든다.

### 5.2 Query 생성 규칙

Query는 한 번에 긴 문장 하나만 만들지 않고 다음 계층으로 생성한다.

```text
Q1 Exact ID: FR ID 또는 Requirement ID
Q2 Feature + Operation: feature_name + 동작
Q3 Target + Condition + Behavior: 대상 + 조건 + 기대 동작
Q4 Synonym Fallback: 약어/정식명칭/과거 명칭 조합
```

### 5.3 상세 수행 알고리즘

1. Exact ID 검색을 최우선 수행한다.
2. 같은 ID의 여러 버전이 검색되면 Target Release 일치 문서를 우선 후보로 둔다.
3. FR 본문에서 조건, 대상, 입력, 기대 동작, 금지 동작을 분리한다.
4. Requirement가 여러 하위 동작을 포함하면 atomic requirement로 분해한다.
5. TC의 Purpose/Procedure/PF와 연결 가능한 Requirement만 유지한다.
6. Requirement ID가 없지만 의미가 유사한 경우 `candidate_requirement`로 표시한다.
7. 버전·Release·Scope가 다른 근거는 `weak` 또는 `human_review_only`로 제한한다.

### 5.4 Output Schema

```yaml
requirement_evidence:
  requirement_id: string
  atomic_requirement_id: string
  condition: string
  target: string
  required_behavior: string
  prohibited_behavior: string | null
  expected_output: string | null
  citation: EvidenceRecord
  match_type: exact_id | semantic_direct | semantic_candidate
```

### 5.5 판정 규칙

- 동일 FR ID·동일 Release·직접 문장이 확인되면 `Strong`.
- Feature는 같지만 Requirement 연결이 간접적이면 `Supporting`.
- 용어만 비슷하거나 Release가 다르면 `Weak`.
- 찾지 못하면 Missing Evidence를 생성한다.

### 5.6 예외 처리

- 서로 다른 FR 문서가 같은 ID에 다른 동작을 정의하면 `conflict_group_id`를 부여한다.
- Latest라는 이유만으로 최신 버전을 자동 채택하지 않는다. Target Release와 승인 기준 문서가 필요하다.

### 5.7 Output

- `Requirement Evidence List`
- `Atomic Requirement List`
- `Requirement Conflict List`
- `Missing Requirement Evidence`

---

## 6. Block 1-3. Design Behavior Retrieval

### 6.1 목적

FR이 요구한 기능이 시스템에서 실제로 어떤 Sequence·API·Input/Output·State로 동작하는지 검색한다.

### 6.2 검색 대상

- HLD, DLD
- Interface/API Specification
- Architecture 및 Sequence Diagram 설명
- Schema, Command Definition, Error Code 문서

### 6.3 상세 수행 알고리즘

1. Atomic Requirement별로 설계 검색 Query를 만든다.
2. 기능 동작을 `Trigger → Processing → Output → Observable Result` 구조로 추출한다.
3. API가 있으면 endpoint, method, request field, allowed value, response, error code를 각각 추출한다.
4. 상태 기반 동작이면 allowed transition과 prohibited transition을 추출한다.
5. 대상 필터가 있으면 포함 조건과 제외 조건을 분리한다.
6. Sequence Diagram은 주변 설명과 결합하여 사용하고, 그림 해석만으로 동작을 확정하지 않는다.
7. TC Step 또는 P/F와 연결 가능한 관측 결과를 표시한다.

### 6.4 Output Schema

```yaml
design_evidence:
  trigger: string
  pre_state: string | null
  input_condition: string
  processing_behavior: string
  output_condition: string
  post_state: string | null
  interface_or_api:
    name: string | null
    method: string | null
    endpoint: string | null
    request_fields: [string]
    response_fields: [string]
    error_codes: [string]
  observable_result: [string]
  exception_behavior: [string]
  citation: EvidenceRecord
```

### 6.5 판정 규칙

- 실행 Step과 Expected Result로 직접 변환 가능한 설계 근거는 `Strong`.
- 동작 개요만 있고 Parameter/API 상세가 없으면 `Supporting`.
- Architecture 개념만 관련되면 `Weak`.

### 6.6 Output

- `Design Behavior Map`
- `API/Interface Evidence`
- `Exception Behavior Evidence`
- `Design Gap List`

---

## 7. Block 1-4. Algorithm / KPI / Parameter Retrieval

### 7.1 목적

알고리즘 판단 조건, KPI 정의, Threshold, Parameter 범위, CM/PM 수집 조건을 확보하여 실행 가능성과 객관적 P/F 판단의 근거를 만든다.

### 7.2 상세 수행 알고리즘

1. TC 및 설계 근거에 등장한 KPI·Parameter·Threshold 이름을 정규화한다.
2. 각 항목의 정의, 단위, 허용 범위, Default, 적용 조건을 검색한다.
3. 알고리즘 식 또는 Decision Table에서 입력 변수와 출력 상태를 분리한다.
4. PM/CM 데이터는 source, aggregation period, collection period, missing-data 처리를 추출한다.
5. 동일 Parameter에 여러 값이 있으면 Release·환경·Scope를 비교한다.
6. TC에 수치가 없더라도 실험 환경에서 주입해야 할 `값의 영역`과 문서가 정의해야 할 `고정값`을 구분한다.

### 7.3 값 구체성 규칙

| 항목 | TC에 필요한 수준 |
|---|---|
| 문서가 고정한 Default/Threshold | 정확한 값과 단위, 출처 필요 |
| Lab마다 달라지는 Cell ID/IP/주파수 | 값 자체보다 입력 대상·허용 영역·선정 규칙 필요 |
| Boundary Test 값 | 경계 기준과 바로 아래/동일/바로 위 값 생성 규칙 필요 |
| API Enum/Switch | 허용값과 Invalid 값 규칙 필요 |
| 결과 Log/KPI | 관측 위치, 필드, 판정 조건 필요 |

### 7.4 Output Schema

```yaml
algorithm_kpi_parameter_evidence:
  item_name: string
  item_type: algorithm_condition | kpi | threshold | parameter | cm | pm
  definition: string
  value: string | number | null
  unit: string | null
  valid_range: string | null
  default_value: string | number | null
  application_condition: string
  collection_period: string | null
  missing_data_behavior: string | null
  observable_output: string | null
  citation: EvidenceRecord
```

### 7.5 Output

- `Algorithm Decision Evidence`
- `KPI/Threshold Table`
- `Parameter/API Value Table`
- `CM/PM Dependency Evidence`
- `Value Conflict List`

---

## 8. Block 1-5. Standard / 3GPP Reference Retrieval

### 8.1 목적

내부 설계에서 사용하는 용어·Measurement·Management Concept의 표준 정의를 확인하고 내부 근거를 보조한다.

### 8.2 사용 우선순위 규칙

```text
승인된 내부 Requirement
→ 동일 Release의 HLD/DLD/Interface/Algorithm
→ 승인된 내부 Test/Issue 자료
→ 3GPP/O-RAN 등 외부 표준
→ 다른 rAPP의 유사 패턴
```

표준은 내부 제품 동작을 직접 정의하지 않는 경우가 많으므로, 3GPP 근거만으로 내부 TC 변경을 확정하지 않는다.

### 8.3 상세 수행 알고리즘

1. 내부 문서에서 표준 번호 또는 표준 용어를 추출한다.
2. 관련 TS/TR의 정확한 Version·Section·Page를 검색한다.
3. 표준 문장이 정의하는 범위와 내부 구현 범위를 구분한다.
4. 내부 근거와 같은 의미인지, 상충하는지, 단순 참고인지 표시한다.
5. 직접 연결되지 않는 표준은 `support_explanation` 용도로 제한한다.

### 8.4 Output

- `Standard Evidence List`
- `Internal-to-Standard Link`
- `Standard Applicability Note`

---

## 9. Block 1-6. Existing / Legacy TC Retrieval

### 9.1 목적

동일 기능 또는 유사 제어 로직의 기존 TC에서 실무 검증 패턴과 누락 후보를 찾는다.

### 9.2 상세 수행 알고리즘

1. 동일 FR → 동일 Feature → 동일 Control Logic 순서로 검색 범위를 넓힌다.
2. 검색된 TC에서 Precondition, Procedure, Expected Result, P/F, Scenario를 분리한다.
3. 현재 TC와 다른 Release·환경·rAPP 조건을 기록한다.
4. 반복 등장하는 검증 항목을 `common_validation_pattern`으로 추출한다.
5. 현재 TC에 없는 항목은 곧바로 필수 누락으로 판정하지 않고 `missing_candidate`로만 생성한다.

### 9.3 판정 규칙

- 같은 FR·Feature·Release이면 Strong 후보가 될 수 있으나, Requirement 문서를 대체하지는 않는다.
- 다른 Release의 TC는 Regression 관점의 Supporting Evidence로 사용한다.
- 다른 rAPP TC는 제안 근거로만 사용한다.

### 9.4 Output

- `Legacy TC Evidence`
- `Reusable Validation Pattern`
- `Legacy-only Scenario Candidate`
- `Applicability Limitation`

---

## 10. Block 1-7. Historical Issue / Bug / Test Result Retrieval

### 10.1 목적

과거 Lab Fail, Field Issue, Commercial Issue, Bug, Regression Result에서 실제 실패 조건과 관측 결과를 찾아 Abnormal·Failure·Recovery 검토 근거를 만든다.

### 10.2 상세 수행 알고리즘

1. Feature, KPI, API, Parameter, Failure Symptom을 조합하여 검색한다.
2. Issue별 발생 환경, Trigger, Symptom, Root Cause, Fix, Verification Result를 추출한다.
3. 현재 Release에 Fix가 반영되었는지 확인한다.
4. 현재 TC가 해당 재현·회귀 조건을 포함하는지 Phase 2에서 비교할 수 있도록 구조화한다.
5. Issue 문서에 근거가 부족하면 Root Cause를 AI가 보충하지 않는다.

### 10.3 Output Schema

```yaml
historical_risk_evidence:
  issue_id: string
  issue_type: field | commercial | lab | regression | bug
  affected_release: string | unknown
  trigger_condition: string
  symptom: string
  root_cause: string | unknown
  fixed_behavior: string | unknown
  verification_method: string | unknown
  recommended_scenario_candidate: string
  citation: EvidenceRecord
```

### 10.4 우선순위 연결 규칙

- 안전성·상용 장애·Regression 재발과 직접 관련된 누락 후보는 Phase 2에서 P1 가능성을 평가한다.
- 일반적인 과거 실패 조건은 P2 후보이다.
- 현재 Release 적용 여부가 불명확하면 `문서 간 충돌` 또는 `판단 근거 부족` 상태로 넘긴다.

### 10.5 Output

- `Historical Risk Evidence`
- `Regression Scenario Candidate`
- `Release Applicability Gap`

---

## 11. Block 1-8. Cross-rAPP / Common Pattern Retrieval

### 11.1 목적

다른 rAPP 또는 공통 플랫폼 기능에서 재사용할 수 있는 검증 관점을 찾되, 현재 기능의 직접 요구사항과 분리한다.

### 11.2 상세 수행 알고리즘

1. 공통 제어 패턴을 기준으로 검색한다.
   - ON/OFF 조합
   - Frequency별 제어
   - NE/Cell Scope Filter
   - Empty/Invalid Input
   - Dependency Failure
   - State Transition 및 Recovery
2. 현재 TC와 구조적으로 같은 부분과 다른 부분을 명시한다.
3. 공통 패턴은 `suggest_scenario` 또는 `human_review_only`로 제한한다.
4. Domain 특화 Parameter·Threshold는 가져오지 않는다.

### 11.3 Output

- `Common Pattern Candidate`
- `Applicable Portion`
- `Non-applicable Limitation`

---

## 12. Block 1-9. Evidence Grading & Evidence Pack Generation

### 12.1 목적

모든 후보 근거를 중복 제거하고, Phase 2가 안전하게 사용할 수 있도록 관련성·출처 완전성·적용 가능성·충돌 여부를 부여한다.

### 12.2 Evidence 등급 규칙

| 등급 | 필수 조건 | 허용 용도 |
|---|---|---|
| Strong | 직접 관련 문장, Target Feature/Release/Scope 일치, 상세 Citation 존재 | 오류 확인, Requirement/Design/PF 검증 |
| Supporting | 관련성은 높으나 직접 요구 또는 적용 범위가 일부 부족 | 판단 보조, 이유 설명, Scenario 제안 |
| Weak | 간접 유사성, 버전 불일치, Citation 불완전 | 사람 확인 요청만 가능 |
| Rejected | 목적·Scope·Feature가 다름 | 사용 금지, 검색 로그에만 보존 |
| Missing | 필요한 문서 또는 항목을 찾지 못함 | 판단 근거 부족 표시 |

### 12.3 중복 제거 규칙

1. 동일 문서·동일 위치·동일 의미의 근거는 하나로 병합한다.
2. 같은 원문이 여러 Query에서 검색된 경우 Query ID는 모두 보존한다.
3. 같은 의미지만 문서 Version이 다르면 병합하지 않는다.
4. 상반된 문장은 삭제하지 않고 같은 `conflict_group_id`로 묶는다.

### 12.4 Evidence Pack Schema

```yaml
evidence_pack:
  pack_id: EPK-0001
  generated_at: datetime
  tc_metadata: object
  requirement_evidence: [EvidenceRecord]
  design_evidence: [EvidenceRecord]
  algorithm_kpi_parameter_evidence: [EvidenceRecord]
  standard_evidence: [EvidenceRecord]
  legacy_tc_evidence: [EvidenceRecord]
  historical_risk_evidence: [EvidenceRecord]
  common_pattern_evidence: [EvidenceRecord]
  conflict_groups:
    - conflict_group_id: CFG-0001
      evidence_ids: [EVD-0003, EVD-0011]
      conflict_summary: string
      required_human_question: string
  missing_evidence:
    - missing_id: MIS-0001
      required_for: string
      attempted_queries: [string]
      effect_on_phase2: string
  retrieval_audit:
    queries_executed: integer
    rejected_count: integer
```

### 12.5 Output

- `Evidence Pack`
- `Conflict List`
- `Missing Evidence List`
- `Retrieval Audit`

---

## 13. Gate 1. Evidence Readiness Gate

### 13.1 목적

검색이 끝났는지가 아니라, Phase 2의 판단이 가능한 상태인지 검사한다.

### 13.2 Gate 검사 항목

| Gate ID | 검사 질문 | 실패 시 처리 |
|---|---|---|
| G1-01 | TC 의도와 대상이 최소한 식별되었는가? | BLOCKED 후보 |
| G1-02 | 직접 관련 Requirement가 존재하는가? | READY_WITH_GAPS 또는 BLOCKED |
| G1-03 | Procedure/PF 검증에 필요한 설계 또는 동작 근거가 있는가? | 판단 근거 부족 표시 |
| G1-04 | KPI/Parameter/API가 언급된 경우 정의 근거가 있는가? | 해당 관점 자동 확정 금지 |
| G1-05 | Reviewer용 Citation이 문서·Version·Section·Page/Line까지 존재하는가? | Strong 승격 금지 |
| G1-06 | Release·Scope 일치 여부가 기록되었는가? | 적용 범위 불명확 표시 |
| G1-07 | 문서 간 충돌과 Missing Evidence가 숨겨지지 않았는가? | Gate Fail |
| G1-08 | Rejected Evidence가 Phase 2 사용 목록에서 제외되었는가? | Gate Fail |

### 13.3 Gate 결과

| 결과 | 조건 | 다음 동작 |
|---|---|---|
| READY | 핵심 근거와 Citation이 확보되고 치명적 충돌 없음 | Phase 2 전체 검토 수행 |
| READY_WITH_GAPS | 일부 근거 부족/충돌이 있으나 제한적 검토 가능 | Phase 2 수행, 해당 제안은 상태 제한 |
| BLOCKED | TC 의도 또는 핵심 Requirement를 식별할 수 없어 검토가 오판 가능 | 자동 변경 제안 제한, 사람에게 필요한 자료 요청 |

근거가 부족하다고 전체 Workflow를 무조건 중단하지는 않는다. 확인 가능한 관점은 계속 검토하되, 부족한 관점은 `판단 근거 부족`으로 명시한다.

### 13.4 Gate Output Schema

```yaml
gate1_result:
  status: READY | READY_WITH_GAPS | BLOCKED
  passed_checks: [G1-01]
  failed_checks: [G1-04]
  restrictions:
    - "API parameter 값 오류 여부 확정 금지"
  human_input_required:
    - "대상 Release의 Interface Spec 제공"
```

---

## 14. Phase 1 의사코드

```text
function run_phase1(tc_v1, document_index, config):
    metadata = parse_tc_and_extract_intent(tc_v1)

    requirement = retrieve_requirement(metadata, document_index)
    design = retrieve_design(metadata, requirement, document_index)
    algorithm = retrieve_algorithm_kpi_parameter(metadata, requirement, design)

    standard = retrieve_standard(metadata, requirement, design)
    legacy = retrieve_legacy_tc(metadata, requirement)
    history = retrieve_issue_and_test_result(metadata, requirement, design)
    common = retrieve_cross_rapp_patterns(metadata)

    candidates = concatenate(
        requirement, design, algorithm,
        standard, legacy, history, common
    )

    normalized = normalize_evidence(candidates)
    deduplicated = deduplicate_without_merging_versions(normalized)
    conflicts = detect_conflicts(deduplicated)
    graded = grade_evidence(deduplicated, metadata, config)
    missing = detect_missing_required_evidence(metadata, graded)

    pack = build_evidence_pack(metadata, graded, conflicts, missing)
    gate1 = evaluate_evidence_readiness(pack)

    return pack, gate1
```

---

## 15. Phase 1 완료 조건

Phase 1은 다음 조건을 모두 만족하면 완료된다.

- TC Metadata가 생성되었다.
- 모든 문서 유형에 대해 검색 수행 또는 검색 불가 사유가 기록되었다.
- Evidence마다 출처와 적용 범위가 기록되었다.
- 근거 등급과 허용 용도가 지정되었다.
- 문서 간 충돌과 Missing Evidence가 분리되었다.
- Gate 1 결과와 Phase 2 제한사항이 생성되었다.
- TC v1은 변경되지 않았다.

