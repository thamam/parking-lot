"""Configuration management for Hebrew OCR."""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def _get_int(key: str, default: int) -> int:
    """Safely get an integer from environment variables.

    Args:
        key: Environment variable key
        default: Default value if not found or invalid

    Returns:
        Integer value
    """
    value = os.getenv(key)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        logger.warning(f"Invalid integer value for {key}='{value}', using default: {default}")
        return default


def _get_float(key: str, default: float) -> float:
    """Safely get a float from environment variables.

    Args:
        key: Environment variable key
        default: Default value if not found or invalid

    Returns:
        Float value
    """
    value = os.getenv(key)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        logger.warning(f"Invalid float value for {key}='{value}', using default: {default}")
        return default


def _get_bool(key: str, default: bool) -> bool:
    """Safely get a boolean from environment variables.

    Args:
        key: Environment variable key
        default: Default value if not found

    Returns:
        Boolean value
    """
    value = os.getenv(key)
    if value is None:
        return default

    return value.lower() in ('true', '1', 'yes', 'on')


class Config:
    """Configuration settings for the Hebrew OCR pipeline."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        # Tesseract Settings
        self.TESSERACT_LANG: str = os.getenv("TESSERACT_LANG", "heb")
        self.DPI: int = _get_int("DPI", 300)

        # LLM Settings
        self.LLM_MODEL: str = os.getenv("LLM_MODEL", "aya:8b")
        self.LLM_TEMPERATURE: float = _get_float("LLM_TEMPERATURE", 0.3)
        self.LLM_MAX_TOKENS: int = _get_int("LLM_MAX_TOKENS", 2000)
        self.USE_LLM_CORRECTION: bool = _get_bool("USE_LLM_CORRECTION", True)

        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def from_env_file(cls, env_file: Path) -> "Config":
        """Load configuration from a specific .env file.

        Args:
            env_file: Path to .env file

        Returns:
            Config instance with loaded settings
        """
        if env_file.exists():
            load_dotenv(env_file, override=True)
        else:
            logger.warning(f"Config file not found: {env_file}")

        return cls()


# Load default .env file if it exists
load_dotenv()
