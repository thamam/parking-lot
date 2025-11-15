#!/usr/bin/env python3
"""Main entry point for Hebrew OCR CLI."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hebrew_ocr.cli import cli

if __name__ == '__main__':
    cli()
