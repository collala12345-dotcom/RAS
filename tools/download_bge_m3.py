#!/usr/bin/env python
"""
Download BGE-M3 model from Hugging Face with proxy bypass.

This script sets NO_PROXY environment variables and downloads
the BGE-M3 embedding model for use with ChromaDB.

Usage:
    python tools/download_bge_m3.py
"""

import os
import sys
from pathlib import Path

# Set environment variables BEFORE any network calls
os.environ["NO_PROXY"] = "huggingface.co,amazonaws.com,s3.amazonaws.com,hf.co"
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

# Disable SSL verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

print("=" * 60)
print("BGE-M3 Model Downloader")
print("=" * 60)
print(f"NO_PROXY: {os.environ.get('NO_PROXY', 'not set')}")
print(f"Target directory: {Path.cwd() / 'bge-m3'}")
print("=" * 60)

try:
    from huggingface_hub import snapshot_download
    
    output_dir = Path.cwd() / "bge-m3"
    print(f"\nDownloading BGE-M3 model to: {output_dir}")
    print("This may take several minutes (model size ~2GB)...")
    
    # Download the model
    snapshot_download(
        repo_id="BAAI/bge-m3",
        local_dir=str(output_dir),
        local_dir_use_symlinks=False,
        resume_download=True,
    )
    
    print("\n" + "=" * 60)
    print("✅ Download completed successfully!")
    print("=" * 60)
    
    # Verify downloaded files
    print("\nDownloaded files:")
    for item in output_dir.iterdir():
        if item.is_file():
            print(f"  - {item.name}")
        else:
            print(f"  - {item.name}/")
            for sub in list(item.iterdir())[:5]:
                print(f"    - {sub.name}")
    
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ Download failed: {e}")
    print("=" * 60)
    
    # Print debug info
    print("\nDebug information:")
    print(f"  Python version: {sys.version}")
    print(f"  NO_PROXY: {os.environ.get('NO_PROXY', 'not set')}")
    print(f"  CURL_CA_BUNDLE: {os.environ.get('CURL_CA_BUNDLE', 'not set')}")
    print(f"  SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE', 'not set')}")
    
    import traceback
    traceback.print_exc()
    sys.exit(1)
