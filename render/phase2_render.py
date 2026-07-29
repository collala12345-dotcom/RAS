#!/usr/bin/env python3
"""
Phase 2 Review Queue Generation - TC v1: 8.6.2.1.9.2.4.3 Cell/Feature level - ES group configuration
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from functions.src.tc_reviewer.phase2_review_queue_generator import (
    ReviewQueue, ChangeProposal, TCLocation,
    Priority, Operation, IssueType, EvidenceStatus,
    render_review_queue_markdown
)

review_queue = ReviewQueue(
    review_id="RQ-20260728-001",
    tc_id="8.6.2.1.9.2.4.3",
    tc_v1_path="input/8.6.2.1.9.2.4.3_Cell_Feature_level_ES_group_configuration.md",
    tc_v1_checksum="a1b2c3d4e5f6",
    generated_at="2026-07-28",
    gate1_status="READY",
    proposals=[
        ChangeProposal(
            change_id="CHG-001",
            review_block_id="2-5",
            priority=Priority.P1,
            priority_reason_code="MISSING_EXCLUSION_CONDITION",
            operation=Operation.ADD,
            tc_location=TCLocation(section="Procedure Step 1-2"),
            issue_type=IssueType.MISSING,
            finding="FR50 exclusion condition 검증 누락 - ES candidate sector list에서 제외 조건(Low KPI, high mobility, high indoor coverage)을 만족하는 sector가 실제로 es_grp_list에서 제외되었는지 검증하는 단계가 없음",
            impact="FR50 요구사항 미충족 - exclusion 대상 sector가 ES candidate에 포함될 위험",
            before_text=None,
            proposed_text="Procedure Step 2 이후에 검증 단계 추가: ES_sector_list.csv 입력에 exclusion 대상 sector(Low KPI, high mobility, Macro-outdoor-high indoor coverage)를 포함시키고, es_grp_list 출력에서 해당 sector의 cell이 ES capability=False로 설정되었는지 또는 그룹에서 제외되었는지 확인",
            rationale="FR50은 ES candidate sector list를 생성할 때 exclusion condition을 만족하는 sector를 제외해야 함. EVD-002(Slide 216)와 EVD-005(Slide 160)에서 exclusion 조건이 명시되어 있으나 TC는 이를 검증하지 않음",
            related_requirement_ids=["FR50"],
            evidence_refs=["EVD-002", "EVD-005"],
            evidence_status=EvidenceStatus.CONFIRMED,
            evidence_status_label_ko="근거로 확인됨",
            citations=[
                {"evidence_id": "EVD-002", "document_title": "ESM Algorithm Design Slides, Slide 216"},
                {"evidence_id": "EVD-005", "document_title": "ESM Algorithm Design Slides, Slide 160"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-002",
            review_block_id="2-1",
            priority=Priority.P1,
            priority_reason_code="MISSING_STAT_VERIFICATION",
            operation=Operation.ADD,
            tc_location=TCLocation(section="Procedure Step 3-4"),
            issue_type=IssueType.MISSING,
            finding="FR60 통계 기반 검증 누락 - multi-level ES configuration이 group IP Tput & group PRB utilization 통계 분포를 기반으로 생성되었는지 검증하는 단계가 없음. TC는 출력 파일 형식만 확인하고 알고리즘 입력 통계를 검증하지 않음",
            impact="FR60 요구사항 미충족 - 통계 기반 ES configuration 생성 로직 검증 불가",
            before_text=None,
            proposed_text="Procedure Step 4 이후에 검증 단계 추가: (1) esConfigurationManagementInterval 이전 주기의 PM 통계(IP Tput, PRB utilization) 데이터가 존재하는지 확인, (2) es_grp_list의 ES level/feature 값이 해당 통계 기반으로 산정되었는지 검증 (예: entering threshold IPT/PRB 값과 PM 통계 비교)",
            rationale="FR60은 group IP Tput & group PRB utilization statistics distribution을 기반으로 multi-level ES configuration을 생성해야 함. EVD-006(Slide 148-151)과 EVD-007(Slide 168-169)에서 통계 기반 알고리즘이 명시되어 있으나 TC는 이를 검증하지 않음",
            related_requirement_ids=["FR60"],
            evidence_refs=["EVD-006", "EVD-007", "EVD-009"],
            evidence_status=EvidenceStatus.CONFIRMED,
            evidence_status_label_ko="근거로 확인됨",
            citations=[
                {"evidence_id": "EVD-006", "document_title": "ESM Algorithm Design Slides, Slide 148-151"},
                {"evidence_id": "EVD-007", "document_title": "ESM Algorithm Design Slides, Slide 168-169"},
                {"evidence_id": "EVD-009", "document_title": "ESM Algorithm Design Slides, Slide 233"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-003",
            review_block_id="2-4",
            priority=Priority.P2,
            priority_reason_code="AMBIGUOUS_PASSFAIL_CRITERIA",
            operation=Operation.MODIFY,
            tc_location=TCLocation(section="Pass/Fail Criteria 1"),
            issue_type=IssueType.AMBIGUOUS,
            finding="Pass/Fail Criteria 1의 'strange value'가 모호하여 객관적 판정이 불가능함. 어떤 값이 'strange'인지 정의가 없어 Reviewer마다 다르게 해석할 수 있음",
            impact="객관적 Pass/Fail 판정 불가, 재현성 저하",
            before_text="group index column에 strange value가 없어야 함",
            proposed_text="Pass/Fail Criteria 1을 구체화: (1) group index column의 유효 값 범위 명시 (예: 양의 정수), (2) 허용되는 ES Level 값 범위 명시 (1~7), (3) 허용되는 ES Feature 값 명시 (0: No ES, 1: Cell off, 2: Tx.Path off 등), (4) 'strange value'를 '유효 범위를 벗어난 값'으로 정의",
            rationale="객관적이고 재현 가능한 Pass/Fail 판정을 위해 허용 값 범위가 명시되어야 함. EVD-008(Slide 205-206)과 EVD-012(Slide 385)에서 ES level/feature 값의 예시가 제공됨",
            related_requirement_ids=["FR60"],
            evidence_refs=["EVD-008", "EVD-012"],
            evidence_status=EvidenceStatus.SUGGESTED,
            evidence_status_label_ko="보완 제안",
            citations=[
                {"evidence_id": "EVD-008", "document_title": "ESM Algorithm Design Slides, Slide 205-206"},
                {"evidence_id": "EVD-012", "document_title": "ESM Algorithm Design Slides, Slide 385"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-004",
            review_block_id="2-5",
            priority=Priority.P2,
            priority_reason_code="MISSING_NEGATIVE_SCENARIO",
            operation=Operation.ADD,
            tc_location=TCLocation(section="Procedure (Negative/Abnormal Scenario)"),
            issue_type=IssueType.UNCOVERED_SCENARIO,
            finding="Negative Scenario가 누락됨 - invalid ES_sector_list.csv 입력, exclusion 대상 sector만 포함된 입력, 빈 sector list 등 예외 상황에 대한 검증 시나리오가 없음",
            impact="비정상 동작 검증 불완전, 예외 상황에서 시스템 안정성 미확인",
            before_text=None,
            proposed_text="Negative Scenario 추가: (1) ES_sector_list.csv에 exclusion 대상 sector만 포함된 경우 es_grp_list가 빈 파일 또는 에러 메시지 출력 확인, (2) 잘못된 형식의 CSV 입력 시 에러 처리 확인, (3) ES capable cell이 0개인 sector에 대한 처리 확인",
            rationale="FR50의 exclusion condition이 모든 sector에 적용될 경우 ES candidate sector list가 빈 상황을 검증해야 함. EVD-005(Slide 160)에서 ES capability=False 설정이 명시됨",
            related_requirement_ids=["FR50"],
            evidence_refs=["EVD-005"],
            evidence_status=EvidenceStatus.SUGGESTED,
            evidence_status_label_ko="보완 제안",
            citations=[
                {"evidence_id": "EVD-005", "document_title": "ESM Algorithm Design Slides, Slide 160"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-005",
            review_block_id="2-2",
            priority=Priority.P2,
            priority_reason_code="MISSING_PRECONDITION_INTERVAL",
            operation=Operation.ADD,
            tc_location=TCLocation(section="Precondition 및 Procedure Step 1"),
            issue_type=IssueType.MISSING,
            finding="FR50 pre-defined interval 검증 누락 - esConfigurationManagementInterval 주기로 ES candidate sector list가 갱신되는지 검증하지 않음. TC는 단일 시점의 출력만 확인하고 주기적 갱신을 검증하지 않음",
            impact="FR50 주기적 갱신 요구사항 검증 불가",
            before_text=None,
            proposed_text="Precondition에 esConfigurationManagementInterval 설정 값 명시 및 Procedure에 주기적 갱신 검증 단계 추가: (1) Precondition에 esConfigurationManagementInterval=1(week) 설정 확인, (2) 2회 이상의 esConfigurationManagementInterval 경과 후 es_grp_list가 갱신되었는지 확인",
            rationale="FR50은 every pre-defined interval마다 ES candidate sector list를 생성해야 함. EVD-010(Slide 46-49)에서 esConfigurationManagementInterval: range 1~4 (week), default 1이 명시됨",
            related_requirement_ids=["FR50"],
            evidence_refs=["EVD-010", "EVD-007"],
            evidence_status=EvidenceStatus.CONFIRMED,
            evidence_status_label_ko="근거로 확인됨",
            citations=[
                {"evidence_id": "EVD-010", "document_title": "ESM Algorithm Design Slides, Slide 46-49"},
                {"evidence_id": "EVD-007", "document_title": "ESM Algorithm Design Slides, Slide 168-169"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-006",
            review_block_id="2-3",
            priority=Priority.P3,
            priority_reason_code="NON_OBSERVABLE_METHOD",
            operation=Operation.MODIFY,
            tc_location=TCLocation(section="Procedure Step 4"),
            issue_type=IssueType.NON_OBSERVABLE,
            finding="관측 방법이 비구체적임 - 'vim or text editor로 csv 파일 열기'는 자동화가 불가능하고 Reviewer마다 다른 도구를 사용할 수 있어 재현성이 떨어짐",
            impact="재현성 저하, 자동화 불가",
            before_text="vim or text editor로 csv 파일 열기",
            proposed_text="관측 방법을 구체화: (1) Python pandas를 사용한 CSV 파싱 및 컬럼별 값 검증 스크립트 제공, (2) grep/awk를 사용한 특정 컬럼 값 추출 방법 명시, (3) 자동화된 검증 스크립트 예시 추가",
            rationale="재현 가능하고 자동화 가능한 검증 방법이 필요함. EVD-009(Slide 233)에서 Yang parameter 구조가 명시되어 있어 자동화 검증이 가능함",
            related_requirement_ids=["FR60"],
            evidence_refs=["EVD-009"],
            evidence_status=EvidenceStatus.SUGGESTED,
            evidence_status_label_ko="보완 제안",
            citations=[
                {"evidence_id": "EVD-009", "document_title": "ESM Algorithm Design Slides, Slide 233"}
            ]
        ),
        ChangeProposal(
            change_id="CHG-007",
            review_block_id="2-4",
            priority=Priority.P3,
            priority_reason_code="INSUFFICIENT_VERIFICATION",
            operation=Operation.MODIFY,
            tc_location=TCLocation(section="Pass/Fail Criteria 2"),
            issue_type=IssueType.AMBIGUOUS,
            finding="FR51 'maximize ES capable cells' 검증이 불충분함 - EN-DC anchor/coverage carrier 선택이 실제로 ES capable cell 수를 최대화하는지 검증하는 기준이 없음. 단순히 ES Level 7 / ES Feature 0을 확인하는 것은 'maximize'를 검증하지 않음",
            impact="FR51 maximize 요구사항 검증 불충분",
            before_text="ES Level 7 / ES Feature 0 확인",
            proposed_text="Pass/Fail Criteria 2 보완: (1) ES_sector_list.csv의 전체 cell 수 대비 es_grp_list에서 ES capability=True로 설정된 cell 수의 비율 확인, (2) EN-DC anchor/coverage carrier 선택을 변경했을 때 ES capable cell 수가 감소하는지 역산 검증",
            rationale="FR51은 EN-DC anchor와 coverage carrier cell을 선택하여 ES capable cell 수를 최대화해야 함. EVD-001(Slide 158-159)과 EVD-005(Slide 160)에서 ES capable cell 최대화 로직이 명시됨",
            related_requirement_ids=["FR51"],
            evidence_refs=["EVD-001", "EVD-005"],
            evidence_status=EvidenceStatus.SUGGESTED,
            evidence_status_label_ko="보완 제안",
            citations=[
                {"evidence_id": "EVD-001", "document_title": "ESM Algorithm Design Slides, Slide 158-159"},
                {"evidence_id": "EVD-005", "document_title": "ESM Algorithm Design Slides, Slide 160"}
            ]
        ),
    ],
    gate2_result=None
)

markdown_output = render_review_queue_markdown(
    review_queue,
    tc_title="Cell/Feature level - ES group configuration",
    related_fr="FR50/FR51/FR60"
)
print(markdown_output)
