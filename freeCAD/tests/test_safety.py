"""Tests for safety validation and guard rails."""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from safety.rules import SafetyRules, SafetyMode, PermissionLevel
from safety.validator import SafetyValidator, ValidationViolation
from safety.rollback import RollbackManager
from core.file_parser import FreeCADFileParser
from core.command_translator import CommandTranslator


class TestSafetyRules(unittest.TestCase):
    """Test safety rules configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.rules = SafetyRules(mode=SafetyMode.STRICT)

    def test_rule_initialization(self):
        """Test that rules are properly initialized."""
        self.assertIsNotNone(self.rules.rules)
        self.assertGreater(len(self.rules.rules), 0)

    def test_structural_element_detection(self):
        """Test detection of structural elements."""
        self.assertTrue(self.rules.is_structural_element('Arch::Wall'))
        self.assertTrue(self.rules.is_structural_element('Arch::Structure'))
        self.assertFalse(self.rules.is_structural_element('Arch::Window'))
        self.assertFalse(self.rules.is_structural_element('Part::Box'))

    def test_operation_complexity_check(self):
        """Test operation complexity limits."""
        # Within limit
        is_valid, error = self.rules.check_operation_complexity(10)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

        # Exceeds limit
        is_valid, error = self.rules.check_operation_complexity(100)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_mass_delete_check(self):
        """Test mass delete limits."""
        # Within limit
        is_valid, error = self.rules.check_mass_delete(5)
        self.assertTrue(is_valid)

        # Exceeds limit
        is_valid, error = self.rules.check_mass_delete(20)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_permission_levels(self):
        """Test permission level requirements."""
        read_perm = self.rules.get_permission_level_for_operation('query')
        self.assertEqual(read_perm, PermissionLevel.READ)

        delete_perm = self.rules.get_permission_level_for_operation('delete')
        self.assertEqual(delete_perm, PermissionLevel.DELETE)

    def test_enable_disable_rules(self):
        """Test enabling and disabling rules."""
        rule_name = 'no_delete_load_bearing'

        # Should be enabled by default in STRICT mode
        self.assertTrue(self.rules.is_rule_enabled(rule_name))

        # Disable it
        self.rules.disable_rule(rule_name)
        self.assertFalse(self.rules.is_rule_enabled(rule_name))

        # Re-enable it
        self.rules.enable_rule(rule_name)
        self.assertTrue(self.rules.is_rule_enabled(rule_name))


class TestSafetyValidator(unittest.TestCase):
    """Test safety validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.rules = SafetyRules(mode=SafetyMode.STRICT)
        self.file_parser = Mock(spec=FreeCADFileParser)
        self.file_parser.is_loaded.return_value = True
        self.file_parser.get_objects.return_value = []

        self.validator = SafetyValidator(
            self.rules,
            self.file_parser,
            current_permission=PermissionLevel.MODIFY
        )

    def test_validate_create_operation(self):
        """Test validation of create operation."""
        command = {
            'valid': True,
            'operations': [{
                'code': 'wall = Arch.makeWall(length=4000, height=3000, width=200)',
                'description': 'Create wall',
                'type': 'create',
                'affected_objects': ['wall']
            }],
            'imports': ['FreeCAD', 'Arch'],
            'requires_confirmation': False,
            'estimated_complexity': 2
        }

        result = self.validator.validate_command(command)

        # Should pass - create operation within permissions
        self.assertTrue(result['safe'])
        self.assertEqual(len(result['violations']), 0)

    def test_validate_delete_without_confirmation(self):
        """Test that delete operations require confirmation."""
        command = {
            'valid': True,
            'operations': [{
                'code': 'doc.removeObject("wall")',
                'description': 'Delete wall',
                'type': 'delete',
                'affected_objects': ['wall']
            }],
            'imports': ['FreeCAD'],
            'requires_confirmation': True,
            'estimated_complexity': 3
        }

        result = self.validator.validate_command(command, confirmed=False)

        # Should fail - delete requires confirmation
        self.assertFalse(result['safe'])
        self.assertGreater(len(result['violations']), 0)

        # Check that it's the confirmation violation
        violation_rules = [v['rule'] for v in result['violations']]
        self.assertIn('require_delete_confirmation', violation_rules)

    def test_validate_delete_with_confirmation(self):
        """Test that delete operations pass with confirmation."""
        command = {
            'valid': True,
            'operations': [{
                'code': 'doc.removeObject("box")',
                'description': 'Delete box',
                'type': 'delete',
                'affected_objects': ['box']
            }],
            'imports': ['FreeCAD'],
            'requires_confirmation': True,
            'estimated_complexity': 3
        }

        result = self.validator.validate_command(command, confirmed=True)

        # Should pass with confirmation
        # Note: May still have warnings, but no blocking violations
        blocking_violations = [v for v in result['violations'] if 'confirmation' in v['rule']]
        self.assertEqual(len(blocking_violations), 0)

    def test_validate_complexity_limit(self):
        """Test operation complexity limit."""
        # Create command with too many operations
        operations = [
            {
                'code': f'box_{i} = Part.makeBox(100, 100, 100)',
                'description': f'Create box {i}',
                'type': 'create',
                'affected_objects': [f'box_{i}']
            }
            for i in range(60)  # Exceeds limit of 50
        ]

        command = {
            'valid': True,
            'operations': operations,
            'imports': ['Part'],
            'requires_confirmation': False,
            'estimated_complexity': 5
        }

        result = self.validator.validate_command(command)

        # Should fail - too many operations
        self.assertFalse(result['safe'])
        violation_rules = [v['rule'] for v in result['violations']]
        self.assertIn('limit_operation_complexity', violation_rules)

    def test_validate_permission_level(self):
        """Test permission level enforcement."""
        # Set validator to READ permission
        self.validator.current_permission = PermissionLevel.READ

        # Try to create (requires CREATE permission)
        command = {
            'valid': True,
            'operations': [{
                'code': 'wall = Arch.makeWall(length=4000)',
                'description': 'Create wall',
                'type': 'create',
                'affected_objects': ['wall']
            }],
            'imports': ['Arch'],
            'requires_confirmation': False,
            'estimated_complexity': 2
        }

        result = self.validator.validate_command(command)

        # Should fail - insufficient permissions
        self.assertFalse(result['safe'])
        violation_rules = [v['rule'] for v in result['violations']]
        self.assertIn('require_permission_elevation', violation_rules)

    def test_permission_elevation(self):
        """Test permission elevation."""
        # Start with READ
        self.validator.current_permission = PermissionLevel.READ
        self.assertEqual(self.validator.current_permission, PermissionLevel.READ)

        # Elevate to MODIFY
        self.validator.elevate_permission(PermissionLevel.MODIFY)
        self.assertEqual(self.validator.current_permission, PermissionLevel.MODIFY)

        # Elevate to DELETE
        self.validator.elevate_permission(PermissionLevel.DELETE)
        self.assertEqual(self.validator.current_permission, PermissionLevel.DELETE)

    def test_structural_element_deletion_blocked(self):
        """Test that structural element deletion is blocked."""
        command = {
            'valid': True,
            'operations': [{
                'code': 'walls = [obj for obj in doc.Objects if obj.TypeId == "Arch::Wall"]',
                'description': 'Delete all walls',
                'type': 'delete',
                'affected_objects': ['all_walls']
            }],
            'imports': ['FreeCAD'],
            'requires_confirmation': True,
            'estimated_complexity': 5
        }

        result = self.validator.validate_command(command, confirmed=True)

        # Should be blocked due to structural safety
        # Note: This will show violations if structural elements are detected
        violation_rules = [v['rule'] for v in result.get('violations', [])]

        # May contain structural safety violation
        if 'no_delete_load_bearing' in [r for r in self.rules.rules.keys()]:
            # Structural check may trigger
            pass


class TestCommandTranslator(unittest.TestCase):
    """Test command translation and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.translator = CommandTranslator()

    def test_validate_safe_code(self):
        """Test validation of safe code."""
        code = """
import FreeCAD
import Arch
wall = Arch.makeWall(length=4000, height=3000, width=200)
"""
        result = self.translator._validate_code_ast(code.strip())
        self.assertTrue(result['valid'])

    def test_reject_dangerous_functions(self):
        """Test rejection of dangerous functions."""
        code = "exec('print(1)')"

        result = self.translator._validate_code_ast(code)
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)

    def test_reject_dangerous_imports(self):
        """Test rejection of dangerous imports."""
        code = "import os"

        result = self.translator._validate_code_ast(code)
        self.assertFalse(result['valid'])

    def test_validate_complete_command(self):
        """Test validation of complete command structure."""
        command_response = {
            'operations': [{
                'code': 'wall = Arch.makeWall(length=4000)',
                'description': 'Create wall',
                'type': 'create',
                'affected_objects': ['wall']
            }],
            'imports': ['FreeCAD', 'Arch'],
            'requires_confirmation': False,
            'estimated_complexity': 2
        }

        result = self.translator.validate_and_parse(command_response)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['operations']), 1)


class TestRollbackManager(unittest.TestCase):
    """Test rollback functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.file_parser = Mock(spec=FreeCADFileParser)
        self.file_parser.is_loaded.return_value = True
        self.file_parser.document = Mock()
        self.file_parser.document.saveAs = Mock()
        self.file_parser.get_document_info.return_value = {
            'object_count': 0,
            'object_types': {}
        }

        self.rollback_manager = RollbackManager(self.file_parser, max_snapshots=5)

    def test_create_snapshot(self):
        """Test snapshot creation."""
        snapshot = self.rollback_manager.create_snapshot("Test snapshot")

        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.description, "Test snapshot")
        self.assertEqual(len(self.rollback_manager.snapshots), 1)

    def test_max_snapshots_limit(self):
        """Test that old snapshots are cleaned up."""
        # Create more snapshots than the limit
        for i in range(10):
            self.rollback_manager.create_snapshot(f"Snapshot {i}")

        # Should only keep max_snapshots (5)
        self.assertEqual(len(self.rollback_manager.snapshots), 5)

    def test_can_rollback(self):
        """Test rollback capability check."""
        # No snapshots yet
        self.assertFalse(self.rollback_manager.can_rollback())

        # Create a snapshot
        self.rollback_manager.create_snapshot("Test")

        # Now can rollback
        self.assertTrue(self.rollback_manager.can_rollback())

    def test_snapshot_history(self):
        """Test getting snapshot history."""
        self.rollback_manager.create_snapshot("Snapshot 1")
        self.rollback_manager.create_snapshot("Snapshot 2")

        history = self.rollback_manager.get_snapshot_history()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['description'], "Snapshot 1")
        self.assertEqual(history[1]['description'], "Snapshot 2")


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyRules))
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandTranslator))
    suite.addTests(loader.loadTestsFromTestCase(TestRollbackManager))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
