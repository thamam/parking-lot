"""
Mouceifi - Natural Language to Mouse Command Translator
"""

__version__ = '0.1.0'
__author__ = 'Mouceifi Contributors'

from .parser import NLPParser
from .executor import get_executor, MouseExecutor

__all__ = ['NLPParser', 'get_executor', 'MouseExecutor', '__version__']
