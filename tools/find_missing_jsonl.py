#!/usr/bin/env python3
"""
Find MD files in data/raw/ that don't have corresponding JSONL files in data/processed/jsonl/.

Usage:
    python functions/tools/find_missing_jsonl.py           # 찾기만 함
    python functions/tools/find_missing_jsonl.py --convert  # 찾아서 JSONL 로 변환
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def find_missing_jsonl() -> list[Path]:
    """
    data/raw/ 폴더의 모든 MD 파일에 대해
    data/processed/jsonl/ 에 해당 JSONL 이 있는지 확인.

    Returns:
        JSONL 이 없는 MD 파일 경로 리스트
    """
    raw_dir = Path("data/raw")
    jsonl_dir = Path("data/processed/jsonl")

    if not raw_dir.exists():
        print("[ERR] data/raw/ 폴더가 없습니다.")
        return []

    if not jsonl_dir.exists():
        print("[ERR] data/processed/jsonl/ 폴더가 없습니다.")
        return []

    # 모든 MD 파일 찾기
    md_files = list(raw_dir.rglob("*.md"))

    # 기존 JSONL 파일명 집합 (stem 기준)
    existing_jsonl_stems = set()
    for jsonl_file in jsonl_dir.glob("*.jsonl"):
        existing_jsonl_stems.add(jsonl_file.stem)

    # JSONL 이 없는 MD 파일 찾기
    missing_files = []
    for md_file in sorted(md_files):
        if md_file.stem not in existing_jsonl_stems:
            missing_files.append(md_file)

    return missing_files


def convert_to_jsonl(md_files: list[Path]) -> int:
    """
    MD 파일들을 JSONL 로 변환.

    Returns:
        성공한 파일 수
    """
    success_count = 0

    for md_file in md_files:
        print(f"\n  Converting: {md_file.name}")

        cmd = [
            sys.executable,
            "functions/scripts/build_jsonl.py",
            "--input-dir", str(md_file.parent),
            "--output-dir", "data/processed/jsonl",
            "--force",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            jsonl_path = Path("data/processed/jsonl") / f"{md_file.stem}.jsonl"
            if jsonl_path.exists():
                print(f"  [OK] {md_file.name} -> {jsonl_path.name}")
                success_count += 1
            else:
                print(f"  [WARN] JSONL 파일이 생성되지 않음: {md_file.name}")
        else:
            print(f"  [ERR] 변환 실패: {md_file.name}")
            if result.stderr:
                print(f"        {result.stderr[:200]}")

    return success_count


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="data/raw/ 에서 JSONL 이 없는 MD 파일 찾기"
    )
    parser.add_argument(
        "--convert",
        action="store_true",
        help="찾은 파일을 JSONL 로 변환",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Find Missing JSONL Files")
    print("=" * 60)

    missing_files = find_missing_jsonl()

    if not missing_files:
        print("\n[OK] 모든 MD 파일에 JSONL 이 존재합니다!")
        return

    print(f"\n[FOUND] JSONL 이 없는 MD 파일: {len(missing_files)} 개\n")

    for i, md_file in enumerate(missing_files, 1):
        rel_path = md_file.relative_to(Path("data/raw"))
        print(f"  {i}. data/raw/{rel_path}")

    if args.convert:
        print(f"\n{'=' * 60}")
        print(f"Converting {len(missing_files)} files to JSONL...")
        print("=" * 60)

        success_count = convert_to_jsonl(missing_files)

        print(f"\n{'=' * 60}")
        print(f"Conversion Complete")
        print(f"  Total: {len(missing_files)} files")
        print(f"  Success: {success_count} files")
        print(f"  Failed: {len(missing_files) - success_count} files")
        print("=" * 60)

        # BM25 인덱스 재생성 안내
        print(f"\n[INFO] BM25 인덱스를 재생성하려면:")
        print(f"   python rebuild_bm25_index.py")
    else:
        print(f"\n[INFO] JSONL 로 변환하려면:")
        print(f"   python functions/tools/find_missing_jsonl.py --convert")


if __name__ == "__main__":
    main()
