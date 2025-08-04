# claude-slash

A Python CLI tool for enhanced development workflows with Rich terminal UI and interactive commands.

## Features

- **Rich Terminal UI** - Beautiful console output with colors and formatting
- **Command Discovery** - Automatic discovery and registration of command modules
- **Interactive Workflows** - User-friendly interactive command interfaces
- **Extensible Architecture** - Easy to add new commands and functionality

## Installation

### Using UV (Recommended)
```bash
# Install from source
git clone https://github.com/jeremyeder/claude-slash.git
cd claude-slash
uv venv && source venv/bin/activate
uv sync --dev
```

### Using Pip
```bash
# Install from source
git clone https://github.com/jeremyeder/claude-slash.git
cd claude-slash
pip install -e .
```

## Usage

### Getting Started

After installation, use the `claude-slash` command:

```bash
# Display version information
claude-slash version

# Get help for all commands
claude-slash --help

# Run available commands
claude-slash --help
```

## Command Reference

The application uses automatic command discovery. Available commands are dynamically loaded from the `src/claude_slash/commands/` directory.

## Development

### Prerequisites

- Python 3.13+
- UV (recommended) or pip
- Node.js (for markdown linting)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/jeremyeder/claude-slash.git
cd claude-slash

# Set up Python environment
uv venv && source venv/bin/activate
uv sync --dev

# Install Node.js dependencies for linting
npm install

# Run the CLI locally
uv run claude-slash --help
```

### Testing

```bash
# Run all tests
npm test

# Python-specific testing
uv run pytest
uv run pytest --cov=claude_slash  # With coverage
uv run pytest tests/test_main.py  # Specific test file

# Run linting
npm run lint

# Run both linting and tests
npm run validate
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint code
uv run flake8 src/ tests/

# Type checking
uv run mypy src/
```

### Adding New Commands

1. Create a new Python file in `src/claude_slash/commands/`
2. Inherit from `BaseCommand`
3. Implement required methods and attributes
4. Commands are automatically discovered and registered

Example:
```python
from .base import BaseCommand
import typer

class NewCommand(BaseCommand):
    name = "new"
    help_text = "Description of the new command"

    def execute(self, arg: str = typer.Argument("default")):
        """Execute the command logic."""
        self.console.print(f"Running new command with: {arg}")
```

### Version Management

```bash
# Bump version levels
npm run bump:patch
npm run bump:minor
npm run bump:major

# Create release (bump + tag + push)
npm run release:patch
npm run release:minor
npm run release:major
```

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run linting and tests locally
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all public interfaces
- Write tests for new functionality
- Update documentation as needed
- Use Rich console for all terminal output

## Architecture

### Project Structure

```
src/claude_slash/
├── main.py              # CLI entry point with command discovery
├── commands/            # Command implementations
│   ├── base.py         # Base command class
│   ├── example.py      # Example command
│   └── ...             # Additional commands
└── ui/                 # User interface components
    ├── console.py      # Console formatting utilities
    ├── formatting.py   # Text formatting helpers
    └── progress.py     # Progress indicators
```

### Key Components

- **Command Discovery**: Automatic loading and registration of command classes
- **Rich Integration**: Enhanced terminal output with colors and formatting
- **Typer Framework**: Robust CLI argument parsing and help generation
- **Modular Design**: Easy to extend with new commands and functionality

## Security

- Commands are executed in your local environment
- No external network calls without explicit user consent
- All data processing happens locally
- Review command implementations before use

## Support

- **Issues**: [GitHub Issues](https://github.com/jeremyeder/claude-slash/issues)
- **Documentation**: See CLAUDE.md for development guidelines

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Release Process

New releases are automatically created when tags are pushed:

```bash
# Create and push a new release tag
git tag v1.2.0
git push origin v1.2.0
```

This triggers GitHub Actions to:
- Create a GitHub release with changelog
- Build and publish Python packages
- Update release documentation

---

*Built with Python, Typer, and Rich for an enhanced development experience*
