# 05. Refinement Rules

## Purpose

Defines how TC v1 is refined into Enhanced TC v2. The goal is to improve quality while preserving the original test intent.

## Core Principles

1. **Preserve original test intent** — Do not change what the TC is trying to verify unless evidence demands it.
2. **Evidence-based refinement** — Every addition or modification must cite evidence or state `Evidence not found`.
3. **Prefer improvement over rewrite** — Modify sections in-place rather than rewriting the entire TC.
4. **No invention** — Never invent API names, NE IDs, threshold values, or KPI names. Use `Human Review Required` instead.
5. **Mark changes** — Every modification is recorded in the Change Log with before/after and reason.

## Refinement Targets

### 1. Missing Scenario Addition

When a required scenario type is missing:

| Missing Type | Refinement Action |
|---|---|
| Negative scenario | Add steps for the "should NOT happen" case (e.g., Detection OFF → no detection) |
| Boundary scenario | Add steps for edge values (e.g., minimum/maximum NE List size, threshold boundaries) |
| Exception scenario | Add steps for error conditions (e.g., invalid NE List, missing CM/PM data) |
| Switch combination | Add steps for each relevant ON/OFF combination |
| Frequency independence | Add steps verifying per-frequency independent behavior |

**Format for added scenario:**
```markdown
[Added Scenario: {type}]
- Reason: {why this scenario is needed, citing FR or evidence}
- Evidence: {source_path, line_range} or `Evidence not found`
- Steps: {new test steps}
- Expected: {expected result}
- Human Review Required: {Yes/No}
```

### 2. Pass/Fail Clarification

When pass/fail criteria are ambiguous:

| Issue | Refinement Action |
|---|---|
| "operate normally" | Replace with specific measurable criteria (e.g., "detection log shows only switch-ON cells as detected") |
| No Fail criteria | Add explicit Fail criteria (e.g., "If any switch-OFF cell is detected as overshooting → FAIL") |
| Subjective criteria | Replace with objective measurement (e.g., specific counter value, log entry, status code) |

**Rule**: If no evidence exists for what the specific measurement should be, use `Human Review Required` with a suggestion.

### 3. Procedure Enhancement

When procedure steps are vague:

| Issue | Refinement Action |
|---|---|
| Generic API reference | Add `Human Review Required` note: "Specific API endpoint needed from DLD. Suggested format: POST /com/v1/..." |
| Missing parameters | Add placeholder with `Human Review Required`: "Parameter values needed from Algorithm Design" |
| Message listing only | Rewrite as tester-triggered action: "Configure UE to {action} to trigger {message}" |
| Missing precondition | Add required precondition with evidence or `Evidence not found` |

### 4. Requirement Coverage Gap

When an FR is not fully covered:

| Issue | Refinement Action |
|---|---|
| FR behavior not tested | Add test steps targeting the untested behavior |
| FR condition not tested | Add test steps for the specific condition |
| FR scope not tested | Add or modify test scope to match FR definition |

### 5. Configuration Detail Addition

When configuration is incomplete:

| Issue | Refinement Action |
|---|---|
| Missing switch config | Add specific switch ON/OFF values per test case |
| Missing frequency config | Add carrier frequency values |
| Missing optimization period | Add period value (e.g., comResolutionPeriod = 1 week) |
| Missing CM/PM data spec | Add specific CM/PM data items to collect |

## Change Log Format

Every change is recorded as:

```markdown
| Section | Change Type | Before | After | Reason | Evidence |
|---|---|---|---|---|---|
| Pass/Fail Criteria | Modified | "COM app must operate normally" | "Only cells with Detection switch ON shall be detected as overshooting (verified via detection log)" | PF-2: Ambiguous pass criteria | FR10 definition in TC Section 4 |
| Test Procedure | Added | (none) | Step 4: Verify Resolution switch OFF → no resolution action | SC-2: Missing negative scenario | FR10: "control ON/OFF of Resolution" |
```

## What NOT to Change

- Do not remove existing test steps unless they are factually wrong (with evidence).
- Do not change TC ID or title.
- Do not change the overall TC structure (Overview, Purpose, Dependency, etc.).
- Do not add scenarios that contradict the FR definition.
- Do not fill in company-specific values without evidence.

---

## 시나리오별 자동 보완 규칙 (COM rAPP 예시)

### 1. Overshooting Detection TC 보완

**누락된 시나리오 탐지 시 자동 추가:**

| 누락 항목 | 자동 보완 내용 | Human Review 필요 조건 |
|---|---|---|
| TA far-distance | "TA histogram 에서 원거리 section (> 100km) 이 normal 대비 증가하는지 확인" 단계 추가 | 임계값 미명시 |
| DL MAC Throughput | "DL MAC Potential Throughput < Th_DMacTputOp" 검증 단계 추가 | Th_DMacTputOp 값 미명시 |
| Aggressor/Victim | "Aggressor Cell A, Victim Cell B 식별" 단계 추가 | Cell ID 미명시 |
| Severity 계산 | "Severity = Max Coverage Distance / Planned Coverage" 계산식 추가 | Planned Coverage 값 미명시 |

**보완 예시:**
```markdown
[Added Scenario: Overshooting Detection Verification]
- Reason: FR10 에서 "Overshooting Cell 은 TA far-distance 증가로 탐지" 명시
- Evidence: algorithm_docs/SVR26A_COM_overshooting_algorithm_design.docx:45-52
- Steps:
  1. Normal baseline 에서 TA histogram 수집
  2. Test 대상 Cell 에서 TA far-distance (> 100km) section 비율 확인
  3. TA far-distance 비율이 normal 대비 2 배 이상 증가했는지 확인
- Expected: TA far-distance ratio > 20%
- Human Review Required: No (evidence 기반)
```

### 2. Coverage Hole Detection TC 보완

**누락된 시나리오 탐지 시 자동 추가:**

| 누락 항목 | 자동 보완 내용 | Human Review 필요 조건 |
|---|---|---|
| Average CQI | "Avg CQI < 7" 검증 단계 추가 | 임계값 미명시 |
| DL/UL BLER | "DL BLER > 10%", "UL BLER > 10%" 검증 단계 추가 | 임계값 미명시 |
| Drop Rate | "Drop Rate > 2%" 검증 단계 추가 | 임계값 미명시 |
| RSRP Event A3 | "RSRP Event A3 bad counter > 100" 검증 단계 추가 | 임계값 미명시 |

**보완 예시:**
```markdown
[Added Scenario: Coverage Hole Detection Verification]
- Reason: FR11 에서 "Coverage Hole Cell 은 낮은 RF 상태로 Drop Rate 및 품질 KPI 저하" 명시
- Evidence: algorithm_docs/SVR26A_COM_overshooting_algorithm_design.docx:78-85
- Steps:
  1. Test 대상 Cell 에서 Average CQI, DL BLER, UL BLER, Drop Rate 수집
  2. 각 KPI 가 임계값 초과하는지 확인
- Expected: Avg CQI < 7, DL BLER > 10%, UL BLER > 10%, Drop Rate > 2%
- Human Review Required: No (evidence 기반)
```

### 3. Switch Control TC 보완

**4 가지 조합 자동 생성:**

| 조합 | 자동 보완 내용 |
|---|---|
| Detection ON + Resolution ON | "탐지 동작 + 해결 액션 생성" 검증 |
| Detection ON + Resolution OFF | "탐지만 동작, 액션 생성 안 함" 검증 |
| Detection OFF + Resolution ON | "탐지 안 함, 액션도 생성 안 함" 검증 |
| Detection OFF + Resolution OFF | "무반응" 검증 |

**보완 예시:**
```markdown
[Added Scenario: Switch Combination Matrix]
- Reason: FR10 에서 "Detection/Resolution Switch ON/OFF 독립 제어" 명시
- Evidence: feature_specs/FR10_COM_overshooting.md:12-18
- Steps:
  1. Detection=ON, Resolution=ON 설정 → 탐지 및 액션 확인
  2. Detection=ON, Resolution=OFF 설정 → 탐지만 확인
  3. Detection=OFF, Resolution=ON 설정 → 무반응 확인
  4. Detection=OFF, Resolution=OFF 설정 → 무반응 확인
- Expected: 표의 예상 동작과 일치
- Human Review Required: No
```

### 4. Frequency Independence TC 보완

**2x2 조합 자동 생성:**

| f1 | f2 | 자동 보완 내용 |
|---|---|---|
| ON | ON | "f1, f2 모두 탐지/해결" 검증 |
| ON | OFF | "f1 만 탐지/해결, f2 무반응" 검증 |
| OFF | ON | "f1 무반응, f2 만 탐지/해결" 검증 |
| OFF | OFF | "모두 무반응" 검증 |

**보완 예시:**
```markdown
[Added Scenario: Frequency Independence Verification]
- Reason: FR10 에서 "주파수별로 Detection/Resolution 독립 제어" 명시
- Evidence: feature_specs/FR10_COM_overshooting.md:20-25
- Steps:
  1. f1=2100MHz: Detection=ON, f2=1800MHz: Detection=OFF 설정
  2. f1 Cell 만 탐지되고 f2 Cell 은 탐지 안 되는지 확인
  3. f1=OFF, f2=ON 으로 설정하여 역방향 검증
- Expected: f1 설정이 f2 에 영향 주지 않음
- Human Review Required: No
```

### 5. NE List Scope TC 보완

**자동 보완 내용:**

| 누락 항목 | 자동 보완 내용 |
|---|---|
| NE List 명시 | "NE List: [81000, 81001, 81002]" 구체화 요청 (Human Review) |
| Indoor 제외 | "cell_type != 'indoor'인 Cell 만 대상" 조건 추가 |
| Scope 검증 | "NE List 밖 Cell 은 결과에 포함 안 됨" 검증 단계 추가 |

---

## Pass/Fail Criteria 구체화 규칙

### 1. 수치 기반 기준

**변환 전:**
```
"COM app 이 정상적으로 동작해야 함"
```

**변환 후:**
```
"Detection Switch ON 인 Cell 만 detection log 에 포함되어야 함"
```

**근거:** FR10 에서 "Detection Switch ON 인 Cell 만 탐지" 명시

### 2. 임계값 기반 기준

**변환 전:**
```
"Throughput 가 감소해야 함"
```

**변환 후:**
```
"DL MAC Potential Throughput < Th_DMacTputOp"
```

**근거:** 알고리즘 설계서에서 Th_DMacTputOp 임계값 명시

### 3. 조합 기반 기준

**변환 전:**
```
"Switch 설정에 따라 동작해야 함"
```

**변환 후:**
```
"Detection=ON, Resolution=ON → 탐지 및 액션 생성
Detection=ON, Resolution=OFF → 탐지만, 액션 없음
Detection=OFF, Resolution=ON → 무반응
Detection=OFF, Resolution=OFF → 무반응"
```

**근거:** FR10 에서 Switch 독립 제어 명시

---

## Procedure 구체화 규칙

### 1. API 명령 구체화

**변환 전:**
```
"API 로 설정한다"
```

**변환 후:**
```
"POST /com/v1/detection/config 에 다음 payload 전송:
{
  "ne_id": "81000",
  "detection_switch": "ON",
  "resolution_switch": "ON"
}"

[Human Review Required: API endpoint 는 DLD 에서 확인 필요]
```

### 2. 파라미터 구체화

**변환 전:**
```
"적절한 값으로 설정한다"
```

**변환 후:**
```
"NE List: [81000, 81001, 81002] (Type 1: CM/PM 관리)
Frequency: f1=2100MHz, f2=1800MHz
Optimization Period: 30 분

[Human Review Required: NE ID 와 주파수는 실제 환경에서 확인 필요]
```

### 3. 검증 단계 구체화

**변환 전:**
```
"결과를 확인한다"
```

**변환 후:**
```
"detection log 에서 다음 확인:
- Cell 81000 (Detection=ON): 탐지됨 ✓
- Cell 81001 (Detection=ON): 탐지됨 ✓
- Cell 81002 (Detection=OFF): 탐지 안 됨 ✓
```

---

## Human Review Required 판정 가이드

### 핵심 원칙: AI 가 먼저 확인하고, 진짜 불확실한 것만 Human Review

> ⚠️ **중요**: Human Review Required 는 "AI 가 떠넘기기"가 아닙니다.  
> AI 가 먼저 Evidence 를 확인해서 확신 있는 것은 자동 보완하고,  
> **진짜 불확실한 것만** Human Review 로 표시합니다.

### Evidence Confidence 기반 자동 판단

| Evidence Score | Grade | AI Action | Human Review |
|---|---|---|---|
| `score > 5.0` | **Strong** | 자동 보완 | ❌ 필요 없음 |
| `3.0 < score <= 5.0` | **Supporting** | 자동 보완 | ❌ 필요 없음 |
| `score <= 3.0` | **Weak** | 보완하되 표시 | ⚠️ 확인 필요 |
| `evidence 없음` | **Missing** | 보완 안 함 | ✅ 필수 확인 |

### 자동 Human Review Required 표시 조건

| 조건 | 예시 | Action |
|---|---|---|
| `confidence < 0.5` | evidence 신뢰도 낮음 | "Human Review Required: evidence 신뢰도 낮음" 표시 |
| 임계값 미명시 | Th_DMacTputOp 값 없음 | "Human Review Required: 알고리즘 설계서에서 임계값 확인 필요" |
| Cell ID 미명시 | "해당 Cell" (모호) | "Human Review Required: 실제 Cell ID 확인 필요" |
| API endpoint 미명시 | "API 로 호출" | "Human Review Required: DLD 에서 API endpoint 확인 필요" |
| evidence 미발견 | 검색 결과 0 개 | "Human Review Required: evidence 검색 필요" |
| **상충되는 evidence** | FR vs HLD 상충 | "Human Review Required: 문서 간 상충" 표시 |

### Human Review Required 필터링 규칙

1. **Top 3 원칙**: 최대 3 개만 표시 (너무 많으면 집중 불가)
2. **증거 없음 우선**: Evidence 가 없는 항목을 최우선으로 표시
3. **High Risk 우선**: High/Critical severity 항목을 우선으로 표시

### Human Review Required 작성 형식

```markdown
[Human Review Required]
- 항목: {어떤 부분이 확인 필요한지}
- 이유: {왜 확인이 필요한지}
- 제안: {AI 가 제안하는 내용 - optional}
- 확인 필요 문서: {어디서 확인해야 하는지}
```

**예시:**
```markdown
[Human Review Required]
- 항목: Th_DMacTputOp 임계값
- 이유: algorithm_docs 에서 해당 임계값을 찾을 수 없음
- 제안: FR10 또는 알고리즘 설계서 3 장 참조 필요
- 확인 필요 문서: SVR26A_COM_overshooting_algorithm_design.docx
```

---

## Before/After 비교 형식

TC v1 과 TC v2 의 차이를 명확히 보여줍니다:

```markdown
## Change Log

| Section | Change Type | Before | After | Reason |
|---|---|---|---|---|
| Pass/Fail Criteria | Modified | "COM app 이 정상 동작" | "Detection Switch ON 인 Cell 만 탐지됨" | PF-2: Ambiguous pass criteria |
| Test Procedure | Added | (none) | Step 4: Resolution OFF 시 액션 없음 확인 | SC-2: Missing negative scenario |
| Precondition | Added | (none) | "Analytic Server 연결 필요" | DC-4: Missing dependency |
```

---

**문서 업데이트**: 2026-07-10  
**버전**: 1.1 (자동 보완 규칙 구체화)
