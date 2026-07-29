# AGENTS.md — RAS-TestCaseReview Agent Guide

> **버전**: 2.0 (2026-07-28, SKILL.md 6.0 연동)

---

# 🚨 [최우선 명령] - TC v1 수신 시 3 초 안에 수행

## 1️⃣ Phase 1 시작 전 - 의무 선행 단계 (Pre-Phase 1)

**TC v1 이 입력되면, Block 1-1 수행 전 반드시 다음 파일을 먼저 읽어야 합니다:**

### 필수 읽기 파일 (12 개 - 전부 읽기)
- [ ] `references/00_ai_agent_persona.md` - AI 페르소나
- [ ] `references/01_gotchas.md` - 과거 실수 패턴
- [ ] `references/02_project_scope.md` - 프로젝트 범위
- [ ] `references/03_retrieval_rules.md` - BM25 검색 규칙
- [ ] `references/04_required_evidence_fields.md` - 필수 Evidence 필드
- [ ] `references/05_tc_validation_checklist.md` - 검증 체크리스트
- [ ] `references/06_quality_rubric.md` - 품질 평가 기준
- [ ] `references/07_refinement_rules.md` - 개선 규칙
- [ ] `references/08_output_format.md` - 출력 형식
- [ ] `references/09_com_domain_rules.md` - COM 도메인 규칙
- [ ] `references/10_security_and_data_policy.md` - 보안 및 데이터 정책
- [ ] `references/com_fr_dependency.json` - FR 의존성
- [ ] `references/rapp_interoperability.json` - rAPP 상호운용성

**위 파일을 읽지 않고 Phase 1 을 시작하면 모든 결과는 무효화되며 Human Review 로 이관됩니다.**

---

## 2️⃣ TC v1 검토 시 반드시 다음 5 가지를 수행하세요:

1. **출력 형식 준수**: Phase 1/2 는 SKILL.md 고정 형식 (채팅창 직접 출력)
2. **Block 2-1~2-10 수행**: `phase2_review_queue_generator.py` 로직 따름
3. **BM25 검색 의무**: 검색 후 Evidence **full text** 읽기 (snippet 만 금지)
4. **테스트 데이터 복사 금지**: pre-built 데이터 사용 시 Human Review Required
5. **Human-in-the-loop**: AI 승인/거절 금지, Reviewer 결정 대기

**위반 시 모든 결과는 무효화되며 Human Review 로 이관됩니다.**

---

## 🚨 Non-negotiable Rules (8 개 압축)

1. **TC v1 의도 보존**: 새로운 TC 생성 금지, 입력 TC v1 검토·보완만
2. **Phase 1 은 근거만**: TC v1 평가/수정 금지, Evidence 수집만
3. **Phase 2 는 Review Queue 만**: TC v2 생성 금지, 변경 제안서만 생성
4. **WAITING 상태 기본값**: AI 가 승인/거절 자동 결정 금지
5. **Phase 3 은 승인된 변경만**: 거절/보류는 병합 금지
6. **Citation 규칙**: PPTX=Slide, DOCX=Page, MD=Line (원본 파일 형식)
7. **문서 충돌 노출**: AI 가 조용히 해결 금지, `CONFLICT` 로 표시
8. **Traceability**: TC v2 의 모든 Diff 는 승인된 Change ID 연결

---

## 📦 Phase 1: Evidence Collection

### 수행 Block (1-1 ~ 1-9) - **반드시 순서대로 수행**
| Block | 내용 | Python 함수 |
|-------|------|-------------|
| 1-1 | TC Intake & Intent Understanding | `extract_search_keywords()` |
| 1-2 | Requirement Matching | FR 매핑 |
| 1-3 | Design Behavior Retrieval | BM25 검색 |
| 1-4 | Algorithm/KPI/Parameter Retrieval | BM25 검색 |
| 1-5 | Standard/3GPP Retrieval | BM25 검색 |
| 1-6 | Legacy TC Retrieval | BM25 검색 |
| 1-7 | Issue/Bug/Test Result Retrieval | BM25 검색 |
| 1-8 | Cross-rAPP/Common Pattern Retrieval | BM25 검색 |
| 1-9 | Evidence Grading & Pack Generation | `grade_evidence_by_bm25_score()` |

### Gate 1 판정 (명시적 기준)
- `READY`: Strong evidence ≥ 1 개 → Phase 2 전체 검토
- `READY_WITH_GAPS`: Strong 0 개 but Supporting ≥ 1 개 → Phase 2 수행 (근거 제한)
- `BLOCKED`: Evidence 0 개 → **Human Review 로 이관 (Phase 2 진행 금지)**

### 출력 (Phase 1) - Python Renderer 사용 (의무!)

**AI 는 반드시 `render_phase1_markdown()` 함수를 사용하여 출력을 생성해야 합니다. 수동 작성 금지!**

```python
from functions.src.tc_reviewer.phase1_evidence_collector import (
    Phase1Output, EvidenceRecord, RequirementMapping, GotchaIssue, ProposedChange,
    render_phase1_markdown
)

# Phase1Output 데이터 모델 생성
phase1_data = Phase1Output(
    tc_id="8.6.2.1.15.3.2.1",
    tc_title="Configure NE for COM operation",
    fr_id="FR13",
    fr_description="NR Coverage Optimization Manager should be able to configure NE...",
    evidence_list=[
        EvidenceRecord(evidence_id="EVD-001", source="SVR26A.docx, Page 15", content="FR13 요구사항 명시", confidence="Strong"),
    ],
    requirement_mapping=[
        RequirementMapping(requirement="NE List", coverage="✅ 반영됨", step="Precondition A.2"),
    ],
    gotcha_issues=[
        GotchaIssue(gotcha_id="GOTCHA-004", past_problem="TC coverage 부족", current_risk="NE List 업데이트 precondition 누락", prevention="Type 1/Type 2 정의"),
    ],
    proposed_changes=[
        ProposedChange(change_id="CHG-001", priority="P1", content="Sector exclusion list 누락"),
    ],
    gate1_status="READY"
)

# 고정 형식으로 렌더링 (절대 수동 작성 금지!)
markdown_output = render_phase1_markdown(phase1_data)
print(markdown_output)
```

**이 함수를 사용하지 않고 수동으로 출력을 작성하면 모든 결과는 무효화됩니다.**

### Block 수행 체크리스트 (의무 출력)

```markdown
### Phase 1 Block 수행 체크리스트

- [ ] Block 1-1: TC Intake & Intent Understanding (수행 완료)
- [ ] Block 1-2: Requirement Matching (수행 완료)
- [ ] Block 1-3: Design Behavior Retrieval (수행 완료)
- [ ] Block 1-4: Algorithm/KPI/Parameter Retrieval (수행 완료)
- [ ] Block 1-5: Standard/3GPP Retrieval (수행 완료)
- [ ] Block 1-6: Legacy TC Retrieval (수행 완료)
- [ ] Block 1-7: Issue/Bug/Test Result Retrieval (수행 완료)
- [ ] Block 1-8: Cross-rAPP/Common Pattern Retrieval (수행 완료)
- [ ] Block 1-9: Evidence Grading & Pack Generation (수행 완료)

**체크되지 않은 Block 이 있으면 Evidence Pack 이 불완전합니다.**
```

---

## 📝 Phase 2: Review Queue 생성

### 수행 Block (2-1 ~ 2-10) - **반드시 순서대로 수행**
| Block | 내용 | Python 함수 |
|-------|------|-------------|
| 2-1 | Requirement Coverage (Intent/Action/Oracle Link) | `_run_block_2_1_requirement_coverage()` |
| 2-2 | Scope/Precondition Review | `_run_block_2_2_scope_precondition()` |
| 2-3 | Procedure Executability Review | `_run_block_2_3_procedure_executability()` |
| 2-4 | Observability & Pass/Fail Review | `_run_block_2_4_observability_passfail()` |
| 2-5 | Scenario Coverage Review | `_run_block_2_5_scenario_coverage()` |
| 2-6 | Historical Risk & Consistency Review | `_run_block_2_6_historical_consistency()` |
| 2-7 | Gotcha Checkpoint 적용 | `_run_block_2_7_gotcha_checkpoint()` |
| 2-8 | Atomic Change Proposal Generation | `_generate_change_proposals()` |
| 2-9 | Priority & Evidence Status (P1/P2/P3, 한글 근거) | `_assign_priority()` |
| 2-10 | Review Queue Generation | `ReviewQueue()` 생성 |

### 우선순위 규칙
- **P1**: FR 직접 충돌, 잘못된 Expected Result, 실행 불가 API, 안전성 누락
- **P2**: Negative/Abnormal Scenario 누락, 주요 Precondition 모호
- **P3**: 표현 명확화, 절차 세분화, 형식 개선

### 근거 상태 (한글)
- `근거로 확인됨`: Strong Evidence 기반
- `보완 제안`: Supporting Evidence 또는 Coverage 기법
- `문서 간 충돌`: Evidence 간 상충
- `판단 근거 부족`: Missing/Weak Evidence

### 출력 (Phase 2) - Python Renderer 사용 (의무!)

**AI 는 반드시 `render_review_queue_markdown()` 함수를 사용하여 출력을 생성해야 합니다. 수동 작성 금지!**

```python
from functions.src.tc_reviewer.phase2_review_queue_generator import (
    ReviewQueue, ChangeProposal,
    render_review_queue_markdown
)

# ReviewQueue 데이터 모델 생성
review_queue = ReviewQueue(
    tc_id="8.6.2.1.15.3.2.1",
    tc_title="Configure NE for COM operation",
    fr_id="FR13",
    changes=[
        ChangeProposal(
            change_id="CHG-001",
            priority="P1",
            tc_location="Precondition A",
            finding="NE List Type 1/Type 2 정의 누락",
            proposal="Type 1/Type 2 정의 추가",
            rationale="FR13 요구사항",
            citation="SVR26A.docx, Page 15",
            evidence_status="근거로 확인됨"
        ),
    ],
    gate2_status="READY_FOR_REVIEW"
)

# 고정 형식으로 렌더링 (절대 수동 작성 금지!)
markdown_output = render_review_queue_markdown(review_queue, tc_title="Configure NE", related_fr="FR13")
print(markdown_output)
```

**이 함수를 사용하지 않고 수동으로 출력을 작성하면 모든 결과는 무효화됩니다.**

```markdown
## [Phase 2] TC v1 검토 완료 - Review Queue 생성

**TC ID**: {tc_id} - {tc_title}
**관련 FR**: {fr_id} ({fr_description})
**검토 완료**: {YYYY-MM-DD}

---

### 📋 Review Queue (변경 검토 제안서)

| Change ID | 우선순위 | TC 위치 | 발견 내용 | 변경 제안 | 제안 이유 | 상세 근거 | 근거 상태 |
|-----------|----------|---------|-----------|-----------|-----------|-----------|-----------|
| CHG-001 | P1 | ... | ... | ... | ... | ... | ... |

---

### 📊 검토 요약

| 항목 | 내용 |
|------|------|
| **총 변경 제안** | {count} 건 |
| **P1 (필수 확인)** | {p1_count} 건 |
| **P2 (주요 보완)** | {p2_count} 건 |
| **P3 (개선 제안)** | {p3_count} 건 |

---

### 🔍 증거 기반 주요 발견

| {fr_id} 요구사항 | TC 반영 여부 | 검증 Step |
|-----------------|--------------|-----------|
| {req_1} | ✅/❌/⚠️ | {step} |

---

### ⚠️ Gotcha 기반 예측 문제

| Gotcha ID | 과거 문제 | 현재 위험 | 예방 조치 |
|-----------|----------|----------|----------|
| GOTCHA-XXX | {과거} | {현재} | {예방} |

**Gotcha Checkpoint 적용 결과:**
- [ ] 적용된 Checkpoint: {X} 개
- [ ] 누락된 Checkpoint: {Y} 개

---

### ⏸️ 다음 단계 (Reviewer Decision 대기)

```
결정 유형: 승인 / 수정후승인 / 거절 / 보류
예시:
CHG-001: 승인
CHG-002: 수정후승인 (최종 반영 내용 필수)
CHG-003: 보류 (사유 필수)
```

**모든 Change ID 기본 상태: `WAITING`**
```

### Block 수행 체크리스트 (의무 출력)

```markdown
### Phase 2 Block 수행 체크리스트

- [ ] Block 2-1: Requirement Coverage (수행 완료)
- [ ] Block 2-2: Scope/Precondition Review (수행 완료)
- [ ] Block 2-3: Procedure Executability Review (수행 완료)
- [ ] Block 2-4: Observability & Pass/Fail Review (수행 완료)
- [ ] Block 2-5: Scenario Coverage Review (수행 완료)
- [ ] Block 2-6: Historical Risk & Consistency Review (수행 완료)
- [ ] Block 2-7: Gotcha Checkpoint 적용 (수행 완료)
- [ ] Block 2-8: Atomic Change Proposal Generation (수행 완료)
- [ ] Block 2-9: Priority & Evidence Status (수행 완료)
- [ ] Block 2-10: Review Queue Generation (수행 완료)

**체크되지 않은 Block 이 있으면 Review Queue 가 불완전합니다.**
```

---

## 🛠️ Phase 3: Controlled Merge

### 수행 Block (3-1 ~ 3-7) - **반드시 순서대로 수행**
| Block | 내용 | Python 함수 |
|-------|------|-------------|
| 3-1 | Reviewer Decision Parser | `_parse_reviewer_decision()` |
| 3-2 | Decision Validation | `_validate_decision()` |
| 3-3 | Approved Change Classification | `_classify_approved_changes()` |
| 3-4 | Controlled Merge (ADD/MODIFY/DELETE/SPLIT) | `_apply_change()` |
| 3-5 | TC v2 Generation & Integrity Check | `_verify_tc_v2()` |
| 3-6 | Change History Generation | `_generate_change_history()` |
| 3-7 | Final Output Packaging | `_package_output()` |

### Gate 3: Decision Readiness Gate
- G3-01: Review ID 와 Proposal Version 일치
- G3-02: TC v1 checksum 일치
- G3-03: 모든 Change ID 존재
- G3-04: 결정 중복 없음
- G3-05: WAITING 항목 없음
- G3-06: 수정후승인 항목에 최종 반영 내용 있음

### 출력 (Phase 3) - 파일 생성
```
output/
└── {tc_id}_{feature_name}/
    ├── 01_TC_v2.md
    └── 02_Review_Queue_With_Change_History.md
```

### Block 수행 체크리스트 (의무 출력)

```markdown
### Phase 3 Block 수행 체크리스트

- [ ] Block 3-1: Reviewer Decision Parser (수행 완료)
- [ ] Block 3-2: Decision Validation (수행 완료)
- [ ] Block 3-3: Approved Change Classification (수행 완료)
- [ ] Block 3-4: Controlled Merge (수행 완료)
- [ ] Block 3-5: TC v2 Generation & Integrity Check (수행 완료)
- [ ] Block 3-6: Change History Generation (수행 완료)
- [ ] Block 3-7: Final Output Packaging (수행 완료)

**체크되지 않은 Block 이 있으면 TC v2 가 불완전합니다.**
```

---

## 📄 Citation 규칙 (P0 Critical)

| 원본 파일 | Citation 형식 | 예시 |
|-----------|---------------|------|
| **PPTX** | `{filename}.pptx, Slide {page}` | `SVR26A_COM.pptx, Slide 12` |
| **DOCX** | `{filename}.docx, Page {page}` | `TS28536.docx, Page 45` |
| **PDF** | `{filename}.pdf, Page {page}` | `TS28.331.pdf, Page 102` |
| **MD** | `{filename}.md, Line {start}-{end}` | `algo.md, Line 45-52` |

**절대 금지**: JSON 파일 인용 (`com_fr_dependency.json, FR13`), 근거 없는 citation

---

## 📚 참조 문서

| 파일 | 목적 |
|------|------|
| `references/00_ai_agent_persona.md` | AI 페르소나 |
| `references/01_gotchas.md` | 과거 실수 |
| `references/05_tc_validation_checklist.md` | 검증 체크리스트 |
| `references/rapp_interoperability.json` | rAPP 연계 규칙 |
| `references/com_fr_dependency.json` | FR 의존성 |

---

**버전**: 2.0 (2026-07-28, SKILL.md 6.0 연동)
