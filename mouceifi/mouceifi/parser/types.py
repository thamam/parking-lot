"""
Type definitions for mouse actions and commands.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class ActionType(Enum):
    """Supported mouse action types."""
    MOVE_ABSOLUTE = "move_absolute"
    MOVE_RELATIVE = "move_relative"
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    DRAG = "drag"
    SCROLL = "scroll"
    UI_SELECT = "ui_select"


class ClickButton(Enum):
    """Mouse button types."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class ScrollDirection(Enum):
    """Scroll directions."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Coordinate:
    """Represents a 2D coordinate."""
    x: int
    y: int

    def __post_init__(self):
        if not isinstance(self.x, (int, float)):
            raise ValueError(f"X coordinate must be numeric, got {type(self.x)}")
        if not isinstance(self.y, (int, float)):
            raise ValueError(f"Y coordinate must be numeric, got {type(self.y)}")
        self.x = int(self.x)
        self.y = int(self.y)


@dataclass
class MouseAction:
    """Base class for all mouse actions."""
    action_type: ActionType = field(init=False)


@dataclass
class MoveAbsoluteAction(MouseAction):
    """Move to absolute coordinates."""
    coordinate: Coordinate

    def __post_init__(self):
        self.action_type = ActionType.MOVE_ABSOLUTE


@dataclass
class MoveRelativeAction(MouseAction):
    """Move relative to current position."""
    dx: int
    dy: int

    def __post_init__(self):
        self.action_type = ActionType.MOVE_RELATIVE


@dataclass
class ClickAction(MouseAction):
    """Click at current or specified position."""
    button: ClickButton
    coordinate: Optional[Coordinate] = None

    def __post_init__(self):
        self.action_type = ActionType.CLICK


@dataclass
class DoubleClickAction(MouseAction):
    """Double-click at current or specified position."""
    button: ClickButton = ClickButton.LEFT
    coordinate: Optional[Coordinate] = None

    def __post_init__(self):
        self.action_type = ActionType.DOUBLE_CLICK


@dataclass
class DragAction(MouseAction):
    """Drag from one position to another."""
    start: Coordinate
    end: Coordinate
    button: ClickButton = ClickButton.LEFT

    def __post_init__(self):
        self.action_type = ActionType.DRAG


@dataclass
class ScrollAction(MouseAction):
    """Scroll in a direction by amount."""
    direction: ScrollDirection
    amount: int

    def __post_init__(self):
        self.action_type = ActionType.SCROLL


@dataclass
class UISelectAction(MouseAction):
    """Select a UI element by label or pattern."""
    label: Optional[str] = None
    pattern: Optional[str] = None
    action_after: Optional[str] = None  # e.g., "click", "double_click"

    def __post_init__(self):
        self.action_type = ActionType.UI_SELECT
        if not self.label and not self.pattern:
            raise ValueError("Either label or pattern must be specified")


@dataclass
class ActionSequence:
    """A sequence of mouse actions to execute."""
    actions: List[MouseAction]
    dry_run: bool = False

    def add_action(self, action: MouseAction):
        """Add an action to the sequence."""
        self.actions.append(action)

    def __len__(self):
        return len(self.actions)
