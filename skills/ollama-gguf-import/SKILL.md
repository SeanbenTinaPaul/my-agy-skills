---
name: ollama-gguf-import
description: >-
  Procedures, automation, and troubleshooting for importing single or bulk GGUF models into Ollama on Windows.
  Use when importing .gguf models from Hugging Face or local storage, constructing Modelfiles,
  handling Windows terminal encoding issues, or verifying imported models via the Ollama REST API.
---

# Ollama Windows — GGUF Model Import & Automation

## Purpose
Use this skill when importing individual or batch `.gguf` quantized models (from Hugging Face or local directories) into Ollama on a Windows system.

This guide addresses specific Windows challenges:
- Handling Windows path formatting inside Modelfiles
- Preventing CLI crashes caused by Ollama's UTF-8 progress spinners on Windows `cp1252` consoles
- Ensuring the Ollama headless service is active without triggering GUI/WebView2 single-instance conflicts
- Batch importing with auto-sanitized model tags and collision avoidance
- Verifying model inference and safely unloading models from VRAM

---

## 1. Pre-flight Checks

### A. Ensure Ollama Service Is Running
On Windows machines where Ollama auto-start is disabled, running `ollama list` or `ollama create` directly may trigger the tray supervisor (`ollama app.exe`), which can fail with:
```text
Failed to start: Unable to init instance: Unspecified error
```

To safely start the Ollama server in the background:
```powershell
Start-Process -FilePath "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 2
```

Verify service connectivity:
```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

### B. Verify Model Storage Path & Disk Space
Ollama copies the GGUF data into blob storage (`blobs/sha256-...`) under `OLLAMA_MODELS`.
Verify the active storage destination and available disk space:
```powershell
$env:OLLAMA_MODELS
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name="FreeGB";Expression={[math]::Round($_.Free/1GB, 2)}}
```
Ensure the target drive has at least as much free space as the total uncompressed size of the GGUF models being imported.

---

## 2. Model Naming & Tagging Conventions

Ollama model names must follow the `[namespace/]<model_name>:<tag>` format:
- Must be all lowercase.
- Only alphanumeric characters, dashes `-`, and underscores `_`.
- If no tag is provided, `:latest` is used by default.

### Recommended Tag Mapping
When importing `.gguf` files with embedded quantization names:
| GGUF Filename Pattern | Example Input | Target Ollama Name |
|-----------------------|---------------|-------------------|
| `*Q8_0.gguf` | `pathumma-thaillm-8b-think-3-Q8_0.gguf` | `pathumma-thaillm-8b-think-3:q8_0` |
| `*.i1-Q6_K.gguf` | `openthaigpt1.5-14b-instruct.i1-Q6_K.gguf` | `openthaigpt1.5-14b-instruct:q6_k` |
| `*.f16.gguf` | `Qwen3-Reranker-0.6B.f16.gguf` | `qwen3-reranker-0.6b:f16` |

> [!WARNING]
> Never import with a generic `:latest` tag if an existing model of that name already exists, as Ollama will overwrite the manifest. Always preserve specific quantization tags.

---

## 3. Importing a Single GGUF Model

### Step 1: Create a Modelfile
In Ollama, GGUF files contain tokenizers, chat templates, and stop tokens. A simple `FROM` line is sufficient:
```dockerfile
FROM "E:/AI/model_from_hf/model-name-Q8_0.gguf"
```
*Note: Use forward slashes (`/`) in the file path to avoid escape issues on Windows.*

### Step 2: Run `ollama create`
```powershell
ollama create model-name:q8_0 -f ./Modelfile
```

---

## 4. Bulk Import Helper Script

This skill provides an automated, robust script located at [import_gguf.py](./scripts/import_gguf.py).

### Key Script Features:
- **Windows UTF-8 Encoding Fix**: Ollama's CLI outputs braille spinner characters (`⠦`, `⠧`) that cause Python `UnicodeDecodeError: 'charmap' codec can't decode...` under Windows default code page 1252. The script explicitly enforces `encoding="utf-8", errors="replace"`.
- **Automatic Tag Sanitization**: Converts quantization suffixes into Ollama tags.
- **Skip Existing**: Queries the Ollama REST API (`/api/tags`) and automatically skips already-imported models.
- **Dry-Run Mode**: Inspects the files, calculates sizes, and previews model tags before writing any data.

### Usage:

```powershell
# Dry run to inspect models and tags:
python "$env:USERPROFILE\.gemini\config\skills\ollama-gguf-import\scripts\import_gguf.py" --dir "E:\AI\model_from_hf" --dry-run

# Run full bulk import:
python "$env:USERPROFILE\.gemini\config\skills\ollama-gguf-import\scripts\import_gguf.py" --dir "E:\AI\model_from_hf"

# Search subdirectories recursively:
python "$env:USERPROFILE\.gemini\config\skills\ollama-gguf-import\scripts\import_gguf.py" --dir "E:\AI\model_from_hf" --recursive

# Import a single file with custom name:
python "$env:USERPROFILE\.gemini\config\skills\ollama-gguf-import\scripts\import_gguf.py" --file "E:\path\model.gguf" --name "my-model:q8_0"
```

---

## 5. Verification & Memory Cleanup

### A. Verify Model Availability
```powershell
ollama list
```
or via the REST API:
```powershell
(Invoke-RestMethod http://127.0.0.1:11434/api/tags).models | Select-Object name, size, modified_at
```

### B. Quick Inference Test
Send a single prompt to ensure the model weights load properly:
```powershell
$body = @{
    model = "model-name:q8_0"
    prompt = "Hello, reply in one sentence."
    stream = $false
} | ConvertTo-Json

(Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -Body $body -ContentType "application/json").response
```

### C. Unload Model from GPU (VRAM Cleanup)
By default, Ollama retains loaded models in VRAM for 5 minutes. To immediately free VRAM:
```powershell
$body = @{
    model = "model-name:q8_0"
    keep_alive = 0
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -Body $body -ContentType "application/json" | Out-Null
ollama ps
```
`ollama ps` should report no active models in memory.

---

## 6. Troubleshooting

### Problem: `Failed to start: Unable to init instance: Unspecified error`
- **Cause**: Ollama CLI attempted to launch the Windows GUI tray application (`ollama app.exe`), which encountered a WebView2 / single-instance conflict.
- **Fix**: Launch the headless engine directly with `ollama.exe serve` or start it via PowerShell `Start-Process ... -ArgumentList "serve"`.

### Problem: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f...`
- **Cause**: Python `subprocess.run(text=True)` on Windows defaults to ANSI code page (`cp1252`), failing to decode Ollama's progress spinners.
- **Fix**: Always specify `encoding="utf-8", errors="replace"` in `subprocess.run()`.

### Problem: `Error: timed out waiting for server to start`
- **Cause**: Port 11434 might already be bound or another process is holding the socket.
- **Fix**: Check port 11434 with `Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue` and kill conflicting orphaned processes if necessary.
