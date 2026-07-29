# RAS-TestCaseReview - 사용자 가이드

> **프로젝트 개요**: AI 가 생성한 Test Case(TC) v1 을 입력받아, RAG 기반으로 검증하고 **Reviewer 의 통제된 결정 하에** 보완합니다.

---

## 🚨 AI 에이전트 사용 시 필수 프롬프트 (중요!)

> [!IMPORTANT] **AI 에이전트 (Cline, Claude Code 등) 에게 다음 프롬프트를 전달하세요:**
>
> ```
> SKILL.md 와 AGENTS.md 파일을 읽고 이 툴이 뭔지 이해하세요.
> 그리고 SKILL.md 의 [최우선 명령] 과 Non-negotiable Rules 를 읽어.
> Phase 1 과 Phase 2 출력은 반드시 SKILL.md 에 정의된 고정 형식을 따라야 해.
> 각 Phase 의 Block 수행 체크리스트도 출력해야 해.
> TC v1 이 들어오면 정해진 출력 형식으로 결과물을 만들어줘.
> ```

AI 는 기본적으로 SKILL.md 를 읽지만, 출력 형식을 명시적으로 지시하지 않으면 자유 형식으로 응답할 수 있습니다. 반드시 출력 형식 준수를 명시하세요.

---

## 📋 빠른 시작

### 1. TC v1 검토하기

1. AI 에이전트에게 **위 필수 프롬프트** 전달
2. TC v1 을 대화창에 붙여넣기
3. AI 가 Phase 1 → Phase 2 수행 (Block 체크리스트 출력 포함)
4. Reviewer 결정 입력 (승인/수정후승인/거절/보류)
5. AI 가 Phase 3 수행 → TC v2 생성

### 2. 워크플로우

```
┌─────────────────────────────────────────────────────────────────┐
│ 1 회차: TC v1 → Review Queue (변경 검토 제안서)                  │
│    - AI 가 TC v1 을 분석하고 변경 제안을 생성합니다              │
│    - TC v2 는 아직 생성되지 않습니다                            │
│    - Reviewer 가 결정할 때까지 대기합니다                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
│ Reviewer 결정 (Human)                                            │
│    - Change ID 별 승인/수정후승인/거절/보류 입력                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2 회차: Review Queue → TC v2 + Change History                    │
│    - 승인된 변경만 TC v1 에 병합합니다                          │
│    - Enhanced TC v2 와 변경 이력을 생성합니다                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 폴더 구조

```
RAS-TestCaseReview/
│
├── data/                          # 데이터 폴더
│   ├── new/                       # 🆕 새 파일 투입구 (자동 처리됨)
│   │   ├── 3gpp_docs/             # 3GPP 표준 문서 (TS 28.xxx, TS 38.xxx 등)
│   │   ├── algorithm_docs/        # 알고리즘 설계서 (Coverage, Hole, Overshooting 등)
│   │   ├── feature_specs/         # Feature 명세서 (Interface, Geo, Redundancy 등)
│   │   ├── hld_dld/               # HLD/DLD 설계 문서 (CMD, UI, Software Pkg 등)
│   │   ├── issue_cases/           # 과거 이슈 사례 (Bug, Fail, Error, Postmortem 등)
│   │   ├── legacy_tc/             # 기존 Test Case (VVT, Test Spec 등)
│   │   ├── pegs/                  # PEGS 문서
│   │   ├── review_comments/       # 리뷰 코멘트
│   │   └── test_results/          # 테스트 결과 (KPI, Log 등)
│   │
│   ├── raw/                       # 📄 원본 파일 보관소 (PPTX, DOCX, PDF, MD)
│   └── processed/                 # ✅ 전처리된 데이터 (RAG LLM 이 읽는 곳)
│       └── jsonl/                 #    chunk 단위 JSONL 파일들
│
├── references/                    # 📚 Review 룰 (AI 에이전트 필수 읽기)
│   ├── 00_ai_agent_persona.md     # (필수!) AI 에이전트 페르소나
│   ├── 01_gotchas.md              # 과거 실수/주의사항
│   ├── 02_project_scope.md        # 프로젝트 범위
│   ├── 03_retrieval_rules.md      # RAG 검색 전략
│   ├── 04_required_evidence_fields.md  # 증거 필드 정의
│   ├── 05_tc_validation_checklist.md   # 검증 체크리스트
│   ├── 06_quality_rubric.md       # 품질 평가 기준 (검토 관점 재사용)
│   ├── 07_refinement_rules.md     # TC 보완 규칙 (Evidence 기반)
│   ├── 08_output_format.md        # 출력 형식 (Review Queue, Change History)
│   ├── 09_com_domain_rules.md     # COM 도메인 규칙
│   └── 10_security_and_data_policy.md  # 보안 규칙
│
├── RAS_Experience/                # 실무 경험 기록
│   └── RAS-gotchas.md             # 파트원들과의 프롬프트 문답 기록
│
├── functions/tools/               # 🛠️ 실행 도구 (LLM 이 사용하는 스크립트)
│   ├── process_new_docs.py        # 새 파일 자동 처리 (data/new/ → JSONL)
│   ├── document_converter.py      # DOCX/PPTX/PDF → MD 변환
│   ├── metadata_enricher.py       # JSONL metadata 추가 (source_file, page_number 등)
│   ├── add_page_metadata.py       # 페이지 번호 metadata 추가
│   ├── add_metadata_to_existing_jsonl.py  # 기존 JSONL metadata 업데이트
│   ├── merge_enriched_jsonl.py    # JSONL 병합
│   ├── enrich_all_jsonl_metadata.py  # 전체 JSONL metadata 일괄 업데이트
│   ├── download_bge_m3.py         # 임베딩 모델 (BGE-M3) 다운로드
│   └── generate_final_presentation.py  # 발표 자료 생성
│
├── functions/src/tc_reviewer/     # 📦 TC Review Python 모듈
│   ├── phase1_evidence_collector.py       # Phase 1: Evidence Collection (Block 1-1~1-9)
│   ├── phase2_review_queue_generator.py   # Phase 2: Review Queue 생성 (Block 2-1~2-10)
│   └── phase3_controlled_merge.py         # Phase 3: Controlled Merge (Block 3-1~3-7)
│
├── scripts/                       # 🚀 파이프라인 실행 스크립트
│   ├── build_jsonl.py             # JSONL 구축
│   └── ...
│
├── output/                        # 📤 산출물
│   ├── enhanced_tc/               # 보완된 TC v2
│   └── review_queues/             # Review Queue (Phase 2 출력)
│
├── README.md                      # 이 파일 (사용자용 가이드)
├── SKILL.md                       # 🤖 AI 에이전트 실행 지침 (LLM 용) - Block 수행 체크리스트 포함
└── AGENTS.md                      # 🤖 AI 에이전트 가이드 (SKILL.md 와 동일 형식)
```

---

## 📊 새 데이터 추가하기

### 새 문서 (PPTX, DOCX, PDF, MD) 를 RAG 에 추가:

**1. 파일을 적절한 폴더에 넣기:**

```bash
# 3GPP 표준 문서
cp TS28536.docx data/new/3gpp_docs/

# 알고리즘 설계서
cp COM_algo_design.docx data/new/algorithm_docs/

# HLD/DLD 설계서
cp HLD_COM_design.docx data/new/hld_dld/
```

> 💡 **팁**: 폴더 이름을 잘못 넣어도 파일명 패턴으로 자동 분류됩니다.

**2. 처리 명령 실행:**

```bash
# 일괄 처리
python functions/tools/process_new_docs.py

# 감시 모드 (파일 추가 시 자동 처리)
python functions/tools/process_new_docs.py --watch
```

**3. BM25 인덱스 재생성 (필요시):**

> ⚠️ **중요**: `process_new_docs.py` 실행 시 BM25 인덱스가 **자동으로 재생성**됩니다.
> 아래 명령은 JSONL 은 이미 존재하고 인덱스만 갱신할 때만 사용하세요.

```bash
# BM25 인덱스만 재생성 (JSONL 은 그대로)
python rebuild_bm25_index.py
```

### 📌 스크립트별 역할 요약

| 스크립트 | 역할 | JSONL 생성 | BM25 인덱스 |
|---------|------|-----------|------------|
| **`process_new_docs.py`** | 전체 파이프라인 (data/new → raw → MD → JSONL → BM25) | ✅ 생성 | ✅ 빌드 |
| **`rebuild_bm25_index.py`** | BM25 인덱스만 재생성 (기존 JSONL 사용) | ❌ 안생김 | ✅ 빌드 |

> 🚨 **JSONL 이 없으면 `process_new_docs.py` 를 먼저 실행해야 합니다!**
> `rebuild_bm25_index.py` 는 이미 존재하는 JSONL 만 읽습니다.

### 상황별 명령어

```bash
# 1. 새 문서 추가 시 (전체 처리 + 인덱스 자동 재생성)
python functions/tools/process_new_docs.py

# 2. 이미 처리된 파일도 다시 처리할 때
python functions/tools/process_new_docs.py --force

# 3. JSONL 은 있는데 인덱스만 갱신하고 싶을 때
python rebuild_bm25_index.py
```

### 🔍 data/raw 에서 JSONL 누락 파일 찾기

`process_new_docs.py` 는 **data/new/** 폴더만 처리합니다.
이미 `data/raw/` 에 있는 MD 파일 중 JSONL 이 누락된 파일이 있는지 확인하려면:

```bash
# 1. 누락된 파일 찾기 (확인만)
python functions/tools/find_missing_jsonl.py

# 2. 누락된 파일을 JSONL 로 변환
python functions/tools/find_missing_jsonl.py --convert

# 3. 변환 후 BM25 인덱스 재생성
python rebuild_bm25_index.py
```

> 💡 **언제 사용하나요?**
> - `data/raw/` 에 MD 파일은 있는데 검색이 안 될 때
> - 과거에 처리되었지만 JSONL 이 누락된 파일이 의심될 때
> - BM25 인덱스를 재생성했는데도 검색 결과가 적을 때

---

## 🔧 핵심 원칙

- **Human-in-the-loop**: AI 는 승인/거절을 자동 결정하지 않음
- **Block 수행 의무**: AI 는 Phase 1(9 개 Block), Phase 2(10 개 Block), Phase 3(7 개 Block) 을 모두 수행
- **출력 형식 준수**: Python Renderer 로 고정 형식 출력 (수동 작성 금지)
- **Citation 규칙**: PPTX=Slide, DOCX=Page, MD=Line (원본 파일 형식)

---

## 📚 상세 지침

자세한 TC Review 프로세스와 규칙은 **SKILL.md** 를 참조하세요 (AI 에이전트용).

---

**마지막 업데이트**: 2026-07-28  
**버전**: 6.0 (사용자용 간소화)
