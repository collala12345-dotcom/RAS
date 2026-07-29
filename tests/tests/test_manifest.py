from rag_preprocessor.manifest import Manifest


def test_manifest_skip_behavior(tmp_path):
    output = tmp_path / "doc.jsonl"
    output.write_text("{}", encoding="utf-8")
    manifest = Manifest(tmp_path)
    manifest.update("source.md", output, "abc", 1)
    manifest.save()

    loaded = Manifest(tmp_path)
    assert loaded.should_skip("source.md", "abc", force=False)
    assert not loaded.should_skip("source.md", "changed", force=False)
    assert not loaded.should_skip("source.md", "abc", force=True)
