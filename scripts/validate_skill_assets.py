from pathlib import Path
import json
import sys


SKILL_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "references/00_project_scope.md",
    "references/01_retrieval_rules.md",
    "references/02_required_evidence_fields.md",
    "references/03_tc_validation_checklist.md",
    "references/04_quality_rubric.md",
    "references/05_refinement_rules.md",
    "references/06_output_format.md",
    "references/07_com_domain_rules.md",
    "references/08_security_and_data_policy.md",
    "assets/sample_tc_v1.md",
    "assets/sample_evidence_chunks.jsonl",
    "assets/sample_quality_report.md",
    "assets/sample_enhanced_tc_v2.md",
    "assets/sample_reviewer_summary.md",
]

REQUIRED_JSONL_FIELDS = {
    "chunk_id",
    "doc_id",
    "doc_type",
    "source_path",
    "section",
    "title",
    "heading_path",
    "start_line",
    "end_line",
    "text",
    "char_count",
    "created_at",
}


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = SKILL_ROOT / relative
        if not path.exists():
            errors.append(f"Missing required file: {relative}")
        elif path.is_file() and relative != "assets/sample_evidence_chunks.jsonl":
            if not path.read_text(encoding="utf-8").strip():
                errors.append(f"Required file is empty: {relative}")

    jsonl_path = SKILL_ROOT / "assets/sample_evidence_chunks.jsonl"
    row_count = 0
    if jsonl_path.exists():
        with jsonl_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row_count += 1
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"Invalid JSONL at line {line_number}: {exc}")
                    continue
                missing = REQUIRED_JSONL_FIELDS - row.keys()
                if missing:
                    errors.append(f"Line {line_number} missing fields: {sorted(missing)}")
                if row.get("char_count") != len(row.get("text", "")):
                    errors.append(f"Line {line_number} char_count mismatch")
                if not row.get("text", "").strip():
                    errors.append(f"Line {line_number} text is empty")

    if row_count == 0:
        errors.append("sample_evidence_chunks.jsonl has no rows")

    if errors:
        print("Skill asset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill asset validation passed.")
    print(f"Skill root: {SKILL_ROOT}")
    print(f"Required files checked: {len(REQUIRED_FILES)}")
    print(f"Evidence JSONL rows checked: {row_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
