#!/usr/bin/env python3
"""
BM25 Index Rebuild Script
- data/processed/jsonl/ 폴더의 모든 JSONL 파일을 인덱싱
- keyword_index.json 으로 저장
"""

import json
import math
import re
from pathlib import Path
from collections import defaultdict

# BM25 파라미터
K1 = 1.5
B = 0.75

def tokenize(text):
    """텍스트를 토큰화"""
    tokens = []
    
    # 영어 단어 (2 글자 이상)
    en_words = re.findall(r'\b[a-z]{2,}\b', text.lower())
    tokens.extend(en_words)
    
    # 한국어 토큰 (공백 기준 + 2-4 글자 세그먼트)
    kr_pattern = re.findall(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]+', text)
    for kr_text in kr_pattern:
        kr_tokens = kr_text.split()
        tokens.extend(kr_tokens)
        
        # 2-4 글자 한국어 세그먼트
        for i in range(len(kr_text) - 1):
            for j in range(i + 2, min(i + 6, len(kr_text) + 1)):
                segment = kr_text[i:j]
                if len(segment) >= 2:
                    tokens.append(f"kr_{segment}")
    
    return tokens

def build_index():
    """BM25 인덱스 빌드"""
    jsonl_dir = Path('data/processed/jsonl')
    
    if not jsonl_dir.exists():
        print(f"Error: {jsonl_dir} not found")
        return
    
    # 모든 JSONL 파일 읽기
    chunks = {}
    chunk_to_source = {}
    documents = {}
    doc_lengths = {}
    index = defaultdict(list)
    
    jsonl_files = list(jsonl_dir.glob('*.jsonl'))
    print(f"Found {len(jsonl_files)} JSONL files")
    
    for jsonl_file in jsonl_files:
        print(f"  Processing: {jsonl_file.name}")
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        chunk = json.loads(line)
                        chunk_id = chunk.get('chunk_id', f"{jsonl_file.stem}_{line_num}")
                        
                        chunks[chunk_id] = chunk
                        chunk_to_source[chunk_id] = str(jsonl_file)
                        
                        text = chunk.get('text', '')
                        documents[chunk_id] = text
                        
                        # 토큰화 및 인덱싱
                        words = tokenize(text)
                        doc_lengths[chunk_id] = len(words)
                        
                        term_freq = defaultdict(int)
                        for word in words:
                            term_freq[word] += 1
                        
                        for term, freq in term_freq.items():
                            index[term].append((chunk_id, freq))
        except Exception as e:
            print(f"    Error: {e}")
    
    # 통계 계산
    num_documents = len(documents)
    avg_doc_length = sum(doc_lengths.values()) / num_documents if num_documents > 0 else 0
    
    # IDF 계산
    idf = {}
    for term, doc_list in index.items():
        df = len(doc_list)
        idf[term] = math.log((num_documents - df + 0.5) / (df + 0.5) + 1)
    
    # 인덱스 저장
    index_data = {
        'chunks': chunks,
        'chunk_to_source': chunk_to_source,
        'documents': documents,
        'doc_lengths': doc_lengths,
        'index': {k: list(v) for k, v in index.items()},
        'idf': idf,
        'num_documents': num_documents,
        'avg_doc_length': avg_doc_length,
    }
    
    output_path = Path('data/processed/keyword_index.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] BM25 인덱스 생성 완료!")
    print(f"  - Output: {output_path}")
    print(f"  - Total chunks: {num_documents}")
    print(f"  - Vocabulary size: {len(index)}")
    print(f"  - Avg doc length: {avg_doc_length:.1f} words")
    
    # ESM 관련 chunk 확인
    esm_chunks = [k for k in chunks.keys() if 'ESM' in k or 'esm' in k]
    print(f"  - ESM 관련 chunks: {len(esm_chunks)} 개")
    for chunk in esm_chunks[:5]:
        print(f"      {chunk}")

if __name__ == '__main__':
    build_index()
