#!/usr/bin/env python3
"""Thin wrapper delegating to E:\\harness2\\agy_memory.py."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

TARGET = Path(r"E:\harness2\agy_memory.py")
if str(TARGET.parent) not in sys.path:
    sys.path.insert(0, str(TARGET.parent))

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
