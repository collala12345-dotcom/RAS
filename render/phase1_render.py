#!/usr/bin/env python3
"""
Phase 1 Evidence Collection - TC v1: 8.6.2.1.9.2.4.3 Cell/Feature level - ES group configuration
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from functions.src.tc_reviewer.phase1_evidence_collector import (
    Phase1Output, EvidenceRecord, RequirementMapping, GotchaIssue, ProposedChange,
    render_phase1_markdown
)

phase1_data = Phase1Output(
    tc_id="8.6.2.1.9.2.4.3",
    tc_title="Cell/Feature level - ES group configuration",
    fr_id="FR50/FR51/FR60",
    fr_description="FR50: ESM shall generate ES candidate sector list in every pre-defined interval. FR51: ESM shall select EN-DC anchor and coverage carrier cell to maximize ES capable cells. FR60: ESM shall configure and transmit multi-level ES configuration for each group based on group IP Tput & group PRB utilization statistics.",
    evidence_list=[
        EvidenceRecord(
            evidence_id="EVD-001",
            source="ESM Algorithm Design Slides, Slide 158-159",
            content="ES configuration (Initial) - ES group list generation (1/5): From prequalification, ES_candidate_sector_info configured. ESFO determines ES capable cells for each group. ES feature can not be performed on DSS enabled cell / e-MTC enabled cell. At least one cell shall support Coverage band / EN-DC anchor. Selection criteria for Coverage carrier / EN-DC priority.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-002",
            source="ESM Algorithm Design Slides, Slide 216",
            content="Overall procedure of LTE+NR ESM: Step 1) Cluster level operation - Determination for coverage carrier, EN(NR)-DC anchor carrier. Step 2) ES candidate sector/cell selection - Exclusion for Low KPI(mobility, IP throughput) cell, high mobility/high indoor coverage cell. Step 3) Offloading target cell selection. Step 4) ES configuration.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-003",
            source="ESM Algorithm Design Slides, Slide 386-388",
            content="ESM shall take care below items: (1/3) If there is no other overlaid cells(any LTE/NR), NR cell can consist single group of ES configuration. (2/3) ES level configuration shall be performed independently. Based on LTE NR group index, ESM determines ES configuration for each LTE+NR group. (3/3) ES level configuration shall be performed based on offloading traffic.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-004",
            source="ESM Algorithm Design Slides, Slide 141",
            content="Pre processing for Multi-level ES configuration: Group List - 1) Generate ES group list with ES_candidate_sector_info. Columns include Cell Num, Common Name, Administrative state, dss-cell-indicator, emtc-switch, Coverage carrier priority, Coverage band, endc-support/endc-anchor-type, EN-DC priority, ES capability.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-005",
            source="ESM Algorithm Design Slides, Slide 160",
            content="ES group list generation (2/5): If there is no highest priority on Coverage carrier / EN-DC, ESFO chooses the other priority that can make more ES cells below NallowedEScell. If there are more carrier whose coverage carrier or EN-DC priority is not the highest, preferred priority is coverage carrier. If there is excluded cell due to high mobility or Macro-outdoor-high indoor coverage, ESM shall set ES capability as False.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-006",
            source="ESM Algorithm Design Slides, Slide 148-151",
            content="Multi-level ES configuration (2/8): concept - ES applied when used RB is lesser than Threshold. ESFO plots the correlation graph between IP Tput and Used RB for each group using the PM statistics per 15mins during (N-1)th ES configuration management interval. ESFO determines RB threshold to satisfy required IP Tput. PRB Threshold = 140.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-007",
            source="ESM Algorithm Design Slides, Slide 168-169",
            content="Multi-level ES configuration procedure (1/8): Operation period - after the last operation window-wise operation in every esConfigurationManagementInterval. Target: every group in ES group list. 1) ESM checks GBP(LBP). 2) ESM checks applying ES capability for each GBP(LBP) in ascending order. If ESM finds entering threshold for target GBP(LBP), ESM increases ES level by 1.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-008",
            source="ESM Algorithm Design Slides, Slide 205-206",
            content="Multi-level ES configuration update procedure (1/4): Output table contains OperationWindow, group index, Level, Cell list, ES feature. Example: OperationWindow 1 (00:00~05:00), group 5615701, Level 1 (Lhigh-1) Cnum#7 (850M) Cell off, Level 2 (Lhigh) Cnum#4 (PCS) Cell off.",
            confidence="Supporting"
        ),
        EvidenceRecord(
            evidence_id="EVD-009",
            source="ESM Algorithm Design Slides, Slide 233",
            content="Yang parameter setting: DU (2/2) - managed-element/gnb-du-function/son/energy-saving/group-operation/group-config-entires. group-level-1~10: 그룹별 ES level 설정 파라미터. group-level-x/es-mode-type: level x에 적용할 ES feature. group-level-x/es-entering-threshold-ipt: level x로 진입을 위해 판단하는 IP Tput 조건. group-level-x/es-entering-threshold-prb: level x로 진입을 위해 판단하는 PRB utilization 조건.",
            confidence="Supporting"
        ),
        EvidenceRecord(
            evidence_id="EVD-010",
            source="ESM Algorithm Design Slides, Slide 46-49",
            content="Cluster level operation: For each cluster, coverage carrier selection priority and EN-DC anchor carrier selection priority are generated. coverageCarrierSelectionInterval: range 1~16 (week), default 4. esConfigurationManagementInterval: range 1~4 (week), default 1. Coverage & EN-DC anchor carrier selection priority: (0) highest priority, (7) lowest priority, (-1) not selected.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-011",
            source="ESM Algorithm Design Slides, Slide 305",
            content="[Recap] Configuration for ESFO operation: Cluster-level operation - Coverage & EN-DC anchor carrier selection priorities generated for each cluster. Sector-level operation - ES candidate sectors selected for each operation window (weekday & weekend). ES cell & feature selection - A proper Cell-ES feature combination determined.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-012",
            source="ESM Algorithm Design Slides, Slide 385",
            content="Concept of Offloading based ES configuration (7/7): ES level, ES feature, Entering Condition, Target Cell, IP Tput Threshold, PRB Threshold table. Example: Level 1 Cell off Target B 12Mbps 19%, Level 2 Tx.Path off Target C 10Mbps 48%, Level 3 Tx.Path off Target D 10Mbps 68%.",
            confidence="Supporting"
        ),
        EvidenceRecord(
            evidence_id="EVD-013",
            source="32551-j00.docx, Page 20",
            content="TS 32.551: Energy Savings Management (ESM); Concepts and Requirements. Two energy saving states: notEnergySaving state, energySaving state. REQ-DIES-FUN-01: IRP Agent shall allow IRPManager to define a list of cells to prevent them from going into energySaving state.",
            confidence="Strong"
        ),
        EvidenceRecord(
            evidence_id="EVD-014",
            source="ESM Algorithm Design Slides, Slide 377",
            content="Energy Consumption data (FR-1): Multi-level ES configuration for maximization of energy efficiency. Automatic setting of multi-level ES operation per group(Sector/band). Configure the multi-level ES operation for each group based on the traffic volume and IP Tput. For each ES level, the combination of ES feature and cell is determined. Configure the transition condition between ES levels to guarantee required IP Tput.",
            confidence="Supporting"
        ),
    ],
    requirement_mapping=[
        RequirementMapping(
            requirement="FR50: ES candidate sector list generation in every pre-defined interval",
            coverage="⚠️ 간접 언급",
            step="Procedure Step 1 (ES_sector_list.csv 확인), Step 4 (es_grp_list 출력 확인)"
        ),
        RequirementMapping(
            requirement="FR50: Sector satisfying exclusion conditions not included in ES candidate list",
            coverage="❌ 누락됨",
            step="-"
        ),
        RequirementMapping(
            requirement="FR51: Select EN-DC anchor and coverage carrier cell to maximize ES capable cells",
            coverage="✅ 반영됨",
            step="Procedure Step 5, Pass/Fail Criteria 2"
        ),
        RequirementMapping(
            requirement="FR51: Maximize the number of ES capable cells in the sector",
            coverage="⚠️ 간접 언급",
            step="Pass/Fail Criteria 2 (ES Level 7 / ES Feature 0 확인)"
        ),
        RequirementMapping(
            requirement="FR60: Configure multi-level ES configuration for each group",
            coverage="✅ 반영됨",
            step="Procedure Step 4, Pass/Fail Criteria 1"
        ),
        RequirementMapping(
            requirement="FR60: Based on group IP Tput & group PRB utilization statistics distribution",
            coverage="❌ 누락됨",
            step="-"
        ),
        RequirementMapping(
            requirement="FR60: Configuration for following ES configuration management interval",
            coverage="⚠️ 간접 언급",
            step="Procedure Step 3 (request_date=20241101-2300 실행)"
        ),
    ],
    gotcha_issues=[
        GotchaIssue(
            gotcha_id="GOTCHA-001",
            past_problem="알고리즘/구조 설계 누락 - 설계 문서에 알고리즘 상세 로직이 명시되지 않음",
            current_risk="FR60의 multi-level ES configuration이 group IP Tput & PRB utilization 통계 기반으로 생성되는지 검증 부족. TC는 출력 파일 형식만 확인하고 알고리즘 입력 통계를 검증하지 않음",
            prevention="es_grp_list 출력 파일의 ES level/feature 값이 이전 esConfigurationManagementInterval의 IP Tput & PRB 통계 기반으로 생성되었는지 검증 단계 추가"
        ),
        GotchaIssue(
            gotcha_id="GOTCHA-003",
            past_problem="TC coverage 부족 - 복잡한 조합/연계 상황 검증 누락",
            current_risk="FR50의 exclusion condition (Low KPI, high mobility, high indoor coverage cell) 검증 누락. ES candidate sector list에서 제외되어야 할 sector가 실제로 제외되었는지 확인하지 않음",
            prevention="ES_sector_list.csv 입력에 exclusion 대상 sector를 포함시키고, es_grp_list 출력에서 해당 sector가 제외되었는지 검증 단계 추가"
        ),
        GotchaIssue(
            gotcha_id="GOTCHA-004",
            past_problem="TC coverage 부족 - Precondition 검증 누락, Pass/Fail Criteria 모호",
            current_risk="Pass/Fail Criteria 1의 'strange value'가 모호하여 객관적 판정 불가. 어떤 값이 'strange'인지 정의 없음",
            prevention="Pass/Fail Criteria를 구체화: group index column의 유효 값 범위, 허용되는 ES Level(1~7), ES Feature(0~N) 값 명시"
        ),
    ],
    proposed_changes=[
        ProposedChange(
            change_id="CHG-001",
            priority="P1",
            content="FR50 exclusion condition 검증 누락 - ES candidate sector list에서 제외 조건(Low KPI, high mobility, high indoor coverage) 만족 sector가 실제 제외되었는지 검증 단계 추가 필요"
        ),
        ProposedChange(
            change_id="CHG-002",
            priority="P1",
            content="FR60 통계 기반 검증 누락 - multi-level ES configuration이 group IP Tput & group PRB utilization 통계 기반으로 생성되었는지 검증 단계 추가 필요"
        ),
        ProposedChange(
            change_id="CHG-003",
            priority="P2",
            content="Pass/Fail Criteria 1 'strange value' 모호 - 객관적 판정 기준(유효 group index 범위, 허용 ES Level/Feature 값) 명시 필요"
        ),
        ProposedChange(
            change_id="CHG-004",
            priority="P2",
            content="Negative Scenario 누락 - invalid ES_sector_list.csv 입력, exclusion 대상 sector 포함 시 검증 시나리오 추가 필요"
        ),
        ProposedChange(
            change_id="CHG-005",
            priority="P2",
            content="FR50 pre-defined interval 검증 누락 - esConfigurationManagementInterval 주기로 ES candidate sector list가 갱신되는지 검증 필요"
        ),
        ProposedChange(
            change_id="CHG-006",
            priority="P3",
            content="관측 방법 명확화 - Step 4 'vim or text editor로 csv 파일 열기'를 자동화 가능한 검증 방법(grep, pandas 등)으로 구체화 필요"
        ),
        ProposedChange(
            change_id="CHG-007",
            priority="P3",
            content="FR51 'maximize ES capable cells' 검증 보완 - EN-DC anchor/coverage carrier 선택이 실제로 ES capable cell 수를 최대화하는지 검증 기준 추가 필요"
        ),
    ],
    gate1_status="READY"
)

markdown_output = render_phase1_markdown(phase1_data)
print(markdown_output)
