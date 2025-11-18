"""Safety rules and permission definitions for FreeCAD operations."""

from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


class PermissionLevel(Enum):
    """Permission levels for operations."""
    READ = 1
    MODIFY = 2
    CREATE = 3
    DELETE = 4


class SafetyMode(Enum):
    """Safety enforcement modes."""
    STRICT = "strict"
    PERMISSIVE = "permissive"
    CUSTOM = "custom"


@dataclass
class SafetyRule:
    """Definition of a safety rule."""
    name: str
    description: str
    rule_type: str  # 'structural', 'data', 'operational', 'permission'
    severity: str  # 'error', 'warning', 'info'
    enabled: bool = True


class SafetyRules:
    """
    Defines and manages safety rules for FreeCAD operations.

    Implements four categories of safety:
    1. Structural Safety - Prevent breaking structural integrity
    2. Data Safety - Prevent data loss
    3. Operational Safety - Prevent resource exhaustion
    4. Permission Safety - Enforce access control
    """

    # Load-bearing element types (critical structural elements)
    STRUCTURAL_ELEMENT_TYPES = {
        'Arch::Wall',
        'Arch::Structure',  # Columns, beams, etc.
        'Arch::Floor',
        'Arch::Building',
        'Arch::Foundation',
        'Arch::Rebar',
    }

    # Non-structural BIM elements
    NON_STRUCTURAL_ELEMENT_TYPES = {
        'Arch::Window',
        'Arch::Door',
        'Arch::Roof',
        'Arch::Stairs',
        'Arch::Space',
        'Arch::Equipment',
        'Arch::Furniture',
    }

    # Maximum limits
    MAX_OPERATIONS_PER_BATCH = 50
    MAX_EXECUTION_TIME_SECONDS = 30.0
    MAX_DELETE_OBJECTS = 10  # Require confirmation for mass deletion

    def __init__(self, mode: SafetyMode = SafetyMode.STRICT):
        """
        Initialize safety rules.

        Args:
            mode: Safety enforcement mode
        """
        self.mode = mode
        self.rules = self._initialize_rules()
        self.custom_rules: List[SafetyRule] = []

    def _initialize_rules(self) -> Dict[str, SafetyRule]:
        """Initialize default safety rules."""
        return {
            # Structural Safety Rules
            'no_delete_load_bearing': SafetyRule(
                name='no_delete_load_bearing',
                description='Prevent deletion of load-bearing structural elements',
                rule_type='structural',
                severity='error',
                enabled=True
            ),
            'no_break_dependencies': SafetyRule(
                name='no_break_dependencies',
                description='Prevent breaking parent-child dependencies',
                rule_type='structural',
                severity='error',
                enabled=True
            ),
            'no_floating_objects': SafetyRule(
                name='no_floating_objects',
                description='Prevent creating objects with no structural support',
                rule_type='structural',
                severity='warning',
                enabled=self.mode == SafetyMode.STRICT
            ),

            # Data Safety Rules
            'require_delete_confirmation': SafetyRule(
                name='require_delete_confirmation',
                description='Require explicit confirmation for delete operations',
                rule_type='data',
                severity='error',
                enabled=True
            ),
            'maintain_version_history': SafetyRule(
                name='maintain_version_history',
                description='Maintain operation history for rollback',
                rule_type='data',
                severity='warning',
                enabled=True
            ),
            'validate_file_integrity': SafetyRule(
                name='validate_file_integrity',
                description='Validate file integrity before/after operations',
                rule_type='data',
                severity='error',
                enabled=True
            ),
            'no_mass_delete': SafetyRule(
                name='no_mass_delete',
                description=f'Block deletion of more than {self.MAX_DELETE_OBJECTS} objects',
                rule_type='data',
                severity='error',
                enabled=True
            ),

            # Operational Safety Rules
            'limit_operation_complexity': SafetyRule(
                name='limit_operation_complexity',
                description=f'Limit to {self.MAX_OPERATIONS_PER_BATCH} operations per batch',
                rule_type='operational',
                severity='error',
                enabled=True
            ),
            'timeout_protection': SafetyRule(
                name='timeout_protection',
                description=f'Maximum execution time: {self.MAX_EXECUTION_TIME_SECONDS}s',
                rule_type='operational',
                severity='error',
                enabled=True
            ),
            'rollback_capability': SafetyRule(
                name='rollback_capability',
                description='Ensure all operations can be rolled back',
                rule_type='operational',
                severity='error',
                enabled=True
            ),

            # Permission Rules
            'require_permission_elevation': SafetyRule(
                name='require_permission_elevation',
                description='Require explicit permission for destructive operations',
                rule_type='permission',
                severity='error',
                enabled=True
            ),
            'audit_all_operations': SafetyRule(
                name='audit_all_operations',
                description='Log all operations for audit trail',
                rule_type='permission',
                severity='warning',
                enabled=True
            ),
        }

    def get_rule(self, rule_name: str) -> Optional[SafetyRule]:
        """Get a rule by name."""
        return self.rules.get(rule_name) or next(
            (r for r in self.custom_rules if r.name == rule_name),
            None
        )

    def is_rule_enabled(self, rule_name: str) -> bool:
        """Check if a rule is enabled."""
        rule = self.get_rule(rule_name)
        return rule.enabled if rule else False

    def enable_rule(self, rule_name: str):
        """Enable a rule."""
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = True

    def disable_rule(self, rule_name: str):
        """Disable a rule."""
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = False

    def add_custom_rule(self, rule: SafetyRule):
        """Add a custom safety rule."""
        self.custom_rules.append(rule)

    def get_rules_by_type(self, rule_type: str) -> List[SafetyRule]:
        """Get all rules of a specific type."""
        all_rules = list(self.rules.values()) + self.custom_rules
        return [r for r in all_rules if r.rule_type == rule_type and r.enabled]

    def get_enabled_rules(self) -> List[SafetyRule]:
        """Get all enabled rules."""
        all_rules = list(self.rules.values()) + self.custom_rules
        return [r for r in all_rules if r.enabled]

    def is_structural_element(self, type_id: str) -> bool:
        """Check if an object type is a structural element."""
        return type_id in self.STRUCTURAL_ELEMENT_TYPES

    def is_load_bearing(self, obj) -> bool:
        """
        Check if an object is load-bearing.

        Args:
            obj: FreeCAD object

        Returns:
            True if object is load-bearing
        """
        if not hasattr(obj, 'TypeId'):
            return False

        # Check if it's a structural element type
        if obj.TypeId in self.STRUCTURAL_ELEMENT_TYPES:
            return True

        # Additional heuristics for load-bearing elements
        # Check if it has structural role
        if hasattr(obj, 'IfcRole') and obj.IfcRole in ['STRUCTURAL', 'COLUMN', 'BEAM', 'LOADBEARING']:
            return True

        # Check name patterns (common naming conventions)
        if hasattr(obj, 'Name'):
            name_lower = obj.Name.lower()
            if any(keyword in name_lower for keyword in ['column', 'beam', 'foundation', 'structural']):
                return True

        return False

    def get_permission_level_for_operation(self, operation_type: str) -> PermissionLevel:
        """
        Get required permission level for an operation type.

        Args:
            operation_type: Type of operation (create, modify, delete, query)

        Returns:
            Required permission level
        """
        permission_map = {
            'query': PermissionLevel.READ,
            'modify': PermissionLevel.MODIFY,
            'create': PermissionLevel.CREATE,
            'delete': PermissionLevel.DELETE,
        }

        return permission_map.get(operation_type, PermissionLevel.READ)

    def check_operation_complexity(self, num_operations: int) -> tuple[bool, Optional[str]]:
        """
        Check if operation count is within limits.

        Args:
            num_operations: Number of operations

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.is_rule_enabled('limit_operation_complexity'):
            return True, None

        if num_operations > self.MAX_OPERATIONS_PER_BATCH:
            return False, f"Too many operations: {num_operations} (max: {self.MAX_OPERATIONS_PER_BATCH})"

        return True, None

    def check_mass_delete(self, num_objects: int) -> tuple[bool, Optional[str]]:
        """
        Check if delete operation affects too many objects.

        Args:
            num_objects: Number of objects to delete

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.is_rule_enabled('no_mass_delete'):
            return True, None

        if num_objects > self.MAX_DELETE_OBJECTS:
            return False, f"Mass delete blocked: {num_objects} objects (max: {self.MAX_DELETE_OBJECTS}). Use explicit confirmation flag."

        return True, None

    def to_dict(self) -> Dict:
        """Export rules configuration to dictionary."""
        return {
            'mode': self.mode.value,
            'rules': {
                name: {
                    'description': rule.description,
                    'type': rule.rule_type,
                    'severity': rule.severity,
                    'enabled': rule.enabled
                }
                for name, rule in self.rules.items()
            },
            'custom_rules': [
                {
                    'name': rule.name,
                    'description': rule.description,
                    'type': rule.rule_type,
                    'severity': rule.severity,
                    'enabled': rule.enabled
                }
                for rule in self.custom_rules
            ],
            'limits': {
                'max_operations_per_batch': self.MAX_OPERATIONS_PER_BATCH,
                'max_execution_time_seconds': self.MAX_EXECUTION_TIME_SECONDS,
                'max_delete_objects': self.MAX_DELETE_OBJECTS
            }
        }
