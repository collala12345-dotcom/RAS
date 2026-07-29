#!/usr/bin/env python3
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from functions.src.rag_embedder.keyword_retriever import KeywordRetriever, KeywordRetrieverConfig
from pathlib import Path

config = KeywordRetrieverConfig(
    jsonl_dir=Path('data/processed/jsonl'),
    index_file=Path('data/processed/keyword_index.json'),
    bm25_k1=1.5,
    bm25_b=0.75,
)

retriever = KeywordRetriever(config)

if retriever.load_from_cache():
    print("BM25 index loaded from cache")
else:
    retriever.load()
    retriever.save()
    print("BM25 index built and saved")

queries = [
    'ESM Energy Saving Management ES candidate sector list',
    'ESM EN-DC anchor coverage carrier cell ES capable',
    'ESM multi-level ES configuration group IP Tput PRB utilization',
    'FR50 FR51 FR60 ESM ES group configuration',
    'esOperationWindow ES sector list energy saving',
    'ES Level ES Feature EN-DC anchor carrier',
    'ES group configuration cell feature level',
    'energy saving candidate sector exclusion condition',
]

results_out = []
seen = set()
for q in queries:
    results = retriever.search(q, top_k=15)
    for r in results:
        if r.score >= 0.35:
            meta = getattr(r, 'metadata', {})
            source_file = meta.get('source_file', 'unknown')
            page_number = meta.get('page_number', 0)
            key = f"{r.chunk_id}"
            if key in seen:
                continue
            seen.add(key)
            results_out.append({
                'query': q,
                'score': round(r.score, 4),
                'source_file': source_file,
                'page_number': page_number,
                'chunk_id': r.chunk_id,
                'text': r.text[:500]
            })

# Sort by score descending
results_out.sort(key=lambda x: x['score'], reverse=True)

with open('bm25_results.json', 'w', encoding='utf-8') as f:
    json.dump(results_out, f, ensure_ascii=False, indent=2)

print(f"Total unique results: {len(results_out)}")
for r in results_out:
    print(f"Score: {r['score']} | {r['source_file']} P{r['page_number']} | {r['text'][:120]}")
