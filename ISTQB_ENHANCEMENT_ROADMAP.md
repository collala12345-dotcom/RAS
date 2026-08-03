# ISTQB 기반 RAG 시스템 고도화 로드맵

> **문서 작성일**: 2026-07-14  
> **버전**: 1.0  
> **기준**: ISTQB CTFL v4.0.1

---

## 📋 개요

본 문서는 ISTQB CTFL 파운데이션 레벨 실러버스 v4.0.1 을 기반으로 RAG 기반 TC 검증·보완 시스템을 3 단계로 고도화하는 로드맵을 제시합니다.

---

## 🎯 구현 완료된 모듈

### 1 단계: 자동화 체크리스트 (MVP+) ✅

| 모듈 | 파일 | 상태 |
|------|------|------|
| **ISTQB Validator** | `src/tc_reviewer/istqb_validator.py` | ✅ 완료 |
| **Technique Recommender** | `src/tc_reviewer/technique_recommender.py` | ✅ 완료 |
| **Risk Prioritizer** | `src/tc_reviewer/risk_prioritizer.py` | ✅ 완료 |

### 구현된 기능

#### 1. ISTQB Validator (57 개 검증 항목)

```python
from src.tc_reviewer.istqb_validator import validate_tc

result = validate_tc(tc_content, {
    "tc_id": "TC_001",
    "fr_id": "FR-COM-001",
    "rapp": "COM"
})

print(f"Overall Score: {result.overall_score}")
print(f"Risk Level: {result.risk_level}")
print(f"Recommendation: {result.decision_recommendation}")
```

**검증 카테고리 (13 개):**
1. Requirement Coverage (RC-1 ~ RC-4)
2. Scenario Completeness (SC-1 ~ SC-6)
3. Procedure Clarity (PC-1 ~ PC-5)
4. Pass/Fail Clarity (PF-1 ~ PF-4)
5. Data/Configuration Consistency (DC-1 ~ DC-4)
6. Evidence Traceability (ET-1 ~ ET-3)
7. Field Issue Awareness (FI-1 ~ FI-2)
8. **Test Level Validation (TL-1 ~ TL-5)** ← ISTQB 추가
9. **Test Type Validation (TT-1 ~ TT-4)** ← ISTQB 추가
10. **Test Technique Validation (TE-BB-1 ~ TE-EB-3)** ← ISTQB 추가
11. **Static Testing Validation (ST-1 ~ ST-4)** ← ISTQB 추가
12. **Risk-Based Testing (RB-1 ~ RB-4)** ← ISTQB 추가
13. **Pass/Fail SMART Validation (PF-SMART-1 ~ PF-SMART-5)** ← ISTQB 추가

#### 2. Technique Recommender (테스트 기법 자동 추천)

```python
from src.tc_reviewer.technique_recommender import recommend_techniques

rec_result = recommend_techniques(validation_result, {"rapp": "COM"})

for rec in rec_result.recommendations:
    print(f"[{rec.priority}] {rec.technique_name}")
    print(f"  Reason: {rec.reason}")
    print(f"  Guide: {rec.application_guide}")
```

**추천 기법:**
- **Black-Box**: EP, BVA, Decision Table, State Transition
- **White-Box**: Statement Coverage, Branch Coverage
- **Experience-Based**: Error Guessing, Exploratory, Checklist

**자동 생성 시나리오:**
- 경계값 테스트 시나리오 (MIN-1, MIN, MIN+1, MAX-1, MAX, MAX+1)
- 조합 테스트 시나리오 (ON-ON, ON-OFF, OFF-ON, OFF-OFF)
- 상태 전이 시나리오 (Initial → Active → Done → Error → Recovery)
- 오류 추정 시나리오 (Null, Timeout, Invalid, Concurrent)

#### 3. Risk Prioritizer (리스크 기반 우선순위)

```python
from src.tc_reviewer.risk_prioritizer import assess_risk

risk_result = assess_risk(tc_metadata, historical_data)

print(f"Risk Level: {risk_result.risk_level}")
print(f"Test Priority: {risk_result.test_priority}/100")
print(f"Top Risks: {[f.factor_name for f in risk_result.risk_factors[:3]]}")
```

**리스크 카테고리:**
- **Product Risk**: 기능 중요도, 사용자 영향, 안전/보안, 수익 영향
- **Project Risk**: 일정 압박, 자원 가용성, 요구사항 안정성, 팀 경험
- **Technical Risk**: 복잡도, 통합 포인트, 기술 신규성, 테스트 커버리지 갭
- **Historical Risk**: 과거 이슈 빈도, 현장 문제 이력, 회귀 리스크, 유사 기능 이슈

**rAPP 별 Risk Modifier:**
- COM: base_risk=0.6, critical_features=[overshooting, coverage_hole, tilt_control]
- ESM: base_risk=0.5, critical_features=[energy_saving, sleep_mode]
- LBM: base_risk=0.5, critical_features=[load_balancing, handover]

---

## 📋 1 단계: 즉시 구현 (완료)

### 1.1 ISTQB 검증 엔진 ✅

**위치**: `src/tc_reviewer/istqb_validator.py`

**기능**:
- 57 개 체크리스트 자동 검증
- Pass/Warning/Issue 3 단계 판정
- 카테고리별 Score 계산
- Risk Level 및 Decision Recommendation 생성

**통합 방법**:
```python
# 기존 TC reviewer 에 통합
from src.tc_reviewer.istqb_validator import validate_tc

def review_tc(tc_content: str, metadata: dict) -> dict:
    # 기존 로직...
    
    # ISTQB 검증 추가
    istqb_result = validate_tc(tc_content, metadata)
    
    return {
        "tc_content": enhanced_tc,
        "quality_score": istqb_result.overall_score,
        "risk_level": istqb_result.risk_level,
        "findings": istqb_result.findings,
    }
```

### 1.2 Quality Report 템플릿 업데이트

**위치**: `references/04_quality_rubric.md` (업데이트 필요)

**추가할 섹션**:
```markdown
## ISTQB Analysis

### Test Level Coverage
- Component: Pass/Warning/Issue
- Integration: Pass/Warning/Issue
- System: Pass/Warning/Issue
- Acceptance: Pass/Warning/Issue

### Test Technique Coverage
- Black-Box Techniques: XX%
  - Equivalence Partitioning: Pass/Warning/Issue
  - Boundary Value Analysis: Pass/Warning/Issue
  - Decision Table: Pass/Warning/Issue
  - State Transition: Pass/Warning/Issue
- White-Box Techniques: XX%
- Experience-Based Techniques: XX%

### Risk-Based Testing
- Product Risk Score: X.XX
- Project Risk Score: X.XX
- Technical Risk Score: X.XX
- Historical Risk Score: X.XX
- Overall Risk Level: High/Medium/Low
```

### 1.3 RAG 검색 쿼리 확장

**위치**: `scripts/search_evidence.py` (업데이트 필요)

**추가할 검색 키워드**:
```python
ISTQB_KEYWORDS = {
    # Test Techniques
    "boundary_value": ["boundary", "edge", "min", "max", "corner"],
    "equivalence_partition": ["partition", "equivalence", "class"],
    "decision_table": ["combination", "decision", "truth table"],
    "state_transition": ["state", "transition", "mode change"],
    
    # Test Levels
    "integration": ["interface", "integration", "connect"],
    "system": ["end-to-end", "E2E", "full flow"],
    
    # Risk
    "risk": ["risk", "critical", "hazard", "severity"],
    "mitigation": ["mitigate", "prevent", "avoid"],
}

def expand_query_with_istqb(base_query: str) -> list[str]:
    """ISTQB keywords로 검색 쿼리 확장"""
    expanded = [base_query]
    
    for technique, keywords in ISTQB_KEYWORDS.items():
        if any(kw in base_query.lower() for kw in keywords):
            # 관련 키워드로 추가 검색
            expanded.append(f"{base_query} {technique}")
    
    return expanded
```

---

## 📋 2 단계: 중기 발전 (Smart Review)

### 2.1 테스트 기법 자동 추천 엔진 ✅

**위치**: `src/tc_reviewer/technique_recommender.py`

**기능**:
- 검증 결과 기반 자동 추천
- High/Medium/Low 우선순위
- 적용 가이드 및 예시 제공
- 자동 시나리오 템플릿 생성

**통합 예시**:
```python
from src.tc_reviewer.technique_recommender import recommend_techniques

def enhance_tc_with_techniques(tc_content: str, metadata: dict) -> str:
    # 1. ISTQB 검증
    validation = validate_tc(tc_content, metadata)
    
    # 2. 기법 추천
    recommendations = recommend_techniques(validation, metadata)
    
    # 3. High 우선순위 기법으로 시나리오 생성
    for rec in recommendations.recommendations:
        if rec.priority == "High":
            # TC 에 시나리오 추가
            tc_content = add_scenario(tc_content, rec.example_scenario)
    
    return tc_content
```

### 2.2 리스크 기반 TC 우선순위 산정 ✅

**위치**: `src/tc_reviewer/risk_prioritizer.py`

**기능**:
- 4 가지 리스크 카테고리 평가
- rAPP 별 Risk Modifier 적용
- Test Priority (1-100) 계산
- Risk Mitigation 권고사항 생성

**활용 시나리오**:
```python
# 다중 FR 검토 시 우선순위 정렬
from src.tc_reviewer.risk_prioritizer import assess_risk

fr_list = [...]  # 여러 FR metadata

# 리스크 평가
risk_results = []
for fr in fr_list:
    risk = assess_risk(fr, historical_data)
    risk_results.append((fr, risk))

# 우선순위 정렬 (High Risk 먼저)
sorted_results = sorted(risk_results, key=lambda x: x[1].test_priority, reverse=True)

# High Risk FR 부터 검토
for fr, risk in sorted_results:
    if risk.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
        print(f"우선 검토 필요: {fr['fr_id']} (Priority: {risk.test_priority})")
```

### 2.3 rAPP 별 ISTQB 가중치 프로파일

**위치**: `references/` 새 파일 생성 예정
**파일명**: `09_rapp_istqb_profiles.json`

```json
{
  "COM": {
    "name": "Coverage Optimization Manager",
    "critical_techniques": ["TE-BB-2", "TE-BB-3", "TE-BB-4"],
    "weights": {
      "boundary_value": 1.5,
      "decision_table": 1.3,
      "state_transition": 1.2
    },
    "critical_features": ["overshooting", "coverage_hole", "tilt_control"],
    "checklist_overrides": {
      "SC-3": {"weight": 1.5},
      "SC-5": {"weight": 1.3}
    }
  },
  "ESM": {
    "name": "Energy Save Manager",
    "critical_techniques": ["TE-BB-4", "TE-EB-1"],
    "weights": {
      "state_transition": 1.5,
      "error_guessing": 1.3
    },
    "critical_features": ["energy_saving", "sleep_mode", "power_control"]
  },
  "LBM": {
    "name": "Load Balancing Manager",
    "critical_techniques": ["TE-BB-3", "TE-BB-4"],
    "weights": {
      "decision_table": 1.4,
      "state_transition": 1.3
    },
    "critical_features": ["load_balancing", "handover", "traffic_distribution"]
  }
}
```

**활용 방법**:
```python
import json

def load_rapp_profile(rapp: str) -> dict:
    with open("references/09_rapp_istqb_profiles.json") as f:
        profiles = json.load(f)
    return profiles.get(rapp, profiles["default"])

def apply_rapp_weights(validation_result, profile: dict):
    """rAPP 프로파일에 따라 검증 항목 가중치 조정"""
    for override_id, override in profile.get("checklist_overrides", {}).items():
        # 해당 체크항목 가중치 조정
        weight = override.get("weight", 1.0)
        # ... 가중치 적용 로직
```

---

## 📋 3 단계: 장기 비전 (AI Test Architect)

### 3.1 Closed-Loop 자동화 설계

**아키텍처**:
```
[FR/HLD/DLD] 
    ↓
[TC v1 생성] ← Cline/Harness Skill
    ↓
[ISTQB Validator] ← 57 개 항목 검증
    ↓              ↓
[Quality Report] ← [RAG Search] ← 과거 이슈/TC/Test Result
    ↓              ↓
[Technique Recommender] ← 누락 기법 추천
    ↓
[Risk Prioritizer] ← 리스크 평가
    ↓
[TC v2 자동 보완] ← 시나리오 추가/수정
    ↓
[Human Review] ← High Risk 항목 중심 검토
    ↓
[최종 TC 승인]
    ↓
[학습 데이터로 환류] ← RAG VectorDB 업데이트
```

**구현 파일**:
- `src/tc_reviewer/closed_loop_engine.py` (신규)

### 3.2 ISTQB 교육 콘텐츠 연동

**기능**:
- TC 검토 시 ISTQB 용어 설명 제공
- 관련 학습 자료 링크
- 조직 내 테스트 역량 향상

**예시 출력**:
```
[ISTQB Learning Tip]
검증 항목: TE-BB-2 (Boundary Value Analysis)

📚 용어 설명:
경계값 분석 (BVA) 은 입력/출력 도메인의 경계값을 테스트하는 기법입니다.
오류는 주로 경계에서 발생하므로, min, max, min-1, max+1 등을 테스트합니다.

📖 관련 자료:
- ISTQB CTFL Syllabus v4.0.1 Chapter 4.2.2
- 삼성네트워크 TC 작성 가이드 Section 3.2
- 사내 교육: "효과적인 테스트 설계 기법" Module 2

💡 적용 예시:
입력: Threshold (0-100)
테스트 값: -1, 0, 1, 99, 100, 101
```

**구현 파일**:
- `references/istqb_glossary.md` (신규)
- `src/tc_reviewer/learning_linker.py` (신규)

### 3.3 품질 예측 모델

**기능**:
- 과거 TC 데이터 학습
- Field Issue 발생 확률 예측
- TC 품질 점수와 실제 Field Fail 상관관계 분석

**데이터 수집**:
```python
# 수집할 데이터
training_data = {
    "tc_id": "TC_001",
    "istqb_scores": {
        "overall": 75.5,
        "requirement_coverage": 80.0,
        "scenario_completeness": 70.0,
        # ...
    },
    "technique_coverage": {
        "BVA": True,
        "EP": True,
        "DecisionTable": False,
        # ...
    },
    "risk_level": "Medium",
    "field_issue_occurred": False,
    "days_to_issue": None,
}
```

**예측 모델**:
```python
from sklearn.ensemble import RandomForestClassifier

class TcQualityPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
    
    def train(self, historical_data: list[dict]):
        """과거 TC 데이터로 학습"""
        X = self._extract_features(historical_data)
        y = self._extract_labels(historical_data)
        self.model.fit(X, y)
    
    def predict_field_fail_probability(self, tc_result: ValidationResult) -> float:
        """TC 검증 결과로 Field Fail 확률 예측"""
        features = self._extract_features_from_result(tc_result)
        proba = self.model.predict_proba([features])[0]
        return proba[1]  # Fail 확률
    
    def _extract_features(self, data: list[dict]) -> list[list[float]]:
        """특징 추출"""
        # ... 구현
```

**구현 파일**:
- `src/tc_reviewer/quality_predictor.py` (신규)

---

## 📊 통합 API 설계

### 통합 엔트리 포인트

```python
# src/tc_reviewer/enhancement_engine.py

from typing import Any
from .istqb_validator import validate_tc, ValidationResult
from .technique_recommender import recommend_techniques, RecommendationResult
from .risk_prioritizer import assess_risk, RiskAssessment


class TCEnhancementEngine:
    """
    통합 TC Enhancement Engine
    
    ISTQB 검증, 기법 추천, 리스크 평가를 하나의 파이프라인으로 실행
    """
    
    def __init__(self, historical_data: dict[str, Any] | None = None):
        self.historical_data = historical_data or {}
    
    def enhance(self, tc_content: str, metadata: dict[str, Any]) -> dict[str, Any]:
        """
        TC Enhancement 파이프라인 실행
        
        Args:
            tc_content: TC 내용 (Markdown)
            metadata: TC 메타데이터 (fr_id, rapp, feature 등)
        
        Returns:
            통합 결과 딕셔너리
        """
        # 1. ISTQB 검증
        validation_result = validate_tc(tc_content, metadata)
        
        # 2. 기법 추천
        technique_result = recommend_techniques(validation_result, metadata)
        
        # 3. 리스크 평가
        risk_result = assess_risk(metadata, self.historical_data)
        
        # 4. 결과 통합
        return {
            "tc_id": metadata.get("tc_id", "Unknown"),
            "validation": {
                "overall_score": validation_result.overall_score,
                "risk_level": validation_result.risk_level,
                "recommendation": validation_result.decision_recommendation,
                "category_scores": validation_result.category_scores,
                "findings": [
                    {
                        "check_id": f.check_id,
                        "name": f.check_name,
                        "verdict": f.verdict.value,
                        "suggestion": f.suggestion,
                    }
                    for f in validation_result.findings
                ],
            },
            "techniques": {
                "current_coverage": technique_result.current_coverage,
                "expected_coverage": technique_result.expected_coverage_after,
                "improvement": technique_result.coverage_improvement,
                "recommendations": [
                    {
                        "technique_id": r.technique_id,
                        "name": r.technique_name,
                        "priority": r.priority,
                        "reason": r.reason,
                        "guide": r.application_guide,
                    }
                    for r in technique_result.recommendations
                ],
                "generated_scenarios": technique_result.generated_scenarios,
            },
            "risk": {
                "overall_score": risk_result.overall_risk_score,
                "risk_level": risk_result.risk_level.value,
                "test_priority": risk_result.test_priority,
                "category_scores": {
                    "product": risk_result.product_risk_score,
                    "project": risk_result.project_risk_score,
                    "technical": risk_result.technical_risk_score,
                    "historical": risk_result.historical_risk_score,
                },
                "recommended_actions": risk_result.recommended_actions,
            },
        }


# 편의 함수
def enhance_tc(
    tc_content: str,
    metadata: dict[str, Any],
    historical_data: dict[str, Any] | None = None
) -> dict[str, Any]:
    """TC Enhancement 원샷 실행"""
    engine = TCEnhancementEngine(historical_data)
    return engine.enhance(tc_content, metadata)
```

---

## 🚀 마이그레이션 가이드

### 기존 파이프라인 통합

**기존 코드** (`scripts/run_full_pipeline.py`):
```python
# 기존 로직...
tc_v1 = generate_tc_v1(fr_docs)
tc_v2 = enhance_tc(tc_v1, rag_results)
save_output(tc_v2)
```

**업그레이드**:
```python
from src.tc_reviewer.enhancement_engine import enhance_tc

# 기존 로직...
tc_v1 = generate_tc_v1(fr_docs)

# ISTQB Enhancement 추가
enhancement_result = enhance_tc(
    tc_v1,
    metadata={
        "tc_id": "TC_001",
        "fr_id": "FR-COM-001",
        "rapp": "COM",
        "feature": "overshooting_detection",
    },
    historical_data=load_historical_data()
)

# 결과 활용
print(f"Quality Score: {enhancement_result['validation']['overall_score']}")
print(f"Risk Level: {enhancement_result['risk']['risk_level']}")

# 자동 보완
tc_v2 = apply_recommendations(tc_v1, enhancement_result['techniques']['recommendations'])
save_output(tc_v2)
```

---

## 📈 기대 효과

| 지표 | 현재 | 1 단계 후 | 2 단계 후 | 3 단계 후 |
|------|------|----------|----------|----------|
| 검증 항목 수 | ~10 | 57 | 57 + 자동추천 | 57 + 예측 |
| 검토 시간 | 100% | 50% | 30% | 20% |
| TC 품질 Score | - | 70+ | 80+ | 85+ |
| Field Issue 감소 | - | 20% | 40% | 60% |
| 시나리오 커버리지 | - | 75% | 85% | 90%+ |

---

## 📝 다음 단계

1. **즉시 실행**: `istqb_validator.py` 테스트 및 기존 파이프라인 통합
2. **1 주 내**: Quality Report 템플릿 업데이트
3. **2 주 내**: RAG 검색 쿼리 확장 구현
4. **1 개월 내**: rAPP 별 프로파일 정의 및 적용
5. **3 개월 내**: Closed-Loop 엔진 구현
6. **6 개월 내**: 품질 예측 모델 학습 및 배포

---

**문서 관리**: RAS-TestCaseReview Team  
**최종 업데이트**: 2026-07-14
