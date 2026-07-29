#!/usr/bin/env python3
"""
JSONL 폴더 병합 도구 - enriched_jsonl + jsonl 통합

enriched_jsonl 폴더의 풍부한 metadata 에
jsonl 폴더의 source_file, page_number 정보를 추가하여 병합합니다.

Usage:
    python functions/tools/merge_enriched_jsonl.py
"""

from __future__ import annotations

import json
import shutil
import copy
from pathlib import Path


def load_jsonl_file(file_path: Path) -> list[dict]:
    """JSONL 파일을 읽어서 chunk 리스트로 반환합니다."""
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    chunks.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"  [WARN] JSON decode error: {e}")
    return chunks


def save_jsonl_file(file_path: Path, chunks: list[dict]) -> None:
    """chunk 리스트를 JSONL 파일로 저장합니다."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')


def merge_chunk_metadata(enriched_chunk: dict, base_chunk: dict) -> dict:
    """
    enriched chunk 에 base chunk 의 metadata 정보를 병합합니다.
    
    - enriched_chunk 의 풍부한 metadata 유지 (v4_tc_review_enriched)
    - base chunk 의 source_file, page_number 정보만 추가
    """
    # enriched chunk 의 모든 필드를 수동으로 복사 (dict comprehension)
    merged = {
        'chunk_id': enriched_chunk.get('chunk_id'),
        'doc_id': enriched_chunk.get('doc_id'),
        'doc_type': enriched_chunk.get('doc_type'),
        'source_path': enriched_chunk.get('source_path'),
        'source_format': enriched_chunk.get('source_format'),
        'section': enriched_chunk.get('section'),
        'title': enriched_chunk.get('title'),
        'heading_path': enriched_chunk.get('heading_path'),
        'start_line': enriched_chunk.get('start_line'),
        'end_line': enriched_chunk.get('end_line'),
        'text': enriched_chunk.get('text'),
        'char_count': enriched_chunk.get('char_count'),
        'created_at': enriched_chunk.get('created_at'),
        'detected_patterns': enriched_chunk.get('detected_patterns', []),
        'feature_area': enriched_chunk.get('feature_area'),
        'related_rapp': enriched_chunk.get('related_rapp'),
        'related_function': enriched_chunk.get('related_function'),
        'review_role': enriched_chunk.get('review_role'),
        'priority': enriched_chunk.get('priority'),
        'human_review_required': enriched_chunk.get('human_review_required'),
        'confidence': enriched_chunk.get('confidence'),
        'evidence_scope': enriched_chunk.get('evidence_scope'),
        'related_keywords': enriched_chunk.get('related_keywords', []),
        'metadata_version': enriched_chunk.get('metadata_version'),
        'metadata': {},
    }
    
    # base chunk 의 metadata 에서 source_file, page_number, slide_number 만 추출
    base_metadata = base_chunk.get('metadata', {})
    
    # source_file 정보 추가 (base 에서 가져옴)
    if 'source_file' in base_metadata:
        merged['metadata']['source_file'] = base_metadata['source_file']
    
    # page_number 정보 추가 (base 에서 가져옴)
    if 'page_number' in base_metadata:
        merged['metadata']['page_number'] = base_metadata['page_number']
    
    # slide_number 정보도 추가 (base 에서 가져옴)
    if 'slide_number' in base_metadata:
        merged['metadata']['slide_number'] = base_metadata['slide_number']
    
    return merged


def merge_jsonl_folders(
    enriched_dir: Path,
    base_dir: Path,
    output_dir: Path
) -> dict:
    """
    enriched_jsonl 폴더와 jsonl 폴더를 병합합니다.
    
    Args:
        enriched_dir: enriched_jsonl 폴더 경로 (풍부한 metadata)
        base_dir: jsonl 폴더 경로 (source_file, page_number 정보 포함)
        output_dir: 병합 결과를 저장할 폴더
    
    Returns:
        병합 통계 정보
    """
    stats = {
        'files_processed': 0,
        'chunks_merged': 0,
        'files_with_metadata_added': 0,
        'errors': []
    }
    
    # 출력 폴더 생성
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # enriched 폴더의 모든 JSONL 파일 처리
    enriched_files = list(enriched_dir.glob('*.jsonl'))
    print(f"Found {len(enriched_files)} JSONL files in enriched folder")
    
    for enriched_file in enriched_files:
        file_name = enriched_file.name
        base_file = base_dir / file_name
        
        print(f"\nProcessing: {file_name}")
        
        try:
            # enriched chunk 읽기
            enriched_chunks = load_jsonl_file(enriched_file)
            
            # base chunk 읽기 (있는 경우만)
            base_chunks = []
            if base_file.exists():
                base_chunks = load_jsonl_file(base_file)
                print(f"  - Base file found: {len(base_chunks)} chunks")
            else:
                print(f"  - No matching base file, using enriched only")
            
            # chunk 병합 (chunk_id 기준 매칭)
            if base_chunks:
                # base_chunks 를 chunk_id 로 인덱싱
                base_index = {c['chunk_id']: c for c in base_chunks}
                
                merged_chunks = []
                metadata_added_count = 0
                
                for enriched_chunk in enriched_chunks:
                    chunk_id = enriched_chunk.get('chunk_id')
                    base_chunk = base_index.get(chunk_id)
                    
                    if base_chunk:
                        merged = merge_chunk_metadata(enriched_chunk, base_chunk)
                        # metadata 가 추가되었는지 확인
                        if 'source_file' in merged.get('metadata', {}) or \
                           'page_number' in merged.get('metadata', {}):
                            metadata_added_count += 1
                        merged_chunks.append(merged)
                    else:
                        # base 에 없으면 enriched 그대로 사용
                        merged_chunks.append(enriched_chunk)
                
                stats['chunks_merged'] += len(merged_chunks)
                stats['files_processed'] += 1
                
                if metadata_added_count > 0:
                    stats['files_with_metadata_added'] += 1
                    print(f"  - Added metadata to {metadata_added_count} chunks")
                
                # 병합된 chunk 저장
                output_file = output_dir / file_name
                save_jsonl_file(output_file, merged_chunks)
                print(f"  - Saved to: {output_file}")
            else:
                # base 파일이 없으면 enriched 그대로 저장
                output_file = output_dir / file_name
                save_jsonl_file(output_file, enriched_chunks)
                stats['files_processed'] += 1
                stats['chunks_merged'] += len(enriched_chunks)
                print(f"  - Saved (enriched only): {output_file}")
        
        except Exception as e:
            error_msg = f"Error processing {file_name}: {e}"
            stats['errors'].append(error_msg)
            print(f"  - ERROR: {e}")
    
    # base 폴더에만 있는 파일들도 복사 (누락 방지)
    base_only_files = set(base_dir.glob('*.jsonl')) - set(enriched_dir.glob('*.jsonl'))
    if base_only_files:
        print(f"\nCopying {len(base_only_files)} base-only files...")
        for base_file in base_only_files:
            try:
                shutil.copy2(base_file, output_dir / base_file.name)
                stats['files_processed'] += 1
                base_chunks = load_jsonl_file(base_file)
                stats['chunks_merged'] += len(base_chunks)
                print(f"  - Copied: {base_file.name}")
            except Exception as e:
                stats['errors'].append(f"Error copying {base_file.name}: {e}")
    
    return stats


def main():
    # 기본 경로 설정
    base_dir = Path('c:/Users/jy2601.kim/RAS-TestCaseReview/data/processed')
    enriched_dir = base_dir / 'enriched_jsonl'
    jsonl_dir = base_dir / 'jsonl'
    output_dir = base_dir / 'jsonl_merged'
    
    print("="*70)
    print("JSONL Folder Merge Tool")
    print("="*70)
    print(f"Enriched folder: {enriched_dir}")
    print(f"Base folder: {jsonl_dir}")
    print(f"Output folder: {output_dir}")
    print()
    
    if not enriched_dir.exists():
        print(f"ERROR: Enriched folder not found: {enriched_dir}")
        return
    
    if not jsonl_dir.exists():
        print(f"ERROR: Base folder not found: {jsonl_dir}")
        return
    
    # 병합 실행
    stats = merge_jsonl_folders(enriched_dir, jsonl_dir, output_dir)
    
    # 결과 보고
    print()
    print("="*70)
    print("Merge Summary")
    print("="*70)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Chunks merged: {stats['chunks_merged']}")
    print(f"Files with metadata added: {stats['files_with_metadata_added']}")
    
    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for error in stats['errors']:
            print(f"  - {error}")
    else:
        print("\nNo errors!")
    
    print()
    print(f"Output saved to: {output_dir}")
    print()
    print("Next steps:")
    print("1. Verify the merged files in jsonl_merged/")
    print("2. If satisfied, replace jsonl/ with jsonl_merged/")
    print("3. Remove enriched_jsonl/ folder if no longer needed")


if __name__ == '__main__':
    main()
