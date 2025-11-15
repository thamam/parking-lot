"""Hebrew OCR to Markdown Converter

A tool for converting Hebrew documents (PDFs and images) to Markdown format
using Tesseract OCR and LLM-based text correction.
"""

__version__ = "0.1.0"

from .ocr_engine import OCREngine
from .llm_corrector import LLMCorrector
from .pipeline import HebrewOCRPipeline

__all__ = ["OCREngine", "LLMCorrector", "HebrewOCRPipeline"]
