#!/usr/bin/env python3
"""
Phase 3 Controlled Merge - TC v1: 8.6.2.1.9.2.4.3 Cell/Feature level - ES group configuration
"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from functions.src.tc_reviewer.phase3_controlled_merge import (
    Phase3ControlledMerge, render_phase3_result_json,
    render_review_queue_with_change_history_markdown,
    render_change_history_card
)

# TC v1 원본 내용
tc_v1_content = """# Test Case v1

## 1. Test Overview
- **TC ID**: 8.6.2.1.9.2.4.3
- **Feature**: Cell/Feature level - ES group configuration
- **Related FR**: FR50, FR51, FR60

## 2. Test Purpose
ESM이 ES candidate sector list를 기반으로 ES group list를 생성하고, multi-level ES configuration을 각 group에 대해 구성하는지 검증

## A. Precondition
- ES_sector_list.csv 파일이 준비됨
- ESM rApp이 정상 동작 중
- gNB DU가 정상 동작 중

## B. Test Procedure
1. ES_sector_list.csv 파일 확인
2. ESM에 request_date=20241101-2300으로 ES group configuration 요청
3. es_grp_list 출력 파일 생성 대기
4. vim or text editor로 es_grp_list csv 파일 열기
5. EN-DC anchor 및 coverage carrier cell 선택 결과 확인

## C. Pass/Fail Criteria
1. Pass: es_grp_list의 group index column에 strange value가 없음
2. Pass: ES Level 7 / ES Feature 0 확인
"""

# Review Proposal (Phase 2 출력을 dict 형식으로 변환)
review_proposal = {
    "review_id": "RQ-20260728-001",
    "tc_id": "8.6.2.1.9.2.4.3",
    "gate2_status": "READY_FOR_REVIEW",
    "proposals": [
        {
            "change_id": "CHG-001",
            "priority": "P1",
            "operation": "ADD",
            "tc_location": {"section": "Procedure Step 1-2", "item_id": None},
            "finding": "FR50 exclusion condition 검증 누락",
            "proposed_text": "Procedure Step 2 이후에 검증 단계 추가: ES_sector_list.csv 입력에 exclusion 대상 sector(Low KPI, high mobility, Macro-outdoor-high indoor coverage)를 포함시키고, es_grp_list 출력에서 해당 sector의 cell이 ES capability=False로 설정되었는지 확인",
            "rationale": "FR50은 exclusion condition을 만족하는 sector를 제외해야 함",
            "evidence_status_label_ko": "근거로 확인됨",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 216"}]
        },
        {
            "change_id": "CHG-002",
            "priority": "P1",
            "operation": "ADD",
            "tc_location": {"section": "Procedure Step 3-4", "item_id": None},
            "finding": "FR60 통계 기반 검증 누락",
            "proposed_text": "Procedure Step 4 이후에 검증 단계 추가: (1) esConfigurationManagementInterval 이전 주기의 PM 통계(IP Tput, PRB utilization) 데이터 존재 확인, (2) es_grp_list의 ES level/feature 값이 통계 기반 산정되었는지 검증",
            "rationale": "FR60은 통계 기반으로 config 생성",
            "evidence_status_label_ko": "근거로 확인됨",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 148-151"}]
        },
        {
            "change_id": "CHG-003",
            "priority": "P2",
            "operation": "MODIFY",
            "tc_location": {"section": "Pass/Fail Criteria 1", "item_id": None},
            "finding": "Pass/Fail Criteria 1 'strange value' 모호",
            "proposed_text": "Pass: es_grp_list의 group index column이 양의 정수이며, ES Level 값이 1~7 범위 내에 있고, ES Feature 값이 0(No ES), 1(Cell off), 2(Tx.Path off) 중 하나임",
            "rationale": "객관적 판정을 위해 허용 값 범위 명시",
            "evidence_status_label_ko": "보완 제안",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 205-206"}]
        },
        {
            "change_id": "CHG-004",
            "priority": "P2",
            "operation": "ADD",
            "tc_location": {"section": "Procedure (Negative Scenario)", "item_id": None},
            "finding": "Negative Scenario 누락",
            "proposed_text": "Negative Scenario 추가: (1) ES_sector_list.csv에 exclusion 대상 sector만 포함된 경우 es_grp_list가 빈 파일 또는 에러 메시지 출력 확인, (2) 잘못된 형식의 CSV 입력 시 에러 처리 확인, (3) ES capable cell이 0개인 sector 처리 확인",
            "rationale": "예외 상황 검증 필요",
            "evidence_status_label_ko": "보완 제안",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 160"}]
        },
        {
            "change_id": "CHG-005",
            "priority": "P2",
            "operation": "ADD",
            "tc_location": {"section": "Precondition", "item_id": None},
            "finding": "FR50 pre-defined interval 검증 누락",
            "proposed_text": "Precondition에 esConfigurationManagementInterval=1(week) 설정 명시 및 2회 이상 경과 후 es_grp_list 갱신 확인 단계 추가",
            "rationale": "FR50은 주기적 갱신 필요",
            "evidence_status_label_ko": "근거로 확인됨",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 46-49"}]
        },
        {
            "change_id": "CHG-006",
            "priority": "P3",
            "operation": "MODIFY",
            "tc_location": {"section": "Procedure Step 4", "item_id": None},
            "finding": "관측 방법 비구체적",
            "proposed_text": "Python pandas를 사용한 CSV 파싱 및 컬럼별 값 검증 스크립트로 대체. 예: df = pd.read_csv('es_grp_list.csv'); assert df['group_index'].apply(lambda x: isinstance(x, int) and x > 0).all()",
            "rationale": "재현 가능한 검증 방법 필요",
            "evidence_status_label_ko": "보완 제안",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 233"}]
        },
        {
            "change_id": "CHG-007",
            "priority": "P3",
            "operation": "MODIFY",
            "tc_location": {"section": "Pass/Fail Criteria 2", "item_id": None},
            "finding": "FR51 'maximize ES capable cells' 검증 불충분",
            "proposed_text": "Pass/Fail Criteria 2 보완: (1) ES_sector_list.csv의 전체 cell 수 대비 es_grp_list에서 ES capability=True로 설정된 cell 수의 비율 확인, (2) EN-DC anchor/coverage carrier 선택 변경 시 ES capable cell 수가 감소하는지 역산 검증",
            "rationale": "FR51은 ES capable cell 수 최대화",
            "evidence_status_label_ko": "보완 제안",
            "citations": [{"document_title": "ESM Algorithm Design Slides, Slide 158-159"}]
        }
    ]
}

# Reviewer Decision (모두 승인)
reviewer_input = """
CHG-001: 승인
CHG-002: 승인
CHG-003: 승인
CHG-004: 승인
CHG-005: 승인
CHG-006: 승인
CHG-007: 승인
"""

# Phase 3 실행
phase3 = Phase3ControlledMerge(
    tc_v1_content=tc_v1_content,
    review_proposal=review_proposal,
    reviewer_input=reviewer_input,
    reviewer_id="reviewer1"
)

result = phase3.run()

# 결과 출력
print("=" * 70)
print("Phase 3 Controlled Merge Result")
print("=" * 70)
print()
print(f"Status: {result.status.value}")
print(f"Gate 3: {result.gate3_result['status']}")
print(f"Gate 3 Message: {result.gate3_result.get('message', '')}")
print()

# Change History 출력
print("=" * 70)
print("Change History")
print("=" * 70)
print()
print(render_change_history_card(result.change_history))

# TC v2 출력
print("=" * 70)
print("TC v2 Content")
print("=" * 70)
print()
print(result.tc_v2_content)
print()

# Review Queue with Change History 출력
print("=" * 70)
print("Review Queue with Change History")
print("=" * 70)
print()
print(render_review_queue_with_change_history_markdown(
    tc_id="8.6.2.1.9.2.4.3",
    tc_title="Cell/Feature level - ES group configuration",
    review_date="2026-07-28",
    reviewer_id="reviewer1",
    proposals=review_proposal.get("proposals", []),
    decisions=phase3.decisions,
    change_history=result.change_history
))

# 파일 저장
from pathlib import Path
output_dir = Path("output/8.6.2.1.9.2.4.3_Cell_Feature_level_ES_group_configuration")
output_dir.mkdir(parents=True, exist_ok=True)

# 01_TC_v2.md 저장
with open(output_dir / "01_TC_v2.md", "w", encoding="utf-8") as f:
    f.write(result.tc_v2_content)

# 02_Review_Queue_With_Change_History.md 저장
rq_ch = render_review_queue_with_change_history_markdown(
    tc_id="8.6.2.1.9.2.4.3",
    tc_title="Cell/Feature level - ES group configuration",
    review_date="2026-07-28",
    reviewer_id="reviewer1",
    proposals=review_proposal.get("proposals", []),
    decisions=phase3.decisions,
    change_history=result.change_history
)
with open(output_dir / "02_Review_Queue_With_Change_History.md", "w", encoding="utf-8") as f:
    f.write(rq_ch)

print()
print(f"Files saved to: {output_dir}")
