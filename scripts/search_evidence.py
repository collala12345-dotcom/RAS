#!/usr/bin/env python3
"""
search_evidence.py — CLI tool to search the vector database for evidence.

Tests the RAG retrieval system by querying the ChromaDB vector database
with natural language queries or TC keywords.

Usage:
    python scripts/search_evidence.py "overshooting cell detection"
    python scripts/search_evidence.py "NE List carrier frequency" --top-k 10
    python scripts/search_evidence.py --fr FR10
    python scripts/search_evidence.py "coverage optimization" --doc-type 3gpp_docs
    python scripts/search_evidence.py --priority "COM rAPP detection resolution"
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

from src.rag_embedder import Embedder, Retriever, VectorDB


def main():
    parser = argparse.ArgumentParser(
        description="Search the ChromaDB vector database for evidence chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Query input (mutually exclusive group)
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Natural language search query",
    )
    query_group.add_argument(
        "--fr",
        type=str,
        help="Search by FR ID (e.g., FR10)",
    )

    # Search options
    parser.add_argument(
        "--vectordb-dir",
        type=str,
        default="processed/vectordb",
        help="Directory for ChromaDB (default: processed/vectordb)",
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
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return (default: 5)",
    )
    parser.add_argument(
        "--doc-type",
        type=str,
        default=None,
        help="Filter by doc_type (e.g., 3gpp_docs, feature_specs)",
    )
    parser.add_argument(
        "--priority",
        action="store_true",
        help="Use priority-based search across all doc_types",
    )
    parser.add_argument(
        "--full-text",
        action="store_true",
        help="Show full text of each result (not just preview)",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Resolve paths
    vectordb_dir = (project_root / args.vectordb_dir).resolve()

    if not vectordb_dir.exists():
        print(f"[ERR] Vector DB not found at: {vectordb_dir}", file=sys.stderr)
        print("   Run 'python scripts/build_vectordb.py' first.", file=sys.stderr)
        sys.exit(1)

    # Initialize components
    print("Loading embedding model and vector database...", file=sys.stderr)
    embedder = Embedder(
        model_name=args.model,
        device=args.device,
    )
    vectordb = VectorDB(db_path=vectordb_dir)
    retriever = Retriever(vectordb=vectordb, embedder=embedder, default_top_k=args.top_k)

    # Show DB stats
    stats = vectordb.get_stats()
    print(f"Vector DB: {stats['total_chunks']} chunks from {stats['total_sources']} sources",
          file=sys.stderr)
    print(file=sys.stderr)

    # Perform search
    if args.fr:
        results = retriever.search_by_fr(args.fr, top_k=args.top_k)
    elif args.priority:
        results = retriever.search_by_priority(
            args.query,
            top_k_per_type=args.top_k,
        )
    else:
        results = retriever.search(
            args.query,
            doc_type_filter=args.doc_type,
            top_k=args.top_k,
        )

    # Output results
    if args.json_output:
        print(json.dumps(results.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_results(results, show_full=args.full_text)


def _print_results(results, show_full: bool = False):
    """Pretty-print search results."""
    print("-" * 70)
    print(f"Query: {results.query}")
    print(f"Results: {len(results.results)}")
    print("-" * 70)

    if not results.results:
        print("  (No results found)")
        return

    for r in results.results:
        print()
        print(f"  +-- Rank #{r.rank} " + "-" * 46)
        print(f"  | Score:      {r.score:.4f}")
        print(f"  | Doc Type:   {r.doc_type}")
        print(f"  | Source:     {r.source_path}")
        print(f"  | Lines:      {r.start_line}-{r.end_line}")
        print(f"  | Section:    {r.section}")
        print(f"  | Title:      {r.title}")
        if isinstance(r.heading_path, list) and r.heading_path:
            print(f"  | Heading:    {' > '.join(r.heading_path)}")
        elif r.heading_path:
            print(f"  | Heading:    {r.heading_path}")
        print(f"  | Chunk ID:   {r.chunk_id}")
        print(f"  +-- Text " + "-" * 50)

        if show_full:
            # Print full text with indentation
            for line in r.text.split("\n"):
                print(f"  | {line}")
        else:
            # Print preview (first 300 chars)
            preview = r.text[:300]
            if len(r.text) > 300:
                preview += "..."
            for line in preview.split("\n"):
                print(f"  | {line}")

        print(f"  " + "-" * 58)


if __name__ == "__main__":
    main()
