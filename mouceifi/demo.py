#!/usr/bin/env python3
"""
Demo script for Mouceifi - shows parsing and dry-run execution without dependencies.

This script demonstrates the NLP parser and command execution in dry-run mode,
which doesn't require PyAutoGUI or other system dependencies to be installed.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mouceifi.parser import NLPParser
from mouceifi.parser.types import *


def demo_parser():
    """Demonstrate the NLP parser capabilities."""
    print("=" * 70)
    print("MOUCEIFI PARSER DEMONSTRATION")
    print("=" * 70)
    print()

    parser = NLPParser()

    # Test commands from the requirements
    test_commands = [
        "move to x=500 y=300 and then left click",
        "right click at current position",
        "move 100 pixels down and 50 pixels right then double click",
        "drag from x=100 y=100 to x=300 y=300",
        "scroll down by 5",
        "left click",
        "move to x=100 y=100",
    ]

    for i, command in enumerate(test_commands, 1):
        print(f"\n[Test {i}] Command: \"{command}\"")
        print("-" * 70)

        try:
            sequence = parser.parse(command, dry_run=True)
            print(f"✓ Parsed successfully: {len(sequence)} action(s)")

            for j, action in enumerate(sequence.actions, 1):
                print(f"  Action {j}: {action.action_type.value}")

                if isinstance(action, MoveAbsoluteAction):
                    print(f"    → Move to ({action.coordinate.x}, {action.coordinate.y})")

                elif isinstance(action, MoveRelativeAction):
                    print(f"    → Move relative ({action.dx:+d}, {action.dy:+d})")

                elif isinstance(action, ClickAction):
                    if action.coordinate:
                        print(f"    → {action.button.value} click at ({action.coordinate.x}, {action.coordinate.y})")
                    else:
                        print(f"    → {action.button.value} click at current position")

                elif isinstance(action, DoubleClickAction):
                    print(f"    → Double-click")

                elif isinstance(action, DragAction):
                    print(f"    → Drag from ({action.start.x}, {action.start.y}) to ({action.end.x}, {action.end.y})")

                elif isinstance(action, ScrollAction):
                    print(f"    → Scroll {action.direction.value} by {action.amount}")

        except ValueError as e:
            print(f"✗ Parse error: {e}")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Note: This demo only shows parsing. To execute mouse commands,")
    print("install dependencies with: pip install -r requirements.txt")
    print()
    print("Then run: python -m mouceifi --dry-run \"your command\"")
    print("Or:       python -m mouceifi --interactive")


if __name__ == '__main__':
    demo_parser()
