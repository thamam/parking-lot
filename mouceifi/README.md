# Mouceifi

**Natural Language to Mouse Command Translator**

Mouceifi is a cross-platform tool that translates natural language descriptions into executable mouse commands. Control your mouse using intuitive English sentences instead of coordinates and API calls.

## Features

- **Natural Language Parsing**: Describe mouse actions in plain English
- **Action Sequences**: Chain multiple actions together
- **Cross-Platform Design**: Modular architecture supports Linux, Windows, and macOS
- **Linux Implementation**: Full support for X11 and Wayland
- **Dry-Run Mode**: Test commands without actual mouse movement
- **Type-Safe**: Comprehensive type hints and validation
- **Interactive Mode**: Enter commands in a REPL-style interface

## Installation

### Prerequisites

- Python 3.8 or higher
- Linux (X11 or Wayland) - Windows and macOS support coming soon

### Install Dependencies

```bash
cd mouceifi
pip install -r requirements.txt
```

Or install system-wide (not recommended):
```bash
pip install -r requirements.txt --break-system-packages
```

For development:
```bash
pip install -e .
```

## Usage

### Command Line

Execute a single command:
```bash
python -m mouceifi "move to x=500 y=300 and then left click"
```

Dry-run mode (preview without executing):
```bash
python -m mouceifi --dry-run "move to x=100 y=100 then double click"
```

### Interactive Mode

Start an interactive session:
```bash
python -m mouceifi --interactive
```

In interactive mode:
```
mouceifi> move to x=100 y=100
mouceifi> left click
mouceifi> help
mouceifi> status
mouceifi> quit
```

## Supported Commands

### Movement

**Absolute positioning:**
```
move to x=500 y=300
move to x=100, y=200
```

**Relative positioning:**
```
move 100 pixels down
move 50 pixels right
move 100 pixels down and 50 pixels right
move 100 pixels up and 75 pixels left
```

### Clicking

**Basic clicks:**
```
left click
right click
middle click
double click
```

**Click at specific position:**
```
move to x=200 y=200 and then left click
right click at current position
```

### Dragging

```
drag from x=100 y=100 to x=300 y=300
```

### Scrolling

```
scroll down
scroll up
scroll down by 5
scroll left by 10
```

### Complex Sequences

Chain multiple actions together using "and then" or "and":
```
move to x=500 y=300 and then left click
move 100 pixels down and 50 pixels right then double click
move to x=100 y=100 then left click then move 50 pixels right then double click
```

## Architecture

```
mouceifi/
├── mouceifi/
│   ├── parser/           # Natural language parsing
│   │   ├── nlp_parser.py # NLP command parser
│   │   └── types.py      # Type definitions for actions
│   ├── executor/         # Platform-specific execution
│   │   ├── base.py       # Abstract executor interface
│   │   ├── linux.py      # Linux implementation (PyAutoGUI)
│   │   ├── windows.py    # Windows stub (future)
│   │   └── macos.py      # macOS stub (future)
│   ├── utils/            # Validation and utilities
│   └── main.py           # CLI interface
├── tests/                # Test suite
├── examples/             # Example commands
└── requirements.txt
```

### Design Principles

1. **Separation of Concerns**: Parsing is separate from execution
2. **Platform Abstraction**: Base executor interface allows platform-specific implementations
3. **Type Safety**: Comprehensive type hints and dataclasses
4. **Testability**: Dry-run mode allows testing without hardware interaction

## Examples

See `examples/example_commands.txt` for a comprehensive list of commands.

**Example 1: Move and click**
```bash
python -m mouceifi "move to x=500 y=300 and then left click"
```

**Example 2: Relative movement with double-click**
```bash
python -m mouceifi "move 100 pixels down and 50 pixels right then double click"
```

**Example 3: Drag operation**
```bash
python -m mouceifi "drag from x=100 y=100 to x=300 y=300"
```

**Example 4: Test with dry-run**
```bash
python -m mouceifi --dry-run "move to x=100 y=100 then left click then scroll down by 5"
```

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m unittest tests/test_parser.py

# Run with verbose output
python -m unittest tests/test_parser.py -v
```

## Development

### Adding New Actions

1. Define action type in `mouceifi/parser/types.py`
2. Add parsing logic in `mouceifi/parser/nlp_parser.py`
3. Implement execution in `mouceifi/executor/base.py` and platform-specific files
4. Add tests in `tests/`

### Adding Platform Support

To add Windows or macOS support:

1. Implement the abstract methods in `mouceifi/executor/base.py`
2. Create platform-specific file (e.g., `windows.py` or `macos.py`)
3. Update factory function in `mouceifi/executor/__init__.py`
4. Recommended libraries:
   - **Windows**: pyautogui, pywinauto, or ctypes with Win32 API
   - **macOS**: pyautogui or pyobjc-framework-Quartz

## Limitations

### Current Version (v0.1.0)

- **UI Element Selection**: Basic implementation; OCR and accessibility API support planned
- **Windows/macOS**: Stub implementations only (Linux fully supported)
- **Error Recovery**: Limited retry logic for failed operations

### Linux-Specific Notes

- **Wayland**: Some features may have limitations due to Wayland's security model
- **Permissions**: May require X11 access permissions
- **Virtual Environments**: PyAutoGUI requires display access

## Advanced Features (Planned)

- **UI Element Detection**: OCR-based text finding, accessibility API integration
- **Macro Recording**: Record mouse actions and play back
- **Conditional Logic**: "if button exists, click it"
- **Voice Input**: Integrate with speech recognition
- **GUI Interface**: Visual command builder

## Safety

- **Fail-Safe**: Move mouse to top-left corner to abort (PyAutoGUI default)
- **Dry-Run Mode**: Always test commands with `--dry-run` first
- **Coordinate Validation**: Prevents out-of-bounds movements
- **Interrupt Handling**: Ctrl+C safely stops execution

## Troubleshooting

**ImportError: No module named 'pyautogui'**
```bash
pip install pyautogui
```

**Permission errors on Linux**
```bash
# Ensure X11 access
xhost +local:
```

**Wayland issues**
```bash
# Try running under XWayland
GDK_BACKEND=x11 python -m mouceifi "your command"
```

**Mouse not moving**
- Verify you're not in dry-run mode
- Check screen coordinates are within bounds
- Try with verbose flag: `python -m mouceifi -v "command"`

## Contributing

Contributions are welcome! Areas of interest:

- Windows and macOS executor implementations
- UI element detection (OCR, accessibility APIs)
- Additional NLP parsing patterns
- Performance optimizations
- Documentation improvements

## License

MIT License - See LICENSE file for details

## Credits

- **PyAutoGUI**: Cross-platform mouse control
- **Python Type Hints**: Static type checking
- **Regex Parsing**: Command pattern matching

## Version History

- **v0.1.0** (Current): Initial release with Linux support, basic NLP parsing, and interactive mode

## Support

For issues, questions, or feature requests, please open an issue on the project repository.
