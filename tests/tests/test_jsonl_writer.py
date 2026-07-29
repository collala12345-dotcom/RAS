import json

from rag_preprocessor.jsonl_writer import write_jsonl
from rag_preprocessor.validator import validate_jsonl


def test_jsonl_validity(tmp_path):
    row = {
        "chunk_id": "c1",
        "doc_id": "d1",
        "doc_type": "general_md",
        "source_path": "sample.md",
        "section": "",
        "title": "Title",
        "heading_path": ["Title"],
        "start_line": 1,
        "end_line": 2,
        "text": "hello",
        "char_count": 5,
        "created_at": "2026-07-08T00:00:00+00:00",
    }
    path = write_jsonl([row], tmp_path / "out.jsonl")
    rows, warnings = validate_jsonl(path)
    assert rows == [row]
    assert warnings == []
    assert json.loads(path.read_text(encoding="utf-8").strip())["text"] == "hello"


def test_duplicate_chunk_id_prevention(tmp_path):
    row = {
        "chunk_id": "c1",
        "doc_id": "d1",
        "doc_type": "general_md",
        "source_path": "sample.md",
        "section": "",
        "title": "Title",
        "heading_path": ["Title"],
        "start_line": 1,
        "end_line": 1,
        "text": "hello",
        "char_count": 5,
        "created_at": "2026-07-08T00:00:00+00:00",
    }
    path = write_jsonl([row, row], tmp_path / "dup.jsonl")
    try:
        validate_jsonl(path)
    except ValueError as exc:
        assert "duplicate chunk_id" in str(exc)
    else:
        raise AssertionError("duplicate chunk_id was not rejected")
