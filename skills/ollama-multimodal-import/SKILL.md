---
name: ollama-multimodal-import
description: Procedure for importing and combining custom multimodal (vision-language) GGUF models into Ollama using a Modelfile and mmproj adapter.
---

# Ollama Multimodal (Vision) Import Guide

## Purpose
Use this procedure when you need to import a custom multimodal/vision-language model (like LLaVA, Qwen-VL, Pixtral) from HuggingFace into Ollama, where the base model and the vision projector (`mmproj`) are provided as separate `.gguf` files.

## 1. Required Files
To run a custom multimodal model in Ollama, you need **two** files:
1. **The Base Text Model**: The primary LLM file (e.g., `model-name.gguf`).
2. **The Vision Projector**: The adapter file that translates images into text tokens, usually prefixed with `mmproj` (e.g., `mmproj-model-name.gguf`).

Download both files and place them in your dedicated model storage directory (e.g., `D:\AI\Ollama\Models`).

## 2. Modelfile Syntax
Ollama requires a configuration file to fuse these two components. 

The `FROM` directive sets the core text brain. It can point to an existing Ollama model or an absolute file path to a `.gguf`.
The `ADAPTER` directive attaches the vision projector. It must point to the absolute file path of the `mmproj` `.gguf`.

## 3. Creating the Modelfile Manually (Windows)
Because Windows hides file extensions, the safest way to create a Modelfile manually is using a standard text file:
1. Right-click in your model directory -> **New** -> **Text Document**.
2. Name it something descriptive, e.g., `Modelfile-vision.txt`.
3. Open the file in Notepad and add the configuration pattern:

```dockerfile
# 1. Point to the main text model (can be a local path or a downloaded hf.co model)
FROM "D:\AI\Ollama\Models\base-model.gguf"

# 2. Attach the vision projector file
ADAPTER "D:\AI\Ollama\Models\mmproj-vision-adapter.gguf"
```
4. Save and close the file.

## 4. Building the Model in Ollama
Open PowerShell or Command Prompt and run the `ollama create` command, pointing the `-f` flag to the text file you just created:

```powershell
ollama create my-custom-vision-model -f "D:\AI\Ollama\Models\Modelfile-vision.txt"
```

Ollama will parse the text file, read the `.gguf` files, and copy them into its internal database (`blobs/` directory) as a unified multimodal model.

## 5. Verification
Once the build is complete, verify the model is installed:
```powershell
ollama list
```
Run the new vision model to test image understanding:
```powershell
ollama run my-custom-vision-model
```

## 6. Advanced Troubleshooting & Compatibility

### Hash Validation (The Pathumma 2.0 Lesson)
If Ollama behaves as if it's using the wrong vision adapter (e.g., pulling a Qwen-VL mmproj instead of your custom model's mmproj), you can cryptographically prove what Ollama is loading.
1. Find your model's manifest in `<Ollama_Dir>\models\manifests\registry.ollama.ai\library\<model_name>\latest`.
2. Look at the SHA256 digest next to the `projector` layer.
3. Compare that SHA256 hash to the actual `.gguf` file you built it from using `Get-FileHash -Algorithm SHA256 <your-mmproj.gguf>`.
If the hashes match, Ollama is definitively using your specific adapter. Any poor vision performance is due to the model itself, not an adapter swap.

### Catastrophic Forgetting in Vision Models
If a multimodal model fails at OCR but succeeds at Image Captioning (e.g., summarizing a dense document in one sentence), it may be suffering from **Catastrophic Forgetting**. If the model creators fine-tuned a base OCR-capable model (like Qwen2-VL) heavily on VQA (Visual Question Answering) or short captioning datasets, the model's weights will overwrite its innate OCR abilities. In this case, the model is working perfectly as trained, but is fundamentally unsuitable for OCR tasks.
