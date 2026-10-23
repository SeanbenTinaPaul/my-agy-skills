---
name: gguf-ollama-compatibility-check
description: The selection pathway for verifying if a Hugging Face model architecture can actually be run by llama.cpp or Ollama before downloading or converting it.
---

# Ollama / llama.cpp Compatibility Selection Pathway

## Purpose
Converting `.safetensors` to `.gguf` does **not** guarantee the model will work in Ollama. `llama.cpp` uses hardcoded C++ tensor mappings for specific model architectures. If an architecture is too new, the model will either crash or output empty text. Use this checklist to verify compatibility *before* investing time into downloads and conversions.

## Pathway Checklist

### 1. Check `config.json` for the Architecture
Go to the model's Hugging Face repository and open the `config.json` file. Look for the `"architectures"` key.
*   **Supported Examples:** `LlamaForCausalLM`, `Qwen2ForCausalLM`, `MistralForCausalLM`, `Qwen2VLForConditionalGeneration`.
*   **Unsupported / Bleeding-edge Examples:** `Qwen3_5ForConditionalGeneration` (If the architecture uses a vastly newer version of transformers, e.g., v5.6.0, `llama.cpp` likely lacks the matrix mappings).

### 2. Verify Result of Unsupported Architectures
If you force a conversion of an unsupported architecture (e.g., using a generic fallback or hacking the config) and load it into Ollama:
*   **Symptom:** The model mounts successfully to the GPU, but outputs a completely blank string or an immediate `<EOS>` (End of Sequence) token.
*   **Cause:** The visual or text tensors are misaligned in memory. The model's "brain" receives garbage data and immediately terminates the generation loop.
*   **Verdict:** You **cannot** use Ollama for this model yet. You must use native Python inference (PyTorch + `transformers`) as specified in the model's README.

### 3. Check for Mismatched Config Metadata
Sometimes the `config.json` claims the model has layers that the `.safetensors` don't actually contain.
*   **Example:** `"mtp_num_hidden_layers": 1` in models that don't have block 24 weights. 
*   **Action:** If `llama.cpp`'s `convert_hf_to_gguf.py` throws an assertion error regarding layers, inspect the raw `.safetensors` keys (using a python script) to see if those layers actually exist. If they don't, use flags like `--no-mtp` during conversion to bypass the metadata bug.

### 4. Multimodal / Vision Projector Availability
For vision models, check if the `.safetensors` repository explicitly provides a separate vision adapter (e.g., `model-0000X-of-0000X.safetensors` containing the `mmproj` weights). If it doesn't, or if the adapter requires custom python code to slice images into patches, standard Ollama vision inference may fail.
