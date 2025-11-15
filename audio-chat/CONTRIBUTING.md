# Contributing to Conversation Review Voice Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run the test suite:
```bash
# Using pytest
pytest tests/

# Or manually
python tests/test_agent.py --manual
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

## Adding Features

### Priority Areas

1. **Voice Integration**: TTS/STT service integrations
2. **Conversation Parsers**: Support for additional formats
3. **Question Detection**: Improved pattern matching
4. **Internationalization**: Multi-language support

### Feature Development Process

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Implement your feature with tests
3. Ensure all tests pass
4. Update documentation (README, docstrings)
5. Submit a pull request

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage
- Include both unit and integration tests
- Test edge cases and error conditions

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include examples for new features
- Update the roadmap if adding planned features

## Pull Request Process

1. Ensure your code passes all tests
2. Update the README with details of changes
3. Add yourself to CONTRIBUTORS.md (create if needed)
4. Reference any related issues in your PR description
5. Wait for review from maintainers

## Reporting Bugs

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error messages

## Suggesting Enhancements

Enhancement suggestions are welcome! Please:

- Check if the enhancement is already planned (see Roadmap)
- Provide clear use cases
- Describe the expected behavior
- Consider implementation challenges

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the technical merits
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
