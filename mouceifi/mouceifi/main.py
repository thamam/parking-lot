#!/usr/bin/env python3
"""
Main CLI interface for Mouceifi - Natural Language Mouse Control.
"""
import sys
import argparse
from typing import Optional
from .parser import NLPParser
from .executor import get_executor
from .utils import validate_action_sequence


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Mouceifi - Natural Language to Mouse Command Translator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "move to x=500 y=300 and then left click"
  %(prog)s "right click at current position"
  %(prog)s "move 100 pixels down and 50 pixels right then double click"
  %(prog)s "drag from x=100 y=100 to x=300 y=300"
  %(prog)s --dry-run "move to x=100 y=100 then left click"
  %(prog)s --interactive

For interactive mode, type 'help' for more commands.
        '''
    )

    parser.add_argument(
        'command',
        nargs='?',
        help='Natural language mouse command to execute'
    )

    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Parse and display actions without executing them'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive mode for entering multiple commands'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--platform',
        choices=['linux', 'windows', 'darwin'],
        help='Override platform detection (for testing)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.interactive and not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize parser and executor
    nlp_parser = NLPParser()

    try:
        executor = get_executor(dry_run=args.dry_run, platform_name=args.platform)
    except NotImplementedError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        screen_size = executor.get_screen_size()
        print(f"Screen size: {screen_size.x}x{screen_size.y}")
        if not args.dry_run:
            current_pos = executor.get_current_position()
            print(f"Current position: ({current_pos.x}, {current_pos.y})")

    # Interactive mode
    if args.interactive:
        run_interactive_mode(nlp_parser, executor, args.verbose)
        return

    # Single command mode
    try:
        execute_command(args.command, nlp_parser, executor, args.verbose, args.dry_run)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def execute_command(
    command: str,
    nlp_parser: NLPParser,
    executor,
    verbose: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Execute a single command.

    Returns:
        True if successful, False otherwise
    """
    try:
        # Parse command
        if verbose:
            print(f"\nParsing: {command}")

        action_sequence = nlp_parser.parse(command, dry_run=dry_run)

        if verbose:
            print(f"Parsed {len(action_sequence)} action(s)")
            for i, action in enumerate(action_sequence.actions, 1):
                print(f"  {i}. {action}")

        # Validate sequence
        screen_size = executor.get_screen_size()
        is_valid, error = validate_action_sequence(action_sequence, screen_size)
        if not is_valid:
            print(f"Validation error: {error}", file=sys.stderr)
            return False

        # Execute
        executor.execute_sequence(action_sequence)
        return True

    except ValueError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Execution error: {e}", file=sys.stderr)
        return False


def run_interactive_mode(nlp_parser: NLPParser, executor, verbose: bool = False):
    """Run in interactive mode."""
    print("=== Mouceifi Interactive Mode ===")
    print("Enter mouse commands in natural language.")
    print("Type 'help' for examples, 'quit' or 'exit' to quit.\n")

    while True:
        try:
            command = input("mouceifi> ").strip()

            if not command:
                continue

            # Handle special commands
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if command.lower() == 'help':
                print_help()
                continue

            if command.lower() == 'status':
                screen_size = executor.get_screen_size()
                print(f"Screen size: {screen_size.x}x{screen_size.y}")
                if not executor.dry_run:
                    current_pos = executor.get_current_position()
                    print(f"Current position: ({current_pos.x}, {current_pos.y})")
                print(f"Dry run: {executor.dry_run}")
                continue

            if command.lower().startswith('dry-run '):
                # Toggle dry-run mode
                if command.lower() == 'dry-run on':
                    executor.dry_run = True
                    print("Dry-run mode enabled")
                elif command.lower() == 'dry-run off':
                    executor.dry_run = False
                    print("Dry-run mode disabled")
                continue

            # Execute command
            execute_command(command, nlp_parser, executor, verbose, executor.dry_run)

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
            continue
        except EOFError:
            print("\nGoodbye!")
            break


def print_help():
    """Print help message for interactive mode."""
    print("""
Available Commands:
  help              - Show this help message
  status            - Show current mouse position and screen size
  dry-run on/off    - Enable/disable dry-run mode
  quit, exit        - Exit interactive mode

Example Mouse Commands:
  move to x=500 y=300
  left click
  right click at current position
  move to x=100 y=100 and then left click
  move 100 pixels down and 50 pixels right then double click
  drag from x=100 y=100 to x=300 y=300
  scroll down by 5
    """)


if __name__ == '__main__':
    main()
