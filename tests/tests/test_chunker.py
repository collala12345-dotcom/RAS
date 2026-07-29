from rag_preprocessor.document_loader import LoadedLine
from rag_preprocessor.section_detector import Section
from rag_preprocessor.chunker import chunk_sections


def test_long_section_splits_with_overlap():
    lines = [LoadedLine(1, "# Big Section")]
    for index in range(2, 80):
        lines.append(LoadedLine(index, f"Paragraph {index} " + ("x" * 80)))
        lines.append(LoadedLine(index + 100, ""))
    section = Section("Big Section", "", ["Big Section"], 1, 179, lines)
    chunks = chunk_sections([section], target_chars=800, max_chars=1200, overlap_chars=100)
    assert len(chunks) > 1
    assert all(chunk.char_count if hasattr(chunk, "char_count") else len(chunk.text) <= 1200 for chunk in chunks)


def test_long_paragraph_fallback_splits_by_max_chars():
    line = LoadedLine(1, "x" * 260)
    section = Section("Document", "", ["Document"], 1, 1, [line])
    chunks = chunk_sections([section], target_chars=80, max_chars=100, overlap_chars=10)
    assert len(chunks) > 1
    assert all(len(chunk.text) <= 100 for chunk in chunks)


def test_table_preservation_when_under_max_chars():
    lines = [
        LoadedLine(1, "| A | B |"),
        LoadedLine(2, "|---|---|"),
        LoadedLine(3, "| 1 | 2 |"),
    ]
    section = Section("Table", "", ["Table"], 1, 3, lines)
    chunks = chunk_sections([section], target_chars=20, max_chars=200, overlap_chars=0)
    assert len(chunks) == 1
    assert "| 1 | 2 |" in chunks[0].text


def test_code_block_preservation_when_under_max_chars():
    lines = [
        LoadedLine(1, "```python"),
        LoadedLine(2, "print('synthetic')"),
        LoadedLine(3, "```"),
    ]
    section = Section("Code", "", ["Code"], 1, 3, lines)
    chunks = chunk_sections([section], target_chars=20, max_chars=200, overlap_chars=0)
    assert len(chunks) == 1
    assert chunks[0].text.count("```") == 2
