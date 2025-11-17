# Setup Guide - FreeCAD LLM Framework

## Prerequisites

### 1. Python Installation
- Python 3.9 or higher
- pip package manager

Check your Python version:
```bash
python --version
# or
python3 --version
```

### 2. FreeCAD Installation

#### Option A: Standalone FreeCAD (Recommended for beginners)
Download and install from: https://www.freecad.org/downloads.php

- **Windows**: Download .exe installer
- **macOS**: Download .dmg package
- **Linux**: Use package manager or AppImage

```bash
# Ubuntu/Debian
sudo apt-get install freecad

# Fedora
sudo dnf install freecad

# macOS (with Homebrew)
brew install --cask freecad
```

#### Option B: FreeCAD as Python Module
For advanced users who want FreeCAD integrated with their Python environment.

Refer to: https://wiki.freecad.org/Embedding_FreeCAD

### 3. LLM API Keys (Optional)

#### For Claude (Anthropic)
1. Sign up at: https://console.anthropic.com/
2. Generate API key
3. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

#### For GPT-4 (OpenAI)
1. Sign up at: https://platform.openai.com/
2. Generate API key
3. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

**Note**: You can use the framework in LOCAL mode without API keys (uses mock responses for testing).

## Installation Steps

### Step 1: Clone/Download Framework

```bash
# If using git
git clone <repository-url>
cd freeCAD

# Or download and extract the zip file
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For LLM API communication

### Step 3: Verify Installation

Run the test suite:

```bash
python tests/test_safety.py
```

Expected output:
```
test_enable_disable_rules ... ok
test_operation_complexity_check ... ok
test_permission_levels ... ok
...
----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

### Step 4: Run Examples

```bash
python examples/usage_examples.py
```

This will run demonstration examples in dry-run mode (safe to run without FreeCAD).

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# LLM API Keys (optional)
ANTHROPIC_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-gpt4-api-key

# Framework Settings (optional)
FREECAD_LLM_LOG_LEVEL=INFO
FREECAD_LLM_SAFETY_MODE=STRICT
```

### Safety Configuration

Edit `safety/rules.py` to customize safety limits:

```python
# Maximum operations per batch (default: 50)
MAX_OPERATIONS_PER_BATCH = 50

# Maximum execution time in seconds (default: 30)
MAX_EXECUTION_TIME_SECONDS = 30.0

# Maximum objects to delete without confirmation (default: 10)
MAX_DELETE_OBJECTS = 10
```

## Usage Modes

### Mode 1: With FreeCAD Python Environment

If FreeCAD is installed and available in your Python path:

```python
from examples.usage_examples import FreeCADLLMFramework
from core.llm_interface import LLMProvider

framework = FreeCADLLMFramework(llm_provider=LLMProvider.CLAUDE)
framework.create_new_document("MyProject")

result = framework.execute_command(
    "Create a wall 4 meters long, 3 meters high, 0.2 meters thick"
)
```

### Mode 2: Within FreeCAD GUI

Run FreeCAD, then from the Python console:

```python
import sys
sys.path.insert(0, '/path/to/freeCAD')

from examples.usage_examples import FreeCADLLMFramework
framework = FreeCADLLMFramework()
# Now execute commands...
```

### Mode 3: Testing/Development (No FreeCAD Required)

Use LOCAL mode for testing without FreeCAD:

```python
from core.llm_interface import LLMProvider

framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
# Uses mock responses, safe for testing
```

## Troubleshooting

### Issue: "FreeCAD module not found"

**Solution 1**: Add FreeCAD to Python path
```python
import sys
sys.path.append('/usr/lib/freecad/lib')  # Linux
# or
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')  # macOS
# or
sys.path.append('C:\\Program Files\\FreeCAD\\lib')  # Windows
```

**Solution 2**: Run within FreeCAD's Python environment
```bash
# Find FreeCAD's Python
/path/to/freecad/bin/python your_script.py
```

### Issue: "LLM API Authentication Failed"

Check:
1. API key is correctly set in environment
2. API key has proper permissions
3. Network connectivity to API endpoint
4. API rate limits not exceeded

**Workaround**: Use LOCAL mode for testing
```python
framework = FreeCADLLMFramework(llm_provider=LLMProvider.LOCAL)
```

### Issue: "Permission Denied" Errors

The framework has strict permission controls. Elevate permissions:

```python
from safety.rules import PermissionLevel

framework.safety_validator.elevate_permission(PermissionLevel.DELETE)
```

### Issue: Operations Blocked by Safety Validator

This is expected behavior! Review the violation messages:

```python
result = framework.execute_command("Delete all walls")

if not result['success']:
    print("Violations:")
    for v in result['violations']:
        print(f"  - {v['message']}")
```

To override (use with caution):
```python
result = framework.execute_command(
    "Delete all walls",
    confirmed=True  # Explicitly confirm dangerous operation
)
```

## Development Setup

For contributing or extending the framework:

### 1. Install Development Tools

```bash
pip install pytest pytest-cov black flake8 mypy
```

### 2. Run Tests with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### 3. Code Formatting

```bash
black freeCAD/
flake8 freeCAD/
```

### 4. Type Checking

```bash
mypy freeCAD/
```

## Next Steps

1. **Read the README.md** for comprehensive documentation
2. **Explore examples/** to see usage patterns
3. **Check tests/** to understand safety features
4. **Review operations/** modules for direct API usage

## Support

For issues or questions:
- Check the troubleshooting section above
- Review existing tests for examples
- Consult FreeCAD Python API documentation: https://wiki.freecad.org/Python

## Quick Reference

### Import Framework
```python
from examples.usage_examples import FreeCADLLMFramework
```

### Initialize
```python
framework = FreeCADLLMFramework()
```

### Execute Command
```python
result = framework.execute_command("your command here")
```

### Check Result
```python
if result['success']:
    print("Success!")
else:
    print(f"Error: {result['error']}")
```

### Save Work
```python
framework.save_file("/path/to/output.FCStd")
```

---

**Ready to start? Run the examples:**

```bash
python examples/usage_examples.py
```
