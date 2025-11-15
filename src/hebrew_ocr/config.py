"""Configuration management for Hebrew OCR."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the Hebrew OCR pipeline."""

    # Tesseract Settings
    TESSERACT_LANG: str = os.getenv("TESSERACT_LANG", "heb")
    DPI: int = int(os.getenv("DPI", "300"))

    # LLM Settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "aya:8b")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    USE_LLM_CORRECTION: bool = os.getenv("USE_LLM_CORRECTION", "true").lower() == "true"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def from_env(cls, env_file: Optional[Path] = None):
        """Load configuration from a specific .env file.

        Args:
            env_file: Path to .env file
        """
        if env_file:
            load_dotenv(env_file)
        return cls()
