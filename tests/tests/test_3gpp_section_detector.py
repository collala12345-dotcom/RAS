"""Tests for 3GPP section heading detection improvements."""
import sys
from pathlib import Path

# Ensure src is importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from rag_preprocessor.document_loader import LoadedLine
from rag_preprocessor.section_detector import (
    detect_sections,
    is_3gpp_section_heading,
    _parse_heading,
    _gpp_section_depth,
    _is_false_positive_heading,
)


# ---------------------------------------------------------------------------
# Plain text 3GPP section heading detection
# ---------------------------------------------------------------------------

def test_plain_text_section_heading_detection():
    """Plain text numeric section headings should be detected."""
    assert is_3gpp_section_heading("1 Scope")
    assert is_3gpp_section_heading("5.3.5 RRC reconfiguration")
    assert is_3gpp_section_heading("5.3.5.1 General")
    assert is_3gpp_section_heading("6.2.2 Message definitions")


def test_3gpp_suffix_letter_heading():
    """3GPP-style suffix letters (7.4A) should be detected."""
    assert is_3gpp_section_heading("7.4A Special section")
    assert is_3gpp_section_heading("5.3.5.13.2 Example title")


def test_annex_heading_detection():
    """Annex headings should be detected."""
    assert is_3gpp_section_heading("Annex A")
    assert is_3gpp_section_heading("Annex B")


def test_annex_subsection_detection():
    """Annex sub-sections like A.1 General should be detected."""
    result = _parse_heading("A.1 General", "3gpp_docs")
    assert result is not None
    title, section, level, metadata = result
    assert section == "A.1"
    assert "General" in title
    assert "3gpp_section_heading" in metadata.get("detected_patterns", [])


def test_markdown_heading_with_section_number():
    """Markdown heading + section number should be detected as 3GPP heading."""
    result = _parse_heading("## 5.3.5 RRC reconfiguration", "3gpp_docs")
    assert result is not None
    title, section, level, metadata = result
    assert section == "5.3.5"
    assert "3gpp_section_heading" in metadata.get("detected_patterns", [])


# ---------------------------------------------------------------------------
# False positive prevention
# ---------------------------------------------------------------------------

def test_table_row_not_heading():
    """Table rows should not be detected as headings."""
    assert _is_false_positive_heading("| 1 | Scope | 28 |")
    assert _is_false_positive_heading("|---|---|")


def test_bullet_not_heading():
    """Bullet list items should not be detected as headings."""
    assert _is_false_positive_heading("- 1 Scope")
    assert _is_false_positive_heading("* 5.3.5 RRC reconfiguration")


def test_numbered_list_not_heading():
    """Numbered list items should not be detected as headings."""
    assert _is_false_positive_heading("1. Scope of the document")


def test_page_number_not_heading():
    """Page number only lines should not be detected as headings."""
    assert _is_false_positive_heading("28")
    assert _is_false_positive_heading("  42  ")


def test_toc_line_not_heading():
    """TOC lines with tab + page number should not be detected as headings."""
    assert _is_false_positive_heading("1\tScope\t28")
    assert _is_false_positive_heading("5.3.5\tRRC reconfiguration\t90")


def test_dotted_leader_not_heading():
    """Dotted leader lines should not be detected as headings."""
    assert _is_false_positive_heading("1 Scope ........................ 28")


def test_procedure_step_not_heading():
    """Procedure steps (1> text) should not be detected as headings."""
    assert _is_false_positive_heading("1> The UE shall apply the configuration")


def test_long_line_not_heading():
    """Very long lines should not be detected as headings."""
    long_line = "1 " + "x" * 250
    assert _is_false_positive_heading(long_line)


# ---------------------------------------------------------------------------
# Heading hierarchy path generation
# ---------------------------------------------------------------------------

def test_heading_hierarchy_path():
    """heading_path should reflect the section hierarchy."""
    lines = [
        LoadedLine(1, "1 Scope"),
        LoadedLine(2, "Some scope text."),
        LoadedLine(3, "5 Procedures"),
        LoadedLine(4, "5.3 Connection control"),
        LoadedLine(5, "5.3.5 RRC reconfiguration"),
        LoadedLine(6, "5.3.5.1 General"),
        LoadedLine(7, "Some general text."),
    ]
    sections = detect_sections(lines, "3gpp_docs")
    # Find the 5.3.5.1 section
    deep_section = [s for s in sections if s.section == "5.3.5.1"]
    assert len(deep_section) == 1
    path = deep_section[0].heading_path
    # Path should contain parent sections
    assert any("5" in p and "Procedures" in p for p in path)
    assert any("5.3" in p and "Connection control" in p for p in path)
    assert any("5.3.5" in p and "RRC reconfiguration" in p for p in path)
    assert any("5.3.5.1" in p and "General" in p for p in path)


def test_section_depth_calculation():
    """_gpp_section_depth should return correct depth."""
    assert _gpp_section_depth("1") == 1
    assert _gpp_section_depth("5.3") == 2
    assert _gpp_section_depth("5.3.5") == 3
    assert _gpp_section_depth("5.3.5.13.2") == 5
    assert _gpp_section_depth("A") == 1
    assert _gpp_section_depth("A.1") == 2
    assert _gpp_section_depth("A.2.1") == 3


# ---------------------------------------------------------------------------
# Section/title metadata not empty
# ---------------------------------------------------------------------------

def test_section_title_not_empty():
    """Detected 3GPP sections should have non-empty section and title."""
    lines = [
        LoadedLine(1, "1 Scope"),
        LoadedLine(2, "Some text."),
        LoadedLine(3, "5.3.5 RRC reconfiguration"),
        LoadedLine(4, "More text."),
    ]
    sections = detect_sections(lines, "3gpp_docs")
    # Skip the "Document" fallback section
    real_sections = [s for s in sections if s.section != ""]
    assert len(real_sections) >= 2
    for s in real_sections:
        assert s.section != "", f"Section is empty for title: {s.title}"
        assert s.title != "Document", f"Title is 'Document' for section: {s.section}"
        assert s.title != "", f"Title is empty for section: {s.section}"


# ---------------------------------------------------------------------------
# detected_patterns contains 3gpp_section_heading
# ---------------------------------------------------------------------------

def test_detected_patterns_contains_3gpp_section_heading():
    """detected_patterns should contain '3gpp_section_heading' for 3GPP headings."""
    lines = [
        LoadedLine(1, "1 Scope"),
        LoadedLine(2, "Some text."),
        LoadedLine(3, "5.3.5 RRC reconfiguration"),
        LoadedLine(4, "More text."),
    ]
    sections = detect_sections(lines, "3gpp_docs")
    real_sections = [s for s in sections if s.section != ""]
    assert len(real_sections) >= 2
    for s in real_sections:
        patterns = s.metadata.get("detected_patterns", [])
        assert "3gpp_section_heading" in patterns, (
            f"3gpp_section_heading not in detected_patterns for section {s.section}: {patterns}"
        )


# ---------------------------------------------------------------------------
# Fallback general_md behavior still works
# ---------------------------------------------------------------------------

def test_general_md_without_headings_gets_document_section():
    """general_md without any recognizable headings should still get 'Document' fallback."""
    lines = [
        LoadedLine(1, "No heading here."),
        LoadedLine(2, "Still meaningful."),
    ]
    sections = detect_sections(lines, "general_md")
    assert len(sections) == 1
    assert sections[0].title == "Document"


def test_general_md_with_3gpp_headings_detected():
    """general_md with 3GPP-style headings should detect them (not just fallback)."""
    lines = [
        LoadedLine(1, "1 Scope"),
        LoadedLine(2, "Some text."),
        LoadedLine(3, "5.3.5 RRC reconfiguration"),
        LoadedLine(4, "More text."),
    ]
    sections = detect_sections(lines, "general_md")
    real_sections = [s for s in sections if s.section != ""]
    assert len(real_sections) >= 2
    assert any(s.section == "1" for s in real_sections)
    assert any(s.section == "5.3.5" for s in real_sections)


# ---------------------------------------------------------------------------
# Line range accuracy
# ---------------------------------------------------------------------------

def test_line_ranges_accurate():
    """start_line and end_line should be accurate to the original md."""
    lines = [
        LoadedLine(1, "1 Scope"),
        LoadedLine(2, "Some scope text."),
        LoadedLine(3, "5.3.5 RRC reconfiguration"),
        LoadedLine(4, "Some reconfiguration text."),
        LoadedLine(5, "More reconfiguration text."),
    ]
    sections = detect_sections(lines, "3gpp_docs")
    scope_section = [s for s in sections if s.section == "1"][0]
    assert scope_section.start_line == 1
    assert scope_section.end_line == 2  # ends before next heading

    rrc_section = [s for s in sections if s.section == "5.3.5"][0]
    assert rrc_section.start_line == 3
    assert rrc_section.end_line == 5  # last line
