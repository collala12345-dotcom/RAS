#!/usr/bin/env python
"""
Test script for Keyword-based RAG Retriever.

This script tests the BM25 keyword search functionality
without requiring any embedding model downloads.

Usage:
    python scripts/test_keyword_search.py
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_embedder.keyword_retriever import (
    KeywordRetriever,
    KeywordRetrieverConfig,
    search_jsonl,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Test keyword search functionality."""
    
    # Configuration
    jsonl_dir = Path(__file__).parent.parent / "processed" / "jsonl"
    index_file = Path(__file__).parent.parent / "processed" / "keyword_index.json"
    
    logger.info(f"JSONL directory: {jsonl_dir}")
    logger.info(f"Index file: {index_file}")
    
    # Check if JSONL directory exists
    if not jsonl_dir.exists():
        logger.error(f"JSONL directory not found: {jsonl_dir}")
        logger.info("Please run 'python scripts/build_jsonl.py' first to create JSONL files")
        return
    
    # Create retriever
    config = KeywordRetrieverConfig(
        jsonl_dir=jsonl_dir,
        index_file=index_file,
        bm25_k1=1.5,
        bm25_b=0.75,
    )
    
    retriever = KeywordRetriever(config)
    
    # Try to load from cache first
    if retriever.load_from_cache():
        logger.info("Loaded index from cache (fast!)")
    else:
        logger.info("Building index from JSONL files (this may take a moment...)")
        retriever.load()
    
    # Get stats
    stats = retriever.get_stats()
    logger.info("=" * 60)
    logger.info("Index Statistics:")
    logger.info(f"  Total chunks: {stats['total_chunks']}")
    logger.info(f"  Total documents: {stats['total_documents']}")
    logger.info(f"  Avg doc length: {stats['avg_doc_length']:.1f} words")
    logger.info(f"  Vocabulary size: {stats['vocabulary_size']} unique terms")
    logger.info("=" * 60)
    
    # Test queries
    test_queries = [
        ("overshooting detection", "COM"),
        ("coverage hole", "3gpp"),
        ("threshold KPI", None),
        ("handover algorithm", "algorithm"),
    ]
    
    for query, doc_type in test_queries:
        logger.info(f"\n📝 Query: '{query}' (doc_type: {doc_type or 'all'})")
        logger.info("-" * 40)
        
        results = retriever.search(
            query=query,
            doc_type_filter=doc_type,
            top_k=3,
            min_score=0.1,
        )
        
        if not results:
            logger.info("  No results found")
            continue
        
        for i, result in enumerate(results, 1):
            logger.info(f"\n  [{i}] Score: {result.score:.4f}")
            logger.info(f"      Source: {result.source_path}")
            text_preview = result.text[:150].replace("\n", " ")
            logger.info(f"      Text: {text_preview}...")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Keyword search test completed!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
