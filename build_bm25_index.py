#!/usr/bin/env python3
"""
BM25 Keyword Index Builder

data/processed/jsonl/ 폴더의 모든 JSONL 파일을 사용하여
BM25 인덱스를 생성하고 캐시에 저장합니다.

이 스크립트는 process_new_docs.py 실행 후 자동으로 호출되지만,
수동으로 실행할 수도 있습니다.

Usage:
    python functions/tools/build_bm25_index.py
"""

from __future__ import annotations

import sys
from pathlib import Path


def build_bm25_index() -> bool:
    """
    BM25 Keyword Index 를 새로 빌드합니다.
    
    Returns:
        bool: 성공 시 True, 실패 시 False
    """
    print("\n" + "=" * 60)
    print("BM25 Keyword Index 빌드")
    print("=" * 60)
    
    try:
        # Add functions/ to sys.path for proper import
        functions_dir = Path(__file__).parent.parent
        if str(functions_dir) not in sys.path:
            sys.path.insert(0, str(functions_dir))
        
        from src.rag_embedder.keyword_retriever import KeywordRetriever, KeywordRetrieverConfig
        
        config = KeywordRetrieverConfig(
            jsonl_dir=Path("data/processed/jsonl"),
            index_file=Path("data/processed/keyword_index.json"),
            bm25_k1=1.5,
            bm25_b=0.75,
        )
        
        retriever = KeywordRetriever(config)
        
        # 인덱스 빌드 (JSONL 파일 읽기)
        print("  [1/2] Building BM25 index from JSONL files...")
        retriever.load()
        # Note: retriever.load() automatically saves to cache via self.index.save_index()
        
        # 캐시에 저장 완료 (load() 에서 자동 저장됨)
        print("  [2/2] Index saved to cache (auto-saved by load())")
        
        # 통계 출력
        stats = retriever.get_stats()
        print(f"  [OK] BM25 인덱스 생성 완료!")
        print(f"    - Total chunks: {stats['total_chunks']}")
        print(f"    - Vocabulary size: {stats['vocabulary_size']}")
        print(f"    - Avg doc length: {stats['avg_doc_length']:.1f} words")
        
        return True
        
    except Exception as e:
        print(f"  [ERR] BM25 인덱스 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    build_bm25_index()
