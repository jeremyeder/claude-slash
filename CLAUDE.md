# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **claude-slash** Python CLI application that provides enhanced development workflows with Rich terminal UI and interactive commands. It features a unique **dual interface architecture** supporting both traditional CLI usage and Claude Code slash command integration.

### Architecture

- **Language**: Python 3.13+ with Typer/Rich CLI framework
- **Dual Interface**: Both standalone CLI and Claude Code slash commands
- **Command Framework**: Hybrid system with Python classes and Markdown files
- **CLI Structure**: Main entry point with automatic command discovery
- **UI Layer**: Rich console formatting and progress indicators
- **Target Runtime**: Standalone Python CLI + Claude Code integration

### Key Components

- **Python CLI** (`src/claude_slash/`):
  - `main.py` - Typer application with automatic command discovery
  - `commands/` - Python command classes inheriting from BaseCommand
  - `ui/` - Rich console formatting and progress indicators
- **Claude Code Integration** (`.claude/commands/`):
  - Python files for complex commands (e.g., `github_init.py`, `menuconfig.py`)
  - Markdown files for simple commands (e.g., `learn.md`, `example.md`)
  - Utility files (e.g., `error-utils.md`)
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

### Dual Command System
This project uses a hybrid approach for maximum flexibility:

1. **Python Commands** (for complex logic): Located in `src/claude_slash/commands/`
2. **Slash Commands** (for Claude Code): Located in `.claude/commands/`

### Python Command Development
Create Python commands by inheriting from `BaseCommand` in `src/claude_slash/commands/`:

```python
from .base import BaseCommand
import typer
from typing import Any

class ExampleCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "example"

    @property
    def help_text(self) -> str:
        return "Example command description with usage examples"

    def execute(self, **kwargs: Any) -> None:
        """Execute the command logic."""
        arg = kwargs.get("arg", "default")
        self.success(f"Running example with: {arg}")

    def create_typer_command(self):
        """Create Typer command with custom arguments."""
        def command_wrapper(
            arg: str = typer.Option("default", help="Example argument")
        ) -> None:
            self.execute(arg=arg)
        return command_wrapper
```

Commands are automatically discovered and registered by `main.py`.

### Slash Command Development
For Claude Code integration, create corresponding files in `.claude/commands/`:

1. **Complex Commands**: Copy Python file to `.claude/commands/` (e.g., `github_init.py`)
2. **Simple Commands**: Create markdown file in `.claude/commands/` (e.g., `learn.md`)

Markdown slash command format:
```markdown
# Command Name - Brief Description

Detailed description of what the command does.

## Usage
/command-name --option value

## Description
Implementation details and examples...
```

### Command Requirements
- Use `BaseCommand` as the parent class for Python commands
- Implement `name` and `help_text` as `@property` methods
- Define `execute()` method with `**kwargs` signature
- Use `self.console` for Rich terminal output
- Create corresponding slash command file in `.claude/commands/`
- Include comprehensive error handling and user feedback

### Security Requirements
- All operations should be safe and reversible
- No hardcoded paths or sensitive information
- Review command implications before implementation
- Use type hints for better development experience

## Implemented Commands

### Core Commands

#### `/github-init` - Repository Initialization
Complete GitHub repository setup with outcome-driven project management:
```bash
/github-init my-repo --description "Project description" --public
/github-init my-repo --dry-run  # Preview without creating
```
- Creates GitHub repository with security-first defaults
- Sets up CI/CD workflows, branch protection, and Dependabot
- Includes outcome/epic/story project management system
- Installs Claude GitHub App for AI-powered code reviews

#### `/learn` - Interactive Learning Integration
Extracts session insights and integrates them into CLAUDE.md:
```bash
/learn  # Interactive session analysis and integration
```
- Analyzes Claude Code session for meaningful insights
- Provides interactive interface for reviewing learnings
- Smart section suggestions based on content analysis
- Automatic backup creation before modifications

#### `/menuconfig` - TUI Configuration Editor
Linux kernel menuconfig-style editor for CLAUDE.md files:
```bash
/menuconfig              # Edit project/global CLAUDE.md
/menuconfig custom.md    # Edit specific file
```
- Navigate hierarchical configuration structure
- Enable/disable sections with visual feedback
- Real-time editing with backup creation

#### `/example` - Development Template
Template command for testing and development reference:
```bash
/example --message "Custom text"
```
- Demonstrates proper BaseCommand inheritance
- Tests command discovery system
- Serves as copy/paste template for new commands

### Utility Commands

#### `version` - Version Information
```bash
claude-slash version
```

#### `checkpoint` & `restore` - Session Management
```bash
claude-slash checkpoint auto
claude-slash restore latest
```
**Note**: These are placeholder commands for future session management functionality.

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

### Dual Interface System
The project implements a sophisticated dual interface architecture:

1. **CLI Interface**: Traditional command-line interface via `uv run claude-slash`
2. **Slash Commands**: Claude Code integration via `/command-name` syntax
3. **Shared Logic**: Python command classes serve both interfaces
4. **Flexible Storage**: Commands can be Python files or Markdown files

### Command Discovery
**Python CLI Commands:**
- Commands automatically discovered from `src/claude_slash/commands/`
- Each command class instantiated and registered with Typer
- Failed imports are logged but don't break the application
- Registration happens at module import time

**Slash Commands:**
- Discovered from `.claude/commands/` directory
- Supports both Python files (complex commands) and Markdown files (simple commands)
- Python files are executed directly by Claude Code
- Markdown files provide documentation and simple command definitions

### CLI Framework
- Built on Typer for robust CLI argument parsing
- Rich integration for enhanced terminal output
- Automatic help generation from command docstrings
- Support for both positional and optional arguments
- Error handling with Rich-formatted messages

### UI Components
- Console formatting utilities in `ui/console.py`
- Progress indicators in `ui/progress.py`
- Consistent styling across all commands
- Support for both interactive and batch modes
- SpinnerManager and ProgressManager for long-running operations

### Command Execution Flow
1. **CLI Mode**: `main.py` → command discovery → Typer registration → execution
2. **Slash Mode**: Claude Code → `.claude/commands/` → direct execution or markdown parsing

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
