# 00. Project Scope

## Purpose

This project is a **TC Review & Enhancement Layer** that sits on top of the existing TC generation AI/RAG pipeline. It does NOT generate new test cases from scratch. Instead, it takes an existing TC v1 (produced by the generation Skill) and reviews, validates, and enhances it using evidence from preprocessed JSONL chunks.

## 🤖 AI 에이전트 초기 응답 (필수!)

**사용자가 "SKILL.md 를 읽고 이 툴이 뭔지 이해하세요"라고 하면, 아래 응답을 반드시 포함하세요:**

```
"이해했습니다. RAS-TestCaseReview 는 Human-in-the-loop TC Review 툴입니다.

[워크플로우]
1. Phase 1: Evidence Collection (RAG 검색)
2. Phase 2: Review Queue 생성 (변경 제안서)
3. Reviewer 결정 대기 (승인/수정후승인/거절/보류)
4. Phase 3: TC v2 생성 (승인된 변경만 병합)

TC v1 을 보내주시면 검토를 시작하겠습니다."
```

> ⚠️ **중요**: 마지막 줄 "**TC v1 을 보내주시면 검토를 시작하겠습니다.**"는 사용자 초대 멘트로 반드시 포함되어야 합니다!

## What This Skill Does

1. Parse TC v1 and extract its structure (Overview, Purpose, Dependency, Precondition, Procedure, Pass/Fail Criteria).
2. Identify relevant evidence from preprocessed JSONL (FR, HLD, DLD, Algorithm, Legacy TC, Issue, Test Result, 3GPP).
3. Validate requirement coverage, scenario completeness, procedure clarity, pass/fail clarity, and data consistency.
4. Detect missing scenarios, ambiguous pass/fail criteria, and unsupported assumptions.
5. Produce Enhanced TC v2, Quality Report, Reviewer Summary, Evidence List, and Change Log.

## What This Skill Does NOT Do

- Generate TC from scratch (that is the generation Skill's job).
- Invent company-specific values (API names, NE IDs, thresholds, KPI names).
- Perform embedding, vector DB indexing, or network calls (Stage 1 / future Stage 5 scope).
- Replace the original test intent of TC v1.
- Upload or process data outside the local environment.

## Boundary

| In Scope | Out of Scope |
|---|---|
| Review and enhance TC v1 | Generate TC v1 from FR/HLD/DLD |
| Evidence-based gap detection | Fine-tuning AI models |
| Quality scoring and risk indication | Automated test execution |
| Domain plugin rules (COM rAPP) | rAPP-specific algorithm implementation |
| Evidence traceability (source_path, line_range) | Real-time data ingestion |

## Current Stage

- **Stage 1 (md → JSONL)**: Completed for 3GPP docs. Other doc types pending.
- **Stage 1.5 (Evidence quality validation)**: In progress.
- **Stage 2 (Review Skill MVP)**: This is the current focus.
- Evidence availability is limited. Reviews are conducted with available evidence; missing evidence is marked `Evidence not found` or `Human Review Required`.

## Key Principle

> When data becomes available, all outputs produced without evidence will be revised based on the new data. The current MVP establishes the review framework, quality rubric, and output structure so that evidence can be plugged in later.
