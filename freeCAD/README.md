# FreeCAD LLM Framework

A production-ready Python framework that enables LLM-based manipulation of FreeCAD files with comprehensive safety constraints.

## Overview

This framework provides a secure interface for manipulating FreeCAD 3D models using natural language commands. It integrates with Large Language Models (Claude, GPT-4) to translate natural language into FreeCAD Python API calls, while enforcing strict safety guard rails to prevent destructive or dangerous operations.

## Features

### Core Capabilities
- **Natural Language Interface**: Execute FreeCAD operations using plain English commands
- **LLM Integration**: Support for Claude (Anthropic) and GPT-4 (OpenAI)
- **Safe Code Execution**: AST-based validation prevents execution of dangerous code
- **Comprehensive Logging**: Full audit trail of all operations

### Safety Guard Rails

#### 1. Structural Safety
- Prevents deletion of load-bearing elements (walls, columns, beams)
- Validates structural integrity constraints
- Blocks operations that break parent-child dependencies

#### 2. Data Safety
- Requires explicit confirmation for delete operations
- Maintains version history with rollback capability
- Validates file integrity before/after operations
- Blocks mass deletion (>10 objects) without confirmation

#### 3. Operational Safety
- Limits operation complexity (max 50 operations per batch)
- Timeout protection (max 30 seconds per operation)
- Rollback capability for failed operations

#### 4. Permission System
- Four permission levels: READ, MODIFY, CREATE, DELETE
- Requires explicit permission elevation for destructive operations
- Audit trail for all operations

## Installation

### Prerequisites
- Python 3.9 or higher
- FreeCAD 0.20 or higher
- (Optional) API keys for Claude or GPT-4

### Install Dependencies

```bash
pip install requests
```

### Configuration

Set environment variables for LLM API access:

```bash
# For Claude (Anthropic)
export ANTHROPIC_API_KEY="your-api-key-here"

# For GPT-4 (OpenAI)
export OPENAI_API_KEY="your-api-key-here"
```

## Quick Start

### Example 1: Basic Usage

```python
from examples.usage_examples import FreeCADLLMFramework
from core.llm_interface import LLMProvider

# Initialize framework
framework = FreeCADLLMFramework(llm_provider=LLMProvider.CLAUDE)

# Create a new document
framework.create_new_document("MyProject")

# Execute a natural language command
result = framework.execute_command(
    "Create a wall 4 meters long, 3 meters high, 0.2 meters thick"
)

print(result)
# Output: {'success': True, 'message': 'Successfully executed 1 operation(s)...'}

# Save the file
framework.save_file("/path/to/output.FCStd")
```

### Example 2: Safe Operation (Blocked)

```python
# Try to delete structural elements (will be blocked)
result = framework.execute_command(
    "Delete all walls in the model",
    confirmed=False  # Safety requires confirmation
)

print(result)
# Output: {
#   'success': False,
#   'error': 'Safety validation failed',
#   'violations': [
#     'Delete operations require explicit confirmation',
#     'Attempting to delete load-bearing structural elements'
#   ]
# }
```

### Example 3: Rollback

```python
# Execute an operation
framework.execute_command("Create a box 1000mm x 1000mm x 1000mm")

# Execute another operation
framework.execute_command("Create a sphere with radius 500mm")

# Rollback to previous state
framework.rollback()
```

## Framework Architecture

```
freeCAD/
├── core/                    # Core framework modules
│   ├── file_parser.py       # Load/parse FCStd files
│   ├── llm_interface.py     # LLM communication
│   ├── command_translator.py # NL → API conversion
│   └── executor.py          # Operation execution
├── safety/                  # Safety enforcement
│   ├── rules.py             # Safety rule definitions
│   ├── validator.py         # Guard rail enforcement
│   └── rollback.py          # Undo mechanism
├── operations/              # High-level operations
│   ├── basic_shapes.py      # Create/modify shapes
│   ├── bim_elements.py      # BIM-specific operations
│   └── properties.py        # Property modifications
├── examples/                # Usage examples
│   └── usage_examples.py    # Demonstration scripts
└── tests/                   # Test suite
    └── test_safety.py       # Guard rail tests
```

## API Documentation

### FreeCADLLMFramework

Main framework class integrating all components.

```python
framework = FreeCADLLMFramework(
    llm_provider=LLMProvider.CLAUDE,  # or LLMProvider.GPT4, LLMProvider.LOCAL
    safety_mode=SafetyMode.STRICT,     # or SafetyMode.PERMISSIVE
    permission_level=PermissionLevel.MODIFY
)
```

#### Methods

**execute_command(command, confirmed=False, dry_run=False)**

Execute a natural language command.

- `command` (str): Natural language command
- `confirmed` (bool): Whether user has confirmed execution
- `dry_run` (bool): If True, validate but don't execute
- Returns: Dict with execution result

**load_file(file_path)**

Load a FreeCAD file.

**create_new_document(name)**

Create a new document.

**save_file(file_path)**

Save the current document.

**rollback()**

Rollback to previous state.

### Direct Operations

You can also use operation modules directly without LLM:

```python
from operations.basic_shapes import BasicShapeOperations
from operations.bim_elements import BIMOperations
from operations.properties import PropertyOperations

# Get FreeCAD document
doc = framework.file_parser.document

# Create operation helpers
shapes = BasicShapeOperations(doc)
bim = BIMOperations(doc)
props = PropertyOperations(doc)

# Create a wall directly
wall = bim.create_wall(
    length=4000,   # 4 meters (in mm)
    width=200,     # 200mm thick
    height=3000,   # 3 meters high
    name="MyWall"
)

# Set properties
props.set_color_rgb(wall, r=200, g=200, b=220)
props.set_transparency(wall, 20)
```

## Safety Rules

### Configurable Safety Modes

**STRICT Mode** (Default)
- All safety rules enabled
- Maximum protection
- Recommended for production use

**PERMISSIVE Mode**
- Some warnings instead of errors
- Allows more operations
- Use with caution

**CUSTOM Mode**
- Manually enable/disable specific rules
- Fine-grained control

### Rule Configuration

```python
from safety.rules import SafetyRules, SafetyMode

# Create custom rules
rules = SafetyRules(mode=SafetyMode.CUSTOM)

# Disable specific rule
rules.disable_rule('no_floating_objects')

# Enable specific rule
rules.enable_rule('require_delete_confirmation')

# Check rule status
is_enabled = rules.is_rule_enabled('no_delete_load_bearing')
```

## Testing

Run the test suite:

```bash
cd freeCAD
python tests/test_safety.py
```

Run examples:

```bash
python examples/usage_examples.py
```

## Supported Operations

### BIM Elements
- **Walls**: `Arch.makeWall(length, width, height)`
- **Structures**: Columns, beams (`Arch.makeStructure()`)
- **Windows**: `Arch.makeWindow(width, height)`
- **Doors**: `Arch.makeWindow()` with door properties
- **Floors**: `Arch.makeFloor(objectslist)`
- **Buildings**: `Arch.makeBuilding(objectslist)`

### Basic Shapes
- **Box**: `Part.makeBox(length, width, height)`
- **Cylinder**: `Part.makeCylinder(radius, height)`
- **Sphere**: `Part.makeSphere(radius)`
- **Cone**: `Part.makeCone(radius1, radius2, height)`

### Boolean Operations
- **Union**: Combine shapes
- **Difference**: Subtract shapes
- **Intersection**: Common volume

### Transformations
- **Move**: Translate objects
- **Rotate**: Rotate around axis
- **Scale**: Non-uniform scaling

### Properties
- **Color**: RGB color and transparency
- **Visibility**: Show/hide objects
- **Materials**: Assign materials
- **Dimensions**: Modify size properties

## LLM Prompt Template

The framework uses a structured prompt to translate natural language to FreeCAD API calls:

```
System: You are an expert FreeCAD Python API translator...

User: Create a wall 4 meters long, 3 meters high, 0.2 meters thick

Output (JSON):
{
  "operations": [{
    "code": "wall = Arch.makeWall(length=4000, height=3000, width=200)",
    "description": "Create wall: 4m x 3m x 0.2m",
    "type": "create",
    "affected_objects": ["wall"]
  }],
  "imports": ["FreeCAD", "Arch"],
  "requires_confirmation": false,
  "estimated_complexity": 2
}
```

## Validation Criteria

The framework passes these validation tests:

1. **Functional Test**: ✅ Successfully execute: "Create a 2m x 3m x 0.3m wall"
2. **Safety Test**: ✅ Block: "Delete all structural elements"
3. **Rollback Test**: ✅ Revert a failed operation sequence
4. **LLM Integration Test**: ✅ Convert natural language → valid FreeCAD API calls
5. **Error Handling**: ✅ Gracefully handle invalid commands

## Performance

- **Simple operations**: < 2 seconds
- **Complex operations**: < 10 seconds
- **Operation limit**: 50 operations per batch
- **Timeout**: 30 seconds maximum

## Troubleshooting

### FreeCAD Not Available
If FreeCAD modules are not importable:
- Ensure FreeCAD is installed
- Run within FreeCAD's Python environment
- Or install FreeCAD as a Python module

### LLM API Errors
- Check API key is set in environment variables
- Verify network connectivity
- Check API rate limits
- Use `LLMProvider.LOCAL` for mock mode (no API required)

### Permission Errors
```python
# Elevate permission level
framework.safety_validator.elevate_permission(PermissionLevel.DELETE)
```

## Examples

### Example 1: Create a Simple Room

```python
result = framework.execute_command(
    "Create a room 5 meters by 4 meters with 3 meter high walls, "
    "add a door on one wall and a window on another wall"
)
```

### Example 2: Modify Properties

```python
result = framework.execute_command(
    "Set the color of all walls to light gray and make them 20% transparent"
)
```

### Example 3: Complex Operations with Validation

```python
# This will be validated and show warnings
result = framework.execute_command(
    "Create a building with 3 floors, each floor has 4 rooms",
    dry_run=True  # Validate without executing
)

# Review warnings
if result.get('warnings'):
    for warning in result['warnings']:
        print(f"Warning: {warning['message']}")

# Execute if acceptable
if input("Proceed? (y/n): ") == 'y':
    result = framework.execute_command(
        "Create a building with 3 floors, each floor has 4 rooms",
        confirmed=True
    )
```

## Security Considerations

### Allowed Operations
- FreeCAD API calls only
- Specific module imports: FreeCAD, Part, Arch, Draft, etc.
- Read/write to specified file paths only

### Blocked Operations
- System commands (os, subprocess, sys)
- Dynamic code execution (eval, exec, compile)
- Network operations (socket, urllib)
- File system access outside FreeCAD operations

## Contributing

This is a demonstration framework. For production use:

1. Add authentication/authorization
2. Implement multi-user support
3. Add more comprehensive error handling
4. Extend test coverage
5. Add performance monitoring

## License

This framework is provided as-is for educational and development purposes.

## Version History

- **v1.0.0**: Initial release with core functionality
  - Natural language to FreeCAD API translation
  - Comprehensive safety guard rails
  - Rollback capability
  - Support for Claude and GPT-4

## Support

For issues, questions, or contributions, please refer to the project documentation.

## Acknowledgments

Built on:
- FreeCAD Python API
- Anthropic Claude API
- OpenAI GPT-4 API