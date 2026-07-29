#!/usr/bin/env python3
"""
build_vectordb.py — CLI tool to build the ChromaDB vector database.

Stage 2: Reads JSONL files from Stage 1, embeds each chunk using BAAI/bge-m3,
and stores in ChromaDB for semantic retrieval.

Usage:
    python scripts/build_vectordb.py
    python scripts/build_vectordb.py --jsonl-dir processed/jsonl --vectordb-dir processed/vectordb
    python scripts/build_vectordb.py --force  # Re-embed all files
    python scripts/build_vectordb.py --device cuda  # Force GPU
    python scripts/build_vectordb.py --batch-size 64  # Larger batches for GPU
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.rag_embedder import EmbedPipelineConfig, run_embed_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Build ChromaDB vector database from JSONL evidence chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--jsonl-dir",
        type=str,
        default="data/processed/jsonl",
        help="Directory containing JSONL files from Stage 1 (default: data/processed/jsonl)",
    )
    parser.add_argument(
        "--vectordb-dir",
        type=str,
        default="data/processed/vectordb",
        help="Directory for ChromaDB persistence (default: data/processed/vectordb)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="BAAI/bge-m3",
        help="Sentence-transformer model name (default: BAAI/bge-m3)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        choices=["cuda", "cpu", None],
        help="Device for embedding (default: auto-detect)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for embedding (default: 32)",
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=8192,
        help="Maximum token length per chunk (default: 8192)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-embedding of all files, even if unchanged",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Resolve paths relative to project root
    jsonl_dir = (project_root / args.jsonl_dir).resolve()
    vectordb_dir = (project_root / args.vectordb_dir).resolve()

    print("=" * 60)
    print("  Stage 2: Building Vector Database")
    print("=" * 60)
    print(f"  JSONL dir:    {jsonl_dir}")
    print(f"  VectorDB dir: {vectordb_dir}")
    print(f"  Model:        {args.model}")
    print(f"  Device:       {args.device or 'auto'}")
    print(f"  Batch size:   {args.batch_size}")
    print(f"  Force:        {args.force}")
    print("=" * 60)
    print()

    # Run pipeline
    config = EmbedPipelineConfig(
        jsonl_dir=jsonl_dir,
        vectordb_dir=vectordb_dir,
        force=args.force,
        model_name=args.model,
        device=args.device,
        batch_size=args.batch_size,
        max_seq_length=args.max_seq_length,
    )

    try:
        summary = run_embed_pipeline(config)

        print()
        print("-" * 60)
        print("Stage 2 Pipeline Summary")
        print("-" * 60)
        print(f"  Total files:          {summary['total_files']}")
        print(f"  Files embedded:       {summary['files_embedded']}")
        print(f"  Files skipped:        {summary['files_skipped']}")
        print(f"  Files errored:        {summary['files_errored']}")
        print(f"  Total chunks embedded: {summary['total_chunks_embedded']}")
        print()

        stats = summary.get("vectordb_stats", {})
        print("Vector DB Statistics:")
        print(f"  Total chunks in DB:   {stats.get('total_chunks', 0)}")
        print(f"  Total sources:        {stats.get('total_sources', 0)}")
        print()

        dist = stats.get("doc_type_distribution", {})
        if dist:
            print("  Doc type distribution:")
            for dt, count in sorted(dist.items(), key=lambda x: -x[1]):
                print(f"    {dt:<30s} {count:>6d} chunks")
        print()

        print("Processed files:")
        for pf in summary.get("processed_files", []):
            status_icon = {"embedded": "[OK]", "skipped": "[SKIP]", "error": "[ERR]"}.get(
                pf["status"], "[?]"
            )
            chunks = pf.get("chunks", 0)
            extra = f" ({pf.get('embed_time_sec', 0):.1f}s)" if "embed_time_sec" in pf else ""
            if "error" in pf:
                extra = f" -- {pf['error']}"
            print(f"  {status_icon} {pf['file']:<40s} {chunks:>6d} chunks{extra}")

        print()
        print("-" * 60)
        print("[OK] Vector database built successfully!")
        print(f"    Location: {vectordb_dir}")
        print("-" * 60)

    except Exception as e:
        print(f"\n[ERR] Pipeline failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
