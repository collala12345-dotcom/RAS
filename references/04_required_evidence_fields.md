# 04. Quality Rubric

## Purpose

Defines the evaluation system for TC v1 quality assessment.
**Version 2.0** replaces point-based scoring with **checklist-based Pass/Fail/Partial evaluation**.

> **Note**: This rubric works with `references/03_tc_validation_checklist.md` — each checklist item is evaluated using this rubric's criteria.

---

## Evaluation Categories (8 개)

| # | Category | ID Range | Weight |
|---|----------|----------|--------|
| 1 | Requirement Coverage | RC-1 ~ RC-4 | 높음 |
| 2 | Scenario Completeness | SC-1 ~ SC-6 | 높음 |
| 3 | Procedure Clarity | PC-1 ~ PC-5 | 중간 |
| 4 | Pass/Fail Clarity | PF-1 ~ PF-4 | 높음 |
| 5 | Data/Configuration Consistency | DC-1 ~ DC-4 | 중간 |
| 6 | Evidence Traceability | ET-1 ~ ET-3 | 낮음 |
| 7 | Field Issue Awareness | FI-1 ~ FI-2 | 중간 |
| 8 | Cross-FR / Cross-rAPP Coverage | XC-1 ~ XC-4 | 높음 |

---

## Evaluation Criteria (상세 평가 기준)

### 1. Requirement Coverage (RC)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 모든 FR 이 TC 에 매핑되었고, 핵심 동작/조건이 모두 검증됨 |
| **⚠️ Partial** | 모든 FR 이 매핑되었으나 일부 조건/범위가 부분적으로만 검증됨 |
| **❌ Fail** | 1 개 이상 FR 이 TC 에서 전혀 다루어지지 않음 |

**Checklist Items:**
- RC-1: FR mapping
- RC-2: FR behavior verification
- RC-3: FR condition verification
- RC-4: FR scope verification

---

### 2. Scenario Completeness (SC)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | Positive + Negative + Boundary + Exception + Switch 조합 + Frequency 독립성 모두 포함 |
| **⚠️ Partial** | Positive 포함, 일부 Negative/Boundary 누락 또는 Switch 조합 일부만 검증 |
| **❌ Fail** | Positive 시나리오만 존재하거나, Negative/Boundary/Exception 전무 |

**Checklist Items:**
- SC-1: Positive scenario
- SC-2: Negative scenario
- SC-3: Boundary scenario
- SC-4: Exception scenario
- SC-5: Switch combination
- SC-6: Frequency independence

---

### 3. Procedure Clarity (PC)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 모든 단계가 구체적 API/파라미터 포함, 논리적 순서, 실제 수행 가능 |
| **⚠️ Partial** | 대부분 명확하나 일부 단계가 모호하거나 ("API 로 실행") 파라미터 누락 |
| **❌ Fail** | 많은 단계가 vague 하거나, 메시지 나열만 있거나, 수행 불가능 |

**Checklist Items:**
- PC-1: Step executability
- PC-2: API command specificity
- PC-3: Parameter completeness
- PC-4: Step ordering
- PC-5: Trigger clarity

---

### 4. Pass/Fail Clarity (PF)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | Pass/Fail 기준이 구체적 수치/상태/메시지로 명시, 자동화 가능, 모호성 없음 |
| **⚠️ Partial** | Pass 기준은 명시되었으나 일부 generic ("정상 동작"), Fail 기준은 암묵적 |
| **❌ Fail** | Pass 기준이 주관적 ("확인한다"), Fail 기준 없음 |

**Checklist Items:**
- PF-1: Measurability
- PF-2: Specificity
- PF-3: Fail criteria
- PF-4: Evidence-based

---

### 5. Data/Configuration Consistency (DC)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 모든 NE ID, 설정, 의존성이 일관되고 완전하며, CM/PM 요구사항 명시됨 |
| **⚠️ Partial** | 대부분 일관되나 사소한 설정/의존성 누락 있음 |
| **❌ Fail** | ID 불일치, 중요한 설정/의존성 누락 |

**Checklist Items:**
- DC-1: NE List consistency
- DC-2: Configuration completeness
- DC-3: Data collection
- DC-4: Dependency completeness

---

### 6. Evidence Traceability (ET)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 모든 TC 내용이 출처 문서에 인용되었고, line range 포함 |
| **⚠️ Partial** | 일부 인용 있으나 line range 누락 또는 불완전 |
| **❌ Fail** | 출처 인용 전무, 대부분 추적 불가능 |

**Checklist Items:**
- ET-1: Source citation
- ET-2: Line range
- ET-3: Modification justification

---

### 7. Field Issue Awareness (FI)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 알려진 과거 이슈가 TC 시나리오에 반영되었고, 위험 완화 시나리오 포함 |
| **⚠️ Partial** | 일부 인식되었으나 완전히 반영되지 않음 |
| **❌ Fail** | 과거 이슈 인식 전무 |

**Checklist Items:**
- FI-1: Historical issue reflection
- FI-2: Risk mitigation

---

### 8. Cross-FR / Cross-rAPP Coverage (XC)

| 평가 | 기준 |
|------|------|
| **✅ Pass** | 관련 FR(의존/충돌) 모두 식별, Multi-FR 시나리오 검토됨, 관련 rAPP 상호운용성 검토됨, Cross-rAPP 위험 식별됨 |
| **⚠️ Partial** | 일부 FR/rAPP 식별되었으나 완전히 검토되지 않음 |
| **❌ Fail** | 관련 FR/rAPP 식별 전무 |

**Checklist Items:**
- XC-1: Related FR identification
- XC-2: Multi-FR scenario review
- XC-3: Cross-rAPP interoperability
- XC-4: Cross-rAPP risk identification

---

## 종합 평가 (Overall Assessment)

### 항목별 집계

각 카테고리별로 Pass/Partial/Fail 개수를 집계:

| 항목 | Pass | Partial | Fail | 결과 |
|------|------|---------|------|------|
| Requirement Coverage | {count} | {count} | {count} | ✅ Pass / ⚠️ Partial / ❌ Fail |
| Scenario Completeness | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Procedure Clarity | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Pass/Fail Clarity | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Data/Config Consistency | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Evidence Traceability | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Field Issue Awareness | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |
| Cross-FR/rAPP Coverage | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |

### 카테고리 결과 판정

| 카테고리 결과 | 기준 |
|---------------|------|
| **✅ Pass** | 모든 체크 항목이 Pass, 또는 Partial 1 개 (경미) |
| **⚠️ Partial** | Partial 2 개 이상, 또는 Fail 1 개 |
| **❌ Fail** | Fail 2 개 이상 |

---

## 최종 판정 (Final Decision)

| 판정 | 기준 | Action |
|------|------|--------|
| ✅ **Approve** | 모든 카테고리 Pass, 또는 Partial 1-2 개 (경미) | 실무자 승인 권장 |
| ⚠️ **Revise** | Partial 3 개 이상, 또는 Fail 1 개 | 수정 후 재검토 |
| ❌ **Regenerate** | Fail 2 개 이상 | TC 재생성 필요 |

---

## Risk Level 상세 기준

### Low Risk (Approve)

- **Categories**: 7 개 이상 Pass, 나머지 Partial 1 개 이하
- **Critical Categories (RC, SC, PF)**: 모두 Pass
- **Human Review Required**: 0-1 개
- **Evidence Citation**: 5 개 이상

**Action:** 실무자는 High Risk 항목만 집중 검토

### Medium Risk (Revise)

- **Categories**: 4-6 개 Pass, 또는 Partial 2-4 개
- **Critical Categories (RC, SC, PF)**: 1 개 이상 Partial
- **Human Review Required**: 2-4 개
- **Evidence Citation**: 2-4 개

**Action:** AI 가 보완한 TC v2 를 검토 후 승인/수정

### High Risk (Regenerate)

- **Categories**: 3 개 이하 Pass, 또는 Fail 2 개 이상
- **Critical Categories (RC, SC, PF)**: 1 개 이상 Fail
- **Human Review Required**: 5 개 이상
- **Evidence Citation**: 0-1 개

**Action:** TC 재생성 필요, evidence 재검색

---

## Evaluation Example (COM rAPP 예시)

### Coverage Hole Detection TC 평가

#### 1. Requirement Coverage: ✅ Pass
```
RC-1: ✅ Pass - FR10.COA.SR1.11 전체 매핑
RC-2: ✅ Pass - Coverage Hole 탐지 로직 모두 검증
RC-3: ✅ Pass - CQI, BLER, Drop Rate 조건 명시
RC-4: ✅ Pass - Coverage Hole scope 정확히 매핑
→ 결과: 4 Pass → ✅ Pass
```

#### 2. Scenario Completeness: ⚠️ Partial
```
SC-1: ✅ Pass - Positive scenario 명확
SC-2: ✅ Pass - Negative scenario 포함 (v2 추가)
SC-3: ✅ Pass - Boundary scenario 포함 (v2 추가)
SC-4: ⚠️ Partial - Exception scenario 암묵적
SC-5: ⚠️ Partial - Switch 조합 2 개만 검증
SC-6: ✅ Pass - 과거 이슈 반영
→ 결과: 4 Pass, 2 Partial → ⚠️ Partial
```

#### 3. Pass/Fail Clarity: ✅ Pass
```
PF-1: ✅ Pass - 측정 가능한 기준
PF-2: ✅ Pass - 구체적 수치 명시 (CQI < 7, BLER > 10%)
PF-3: ✅ Pass - Fail 기준 명시
PF-4: ✅ Pass - FR/HLD 근거 있음
→ 결과: 4 Pass → ✅ Pass
```

#### 4. Cross-FR/rAPP Coverage: ⚠️ Partial
```
XC-1: ✅ Pass - FR10.COA.SR1.10 (Trade-off) 식별
XC-2: ⚠️ Partial - Multi-FR 시나리오 별도 TC 권장
XC-3: ⚠️ Partial - ESM/LBM 상호운용성 미반영
XC-4: ✅ Pass - Cross-rAPP 위험 3 개 식별
→ 결과: 2 Pass, 2 Partial → ⚠️ Partial
```

#### 종합 평가
```
| 항목 | 결과 |
|------|------|
| Requirement Coverage | ✅ Pass |
| Scenario Completeness | ⚠️ Partial |
| Procedure Clarity | ✅ Pass |
| Pass/Fail Clarity | ✅ Pass |
| Data/Config Consistency | ✅ Pass |
| Evidence Traceability | ⚠️ Partial |
| Field Issue Awareness | ✅ Pass |
| Cross-FR/rAPP Coverage | ⚠️ Partial |
| **총합** | **Pass 5, Partial 3** |
```

**최종 판정**: ⚠️ **Revise** (Partial 3 개)

**근거**: Scenario Completeness, Evidence Traceability, Cross-FR/rAPP Coverage 에서 Partial 발생.
실무자는 다음 항목을 중점 검토:
1. Switch 조합 검증 보완
2. ESM/LBM 상호운용성 TC 추가 검토
3. Line range 인용 보완

---

## Confidence Level 기반 평가 보정

AI 의 확신도 (confidence) 에 따라 평가 결과를 보정할 수 있습니다:

| Confidence | 보정 | Action |
|------------|------|--------|
| 0.8~1.0 | 없음 | 평가 신뢰함 |
| 0.6~0.79 | -1 단계 | Pass → Partial, Partial → Fail |
| 0.5~0.59 | -1 단계 + Human Review | Human Review Required 표시 |
| < 0.5 | -2 단계 + 재검색 | Human Review 필수, evidence 재검색 |

**보정 예시:**
```
원평가: Pass (4 Pass, 0 Partial)
Confidence: 0.55 (1 단계 감점 + Human Review)
보정 후: Partial → Human Review Required 항목 표시
```

---

## Reviewer Summary 작성 가이드

최종 Quality Report 의 마지막에 Reviewer Summary 를 작성합니다:

```markdown
## Reviewer Summary

### 📌 결론: Revise (Partial 3 개)

TC v1 대비 5 건 자동 보완됨. 실무자는 3 건만 확인하면 승인 가능.

### must Check (실무자가 반드시 확인해야 할 항목)

1. **Threshold 값**: RSRP < -120dBm, CQI < 3, Drop Rate > 3%
   - 현장 환경에 맞는 적절한 Threshold 값인지 확인 필요
   - 3GPP 28.554 참고

2. **PM 수집 주기**: 5 분 대기
   - 실제 PM 수집 주기가 5 분인지 확인 필요 (통신사별 상이)
   - HLD [COA-CSON0004] 참고

3. **Resolution 동작**: Tilt 조정, Power 조정
   - 실제 COM rAPP 이 어떤 Resolution 동작을 수행하는지 확인 필요
   - FR10.COA.SR1.12 참고

### Modified Section (AI 가 보완한 항목)

1. **Pass/Fail Criteria**: "정상 동작" → "Detection ON Cell 만 탐지" (evidence: FR10:12-18)
2. **Test Procedure**: Resolution OFF 시나리오 추가 (evidence: FR10:20-25)
3. **Precondition**: Analytic Server 연결 추가 (evidence: HLD:45-50)

### Remaining Risk (남은 위험 요소)

1. **Frequency independence**: f1/f2 cross-check 검증 부족 (Medium Risk)
2. **Optimization period**: period 만료 시 동작 검증 없음 (Low Risk)

### Recommendation

- **Approve**: High Risk 항목 없음, 실무자가 Must Check 3 개만 확인하면 승인 가능
- **Review Priority**: P0 (즉시 검토 권장)
```

---

**문서 업데이트**: 2026-07-16  
**버전**: 2.0 (체크리스트 기반 Pass/Fail/Partial 평가로 전환)

### 버전 2.0 변경 사항

| 변경 항목 | 버전 1.x | 버전 2.0 |
|-----------|----------|----------|
| 평가 방식 | 점수 (100 점 만점) | Pass/Fail/Partial |
| 카테고리 | 7 개 | 8 개 (Cross-FR/rAPP 추가) |
| 판정 기준 | 80-100=Approve | Pass 대부분=Approve |
| Risk Level | 점수 기반 | 카테고리 결과 기반 |
| Cross-FR/rAPP | 없음 | XC-1~XC-4 추가 |
