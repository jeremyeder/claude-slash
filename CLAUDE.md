# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **claude-slash** Python CLI application that provides enhanced development workflows with Rich terminal UI and interactive commands.

### Architecture

- **Language**: Python 3.13+ with Typer/Rich CLI framework
- **Command Framework**: Class-based commands with automatic discovery
- **CLI Structure**: Main entry point with modular command system
- **UI Layer**: Rich console formatting and progress indicators
- **Target Runtime**: Standalone Python CLI application

### Key Components

- **Python CLI** (`src/claude_slash/`):
  - `main.py` - Typer application with automatic command discovery
  - `commands/` - Python command classes inheriting from BaseCommand
  - `ui/` - Rich console formatting and progress indicators
- **Scripts**: Build and release automation in `scripts/`
- **Tests**: Python test suite in `tests/`
- **CI/CD**: GitHub Actions workflows in `.github/workflows/`

## Development Commands

### Testing and Validation
```bash
# Python-specific testing
uv run pytest                    # All Python tests
uv run pytest tests/test_main.py  # Specific test file
uv run pytest --cov=claude_slash # With coverage

# Python-specific linting
uv run black src/ tests/        # Format code
uv run isort src/ tests/        # Sort imports
uv run flake8 src/ tests/       # Lint code
uv run mypy src/                # Type checking

# Run all tests (via npm)
npm test

# Run linting (markdown + shell)
npm run lint

# Run both lint and test
npm run validate
```

### Version Management
```bash
# Bump version levels
npm run bump:patch
npm run bump:minor
npm run bump:major

# Release (bump + tag + push)
npm run release:patch
npm run release:minor
npm run release:major

# Manual version bump with options
./scripts/bump-version.sh patch --dry-run
./scripts/bump-version.sh minor --push --yes
```

### Development Setup
```bash
# Install Python dependencies (with virtual environment)
uv venv && source venv/bin/activate  # Create and activate venv
uv sync --dev                        # Install all dependencies including dev tools

# Install Node.js tooling
npm install                          # Markdown linting

# Install shellcheck (varies by OS)
# macOS: brew install shellcheck
# Ubuntu: sudo apt-get install shellcheck

# Python CLI development
uv run claude-slash --help          # Test CLI locally
uv run python -m claude_slash.main  # Alternative entry point
```

## Command Development Guidelines

### Python Command Development
Create Python commands by inheriting from `BaseCommand` in `src/claude_slash/commands/`:

```python
from .base import BaseCommand
import typer

class ExampleCommand(BaseCommand):
    name = "example"
    help_text = "Example command description"

    def execute(self, arg: str = typer.Argument("default")):
        """Execute the command logic."""
        self.console.print(f"Running example with: {arg}")
```

Commands are automatically discovered and registered by `main.py`.

### Command Requirements
- Use `BaseCommand` as the parent class
- Implement `name` and `help_text` class attributes
- Define `execute()` method with Typer-compatible signature
- Use `self.console` for Rich terminal output
- Include error handling and user feedback
- Follow existing patterns for consistency

### Security Requirements
- All operations should be safe and reversible
- No hardcoded paths or sensitive information
- Review command implications before implementation
- Use type hints for better development experience

## Testing Requirements

### Test Coverage
- Unit tests for all command classes
- Integration tests for CLI functionality
- Error handling validation
- Mock external dependencies appropriately

### Test Development
- Add tests to `tests/` directory for new commands
- Use pytest fixtures from `conftest.py`
- Test both success and failure scenarios
- Validate Rich console output when applicable

## Git Workflow

### Commit Standards
- Use present tense commit messages
- Include detailed descriptions for complex changes
- Always squash commits before merging
- Sign commits with personal git signature

### Release Process
- Version bumping updates `VERSION` file and `pyproject.toml`
- Git tags trigger automated releases via GitHub Actions
- Releases include changelog generation and wheel packaging
- Use semantic versioning (major.minor.patch)

### Tagging Releases
```bash
# Create and push tag (triggers CI release)
git tag v1.2.0
git push origin v1.2.0
```

## Architecture Notes

### Command Discovery
- Commands are automatically discovered from `src/claude_slash/commands/`
- Each command class is instantiated and registered with Typer
- Failed imports are logged but don't break the application
- Command registration happens at module import time

### CLI Framework
- Built on Typer for robust CLI argument parsing
- Rich integration for enhanced terminal output
- Automatic help generation from command docstrings
- Support for both positional and optional arguments

### UI Components
- Console formatting utilities in `ui/console.py`
- Progress indicators in `ui/progress.py`
- Consistent styling across all commands
- Support for both interactive and batch modes

## Project Standards

### Code Quality
- Type hints required for all public interfaces
- Black code formatting with 88-character line length
- isort for import organization
- flake8 linting with project-specific configuration
- mypy type checking enabled

### User Experience
- Clear command documentation with examples
- Comprehensive error handling and user feedback
- Rich terminal output with colors and formatting
- Consistent command structure and behavior
