"""Safety validator for enforcing guard rails on FreeCAD operations."""

import ast
import logging
from typing import Dict, List, Any, Optional, Set
from .rules import SafetyRules, PermissionLevel

logger = logging.getLogger(__name__)


class ValidationViolation:
    """Represents a safety rule violation."""

    def __init__(self, rule_name: str, severity: str, message: str, blocked: bool = True):
        """
        Initialize a validation violation.

        Args:
            rule_name: Name of the violated rule
            severity: Severity level (error, warning, info)
            message: Human-readable message
            blocked: Whether this violation blocks execution
        """
        self.rule_name = rule_name
        self.severity = severity
        self.message = message
        self.blocked = blocked

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'rule': self.rule_name,
            'severity': self.severity,
            'message': self.message,
            'blocked': self.blocked
        }


class SafetyValidator:
    """
    Validates operations against safety rules before execution.

    Enforces guard rails across structural, data, operational,
    and permission safety categories.
    """

    def __init__(
        self,
        safety_rules: SafetyRules,
        file_parser,
        current_permission: PermissionLevel = PermissionLevel.MODIFY
    ):
        """
        Initialize the safety validator.

        Args:
            safety_rules: SafetyRules instance
            file_parser: FreeCADFileParser instance
            current_permission: Current permission level
        """
        self.rules = safety_rules
        self.file_parser = file_parser
        self.current_permission = current_permission
        self.violations: List[ValidationViolation] = []

    def validate_command(
        self,
        validated_command: Dict[str, Any],
        confirmed: bool = False
    ) -> Dict[str, Any]:
        """
        Validate a command against all safety rules.

        Args:
            validated_command: Validated command from CommandTranslator
            confirmed: Whether user has explicitly confirmed execution

        Returns:
            Validation result
        """
        self.violations = []

        if not validated_command.get('valid'):
            return {
                'safe': False,
                'violations': [
                    ValidationViolation(
                        'invalid_command',
                        'error',
                        'Command is not valid',
                        blocked=True
                    ).to_dict()
                ]
            }

        operations = validated_command.get('operations', [])

        # Check operational safety - complexity
        self._check_operation_complexity(operations)

        # Check permission level
        self._check_permissions(operations)

        # Check data safety
        self._check_data_safety(operations, confirmed)

        # Check structural safety (requires document analysis)
        if self.file_parser.is_loaded():
            self._check_structural_safety(operations)

        # Determine if command is safe to execute
        blocking_violations = [v for v in self.violations if v.blocked]
        warnings = [v for v in self.violations if not v.blocked]

        is_safe = len(blocking_violations) == 0

        return {
            'safe': is_safe,
            'violations': [v.to_dict() for v in blocking_violations],
            'warnings': [v.to_dict() for v in warnings],
            'requires_confirmation': validated_command.get('requires_confirmation', False) and not confirmed
        }

    def _check_operation_complexity(self, operations: List[Dict[str, Any]]):
        """Check operation complexity constraints."""
        if not self.rules.is_rule_enabled('limit_operation_complexity'):
            return

        is_valid, error_msg = self.rules.check_operation_complexity(len(operations))
        if not is_valid:
            self.violations.append(
                ValidationViolation(
                    'limit_operation_complexity',
                    'error',
                    error_msg,
                    blocked=True
                )
            )

    def _check_permissions(self, operations: List[Dict[str, Any]]):
        """Check permission requirements for operations."""
        if not self.rules.is_rule_enabled('require_permission_elevation'):
            return

        for op in operations:
            op_type = op.get('type', 'query')
            required_permission = self.rules.get_permission_level_for_operation(op_type)

            if required_permission.value > self.current_permission.value:
                self.violations.append(
                    ValidationViolation(
                        'require_permission_elevation',
                        'error',
                        f"Operation '{op['description']}' requires {required_permission.name} permission, "
                        f"but current level is {self.current_permission.name}",
                        blocked=True
                    )
                )

    def _check_data_safety(self, operations: List[Dict[str, Any]], confirmed: bool):
        """Check data safety constraints."""
        delete_ops = [op for op in operations if op.get('type') == 'delete']

        if not delete_ops:
            return

        # Check if delete requires confirmation
        if self.rules.is_rule_enabled('require_delete_confirmation'):
            if not confirmed:
                self.violations.append(
                    ValidationViolation(
                        'require_delete_confirmation',
                        'error',
                        f"{len(delete_ops)} delete operation(s) require explicit confirmation. "
                        "Set confirmed=True to proceed.",
                        blocked=True
                    )
                )

        # Check for mass delete
        total_affected = sum(
            len(op.get('affected_objects', [])) for op in delete_ops
        )

        if total_affected > 0:
            is_valid, error_msg = self.rules.check_mass_delete(total_affected)
            if not is_valid and not confirmed:
                self.violations.append(
                    ValidationViolation(
                        'no_mass_delete',
                        'error',
                        error_msg,
                        blocked=True
                    )
                )

    def _check_structural_safety(self, operations: List[Dict[str, Any]]):
        """Check structural safety constraints."""
        if not self.file_parser.is_loaded():
            return

        # Check for deletion of load-bearing elements
        if self.rules.is_rule_enabled('no_delete_load_bearing'):
            self._check_load_bearing_deletion(operations)

        # Check for breaking dependencies
        if self.rules.is_rule_enabled('no_break_dependencies'):
            self._check_dependency_violations(operations)

    def _check_load_bearing_deletion(self, operations: List[Dict[str, Any]]):
        """Check for deletion of load-bearing structural elements."""
        delete_ops = [op for op in operations if op.get('type') == 'delete']

        for op in delete_ops:
            # Analyze code to find what's being deleted
            affected_objects = self._analyze_delete_operation(op)

            for obj_identifier in affected_objects:
                # Check if it's deleting structural elements
                if self._is_deleting_structural_elements(op['code']):
                    self.violations.append(
                        ValidationViolation(
                            'no_delete_load_bearing',
                            'error',
                            f"Operation attempts to delete load-bearing structural elements. "
                            f"This is blocked for safety. Description: {op['description']}",
                            blocked=True
                        )
                    )
                    break

    def _is_deleting_structural_elements(self, code: str) -> bool:
        """
        Check if code deletes structural elements.

        Args:
            code: Python code to analyze

        Returns:
            True if code deletes structural elements
        """
        # Simple heuristic: check if code filters for structural types
        for struct_type in self.rules.STRUCTURAL_ELEMENT_TYPES:
            if struct_type in code:
                return True

        # Check for keywords
        structural_keywords = ['wall', 'column', 'beam', 'foundation', 'structural']
        code_lower = code.lower()

        if 'removeobject' in code_lower or 'delete' in code_lower:
            if any(keyword in code_lower for keyword in structural_keywords):
                return True

        return False

    def _analyze_delete_operation(self, operation: Dict[str, Any]) -> List[str]:
        """
        Analyze a delete operation to determine what's being deleted.

        Args:
            operation: Delete operation

        Returns:
            List of object identifiers being deleted
        """
        code = operation['code']
        affected = operation.get('affected_objects', [])

        # If affected_objects is specified, use that
        if affected and affected != ['all_walls']:
            return affected

        # Otherwise, try to parse from code
        identifiers = []

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        if node.func.attr in ['removeObject', 'delete']:
                            # Extract object name if possible
                            if node.args:
                                arg = node.args[0]
                                if isinstance(arg, ast.Str):
                                    identifiers.append(arg.s)
                                elif isinstance(arg, ast.Constant):
                                    identifiers.append(str(arg.value))
        except:
            pass

        return identifiers or ['unknown']

    def _check_dependency_violations(self, operations: List[Dict[str, Any]]):
        """Check for operations that would break dependencies."""
        # This is a simplified check
        # In a full implementation, we would analyze the dependency graph

        delete_ops = [op for op in operations if op.get('type') == 'delete']

        if not delete_ops:
            return

        # Get all objects in the document
        try:
            objects = self.file_parser.get_objects()

            # Build a simple dependency map
            dependencies = {}
            for obj in objects:
                if hasattr(obj, 'OutList'):
                    # Objects this one depends on
                    deps = [o.Name for o in obj.OutList if hasattr(o, 'Name')]
                    if deps:
                        dependencies[obj.Name] = deps

            # Check if any delete operation would break dependencies
            for op in delete_ops:
                affected = self._analyze_delete_operation(op)

                for obj_name in affected:
                    # Check if other objects depend on this one
                    dependents = [
                        name for name, deps in dependencies.items()
                        if obj_name in deps
                    ]

                    if dependents:
                        self.violations.append(
                            ValidationViolation(
                                'no_break_dependencies',
                                'warning',
                                f"Deleting '{obj_name}' may break dependencies. "
                                f"Objects that depend on it: {', '.join(dependents[:5])}",
                                blocked=False  # Warning, not error
                            )
                        )

        except Exception as e:
            logger.warning(f"Error checking dependencies: {e}")

    def elevate_permission(self, new_permission: PermissionLevel):
        """
        Elevate the current permission level.

        Args:
            new_permission: New permission level
        """
        if new_permission.value > self.current_permission.value:
            logger.info(f"Permission elevated: {self.current_permission.name} -> {new_permission.name}")
            self.current_permission = new_permission
        else:
            logger.warning(f"Cannot lower permission level")

    def get_violations_summary(self) -> str:
        """
        Get a human-readable summary of violations.

        Returns:
            Summary string
        """
        if not self.violations:
            return "No safety violations"

        blocking = [v for v in self.violations if v.blocked]
        warnings = [v for v in self.violations if not v.blocked]

        summary = []

        if blocking:
            summary.append(f"BLOCKING VIOLATIONS ({len(blocking)}):")
            for v in blocking:
                summary.append(f"  - [{v.severity.upper()}] {v.message}")

        if warnings:
            summary.append(f"\nWARNINGS ({len(warnings)}):")
            for v in warnings:
                summary.append(f"  - [{v.severity.upper()}] {v.message}")

        return "\n".join(summary)
