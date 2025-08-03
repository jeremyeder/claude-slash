# Contributing to claude-slash

Thank you for your interest in contributing to claude-slash! This document provides comprehensive guidelines for contributing to this hybrid Python/shell command project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or fix
5. Choose your development approach (Python vs Legacy)
6. Make your changes following the appropriate guidelines
7. Test your changes thoroughly
8. Submit a pull request

## Development Setup

### Python Development Environment (Recommended)

```bash
# Clone your fork
git clone https://github.com/your-username/claude-slash.git
cd claude-slash

# Set up Python development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Create a new branch
git checkout -b feature/your-feature-name

# Test your setup
claude-slash --help
pytest
```

### Legacy Development Environment

```bash
# For shell script development
npm install  # Install markdown linting

# Install shellcheck (varies by OS)
# macOS: brew install shellcheck
# Ubuntu: sudo apt-get install shellcheck

# Test legacy commands
./tests/test_commands.sh
```

## Creating New Commands

### Python Commands (Recommended)

Create new Python commands by inheriting from `BaseCommand`:

```python
# src/claude_slash/commands/mycommand.py
from typing import Any
import typer
from rich.panel import Panel

from .base import BaseCommand


class MyCommand(BaseCommand):
    """Example command demonstrating the BaseCommand interface."""
    
    @property
    def name(self) -> str:
        """Return the command name."""
        return "mycommand"
    
    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return "Example command with Rich formatting"
    
    def execute(self, **kwargs: Any) -> None:
        """Execute the command."""
        self.console.print(
            Panel(
                "Hello from my command!",
                title="My Command",
                style="green"
            )
        )
```

### Legacy Shell Commands

Create markdown files in `.claude/commands/` following this structure:

```markdown
# Command Name

Brief description of what the command does.

## Usage
\```
/project:command-name [arguments]
\```

## Description
Detailed description of the command functionality.

## Implementation

!# Your shell commands here
!echo "Hello, world!"
```

### Development Guidelines

#### Python Command Guidelines

1. **Class Design**: Inherit from `BaseCommand` for consistent behavior
2. **Rich Output**: Use Rich components (Panel, Table, Progress) for all output
3. **Type Safety**: Add comprehensive type hints to all methods
4. **Documentation**: Include detailed docstrings with examples
5. **Error Handling**: Use the base class error methods (`self.error()`, `self.warning()`)
6. **Testing**: Write pytest tests for all functionality

#### Legacy Command Guidelines

1. **Naming**: Use descriptive names and provide aliases for common operations
2. **Documentation**: Include comprehensive usage examples
3. **Security**: Never include dangerous operations (rm -rf, sudo, etc.)
4. **Testing**: Test commands thoroughly before submitting
5. **Error Handling**: Handle edge cases gracefully

### Command Best Practices

#### Python Command Best Practices

- Use Rich formatting consistently across all output
- Implement progress tracking for long-running operations
- Follow the existing UI patterns from other commands
- Use the shared console from `BaseCommand`
- Handle exceptions gracefully with user-friendly error messages
- Add examples to docstrings and help text

#### Legacy Command Best Practices

- Use `git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")` to find repository root
- Store outputs in the git repository when possible
- Provide clear status messages to users
- Use `$ARGUMENTS` for user-provided arguments
- Include error handling for missing dependencies

## Testing

Before submitting a pull request:

### Python Command Testing

1. Run the Python test suite:
   ```bash
   pytest                    # Run all tests
   pytest -v                 # Verbose output
   pytest tests/test_main.py # Specific test file
   ```

2. Run type checking and linting:
   ```bash
   mypy src/                 # Type checking
   black --check src/ tests/ # Code formatting
   isort --check src/ tests/ # Import sorting
   flake8 src/ tests/        # Linting
   ```

3. Test CLI functionality:
   ```bash
   claude-slash --help       # Test CLI
   claude-slash mycommand    # Test your command
   ```

### Legacy Command Testing

1. Run shell script tests:
   ```bash
   ./tests/test_commands.sh  # Shell script validation
   npm run lint              # Markdown linting
   npm test                  # Combined tests
   ```

2. Test commands manually in a Claude Code session

### All Tests

3. Ensure all GitHub Actions checks pass
4. Test both Python CLI and Claude Code integration modes

## Code Review Process

1. All submissions require review
2. We may suggest changes or improvements
3. Once approved, maintainers will merge your PR

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include detailed reproduction steps
- Mention your operating system and Claude Code version

## Security

- Never include secrets, API keys, or sensitive data
- Avoid commands that could harm the user's system
- Review the security implications of shell commands

## Style Guide

### Python Code
- Follow PEP 8 style guidelines
- Use Black for automatic code formatting (line length: 88)
- Sort imports with isort
- Add comprehensive type hints
- Write descriptive docstrings for all public methods
- Use Rich markup for all terminal output

### Markdown
- Use consistent heading levels
- Include code blocks with proper syntax highlighting
- Keep lines under 80 characters when possible

### Shell Scripts
- Use `set -e` for error handling
- Quote variables properly
- Use descriptive variable names
- Include comments for complex logic

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Include detailed description if necessary
- Reference issue numbers when applicable (e.g., "Fixes #37")
- Use conventional commit format when possible:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation updates
  - `test:` for test additions
  - `refactor:` for code refactoring

## License

By contributing to claude-slash, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue if you have questions about contributing!

---

*Thank you for contributing to claude-slash! 🚀*