#!/usr/bin/env python3
"""
Add metadata to existing JSONL files that are missing it.

This script:
1. Reads all JSONL files from data/processed/jsonl/
2. Finds corresponding MD files (including nested subdirectories)
3. Adds missing metadata:
   - metadata.source_file: original filename (DOCX/PPTX/PDF)
   - metadata.page_number: page number from MD heading
   - metadata.related_rapp: rAPP name (extracted from filename)
   - metadata.related_function: function name (extracted from filename/content)
   - metadata.review_role: review role (inferred from doc_type)

Usage:
    python functions/tools/add_metadata_to_existing_jsonl.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional


def find_md_file_for_jsonl(source_path: str) -> Optional[Path]:
    """
    Find MD file corresponding to JSONL source_path.
    Searches recursively in all subdirectories.
    
    Tries multiple strategies:
    1. Direct path from source_path
    2. Stem-based search in data/raw/ and data/3gpp_docs/
    3. Fuzzy match (ignore underscores/hyphens)
    """
    source_name = Path(source_path).stem
    
    # Strategy 1: Try direct path from source_path
    # e.g., source_path = "data\\raw\\3gpp_docs\\28540-k20\\28540-k20.md"
    direct_path = Path(source_path)
    if direct_path.exists() and direct_path.suffix == '.md':
        return direct_path
    
    # Strategy 2: Search recursively in all subdirectories
    base_dirs = [
        Path("data/raw"),
        Path("data/3gpp_docs"),
    ]
    
    for base_dir in base_dirs:
        if not base_dir.exists():
            continue
        for md_file in base_dir.rglob("*.md"):
            if md_file.stem == source_name:
                return md_file
    
    # Strategy 3: Fuzzy match (normalize name)
    normalized_source = source_name.replace('_', '-').replace('__', '-').lower()
    for base_dir in base_dirs:
        if not base_dir.exists():
            continue
        for md_file in base_dir.rglob("*.md"):
            normalized_md = md_file.stem.replace('_', '-').replace('__', '-').lower()
            if normalized_source in normalized_md or normalized_md in normalized_source:
                return md_file
    
    return None


def extract_page_mapping(md_path: Path) -> dict[int, int]:
    """
    Extract page number mapping from MD file.
    
    MD headings may contain page numbers like:
    - "## Abbreviations\t33" → page 33
    - "## 1. Introduction\t5" → page 5
    
    Returns: dict mapping line_number → page_number
    """
    page_mapping: dict[int, int] = {}
    current_page = 1
    
    with open(md_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            match = re.match(r'^#+\s+.+?\t(\d+)\s*$', line)
            if match:
                current_page = int(match.group(1))
                page_mapping[line_num] = current_page
    
    return page_mapping


def get_page_for_line(line_num: int, page_mapping: dict[int, int]) -> int:
    """Get page number for a given line number."""
    if not page_mapping:
        return 1
    
    last_page = 1
    for mapping_line, page in sorted(page_mapping.items()):
        if mapping_line <= line_num:
            last_page = page
        else:
            break
    
    return last_page


def extract_related_rapp(filename: str, text: str) -> Optional[str]:
    """Extract related_rapp from filename or content."""
    filename_upper = filename.upper()
    
    rapp_patterns = [
        (r"COM", "COM"),
        (r"VISTA", "VISTA"),
        (r"ANALYTICS", "Analytics"),
        (r"SAMM", "SAMM"),
        (r"KAD", "KAD"),
        (r"ROI", "ROI"),
        (r"ML", "ML"),
        (r"AI", "AI"),
        (r"TCE", "TCE"),
    ]
    
    for pattern, rapp_name in rapp_patterns:
        if re.search(pattern, filename_upper):
            return rapp_name
    
    for pattern, rapp_name in rapp_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return rapp_name
    
    return None


def extract_related_function(filename: str, text: str) -> Optional[str]:
    """Extract related_function from filename or content."""
    filename_upper = filename.upper()
    text_upper = text.upper()
    
    func_patterns = [
        (r"OVERSHOOTING", "Overshooting_Detection"),
        (r"COVERAGE", "Coverage_Optimization"),
        (r"CAPACITY", "Capacity_Optimization"),
        (r"INTERFERENCE", "Interference_Management"),
        (r"LOAD\s*BALANC", "Load_Balancing"),
        (r"ENERGY\s*SAV", "Energy_Saving"),
        (r"QOS", "QoS_Management"),
        (r"HANDOVER", "Handover_Optimization"),
        (r"RETRANSMISSION", "Retransmission_Optimization"),
        (r"SCHEDULING", "Scheduling_Optimization"),
        (r"NRM", "NRM"),
        (r"SCHEMA", "Schema_Management"),
        (r"API\s*COMMAND", "API_Command"),
        (r"FAULT", "Fault_Management"),
        (r"PERF", "Performance_Management"),
        (r"CONFIG", "Configuration_Management"),
    ]
    
    for pattern, func_name in func_patterns:
        if re.search(pattern, filename_upper):
            return func_name
    
    for pattern, func_name in func_patterns:
        if re.search(pattern, text_upper[:1000]):
            return func_name
    
    return None


def extract_review_role(doc_type: str) -> str:
    """Extract review_role from doc_type."""
    role_map = {
        "3gpp_docs": "requirement_reviewer",
        "hld_dld": "design_reviewer",
        "algorithm_docs": "algorithm_reviewer",
        "feature_specs": "feature_reviewer",
        "legacy_tc": "tc_reviewer",
        "issue_cases": "issue_analyst",
        "review_comments": "reviewer",
        "test_results": "test_engineer",
        "pegs": "peg_reviewer",
    }
    return role_map.get(doc_type, "general_reviewer")


def process_jsonl_file(jsonl_path: Path) -> int:
    """Process a single JSONL file and add metadata."""
    updated_count = 0
    skipped_count = 0
    
    # Find corresponding MD file
    md_path = find_md_file_for_jsonl(str(jsonl_path))
    if not md_path:
        print(f"  [WARN] MD file not found for {jsonl_path.name}")
        return 0, 0
    
    # Extract page mapping from MD
    page_mapping = extract_page_mapping(md_path)
    
    # Determine source_file from MD path
    source_file = md_path.name
    for ext in ['.docx', '.pptx', '.pdf']:
        original = md_path.with_suffix(ext)
        if original.exists():
            source_file = original.name
            break
    
    # Get doc_type from filename
    jsonl_str = str(jsonl_path).lower()
    if "3gpp" in jsonl_str:
        doc_type = "3gpp_docs"
    elif "hld" in jsonl_str or "dld" in jsonl_str:
        doc_type = "hld_dld"
    elif "algorithm" in jsonl_str:
        doc_type = "algorithm_docs"
    elif "tc" in jsonl_str or "test" in jsonl_str:
        doc_type = "legacy_tc"
    elif "issue" in jsonl_str or "bug" in jsonl_str:
        doc_type = "issue_cases"
    else:
        doc_type = "unknown"
    
    # Read and update JSONL
    updated_rows = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            chunk = json.loads(line)
            
            # Skip if metadata already exists
            if 'metadata' in chunk and chunk['metadata'].get('review_role'):
                skipped_count += 1
                updated_rows.append(chunk)
                continue
            
            # Update metadata
            if 'metadata' not in chunk:
                chunk['metadata'] = {}
            
            # Add source_file
            chunk['metadata']['source_file'] = source_file
            
            # Add page_number based on start_line
            start_line = chunk.get('start_line', 1)
            page_number = get_page_for_line(start_line, page_mapping)
            chunk['metadata']['page_number'] = page_number
            
            # Add related_rapp (preserve existing if present)
            if 'related_rapp' not in chunk['metadata']:
                rapp = extract_related_rapp(md_path.name, chunk.get('text', ''))
                if rapp:
                    chunk['metadata']['related_rapp'] = rapp
            
            # Add related_function (preserve existing if present)
            if 'related_function' not in chunk['metadata']:
                func = extract_related_function(md_path.name, chunk.get('text', ''))
                if func:
                    chunk['metadata']['related_function'] = func
            
            # Add review_role (preserve existing if present)
            if 'review_role' not in chunk['metadata']:
                chunk['metadata']['review_role'] = extract_review_role(doc_type)
            
            updated_rows.append(chunk)
            updated_count += 1
    
    # Write updated JSONL
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for row in updated_rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    
    return updated_count, skipped_count


def main():
    """Main function."""
    jsonl_dir = Path("data/processed/jsonl")
    
    if not jsonl_dir.exists():
        print(f"Error: {jsonl_dir} does not exist")
        return
    
    print("=" * 60)
    print("Add metadata to existing JSONL files")
    print("=" * 60)
    
    total_files = 0
    total_updated = 0
    total_skipped = 0
    
    for jsonl_file in sorted(jsonl_dir.glob("*.jsonl")):
        print(f"\nProcessing: {jsonl_file.name}")
        
        try:
            updated, skipped = process_jsonl_file(jsonl_file)
            total_files += 1
            total_updated += updated
            total_skipped += skipped
            if updated > 0:
                print(f"  [OK] Updated {updated} chunks")
            if skipped > 0:
                print(f"  [SKIP] Already has metadata: {skipped} chunks")
        except Exception as e:
            print(f"  [ERR] Error: {e}")
    
    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  Files processed: {total_files}")
    print(f"  Chunks updated: {total_updated}")
    print(f"  Chunks skipped (already has metadata): {total_skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
