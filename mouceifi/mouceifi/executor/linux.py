"""
Linux-specific mouse executor using PyAutoGUI.
"""
import os
import time
from typing import Optional
import pyautogui
from ..parser.types import Coordinate
from .base import MouseExecutor


class LinuxMouseExecutor(MouseExecutor):
    """Linux mouse executor using PyAutoGUI with X11/Wayland support."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize Linux mouse executor.

        Args:
            dry_run: If True, log actions instead of executing them
        """
        super().__init__(dry_run)

        # Detect display server
        self.display_server = self._detect_display_server()
        self._log_action(f"Detected display server: {self.display_server}")

        # Configure PyAutoGUI
        if not dry_run:
            # Disable fail-safe (move mouse to corner to abort)
            # pyautogui.FAILSAFE = True  # Keep enabled for safety
            # Set pause between actions (0 for immediate execution)
            pyautogui.PAUSE = 0.1

    def _detect_display_server(self) -> str:
        """Detect whether running on X11 or Wayland."""
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        if 'wayland' in session_type:
            return 'wayland'
        elif 'x11' in session_type or os.environ.get('DISPLAY'):
            return 'x11'
        return 'unknown'

    def get_screen_size(self) -> Coordinate:
        """Get the screen dimensions."""
        if self.dry_run:
            return Coordinate(1920, 1080)  # Default for dry run
        size = pyautogui.size()
        return Coordinate(size.width, size.height)

    def get_current_position(self) -> Coordinate:
        """Get current mouse position."""
        if self.dry_run:
            return Coordinate(0, 0)
        pos = pyautogui.position()
        return Coordinate(pos.x, pos.y)

    def move_to(self, coord: Coordinate, duration: float = 0.0):
        """
        Move mouse to absolute position.

        Args:
            coord: Target coordinate
            duration: Time in seconds to complete the move (0 for instant)
        """
        if not self.validate_coordinate(coord):
            screen = self.get_screen_size()
            raise ValueError(
                f"Coordinate ({coord.x}, {coord.y}) out of bounds. "
                f"Screen size: ({screen.x}, {screen.y})"
            )

        if not self.dry_run:
            pyautogui.moveTo(coord.x, coord.y, duration=duration)

    def move_relative(self, dx: int, dy: int, duration: float = 0.0):
        """
        Move mouse relative to current position.

        Args:
            dx: Horizontal offset
            dy: Vertical offset
            duration: Time in seconds to complete the move
        """
        if not self.dry_run:
            pyautogui.moveRel(dx, dy, duration=duration)

    def click(self, button: str, coord: Optional[Coordinate] = None):
        """
        Click at current or specified position.

        Args:
            button: Button to click ('left', 'right', 'middle')
            coord: Optional coordinate to click at
        """
        if coord and not self.dry_run:
            self.move_to(coord)

        if not self.dry_run:
            pyautogui.click(button=button)

    def double_click(self, button: str, coord: Optional[Coordinate] = None):
        """
        Double-click at current or specified position.

        Args:
            button: Button to double-click
            coord: Optional coordinate to double-click at
        """
        if coord and not self.dry_run:
            self.move_to(coord)

        if not self.dry_run:
            pyautogui.doubleClick(button=button)

    def drag(self, start: Coordinate, end: Coordinate, button: str = 'left', duration: float = 0.5):
        """
        Drag from start to end position.

        Args:
            start: Starting coordinate
            end: Ending coordinate
            button: Button to hold while dragging
            duration: Time in seconds to complete the drag
        """
        if not self.validate_coordinate(start):
            raise ValueError(f"Start coordinate ({start.x}, {start.y}) out of bounds")
        if not self.validate_coordinate(end):
            raise ValueError(f"End coordinate ({end.x}, {end.y}) out of bounds")

        if not self.dry_run:
            # Move to start position
            self.move_to(start)
            # Perform drag
            pyautogui.drag(end.x - start.x, end.y - start.y, duration=duration, button=button)

    def scroll(self, direction: str, amount: int):
        """
        Scroll in specified direction.

        Args:
            direction: Direction to scroll ('up', 'down', 'left', 'right')
            amount: Amount to scroll (scroll clicks)
        """
        if not self.dry_run:
            if direction == 'up':
                pyautogui.scroll(amount)
            elif direction == 'down':
                pyautogui.scroll(-amount)
            elif direction == 'left':
                pyautogui.hscroll(-amount)
            elif direction == 'right':
                pyautogui.hscroll(amount)

    def find_ui_element(self, label: Optional[str] = None, pattern: Optional[str] = None) -> Optional[Coordinate]:
        """
        Find UI element by label or pattern using PyAutoGUI's image recognition.

        Note: This is a basic implementation. For production use, consider:
        - OCR libraries (pytesseract) for text recognition
        - Template matching with screenshots
        - Accessibility APIs (AT-SPI on Linux)

        Args:
            label: Text label to find
            pattern: Pattern to match

        Returns:
            Coordinate of element if found, None otherwise
        """
        # Basic implementation: Try to find by image template
        # In production, you'd want to use OCR or accessibility APIs

        if self.dry_run:
            self._log_action(f"Would search for UI element: {label or pattern}")
            return Coordinate(100, 100)  # Mock coordinate for dry run

        # For now, raise NotImplementedError with helpful message
        # In production, implement using:
        # 1. pytesseract for OCR
        # 2. pyautogui.locateOnScreen() for image matching
        # 3. AT-SPI/accessibility APIs for native UI element detection

        raise NotImplementedError(
            "UI element detection requires additional setup. Options:\n"
            "1. Image-based: Use pyautogui.locateOnScreen(image_path)\n"
            "2. Text-based: Install pytesseract for OCR\n"
            "3. Accessibility: Use AT-SPI/atspi Python bindings"
        )
