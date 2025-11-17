"""
FreeCAD LLM Framework

A production-ready framework for LLM-based manipulation of FreeCAD files
with comprehensive safety constraints.
"""

__version__ = "1.0.0"
__author__ = "FreeCAD LLM Framework Team"

# Core imports
from .core.file_parser import FreeCADFileParser
from .core.llm_interface import LLMInterface, LLMProvider
from .core.command_translator import CommandTranslator
from .core.executor import OperationExecutor

# Safety imports
from .safety.rules import SafetyRules, SafetyMode, PermissionLevel
from .safety.validator import SafetyValidator
from .safety.rollback import RollbackManager

# Operations imports
from .operations.basic_shapes import BasicShapeOperations
from .operations.bim_elements import BIMOperations
from .operations.properties import PropertyOperations

__all__ = [
    # Version info
    '__version__',

    # Core
    'FreeCADFileParser',
    'LLMInterface',
    'LLMProvider',
    'CommandTranslator',
    'OperationExecutor',

    # Safety
    'SafetyRules',
    'SafetyMode',
    'PermissionLevel',
    'SafetyValidator',
    'RollbackManager',

    # Operations
    'BasicShapeOperations',
    'BIMOperations',
    'PropertyOperations',
]
