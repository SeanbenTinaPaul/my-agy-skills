---
name: hf-safetensors-gguf-conversion
description: Procedure for converting Hugging Face safetensors models into GGUF format for use in Ollama and llama.cpp.
---

# Safetensors to GGUF Conversion Guide

## Purpose
Use this skill when you have a downloaded Hugging Face model (`.safetensors` format) that you need to run locally in Ollama or `llama.cpp`, and a pre-converted GGUF is not available.

## Prerequisites
1. **llama.cpp repository**: Ensure you have cloned `llama.cpp` to your machine (e.g., `D:\AI\llama.cpp`).
2. **Python Environment**: Ensure you have a virtual environment with the required dependencies (e.g., `D:\AI\llama.cpp\.venv`). Install requirements via `pip install -r requirements.txt` inside the `llama.cpp` directory.

## Standard Conversion Process

Run the conversion script, passing the directory containing the `config.json` and `model.safetensors` files.

**Basic command (FP16/BF16):**
```powershell
# Using the llama.cpp virtual environment
$python_exe = "D:\AI\llama.cpp\.venv\Scripts\python.exe"
$converter = "D:\AI\llama.cpp\convert_hf_to_gguf.py"
$model_dir = "D:\AI\models\my-custom-model"

& $python_exe $converter $model_dir --outtype bf16
```
*(Use `--outtype f16` for standard Float16, or `--outtype bf16` for BFloat16).*

## Advanced Troubleshooting & Known Bugs

### 1. The MTP Layer Crash (e.g., Qwen Models)
**Symptom:** The conversion script crashes with an assertion error (`assert self.opt_num_mtp_layers != 0`), or the converted GGUF crashes Ollama instantly when loading.
**Cause:** The model creator accidentally left speculative decoding metadata (e.g., `"mtp_num_hidden_layers": 1`) in the `config.json`, but the actual `.safetensors` weights do not contain these extra layers. 
**Fix:** Append the `--no-mtp` flag to strip the speculative layers from the conversion requirement:
```powershell
& $python_exe $converter $model_dir --outtype bf16 --no-mtp
```

### 2. Output is completely blank (Immediate EOS)
If the model successfully converts and loads into Ollama, but outputs absolutely nothing, see the `gguf-ollama-compatibility-check` skill. The model's architecture is likely unsupported by the current C++ tensor mappings.
