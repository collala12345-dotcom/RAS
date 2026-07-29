#!/usr/bin/env python3
"""
JSONL Metadata Enrichment Tool - v2

모든 JSONL chunk 에 대해 raw data 의 형식에 따른 metadata 를 추가합니다:
- PDF: page_number
- PPTX: slide_number
- MD/DOCX: line 정보 (start_line, end_line) - 이미 존재

데이터 흐름:
1. processed/jsonl/ 의 모든 JSONL 파일 읽기
2. source_path 로 원본 MD 파일 찾기
3. MD 파일에서 Slide/Page 번호 추출
4. 원본 파일명 (PPTX, PDF) 찾기
5. metadata 에 추가: source_file, slide_number, page_number

Usage:
    python tools/enrich_all_jsonl_metadata.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any


def find_md_file(source_path: str, search_dirs: list[Path]) -> Optional[Path]:
    """
    source_path 를 기반으로 MD 파일을 찾습니다.
    
    Args:
        source_path: JSONL 의 source_path 필드
        search_dirs: 검색할 디렉토리 목록
        
    Returns:
        MD 파일 경로 또는 None
    """
    # source_path 를 상대 경로로 변환
    # 예: data\3gpp_docs\28536-j20\28536-j20.md → 3gpp_docs\28536-j20\28536-j20.md
    rel_path = source_path.replace('data\\', '').replace('data/', '')
    
    for search_dir in search_dirs:
        candidate = search_dir / rel_path
        if candidate.exists():
            return candidate
    
    return None


def find_original_file(md_path: Path, search_dirs: list[Path]) -> Optional[str]:
    """
    MD 파일에 대응하는 원본 파일 (PPTX, PDF, DOCX) 을 찾습니다.
    
    Args:
        md_path: MD 파일 경로
        search_dirs: 검색할 디렉토리 목록
        
    Returns:
        원본 파일명 (확장자 포함) 또는 None
    """
    md_name = md_path.stem
    
    # 1. 같은 폴더에서 원본 파일 검색
    parent_dir = md_path.parent
    for ext in ['.pptx', '.pdf', '.docx']:
        candidate = parent_dir / f"{md_name}{ext}"
        if candidate.exists():
            return candidate.name
    
    # 2. search_dirs 에서 원본 파일 검색
    for search_dir in search_dirs:
        for ext in ['.pptx', '.pdf', '.docx']:
            candidate = search_dir / f"{md_name}{ext}"
            if candidate.exists():
                return candidate.name
    
    return None


def extract_page_slide_info(md_path: Path) -> tuple[Optional[int], Optional[int]]:
    """
    MD 파일에서 page/slide 번호를 추출합니다.
    
    Args:
        md_path: MD 파일 경로
        
    Returns:
        (slide_number, page_number) 튜플
    """
    slide_number = None
    page_number = None
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Slide 번호 추출 (PPTX)
        # 패턴: ## Slide 12: 제목 또는 ## Slide 12
        slide_match = re.search(r'##\s*Slide\s+(\d+)', content)
        if slide_match:
            slide_number = int(slide_match.group(1))
        
        # Page 번호 추출 (PDF)
        # 패턴: <!-- Page 45 --> 또는 <!-- Page: 45 -->
        page_match = re.search(r'<!--\s*Page\s*:?\s*(\d+)\s*-->', content)
        if page_match:
            page_number = int(page_match.group(1))
        
    except Exception as e:
        pass  # 에러 발생 시 None 반환
    
    return slide_number, page_number


def extract_source_file_from_heading(md_path: Path) -> Optional[str]:
    """
    MD 파일의 heading 에서 원본 파일명을 추출합니다.
    
    Args:
        md_path: MD 파일 경로
        
    Returns:
        원본 파일명 또는 None
    """
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            first_lines = f.read(2000)  # 첫 2000 자만 읽기
        
        # 파일명 패턴 검색 (확장자 포함)
        patterns = [
            r'([A-Za-z0-9_\-\[\]\(\)\s]+\.pptx)',
            r'([A-Za-z0-9_\-\[\]\(\)\s]+\.pdf)',
            r'([A-Za-z0-9_\-\[\]\(\)\s]+\.docx)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, first_lines)
            if match:
                return match.group(1).strip()
    
    except Exception:
        pass
    
    return None


def enrich_chunk(chunk: dict, search_dirs: list[Path], cache: dict) -> dict:
    """
    chunk metadata 에 source_file, slide_number, page_number 를 추가합니다.
    
    Args:
        chunk: JSONL chunk 데이터
        search_dirs: 검색할 디렉토리 목록
        cache: MD 파일 정보 캐시
        
    Returns:
        업데이트된 chunk 데이터
    """
    source_path = chunk.get('source_path', '')
    if not source_path:
        return chunk
    
    # 캐시에서 MD 파일 정보 가져오기
    if source_path not in cache:
        md_path = find_md_file(source_path, search_dirs)
        if md_path:
            slide_num, page_num = extract_page_slide_info(md_path)
            source_file = find_original_file(md_path, search_dirs)
            
            # source_file 이 없으면 heading 에서 추출 시도
            if not source_file and md_path:
                source_file = extract_source_file_from_heading(md_path)
            
            cache[source_path] = {
                'md_path': md_path,
                'slide_number': slide_num,
                'page_number': page_num,
                'source_file': source_file,
            }
        else:
            cache[source_path] = None
    
    file_info = cache.get(source_path)
    if not file_info:
        return chunk
    
    # metadata 필드 추가
    if 'metadata' not in chunk:
        chunk['metadata'] = {}
    
    if file_info['source_file']:
        chunk['metadata']['source_file'] = file_info['source_file']
    if file_info['slide_number'] is not None:
        chunk['metadata']['slide_number'] = file_info['slide_number']
    if file_info['page_number'] is not None:
        chunk['metadata']['page_number'] = file_info['page_number']
    
    # section 업데이트 (기존 section 이 있으면 유지)
    current_section = chunk.get('section', '')
    if file_info['slide_number'] is not None and 'Slide' not in current_section:
        chunk['section'] = f"Slide {file_info['slide_number']}" + (f": {current_section}" if current_section else '')
    elif file_info['page_number'] is not None and 'Page' not in current_section:
        chunk['section'] = f"Page {file_info['page_number']}" + (f": {current_section}" if current_section else '')
    
    return chunk


def process_jsonl_file(jsonl_path: Path, search_dirs: list[Path], cache: dict) -> int:
    """
    단일 JSONL 파일을 처리합니다.
    
    Args:
        jsonl_path: JSONL 파일 경로
        search_dirs: 검색할 디렉토리 목록
        cache: MD 파일 정보 캐시
        
    Returns:
        처리된 chunk 수
    """
    updated_count = 0
    updated_chunks = []
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    chunk = json.loads(line)
                    chunk = enrich_chunk(chunk, search_dirs, cache)
                    updated_chunks.append(chunk)
                    updated_count += 1
        
        # 업데이트된 JSONL 다시 쓰기
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for chunk in updated_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        
    except Exception as e:
        print(f"  [ERROR] {jsonl_path.name}: {e}")
        return 0
    
    return updated_count


def main():
    # 기본 경로 설정
    base_dir = Path('c:/Users/jy2601.kim/RAS-TestCaseReview')
    jsonl_dir = base_dir / 'data/processed/jsonl'
    
    # 검색할 디렉토리 목록
    # 1. data/raw/ - 원본 파일 보관소
    # 2. data/ - 루트 (하위 폴더 검색)
    search_dirs = [
        base_dir / 'data/raw',
        base_dir / 'data',
    ]
    
    # algorithm_docs, 3gpp_docs, hld_dld 등 하위 폴더도 추가
    for subdir in ['algorithm_docs', '3gpp_docs', 'hld_dld', 'feature_specs', 'issue_cases', 'legacy_tc']:
        subdir_path = base_dir / 'data' / subdir
        if subdir_path.exists():
            search_dirs.append(subdir_path)
    
    print("=" * 70)
    print("JSONL Metadata Enrichment Tool - v2")
    print("=" * 70)
    print(f"JSONL directory: {jsonl_dir}")
    print(f"Search directories: {len(search_dirs)}")
    for d in search_dirs:
        print(f"  - {d}")
    print()
    
    # JSONL 파일 목록
    jsonl_files = list(jsonl_dir.glob("*.jsonl"))
    print(f"Found {len(jsonl_files)} JSONL files")
    print()
    
    # 처리
    cache: Dict[str, Any] = {}
    total_updated = 0
    files_with_source = 0
    files_with_slide = 0
    files_with_page = 0
    
    for i, jsonl_file in enumerate(jsonl_files, 1):
        print(f"[{i}/{len(jsonl_files)}] {jsonl_file.name}...", end=" ")
        
        count = process_jsonl_file(jsonl_file, search_dirs, cache)
        total_updated += count
        
        # 통계 (캐시에서 첫 번째 결과만 확인)
        if cache:
            first_info = next(iter(cache.values()))
            if first_info:
                if first_info.get('source_file'):
                    files_with_source += 1
                if first_info.get('slide_number') is not None:
                    files_with_slide += 1
                if first_info.get('page_number') is not None:
                    files_with_page += 1
        
        print(f"OK ({count} chunks)")
    
    print()
    print("=" * 70)
    print(f"Total updated chunks: {total_updated}")
    print(f"Files with source_file: {files_with_source}")
    print(f"Files with slide_number: {files_with_slide}")
    print(f"Files with page_number: {files_with_page}")
    print("=" * 70)


if __name__ == "__main__":
    main()
