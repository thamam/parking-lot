"""
Tests for the NLP parser.
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mouceifi.parser import (
    NLPParser, Coordinate, MoveAbsoluteAction, MoveRelativeAction,
    ClickAction, DoubleClickAction, DragAction, ScrollAction,
    ClickButton, ScrollDirection
)


class TestNLPParser(unittest.TestCase):
    """Test cases for NLP parser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = NLPParser()

    def test_parse_simple_move(self):
        """Test parsing simple move command."""
        sequence = self.parser.parse("move to x=100 y=200")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, MoveAbsoluteAction)
        self.assertEqual(action.coordinate.x, 100)
        self.assertEqual(action.coordinate.y, 200)

    def test_parse_move_with_commas(self):
        """Test parsing move with comma separator."""
        sequence = self.parser.parse("move to x=500, y=300")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, MoveAbsoluteAction)
        self.assertEqual(action.coordinate.x, 500)
        self.assertEqual(action.coordinate.y, 300)

    def test_parse_move_and_click(self):
        """Test parsing move followed by click."""
        sequence = self.parser.parse("move to x=500 y=300 and then left click")
        self.assertEqual(len(sequence), 2)
        self.assertIsInstance(sequence.actions[0], MoveAbsoluteAction)
        self.assertIsInstance(sequence.actions[1], ClickAction)
        self.assertEqual(sequence.actions[1].button, ClickButton.LEFT)

    def test_parse_relative_move(self):
        """Test parsing relative move."""
        sequence = self.parser.parse("move 100 pixels down and 50 pixels right")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, MoveRelativeAction)
        self.assertEqual(action.dx, 50)  # right
        self.assertEqual(action.dy, 100)  # down

    def test_parse_double_click(self):
        """Test parsing double click."""
        sequence = self.parser.parse("double click")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, DoubleClickAction)

    def test_parse_drag(self):
        """Test parsing drag command."""
        sequence = self.parser.parse("drag from x=100 y=100 to x=300 y=300")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, DragAction)
        self.assertEqual(action.start.x, 100)
        self.assertEqual(action.start.y, 100)
        self.assertEqual(action.end.x, 300)
        self.assertEqual(action.end.y, 300)

    def test_parse_right_click(self):
        """Test parsing right click."""
        sequence = self.parser.parse("right click")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, ClickAction)
        self.assertEqual(action.button, ClickButton.RIGHT)

    def test_parse_middle_click(self):
        """Test parsing middle click."""
        sequence = self.parser.parse("middle click")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, ClickAction)
        self.assertEqual(action.button, ClickButton.MIDDLE)

    def test_parse_scroll(self):
        """Test parsing scroll command."""
        sequence = self.parser.parse("scroll down by 5")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, ScrollAction)
        self.assertEqual(action.direction, ScrollDirection.DOWN)
        self.assertEqual(action.amount, 5)

    def test_parse_scroll_default_amount(self):
        """Test parsing scroll with default amount."""
        sequence = self.parser.parse("scroll up")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, ScrollAction)
        self.assertEqual(action.direction, ScrollDirection.UP)
        self.assertEqual(action.amount, 3)  # default

    def test_parse_complex_sequence(self):
        """Test parsing complex action sequence from user example."""
        sequence = self.parser.parse(
            "move to x=500 y=300 and then left click"
        )
        self.assertEqual(len(sequence), 2)
        self.assertIsInstance(sequence.actions[0], MoveAbsoluteAction)
        self.assertIsInstance(sequence.actions[1], ClickAction)

    def test_parse_click_at_current_position(self):
        """Test parsing click at current position."""
        sequence = self.parser.parse("right click at current position")
        self.assertEqual(len(sequence), 1)
        action = sequence.actions[0]
        self.assertIsInstance(action, ClickAction)
        self.assertEqual(action.button, ClickButton.RIGHT)
        self.assertIsNone(action.coordinate)

    def test_parse_empty_command(self):
        """Test parsing empty command raises error."""
        with self.assertRaises(ValueError):
            self.parser.parse("")

    def test_parse_invalid_command(self):
        """Test parsing invalid command raises error."""
        with self.assertRaises(ValueError):
            self.parser.parse("do something random")

    def test_coordinate_validation(self):
        """Test coordinate validation."""
        # Valid coordinate
        coord = Coordinate(100, 200)
        self.assertEqual(coord.x, 100)
        self.assertEqual(coord.y, 200)

        # Should convert floats to ints
        coord = Coordinate(100.5, 200.7)
        self.assertEqual(coord.x, 100)
        self.assertEqual(coord.y, 200)


class TestParserValidation(unittest.TestCase):
    """Test validation methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = NLPParser()

    def test_validate_move_action(self):
        """Test validation of move action."""
        action = MoveAbsoluteAction(coordinate=Coordinate(100, 200))
        is_valid, error = self.parser.validate_action(action)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_negative_coordinates(self):
        """Test validation rejects negative coordinates."""
        action = MoveAbsoluteAction(coordinate=Coordinate(-100, 200))
        is_valid, error = self.parser.validate_action(action)
        self.assertFalse(is_valid)
        self.assertIn("Negative coordinates", error)

    def test_validate_drag_action(self):
        """Test validation of drag action."""
        action = DragAction(
            start=Coordinate(100, 100),
            end=Coordinate(300, 300)
        )
        is_valid, error = self.parser.validate_action(action)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
