"""
Windows-specific mouse executor (stub for future implementation).
"""
from typing import Optional
from ..parser.types import Coordinate
from .base import MouseExecutor


class WindowsMouseExecutor(MouseExecutor):
    """
    Windows mouse executor (placeholder).

    For production implementation, consider:
    - pyautogui (cross-platform, works on Windows)
    - pywinauto (Windows-specific, more powerful)
    - ctypes with Windows API calls
    """

    def __init__(self, dry_run: bool = False):
        super().__init__(dry_run)
        raise NotImplementedError(
            "Windows executor not yet implemented. "
            "To implement, use pyautogui or pywinauto."
        )

    def get_screen_size(self) -> Coordinate:
        raise NotImplementedError()

    def get_current_position(self) -> Coordinate:
        raise NotImplementedError()

    def move_to(self, coord: Coordinate, duration: float = 0.0):
        raise NotImplementedError()

    def move_relative(self, dx: int, dy: int, duration: float = 0.0):
        raise NotImplementedError()

    def click(self, button: str, coord: Optional[Coordinate] = None):
        raise NotImplementedError()

    def double_click(self, button: str, coord: Optional[Coordinate] = None):
        raise NotImplementedError()

    def drag(self, start: Coordinate, end: Coordinate, button: str = 'left', duration: float = 0.5):
        raise NotImplementedError()

    def scroll(self, direction: str, amount: int):
        raise NotImplementedError()

    def find_ui_element(self, label: Optional[str] = None, pattern: Optional[str] = None) -> Optional[Coordinate]:
        raise NotImplementedError()
