#!/usr/bin/env python3
"""
Comprehensive test runner for Mouceifi.

Runs all tests that don't require PyAutoGUI or other optional dependencies.
This allows testing the core parser and architecture without installing
platform-specific mouse control libraries.
"""

import sys
import unittest
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests(verbosity=2):
    """Run all available tests."""

    print("=" * 70)
    print("MOUCEIFI TEST SUITE")
    print("=" * 70)
    print()

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add parser tests (no dependencies required)
    print("Loading parser tests...")
    try:
        from tests import test_parser
        parser_tests = loader.loadTestsFromModule(test_parser)
        suite.addTests(parser_tests)
        print(f"✓ Loaded {parser_tests.countTestCases()} parser tests")
    except Exception as e:
        print(f"✗ Failed to load parser tests: {e}")
        return False

    # Try to add executor tests (requires PyAutoGUI)
    print("Loading executor tests...")
    try:
        from tests import test_executor
        executor_tests = loader.loadTestsFromModule(test_executor)
        suite.addTests(executor_tests)
        print(f"✓ Loaded {executor_tests.countTestCases()} executor tests")
    except ImportError as e:
        print(f"⚠ Skipping executor tests (PyAutoGUI not installed): {e}")
        print("  Install with: pip install -r requirements.txt")
    except Exception as e:
        print(f"✗ Failed to load executor tests: {e}")

    print()
    print("-" * 70)
    print(f"Running {suite.countTestCases()} tests...")
    print("-" * 70)
    print()

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    # Parse arguments
    verbosity = 2
    if '-v' in sys.argv or '--verbose' in sys.argv:
        verbosity = 2
    elif '-q' in sys.argv or '--quiet' in sys.argv:
        verbosity = 0

    success = run_tests(verbosity)
    sys.exit(0 if success else 1)
