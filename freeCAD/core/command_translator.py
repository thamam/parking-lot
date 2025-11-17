"""Command translator for converting and validating LLM-generated code."""

import ast
import logging
from typing import Dict, List, Any, Optional, Set

logger = logging.getLogger(__name__)


class CommandTranslator:
    """
    Validates and translates LLM-generated commands into safe, executable code.

    Performs AST-based validation to ensure code safety before execution.
    """

    # Allowed FreeCAD modules and functions
    ALLOWED_MODULES = {
        'FreeCAD', 'Part', 'Arch', 'Draft', 'Sketcher', 'PartDesign',
        'Mesh', 'MeshPart', 'Drawing', 'Spreadsheet'
    }

    # Dangerous functions that should never be allowed
    FORBIDDEN_FUNCTIONS = {
        'eval', 'exec', 'compile', '__import__', 'open', 'input',
        'file', 'execfile', 'reload', 'globals', 'locals', 'vars',
        'dir', 'help', 'quit', 'exit', 'copyright', 'credits', 'license'
    }

    # Dangerous modules
    FORBIDDEN_MODULES = {
        'os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib',
        'pickle', 'shelve', 'marshal', 'imp', 'importlib'
    }

    def __init__(self):
        """Initialize the command translator."""
        self.validation_errors: List[str] = []

    def validate_and_parse(self, command_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and parse an LLM command response.

        Args:
            command_response: Response from LLM interface

        Returns:
            Validated and parsed command structure
        """
        self.validation_errors = []

        # Check for errors in the response
        if 'error' in command_response:
            return {
                'valid': False,
                'errors': [command_response['error']],
                'operations': []
            }

        # Validate structure
        if not self._validate_structure(command_response):
            return {
                'valid': False,
                'errors': self.validation_errors,
                'operations': []
            }

        # Validate each operation
        validated_operations = []
        for op in command_response.get('operations', []):
            validated_op = self._validate_operation(op)
            if validated_op['valid']:
                validated_operations.append(validated_op)
            else:
                self.validation_errors.extend(validated_op['errors'])

        # Check if any operations are valid
        if not validated_operations and command_response.get('operations'):
            return {
                'valid': False,
                'errors': self.validation_errors or ['No valid operations found'],
                'operations': []
            }

        return {
            'valid': True,
            'operations': validated_operations,
            'imports': command_response.get('imports', []),
            'requires_confirmation': command_response.get('requires_confirmation', False),
            'estimated_complexity': command_response.get('estimated_complexity', 0)
        }

    def _validate_structure(self, response: Dict[str, Any]) -> bool:
        """Validate the overall structure of the response."""
        required_fields = ['operations', 'imports']

        for field in required_fields:
            if field not in response:
                self.validation_errors.append(f"Missing required field: {field}")
                return False

        if not isinstance(response['operations'], list):
            self.validation_errors.append("'operations' must be a list")
            return False

        if not isinstance(response['imports'], list):
            self.validation_errors.append("'imports' must be a list")
            return False

        return True

    def _validate_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single operation.

        Args:
            operation: Operation dictionary

        Returns:
            Validation result with parsed operation
        """
        errors = []

        # Check required fields
        required_fields = ['code', 'description', 'type', 'affected_objects']
        for field in required_fields:
            if field not in operation:
                errors.append(f"Operation missing required field: {field}")

        if errors:
            return {'valid': False, 'errors': errors}

        # Validate code using AST
        code = operation['code']
        ast_validation = self._validate_code_ast(code)

        if not ast_validation['valid']:
            return {
                'valid': False,
                'errors': ast_validation['errors']
            }

        # Check operation type
        valid_types = ['create', 'modify', 'delete', 'query']
        if operation['type'] not in valid_types:
            errors.append(f"Invalid operation type: {operation['type']}")

        if errors:
            return {'valid': False, 'errors': errors}

        return {
            'valid': True,
            'code': code,
            'description': operation['description'],
            'type': operation['type'],
            'affected_objects': operation['affected_objects'],
            'ast_tree': ast_validation['ast_tree']
        }

    def _validate_code_ast(self, code: str) -> Dict[str, Any]:
        """
        Validate code using Abstract Syntax Tree parsing.

        Args:
            code: Python code to validate

        Returns:
            Validation result
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                'valid': False,
                'errors': [f"Syntax error in code: {e}"]
            }

        # Analyze the AST for security issues
        errors = []
        warnings = []

        for node in ast.walk(tree):
            # Check for forbidden function calls
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node)
                if func_name in self.FORBIDDEN_FUNCTIONS:
                    errors.append(f"Forbidden function call: {func_name}")

            # Check for imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.FORBIDDEN_MODULES:
                        errors.append(f"Forbidden module import: {alias.name}")
                    elif alias.name not in self.ALLOWED_MODULES:
                        warnings.append(f"Unrecognized module: {alias.name}")

            elif isinstance(node, ast.ImportFrom):
                if node.module in self.FORBIDDEN_MODULES:
                    errors.append(f"Forbidden module import: {node.module}")
                elif node.module and node.module not in self.ALLOWED_MODULES:
                    warnings.append(f"Unrecognized module: {node.module}")

            # Check for attribute access to dangerous methods
            elif isinstance(node, ast.Attribute):
                if node.attr.startswith('__') and node.attr.endswith('__'):
                    warnings.append(f"Access to dunder method: {node.attr}")

        if errors:
            return {'valid': False, 'errors': errors}

        if warnings:
            logger.warning(f"Code validation warnings: {warnings}")

        return {
            'valid': True,
            'ast_tree': tree,
            'warnings': warnings
        }

    def _get_function_name(self, call_node: ast.Call) -> Optional[str]:
        """
        Extract function name from a Call node.

        Args:
            call_node: AST Call node

        Returns:
            Function name or None
        """
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return None

    def extract_required_imports(self, operations: List[Dict[str, Any]]) -> Set[str]:
        """
        Extract required imports from a list of operations.

        Args:
            operations: List of validated operations

        Returns:
            Set of required module names
        """
        imports = set()

        for op in operations:
            if 'ast_tree' not in op:
                continue

            tree = op['ast_tree']
            for node in ast.walk(tree):
                # Check for Name nodes (module references)
                if isinstance(node, ast.Name):
                    if node.id in self.ALLOWED_MODULES:
                        imports.add(node.id)

                # Check for Attribute nodes (module.function)
                elif isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        if node.value.id in self.ALLOWED_MODULES:
                            imports.add(node.value.id)

        return imports

    def generate_import_statements(self, modules: Set[str]) -> str:
        """
        Generate import statements for required modules.

        Args:
            modules: Set of module names

        Returns:
            Import statements as a string
        """
        import_lines = []

        for module in sorted(modules):
            if module in self.ALLOWED_MODULES:
                import_lines.append(f"import {module}")

        return '\n'.join(import_lines)

    def prepare_executable_code(self, validated_command: Dict[str, Any]) -> str:
        """
        Prepare complete executable code from validated command.

        Args:
            validated_command: Validated command structure

        Returns:
            Complete Python code ready for execution
        """
        if not validated_command.get('valid'):
            raise ValueError("Cannot prepare code from invalid command")

        operations = validated_command.get('operations', [])
        if not operations:
            return ""

        # Extract required imports
        imports = self.extract_required_imports(operations)

        # Generate import statements
        import_code = self.generate_import_statements(imports)

        # Combine all operation code
        operation_code = []
        for op in operations:
            operation_code.append(f"# {op['description']}")
            operation_code.append(op['code'])
            operation_code.append("")  # Blank line

        # Combine everything
        full_code = import_code + "\n\n" + "\n".join(operation_code)

        return full_code.strip()

    def estimate_execution_time(self, validated_command: Dict[str, Any]) -> float:
        """
        Estimate execution time for a command.

        Args:
            validated_command: Validated command

        Returns:
            Estimated time in seconds
        """
        complexity = validated_command.get('estimated_complexity', 1)
        num_operations = len(validated_command.get('operations', []))

        # Simple heuristic: ~0.5 seconds per complexity point per operation
        estimated_time = complexity * num_operations * 0.5

        return min(estimated_time, 30.0)  # Cap at 30 seconds
