"""Usage examples for the FreeCAD LLM Framework."""

import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.file_parser import FreeCADFileParser
from core.llm_interface import LLMInterface, LLMProvider
from core.command_translator import CommandTranslator
from core.executor import OperationExecutor
from safety.rules import SafetyRules, SafetyMode, PermissionLevel
from safety.validator import SafetyValidator
from safety.rollback import RollbackManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class FreeCADLLMFramework:
    """Main framework class integrating all components."""

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.CLAUDE,
        safety_mode: SafetyMode = SafetyMode.STRICT,
        permission_level: PermissionLevel = PermissionLevel.MODIFY
    ):
        """
        Initialize the framework.

        Args:
            llm_provider: LLM provider to use
            safety_mode: Safety enforcement mode
            permission_level: Initial permission level
        """
        self.file_parser = FreeCADFileParser(headless=True)
        self.llm_interface = LLMInterface(provider=llm_provider)
        self.command_translator = CommandTranslator()
        self.executor = OperationExecutor(self.file_parser)

        self.safety_rules = SafetyRules(mode=safety_mode)
        self.safety_validator = SafetyValidator(
            self.safety_rules,
            self.file_parser,
            permission_level
        )
        self.rollback_manager = RollbackManager(self.file_parser)

        logger.info("FreeCAD LLM Framework initialized")

    def execute_command(
        self,
        natural_language_command: str,
        confirmed: bool = False,
        dry_run: bool = False
    ) -> dict:
        """
        Execute a natural language command.

        Args:
            natural_language_command: User's command in natural language
            confirmed: Whether user has confirmed execution
            dry_run: If True, validate but don't execute

        Returns:
            Result dictionary
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Command: {natural_language_command}")
        logger.info(f"{'='*60}")

        # Step 1: Translate natural language to FreeCAD API calls
        logger.info("Step 1: Translating command...")
        doc_context = self.file_parser.get_document_info()
        llm_response = self.llm_interface.translate_command(
            natural_language_command,
            context=doc_context
        )

        # Step 2: Validate and parse the LLM response
        logger.info("Step 2: Validating command structure...")
        validated_command = self.command_translator.validate_and_parse(llm_response)

        if not validated_command['valid']:
            logger.error("Command validation failed")
            return {
                'success': False,
                'error': 'Command validation failed',
                'details': validated_command['errors']
            }

        # Step 3: Check safety constraints
        logger.info("Step 3: Checking safety constraints...")

        # Create snapshot before execution (if not dry run)
        if not dry_run and self.file_parser.is_loaded():
            self.rollback_manager.create_snapshot(
                description=f"Before: {natural_language_command[:50]}"
            )

        safety_result = self.safety_validator.validate_command(
            validated_command,
            confirmed=confirmed
        )

        if not safety_result['safe']:
            logger.error("Safety validation failed")
            logger.error(self.safety_validator.get_violations_summary())
            return {
                'success': False,
                'error': 'Safety validation failed',
                'violations': safety_result['violations'],
                'warnings': safety_result.get('warnings', [])
            }

        # Step 4: Execute the operations
        logger.info("Step 4: Executing operations...")
        execution_result = self.executor.execute_operations(
            validated_command,
            dry_run=dry_run
        )

        return {
            'success': execution_result.success,
            'message': execution_result.message,
            'data': execution_result.data,
            'warnings': safety_result.get('warnings', [])
        }

    def load_file(self, file_path: str) -> bool:
        """Load a FreeCAD file."""
        return self.file_parser.load_file(file_path)

    def create_new_document(self, name: str = "Untitled") -> bool:
        """Create a new document."""
        return self.file_parser.create_new_document(name)

    def save_file(self, file_path: str = None) -> bool:
        """Save the current document."""
        return self.file_parser.save_file(file_path)

    def rollback(self) -> bool:
        """Rollback to previous state."""
        return self.rollback_manager.rollback_last_operation()


# Example 1: Create a simple wall
def example_1_create_wall():
    """Example 1: Create a rectangular wall."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Create a Wall")
    print("="*60)

    framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
    framework.create_new_document("Example1")

    result = framework.execute_command(
        "Create a wall 4 meters long, 3 meters high, 0.2 meters thick",
        dry_run=True  # Dry run for demonstration
    )

    print(f"\nResult: {result}")


# Example 2: Try to delete structural elements (should be blocked)
def example_2_blocked_operation():
    """Example 2: Attempt to delete structural elements (blocked by safety)."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Blocked Operation (Delete Walls)")
    print("="*60)

    framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
    framework.create_new_document("Example2")

    # First create a wall
    framework.execute_command(
        "Create a wall 4 meters long, 3 meters high, 0.2 meters thick",
        dry_run=True
    )

    # Try to delete it (should be blocked)
    result = framework.execute_command(
        "Delete all walls in the model",
        dry_run=True
    )

    print(f"\nResult: {result}")
    print("\nExpected: Operation should be blocked by safety validator")


# Example 3: Create a room with multiple elements
def example_3_complex_operation():
    """Example 3: Create a room with multiple elements."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Complex Operation (Room with Door and Window)")
    print("="*60)

    framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
    framework.create_new_document("Example3")

    result = framework.execute_command(
        "Create a room 5 meters by 4 meters with 3 meter high walls, "
        "add a door on one wall and a window on another wall",
        dry_run=True
    )

    print(f"\nResult: {result}")


# Example 4: Rollback operation
def example_4_rollback():
    """Example 4: Demonstrate rollback functionality."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Rollback Demonstration")
    print("="*60)

    framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
    framework.create_new_document("Example4")

    # Execute first command
    print("\nExecuting first command...")
    framework.execute_command(
        "Create a box 1000mm x 1000mm x 1000mm",
        dry_run=True
    )

    # Execute second command
    print("\nExecuting second command...")
    framework.execute_command(
        "Create a sphere with radius 500mm",
        dry_run=True
    )

    # Rollback
    print("\nPerforming rollback...")
    success = framework.rollback()
    print(f"Rollback successful: {success}")


# Example 5: Permission elevation
def example_5_permission_elevation():
    """Example 5: Demonstrate permission elevation for delete operations."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Permission Elevation")
    print("="*60)

    # Start with READ permission
    framework = FreeCADLLMFramework(
        llm_provider=LLMProvider.LOCAL,
        permission_level=PermissionLevel.READ
    )
    framework.create_new_document("Example5")

    # Try to create (should fail - need CREATE permission)
    print("\nAttempting to create with READ permission...")
    result = framework.execute_command(
        "Create a wall 4 meters long",
        dry_run=True
    )
    print(f"Result: {result}")

    # Elevate permission
    print("\nElevating permission to CREATE...")
    framework.safety_validator.elevate_permission(PermissionLevel.CREATE)

    # Try again
    print("\nAttempting to create with CREATE permission...")
    result = framework.execute_command(
        "Create a wall 4 meters long",
        dry_run=True
    )
    print(f"Result: {result}")


# Example 6: Using direct operations (without LLM)
def example_6_direct_operations():
    """Example 6: Use operations modules directly."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Direct Operations (No LLM)")
    print("="*60)

    from operations.basic_shapes import BasicShapeOperations
    from operations.bim_elements import BIMOperations
    from operations.properties import PropertyOperations

    framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
    framework.create_new_document("Example6")

    doc = framework.file_parser.document

    # Create operations helpers
    shapes = BasicShapeOperations(doc)
    bim = BIMOperations(doc)
    props = PropertyOperations(doc)

    # Create a wall using direct API
    print("\nCreating wall directly...")
    wall = bim.create_wall(
        length=4000,  # 4 meters in mm
        width=200,    # 200mm thick
        height=3000,  # 3 meters high
        position=(0, 0, 0),
        name="MyWall"
    )

    if wall:
        print(f"Wall created: {wall.Label}")

        # Set color
        props.set_color_rgb(wall, r=200, g=200, b=220)
        print("Color set to light gray")


def main():
    """Run all examples."""
    print("\n" + "#"*60)
    print("# FreeCAD LLM Framework - Usage Examples")
    print("#"*60)

    examples = [
        ("Create a Wall", example_1_create_wall),
        ("Blocked Operation", example_2_blocked_operation),
        ("Complex Operation", example_3_complex_operation),
        ("Rollback", example_4_rollback),
        ("Permission Elevation", example_5_permission_elevation),
        ("Direct Operations", example_6_direct_operations),
    ]

    for i, (name, example_func) in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            logger.error(f"Example {i} failed: {e}", exc_info=True)

    print("\n" + "#"*60)
    print("# Examples Complete")
    print("#"*60)


if __name__ == "__main__":
    main()
