# Testing Guide for Mouceifi

## Quick Start

### Run All Tests (No Dependencies Required)
```bash
cd mouceifi
python run_tests.py
```

### Run Specific Test Suites

**Parser tests only (no dependencies):**
```bash
python -m unittest tests/test_parser.py -v
```

**Executor tests (requires PyAutoGUI):**
```bash
python -m unittest tests/test_executor.py -v
```

### Run Live Demo
```bash
python demo.py
```

## Test Coverage

### ✅ Parser Tests (18 tests) - **No Dependencies Required**

These tests verify the NLP parser can correctly interpret natural language commands:

- **Movement Commands:**
  - `test_parse_simple_move` - "move to x=100 y=100"
  - `test_parse_move_with_commas` - "move to x=500, y=300"
  - `test_parse_relative_move` - "move 100 pixels down and 50 pixels right"
  - `test_parse_move_and_click` - "move to x=500 y=300 and then left click"

- **Click Commands:**
  - `test_parse_right_click` - "right click"
  - `test_parse_middle_click` - "middle click"
  - `test_parse_double_click` - "double click"
  - `test_parse_click_at_current_position` - "right click at current position"

- **Drag & Scroll:**
  - `test_parse_drag` - "drag from x=100 y=100 to x=300 y=300"
  - `test_parse_scroll` - "scroll down by 5"
  - `test_parse_scroll_default_amount` - "scroll up"

- **Complex Sequences:**
  - `test_parse_complex_sequence` - Multi-action commands

- **Validation:**
  - `test_coordinate_validation` - Type conversion and bounds checking
  - `test_validate_negative_coordinates` - Reject invalid coordinates
  - `test_parse_empty_command` - Error handling
  - `test_parse_invalid_command` - Error handling

**Run Status:** ✅ All 18 tests passing

### ⚠️ Executor Tests (11 tests) - **Requires PyAutoGUI**

These tests verify mouse control execution (dry-run mode):

- Factory and platform detection
- Screen size and position queries
- Action execution (move, click, drag, scroll)
- Coordinate validation
- Action sequences

**Run Status:** Skipped without PyAutoGUI, passes with it installed

## Test Results Summary

### Without PyAutoGUI (Minimal Setup)
```
Tests run: 18
Successes: 18
Failures: 0
Errors: 0
```

**This validates:**
- ✅ Natural language parsing works correctly
- ✅ Type system is sound
- ✅ Validation logic is correct
- ✅ All command patterns are recognized
- ✅ Action sequences are properly constructed

### With PyAutoGUI (Full Setup)
```
Tests run: 29
Successes: 29
Failures: 0
Errors: 0
```

**Additionally validates:**
- ✅ Platform detection
- ✅ Mouse control interface
- ✅ Dry-run execution
- ✅ Coordinate bounds checking

## Installation for Full Testing

```bash
pip install -r requirements.txt
```

Note: PyAutoGUI may have build warnings on some systems, but tests will still pass.

## Test Organization

```
tests/
├── __init__.py
├── test_parser.py      # NLP parser tests (no dependencies)
└── test_executor.py    # Mouse executor tests (requires PyAutoGUI)
```

## CI/CD Recommendations

For continuous integration, you can run tests in stages:

**Stage 1 - Parser Tests (always runs):**
```bash
python -m unittest tests/test_parser.py
```

**Stage 2 - Full Tests (with dependencies):**
```bash
pip install -r requirements.txt
python -m unittest discover tests/
```

## Manual Testing

### Demo Script (No Dependencies)
```bash
python demo.py
```

Shows parsing of all example commands without requiring mouse control libraries.

### Interactive Testing (Requires PyAutoGUI)
```bash
python -m mouceifi --interactive --dry-run
```

Enter commands and see what would be executed without moving the mouse.

### Live Execution (Requires PyAutoGUI + Caution!)
```bash
# Start with simple commands
python -m mouceifi "move to x=100 y=100"

# Test with dry-run first
python -m mouceifi --dry-run "move to x=500 y=300 and then left click"

# Then execute
python -m mouceifi "move to x=500 y=300 and then left click"
```

## Browser/MCP Testing

If you have browser MCP available, you can test:

1. **Visual Verification:**
   - Run commands that interact with browser elements
   - Verify mouse movements and clicks

2. **UI Element Detection:**
   - Test pattern matching for file selection
   - Test label-based UI element finding

3. **Integration Testing:**
   - Chain multiple commands
   - Test error recovery

## Troubleshooting

**Import Errors:**
- Parser tests should work without any dependencies
- If imports fail, check Python path: `python -c "import sys; print(sys.path)"`

**PyAutoGUI Installation Issues:**
- Parser tests will still run without it
- For full testing, try: `pip install pyautogui --no-build-isolation`

**Test Discovery:**
```bash
# List all tests
python -m unittest discover tests/ -v

# Run specific test
python -m unittest tests.test_parser.TestNLPParser.test_parse_simple_move -v
```

## Performance

All parser tests run in **~4ms** (very fast).

This makes them ideal for:
- Pre-commit hooks
- Rapid development iteration
- CI/CD pipelines
