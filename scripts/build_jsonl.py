import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from rag_preprocessor.document_discovery import DOC_TYPES
from rag_preprocessor.pipeline import PipelineConfig, run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build JSONL chunks from local Markdown files.")
    parser.add_argument("--input-dir", required=True, help="Directory containing Markdown files.")
    parser.add_argument("--output-dir", default="data/processed/jsonl", help="Directory for JSONL output.")
    parser.add_argument("--force", action="store_true", help="Reprocess even when manifest hashes match.")
    parser.add_argument("--doc-type", choices=sorted(DOC_TYPES), help="Override detected document type.")
    parser.add_argument("--target-chars", type=int, default=2000, help="Target chunk size for long sections.")
    parser.add_argument("--max-chars", type=int, default=5000, help="Maximum chunk size.")
    parser.add_argument("--overlap-chars", type=int, default=250, help="Overlap when splitting long sections.")
    parser.add_argument("--min-chars", type=int, default=100, help="Minimum meaningful chunk size before merging adjacent sections.")
    parser.add_argument("--print-samples", action="store_true", help="Print a few generated JSONL rows.")
    parser.add_argument("--validate-only", action="store_true", help="Validate existing JSONL files in --output-dir without preprocessing.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        force=args.force,
        doc_type=args.doc_type,
        target_chars=args.target_chars,
        max_chars=args.max_chars,
        overlap_chars=args.overlap_chars,
        min_chars=args.min_chars,
        print_samples=args.print_samples,
        validate_only=args.validate_only,
    )
    run_pipeline(config)


if __name__ == "__main__":
    main()
