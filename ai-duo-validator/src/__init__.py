"""
AI Duo Validator - Orchestrator for AI-to-AI validation coordination.
"""

from .orchestrator import AIOrchestrator
from .parser import extract_handoff, extract_validation, ParserError
from .state import SessionState
from .formatter import (
    format_handoff_for_validator,
    format_validation_for_executor,
    pretty_print_handoff,
    pretty_print_validation
)

__version__ = '1.0.0'

__all__ = [
    'AIOrchestrator',
    'extract_handoff',
    'extract_validation',
    'ParserError',
    'SessionState',
    'format_handoff_for_validator',
    'format_validation_for_executor',
    'pretty_print_handoff',
    'pretty_print_validation'
]
