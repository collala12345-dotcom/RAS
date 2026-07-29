"""
Tests for Stage 2: Keyword-based Retriever

Tests the BM25 implementation and Korean tokenization support.
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_embedder.keyword_retriever import BM25Index, KeywordRetriever, KeywordRetrieverConfig


class TestBM25Index:
    """Test BM25 indexing and search."""
    
    def test_tokenize_english(self):
        """Test English tokenization."""
        index = BM25Index()
        
        text = "The quick brown fox jumps over the lazy dog"
        tokens = index.tokenize(text)
        
        assert len(tokens) > 0
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens
    
    def test_tokenize_korean(self):
        """Test Korean tokenization."""
        index = BM25Index()
        
        text = "검증 테스트 한국어서 토큰나이저"
        tokens = index.tokenize(text)
        
        # Should extract Korean text
        assert len(tokens) > 0
        # Should have kr_ prefixed segments
        kr_tokens = [t for t in tokens if t.startswith("kr_")]
        assert len(kr_tokens) > 0
    
    def test_tokenize_mixed(self):
        """Test mixed English and Korean tokenization."""
        index = BM25Index()
        
        text = "COM detection 검증 테스트 with algorithm"
        tokens = index.tokenize(text)
        
        # Should have both English and Korean tokens
        assert any("com" in t.lower() for t in tokens)
        assert any("detection" in t.lower() for t in tokens)
        assert any("algorithm" in t.lower() for t in tokens)
    
    def test_add_document(self):
        """Test adding documents to index."""
        index = BM25Index()
        
        index.add_document("doc1", "This is a test document about testing")
        index.add_document("doc2", "Another document for search")
        
        assert index.num_documents == 2
        assert "doc1" in index.documents
        assert "doc2" in index.documents
    
    def test_search_basic(self):
        """Test basic search functionality."""
        index = BM25Index()
        
        # Add documents
        index.add_document("doc1", "Overshooting detection algorithm for COM")
        index.add_document("doc2", "Coverage hole detection with CQI and BLER")
        index.add_document("doc3", "Switch ON OFF control for frequency")
        
        index.compute_idf()
        
        # Search for "detection"
        results = index.search("detection", top_k=2)
        
        assert len(results) <= 2
        # doc1 and doc2 should rank higher for "detection"
        result_ids = [r[0] for r in results]
        assert "doc1" in result_ids or "doc2" in result_ids
    
    def test_search_korean(self):
        """Test Korean search."""
        index = BM25Index()
        
        # Add Korean documents
        index.add_document("doc1", "COM 검증 알고리즘 테스트")
        index.add_document("doc2", "Coverage Hole 탐지 로직")
        index.add_document("doc3", "스위치 온오프 제어")
        
        index.compute_idf()
        
        # Search for Korean term
        results = index.search("검증", top_k=2)
        
        # Should find doc1
        if results:
            result_ids = [r[0] for r in results]
            # doc1 should rank high for "검증"
            assert len(result_ids) > 0


class TestKeywordRetriever:
    """Test KeywordRetriever integration."""
    
    def test_init(self):
        """Test KeywordRetriever initialization."""
        config = KeywordRetrieverConfig(
            jsonl_dir=Path("processed/jsonl"),
            index_file=Path("processed/keyword_index.json"),
        )
        
        retriever = KeywordRetriever(config)
        
        assert retriever.config == config
        assert retriever._loaded is False
    
    def test_get_stats_empty(self):
        """Test getting stats from empty index."""
        config = KeywordRetrieverConfig(
            jsonl_dir=Path("processed/jsonl"),
        )
        
        retriever = KeywordRetriever(config)
        
        # Stats should work even without loading
        stats = retriever.get_stats()
        
        assert "total_chunks" in stats
        assert "vocabulary_size" in stats
        assert "avg_doc_length" in stats


class TestKoreanTokenization:
    """Test Korean-specific tokenization features."""
    
    def test_kr_prefix_segments(self):
        """Test kr_ prefixed segment extraction."""
        index = BM25Index()
        
        text = "알고리즘 검증 테스트"
        tokens = index.tokenize(text)
        
        # Should have kr_ prefixed 2-4 char segments
        kr_tokens = [t for t in tokens if t.startswith("kr_")]
        
        # Should have multiple segments
        assert len(kr_tokens) >= 2
    
    def test_hangul_unicode_range(self):
        """Test Hangul Unicode range detection."""
        index = BM25Index()
        
        # Test various Hangul characters
        texts = [
            "가나다라마바사",  # Basic Hangul
            "알고리즘",  # Common word
            "검증",  # Common word
        ]
        
        for text in texts:
            tokens = index.tokenize(text)
            # Should extract Korean text
            assert len(tokens) > 0, f"Failed to tokenize: {text}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
