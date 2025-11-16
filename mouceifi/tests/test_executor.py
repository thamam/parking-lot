"""
Tests for the executor module.
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mouceifi.executor import get_executor, LinuxMouseExecutor
from mouceifi.parser import (
    Coordinate, MoveAbsoluteAction, MoveRelativeAction,
    ClickAction, DoubleClickAction, DragAction, ScrollAction,
    ActionSequence, ClickButton, ScrollDirection
)


class TestExecutorFactory(unittest.TestCase):
    """Test executor factory function."""

    def test_get_linux_executor(self):
        """Test getting Linux executor."""
        executor = get_executor(dry_run=True, platform_name='linux')
        self.assertIsInstance(executor, LinuxMouseExecutor)
        self.assertTrue(executor.dry_run)

    def test_get_executor_unsupported_platform(self):
        """Test getting executor for unsupported platform."""
        with self.assertRaises(NotImplementedError):
            get_executor(platform_name='unsupported')


class TestLinuxExecutor(unittest.TestCase):
    """Test Linux executor (in dry-run mode)."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = LinuxMouseExecutor(dry_run=True)

    def test_get_screen_size(self):
        """Test getting screen size."""
        size = self.executor.get_screen_size()
        self.assertIsInstance(size, Coordinate)
        self.assertGreater(size.x, 0)
        self.assertGreater(size.y, 0)

    def test_get_current_position(self):
        """Test getting current position."""
        pos = self.executor.get_current_position()
        self.assertIsInstance(pos, Coordinate)

    def test_execute_move_action(self):
        """Test executing move action."""
        action = MoveAbsoluteAction(coordinate=Coordinate(100, 200))
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_click_action(self):
        """Test executing click action."""
        action = ClickAction(button=ClickButton.LEFT)
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_double_click_action(self):
        """Test executing double click action."""
        action = DoubleClickAction()
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_drag_action(self):
        """Test executing drag action."""
        action = DragAction(
            start=Coordinate(100, 100),
            end=Coordinate(300, 300)
        )
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_scroll_action(self):
        """Test executing scroll action."""
        action = ScrollAction(direction=ScrollDirection.DOWN, amount=5)
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_relative_move(self):
        """Test executing relative move."""
        action = MoveRelativeAction(dx=50, dy=100)
        # Should not raise exception
        self.executor.execute_action(action)

    def test_execute_action_sequence(self):
        """Test executing action sequence."""
        sequence = ActionSequence(actions=[
            MoveAbsoluteAction(coordinate=Coordinate(100, 100)),
            ClickAction(button=ClickButton.LEFT),
            MoveRelativeAction(dx=50, dy=50),
            DoubleClickAction()
        ])
        # Should not raise exception
        self.executor.execute_sequence(sequence)

    def test_validate_coordinate_in_bounds(self):
        """Test coordinate validation within bounds."""
        coord = Coordinate(100, 100)
        self.assertTrue(self.executor.validate_coordinate(coord))

    def test_validate_coordinate_out_of_bounds(self):
        """Test coordinate validation out of bounds."""
        # Get screen size
        screen = self.executor.get_screen_size()
        # Create coordinate outside bounds
        coord = Coordinate(screen.x + 100, screen.y + 100)
        self.assertFalse(self.executor.validate_coordinate(coord))

    def test_move_to_invalid_coordinate(self):
        """Test that moving to invalid coordinate raises error."""
        # Create an executor that would actually validate (not in dry-run for this specific test)
        # But we'll use dry-run to avoid actual mouse movement
        screen = self.executor.get_screen_size()
        invalid_coord = Coordinate(screen.x + 1000, screen.y + 1000)

        with self.assertRaises(ValueError):
            self.executor.move_to(invalid_coord)


if __name__ == '__main__':
    unittest.main()
