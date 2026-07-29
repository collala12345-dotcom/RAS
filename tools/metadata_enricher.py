#!/usr/bin/env python3
"""
JSONL Metadata Enricher Tool

JSONL chunk 에 source_file, page_number, slide_number metadata 를 추가합니다.

Usage:
    python functions/tools/metadata_enricher.py [jsonl_dir]
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional


def find_md_file(source_path: str, search_dirs: list[Path]) -> Optional[Path]:
    """Find MD file based on source_path."""
    rel_path = source_path.replace('data\\', 'data/').replace('data/', '')
    
    for search_dir in search_dirs:
        candidate = search_dir / rel_path
        if candidate.exists():
            return candidate
    
    if '3gpp_docs' in rel_path and 'raw' not in rel_path:
        rel_path = rel_path.replace('3gpp_docs', 'raw/3gpp_docs')
        for search_dir in search_dirs:
            candidate = search_dir / rel_path
            if candidate.exists():
                return candidate
    
    return None


def extract_page_info_from_md(md_path: Path) -> dict[int, int]:
    """Extract line number to page number mapping from MD file."""
    line_to_page: dict[int, int] = {}
    current_page = 1
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.rstrip()
            
            # 3GPP heading: "## Title\t33"
            heading_match = re.match(r'^(#+)\s+(.+?)\t(\d+)\s*$', line)
            if heading_match:
                page_num = int(heading_match.group(3))
                heading_text = heading_match.group(2)
                if 'page' not in heading_text.lower() and 'slide' not in heading_text.lower():
                    current_page = page_num
            
            # TOC entry: "1\tScope\t25"
            elif not line.startswith('#') and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2 and parts[-1].isdigit():
                    page_num = int(parts[-1])
                    if parts[0].replace('.', '').isdigit():
                        current_page = page_num
            
            line_to_page[line_num] = current_page
        
    except Exception as e:
        print(f"  [WARN] Error reading {md_path}: {e}")
    
    return line_to_page


def find_original_file(md_path: Path, search_dirs: list[Path]) -> tuple[Optional[str], str]:
    """Find original file (DOCX, PPTX, PDF) corresponding to MD file."""
    md_name = md_path.stem
    
    parent_dir = md_path.parent
    for ext in ['.docx', '.pptx', '.pdf']:
        candidate = parent_dir / f"{md_name}{ext}"
        if candidate.exists():
            return candidate.name, ext[1:].upper()
    
    for search_dir in search_dirs:
        for ext in ['.docx', '.pptx', '.pdf']:
            candidate = search_dir / f"{md_name}{ext}"
            if candidate.exists():
                return candidate.name, ext[1:].upper()
    
    if 'pptx' in md_name.lower():
        return f"{md_name}.pptx", "PPTX"
    elif 'pdf' in md_name.lower():
        return f"{md_name}.pdf", "PDF"
    else:
        return f"{md_name}.docx", "DOCX"


def enrich_chunk(chunk: dict, search_dirs: list[Path], md_cache: dict) -> dict:
    """Enrich chunk with source_file and page_number metadata."""
    source_path = chunk.get('source_path', '')
    if not source_path:
        return chunk
    
    if source_path not in md_cache:
        md_path = find_md_file(source_path, search_dirs)
        if md_path:
            source_file, file_format = find_original_file(md_path, search_dirs)
            line_to_page = extract_page_info_from_md(md_path)
            
            md_cache[source_path] = {
                'md_path': md_path,
                'source_file': source_file,
                'file_format': file_format,
                'line_to_page': line_to_page,
            }
        else:
            md_cache[source_path] = None
    
    file_info = md_cache.get(source_path)
    if not file_info:
        return chunk
    
    if 'metadata' not in chunk:
        chunk['metadata'] = {}
    
    if file_info['source_file']:
        chunk['metadata']['source_file'] = file_info['source_file']
    
    start_line = chunk.get('start_line', 1)
    page_num = file_info['line_to_page'].get(start_line)
    if page_num is not None:
        chunk['metadata']['page_number'] = page_num
    
    return chunk


def process_jsonl_file(jsonl_path: Path, search_dirs: list[Path], md_cache: dict) -> int:
    """Process a single JSONL file."""
    updated_count = 0
    updated_chunks = []
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    chunk = json.loads(line)
                    chunk = enrich_chunk(chunk, search_dirs, md_cache)
                    updated_chunks.append(chunk)
                    updated_count += 1
        
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for chunk in updated_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        
    except Exception as e:
        print(f"  [ERROR] {jsonl_path.name}: {e}")
        return 0
    
    return updated_count


def main():
    import sys
    
    base_dir = Path('c:/Users/jy2601.kim/RAS-TestCaseReview')
    jsonl_dir_arg = sys.argv[1] if len(sys.argv) > 1 else None
    jsonl_dir = Path(jsonl_dir_arg) if jsonl_dir_arg else base_dir / 'data/processed/jsonl'
    
    search_dirs = [
        base_dir / 'data/raw',
        base_dir / 'data',
        base_dir / 'data/raw/3gpp_docs',
        base_dir / 'data/3gpp_docs',
    ]
    
    for subdir in ['algorithm_docs', 'hld_dld', 'feature_specs', 'issue_cases', 'legacy_tc']:
        subdir_path = base_dir / 'data' / subdir
        if subdir_path.exists():
            search_dirs.append(subdir_path)
    
    print("="*70)
    print("JSONL Metadata Enrichment Tool")
    print("="*70)
    print(f"JSONL directory: {jsonl_dir}")
    print(f"Search directories: {len(search_dirs)}")
    print()
    
    jsonl_files = list(jsonl_dir.glob("*.jsonl"))
    print(f"Found {len(jsonl_files)} JSONL files")
    print()
    
    md_cache: dict = {}
    total_updated = 0
    files_with_source = 0
    files_with_page = 0
    
    for i, jsonl_file in enumerate(jsonl_files, 1):
        print(f"[{i}/{len(jsonl_files)}] {jsonl_file.name}...", end=" ")
        
        count = process_jsonl_file(jsonl_file, search_dirs, md_cache)
        total_updated += count
        
        if md_cache:
            first_info = next(iter(md_cache.values()))
            if first_info:
                if first_info.get('source_file'):
                    files_with_source += 1
                if first_info.get('line_to_page'):
                    files_with_page += 1
        
        print(f"OK ({count} chunks)")
    
    print()
    print("="*70)
    print(f"Total updated chunks: {total_updated}")
    print(f"Files with source_file metadata: {files_with_source}")
    print(f"Files with page_number mapping: {files_with_page}")
    print("="*70)


if __name__ == "__main__":
    main()
