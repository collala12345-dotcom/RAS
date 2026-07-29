# Review Queue & Change History - 8.6.2.1.9.2.4.3

**검토 완료일**: 2026-07-28
**Reviewer**: reviewer1

---

## 📋 Review Queue (변경 검토 제안서)

### CHG-001 | 🔴 P1 | Procedure Step 1-2 | ✅ 승인

**발견 내용**
FR50 exclusion condition 검증 누락

**변경 제안**
Procedure Step 2 이후에 검증 단계 추가: ES_sector_list.csv 입력에 exclusion 대상 sector(Low KPI, high mobility, Macro-outdoor-high indoor coverage)를 포함시키고, es_grp_list 출력에서 해당 sector의 cell이 ES capability=False로 설정되었는지 확인

**제안 이유**
FR50은 exclusion condition을 만족하는 sector를 제외해야 함

**상세 근거**
ESM Algorithm Design Slides, Slide 216

**근거 상태**
근거로 확인됨

---

### CHG-002 | 🔴 P1 | Procedure Step 3-4 | ✅ 승인

**발견 내용**
FR60 통계 기반 검증 누락

**변경 제안**
Procedure Step 4 이후에 검증 단계 추가: (1) esConfigurationManagementInterval 이전 주기의 PM 통계(IP Tput, PRB utilization) 데이터 존재 확인, (2) es_grp_list의 ES level/feature 값이 통계 기반 산정되었는지 검증

**제안 이유**
FR60은 통계 기반으로 config 생성

**상세 근거**
ESM Algorithm Design Slides, Slide 148-151

**근거 상태**
근거로 확인됨

---

### CHG-003 | 🟡 P2 | Pass/Fail Criteria 1 | ✅ 승인

**발견 내용**
Pass/Fail Criteria 1 'strange value' 모호

**변경 제안**
Pass: es_grp_list의 group index column이 양의 정수이며, ES Level 값이 1~7 범위 내에 있고, ES Feature 값이 0(No ES), 1(Cell off), 2(Tx.Path off) 중 하나임

**제안 이유**
객관적 판정을 위해 허용 값 범위 명시

**상세 근거**
ESM Algorithm Design Slides, Slide 205-206

**근거 상태**
보완 제안

---

### CHG-004 | 🟡 P2 | Procedure (Negative Scenario) | ✅ 승인

**발견 내용**
Negative Scenario 누락

**변경 제안**
Negative Scenario 추가: (1) ES_sector_list.csv에 exclusion 대상 sector만 포함된 경우 es_grp_list가 빈 파일 또는 에러 메시지 출력 확인, (2) 잘못된 형식의 CSV 입력 시 에러 처리 확인, (3) ES capable cell이 0개인 sector 처리 확인

**제안 이유**
예외 상황 검증 필요

**상세 근거**
ESM Algorithm Design Slides, Slide 160

**근거 상태**
보완 제안

---

### CHG-005 | 🟡 P2 | Precondition | ✅ 승인

**발견 내용**
FR50 pre-defined interval 검증 누락

**변경 제안**
Precondition에 esConfigurationManagementInterval=1(week) 설정 명시 및 2회 이상 경과 후 es_grp_list 갱신 확인 단계 추가

**제안 이유**
FR50은 주기적 갱신 필요

**상세 근거**
ESM Algorithm Design Slides, Slide 46-49

**근거 상태**
근거로 확인됨

---

### CHG-006 | 🟢 P3 | Procedure Step 4 | ✅ 승인

**발견 내용**
관측 방법 비구체적

**변경 제안**
Python pandas를 사용한 CSV 파싱 및 컬럼별 값 검증 스크립트로 대체. 예: df = pd.read_csv('es_grp_list.csv'); assert df['group_index'].apply(lambda x: isinstance(x, int) and x > 0).all()

**제안 이유**
재현 가능한 검증 방법 필요

**상세 근거**
ESM Algorithm Design Slides, Slide 233

**근거 상태**
보완 제안

---

### CHG-007 | 🟢 P3 | Pass/Fail Criteria 2 | ✅ 승인

**발견 내용**
FR51 'maximize ES capable cells' 검증 불충분

**변경 제안**
Pass/Fail Criteria 2 보완: (1) ES_sector_list.csv의 전체 cell 수 대비 es_grp_list에서 ES capability=True로 설정된 cell 수의 비율 확인, (2) EN-DC anchor/coverage carrier 선택 변경 시 ES capable cell 수가 감소하는지 역산 검증

**제안 이유**
FR51은 ES capable cell 수 최대화

**상세 근거**
ESM Algorithm Design Slides, Slide 158-159

**근거 상태**
보완 제안

---


---

## 📊 검토 요약

| 항목 | 내용 |
|------|------|
| **총 변경 제안** | 7 건 |
| **승인** | 7 건 |
| **수정후승인** | 0 건 |
| **거절** | 0 건 |
| **보류** | 0 건 |

### 우선순위별 요약

| 우선순위 | 건수 | Change IDs |
|----------|------|------------|
| **P1 (필수 확인)** | 2 건 | CHG-001, CHG-002 |
| **P2 (주요 보완)** | 3 건 | CHG-003, CHG-004, CHG-005 |
| **P3 (개선 제안)** | 2 건 | CHG-006, CHG-007 |

---

## 📝 변경 이력 (Change History)

### 🔴 CHG-001 | P1 | Procedure Step 1-2 | **승인**

**발견 내용:**
FR50 exclusion condition 검증 누락

**AI 제안:**
Procedure Step 2 이후에 검증 단계 추가: ES_sector_list.csv 입력에 exclusion 대상 sector(Low KPI, high mobility, Macro-outdoor-high indoor coverage)를 포함시키고, es_grp_list 출력에서 해당 sector의 cell이 ES capability=False로 설정되었는지 확인

**최종 반영 내용:**
Procedure Step 2 이후에 검증 단계 추가: ES_sector_list.csv 입력에 exclusion 대상 sector(Low KPI, high mobility, Macro-outdoor-high indoor coverage)를 포함시키고, es_grp_list 출력에서 해당 sector의 cell이 ES capability=False로 설정되었는지 확인

**근거 상태:** 근거로 확인됨

---

### 🔴 CHG-002 | P1 | Procedure Step 3-4 | **승인**

**발견 내용:**
FR60 통계 기반 검증 누락

**AI 제안:**
Procedure Step 4 이후에 검증 단계 추가: (1) esConfigurationManagementInterval 이전 주기의 PM 통계(IP Tput, PRB utilization) 데이터 존재 확인, (2) es_grp_list의 ES level/feature 값이 통계 기반 산정되었는지 검증

**최종 반영 내용:**
Procedure Step 4 이후에 검증 단계 추가: (1) esConfigurationManagementInterval 이전 주기의 PM 통계(IP Tput, PRB utilization) 데이터 존재 확인, (2) es_grp_list의 ES level/feature 값이 통계 기반 산정되었는지 검증

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-003 | P2 | Pass/Fail Criteria 1 | **승인**

**발견 내용:**
Pass/Fail Criteria 1 'strange value' 모호

**AI 제안:**
Pass: es_grp_list의 group index column이 양의 정수이며, ES Level 값이 1~7 범위 내에 있고, ES Feature 값이 0(No ES), 1(Cell off), 2(Tx.Path off) 중 하나임

**최종 반영 내용:**
Pass: es_grp_list의 group index column이 양의 정수이며, ES Level 값이 1~7 범위 내에 있고, ES Feature 값이 0(No ES), 1(Cell off), 2(Tx.Path off) 중 하나임

**근거 상태:** 보완 제안

---

### 🟡 CHG-004 | P2 | Procedure (Negative Scenario) | **승인**

**발견 내용:**
Negative Scenario 누락

**AI 제안:**
Negative Scenario 추가: (1) ES_sector_list.csv에 exclusion 대상 sector만 포함된 경우 es_grp_list가 빈 파일 또는 에러 메시지 출력 확인, (2) 잘못된 형식의 CSV 입력 시 에러 처리 확인, (3) ES capable cell이 0개인 sector 처리 확인

**최종 반영 내용:**
Negative Scenario 추가: (1) ES_sector_list.csv에 exclusion 대상 sector만 포함된 경우 es_grp_list가 빈 파일 또는 에러 메시지 출력 확인, (2) 잘못된 형식의 CSV 입력 시 에러 처리 확인, (3) ES capable cell이 0개인 sector 처리 확인

**근거 상태:** 보완 제안

---

### 🟡 CHG-005 | P2 | Precondition | **승인**

**발견 내용:**
FR50 pre-defined interval 검증 누락

**AI 제안:**
Precondition에 esConfigurationManagementInterval=1(week) 설정 명시 및 2회 이상 경과 후 es_grp_list 갱신 확인 단계 추가

**최종 반영 내용:**
Precondition에 esConfigurationManagementInterval=1(week) 설정 명시 및 2회 이상 경과 후 es_grp_list 갱신 확인 단계 추가

**근거 상태:** 근거로 확인됨

---

### 🟢 CHG-006 | P3 | Procedure Step 4 | **승인**

**발견 내용:**
관측 방법 비구체적

**AI 제안:**
Python pandas를 사용한 CSV 파싱 및 컬럼별 값 검증 스크립트로 대체. 예: df = pd.read_csv('es_grp_list.csv'); assert df['group_index'].apply(lambda x: isinstance(x, int) and x > 0).all()

**최종 반영 내용:**
Python pandas를 사용한 CSV 파싱 및 컬럼별 값 검증 스크립트로 대체. 예: df = pd.read_csv('es_grp_list.csv'); assert df['group_index'].apply(lambda x: isinstance(x, int) and x > 0).all()

**근거 상태:** 보완 제안

---

### 🟢 CHG-007 | P3 | Pass/Fail Criteria 2 | **승인**

**발견 내용:**
FR51 'maximize ES capable cells' 검증 불충분

**AI 제안:**
Pass/Fail Criteria 2 보완: (1) ES_sector_list.csv의 전체 cell 수 대비 es_grp_list에서 ES capability=True로 설정된 cell 수의 비율 확인, (2) EN-DC anchor/coverage carrier 선택 변경 시 ES capable cell 수가 감소하는지 역산 검증

**최종 반영 내용:**
Pass/Fail Criteria 2 보완: (1) ES_sector_list.csv의 전체 cell 수 대비 es_grp_list에서 ES capability=True로 설정된 cell 수의 비율 확인, (2) EN-DC anchor/coverage carrier 선택 변경 시 ES capable cell 수가 감소하는지 역산 검증

**근거 상태:** 보완 제안

---

---

**출력 파일:**
- `01_TC_v2.md`: 최종 보완된 TC
- `02_Review_Queue_With_Change_History.md`: 본 파일 (검토보완서 + 변경이력 통합)