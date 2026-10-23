---
name: markitdown-office-to-md
description: >-
  Procedures, automation, and architecture for converting Microsoft Office documents
  (Excel .xlsx/.xls/.xlsm, Word .docx/.doc, PowerPoint .pptx/.ppt), PDFs, and tables
  to high-fidelity Markdown with multi-sheet workbook support, Thai Unicode safety,
  and PyInstaller desktop GUI packaging.
---

# MarkItDown Office to Markdown Converter & Desktop GUI Guide

## Purpose
Use this skill when converting Office documents (Excel workbooks, Word docs, PowerPoint presentations, PDFs) to Markdown, handling multi-sheet spreadsheets, fixing MarkItDown runtime quirks on Windows, or packaging/maintaining the **MarkItDown Studio** standalone desktop application (`.exe`).

---

## 0. Prerequisites & Isolated Environment Setup

To ensure `markitdown` and its dependencies do not conflict with global Python packages, you must always execute and build this workflow inside an isolated virtual environment (`.venv`).

```powershell
# Create and activate environment
python -m venv .venv
.\.venv\Scripts\activate

# Install required core dependencies
pip install markitdown pandas openpyxl xlrd pywin32
```
*Note for Agents: If running a `.bat` file to automate this (like `run_from_source.bat`), ensure the batch script explicitly references `%PROJECT_DIR%.venv\Scripts\python.exe` and `%PROJECT_DIR%.venv\Scripts\pip.exe` to guarantee isolation.*

---

## 1. Supported Document Types & Strategies

| Format | Extension(s) | Conversion Strategy | Key Considerations |
| :--- | :--- | :--- | :--- |
| **Excel Workbook** | `.xlsx`, `.xlsm` | `openpyxl` + `HtmlConverter` (or `MarkItDown`) | Supports multi-sheet separation and macro-enabled workbooks (`.xlsm`). |
| **Legacy Excel** | `.xls` | `xlrd` + `HtmlConverter` (or `MarkItDown`) | Requires `xlrd` engine for BIFF8 binary workbooks. |
| **Word Document** | `.docx` | Microsoft `MarkItDown` (`mammoth` / `docx`) | Preserves headers, bold, italics, lists, and tables. |
| **Legacy Word** | `.doc` | Windows Word COM Automation -> temp `.docx` -> MarkItDown | Requires `pywin32` and Microsoft Word installed locally. |
| **PowerPoint** | `.pptx` | Microsoft `MarkItDown` (`python-pptx`) | Extracts slide titles, text blocks, and tables. |
| **Legacy PPT** | `.ppt` | Windows PowerPoint COM Automation -> temp `.pptx` -> MarkItDown | Requires `pywin32` and Microsoft PowerPoint installed locally. |
| **PDF** | `.pdf` | Microsoft `MarkItDown` (`pdfminer` / `pypdf`) | Extracts text and tabular layouts. |

---

## 2. Multi-Sheet Excel Conversion Modes

When converting multi-sheet workbooks, standard converters often dump only the active sheet or flatten sheets unpredictably. Use the modular multi-mode architecture:

- **Mode 2 (Both - Recommended):** 
  - Produces `{Workbook_Name}_full.md` (combined markdown with `## Sheet Name` headers).
  - Simultaneously produces individual modular files `{Sheet_Name}.md` for each worksheet.
- **Mode 1 (Combined Only):**
  - Produces `{Workbook_Name}_full.md` containing all sheets sequential in one markdown file.
- **Mode 0 (Separate Sheets Only):**
  - Produces individual `{Sheet_Name}.md` files for each sheet.

### High-Performance Single-Pass Extraction Engine
Rather than re-reading large Excel workbooks multiple times, parse the sheets dictionary once and render both outputs:

```python
import pandas as pd
from markitdown.converters import HtmlConverter
from pathlib import Path

def export_workbook(excel_path: Path, output_dir: Path, mode: int = 2):
    output_dir.mkdir(parents=True, exist_ok=True)
    engine = "xlrd" if excel_path.suffix.lower() == ".xls" else "openpyxl"
    
    html_converter = HtmlConverter()
    sheets_dict = pd.read_excel(excel_path, sheet_name=None, engine=engine)

    # 1. Combined Full Markdown
    if mode in (1, 2):
        full_parts = []
        for sheet_name, df in sheets_dict.items():
            html_tbl = df.to_html(index=False)
            md_tbl = html_converter.convert_string(html_tbl).markdown.strip()
            full_parts.append(f"## {sheet_name}\n\n{md_tbl}\n")
        
        with open(output_dir / f"{excel_path.stem}_full.md", "w", encoding="utf-8") as f:
            f.write("\n\n".join(full_parts) + "\n")

    # 2. Individual Sheet Markdown Files
    if mode in (0, 2):
        for sheet_name, df in sheets_dict.items():
            safe_name = sanitize_filename(sheet_name)
            html_tbl = df.to_html(index=False)
            md_tbl = html_converter.convert_string(html_tbl).markdown.strip()
            with open(output_dir / f"{safe_name}.md", "w", encoding="utf-8") as f:
                f.write(f"# {sheet_name}\n\n{md_tbl}\n")
```

---

## 3. Thai Unicode & Windows File System Safety

Windows filenames disallow characters `\ / : * ? " < > |`. Standard ASCII sanitizers often destroy Thai vowel signs and tone marks (Unicode ranges `\u0E00`–`\u0E7F`).

Use this regex sanitizer to preserve Thai script while eliminating illegal Windows filesystem characters:

```python
import re

def sanitize_filename(name: str) -> str:
    """Sanitize sheet or document name for Windows filesystem while preserving Thai vowels and tone marks."""
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(name)).strip().rstrip('. ')
    return clean or "document"
```

---

## 4. Resolving Critical MarkItDown Gotchas on Windows

### A. The `.xlsm` Rejection Issue
By default, Microsoft MarkItDown's `XlsxConverter` only accepts `[".xlsx"]` in `ACCEPTED_XLSX_FILE_EXTENSIONS`.
When passed an `.xlsm` file, MarkItDown falls back to `XlsConverter`, which passes `.xlsm` to `xlrd`, causing:
```text
XLRDError: Excel xlsx file; not supported
```
**Fix:** Explicitly register `.xlsm` before invoking MarkItDown:
```python
try:
    import markitdown.converters._xlsx_converter as _xc
    if ".xlsm" not in _xc.ACCEPTED_XLSX_FILE_EXTENSIONS:
        _xc.ACCEPTED_XLSX_FILE_EXTENSIONS.append(".xlsm")
except Exception:
    pass
```

### B. Magika ONNX Model Missing in Frozen Executables
MarkItDown depends on Google's `magika` library for content detection. When packaged with PyInstaller, `magika` fails with `MagikaError: model dir not found` unless its ONNX model directory is collected.
**Fix 1:** Supply PyInstaller with `--collect-all magika` and `--collect-all onnxruntime`.
**Fix 2:** Provide a resilient in-code fallback class:
```python
try:
    import magika
    _test = magika.Magika()
except Exception:
    try:
        class _DummyMagikaPrediction:
            def __init__(self):
                self.output = type("Output", (), {"label": "unknown"})()
        class _DummyMagikaResult:
            def __init__(self):
                self.status = "ok"
                self.prediction = _DummyMagikaPrediction()
        class _DummyMagika:
            def __init__(self, *args, **kwargs): pass
            def identify_stream(self, stream): return _DummyMagikaResult()
            def identify_path(self, path): return _DummyMagikaResult()
        magika.Magika = _DummyMagika
    except Exception:
        pass
```

---

## 5. Packaging into Standalone `.exe` with PyInstaller

When compiling a Tkinter/custom GUI into a standalone Windows `.exe`:
1. Use `--onefile` and `--windowed` (no black console prompt).
2. Set `--workpath` and `--distpath` to the target working drive (e.g. `E:`) to avoid filling system drives.
3. Collect all necessary metadata, data files, and hidden imports:

```python
import sys
import subprocess
from pathlib import Path

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--name", "MarkItDownStudio",
    "--workpath", r"E:\temp\build",
    "--distpath", r"E:\temp\dist",
    "--collect-all", "markitdown",
    "--collect-all", "magika",
    "--collect-all", "onnxruntime",
    "--collect-all", "openpyxl",
    "--collect-all", "pandas",
    "--collect-all", "xlrd",
    "--collect-all", "bs4",
    "--collect-all", "charset_normalizer",
    "--hidden-import", "win32com",
    "--hidden-import", "win32com.client",
    "--hidden-import", "markitdown.converters",
    "src/markitdown_gui.py"  # Ensure this points to the src/ folder!
]
subprocess.check_call(cmd)
```

---

## 6. GUI Application Architecture Patterns

- **High-DPI Awareness on Windows:**
  ```python
  import ctypes
  try:
      ctypes.windll.shcore.SetProcessDpiAwareness(1)
  except Exception:
      try:
          ctypes.windll.user32.SetProcessDPIAware()
      except Exception: pass
  ```
- **Threaded Worker:** Always execute document parsing in a `threading.Thread(daemon=True)` worker to avoid freezing the Tkinter main loop.
- **Queue-Based UI Logging:** Worker threads push log messages `(message, level)` to a thread-safe `queue.Queue()`, which the main thread drains using `root.after(100, process_queue)`.
- **Traceback Visibility:** Always capture and log `traceback.format_exc()` on exceptions in the worker thread so silent errors are avoided.

---

## 7. Legacy Binary Formats (.doc, .ppt) COM Automation

MarkItDown natively fails on binary `.doc` and `.ppt` files. To solve this without third-party web APIs, use local Windows COM automation to invisibly resave them into OpenXML formats (`.docx`, `.pptx`) before handing them to MarkItDown. 

*Note: Requires `pip install pywin32` and a local Microsoft Office installation.*

### Word (.doc -> .docx)
```python
def _convert_legacy_doc_to_docx(doc_path: Path) -> Path:
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    temp_docx = doc_path.with_suffix(".temp_convert.docx")
    try:
        doc = word.Documents.Open(str(doc_path.resolve()))
        # 16 = wdFormatXMLDocument (standard docx)
        doc.SaveAs2(str(temp_docx.resolve()), FileFormat=16)
        doc.Close()
        return temp_docx
    finally:
        word.Quit()
```

### PowerPoint (.ppt -> .pptx)
```python
def _convert_legacy_ppt_to_pptx(ppt_path: Path) -> Path:
    import win32com.client
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    temp_pptx = ppt_path.with_suffix(".temp_convert.pptx")
    try:
        presentation = powerpoint.Presentations.Open(str(ppt_path.resolve()), WithWindow=False)
        # 24 = ppSaveAsOpenXMLPresentation (standard pptx)
        presentation.SaveAs(str(temp_pptx.resolve()), 24)
        presentation.Close()
        return temp_pptx
    finally:
        powerpoint.Quit()
```

---

## 8. Output Folder Isolation Pattern

To avoid cluttering the user's workspace when processing files (especially spreadsheets which produce many files), always isolate the output in a dedicated subdirectory named after the document:

```python
def get_isolated_output_dir(file_path: Path, output_dir: Path | None = None) -> Path:
    if output_dir is None:
        # Create a new folder matching the document's name
        output_dir = file_path.parent / file_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
```

---

## 9. Recommended Project Directory Structure

As the tool expands, avoid leaving Python source files, build scripts, and executables in a single flat folder. Instead, adopt a partitioned, role-based structure:

```text
Project_Root/
├── src/                       # All Python source code
│   ├── markitdown_multi_sheet.py
│   └── markitdown_gui.py
├── build_tools/               # PyInstaller scripts and batches
│   ├── build_exe.bat
│   └── build_exe.py
├── MarkItDownStudio.exe       # Final portable application
├── run_from_source.bat        # Fast-launch script for testing without building
├── SKILL.md                   # Documentation
└── README.md                  # User instructions
```

When separating files like this, always ensure your PyInstaller target points to `"src/markitdown_gui.py"` and your `.bat` runner scripts are updated to look inside the `src/` directory!
