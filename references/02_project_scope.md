# 02. Required Evidence Fields

## Purpose

Defines what fields must be extracted from TC v1 and what evidence fields must be sought during review.

## TC v1 Parse Fields

When parsing TC v1, extract the following:

| Field | Description | Required |
|---|---|---|
| `tc_id` | Test Case ID (e.g., 8.6.2.1.15.3.1.1) | ✅ |
| `tc_title` | Test Case title | ✅ |
| `test_overview` | What the test verifies | ✅ |
| `test_purpose` | Detailed test purpose | ✅ |
| `dependency` | Required NEs, interfaces, protocols, radio technology | ✅ |
| `related_feature` | Feature ID (e.g., COA-CSON0003) | ✅ |
| `related_fr` | FR IDs referenced (e.g., FR10, FR11, FR12) | ✅ |
| `precondition` | Test environment, pre-configuration, required data | ✅ |
| `test_procedure` | Step-by-step test execution | ✅ |
| `pass_fail_criteria` | Pass/Fail determination criteria | ✅ |
| `api_command` | API commands mentioned (if any) | ❌ |
| `ne_list_scope` | NE List / cell scope mentioned | ❌ |
| `frequency_condition` | Carrier frequency conditions | ❌ |
| `switch_config` | Switch ON/OFF settings (Detection, Resolution) | ❌ |
| `threshold_kpi` | Threshold or KPI values mentioned | ❌ |
| `cm_pm_data` | CM/PM data collection requirements | ❌ |
| `optimization_period` | Optimization period settings | ❌ |
| `test_env_assumptions` | Assumptions about test environment | ❌ |

## Evidence Chunk Fields (from JSONL)

When retrieving evidence, look for these fields in each JSONL chunk:

| Field | Description | Usage |
|---|---|---|
| `chunk_id` | Unique chunk identifier | Reference tracking |
| `doc_id` | Source document identifier | Source grouping |
| `doc_type` | Document type (fr, hld, dld, etc.) | Priority filtering |
| `source_path` | Original file path | Traceability |
| `section` | Section name/number | Context matching |
| `title` | Chunk title | Relevance matching |
| `heading_path` | Full heading hierarchy | Structure matching |
| `start_line` | Start line in source file | Exact citation |
| `end_line` | End line in source file | Exact citation |
| `text` | Chunk content | Content analysis |
| `requirement_id` | FR ID if applicable | FR matching |
| `tc_id` | TC ID if applicable | TC matching |
| `related_fr` | Related FR IDs | Cross-reference |
| `ne_id` | NE identifier | Scope matching |
| `cell_id` | Cell identifier | Scope matching |

## Evidence Gap Tracking

For each TC field that cannot be validated with available evidence:

```json
{
  "tc_field": "api_command",
  "tc_value": "Run the COM with API command",
  "evidence_needed": "DLD or API specification listing actual REST API endpoint for COM execution",
  "evidence_status": "not_found",
  "impact": "Cannot verify if API command is correct",
  "action": "Human Review Required"
}
```

---

## Review Metadata Schema (v2_review_metadata)

모든 JSONL chunk 는 10 개의 review metadata 필드를 포함합니다. 이 필드들은 RAG 검색과 TC 검증에 활용됩니다.

### Metadata 필드 상세

| # | 필드명 | 타입 | 설명 | 예시 | 생성 규칙 |
|---|---|---|---|---|---|
| 1 | `feature_area` | str | 기능 영역 | "Overshooting", "Coverage Hole", "Mobility" | chunk content 기반 분류 |
| 2 | `related_rapp` | str | 관련 rAPP | "COM", "SON", "Energy Saving" | chunk content 에서 추출 |
| 3 | `related_function` | str | 세부 기능 | "Detection", "Resolution", "Compensation" | chunk content 에서 추출 |
| 4 | `review_role` | str | Review 용도 | "Use this chunk to verify detection logic" | chunk 의 용도 명시 |
| 5 | `priority` | str | 우선순위 | "P0", "P1", "P2", "P3" | 중요도 기반 할당 |
| 6 | `human_review_required` | bool | 사람 확인 필요 | true, false | 불확실성 기반 |
| 7 | `confidence` | float | 신뢰도 | 0.0 ~ 1.0 | 추출 신뢰도 |
| 8 | `evidence_scope` | str | evidence 수준 | "algorithm", "requirement", "standard" | 문서 유형 기반 |
| 9 | `related_keywords` | list[str] | 검색 키워드 | ["threshold", "KPI", "switch"] | chunk 에서 추출 |
| 10 | `metadata_version` | str | schema 버전 | "v2_review_metadata" | 고정 값 |

### Metadata Priority 규칙

| 우선순위 | 기준 | 예시 |
|---|---|---|
| **P0** | FR 원문, 핵심 알고리즘 | FR10/11/12 정의, Detection logic |
| **P1** | HLD/DLD, Algorithm Design | System flow, API spec, Threshold |
| **P2** | Legacy TC, Issue cases | TC 패턴, 과거 문제 |
| **P3** | 3GPP 표준, 일반 문서 | 용어 정의, 절차 |

### Metadata 생성 예시

**예시 1: FR10 Overshooting Detection chunk**

```json
{
  "chunk_id": "fr10_overshooting_001",
  "doc_type": "feature_specs",
  "source_path": "data/feature_specs/FR10_COM_overshooting.md",
  "feature_area": "Overshooting",
  "related_rapp": "COM",
  "related_function": "Detection",
  "review_role": "Use this chunk to verify FR10 requirement coverage",
  "priority": "P0",
  "human_review_required": false,
  "confidence": 0.95,
  "evidence_scope": "requirement",
  "related_keywords": ["overshooting", "detection", "aggressor", "victim", "TA far-distance"],
  "metadata_version": "v2_review_metadata"
}
```

**예시 2: Algorithm Design Threshold chunk**

```json
{
  "chunk_id": "algo_threshold_001",
  "doc_type": "algorithm_docs",
  "source_path": "data/algorithm_docs/SVR26A_COM_overshooting_algorithm_design.docx",
  "feature_area": "Overshooting",
  "related_rapp": "COM",
  "related_function": "Detection",
  "review_role": "Use this chunk to verify threshold values (Th_DMacTputOp)",
  "priority": "P1",
  "human_review_required": false,
  "confidence": 0.85,
  "evidence_scope": "algorithm",
  "related_keywords": ["Th_DMacTputOp", "threshold", "KPI", "DL MAC Potential Throughput"],
  "metadata_version": "v2_review_metadata"
}
```

**예시 3: 불확실한 chunk (Human Review 필요)**

```json
{
  "chunk_id": "ppt_diagram_001",
  "doc_type": "algorithm_docs",
  "source_path": "data/algorithm_docs/COM_design_overview.pptx",
  "feature_area": "Unknown",
  "related_rapp": "COM",
  "related_function": "Unknown",
  "review_role": "Diagram extracted from PPT - text content may be incomplete",
  "priority": "P2",
  "human_review_required": true,
  "confidence": 0.4,
  "evidence_scope": "design",
  "related_keywords": ["diagram", "flow"],
  "metadata_version": "v2_review_metadata"
}
```

### Metadata 활용 방법

**1. RAG 검색 시 필터링:**

```python
collection.query(
    query_embeddings=embedding,
    where={
        "feature_area": {"$in": ["Overshooting"]},
        "related_rapp": "COM",
        "priority": {"$in": ["P0", "P1"]},
        "confidence": {"$gte": 0.5}
    }
)
```

**2. Human Review Required 판정:**

```python
if evidence.confidence < 0.5 or evidence.human_review_required:
    mark_as_human_review_required()
```

**3. Evidence 우선순위 정렬:**

```python
# P0 > P1 > P2 > P3 순으로 정렬
priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
sorted_evidence = sorted(evidence, key=lambda x: priority_order[x.priority])
```

---

## Evidence Traceability 규칙

모든 TC 검증 결과는 evidence 와 연결되어야 합니다:

| 규칙 | 설명 | 예시 |
|---|---|---|
| **Citation 필수** | 모든 주장에는 evidence citation 이 필요 | "FR10 에 명시됨 [1]" |
| **Line Range 명시** | 줄 범위까지 정확히 기록 | `FR10_COM_overshooting.md:12-18` |
| **Multiple Evidence** | 여러 증거는 번호 목록으로 병기 | "[1] FR10:12-18, [2] HLD:45-50" |
| **Evidence Not Found** | 없는 증거는 명시적으로 기록 | "Evidence not found: API endpoint spec" |


