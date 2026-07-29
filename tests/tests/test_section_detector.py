from rag_preprocessor.document_loader import LoadedLine
from rag_preprocessor.section_detector import (
    detect_sections,
    is_algorithm_section_heading,
    is_3gpp_section_heading,
    is_feature_section_heading,
    is_hld_dld_section_heading,
    is_issue_case_section_heading,
    is_legacy_tc_section_heading,
    is_markdown_heading,
    is_review_comment_section_heading,
    is_slide_boundary,
    is_test_result_section_heading,
)


def test_3gpp_section_heading_detection():
    assert is_3gpp_section_heading("5.3.5 RRC reconfiguration")
    assert is_3gpp_section_heading("A.1 General")


def test_markdown_heading_detection():
    assert is_markdown_heading("## Interface")


def test_feature_fr_detection():
    assert is_feature_section_heading("FR10 Adaptive Cell Filter")


def test_legacy_tc_section_detection():
    assert is_legacy_tc_section_heading("Pass/Fail Criteria")


def test_ppt_slide_boundary_detection():
    assert is_slide_boundary("## Slide 3: System Architecture")
    assert is_slide_boundary("---")


def test_hld_dld_section_detection():
    assert is_hld_dld_section_heading("System Flow")


def test_algorithm_step_detection():
    assert is_algorithm_section_heading("Step 2")


def test_issue_case_detection():
    assert is_issue_case_section_heading("Root Cause")


def test_test_result_log_detection():
    assert is_test_result_section_heading("[2026-07-01 10:01:00] ERROR ERR-204 CELL-22")


def test_review_comment_detection():
    assert is_review_comment_section_heading("Human Review Required")


def test_general_markdown_without_headings_gets_document_section():
    lines = [LoadedLine(1, "No heading here."), LoadedLine(2, "Still meaningful.")]
    sections = detect_sections(lines, "general_md")
    assert len(sections) == 1
    assert sections[0].title == "Document"


def test_detect_sections_returns_line_ranges():
    lines = [
        LoadedLine(1, "# Title"),
        LoadedLine(2, "Intro"),
        LoadedLine(3, "5.3.5 RRC reconfiguration"),
        LoadedLine(4, "Body"),
    ]
    sections = detect_sections(lines, "3gpp_docs")
    assert sections[0].start_line == 1
    assert sections[-1].section == "5.3.5"
    assert sections[-1].end_line == 4
