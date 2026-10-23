# My Antigravity Skills (`my-agy-skills`)

A curated collection of custom skills for Google Antigravity (AGY) agents and CLI.

## Included Skills

| Skill | Description |
| :--- | :--- |
| **archify** | Create polished architecture, sequence, data-flow, and state diagrams as standalone HTML with inline SVG. |
| **brag** | Turn project websites into short launch videos using Hyperframes. |
| **brag-slim** | Lightweight, zero-dependency launch video generator for projects and sites. |
| **design-skills** | Curated registry and implementation engine for 67 UI/UX design systems. |
| **gguf-ollama-compatibility-check** | Compatibility verifier for Hugging Face model architectures before downloading/converting for Ollama. |
| **grilling** | Stress-test decisions, architectural designs, and project plans through interactive Socratic questioning. |
| **harness2** | Token-efficient cross-session memory, friction digestion, and harness evolution. |
| **hf-safetensors-gguf-conversion** | Workflow for converting Hugging Face Safetensors models into GGUF format for llama.cpp and Ollama. |
| **markitdown-office-to-md** | High-fidelity conversion of Office documents (Word, Excel, PowerPoint) and PDFs into Markdown. |
| **ollama-gguf-import** | Procedures and automation for importing GGUF models into Ollama on Windows. |
| **ollama-multimodal-import** | Workflow for importing multimodal vision-language models with mmproj adapters into Ollama. |
| **ollama-windows-management** | Safely migrate Ollama model storage to secondary drives and manage startup behavior. |
| **ponytail-audit** | Whole-codebase quality audit for bugs, load bottlenecks, dead code, and security risks. |
| **ponytail-debt** | Technical debt ledger tracking deferred tasks and shortcut comments. |
| **ponytail-review** | In-depth quality review of code changes and pull requests. |

---

## Included Rules

| Rule | Description |
| :--- | :--- |
| **karpathy-guidelines** | Disciplined software engineering guidelines biasing toward simplicity, surgical changes, and rigorous verification. |

---

## Installation & Usage

### Installing Skills
To use these skills in your Antigravity environment:

#### Option 1: Global Installation
Copy desired skills into your global Antigravity config directory:
```powershell
Copy-Item -Path "skills\*" -Destination "$HOME\.gemini\config\skills\" -Recurse -Force
```

#### Option 2: Project-Level Installation
Copy or link skills into your repository's `.agents/skills` or `.gemini/skills`:
```powershell
New-Item -ItemType Directory -Path ".agents\skills" -Force
Copy-Item -Path "skills\<skill-name>" -Destination ".agents\skills\" -Recurse -Force
```

### Installing Rules
To install custom rules:

#### Option 1: Global Installation
Copy rules into your global Antigravity rules directory:
```powershell
New-Item -ItemType Directory -Path "$HOME\.gemini\config\rules" -Force
Copy-Item -Path "rules\*" -Destination "$HOME\.gemini\config\rules\" -Force
```

#### Option 2: Project-Level Installation
Copy rules into your repository's `.agents/rules`:
```powershell
New-Item -ItemType Directory -Path ".agents\rules" -Force
Copy-Item -Path "rules\*" -Destination ".agents\rules\" -Force
```
