#!/usr/bin/env python3
"""
import_gguf.py: Reusable helper script to import single or batch GGUF models into Ollama on Windows.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"

def get_existing_models():
    try:
        req = urllib.request.urlopen(OLLAMA_TAGS_URL, timeout=5)
        data = json.loads(req.read().decode("utf-8"))
        return [m.get("name", "").lower() for m in data.get("models", [])]
    except Exception:
        return []

def sanitize_model_name(filename):
    """
    Derives an Ollama-compatible `<model>:<tag>` from a GGUF filename.
    Examples:
      'typhoon2.1-gemma3-12b.Q8_0.gguf' -> 'typhoon2.1-gemma3-12b:q8_0'
      'openthaigpt1.5-14b-instruct.i1-Q6_K.gguf' -> 'openthaigpt1.5-14b-instruct:q6_k'
      'Qwen3-Reranker-0.6B.f16.gguf' -> 'qwen3-reranker-0.6b:f16'
    """
    base = os.path.splitext(filename)[0]
    
    # Common quantization pattern at the end of the filename
    quant_pattern = re.compile(r'[\.\-_]([qQ]\d+_[a-zA-Z0-9_]+|[fF]16|[fF]32|[bB][fF]16)$')
    match = quant_pattern.search(base)
    
    if match:
        tag = match.group(1).lower()
        model_part = base[:match.start()]
    else:
        tag = "latest"
        model_part = base

    # Clean model part: remove trailing .i1 or dots/dashes
    model_part = re.sub(r'[\._-]i\d+$', '', model_part, flags=re.IGNORECASE)
    # Lowercase and clean characters
    model_clean = re.sub(r'[^a-zA-Z0-9_\.\-]', '-', model_part).lower().strip('-._')
    
    return f"{model_clean}:{tag}"

def import_model(model_name, gguf_path, dry_run=False):
    normalized_path = os.path.abspath(gguf_path).replace("\\", "/")
    size_gb = os.path.getsize(gguf_path) / (1024**3)
    
    print(f"\nModel: {model_name}")
    print(f"File : {normalized_path} ({size_gb:.2f} GB)")
    
    if dry_run:
        print(" [DRY-RUN] Skipped.")
        return True, "dry-run"
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_modelfile = os.path.join(script_dir, f".temp_modelfile_{os.getpid()}")
    
    with open(temp_modelfile, "w", encoding="utf-8") as f:
        f.write(f'FROM "{normalized_path}"\n')
        
    t0 = time.time()
    cmd = ["ollama", "create", model_name, "-f", temp_modelfile]
    try:
        # Note: encoding="utf-8" and errors="replace" are critical on Windows to prevent UnicodeDecodeError with Ollama spinners
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        elapsed = time.time() - t0
        if res.returncode == 0:
            print(f" -> SUCCESS in {elapsed:.1f}s")
            return True, f"{elapsed:.1f}s"
        else:
            stderr_snippet = " ".join(res.stderr.strip().splitlines()[-3:]) if res.stderr else "Unknown error"
            print(f" -> FAILED in {elapsed:.1f}s: {stderr_snippet}")
            return False, stderr_snippet
    except Exception as e:
        elapsed = time.time() - t0
        print(f" -> ERROR in {elapsed:.1f}s: {e}")
        return False, str(e)
    finally:
        if os.path.exists(temp_modelfile):
            try:
                os.remove(temp_modelfile)
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(description="Import GGUF models into Ollama on Windows")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dir", "-d", help="Directory containing .gguf files")
    group.add_argument("--file", "-f", help="Path to a single .gguf file")
    parser.add_argument("--name", "-n", help="Explicit model name (only used with --file)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search directory recursively")
    parser.add_argument("--force", action="store_true", help="Force re-import even if model already exists")
    parser.add_argument("--dry-run", action="store_true", help="Preview models to be imported without executing")
    
    args = parser.parse_args()
    
    targets = []
    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        name = args.name or sanitize_model_name(os.path.basename(args.file))
        targets.append((name, args.file))
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"Error: Directory not found: {args.dir}")
            sys.exit(1)
            
        if args.recursive:
            for root, _, files in os.walk(args.dir):
                for file in files:
                    if file.lower().endswith(".gguf"):
                        fp = os.path.join(root, file)
                        targets.append((sanitize_model_name(file), fp))
        else:
            for item in os.listdir(args.dir):
                if item.lower().endswith(".gguf"):
                    fp = os.path.join(args.dir, item)
                    if os.path.isfile(fp):
                        targets.append((sanitize_model_name(item), fp))
                        
    if not targets:
        print("No .gguf files found.")
        sys.exit(0)
        
    print(f"Found {len(targets)} GGUF file(s) to process.")
    
    existing = get_existing_models() if not args.force else []
    
    results = []
    total_start = time.time()
    for idx, (name, path) in enumerate(targets, 1):
        if not args.force and name.lower() in existing:
            print(f"\n[{idx}/{len(targets)}] Model '{name}' already exists. Skipping.")
            results.append((name, "SKIPPED", "Already exists"))
            continue
            
        print(f"\n[{idx}/{len(targets)}] Importing '{name}'...")
        success, detail = import_model(name, path, dry_run=args.dry_run)
        status = "SUCCESS" if success else "FAILED"
        results.append((name, status, detail))
        
    total_elapsed = time.time() - total_start
    print(f"\nFinished in {total_elapsed:.1f}s.")
    print("\nSummary:")
    for name, status, detail in results:
        print(f" - {name}: {status} ({detail})")

if __name__ == "__main__":
    main()
