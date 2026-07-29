from pathlib import Path

from rag_preprocessor.pipeline import PipelineConfig, run_pipeline


def test_empty_file_handling(tmp_path):
    input_dir = tmp_path / "sample_data" / "edge_cases"
    input_dir.mkdir(parents=True)
    (input_dir / "empty.md").write_text("", encoding="utf-8")
    output_dir = tmp_path / "out"

    paths = run_pipeline(PipelineConfig(input_dir=input_dir, output_dir=output_dir, force=True))

    assert paths == []
    manifest_text = (output_dir / "manifest.json").read_text(encoding="utf-8")
    assert '"chunk_count": 0' in manifest_text


def test_validate_only_uses_existing_jsonl(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "one.jsonl").write_text(
        '{"chunk_id":"c1","doc_id":"d1","doc_type":"general_md","source_path":"x.md","section":"","title":"x","heading_path":["x"],"start_line":1,"end_line":1,"text":"hello","char_count":5,"created_at":"2026-07-08T00:00:00+00:00"}\n',
        encoding="utf-8",
    )

    paths = run_pipeline(PipelineConfig(input_dir=Path("."), output_dir=output_dir, validate_only=True))

    assert paths == [output_dir / "one.jsonl"]
