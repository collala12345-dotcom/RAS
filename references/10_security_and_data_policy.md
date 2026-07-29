# TC Review Gotchas

> Common mistakes and important notes for TC Review/Enhancement operations.

---

## 핵심 원칙 (절대 위반 금지)

1. **근거 없이 TC 를 수정하지 않는다**: 항상 evidence citation(문서명, 줄 범위) 을 포함한다.
2. **confidence < 0.5**: 자동 Human Review Required 표시. AI 가 확신 없는 판단은 사람에게 넘긴다.
3. **Source 와 Extraction 을 분리한다**: 먼저 전체 evidence 를 검색한 후, TC 관련 항목만 필터링한다.
4. **TC 는 파생 산출물이다**: TC 가 FR/HLD/DLD 의 요구사항을 검증하는 도구임을 잊지 않는다.
5. **빈 증거로 판단하지 않는다**: "Evidence not found"는 "증거 없음"이 아닌 "검색 전략 재검토 필요"다.

---

## RAG 검색 시 주의사항

### 1. Evidence 현황을 정확히 파악한다

| doc_type | JSONL Available? | Notes |
|---|---|---|
| `3gpp_docs` | ✅ Yes | 170 개 파일, 9,642 chunks |
| `algorithm_docs` | ✅ Yes | 3 개 파일, 244 chunks |
| `hld_dld` | ✅ Yes | 2 개 파일, 86 chunks |
| `legacy_tc` | ✅ Yes | 81 개 파일, 571 chunks |
| `feature_specs` | ⚠️ Partial | 일부 파일 존재, 변환 필요 |
| `issue_cases` | ⚠️ Partial | 일부 파일 존재, 변환 필요 |
| `test_results` | ⚠️ Partial | 일부 파일 존재, 변환 필요 |
| `review_comments` | ❌ No | 아직 미처리 |
| `pegs` | ❌ No | Raw data 존재 but 포맷 정리 필요 |

### 2. Metadata 필터를 적극 활용한다

```python
# 예시: COM Overshooting 관련 증거 검색
collection.query(
    query_embeddings=embedding,
    where={
        "feature_area": {"$in": ["Overshooting", "Coverage Hole"]},
        "related_rapp": "COM",
        "priority": {"$in": ["P0", "P1"]},
        "confidence": {"$gte": 0.5}
    },
    n_results=10
)
```

**새 Metadata 필드 활용:**
- `feature_area`: "Overshooting", "Coverage Hole", "Mobility" 등 기능 영역 필터
- `related_rapp`: "COM", "SON", "Energy Saving" 등 rAPP 필터
- `priority`: P0/P1/P2/P3 우선순위 필터
- `confidence`: 신뢰도 기반 evidence 품질 필터 (0.0-1.0)
- `human_review_required`: 사람 확인 필요 증거 식별
- `evidence_scope`: "algorithm", "requirement", "standard" 등 용도별 필터
- `review_role`: "Use this chunk to verify..." 활용 방법

### 3. 검색 결과 Overlap 처리

- 동일 내용이 여러 문서에 있을 경우 **우선순위 높은 문서 1 개**만 인용
- `priority` 필드 기반 정렬: P0 > P1 > P2 > P3
- `confidence` 필드 기반 필터링: 0.5 미만은 Human Review 로 넘김

---

## TC 검증 시 주의사항

### 1. Requirement Coverage

- ✅ FR 의 각 requirement 가 TC 에 반영되었는지 확인
- ⚠️ "FR 을 참조한다"는 막연한 표현은 부족함. **구체적인 requirement ID** 명시
- ❌ FR 과 TC 의 behavior 가 다르면 Warning

### 2. Scenario Completeness

| Scenario Type | 검증 항목 | COM 예시 |
|---|---|---|
| Positive | 정상 동작 | Detection/Resolution Switch ON 시 정상 탐지/해결 |
| Negative | 비정상 동작 | Switch OFF 시 동작 안 함 |
| Boundary | 경계 조건 | Threshold 경계값 (예: Th_DMacTputOp ±1) |
| Exception | 예외 처리 | Analytic Server 연결 끊김 |

### 3. Pass/Fail Clarity

- ✅ 측정 가능한 수치 명시 (예: "PRB usage ≥ 90%")
- ⚠️ "정상 동작해야 함"은 모호함. **어떤 값으로 판단하는지** 명시
- ❌ "확인한다"만 있고 기준이 없으면 Fail

### 4. Procedure Completeness

- ✅ 단계별 실행 가능한 명령/설정 명시
- ⚠️ "적절한 설정을 한다"는 모호함. **구체적인 값** 명시
- ❌ 순서가 뒤죽박죽이면 Fail

---

## COM rAPP 특화 주의사항

### 1. NE List Scope Verification (CP-1)

- ✅ NE List 에 포함된 cell 만 대상인지 검증
- ⚠️ Indoor cell 제외 조건이 반영되었는지 확인
- ❌ 모든 cell 을 대상으로 하면 Fail

### 2. Carrier Frequency Independence (CP-2)

- ✅ 주파수별 Detection/Resolution 이 독립적으로 적용되는지 검증
- ⚠️ f1=ON, f2=OFF 조합이 올바르게 처리되는지 확인
- ❌ 주파수 간 상호영향 있으면 Fail

### 3. Detection/Resolution Switch Control (CP-3, CP-4)

| Switch | ON | OFF |
|---|---|---|
| Detection | 탐지 동작 | 탐지 안 함 |
| Resolution | 해결 동작 | 해결 안 함 |

- ✅ 4 가지 조합 (ON-ON, ON-OFF, OFF-ON, OFF-OFF) 모두 검증
- ⚠️ Switch 상태와 실제 동작이 일치하는지 확인

### 4. Optimization Period (CP-5)

- ✅ cluster 별로 최적화 주기가 설정되는지 검증
- ⚠️ 주기 시간 (예: 15 분, 30 분) 이 Pass/Fail Criteria 에 명시되었는지 확인

### 5. CM/PM Data Collection (CP-6)

- ✅ comResolutionPeriod 동안 statistics item 이 수집되는지 검증
- ⚠️ CM/PM 데이터 수집 조건이 precondition 에 포함되었는지 확인

### 6. Analytic Server Dependency (CP-7)

- ✅ Analytic Server 연결이 전제조건으로 명시되었는지 확인
- ⚠️ 서버 연결 끊김 시나리오가 있는지 확인

### 7. Optional Data (CP-8)

- ✅ Azimuth, Cell-RET mapping 등 optional dataが必要な場合 반영되었는지 확인
- ⚠️ optional data 가 없을 때 fallback 동작이 있는지 확인

### 8. Threshold/KPI (CP-9)

- ✅ Th_DMacTputOp 등 threshold 기반 KPI 조건이 명확히 검증되는지 확인
- ⚠️ threshold 값이 Pass/Fail Criteria 에 구체적으로 명시되었는지 확인

---

## Human Review Required 판정 기준

| 기준 | 값 | Action |
|---|---|---|
| `confidence` | < 0.5 | 자동 Human Review Required 표시 |
| `feature_area` | "Unknown" | 기능 영역 불명확 |
| `related_function` | "Unknown" | 세부 기능 불명확 |
| doc_type 과 내용 불일치 | 3GPP 문서에 "algorithm" 키워드 | 오해 가능성 |
| PPT/그림 추출 | `source_format` 에 "ppt" 포함 | 텍스트 누락 가능성 |
| Table 내용 | `heading_path` 에 "table" 포함 | header 불명확 |

---

## 코드 수정 시 체크리스트

1. **근거 citation 포함**: 수정 이유와 근거 문서 (문서명, 줄 범위) 를 함께 남긴다.
2. **Before/After 비교**: TC v1 과 TC v2 의 차이를 명확히 보여준다.
3. **Human Review 명시**: 불확실한 부분은 "Human Review Required"로 표시한다.
4. **RAG 검색 결과 연결**: 검색된 과거 사례가 어떤 scenario 로 반영되었는지 보여준다.
5. **우선순위 반영**: P0 evidence 를 반드시 검색 결과에 포함한다.

---

## 자주 하는 실수

| 실수 | 원인 | 해결 |
|---|---|---|
| "Evidence not found" | 검색어만 믿고 필터링 안 함 | metadata 필터 적극 활용 |
| 모호한 Pass/Fail | "정상 동작" 등 추상적 표현 | 구체적 수치 명시 |
| Procedure 순서 오류 | 의존성 고려 안 함 | precondition → action → verification 순서 |
| NE ID 하드코딩 | 특정 환경만 검증 | 변수화 또는 범위 명시 |
| Switch 조합 누락 | 2 개 변수 간 독립 검증 안 함 | 2x2 조합 매트릭스 작성 |

---

## 참고 문서

- `references/01_retrieval_rules.md` - Evidence 검색 전략
- `references/03_tc_validation_checklist.md` - 30+ 개 검증 항목
- `references/04_quality_rubric.md` - 7 차원 100 점 평가
- `references/07_com_domain_rules.md` - COM 전용 9 개 규칙

---

**문서 업데이트**: 2026-07-10  
**버전**: 1.1 (SynthRAN 체크리스트 형식 차용)
