"""Operation executor for running validated FreeCAD operations."""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ExecutionResult:
    """Result of an operation execution."""

    def __init__(self, success: bool, message: str, data: Optional[Dict] = None, error: Optional[str] = None):
        """
        Initialize execution result.

        Args:
            success: Whether execution succeeded
            message: Human-readable message
            data: Optional result data
            error: Optional error message
        """
        self.success = success
        self.message = message
        self.data = data or {}
        self.error = error
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error,
            'timestamp': self.timestamp.isoformat()
        }


class OperationExecutor:
    """
    Executes validated FreeCAD operations safely.

    Handles execution timeouts, error recovery, and logging.
    """

    def __init__(self, file_parser, max_execution_time: float = 30.0):
        """
        Initialize the operation executor.

        Args:
            file_parser: FreeCADFileParser instance
            max_execution_time: Maximum execution time in seconds
        """
        self.file_parser = file_parser
        self.max_execution_time = max_execution_time
        self.execution_history: List[Dict[str, Any]] = []

    def execute_operations(
        self,
        validated_command: Dict[str, Any],
        dry_run: bool = False
    ) -> ExecutionResult:
        """
        Execute a validated command.

        Args:
            validated_command: Validated command from CommandTranslator
            dry_run: If True, don't actually execute, just validate

        Returns:
            ExecutionResult
        """
        if not validated_command.get('valid'):
            return ExecutionResult(
                success=False,
                message="Cannot execute invalid command",
                error="Command validation failed"
            )

        if not self.file_parser.is_loaded():
            return ExecutionResult(
                success=False,
                message="No FreeCAD document loaded",
                error="Document not loaded"
            )

        operations = validated_command.get('operations', [])
        if not operations:
            return ExecutionResult(
                success=False,
                message="No operations to execute",
                error="Empty operations list"
            )

        logger.info(f"Executing {len(operations)} operation(s), dry_run={dry_run}")

        if dry_run:
            return self._dry_run_execution(validated_command)

        # Execute operations
        start_time = time.time()
        results = []
        executed_count = 0

        try:
            for i, operation in enumerate(operations):
                # Check timeout
                elapsed = time.time() - start_time
                if elapsed > self.max_execution_time:
                    raise TimeoutError(
                        f"Execution timeout after {elapsed:.2f}s (max: {self.max_execution_time}s)"
                    )

                # Execute single operation
                op_result = self._execute_single_operation(operation, i + 1, len(operations))
                results.append(op_result)

                if op_result.success:
                    executed_count += 1
                else:
                    logger.warning(f"Operation {i + 1} failed: {op_result.error}")

            # Recompute document
            if executed_count > 0:
                self.file_parser.recompute()

            execution_time = time.time() - start_time

            # Log execution
            self._log_execution(validated_command, results, execution_time)

            # Determine overall success
            all_success = all(r.success for r in results)
            partial_success = executed_count > 0 and not all_success

            if all_success:
                message = f"Successfully executed {executed_count} operation(s) in {execution_time:.2f}s"
            elif partial_success:
                message = f"Partially executed {executed_count}/{len(operations)} operation(s) in {execution_time:.2f}s"
            else:
                message = f"Failed to execute operations"

            return ExecutionResult(
                success=all_success,
                message=message,
                data={
                    'executed_count': executed_count,
                    'total_count': len(operations),
                    'execution_time': execution_time,
                    'results': [r.to_dict() for r in results]
                }
            )

        except TimeoutError as e:
            logger.error(f"Execution timeout: {e}")
            return ExecutionResult(
                success=False,
                message=f"Execution timeout after {executed_count} operations",
                error=str(e),
                data={'executed_count': executed_count}
            )

        except Exception as e:
            logger.error(f"Execution error: {e}", exc_info=True)
            return ExecutionResult(
                success=False,
                message=f"Execution failed after {executed_count} operations",
                error=str(e),
                data={'executed_count': executed_count}
            )

    def _execute_single_operation(
        self,
        operation: Dict[str, Any],
        op_num: int,
        total_ops: int
    ) -> ExecutionResult:
        """
        Execute a single operation.

        Args:
            operation: Operation to execute
            op_num: Operation number (for logging)
            total_ops: Total number of operations

        Returns:
            ExecutionResult
        """
        code = operation['code']
        description = operation['description']

        logger.info(f"Executing operation {op_num}/{total_ops}: {description}")

        try:
            # Get the FreeCAD document
            doc = self.file_parser.document

            # Create execution namespace
            namespace = self._create_execution_namespace(doc)

            # Execute the code
            exec(code, namespace)

            # Extract created objects (simple heuristic)
            created_objects = []
            for name, obj in namespace.items():
                if not name.startswith('_') and name not in ['FreeCAD', 'Part', 'Arch', 'Draft']:
                    if hasattr(obj, 'Name'):  # Likely a FreeCAD object
                        created_objects.append(obj.Name)

            return ExecutionResult(
                success=True,
                message=f"Operation completed: {description}",
                data={
                    'description': description,
                    'type': operation['type'],
                    'created_objects': created_objects
                }
            )

        except Exception as e:
            logger.error(f"Operation failed: {e}", exc_info=True)
            return ExecutionResult(
                success=False,
                message=f"Operation failed: {description}",
                error=str(e),
                data={'description': description}
            )

    def _create_execution_namespace(self, document) -> Dict[str, Any]:
        """
        Create a safe execution namespace for code execution.

        Args:
            document: FreeCAD document

        Returns:
            Namespace dictionary
        """
        namespace = {
            '__builtins__': {
                # Only allow safe built-ins
                'True': True,
                'False': False,
                'None': None,
                'range': range,
                'len': len,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'min': min,
                'max': max,
                'round': round,
                'sum': sum,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
            }
        }

        # Add FreeCAD modules
        try:
            import FreeCAD
            namespace['FreeCAD'] = FreeCAD
            namespace['App'] = FreeCAD  # Alias

            # Set active document
            if document:
                FreeCAD.setActiveDocument(document.Name)
                namespace['doc'] = document
                namespace['ActiveDocument'] = document

        except ImportError:
            logger.warning("FreeCAD not available")

        # Add other FreeCAD modules if available
        for module_name in ['Part', 'Arch', 'Draft', 'Sketcher', 'PartDesign']:
            try:
                module = __import__(module_name)
                namespace[module_name] = module
            except ImportError:
                logger.debug(f"Module {module_name} not available")

        return namespace

    def _dry_run_execution(self, validated_command: Dict[str, Any]) -> ExecutionResult:
        """
        Perform a dry run (validation only, no execution).

        Args:
            validated_command: Validated command

        Returns:
            ExecutionResult
        """
        operations = validated_command.get('operations', [])

        summary = []
        for i, op in enumerate(operations, 1):
            summary.append(f"{i}. {op['description']} (type: {op['type']})")

        return ExecutionResult(
            success=True,
            message=f"Dry run: {len(operations)} operation(s) would be executed",
            data={
                'operations': summary,
                'estimated_complexity': validated_command.get('estimated_complexity', 0),
                'requires_confirmation': validated_command.get('requires_confirmation', False)
            }
        )

    def _log_execution(
        self,
        command: Dict[str, Any],
        results: List[ExecutionResult],
        execution_time: float
    ):
        """
        Log execution to history.

        Args:
            command: Validated command
            results: List of execution results
            execution_time: Total execution time
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operations_count': len(command.get('operations', [])),
            'execution_time': execution_time,
            'success_count': sum(1 for r in results if r.success),
            'failure_count': sum(1 for r in results if not r.success),
            'operations': [
                {
                    'description': op['description'],
                    'type': op['type'],
                    'success': results[i].success if i < len(results) else False
                }
                for i, op in enumerate(command.get('operations', []))
            ]
        }

        self.execution_history.append(log_entry)

        # Keep only last 100 entries
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent execution history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of execution log entries
        """
        return self.execution_history[-limit:]

    def clear_history(self):
        """Clear execution history."""
        self.execution_history = []
        logger.info("Execution history cleared")
