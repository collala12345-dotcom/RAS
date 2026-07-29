# 01. Gotchas - 과거 상용/현장 문제 패턴

> **Purpose**: 과거 상용화/현장에서 발생한 문제 패턴을 정리하여, 향후 TC Review 시 유사 문제를 탐지하고 보완합니다.

---

## 📋 Gotcha 목록

| ID | rAPP | 문제 유형 | 제목 |
|----|------|----------|------|
| GOTCHA-001 | ESM | 알고리즘/구조설계 누락 | TS2650L5 |
| GOTCHA-002 | ESM | TC 부재 | TS26409J |
| GOTCHA-003 | ESM | TC coverage 부족 | TS2610H1 |
| GOTCHA-004 | ESM | TC coverage 부족 | TS26202E |

---

## GOTCHA-001: 알고리즘/구조설계 누락 (ESM)

### 기본 정보
- **Ticket ID**: TS2650L5
- **rAPP**: ESM (Energy Saving Management)
- **문제 유형**: 알고리즘/구조설계 누락
- **출처**: `ESM 문제점 포스트모텀_202629.pptx, Slide 3`

### 발생 상황
ESM SW 개발 과정에서 알고리즘 로직과 구조 설계가 누락됨.

### 문제 내용
- 설계 문서에 알고리즘 상세 로직이 명시되지 않음
- 구조 설계가 불완전하여 구현 시 일관성 부족 발생

### 일반화된 Pattern
> **핵심**: "알고리즘/구조 설계 누락 → 구현 불일치 → 상용화 후 오류"

### 적용 가능 rAPP/시나리오
- **COM**: Overshooting Detection/Resolution 알고리즘 상세 로직 누락
- **ES**: Energy Saving Switch 제어 로직 누락
- **PM**: Prediction Model 학습/적용 파이프라인 누락

### TC Review Checkpoint
- [ ] 알고리즘 상세 로직이 설계서에 명시되어 있는가?
- [ ] 구조 설계가 구현 코드와 일치하는가?
- [ ] 예외 상황 (edge case) 에 대한 처리 로직이 있는가?
- [ ] 알고리즘 입력/출력 조건이 명확히 정의되어 있는가?

---

## GOTCHA-002: TC 부재 (ESM)

### 기본 정보
- **Ticket ID**: TS26409J
- **rAPP**: ESM
- **문제 유형**: TC 부재
- **출처**: `ESM 문제점 포스트모텀_202629.pptx, Slide 7`

### 발생 상황
특정 기능/시나리오에 대한 Test Case 가 존재하지 않음.

### 문제 내용
- 검증할 TC 가 없어 상용화 전까지 문제 미발견
- 현장 이슈 발생 후 사후 대응

### 일반화된 Pattern
> **핵심**: "TC 부재 → 검증 불가 → 상용화 후 현장 이슈"

### 적용 가능 rAPP/시나리오
- **COM**: Frequency 별 Switch OFF 시나리오 TC 부재
- **ES**: Night Time Energy Saving 모드 TC 부재
- **PM**: Model Retraining 실패 시나리오 TC 부재

### TC Review Checkpoint
- [ ] 모든 FR 요구사항에 대응하는 TC 가 존재하는가?
- [ ] Positive/Negative 시나리오 모두 검증되는가?
- [ ] Boundary condition (임계값) 검증 TC 가 있는가?
- [ ] Exception handling (예외 처리) 검증 TC 가 있는가?

---

## GOTCHA-003: TC coverage 부족 (ESM)

### 기본 정보
- **Ticket ID**: TS2610H1
- **rAPP**: ESM
- **문제 유형**: TC coverage 부족으로 인한 미검출
- **출처**: `ESM 문제점 포스트모텀_202629.pptx, Slide 8`

### 발생 상황
TC 는 존재하나 검증 범위가 부족하여 문제를 찾아내지 못함.

### 문제 내용
- TC 가 일부 시나리오만 검증
- 복잡한 조합/연계 상황 검증 누락

### 일반화된 Pattern
> **핵심**: "TC coverage 부족 → 일부 시나리오만 검증 → 누락된 문제"

### 적용 가능 rAPP/시나리오
- **COM**: 주파수별 조합 (f1=ON/f2=OFF 등) 검증 누락
- **ES**: 시간대별/요일별 조합 검증 누락
- **PM**: Input data 품질별 (정상/이상) 검증 누락

### TC Review Checkpoint
- [ ] 모든 Switch 조합 (ON/OFF) 을 검증하는가?
- [ ] 모든 Frequency 조합을 검증하는가?
- [ ] 연계 rAPP 간 상호작용을 검증하는가?
- [ ] 시간/주기 관련 조건을 모두 검증하는가?

---

## GOTCHA-004: TC coverage 부족 (ESM)

### 기본 정보
- **Ticket ID**: TS26202E
- **rAPP**: ESM
- **문제 유형**: TC coverage 부족으로 인한 미검출
- **출처**: `ESM 문제점 포스트모텀_202629.pptx, Slide 9`

### 발생 상황
TC coverage 가 부족하여 중요한 시나리오를 검증하지 못함.

### 문제 내용
- Precondition 검증 누락
- Pass/Fail Criteria 가 모호함

### 일반화된 Pattern
> **핵심**: "TC coverage 부족 → Preconditions/P/F Criteria 누락 → 불완전 검증"

### 적용 가능 rAPP/시나리오
- **COM**: NE List 업데이트 precondition 검증 누락
- **ES**: Energy Saving 활성화 조건 검증 누락
- **PM**: Model accuracy 임계값 검증 누락

### TC Review Checkpoint
- [ ] 모든 Precondition 이 명시되고 검증되는가?
- [ ] Pass/Fail Criteria 가 측정 가능한가?
- [ ] Expected Result 가 구체적인가?
- [ ] Actual Result 확인 방법이 명시되어 있는가?

---

## 🔍 KDDI SVR25A 출하 후 문제점 (추가 Gotcha)

### Ticket ID: TS25A0BL, TS25C013, NONE, TS25A0AZ

**출처**: `ESM 문제점 포스트모텀_202629.pptx, Slide 22-25`

KDDI SVR25A 출하 후 발견된 문제들:
- **TS25A0BL**: 출하 후 현장 이슈
- **TS25C013**: 출하 후 현장 이슈
- **NONE**: Ticket ID 없음 (미등록 이슈)
- **TS25A0AZ**: 출하 후 현장 이슈

### 교훈
> **핵심**: "출하 후 문제 = TC 검증 누락 또는 coverage 부족"

### TC Review Checkpoint
- [ ] 출하 전 모든 FR 요구사항을 검증했는가?
- [ ] 현장 사용 환경을 반영한 TC 가 있는가?
- [ ] Operator 설정 (VISTA UI 등) 관련 검증이 있는가?
- [ ] 장기간 운영 시나리오 (Periodic operation) 검증이 있는가?

---

## 📚 Gotcha 활용 가이드

### TC Review 시 Gotcha 참조 방법

1. **Review Queue 생성 전**: `references/01_gotchas.md` 읽기
2. **유사 Gotcha 검색**: 현재 TC 의 rAPP/기능과 관련된 Gotcha 찾기
3. **Checkpoint 적용**: Gotcha 의 TC Review Checkpoint 를 현재 TC 에 적용
4. **누락 탐지**: Checkpoint 중 누락된 항목을 Change Proposal 로 생성

### Gotcha 추가 방법

새로운 상용/현장 문제를 발견하면:
1. PPTX/MD 파일로 문제 정리
2. AI 가 분석하여 일반화된 Pattern 추출
3. `references/01_gotchas.md` 에 추가
4. 다음 TC Review 시 자동 참조

---

**마지막 업데이트**: 2026-07-22  
**출처**: ESM 문제점 포스트모텀_202629.pptx (25 slides)
