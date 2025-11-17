"""
Base executor interface for platform abstraction.
"""
from abc import ABC, abstractmethod
from typing import Optional
from ..parser.types import (
    ActionSequence, MouseAction, MoveAbsoluteAction, MoveRelativeAction,
    ClickAction, DoubleClickAction, DragAction, ScrollAction, UISelectAction,
    Coordinate
)


class MouseExecutor(ABC):
    """Abstract base class for platform-specific mouse executors."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize executor.

        Args:
            dry_run: If True, log actions instead of executing them
        """
        self.dry_run = dry_run

    @abstractmethod
    def get_screen_size(self) -> Coordinate:
        """Get the screen dimensions."""
        pass

    @abstractmethod
    def get_current_position(self) -> Coordinate:
        """Get current mouse position."""
        pass

    @abstractmethod
    def move_to(self, coord: Coordinate, duration: float = 0.0):
        """Move mouse to absolute position."""
        pass

    @abstractmethod
    def move_relative(self, dx: int, dy: int, duration: float = 0.0):
        """Move mouse relative to current position."""
        pass

    @abstractmethod
    def click(self, button: str, coord: Optional[Coordinate] = None):
        """Click at current or specified position."""
        pass

    @abstractmethod
    def double_click(self, button: str, coord: Optional[Coordinate] = None):
        """Double-click at current or specified position."""
        pass

    @abstractmethod
    def drag(self, start: Coordinate, end: Coordinate, button: str = 'left', duration: float = 0.5):
        """Drag from start to end position."""
        pass

    @abstractmethod
    def scroll(self, direction: str, amount: int):
        """Scroll in specified direction."""
        pass

    @abstractmethod
    def find_ui_element(self, label: Optional[str] = None, pattern: Optional[str] = None) -> Optional[Coordinate]:
        """
        Find UI element by label or pattern.

        Returns:
            Coordinate of element if found, None otherwise
        """
        pass

    def execute_action(self, action: MouseAction):
        """Execute a single mouse action."""
        if isinstance(action, MoveAbsoluteAction):
            self._log_action(f"Moving to ({action.coordinate.x}, {action.coordinate.y})")
            if not self.dry_run:
                self.move_to(action.coordinate)

        elif isinstance(action, MoveRelativeAction):
            self._log_action(f"Moving relative ({action.dx:+d}, {action.dy:+d})")
            if not self.dry_run:
                self.move_relative(action.dx, action.dy)

        elif isinstance(action, ClickAction):
            if action.coordinate:
                self._log_action(f"{action.button.value.capitalize()} clicking at ({action.coordinate.x}, {action.coordinate.y})")
            else:
                self._log_action(f"{action.button.value.capitalize()} clicking at current position")
            if not self.dry_run:
                self.click(action.button.value, action.coordinate)

        elif isinstance(action, DoubleClickAction):
            if action.coordinate:
                self._log_action(f"Double-clicking at ({action.coordinate.x}, {action.coordinate.y})")
            else:
                self._log_action(f"Double-clicking at current position")
            if not self.dry_run:
                self.double_click(action.button.value, action.coordinate)

        elif isinstance(action, DragAction):
            self._log_action(
                f"Dragging from ({action.start.x}, {action.start.y}) to ({action.end.x}, {action.end.y})"
            )
            if not self.dry_run:
                self.drag(action.start, action.end, action.button.value)

        elif isinstance(action, ScrollAction):
            self._log_action(f"Scrolling {action.direction.value} by {action.amount}")
            if not self.dry_run:
                self.scroll(action.direction.value, action.amount)

        elif isinstance(action, UISelectAction):
            if action.label:
                self._log_action(f"Selecting UI element with label: {action.label}")
            else:
                self._log_action(f"Selecting UI element matching pattern: {action.pattern}")
            if not self.dry_run:
                coord = self.find_ui_element(action.label, action.pattern)
                if coord:
                    self.move_to(coord)
                    self.click('left')
                else:
                    raise ValueError(f"Could not find UI element: {action.label or action.pattern}")

        else:
            raise NotImplementedError(f"Action type {type(action)} not implemented")

    def execute_sequence(self, sequence: ActionSequence):
        """Execute a sequence of mouse actions."""
        self._log_action(f"\n=== Executing {len(sequence)} action(s) ===")
        for i, action in enumerate(sequence.actions, 1):
            self._log_action(f"\n[Action {i}/{len(sequence)}]")
            self.execute_action(action)
        self._log_action("\n=== Sequence complete ===\n")

    def _log_action(self, message: str):
        """Log an action message."""
        prefix = "[DRY RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")

    def validate_coordinate(self, coord: Coordinate) -> bool:
        """Validate that coordinate is within screen bounds."""
        screen = self.get_screen_size()
        return 0 <= coord.x < screen.x and 0 <= coord.y < screen.y
