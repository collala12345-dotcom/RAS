# 03. TC Validation Checklist

## Purpose

Defines the validation checks applied to TC v1 during review. Each check produces a finding: Pass, Warning, or Issue.

> 이 체크리스트는 ISTQB CTFL 파운데이션 레벨 실러버스 v4.0.1 을 기반으로 확장되었습니다.

## Validation Categories

### 1. Requirement Coverage (RC)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| RC-1 | FR mapping | Is every FR listed in Related Feature covered by at least one TC step? | All FRs mapped | Some FRs partially mapped | FR not addressed at all |
| RC-2 | FR behavior verification | Does the TC verify the core behavior defined in each FR? | All behaviors verified | Some behaviors implicit | Core behavior not tested |
| RC-3 | FR condition verification | Does the TC verify conditions/constraints mentioned in FR? | All conditions tested | Some conditions missing | Critical condition ignored |
| RC-4 | FR scope verification | Does the TC operate within the scope defined by FR? | Scope matches | Scope partially matches | Scope mismatch |

### 2. Scenario Completeness (SC)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| SC-1 | Positive scenario | Is the normal/expected flow tested? | Yes, clearly | Yes but vague | Missing |
| SC-2 | Negative scenario | Is the failure/rejection path tested? | Yes, clearly | Partially | Missing |
| SC-3 | Boundary scenario | Are edge/boundary conditions tested? | Yes, clearly | Partially | Missing |
| SC-4 | Exception scenario | Are exception/error conditions tested? | Yes, clearly | Partially | Missing |
| SC-5 | Switch combination | Are all relevant ON/OFF switch combinations tested? | All combinations | Some combinations | Only single state |
| SC-6 | Frequency independence | If FR requires per-frequency control, are independent frequency behaviors tested? | Yes, explicitly | Partially | Missing |

### 3. Procedure Clarity (PC)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| PC-1 | Step executability | Are test steps executable by a real tester/UE? | All executable | Some ambiguous | Not executable |
| PC-2 | API command specificity | Are API commands specific (not "run with API command")? | Specific commands | Generic reference | No API specified |
| PC-3 | Parameter completeness | Are required parameters specified with values? | All parameters | Some missing | Critical params missing |
| PC-4 | Step ordering | Is the step order logical and correct? | Correct order | Minor issues | Wrong order |
| PC-5 | Trigger clarity | Does each step explain how to trigger the action (not just list system messages)? | Clear triggers | Some unclear | Just message listing |

### 4. Pass/Fail Clarity (PF)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| PF-1 | Measurability | Can Pass/Fail be objectively measured? | Measurable | Partially measurable | Subjective/ambiguous |
| PF-2 | Specificity | Are specific values/states/messages defined for Pass? | Specific values | Some generic | "operate normally" |
| PF-3 | Fail criteria | Is Fail criteria explicitly stated? | Explicit | Implicit | Missing |
| PF-4 | Evidence-based | Are Pass/Fail criteria backed by FR/HLD/DLD evidence? | Evidence-backed | Partially | No evidence |

### 5. Data/Configuration Consistency (DC)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| DC-1 | NE List consistency | Are NE IDs, Cell IDs consistent throughout TC? | Consistent | Minor mismatch | Inconsistent |
| DC-2 | Configuration completeness | Are all required configs (switch, frequency, period) specified? | All specified | Some missing | Critical configs missing |
| DC-3 | Data collection | Are CM/PM data collection requirements in precondition? | Yes | Partially | Missing |
| DC-4 | Dependency completeness | Are all required NEs/servers/interfaces listed in Dependency? | All listed | Some missing | Critical dependency missing |

### 6. Evidence Traceability (ET)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| ET-1 | Source citation | Does TC cite source documents for its content? | Cited | Partially | No citations |
| ET-2 | Line range | Are source line ranges available for verification? | Available | Partially | None |
| ET-3 | Modification justification | Are any deviations from FR/HLD justified? | Justified | Partially | Unjustified |

### 7. Field Issue Awareness (FI)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| FI-1 | Historical issue reflection | Are known past issues reflected in TC scenarios? | Reflected | Partially | Not reflected |
| FI-2 | Risk mitigation | Does TC include scenarios to prevent known failure modes? | Yes | Partially | No |

### 8. Cross-FR / Cross-rAPP Coverage (XC)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| XC-1 | Related FR identification | Are related FRs (dependency/conflict/trade-off) identified? | All identified | Some identified | None identified |
| XC-2 | Multi-FR scenario review | Are multi-FR composite scenarios (simultaneous/sequential) considered? | Reviewed | Partially | Not reviewed |
| XC-3 | Cross-rAPP interoperability | Are interactions with other rAPPs (ESM, LBM, etc.) reviewed? | All reviewed | Partially | Not reviewed |
| XC-4 | Cross-rAPP risk identification | Are cross-rAPP risks (conflicts, infinite loops, data corruption) identified? | All identified | Some identified | None identified |

### 8. Test Level Validation (TL) - ISTQB 기반

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| TL-1 | Test level identification | Is the appropriate test level (component/integration/system) identified? | Clearly identified | Implicit | Not identified |
| TL-2 | Component test | Are individual component functions tested? | Yes | Partially | No |
| TL-3 | Integration test | Are interfaces between components tested? | All interfaces | Some interfaces | No integration test |
| TL-4 | System test | Are end-to-end system behaviors tested? | Yes | Partially | No |
| TL-5 | System integration test | Are external system interfaces tested (other rAPPs)? | All interfaces | Some interfaces | No SIT |

### 9. Test Type Validation (TT) - ISTQB 기반

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| TT-1 | Functional testing | Are functional requirements verified? | All functions | Some functions | Missing |
| TT-2 | Non-functional testing | Are KPI/performance/reliability requirements tested? | All NFRs | Some NFRs | Missing |
| TT-3 | Black-box testing | Are input/output behaviors tested without internal knowledge? | Yes | Partially | No |
| TT-4 | White-box testing | Are internal logic/code paths considered? | Yes | Partially | No |

### 10. Test Technique Validation (TE) - ISTQB 기반

#### 10.1 Black-Box Techniques

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| TE-BB-1 | Equivalence Partitioning | Are valid/invalid partitions tested with representative values? | Yes | Partially | No |
| TE-BB-2 | Boundary Value Analysis | Are boundary values (min/max/edge) tested? | All boundaries | Some boundaries | No BVA |
| TE-BB-3 | Decision Table | Are condition combinations tested systematically? | All combinations | Some combinations | No decision table |
| TE-BB-4 | State Transition | Are state changes and transitions tested? | All transitions | Some transitions | No state test |

#### 10.2 White-Box Techniques

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| TE-WB-1 | Statement coverage | Are all executable statements covered? | 100% | >80% | <80% |
| TE-WB-2 | Branch coverage | Are all true/false branches tested? | 100% | >80% | <80% |

#### 10.3 Experience-Based Techniques

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| TE-EB-1 | Error guessing | Are past error patterns used for test design? | Yes | Partially | No |
| TE-EB-2 | Exploratory testing | Are unexplored areas identified for testing? | Yes | Partially | No |
| TE-EB-3 | Checklist-based | Are standard checklists applied? | Yes | Partially | No |

### 11. Static Testing Validation (ST) - TC 자체 품질

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| ST-1 | Clarity | Are ambiguous expressions avoided ("적절한", "충분한")? | Clear | Some ambiguity | Many ambiguous |
| ST-2 | Completeness | Are all required TC elements present (10.1 in persona)? | Complete | Minor missing | Major missing |
| ST-3 | Consistency | Are terminology and format consistent? | Consistent | Minor issues | Inconsistent |
| ST-4 | Traceability | Is FR ID explicitly linked? | All linked | Some linked | No links |

### 12. Risk-Based Testing Validation (RB) - ISTQB 기반

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| RB-1 | Product risk identification | Are product risks (function loss, performance degradation) identified? | All risks | Some risks | No risk analysis |
| RB-2 | Project risk consideration | Are project risks (schedule, resources) considered in test priority? | Yes | Partially | No |
| RB-3 | Risk-based priority | Are high-risk items tested with higher priority? | Yes | Partially | No |
| RB-4 | Risk mitigation scenarios | Are scenarios designed to mitigate identified risks? | Yes | Partially | No |

### 13. Pass/Fail Criteria SMART Validation (PF-SMART)

| # | Check | Question | Pass | Warning | Issue |
|---|---|---|---|---|---|
| PF-SMART-1 | Specific | Are criteria specific (not "check KPI" but "KPI > 95%")? | Specific | Some generic | Vague |
| PF-SMART-2 | Measurable | Can criteria be objectively measured (numeric/boolean)? | Measurable | Partially | Subjective |
| PF-SMART-3 | Achievable | Are criteria realistically achievable? | Yes | Some aggressive | Unrealistic |
| PF-SMART-4 | Relevant | Are criteria directly linked to FR requirements? | All linked | Some linked | No link |
| PF-SMART-5 | Time-bound | Are time constraints specified where applicable? | All specified | Some missing | No time limits |

## Issue Classification

Each detected issue is classified as:

| Classification | Description | Severity |
|---|---|---|
| `Missing Scenario` | Required scenario type not present | Critical/High |
| `Ambiguous Pass/Fail` | Pass/Fail criteria not measurable | Critical/High |
| `Missing Precondition` | Required precondition not stated | High/Medium |
| `Missing Dependency` | Required dependency not listed | High/Medium |
| `Incorrect Scope` | TC scope doesn't match FR scope | High |
| `Missing Configuration Detail` | Config values not specified | Medium |
| `Missing API Command` | API not specifically named | Medium |
| `Missing CM/PM Data` | Data collection requirements absent | Medium |
| `Inconsistent ID or Value` | IDs/values inconsistent across TC | Medium |
| `Weak Evidence` | Claim not backed by evidence | Medium |
| `Unsupported Assumption` | Assumption without basis | Medium/High |
| `Potential Field Risk` | Known field issue pattern not addressed | High |
| `Human Review Required` | Cannot determine without evidence | Info |

---

## 시나리오별 구체적 검증 기준 (COM rAPP 예시)

### 1. Overshooting Detection TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **TA far-distance** | TA histogram 에서 원거리 section 증가 | "TA > 100km section 이 normal 대비 2 배 이상" | "TA 가 증가한다" (구체적 수치 없음) |
| **DL MAC Throughput** | DL MAC Potential Throughput 감소 | "DL MAC Potential Tput < Th_DMacTputOp" | "Throughput 가 감소한다" |
| **DL Efficiency** | DL Efficiency 감소 | "DL Efficiency < 80% of baseline" | "효율이 떨어진다" |
| **Handover Failure** | HO 실패 증가 | "HO Failure Rate > 5%" | "HO 실패가 발생한다" |
| **Aggressor/Victim** | Aggressor/Victim Cell 식별 | "Cell A(aggressor), Cell B(victim) 명시" | "주변 Cell" (모호) |
| **Severity 계산** | Severity = Max Coverage / Planned Coverage | "Severity = 1.5 (계획의 150%)" | 계산식 없음 |

### 2. Coverage Hole Detection TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **Average CQI** | CQI 감소 | "Avg CQI < 7" | "CQI 가 낮아진다" |
| **DL BLER** | DL BLER 증가 | "DL BLER > 10%" | "BLER 이 증가한다" |
| **UL BLER** | UL BLER 증가 | "UL BLER > 10%" | "UL 품질 저하" |
| **Drop Rate** | Drop Rate 증가 | "Drop Rate > 2%" | "Drop 이 발생한다" |
| **RSRP Event A3** | RSRP Event A3 bad 증가 | "RSRP Event A3 bad counter > 100" | "RSRP 가 낮아진다" |
| **Coverage Hole Score** | Score 임계값 초과 | "Coverage Hole Score > 0.7" | Score 언급 없음 |

### 3. Detection/Resolution Switch Control TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **Detection ON** | 탐지 동작 | "Detection Switch ON → Overshooting Cell 탐지됨" | "동작한다" |
| **Detection OFF** | 탐지 안 함 | "Detection Switch OFF → 탐지 안 됨" | 검증 없음 |
| **Resolution ON** | 해결 동작 | "Resolution Switch ON → Tilt 조정 액션 생성" | "해결한다" |
| **Resolution OFF** | 해결 안 함 | "Resolution OFF → 액션 생성 안 됨" | 검증 없음 |
| **4 가지 조합** | ON-ON, ON-OFF, OFF-ON, OFF-OFF | 4 개 TC 또는 1 개 TC 내 4 개 scenario | 1~2 개 조합만 검증 |

### 4. Carrier Frequency Independence TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **f1 독립 동작** | f1=ON, f2=OFF 시 f1 만 동작 | "f1=ON → f1 Cell 만 탐지, f2=OFF → f2 Cell 탐지 안 됨" | "주파수별로 동작한다" |
| **f2 독립 동작** | f1=OFF, f2=ON 시 f2 만 동작 | "f2=ON → f2 Cell 만 탐지" | 검증 없음 |
| **f1+f2 동시 ON** |両方 ON 시 둘 다 동작 | "f1=ON, f2=ON → 둘 다 탐지" | 검증 없음 |
| **Frequency List** | 검증할 주파수 명시 | "f1=2100MHz, f2=1800MHz" | "각 주파수" (모호) |

### 5. NE List Scope TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **NE List 포함** | List 에 포함된 NE 만 대상 | "NE List: [81000, 81001, 81002]" | "해당 NE" |
| **Indoor 제외** | Indoor cell 제외 조건 | "cell_type != 'indoor'인 Cell 만" | "실내 제외" (조건 명시 없음) |
| **Scope 검증** | List 밖 NE 는 영향 없음 | "NE 81999 는 결과에 포함 안 됨" | 검증 없음 |

### 6. Optimization Period TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **Period 설정** | cluster 별 최적화 주기 | "Optimization Period = 30 분" | "주기적으로" |
| **Period 만료** | Period 만료 시 동작 | "30 분 후 다음 optimization 실행" | 검증 없음 |
| **Period 중 변경** | Period 중 설정 변경 | "Period 중에 변경된 config 는 다음 period 에 적용" | 검증 없음 |

### 7. CM/PM Data Collection TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **Collection Period** | comResolutionPeriod 동안 수집 | "comResolutionPeriod=15 분 동안 PM 수집" | "데이터 수집" |
| **Statistics Item** | 수집 항목 명시 | "PRB, CQI, TA, HO Counter 수집" | "필요한 데이터" |
| **Data Validity** | 유효한 데이터만 사용 | "95% 이상 valid sample 일 때만 계산" | 검증 없음 |

### 8. Analytic Server Dependency TC 검증

| 검증 항목 | 구체적 기준 | Pass 예시 | Issue 예시 |
|---|---|---|---|
| **Server 연결** | Analytic Server 연결 필요 | "Analytic Server 연결 확인" | "서버 필요" |
| **연결 끊김** | 연결 끊김 시나리오 | "연결 끊김 → 오류 로그, graceful degradation" | 검증 없음 |
| **Recovery** | 복구 시나리오 | "연결 복구 → 자동 재시작" | 검증 없음 |

---

## 검증 체크리스트 사용 가이드

### 1. 검증 시작 전

1. **FR 확인**: 검증할 FR 의 requirement 목록 추출
2. **시나리오 식별**: Overshooting/Coverage Hole/Switch Control 등 해당 시나리오 파악
3. **관련 evidence 로드**: `01_retrieval_rules.md` 에 따라 검색

### 2. 검증 수행

1. **RC checks**: FR 매핑 확인
2. **SC checks**: 시나리오 완결성 확인 (위 표의 구체적 기준 적용)
3. **PC checks**: Procedure 실행 가능성 확인
4. **PF checks**: Pass/Fail 기준 측정 가능성 확인
5. **DC checks**: 데이터/설정 일관성 확인
6. **ET checks**: Evidence 인용 확인
7. **FI checks**: 과거 이슈 반영 확인

### 3. 결과 기록

1. **Pass/Warning/Issue 분류**: 각 체크 항목별 판정
2. **근거 인용**: `문서명:줄범위` 형식으로 기록
3. **Human Review Required**: confidence < 0.5 또는 evidence 부족 시 표시

---

## 📄 Citation 규칙 (P0 Critical)

**모든 증거 인용은 원본 파일 형식 (PPTX/DOCX) 으로 해야 합니다!**

### 올바른 Citation 형식

| 원본 파일 | Citation 형식 | 예시 |
|-----------|---------------|------|
| **PPTX** | `{filename}.pptx, Slide {page_number}` | `SVR26A_COM_overshooting.pptx, Slide 12` |
| **DOCX** | `{filename}.docx, Page {page_number}` | `TS28536.docx, Page 45` |
| **PDF** | `{filename}.pdf, Page {page_number}` | `TS28.331.pdf, Page 102` |
| **MD** (원본이 MD 인 경우) | `{filename}.md, Line {start_line}-{end_line}` | `algorithm_design.md, Line 45-52` |

### AI 구현 규칙

AI 는 JSONL chunk 의 metadata 를 사용하여 citation 을 생성합니다:

```python
# JSONL chunk metadata 예시
{
  "source_path": "data\\raw\\algorithm_docs\\SVR26A_Patch_COM_overshooting_algorithm_design.md",
  "metadata": {
    "source_file": "SVR26A_Patch_COM_overshooting_algorithm_design.pptx",
    "page_number": 12
  }
}

# AI citation 생성
if metadata.source_file.endswith('.pptx'):
    citation = f"{metadata.source_file}, Slide {metadata.page_number}"
elif metadata.source_file.endswith('.docx'):
    citation = f"{metadata.source_file}, Page {metadata.page_number}"
elif metadata.source_file.endswith('.pdf'):
    citation = f"{metadata.source_file}, Page {metadata.page_number}"
else:
    citation = f"{metadata.source_file}, Line {chunk.start_line}-{chunk.end_line}"
```

### ❌ 잘못된 Citation 예시

```markdown
# 변환된 MD 파일을 인용하지 마세요!

❌ `SVR26A_COM_overshooting_algorithm_design.md:45-52`
   → 원본은 PPTX 입니다! Slide 번호를 사용해야 합니다.

❌ `algorithm_docs 폴더의 어떤 파일`
   → 파일명을 명시하세요.

❌ `어딘가에서 본 내용인데...`
   → 근거 없는 citation 금지.

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

### Human Review Required 판정 기준

다음 조건 중 하나라도 해당되면 자동 Human Review Required 표시:

| 기준 | 값 | Action |
|------|------|------|
| `metadata.source_file` 없음 | `null` 또는 `undefined` | Human Review Required |
| `metadata.page_number` 없음 | `null` 또는 `undefined` | Line 번호 사용 |
| `confidence` < 0.5 | 신뢰도 낮음 | Human Review Required |
| PPT/Table 추출 | `source_format` 에 "ppt" 또는 "table" 포함 | 내용 누락 가능성 경고 |

---

**문서 업데이트**: 2026-07-27  
**버전**: 3.0 (BM25 Keyword Retrieval 추가)

### 버전 2.0 변경 사항

| 카테고리 | 추가된 검증 항목 | 출처 |
|----------|-----------------|------|
| **Test Level Validation (TL)** | TL-1 ~ TL-5 (5 개) | ISTQB Chapter 2 (SDLC and Testing) |
| **Test Type Validation (TT)** | TT-1 ~ TT-4 (4 개) | ISTQB Chapter 1.2 (Test Types) |
| **Test Technique Validation (TE)** | TE-BB-1 ~ TE-EB-3 (9 개) | ISTQB Chapter 4.2-4.4 (Test Techniques) |
| **Static Testing Validation (ST)** | ST-1 ~ ST-4 (4 개) | ISTQB Chapter 3 (Static Testing) |
| **Risk-Based Testing Validation (RB)** | RB-1 ~ RB-4 (4 개) | ISTQB Chapter 1.3 (Risk-based Testing) |
| **Pass/Fail SMART Validation** | PF-SMART-1 ~ PF-SMART-5 (5 개) | ISTQB Smart Testing 원칙 |

**총 검증 항목**: 기존 30 개 → **57 개**로 확장

---

## 4. BM25 Keyword Retrieval (v3.0 추가)

### 4.1 KeywordRetriever 사용법

```python
from functions.src.rag_embedder.keyword_retriever import KeywordRetriever, KeywordRetrieverConfig
from pathlib import Path

config = KeywordRetrieverConfig(
    jsonl_dir=Path("data/processed/jsonl"),
    index_file=Path("data/processed/keyword_index.json"),
    bm25_k1=1.5,  # BM25 k1 parameter
    bm25_b=0.75,  # BM25 b parameter
)

retriever = KeywordRetriever(config)

# 캐시에서 로드 (권장, 4 초)
if retriever.load_from_cache():
    print("Loaded from cache")
else:
    retriever.load()  # 처음에는 1 분 소요
    retriever.save()

# 검색
results = retriever.search("Overshooting Detection threshold", top_k=5)
for result in results:
    print(f"Score: {result.score:.2f}, Source: {result.source_path}")
```

### 4.2 검색어 추출 규칙 (Phase 1)

Phase 1 에서 추출할 검색어:

| TC 섹션 | 추출 키워드 | 예시 |
|---------|------------|------|
| **Test Purpose** | 핵심 기능 키워드 | "Overshooting Detection", "Resolution algorithm" |
| **Precondition** | 의존성 키워드 | "NE List", "Analytic Server", "VISTA" |
| **Procedure** | API/명령어 키워드 | "REST API", "POST /api/v1", "GET /cells" |
| **Pass/Fail Criteria** | KPI/threshold 키워드 | "TA > 100km", "DL MAC Throughput < threshold" |

### 4.3 Evidence Grade 규칙 (BM25 Score 기반)

| BM25 Score | Grade | 사용 용도 |
|------------|-------|----------|
| ≥ 0.7 | Strong | 요구사항 검증, Pass/Fail 기준 |
| ≥ 0.4 | Supporting | 시나리오 보완, 참고 자료 |
| < 0.4 | Weak | Human Review Required |

### 4.4 BM25 Parameter 튜닝

| Parameter | 기본값 | 설명 | 조정 방향 |
|-----------|--------|------|----------|
| `k1` | 1.5 | Term frequency saturation | 높을수록 TF 영향 증가 |
| `b` | 0.75 | Document length normalization | 1 에 가까울수록 길이 보정 강함 |

**추천 튜닝 시나리오:**
- **짧은 문서 중심**: `k1=1.2, b=0.75`
- **긴 문서 중심**: `k1=1.5, b=0.9`
- **균형 잡힌 검색**: `k1=1.5, b=0.75` (기본값)

### 4.5 주의사항

1. **`search_files` 도구 사용 금지**: BM25 Retriever 를 사용하세요.
2. **캐시 활용**: 첫 로드 후 캐시를 사용하면 4 초 내에 로드됩니다.
3. **Citation 규칙**: BM25 검색 결과도 SKILL.md Non-negotiable Rule #8-1 을 따릅니다.
4. **Evidence Grade**: BM25 score 만으로 Grade 를 결정하지 말고, content quality 도 함께 평가하세요.

---

### 버전 3.0 변경 사항

| 카테고리 | 추가 항목 | 설명 |
|----------|----------|------|
| **BM25 Keyword Retrieval** | Section 4 전체 | BM25 Retriever 사용법, 검색어 추출 규칙, Evidence Grade 규칙 |
| **SKILL.md Non-negotiable Rule** | Rule #13 | Phase 1 Evidence Collection 은 BM25 Keyword Retriever 를 사용한다 |
| **AGENTS.md Step 0** | BM25 Retriever 초기화 | TC Review 시작 전 BM25 Retriever 초기화 코드 추가 |

**총 문서 버전**: 2.1 → **3.0**
