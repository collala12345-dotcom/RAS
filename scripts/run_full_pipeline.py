#!/usr/bin/env python
"""
Full RAG TC Review Pipeline Runner

This script runs the complete TC Review pipeline:
1. Load/Verify JSONL data
2. Initialize Keyword Retriever
3. Generate TC v1 (if FR/HLD/DLD provided)
4. Review TC v1 with RAG
5. Refine to TC v2
6. Generate Quality Report

Usage:
    # Full pipeline with TC generation
    python scripts/run_full_pipeline.py --feature FGR-CC3101 --pkg SVR26A --rapp COM

    # Review existing TC
    python scripts/run_full_pipeline.py --tc-path output/enhanced_tc/TC_v1.md --feature FGR-COA-SR1.10 --pkg SVR26A
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_embedder.keyword_retriever import KeywordRetriever, KeywordRetrieverConfig
from tc_reviewer import ReviewConfig, ReviewEngine, RefinementEngine, Finding

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"output/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_persona_file():
    """Check and log AI Agent Persona file (Step 0)."""
    persona_path = Path(__file__).parent.parent / "references" / "09_ai_agent_persona.md"
    
    if persona_path.exists():
        logger.info("=" * 70)
        logger.info("Step 0: AI Agent Persona 확인")
        logger.info("=" * 70)
        logger.info(f"Persona file found: {persona_path}")
        logger.info("AI 에이전트는 이 문서를 먼저 읽고 TC Review 를 수행합니다.")
        logger.info("=" * 70)
    else:
        logger.warning(f"Persona file not found: {persona_path}")
        logger.warning("Creating default persona file...")
        
        # Create default persona file
        default_persona = """# AI Agent Persona for RAS-TestCaseReview

> 이 문서는 모든 AI 에이전트가 RAS-TestCaseReview 작업을 시작할 때 반드시 먼저 읽어야 할 핵심 지침서입니다.

## 당신의 정체성 (Identity)
당신은 RAS-TestCaseReview AI 에이전트입니다.

## 핵심 원칙 (6 가지)
1. 근거 기반 수정
2. 자동 보완
3. Human Review 명시
4. Core/Plugin 분리
5. Before/After 비교
6. RAG 연결

## 필수 선행 읽기
1. references/gotchas.md
2. RAS_Experience/RAS-gotchas.md
3. references/03_tc_validation_checklist.md
4. references/rapp_interoperability.json
"""
        
        with open(persona_path, "w", encoding="utf-8") as f:
            f.write(default_persona)
        
        logger.info(f"Created default persona file: {persona_path}")


def verify_jsonl_data(jsonl_dir: Path) -> dict:
    """Verify JSONL data availability."""
    logger.info(f"Verifying JSONL data in {jsonl_dir}")
    
    if not jsonl_dir.exists():
        logger.error(f"JSONL directory not found: {jsonl_dir}")
        return {"status": "error", "message": "JSONL directory not found"}
    
    jsonl_files = list(jsonl_dir.glob("*.jsonl"))
    
    # Count by doc_type
    doc_type_counts = {}
    for f in jsonl_files:
        # Extract doc_type from filename
        name = f.stem
        if "3gpp" in name.lower():
            doc_type = "3gpp_docs"
        elif "hld" in name.lower() or "dld" in name.lower():
            doc_type = "hld_dld"
        elif "algorithm" in name.lower():
            doc_type = "algorithm_docs"
        elif "tc" in name.lower() or "vvt" in name.lower():
            doc_type = "legacy_tc"
        else:
            doc_type = "other"
        
        doc_type_counts[doc_type] = doc_type_counts.get(doc_type, 0) + 1
    
    logger.info(f"Found {len(jsonl_files)} JSONL files")
    for dt, count in sorted(doc_type_counts.items()):
        logger.info(f"  - {dt}: {count} files")
    
    return {
        "status": "ok",
        "total_files": len(jsonl_files),
        "by_type": doc_type_counts
    }


def initialize_retriever(jsonl_dir: Path, index_file: Path) -> KeywordRetriever:
    """Initialize Keyword Retriever."""
    logger.info("Initializing Keyword Retriever...")
    
    config = KeywordRetrieverConfig(
        jsonl_dir=jsonl_dir,
        index_file=index_file,
        bm25_k1=1.5,
        bm25_b=0.75,
    )
    
    retriever = KeywordRetriever(config)
    
    # Try to load from cache first
    if retriever.load_from_cache():
        logger.info("Loaded Keyword Index from cache (fast!)")
    else:
        logger.info("Building Keyword Index from JSONL files...")
        retriever.load()
        logger.info("Keyword Index built and saved")
    
    stats = retriever.get_stats()
    logger.info(f"Index Statistics:")
    logger.info(f"  - Total chunks: {stats['total_chunks']}")
    logger.info(f"  - Vocabulary size: {stats['vocabulary_size']}")
    logger.info(f"  - Avg doc length: {stats['avg_doc_length']:.1f} words")
    
    return retriever


def generate_tc_v1(feature_id: str, sw_pkg: str, rapp: str, 
                   hld_path: Path = None, dld_path: Path = None,
                   algorithm_path: Path = None) -> str:
    """
    Generate TC v1 from FR/HLD/DLD.
    
    Note: This is a placeholder. In production, this would call
    the TC Generation Skill (like RAS-TestCaseCreation).
    """
    logger.info(f"Generating TC v1 for {feature_id}, {sw_pkg}, {rapp}")
    
    # TODO: Integrate with RAS-TestCaseCreation skill
    # For now, return a placeholder
    tc_v1_content = f"""# Test Case: {feature_id} - {sw_pkg}

## Test Overview
- Feature ID: {feature_id}
- SW Package: {sw_pkg}
- rAPP: {rapp}
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Test Purpose
TODO: Generate from FR/HLD/DLD

## Dependency & Limitation
TODO: Extract from HLD/DLD

## Precondition
TODO: Extract from HLD/DLD

## Test Procedure
TODO: Generate from Functional Design

## Pass/Fail Criteria
TODO: Define measurable criteria
"""
    
    logger.warning("TC v1 generation is a placeholder. Integrate with RAS-TestCaseCreation skill for full automation.")
    
    return tc_v1_content


def review_tc(tc_v1_content: str, feature_id: str, sw_pkg: str, 
              rapp: str, retriever: KeywordRetriever) -> tuple:
    """
    Review TC v1 using RAG with integrated ISTQB validation and Multi-FR review.
    
    Returns:
        Tuple of (ReviewResult, evidence_list)
    """
    logger.info("Starting TC Review with RAG...")
    
    # Create temp TC v1 file
    output_dir = Path("output/enhanced_tc")
    output_dir.mkdir(parents=True, exist_ok=True)
    tc_v1_path = output_dir / f"{feature_id}_{sw_pkg}_tc_v1_temp.md"
    
    with open(tc_v1_path, "w", encoding="utf-8") as f:
        f.write(tc_v1_content)
    
    # Create review config
    config = ReviewConfig(
        tc_v1_path=tc_v1_path,
        feature_id=feature_id,
        sw_package=sw_pkg,
        rapp_name=rapp,
        search_keywords=[],
        vectordb_path=Path("data/processed/vectordb"),
        output_dir=Path("output/quality_reports"),
    )
    
    # Create review engine
    review_engine = ReviewEngine(config)
    
    # Build requirements based on rAPP and feature
    mock_requirements = build_requirements_for_review(feature_id, rapp)
    
    # Retrieve evidence using our retriever
    logger.info("Retrieving evidence with Keyword Retriever...")
    evidence_list = review_engine._retrieve_evidence(mock_requirements)
    logger.info(f"Retrieved {len(evidence_list)} pieces of evidence")
    
    # Run review (now includes ISTQB validation internally)
    logger.info("Running TC review with ISTQB validation...")
    review_result = review_engine.run()
    
    # Additional Multi-FR review if dependency graph exists
    dependency_graph_path = Path("references/com_fr_dependency.json")
    if dependency_graph_path.exists() and rapp == "COM":
        logger.info("Running Multi-FR review...")
        try:
            from tc_reviewer.multi_fr_reviewer import MultiFRReviewer
            
            multi_fr_reviewer = MultiFRReviewer(dependency_graph_path)
            feature_list = extract_fr_ids_from_tc(tc_v1_content)
            
            if feature_list:
                multi_fr_result = multi_fr_reviewer.review(tc_v1_path, feature_list)
                logger.info(f"Multi-FR Review completed: Quality={multi_fr_result.quality_score:.1f}")
                
                # Add Multi-FR findings to review result
                for finding in multi_fr_result.findings:
                    review_result.findings.append(Finding(
                        category=finding.category,
                        check_id=finding.check_id,
                        severity=finding.severity,
                        description=finding.description,
                        tc_section=finding.tc_section,
                        evidence_status=finding.evidence_status,
                        human_review_required=False,
                    ))
        except Exception as e:
            logger.warning(f"Multi-FR review skipped: {e}")
    
    logger.info(f"Review completed:")
    logger.info(f"  - Quality Score: {review_result.quality_score}")
    logger.info(f"  - Risk Level: {review_result.risk_level}")
    logger.info(f"  - Decision: {review_result.decision}")
    logger.info(f"  - Missing Scenarios: {len(review_result.missing_scenarios)}")
    logger.info(f"  - Total Findings: {len(review_result.findings)}")
    
    return review_result, evidence_list


def build_requirements_for_review(feature_id: str, rapp: str) -> list[dict]:
    """
    Build search requirements based on feature and rAPP.
    
    Args:
        feature_id: Feature ID (e.g., FGR-CC3101)
        rapp: rAPP name (e.g., COM)
    
    Returns:
        List of requirement dicts for evidence retrieval
    """
    requirements = []
    
    # Base requirements for all features
    requirements.extend([
        {"keyword": f"{rapp} detection", "doc_type": None, "feature_area": "detection", "rapp": rapp},
        {"keyword": f"{rapp} resolution", "doc_type": None, "feature_area": "resolution", "rapp": rapp},
        {"keyword": "threshold KPI", "doc_type": None, "feature_area": "KPI", "rapp": rapp},
        {"keyword": "algorithm", "doc_type": "algorithm_docs", "feature_area": "algorithm", "rapp": rapp},
    ])
    
    # COM rAPP specific requirements
    if rapp == "COM":
        requirements.extend([
            {"keyword": "overshooting", "doc_type": "algorithm_docs", "feature_area": "Overshooting", "rapp": rapp},
            {"keyword": "coverage hole", "doc_type": "algorithm_docs", "feature_area": "Coverage Hole", "rapp": rapp},
            {"keyword": "switch ON OFF", "doc_type": None, "feature_area": "Switch Control", "rapp": rapp},
            {"keyword": "NE List", "doc_type": None, "feature_area": "NE List", "rapp": rapp},
            {"keyword": "frequency independent", "doc_type": None, "feature_area": "Frequency", "rapp": rapp},
            {"keyword": "CM PM data collection", "doc_type": None, "feature_area": "Data Collection", "rapp": rapp},
        ])
    
    # Add feature-specific keywords
    if "CC3101" in feature_id:
        requirements.extend([
            {"keyword": "SCC Change", "doc_type": None, "feature_area": "SCC Change", "rapp": "VCCB"},
            {"keyword": "VoNR", "doc_type": None, "feature_area": "VoNR", "rapp": "VCCB"},
            {"keyword": "carrier aggregation", "doc_type": None, "feature_area": "CA", "rapp": "VCCB"},
        ])
    
    return requirements


def extract_fr_ids_from_tc(tc_content: str) -> list[str]:
    """
    Extract FR IDs from TC content.
    
    Args:
        tc_content: TC v1 content
    
    Returns:
        List of FR IDs found in the TC
    """
    import re
    
    fr_ids = []
    
    # Pattern 1: FR ID format (e.g., FR10.COA.SR1.10, FR22.CACP.SR1.HD1)
    pattern1 = r'FR\d+\.[A-Z]+\.[A-Z\d]+\.[A-Z\d]+'
    matches1 = re.findall(pattern1, tc_content)
    fr_ids.extend(matches1)
    
    # Pattern 2: Simple FR format (e.g., FR10, FR22)
    pattern2 = r'\bFR(\d+)\b'
    matches2 = re.findall(pattern2, tc_content)
    for num in matches2:
        fr_ids.append(f"FR{num}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_fr_ids = []
    for fr_id in fr_ids:
        if fr_id not in seen:
            seen.add(fr_id)
            unique_fr_ids.append(fr_id)
    
    return unique_fr_ids


def refine_tc(tc_v1_content: str, review_result, evidence_list: list) -> str:
    """
    Refine TC v1 to TC v2 based on review results.
    Implements refinement rules from 05_refinement_rules.md
    """
    logger.info("Starting TC Refinement...")
    
    # Parse TC sections
    sections = parse_tc_sections(tc_v1_content)
    
    # Build refinement notes
    refinement_lines = []
    change_log = []
    
    # 1. Add missing scenarios
    if review_result.missing_scenarios:
        refinement_lines.append("\n\n## Added Scenarios")
        for scenario in review_result.missing_scenarios:
            scenario_content = generate_scenario_content(scenario, evidence_list)
            refinement_lines.append(scenario_content)
            change_log.append(f"| Test Procedure | Added | (none) | {scenario} scenario | SC: Missing scenario |")
    
    # 2. Clarify Pass/Fail criteria based on findings
    pf_findings = [f for f in review_result.findings if "PF" in f.check_id or "pass/fail" in f.description.lower()]
    if pf_findings:
        refinement_lines.append("\n\n## Clarified Pass/Fail Criteria")
        for finding in pf_findings:
            refinement_lines.append(f"- **{finding.check_id}**: {finding.description}")
            refinement_lines.append(f"  → Suggestion: {finding.suggestion if hasattr(finding, 'suggestion') else 'Review required'}")
            change_log.append(f"| Pass/Fail Criteria | Modified | Ambiguous | Clarified per {finding.check_id} | {finding.description} |")
    
    # 3. Add missing preconditions from evidence
    precondition_items = extract_preconditions_from_evidence(evidence_list)
    if precondition_items:
        refinement_lines.append("\n\n## Additional Precondition Items")
        for item in precondition_items:
            refinement_lines.append(f"- {item}")
        change_log.append(f"| Precondition | Added | (none) | {len(precondition_items)} items | DC-4: Missing dependency |")
    
    # 4. Add Human Review Required section
    if review_result.human_review_items:
        refinement_lines.append("\n\n## Human Review Required")
        for item in review_result.human_review_items:
            refinement_lines.append(f"- [ ] {item}")
    
    # 5. Add Change Log
    if change_log:
        refinement_lines.append("\n\n## Change Log")
        refinement_lines.append("| Section | Change Type | Before | After | Reason |")
        refinement_lines.append("|---|---|---|---|---|")
        refinement_lines.extend(change_log)
    
    # 6. Add Enhancement Notes summary
    refinement_lines.append("\n\n## Enhancement Notes")
    refinement_lines.append(f"- Review completed with {len(evidence_list)} evidence chunks")
    refinement_lines.append(f"- Quality Score: {review_result.quality_score}")
    refinement_lines.append(f"- Missing Scenarios Detected: {len(review_result.missing_scenarios)}")
    refinement_lines.append(f"- Total Findings: {len(review_result.findings)}")
    refinement_lines.append(f"- Human Review Items: {len(review_result.human_review_items)}")
    
    # Combine original TC with refinements
    tc_v2_content = tc_v1_content + "\n".join(refinement_lines)
    
    logger.info(f"TC Refinement completed: {len(refinement_lines)} lines added")
    
    return tc_v2_content


def parse_tc_sections(tc_content: str) -> dict[str, str]:
    """
    Parse TC markdown into sections.
    
    Args:
        tc_content: Full TC content
    
    Returns:
        Dictionary of section name -> content
    """
    import re
    
    sections = {}
    current_section = "header"
    current_content = []
    
    for line in tc_content.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_content:
                sections[current_section] = "\n".join(current_content)
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content)
    
    return sections


def generate_scenario_content(scenario_type: str, evidence_list: list) -> str:
    """
    Generate scenario content based on type.
    
    Args:
        scenario_type: Type of scenario (e.g., "Negative/Failure path scenario")
        evidence_list: List of evidence for context
    
    Returns:
        Markdown formatted scenario content
    """
    scenario_templates = {
        "Positive/Normal flow scenario": """
### [Added Scenario: Positive Flow]
- **Purpose**: Verify normal/expected behavior
- **Steps**:
  1. Configure system with valid parameters
  2. Trigger the feature under test
  3. Verify expected output
- **Expected**: Feature operates as specified in FR
- **Evidence**: Based on FR requirement analysis
""",
        "Negative/Failure path scenario": """
### [Added Scenario: Negative Flow]
- **Purpose**: Verify failure/rejection handling
- **Steps**:
  1. Configure system with invalid/error conditions
  2. Trigger the feature under test
  3. Verify error handling
- **Expected**: System handles error gracefully, logs appropriate messages
- **Evidence**: Based on exception handling requirements
""",
        "Boundary value scenario": """
### [Added Scenario: Boundary Values]
- **Purpose**: Verify edge/boundary conditions
- **Steps**:
  1. Set parameters to minimum boundary value
  2. Execute and verify
  3. Set parameters to maximum boundary value
  4. Execute and verify
- **Expected**: System handles boundary values correctly
- **Evidence**: Based on parameter constraints in DLD
""",
        "Exception handling scenario": """
### [Added Scenario: Exception Handling]
- **Purpose**: Verify exception/error recovery
- **Steps**:
  1. Simulate exception condition (e.g., connection loss, invalid data)
  2. Verify system detects exception
  3. Verify recovery or graceful degradation
- **Expected**: System handles exception without crash, logs error
- **Evidence**: Based on error handling requirements
""",
        "Switch ON/OFF combination scenario": """
### [Added Scenario: Switch Combination]
- **Purpose**: Verify switch ON/OFF combinations
- **Steps**:
  1. Detection=ON, Resolution=ON → Verify both work
  2. Detection=ON, Resolution=OFF → Verify detection only
  3. Detection=OFF, Resolution=ON → Verify no action
  4. Detection=OFF, Resolution=OFF → Verify no action
- **Expected**: Each switch controls its function independently
- **Evidence**: Based on FR switch control requirements
""",
        "Frequency independence scenario": """
### [Added Scenario: Frequency Independence]
- **Purpose**: Verify per-frequency independent operation
- **Steps**:
  1. f1=ON, f2=OFF → Verify f1 only
  2. f1=OFF, f2=ON → Verify f2 only
  3. f1=ON, f2=ON → Verify both
- **Expected**: Each frequency operates independently
- **Evidence**: Based on FR frequency independence requirements
""",
    }
    
    # Find matching template
    for key, template in scenario_templates.items():
        if key.lower() in scenario_type.lower():
            return template
    
    # Default template for unknown scenarios
    return f"""
### [Added Scenario: {scenario_type}]
- **Purpose**: {scenario_type}
- **Steps**: [Human Review Required - specific steps needed]
- **Expected**: [Human Review Required - expected result needed]
- **Evidence**: Based on review analysis
"""


def extract_preconditions_from_evidence(evidence_list: list) -> list[str]:
    """
    Extract precondition items from evidence.
    
    Args:
        evidence_list: List of evidence
    
    Returns:
        List of precondition items
    """
    preconditions = []
    
    # Common precondition patterns
    precondition_keywords = {
        "Analytic Server": "Analytic Server 연결 확인",
        "NE List": "NE List 수신 및 설정 완료",
        "CM/PM": "CM/PM data collection 설정 완료",
        "switch": "관련 switch 초기화",
        "threshold": "임계값 설정 완료",
        "configuration": "설정 파라미터 확인",
    }
    
    for evidence in evidence_list:
        text_lower = evidence.text.lower()
        for keyword, precondition in precondition_keywords.items():
            if keyword.lower() in text_lower and precondition not in preconditions:
                preconditions.append(precondition)
    
    return preconditions


def generate_quality_report(review_result, evidence_list: list, 
                           feature_id: str, sw_pkg: str, rapp: str,
                           related_frs: list[str] | None = None,
                           output_dir: Path = None) -> Path:
    """Generate final Quality Report."""
    logger.info("Generating Quality Report...")
    
    # Use provided output_dir or default to legacy location
    if output_dir is None:
        output_dir = Path("output/quality_reports")
        output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / "quality_report.md"
    
    # Build Related FRs section
    related_frs_section = ""
    if related_frs:
        related_frs_section = f"- **Related FRs**: {', '.join(related_frs)}\n"
    
    report_content = f"""# Final Quality Report

## TC Information
- Feature ID: {feature_id}
- SW Package: {sw_pkg}
- rAPP: {rapp}
{related_frs_section}- Review Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Quality Score

| Metric | Value |
|--------|-------|
| Overall Score | {review_result.quality_score}/100 |
| Risk Level | {review_result.risk_level} |
| Decision | {review_result.decision} |
| Confidence | {review_result.confidence} |

## Review Summary

### Findings
- Total Findings: {len(review_result.findings)}
- Missing Scenarios: {len(review_result.missing_scenarios)}
- Human Review Items: {len(review_result.human_review_items)}

### Evidence Used
- Total Evidence Chunks: {len(evidence_list)}

## Evidence List (Top 10)

| # | Score | Source | Text Preview |
|---|-------|--------|--------------|
"""
    
    for i, ev in enumerate(sorted(evidence_list, key=lambda x: x.score, reverse=True)[:10], 1):
        text_preview = ev.text[:80].replace("\n", " ")
        report_content += f"| {i} | {ev.score:.2f} | {ev.source_path.split('/')[-1][:30]} | {text_preview}... |\n"
    
    report_content += f"""
## Recommendation

**Decision**: {review_result.decision}

"""
    
    if review_result.decision == "Approve":
        report_content += "This TC meets quality standards and is ready for use.\n"
    elif review_result.decision == "Revise":
        report_content += "This TC requires minor revisions before use. Review missing scenarios and findings.\n"
    else:
        report_content += "This TC requires significant revision. Consider regenerating with more complete input.\n"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    logger.info(f"Quality Report saved to: {report_path}")
    
    return report_path


def generate_reviewer_summary(review_result, evidence_list: list, tc_v1_content: str, tc_v2_content: str,
                              feature_id: str, sw_pkg: str, rapp: str,
                              refinement_items: list = None,
                              related_frs: list[str] | None = None,
                              output_dir: Path = None) -> Path:
    """
    Generate Reviewer Summary per 06_output_format.md Section 3.
    
    This is a practitioner's guide that should be readable in 3 minutes.
    
    Key improvements:
    1. Show only Top 3 Human Review Required items (P0 priority)
    2. Show Before/After for each refinement item clearly
    3. Provide concrete review guidance
    """
    logger.info("Generating Reviewer Summary...")
    
    if output_dir is None:
        output_dir = Path("output/quality_reports")
        output_dir.mkdir(parents=True, exist_ok=True)
    
    summary_path = output_dir / "reviewer_summary.md"
    
    # Build Related FRs section
    related_frs_section = ", ".join(related_frs) if related_frs else "N/A"
    
    # Get Top 3 P0 Human Review items
    top3_hr_items = review_result.human_review_items[:3] if review_result.human_review_items else []
    
    # Get Top 5 High severity findings
    high_findings = [f for f in review_result.findings if f.severity in ["Critical", "High"]][:5]
    
    # Build Top 3 review priorities
    top3_priorities = []
    for i, item in enumerate(top3_hr_items, 1):
        # Extract meaningful description from the item
        short_desc = item[:80] + "..." if len(item) > 80 else item
        top3_priorities.append({
            "order": i,
            "item": item,
            "short_desc": short_desc,
            "check_point": _get_check_point(item, rapp),
            "evidence_hint": _get_evidence_hint(item, evidence_list)
        })
    
    # Build Top 5 Before/After improvements from refinement_items
    improvements = []
    if refinement_items:
        for i, item in enumerate(refinement_items[:5], 1):
            before, after = _get_before_after(item)
            improvements.append({
                "order": i,
                "section": item.target_section,
                "before": before,
                "after": after,
                "reason": item.reason[:50] + "..." if len(item.reason) > 50 else item.reason,
                "auto": "✅" if item.auto_apply else "⚠️"
            })
    
    # Build risk table
    risks = []
    if review_result.risk_level == "High":
        risks.append(f"| Critical Issue 다수 | Field Risk | Quality Score {review_result.quality_score} 미만 | High | 대폭 수정 필요 |")
    elif review_result.risk_level == "Medium":
        risks.append(f"| 일부 High Issue | Field Risk | Quality Score {review_result.quality_score} | Medium | 보완 후 재검토 |")
    
    # Add specific risks from high findings
    for finding in high_findings[:3]:
        risks.append(f"| {finding.check_id}: {finding.description[:40]}... | Field Risk | {finding.severity} | {finding.tc_section} | {finding.evidence_status} |")
    
    # Calculate estimated review time
    estimated_time = max(10, len(top3_hr_items) * 3 + len(high_findings) * 2)
    
    # Build Cross-FR/rAPP section
    cross_fr_content = ""
    if rapp == "COM":
        cross_fr_content = """
### 관련 FR 및 rAPP 영향도

| 관련 FR | 관계 유형 | 검토 포인트 |
|---------|----------|------------|
| FR160 | Base | CMD ON/OFF 제어 기본 요구사항 |
| FR10 | Dependency | Overshooting Detection 연동 |
| FR20 | Dependency | Coverage Hole Detection 연동 |

| 관련 rAPP | 검토 포인트 |
|-----------|------------|
| ESM | ESM operation time 동안 PM 수집 제외 |
| LBM | COM tilt target 최적화 제외 |
"""
    
    summary_content = f"""# Reviewer Summary

## 📌 결론: **{review_result.decision}** (Quality Score: {review_result.quality_score}/100, Risk: {review_result.risk_level})

> ⏱️ **예상 검토 시간**: {estimated_time}분

---

## 🤖 AI 가 확인해서 보완한 내용 (Top {len(improvements)})

AI 가 다음 내용을 먼저 확인하고 TC 에 보완했습니다.

"""
    
    for imp in improvements:
        summary_content += f"""### {imp['order']}. {imp['section']}

- **Before**: {imp['before']}
- **After**: {imp['after']}
- **근거 문서**: {imp['reason']}
- **AI 자동 적용**: {imp['auto']}

---

"""
    
    summary_content += f"""## ⚠️ Human Review Required (Top {len(top3_hr_items)})

실무자 확인이 **정말로 필요한 항목만** 추렸습니다.

"""
    
    for priority in top3_priorities:
        summary_content += f"""### {priority['order']}. {priority['short_desc']}

- **확인 포인트**: {priority['check_point']}
- **근거 Evidence**: {priority['evidence_hint']}
- **확인 필요 이유**: AI 검색 결과 증거가 불충분함
- **검토 방법**: 
  1. TC 에서 해당 항목 검색
  2. 실제 구현/명세서와 일치하는지 확인
  3. 필요시 수정 제안

---

"""
    
    summary_content += f"""## 📝 AI 가 고친 내용 (Top {len(improvements)})

AI 가 다음 내용을 보완했습니다. **Before/After 를 확인**하세요.

| # | 항목 | Before | After | 근거 |
|---|------|--------|-------|------|
"""
    
    for imp in improvements:
        summary_content += f"| {imp['order']} | {imp['section']} | {imp['before']} | {imp['after']} | {imp['reason']} |\n"
    
    if not improvements:
        summary_content += "| - | 자동 보완 항목 없음 | - | - | - |\n"
    
    summary_content += f"""
---

## ⚠️ 위험 요소 (High Risk 항목만)

| 위험 | 유형 | 내용 | 영향도 |
|------|------|------|--------|
"""
    
    for risk in risks:
        summary_content += f"| {risk.split('|')[1].strip()} | {risk.split('|')[2].strip()} | {risk.split('|')[3].strip()} | {risk.split('|')[4].strip()} |\n"
    
    if not risks:
        summary_content += "| - | - | 특정 위험 요소 없음 | - |\n"
    
    summary_content += f"""
---

## 📊 전체 통계

| 항목 | 값 |
|------|-----|
| Quality Score | {review_result.quality_score}/100 |
| Risk Level | {review_result.risk_level} |
| Decision | {review_result.decision} |
| Total Findings | {len(review_result.findings)}개 |
| **Human Review Required** | **{len(review_result.human_review_items)}개 중 {len(top3_hr_items)}개 표시** |
| High Severity Findings | {len(high_findings)}개 |
| TC v1 → v2 | {len(tc_v1_content.split(chr(10)))}줄 → {len(tc_v2_content.split(chr(10)))}줄 |
| 사용된 Evidence | {len(evidence_list)}개 |

---

## 📋 참고 문서

| 우선순위 | 문서 | 확인 포인트 |
|----------|------|------------|
| 🔴 필수 | {rapp} Algorithm 설계서 | Threshold, KPI 정의 |
| 🔴 필수 | FR 명세서 | {related_frs_section} 요구사항 |
| 🟡 권장 | HLD/DLD | 의존성 및 제한사항 |
| 🟢 참고 | 과거 이슈 사례 | 유사 문제 패턴 |

---

> 💡 **검토 팁**: 
> 1. 위 **Top {len(top3_hr_items)}개 항목**부터 확인하세요
> 2. 각 항목당 **3 분** 정도 소요됩니다
> 3. 불명확한 부분은 TC v2 의 "Human Review Required" 섹션을 참고하세요
"""
    
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    logger.info(f"Reviewer Summary saved to: {summary_path}")
    
    return summary_path


def _get_check_point(item: str, rapp: str) -> str:
    """Extract check point from human review item - more intuitive version."""
    item_lower = item.lower()
    
    # FR behavior verification
    if "fr behavior" in item_lower or "core behavior" in item_lower:
        return "FR 에 정의된 핵심 동작 (ON/OFF, Switch 제어 등) 이 TC 에 있는지 확인"
    # FR scope verification  
    elif "fr scope" in item_lower or "scope defined" in item_lower:
        return "TC 가 FR 의 scope 범위 내에서 동작하는지 확인 (제외 대상, 조건 등)"
    # Positive scenario
    elif "positive" in item_lower or "normal" in item_lower or "expected flow" in item_lower:
        return "정상 동작 시나리오가 TC 에 포함되었는지 확인"
    # Negative scenario
    elif "negative" in item_lower or "failure" in item_lower or "rejection" in item_lower:
        return "오류/실패 시나리오가 TC 에 포함되었는지 확인"
    # Boundary scenario
    elif "boundary" in item_lower or "edge" in item_lower:
        return "경계값 (threshold ±0.5, 최소/최대) 테스트가 TC 에 포함되었는지 확인"
    # Exception scenario
    elif "exception" in item_lower or "error" in item_lower:
        return "예외 상황 (data loss, connection fail) 처리가 TC 에 포함되었는지 확인"
    # API command specificity
    elif "api command" in item_lower or "specific" in item_lower:
        return "API 명령이 구체적으로 명시되었는지 확인 (예: 'run' → 'POST /api/v1/...')"
    # Parameter completeness
    elif "parameter" in item_lower or "completeness" in item_lower:
        return "필수 파라미터가 모두 명시되었는지 확인"
    # Step ordering
    elif "step ordering" in item_lower or "order" in item_lower:
        return "Step 순서가 논리적인지 확인 (선행조건 → 실행 → 결과확인)"
    # Trigger clarity
    elif "trigger" in item_lower:
        return "각 step 의 trigger (어떻게 실행) 이 명확한지 확인"
    # CMD/Switch specific
    elif "cmd" in item_lower or "switch" in item_lower:
        return "CMD/Detection Switch ON/OFF 조건이 구체적으로 명시되었는지 확인"
    # Frequency specific
    elif "frequency" in item_lower or "carrier" in item_lower:
        return "Carrier Frequency 별 독립 동작 조건이 명시되었는지 확인"
    # NE List specific
    elif "ne list" in item_lower or "cell" in item_lower:
        return "NE List 포함 cell 만 대상임이 명시되었는지 확인"
    # Overshooting specific
    elif "overshoot" in item_lower:
        return "Overshooting detection threshold (TA, RSRP) 가 명시되었는지 확인"
    # Coverage Hole specific
    elif "coverage hole" in item_lower:
        return "Coverage hole detection threshold (CQI, BLER, RSRP) 가 명시되었는지 확인"
    # KPI/Threshold specific
    elif "kpi" in item_lower or "threshold" in item_lower:
        return "KPI/threshold 값이 구체적 수치로 명시되었는지 확인"
    # Default
    else:
        return f"{rapp} 의 동작 조건이 구체적으로 명시되었는지 확인"


def _get_evidence_hint(item: str, evidence_list: list) -> str:
    """Get evidence hint for human review item - more intuitive version."""
    item_lower = item.lower()
    
    # Search for matching evidence
    for ev in evidence_list[:10]:
        text_lower = ev.text.lower()
        # Check for keyword matches
        if any(kw in text_lower for kw in item_lower.split()[:3]):
            # Return shortened file name
            file_name = ev.source_path.split("/")[-1] if "/" in ev.source_path else ev.source_path.split("\\")[-1]
            if len(file_name) > 40:
                return file_name[:40] + "..."
            return file_name
    
    # Default based on item type
    if "fr" in item_lower:
        return "FR 명세서"
    elif "algorithm" in item_lower or "threshold" in item_lower:
        return "Algorithm 설계서"
    elif "switch" in item_lower or "cmd" in item_lower:
        return "COM Interface 문서"
    else:
        return "Algorithm 설계서 또는 FR 명세서"


def _get_before_after(refinement_item) -> tuple[str, str]:
    """Extract Before/After from refinement item - more intuitive version."""
    problem_type = refinement_item.problem_type
    reason = refinement_item.reason[:30] + "..." if len(refinement_item.reason) > 30 else refinement_item.reason
    
    if problem_type == "missing_scenario":
        return "검증 시나리오 없음", "검증 시나리오 추가됨"
    elif problem_type == "RC-2":
        return "FR 요구사항 검증 누락", "FR 요구사항 검증 단계 추가됨"
    elif problem_type == "RC-4":
        return "FR scope 검증 안됨", "FR scope 검증 단계 추가됨"
    elif problem_type == "SC-1":
        return "Positive 시나리오 없음", "Positive 시나리오 추가됨"
    elif problem_type == "SC-2":
        return "Negative 시나리오 없음", "Negative 시나리오 추가됨"
    elif problem_type == "SC-3":
        return "Boundary 시나리오 없음", "Boundary 시나리오 추가됨"
    elif problem_type == "SC-4":
        return "Exception 시나리오 없음", "Exception 시나리오 추가됨"
    elif problem_type == "PF-3":
        return "'정상 동작 확인' (모호함)", "구체적 수치/상태 기준 명시됨"
    elif problem_type == "PE-2":
        return "명령어 없음 (예: 'run')", "구체적 API 명령 명시됨"
    elif problem_type == "DC-4":
        return "Precondition 누락", "Precondition 추가됨"
    elif problem_type == "OT-1":
        return "Log 확인 방법 없음", "Log file/path 명시됨"
    elif problem_type == "human_review":
        return "AI 확신 부족", f"실무자 확인 필요: {reason}"
    else:
        return "보완 전", f"보완 후: {reason}"


def record_to_gotchas(feature_id: str, sw_pkg: str, rapp: str, 
                     review_result, evidence_count: int, output_path: str):
    """
    Record work summary to RAS_Experience/RAS-gotchas.md (Step 9 - Automatic Recording).
    
    Per SKILL.md Line 390-419: "자동 기록 의무"
    """
    gotchas_path = Path("RAS_Experience/RAS-gotchas.md")
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Build summary
    summary_lines = [
        "",
        f"## {timestamp} - Automated - {feature_id}, {sw_pkg}, {rapp}",
        "",
        "### 작업 내용",
        f"- TC Review 수행: {feature_id} ({sw_pkg})",
        f"- rAPP: {rapp}",
        f"- Quality Score: {review_result.quality_score}/100",
        f"- Risk Level: {review_result.risk_level}",
        f"- Decision: {review_result.decision}",
        "",
        "### 발견된 이슈",
        f"- Total Findings: {len(review_result.findings)}",
        f"- Missing Scenarios: {len(review_result.missing_scenarios)}",
        f"- Human Review Items: {len(review_result.human_review_items)}",
        "",
        "### RAG Evidence",
        f"- 검색된 Evidence Chunks: {evidence_count}개",
        "",
        "### 교훈/주의사항",
    ]
    
    # Add specific notes based on results
    if review_result.quality_score < 60:
        summary_lines.append(f"- Quality Score {review_result.quality_score}로 낮음. 대폭 수정 필요.")
    if review_result.risk_level == "High":
        summary_lines.append(f"- High Risk 판정. Critical Issue 다수 발견.")
    if evidence_count == 0:
        summary_lines.append("- RAG 검색 결과 Evidence 없음. 검색어 또는 데이터 확인 필요.")
    if len(review_result.missing_scenarios) > 5:
        summary_lines.append(f"- Missing Scenario {len(review_result.missing_scenarios)}개. 시나리오 보완 필요.")
    
    summary_lines.append("")
    summary_lines.append("---")
    summary_lines.append("")
    
    # Read existing content and append
    if gotchas_path.exists():
        with open(gotchas_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
        new_content = existing_content + "\n".join(summary_lines)
    else:
        new_content = "# RAS-TestCaseReview Experience Log\n\n" + "\n".join(summary_lines)
    
    with open(gotchas_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    logger.info(f"Work summary recorded to: {gotchas_path}")


def main():
    """Main pipeline entry point."""
    parser = argparse.ArgumentParser(description="Full RAG TC Review Pipeline")
    parser.add_argument("--feature", type=str, required=True, help="Feature ID (e.g., FGR-CC3101)")
    parser.add_argument("--related-frs", type=str, nargs="+", help="Related FR IDs for Multi-FR review (e.g., FR10.COA.SR1.10 FR10.COA.SR1.11)")
    parser.add_argument("--pkg", type=str, required=True, help="SW Package (e.g., SVR26A)")
    parser.add_argument("--rapp", type=str, default="COM", help="rAPP name (e.g., COM)")
    parser.add_argument("--tc-path", type=str, help="Path to existing TC v1 (optional)")
    parser.add_argument("--hld-path", type=str, help="Path to HLD document (optional)")
    parser.add_argument("--dld-path", type=str, help="Path to DLD document (optional)")
    parser.add_argument("--algo-path", type=str, help="Path to Algorithm doc (optional)")
    parser.add_argument("--multi-fr", action="store_true", help="Use Multi-FR Pipeline instead of single FR pipeline")
    
    args = parser.parse_args()
    
    logger.info("=" * 70)
    logger.info("RAG TC Review Pipeline - Starting")
    logger.info("=" * 70)
    logger.info(f"Feature: {args.feature}")
    logger.info(f"Package: {args.pkg}")
    logger.info(f"rAPP: {args.rapp}")
    logger.info("=" * 70)
    
    # Step 1: Verify JSONL data
    jsonl_dir = Path("data/jsonl")
    data_status = verify_jsonl_data(jsonl_dir)
    if data_status["status"] != "ok":
        logger.error(f"Data verification failed: {data_status['message']}")
        return 1
    
    # Step 2: Initialize Keyword Retriever
    index_file = Path("data/jsonl/keyword_index.json")
    retriever = initialize_retriever(jsonl_dir, index_file)
    
    # Step 3: Generate or Load TC v1
    if args.tc_path:
        logger.info(f"Loading existing TC v1 from {args.tc_path}")
        with open(args.tc_path, "r", encoding="utf-8") as f:
            tc_v1_content = f.read()
    else:
        logger.info("Generating TC v1 from FR/HLD/DLD...")
        tc_v1_content = generate_tc_v1(
            feature_id=args.feature,
            sw_pkg=args.pkg,
            rapp=args.rapp,
            hld_path=Path(args.hld_path) if args.hld_path else None,
            dld_path=Path(args.dld_path) if args.dld_path else None,
            algorithm_path=Path(args.algo_path) if args.algo_path else None,
        )
    
    # Step 4: Review TC v1
    review_result, evidence_list = review_tc(
        tc_v1_content=tc_v1_content,
        feature_id=args.feature,
        sw_pkg=args.pkg,
        rapp=args.rapp,
        retriever=retriever,
    )
    
    # Step 5: Refine TC using RefinementEngine
    logger.info("Starting TC Refinement with RefinementEngine...")
    
    from tc_reviewer import RefinementEngine, ReviewConfig
    
    # Create config for RefinementEngine
    refinement_config = ReviewConfig(
        tc_v1_path=Path(args.tc_path) if args.tc_path else Path("output/enhanced_tc/temp.md"),
        feature_id=args.feature,
        sw_package=args.pkg,
        rapp_name=args.rapp,
    )
    
    refinement_engine = RefinementEngine(refinement_config)
    tc_v2_content, refinement_items, evidence_trace, added_scenarios = refinement_engine.refine(
        tc_v1_content, review_result, evidence_list
    )
    
    # Create TC-specific output folder (all-in-one structure)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    review_folder = Path(f"output/reviews/{args.feature}_{args.pkg}_{timestamp}")
    review_folder.mkdir(parents=True, exist_ok=True)
    
    # Save TC v2 in the review folder
    tc_v2_path = review_folder / "enhanced_tc_v2.md"
    
    with open(tc_v2_path, "w", encoding="utf-8") as f:
        f.write(tc_v2_content)
    
    logger.info(f"TC v2 saved to: {tc_v2_path}")
    
    # Save Evidence Trace Table
    evidence_trace_path = review_folder / "evidence_trace_table.md"
    with open(evidence_trace_path, "w", encoding="utf-8") as f:
        f.write("# Evidence Trace Table\n\n")
        f.write("| Change ID | Modified Section | Change Summary | Reason | Evidence ID | Source | Confidence | Human Review |\n")
        f.write("|-----------|-----------------|----------------|--------|-------------|--------|------------|---------------|\n")
        for trace in evidence_trace:
            hr_mark = "⚠️" if trace.human_review_required else "✅"
            f.write(f"| {trace.change_id} | {trace.modified_section} | {trace.change_summary} | {trace.reason[:50]}... | {trace.evidence_id} | {trace.source_file} | {trace.confidence:.2f} | {hr_mark} |\n")
    logger.info(f"Evidence Trace Table saved to: {evidence_trace_path}")
    
    # Save Added Scenario List
    added_scenario_path = review_folder / "added_scenario_list.md"
    with open(added_scenario_path, "w", encoding="utf-8") as f:
        f.write("# Added Scenario List\n\n")
        f.write("| # | Scenario Name | Type | Reason | Target Section | Risk |\n")
        f.write("|---|--------------|------|--------|----------------|------|\n")
        for i, scenario in enumerate(added_scenarios, 1):
            risk_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(scenario.risk_level, "⚪")
            f.write(f"| {i} | {scenario.scenario_name} | {scenario.scenario_type} | {scenario.reason[:50]}... | {scenario.target_tc_section} | {risk_icon} |\n")
    logger.info(f"Added Scenario List saved to: {added_scenario_path}")
    
    # Step 6: Generate Quality Report in the same folder
    report_path = generate_quality_report(
        review_result=review_result,
        evidence_list=evidence_list,
        feature_id=args.feature,
        sw_pkg=args.pkg,
        rapp=args.rapp,
        related_frs=args.related_frs,
        output_dir=review_folder,
    )
    
    # Step 7: Generate Reviewer Summary (per SKILL.md and 06_output_format.md)
    summary_path = generate_reviewer_summary(
        review_result=review_result,
        evidence_list=evidence_list,
        tc_v1_content=tc_v1_content,
        tc_v2_content=tc_v2_content,
        refinement_items=refinement_items,
        feature_id=args.feature,
        sw_pkg=args.pkg,
        rapp=args.rapp,
        related_frs=args.related_frs,
        output_dir=review_folder,
    )
    
    # Step 8: Record to RAS-gotchas.md (Automatic Recording - SKILL.md Line 390-419)
    record_to_gotchas(
        feature_id=args.feature,
        sw_pkg=args.pkg,
        rapp=args.rapp,
        review_result=review_result,
        evidence_count=len(evidence_list),
        output_path=str(review_folder),
    )
    
    logger.info("=" * 70)
    logger.info("Pipeline Completed Successfully!")
    logger.info("=" * 70)
    logger.info(f"TC v2: {tc_v2_path}")
    logger.info(f"Quality Report: {report_path}")
    logger.info(f"Reviewer Summary: {summary_path}")
    logger.info(f"Review Folder: {review_folder}")
    logger.info("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
