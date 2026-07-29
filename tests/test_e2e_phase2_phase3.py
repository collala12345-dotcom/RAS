#!/usr/bin/env python3
"""
End-to-End Integration Test: Phase 2 → Phase 3

TC v1 → Phase 2 (Review Queue) → Reviewer Decision → Phase 3 (TC v2 + Change History)

전체 Human-in-the-loop 워크플로우를 검증합니다.
"""

import json
import sys
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tc_reviewer.phase2_review_queue_generator import (
    Phase2ReviewQueueGenerator,
    render_review_queue_markdown,
    render_review_queue_json
)
from tc_reviewer.phase3_controlled_merge import (
    Phase3ControlledMerge,
    render_change_history_markdown,
    render_phase3_result_json
)


# ============================================================================
# 테스트용 샘플 데이터
# ============================================================================

SAMPLE_TC_V1 = """# Test Case: TC-COM-001

## 1. Test Overview
- **TC ID**: TC-COM-001
- **Feature**: FGR-CC3101
- **Target rAPP**: COM
- **TC Title**: NR Cell Overshooting Detection Verification

## 2. Test Purpose
NR Cell 대상 Overshooting Detection 기능 검증

## 3. Dependency & Limitation
- **Dependencies**:
  - Analytic Server 연결 필요
  - NE List 수신 완료

## 4. Related Feature
- FGR-CC3101: Overshooting Detection

## A. Precondition
- NE List 준비
- CM/PM 데이터 수집 완료
- Detection Switch 초기화

## B. Test Procedure

### B.1. Normal Scenario
1. Detection Switch ON 설정
2. Result 확인

### B.2. Additional Test
1. Frequency 1 대상 Detection 수행
2. 결과 Log 확인

## C. Pass/Fail Criteria
- Pass: 정상 동작 확인
"""

SAMPLE_EVIDENCE_PACK = {
    "requirement_evidence": [
        {
            "evidence_id": "EVD-REQ-001",
            "source_type": "requirement",
            "document_title": "FR-11",
            "document_version": "2.0",
            "section_number": "3.2",
            "normalized_statement": "Carrier Frequency 별 Detection ON/OFF 제어",
            "source_excerpt": "The system shall control Overshooting Detection per Carrier Frequency..."
        },
        {
            "evidence_id": "EVD-REQ-002",
            "source_type": "requirement",
            "document_title": "FR-11",
            "document_version": "2.0",
            "section_number": "3.3",
            "normalized_statement": "Detection Resolution 연동",
            "source_excerpt": "Detection 결과에 따라 Resolution 을 수행한다..."
        }
    ],
    "design_evidence": [
        {
            "evidence_id": "EVD-HLD-001",
            "source_type": "design",
            "document_title": "HLD-COM",
            "document_version": "2.1",
            "section_number": "6.2",
            "normalized_statement": "Detection OFF 시 미동작",
            "source_excerpt": "Detection Switch 가 OFF 이면 Detection 을 수행하지 않는다..."
        }
    ],
    "historical_risk_evidence": [
        {
            "evidence_id": "EVD-ISSUE-001",
            "source_type": "issue",
            "document_title": "Field Issue Report",
            "document_version": "1.0",
            "trigger_condition": "Detection OFF 상태에서 Resolution ON",
            "symptom": "잘못된 Resolution Action 생성"
        }
    ],
    "conflict_groups": [],
    "missing_evidence": []
}

SAMPLE_GATE1_RESULT = {
    "status": "READY",
    "restrictions": []
}

# Reviewer Decision 시뮬레이션
SAMPLE_REVIEWER_INPUT = """
CHG-001: 승인
사유: Detection OFF 시나리오 필수

CHG-002: 수정후승인
최종 반영 내용:
Fail: 관측 결과가 기대값과 일치하지 않거나 오류 Log 발생 시

CHG-003: 승인

CHG-004: 거절
사유: 이번 Release 검증 범위에 포함되지 않음

CHG-005: 보류
사유: API 담당자에게 기준 Parameter 확인 필요
"""


def run_e2e_test():
    """
    End-to-End 테스트 실행
    
    Phase 2 → Reviewer Decision → Phase 3 전체 흐름
    """
    print("=" * 80)
    print("End-to-End Integration Test: Phase 2 -> Phase 3")
    print("=" * 80)
    print()
    
    # =========================================================================
    # Phase 2: Review Queue Generation
    # =========================================================================
    print("[Phase 2] Review Queue Generation")
    print("-" * 80)
    
    phase2 = Phase2ReviewQueueGenerator(
        tc_v1_content=SAMPLE_TC_V1,
        evidence_pack=SAMPLE_EVIDENCE_PACK,
        gate1_result=SAMPLE_GATE1_RESULT
    )
    
    review_queue = phase2.run()
    
    print(f"Review ID: {review_queue.review_id}")
    print(f"TC ID: {review_queue.tc_id}")
    print(f"Gate 1 Status: {review_queue.gate1_status}")
    print(f"Gate 2 Status: {review_queue.gate2_result['status']}")
    print(f"Total Proposals: {review_queue.proposal_count['total']}")
    print(f"  - P1: {review_queue.proposal_count['p1']}")
    print(f"  - P2: {review_queue.proposal_count['p2']}")
    print(f"  - P3: {review_queue.proposal_count['p3']}")
    print()
    
    # Review Queue Markdown 출력 (일부)
    print("[Review Queue Summary]")
    print(render_review_queue_markdown(review_queue)[:2000] + "...")
    print()
    
    # =========================================================================
    # Reviewer Decision (시뮬레이션)
    # =========================================================================
    print("[Reviewer Decision (Simulated)]")
    print("-" * 80)
    print(SAMPLE_REVIEWER_INPUT.strip())
    print()
    
    # =========================================================================
    # Phase 3: Controlled Merge
    # =========================================================================
    print("[Phase 3] Controlled Merge")
    print("-" * 80)
    
    # Review Proposal (Phase 2 출력)
    review_proposal = render_review_queue_json(review_queue)
    
    phase3 = Phase3ControlledMerge(
        tc_v1_content=SAMPLE_TC_V1,
        review_proposal=review_proposal,
        reviewer_input=SAMPLE_REVIEWER_INPUT,
        reviewer_id="test_reviewer"
    )
    
    result = phase3.run()
    
    print(f"Status: {result.status.value}")
    print(f"Gate 3 Status: {result.gate3_result['status']}")
    print(f"Applied Changes: {len(result.finalization_manifest.get('applied_change_ids', []))}")
    print()
    
    # Change History 출력
    print("[Change History]")
    print(render_change_history_markdown(result.change_history))
    print()
    
    # TC v2 출력 (간략화)
    print("[TC v2 Content Preview]")
    print("-" * 80)
    print(result.tc_v2_content[:1500] + "..." if len(result.tc_v2_content) > 1500 else result.tc_v2_content)
    print()
    
    # =========================================================================
    # 테스트 결과 검증
    # =========================================================================
    print("[Test Validation]")
    print("-" * 80)
    
    errors = []
    
    # 1. Gate 2 통과 확인
    if review_queue.gate2_result["status"] != "READY_FOR_REVIEW":
        errors.append(f"Gate 2 실패: {review_queue.gate2_result['status']}")
    
    # 2. Gate 3 통과 확인
    if result.gate3_result["status"] not in ["READY_TO_MERGE", "READY_TO_MERGE_WITH_WARNING"]:
        errors.append(f"Gate 3 실패: {result.gate3_result['status']}")
    
    # 3. Change History 완전성 확인
    if len(result.change_history) != review_queue.proposal_count['total']:
        errors.append(f"Change History 불일치: {len(result.change_history)} != {review_queue.proposal_count['total']}")
    
    # 4. TC v2 가 비어있지 않은지 확인
    if not result.tc_v2_content.strip():
        errors.append("TC v2 가 비어있음")
    
    # 5. Finalization Manifest 확인
    manifest = result.finalization_manifest
    if manifest.get("proposal_count", 0) != review_queue.proposal_count['total']:
        errors.append(f"Manifest proposal_count 불일치")
    
    # 결과 출력
    if errors:
        print("[FAILED] Test FAILED")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("[PASSED] Test PASSED")
        print()
        print("[Final Summary]")
        print(f"  - Phase 2 Proposals: {review_queue.proposal_count['total']}")
        print(f"  - Phase 3 Applied: {len(manifest.get('applied_change_ids', []))}")
        print(f"  - Change History: {len(result.change_history)} entries")
        print(f"  - Final Status: {result.status.value}")
        return True


def save_test_output():
    """테스트 결과를 output/ 폴더에 저장"""
    output_dir = Path(__file__).parent.parent.parent / "output" / "e2e_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Phase 2 실행
    phase2 = Phase2ReviewQueueGenerator(
        tc_v1_content=SAMPLE_TC_V1,
        evidence_pack=SAMPLE_EVIDENCE_PACK,
        gate1_result=SAMPLE_GATE1_RESULT
    )
    review_queue = phase2.run()
    
    # Review Queue 저장
    with open(output_dir / "review_queue.md", "w", encoding="utf-8") as f:
        f.write(render_review_queue_markdown(review_queue))
    
    with open(output_dir / "review_queue.json", "w", encoding="utf-8") as f:
        json.dump(render_review_queue_json(review_queue), f, indent=2, ensure_ascii=False)
    
    # Phase 3 실행
    review_proposal = render_review_queue_json(review_queue)
    phase3 = Phase3ControlledMerge(
        tc_v1_content=SAMPLE_TC_V1,
        review_proposal=review_proposal,
        reviewer_input=SAMPLE_REVIEWER_INPUT,
        reviewer_id="test_reviewer"
    )
    result = phase3.run()
    
    # TC v2 저장
    with open(output_dir / "tc_v2.md", "w", encoding="utf-8") as f:
        f.write(result.tc_v2_content)
    
    # Change History 저장
    with open(output_dir / "change_history.md", "w", encoding="utf-8") as f:
        f.write(render_change_history_markdown(result.change_history))
    
    # Finalization Manifest 저장
    with open(output_dir / "finalization_manifest.json", "w", encoding="utf-8") as f:
        json.dump(result.finalization_manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n[Output] Output saved to: {output_dir}")
    print(f"  - review_queue.md")
    print(f"  - review_queue.json")
    print(f"  - tc_v2.md")
    print(f"  - change_history.md")
    print(f"  - finalization_manifest.json")


if __name__ == "__main__":
    success = run_e2e_test()
    
    if success:
        save_test_output()
        print("\n[PASSED] End-to-End Test COMPLETED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("\n[FAILED] End-to-End Test FAILED")
        sys.exit(1)
