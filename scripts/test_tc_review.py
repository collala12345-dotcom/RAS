#!/usr/bin/env python
"""
Test script for TC Review with Keyword-based RAG.

This script demonstrates the TC Review process using the Keyword Retriever
instead of VectorDB (due to company firewall restrictions).

Usage:
    python scripts/test_tc_review.py
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tc_reviewer import ReviewConfig, ReviewEngine, Evidence

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Test TC Review with Keyword-based RAG."""
    
    # Configuration
    tc_v1_path = Path(__file__).parent.parent / "sample_data" / "sample_tc_v1.md"
    feature_id = "COM_overshooting_detection"
    sw_package = "SVR26A"
    rapp_name = "COM"
    
    logger.info("=" * 60)
    logger.info("TC Review Test with Keyword-based RAG")
    logger.info("=" * 60)
    logger.info(f"TC v1 Path: {tc_v1_path}")
    logger.info(f"Feature ID: {feature_id}")
    logger.info(f"RAPP Name: {rapp_name}")
    logger.info("=" * 60)
    
    # Create config
    config = ReviewConfig(
        tc_v1_path=tc_v1_path,
        feature_id=feature_id,
        sw_package=sw_package,
        rapp_name=rapp_name,
        search_keywords=[
            "overshooting detection",
            "coverage hole",
            "threshold",
            "KPI",
            "NE List",
            "COM algorithm",
        ],
    )
    
    # Create review engine
    review_engine = ReviewEngine(config)
    
    # Mock requirements for testing (since _extract_requirements is TODO)
    # In real usage, this would be extracted from FR
    mock_requirements = [
        {"keyword": "overshooting detection", "doc_type": "hld", "feature_area": "detection", "rapp": "COM"},
        {"keyword": "threshold KPI", "doc_type": "3gpp", "feature_area": "KPI", "rapp": "COM"},
        {"keyword": "NE List", "doc_type": "hld", "feature_area": "configuration", "rapp": "COM"},
        {"keyword": "coverage hole", "doc_type": "algorithm", "feature_area": "resolution", "rapp": "COM"},
        {"keyword": "detection switch", "doc_type": "hld", "feature_area": "control", "rapp": "COM"},
    ]
    
    logger.info("\nMock Requirements (simulating FR extraction):")
    for i, req in enumerate(mock_requirements, 1):
        logger.info(f"  {i}. {req['keyword']} (type: {req['doc_type']})")
    
    # Test evidence retrieval
    logger.info("\n" + "=" * 60)
    logger.info("Retrieving Evidence using Keyword Search...")
    logger.info("=" * 60)
    
    evidence_list = review_engine._retrieve_evidence(mock_requirements)
    
    if not evidence_list:
        logger.warning("No evidence retrieved!")
        logger.info("\nThis is expected if the Keyword Retriever is not properly connected.")
        return
    
    logger.info(f"\nRetrieved {len(evidence_list)} pieces of evidence")
    
    # Group by source document
    by_source = {}
    for ev in evidence_list:
        source = ev.source_path.split("\\")[-1][:50]
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(ev)
    
    logger.info("\nEvidence by Source Document:")
    for source, evs in sorted(by_source.items()):
        logger.info(f"\n  {source} ({len(evs)} chunks):")
        for ev in evs[:3]:  # Show top 3 per source
            logger.info(f"    - Score: {ev.score:.2f}, Title: {ev.title[:50]}...")
    
    # Show detailed evidence samples
    logger.info("\n" + "=" * 60)
    logger.info("Evidence Samples (Top 5 by Score):")
    logger.info("=" * 60)
    
    sorted_evidence = sorted(evidence_list, key=lambda x: x.score, reverse=True)
    for i, ev in enumerate(sorted_evidence[:5], 1):
        logger.info(f"\n[{i}] Score: {ev.score:.2f} | Priority: {ev.priority}")
        logger.info(f"    Source: {ev.source_path.split('\\\\')[-1]}")
        logger.info(f"    Section: {ev.section}")
        logger.info(f"    Text Preview: {ev.text[:200].replace(chr(10), ' ')}...")
        logger.info(f"    Confidence: {ev.confidence:.2f}")
    
    logger.info("\n" + "=" * 60)
    logger.info("TC Review Test Completed!")
    logger.info("=" * 60)
    
    # Summary
    logger.info("\nSummary:")
    logger.info(f"  - Total evidence retrieved: {len(evidence_list)}")
    logger.info(f"  - Unique source documents: {len(by_source)}")
    logger.info(f"  - Average confidence: {sum(e.confidence for e in evidence_list) / len(evidence_list):.2f}" if evidence_list else "  - No evidence")


if __name__ == "__main__":
    main()
