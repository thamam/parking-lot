"""
Validation utilities for mouse commands.
"""
from typing import Tuple, Optional
from ..parser.types import Coordinate, MouseAction, ActionSequence


def validate_coordinate_bounds(coord: Coordinate, screen_size: Coordinate) -> Tuple[bool, Optional[str]]:
    """
    Validate that a coordinate is within screen bounds.

    Args:
        coord: Coordinate to validate
        screen_size: Screen dimensions

    Returns:
        (is_valid, error_message)
    """
    if coord.x < 0 or coord.y < 0:
        return False, f"Negative coordinates not allowed: ({coord.x}, {coord.y})"

    if coord.x >= screen_size.x or coord.y >= screen_size.y:
        return False, (
            f"Coordinate ({coord.x}, {coord.y}) out of screen bounds "
            f"({screen_size.x}, {screen_size.y})"
        )

    return True, None


def validate_action_sequence(sequence: ActionSequence, screen_size: Optional[Coordinate] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate an entire action sequence.

    Args:
        sequence: ActionSequence to validate
        screen_size: Optional screen size for bounds checking

    Returns:
        (is_valid, error_message)
    """
    if not sequence.actions:
        return False, "Action sequence is empty"

    # Validate each action
    for i, action in enumerate(sequence.actions):
        is_valid, error = validate_action(action, screen_size)
        if not is_valid:
            return False, f"Action {i+1}: {error}"

    return True, None


def validate_action(action: MouseAction, screen_size: Optional[Coordinate] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate a single action.

    Args:
        action: MouseAction to validate
        screen_size: Optional screen size for bounds checking

    Returns:
        (is_valid, error_message)
    """
    # Add action-specific validation here
    # For now, basic validation is done in the parser
    return True, None
