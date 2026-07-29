# Review Queue & Change History - 8.6.2.1.15.3.2.1

**검토 완료일**: 2026-07-27  
**Reviewer**: Reviewer

---

## 📋 Review Queue (변경 검토 제안서)

### CHG-001 | 🔴 P1 | Precondition A.2 | ✅ 승인

**발견 내용**  
NE List 에 대한 구체적 정의 누락

**변경 제안**  
"NE List 는 Type 1 과 Type 2 로 구분되며, Type 1 은 CM/PM 관리 대상, Type 2 는 최적화 적용 대상임을 명시" 추가

**제안 이유**  
FR13 에서 NE List 요구사항이 명시되어 있으나 TC 에서 구체화되지 않음

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

### CHG-002 | 🔴 P1 | Test Procedure B.1 | ✅ 승인

**발견 내용**  
VISTA 로부터 수신하는 정보의 구체적 항목 누락

**변경 제안**  
"NE List, Network Freeze information, Sector exclusion cell list, Dynamic sector list" 각 항목에 대한 구체적 데이터 포맷 명시

**제안 이유**  
FR13 요구사항에서 4 가지 정보 항목을 명시하고 있음

**상세 근거**  
FR13 요구사항 명세서

**근거 상태**  
근거로 확인됨

---

### CHG-003 | 🔴 P1 | Pass/Fail Criteria C | ✅ 승인

**발견 내용**  
Pass/Fail 기준이 모호함 ("normally", "should be able to")

**변경 제안**  
구체적 검증 항목 추가: "1) Type 2 NE List 가 Type 1 NE List 기반으로 올바르게 구성되었는지 확인. 2) Exclusion list 에 포함된 NE 가 Type 2 에서 제외되었는지 확인"

**제안 이유**  
GOTCHA-004 에서 Pass/Fail Criteria 모호성으로 인한 문제 발생 이력

**상세 근거**  
GOTCHA-004

**근거 상태**  
근거로 확인됨

---

### CHG-004 | 🟡 P2 | Test Procedure B.1 | ✅ 승인

**발견 내용**  
Cluster 별 Optimization period 설정 방법 미명시

**변경 제안**  
"Operator 가 VISTA UI 를 통해 cluster 별 optimization period 를 설정하는 단계" 추가

**제안 이유**  
알고리즘 설계서에서 cluster 단위 동작 명시 (Line 327)

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

### CHG-005 | 🟡 P2 | Precondition A.2 | ✅ 승인

**발견 내용**  
Frequency 조합 조건 누락

**변경 제안**  
"File containing information for Overshooting Detection and Resolution provides different combinations for different Carrier frequency" 조건에 대한 구체적 예시 추가 (예: f1=ON/f2=OFF 등)

**제안 이유**  
GOTCHA-003 에서 주파수 조합 검증 누락으로 인한 문제 발생 이력

**상세 근거**  
GOTCHA-003

**근거 상태**  
근거로 확인됨

---

### CHG-006 | 🟡 P2 | Test Procedure B.1 | ✅ 승인

**발견 내용**  
ESM operation time 고려사항 누락

**변경 제안**  
"ESM operation time 을 고려하여 PM counter 수집 제외 시간 (exceptionPMcollectionTime) 을 관리하는지 확인" 단계 추가

**제안 이유**  
알고리즘 설계서에서 ESM operation time superset 계산 명시 (Line 339-364)

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

### CHG-007 | 🟡 P2 | Test Procedure B.1 | ✅ 승인

**발견 내용**  
Cell-RET mapping 검증 단계 누락

**변경 제안**  
"RET information mapping 이 올바르게 되었는지 확인 (o-ran-ru-id, antenna-line-device-id, antenna-id)" 단계 추가

**제안 이유**  
알고리즘 설계서에서 RET mapping 요구사항 명시 (Line 384-399)

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

### CHG-008 | 🟢 P3 | Test Overview | ✅ 승인

**발견 내용**  
Test Purpose 에 "Overshooting Cell Detection and Resolution algorithm" 언급 but Test Overview 에는 COM operation 만

**변경 제안**  
Test Overview 에 "Overshooting Cell Detection 과 Resolution 알고리즘 검증 포함" 명시화

**제안 이유**  
TC 일관성 개선 제안

**상세 근거**  
-

**근거 상태**  
보완 제안

---

### CHG-009 | 🟢 P3 | Precondition A.1 | ✅ 승인

**발견 내용**  
"Statistics items must be collected during comResolutionPeriod" - 구체적 statistics 항목 누락

**변경 제안**  
수집해야 할 PM counter 항목 목록 추가 (Availability, Timing Advance, Air MAC Packet 등)

**제안 이유**  
알고리즘 설계서에서 수집 PM 항목 명시 (Line 366-383)

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

### CHG-010 | 🟡 P2 | Test Procedure B.1 | ✅ 승인

**발견 내용**  
NE List 변경 시나리오 (추가/삭제) 검증 단계 구체화 필요

**변경 제안**  
"NE List 추가 시: 다음 cycle 에 포함됨 검증. NE List 삭제 시: 즉시 제외됨 검증" 단계 명시

**제안 이유**  
알고리즘 설계서에서 NE List 변경 동작 명시 (Line 3-4)

**상세 근거**  
SVR26A_COM_overshooting_algorithm_design.docx

**근거 상태**  
근거로 확인됨

---

## 📊 검토 요약

| 항목 | 내용 |
|------|------|
| **총 변경 제안** | 10 건 |
| **승인** | 10 건 |
| **수정후승인** | 0 건 |
| **거절** | 0 건 |
| **보류** | 0 건 |
| **P1 (필수 확인)** | 3 건 - CHG-001, CHG-002, CHG-003 |
| **P2 (주요 보완)** | 5 건 - CHG-004, CHG-005, CHG-006, CHG-007, CHG-010 |
| **P3 (개선 제안)** | 2 건 - CHG-008, CHG-009 |

---

## 📝 변경 이력 (Change History)

### 🔴 CHG-001 | P1 | Precondition A.2 | **승인**

**발견 내용:**
NE List 에 대한 구체적 정의 누락

**AI 제안:**
"NE List 는 Type 1 과 Type 2 로 구분되며, Type 1 은 CM/PM 관리 대상, Type 2 는 최적화 적용 대상임을 명시" 추가

**최종 반영 내용:**
"NE List 는 Type 1 과 Type 2 로 구분되며, Type 1 은 CM/PM 관리 대상, Type 2 는 최적화 적용 대상임을 명시" 추가

**근거 상태:** 근거로 확인됨

---

### 🔴 CHG-002 | P1 | Test Procedure B.1 | **승인**

**발견 내용:**
VISTA 로부터 수신하는 정보의 구체적 항목 누락

**AI 제안:**
"NE List, Network Freeze information, Sector exclusion cell list, Dynamic sector list" 각 항목에 대한 구체적 데이터 포맷 명시

**최종 반영 내용:**
"NE List, Network Freeze information, Sector exclusion cell list, Dynamic sector list" 각 항목에 대한 구체적 데이터 포맷 명시

**근거 상태:** 근거로 확인됨

---

### 🔴 CHG-003 | P1 | Pass/Fail Criteria C | **승인**

**발견 내용:**
Pass/Fail 기준이 모호함 ("normally", "should be able to")

**AI 제안:**
구체적 검증 항목 추가: "1) Type 2 NE List 가 Type 1 NE List 기반으로 올바르게 구성되었는지 확인. 2) Exclusion list 에 포함된 NE 가 Type 2 에서 제외되었는지 확인"

**최종 반영 내용:**
구체적 검증 항목 추가: "1) Type 2 NE List 가 Type 1 NE List 기반으로 올바르게 구성되었는지 확인. 2) Exclusion list 에 포함된 NE 가 Type 2 에서 제외되었는지 확인"

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-004 | P2 | Test Procedure B.1 | **승인**

**발견 내용:**
Cluster 별 Optimization period 설정 방법 미명시

**AI 제안:**
"Operator 가 VISTA UI 를 통해 cluster 별 optimization period 를 설정하는 단계" 추가

**최종 반영 내용:**
"Operator 가 VISTA UI 를 통해 cluster 별 optimization period 를 설정하는 단계" 추가

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-005 | P2 | Precondition A.2 | **승인**

**발견 내용:**
Frequency 조합 조건 누락

**AI 제안:**
"File containing information for Overshooting Detection and Resolution provides different combinations for different Carrier frequency" 조건에 대한 구체적 예시 추가 (예: f1=ON/f2=OFF 등)

**최종 반영 내용:**
"File containing information for Overshooting Detection and Resolution provides different combinations for different Carrier frequency" 조건에 대한 구체적 예시 추가 (예: f1=ON/f2=OFF 등)

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-006 | P2 | Test Procedure B.1 | **승인**

**발견 내용:**
ESM operation time 고려사항 누락

**AI 제안:**
"ESM operation time 을 고려하여 PM counter 수집 제외 시간 (exceptionPMcollectionTime) 을 관리하는지 확인" 단계 추가

**최종 반영 내용:**
"ESM operation time 을 고려하여 PM counter 수집 제외 시간 (exceptionPMcollectionTime) 을 관리하는지 확인" 단계 추가

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-007 | P2 | Test Procedure B.1 | **승인**

**발견 내용:**
Cell-RET mapping 검증 단계 누락

**AI 제안:**
"RET information mapping 이 올바르게 되었는지 확인 (o-ran-ru-id, antenna-line-device-id, antenna-id)" 단계 추가

**최종 반영 내용:**
"RET information mapping 이 올바르게 되었는지 확인 (o-ran-ru-id, antenna-line-device-id, antenna-id)" 단계 추가

**근거 상태:** 근거로 확인됨

---

### 🟢 CHG-008 | P3 | Test Overview | **승인**

**발견 내용:**
Test Purpose 에 "Overshooting Cell Detection and Resolution algorithm" 언급 but Test Overview 에는 COM operation 만

**AI 제안:**
Test Overview 에 "Overshooting Cell Detection 과 Resolution 알고리즘 검증 포함" 명시화

**최종 반영 내용:**
Test Overview 에 "Overshooting Cell Detection 과 Resolution 알고리즘 검증 포함" 명시화

**근거 상태:** 보완 제안

---

### 🟢 CHG-009 | P3 | Precondition A.1 | **승인**

**발견 내용:**
"Statistics items must be collected during comResolutionPeriod" - 구체적 statistics 항목 누락

**AI 제안:**
수집해야 할 PM counter 항목 목록 추가 (Availability, Timing Advance, Air MAC Packet 등)

**최종 반영 내용:**
수집해야 할 PM counter 항목 목록 추가 (Availability, Timing Advance, Air MAC Packet 등)

**근거 상태:** 근거로 확인됨

---

### 🟡 CHG-010 | P2 | Test Procedure B.1 | **승인**

**발견 내용:**
NE List 변경 시나리오 (추가/삭제) 검증 단계 구체화 필요

**AI 제안:**
"NE List 추가 시: 다음 cycle 에 포함됨 검증. NE List 삭제 시: 즉시 제외됨 검증" 단계 명시

**최종 반영 내용:**
"NE List 추가 시: 다음 cycle 에 포함됨 검증. NE List 삭제 시: 즉시 제외됨 검증" 단계 명시

**근거 상태:** 근거로 확인됨

---

## 📊 Evidence Summary

### 요구사항 매핑

| FR13 요구사항 | TC 반영 여부 | 검증 Step |
|---------------|--------------|-----------|
| NE List | ✅ 반영됨 | Precondition A.2, Test Procedure B.1 |
| Network Freeze information | ✅ 반영됨 | Test Procedure B.1 |
| Sector exclusion cell list | ✅ 반영됨 | Precondition A.2, Test Procedure B.1 |
| Dynamic sector list | ✅ 반영됨 | Test Procedure B.1 |

### Gotcha Checkpoint 적용 결과

| Gotcha ID | 과거 문제 | 현재 TC 적용 여부 |
|-----------|----------|------------------|
| GOTCHA-003 | TC coverage 부족 (주파수 조합) | ✅ CHG-005 에서 반영 |
| GOTCHA-004 | Pass/Fail Criteria 모호함 | ✅ CHG-003 에서 반영 |

---

**최종 상태**: FINAL (모든 Change ID 결정 완료, P1 보류 없음)  
**검토자**: Reviewer  
**승인일**: 2026-07-27
