#!/usr/bin/env python3
"""Setup script for Conversation Review Voice Agent."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="conversation-review-voice-agent",
    version="1.0.0",
    description="Analyzes Claude Code conversations and facilitates decision-making through voice interaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anthropic",
    author_email="",
    url="https://github.com/anthropics/conversation-review-voice-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["conversation_review_agent"],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "voice": [
            # Future v2 voice integration dependencies
            # "openai-whisper>=20230124",
            # "elevenlabs>=0.2.0",
            # "pyaudio>=0.2.13",
            # "pydub>=0.25.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "conversation-review=conversation_review_agent:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="conversation analysis decision-making voice-interaction claude-code",
)
