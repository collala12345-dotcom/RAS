# Test Case: TC-COM-001

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
