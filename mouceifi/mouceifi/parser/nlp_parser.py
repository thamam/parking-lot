"""
Natural language parser for mouse commands.
"""
import re
from typing import List, Optional, Tuple
from .types import (
    ActionSequence, MouseAction, MoveAbsoluteAction, MoveRelativeAction,
    ClickAction, DoubleClickAction, DragAction, ScrollAction, UISelectAction,
    Coordinate, ClickButton, ScrollDirection
)


class NLPParser:
    """Parse natural language commands into structured mouse actions."""

    def __init__(self):
        # Compile regex patterns for efficiency
        self.coord_pattern = re.compile(r'x\s*=\s*(\d+)\s*[,\s]\s*y\s*=\s*(\d+)', re.IGNORECASE)
        self.relative_pattern = re.compile(r'(\d+)\s*pixels?\s+(up|down|left|right)', re.IGNORECASE)
        self.button_pattern = re.compile(r'\b(left|right|middle)\s+click\b', re.IGNORECASE)
        self.double_click_pattern = re.compile(r'\bdouble\s*[-\s]?click\b', re.IGNORECASE)
        self.drag_pattern = re.compile(
            r'drag\s+from\s+x\s*=\s*(\d+)\s*[,\s]\s*y\s*=\s*(\d+)\s+to\s+x\s*=\s*(\d+)\s*[,\s]\s*y\s*=\s*(\d+)',
            re.IGNORECASE
        )
        self.scroll_pattern = re.compile(r'scroll\s+(up|down|left|right)(?:\s+by\s+(\d+))?', re.IGNORECASE)
        self.ui_select_pattern = re.compile(r"select\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)
        self.ui_pattern_match = re.compile(r"file\s+starting\s+with\s+([^\s]+)", re.IGNORECASE)

    def parse(self, command: str, dry_run: bool = False) -> ActionSequence:
        """
        Parse a natural language command into an action sequence.

        Args:
            command: Natural language command string
            dry_run: If True, actions will be logged but not executed

        Returns:
            ActionSequence containing parsed actions

        Raises:
            ValueError: If command cannot be parsed
        """
        # Split command by common separators (and then, then)
        # Don't split on "and" alone, as it might be part of compound moves like "move X and Y"
        parts = re.split(r'\s+(?:and\s+)?then\s+|\s+and\s+then\s+', command, flags=re.IGNORECASE)

        actions: List[MouseAction] = []
        for part in parts:
            part = part.strip()
            if not part:
                continue

            action = self._parse_single_command(part)
            if action:
                actions.append(action)

        if not actions:
            raise ValueError(f"Could not parse any actions from command: {command}")

        return ActionSequence(actions=actions, dry_run=dry_run)

    def _parse_single_command(self, command: str) -> Optional[MouseAction]:
        """Parse a single command (no separators)."""
        command = command.strip()

        # Try to parse drag (must come before move, as it contains 'to')
        drag_match = self.drag_pattern.search(command)
        if drag_match:
            x1, y1, x2, y2 = map(int, drag_match.groups())
            return DragAction(
                start=Coordinate(x1, y1),
                end=Coordinate(x2, y2)
            )

        # Try to parse absolute move with click
        move_click_match = re.search(
            r'move\s+to\s+x\s*=\s*(\d+)\s*[,\s]\s*y\s*=\s*(\d+)(?:\s+(?:and\s+)?(?:then\s+)?(.+))?',
            command,
            re.IGNORECASE
        )
        if move_click_match:
            x, y, rest = move_click_match.groups()
            actions = [MoveAbsoluteAction(coordinate=Coordinate(int(x), int(y)))]
            # If there's a trailing action (like "and then left click")
            if rest and rest.strip():
                trailing_action = self._parse_single_command(rest.strip())
                if trailing_action:
                    # Return only the move for now; the rest will be parsed separately
                    pass
            return actions[0]

        # Try to parse absolute move
        coord_match = self.coord_pattern.search(command)
        if coord_match and 'move' in command.lower():
            x, y = map(int, coord_match.groups())
            return MoveAbsoluteAction(coordinate=Coordinate(x, y))

        # Try to parse relative move (multiple relative moves in one command)
        relative_moves = self.relative_pattern.findall(command)
        if relative_moves and 'move' in command.lower():
            dx, dy = 0, 0
            for amount, direction in relative_moves:
                amount = int(amount)
                direction = direction.lower()
                if direction == 'right':
                    dx += amount
                elif direction == 'left':
                    dx -= amount
                elif direction == 'down':
                    dy += amount
                elif direction == 'up':
                    dy -= amount
            return MoveRelativeAction(dx=dx, dy=dy)

        # Try to parse double click
        if self.double_click_pattern.search(command):
            coord_match = self.coord_pattern.search(command)
            coord = Coordinate(int(coord_match.group(1)), int(coord_match.group(2))) if coord_match else None
            return DoubleClickAction(coordinate=coord)

        # Try to parse click
        button_match = self.button_pattern.search(command)
        if button_match or 'click' in command.lower():
            button_str = button_match.group(1).lower() if button_match else 'left'
            button = ClickButton[button_str.upper()]

            # Check for coordinate in click command
            coord_match = self.coord_pattern.search(command)
            coord = Coordinate(int(coord_match.group(1)), int(coord_match.group(2))) if coord_match else None

            # Check for "at current position"
            if 'current position' in command.lower():
                coord = None

            return ClickAction(button=button, coordinate=coord)

        # Try to parse scroll
        scroll_match = self.scroll_pattern.search(command)
        if scroll_match:
            direction_str, amount_str = scroll_match.groups()
            direction = ScrollDirection[direction_str.upper()]
            amount = int(amount_str) if amount_str else 3
            return ScrollAction(direction=direction, amount=amount)

        # Try to parse UI selection
        ui_select_match = self.ui_select_pattern.search(command)
        if ui_select_match:
            label = ui_select_match.group(1)
            return UISelectAction(label=label)

        # Try to parse UI pattern matching
        ui_pattern = self.ui_pattern_match.search(command)
        if ui_pattern:
            pattern = ui_pattern.group(1)
            return UISelectAction(pattern=pattern)

        # If nothing matched, return None (caller will handle)
        return None

    def validate_action(self, action: MouseAction) -> Tuple[bool, Optional[str]]:
        """
        Validate an action for correctness.

        Returns:
            (is_valid, error_message)
        """
        if isinstance(action, (MoveAbsoluteAction, ClickAction, DoubleClickAction)):
            coord = getattr(action, 'coordinate', None)
            if coord:
                if coord.x < 0 or coord.y < 0:
                    return False, f"Negative coordinates not allowed: ({coord.x}, {coord.y})"
                # Add screen bounds check if needed (would require screen size detection)

        if isinstance(action, DragAction):
            if action.start.x < 0 or action.start.y < 0:
                return False, f"Negative start coordinates: ({action.start.x}, {action.start.y})"
            if action.end.x < 0 or action.end.y < 0:
                return False, f"Negative end coordinates: ({action.end.x}, {action.end.y})"

        return True, None
