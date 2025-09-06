# claude-slash

A Python CLI tool for enhanced development workflows with Rich terminal UI, interactive commands, and comprehensive GitHub repository initialization.

## Features

- **GitHub Repository Initialization** - Complete `/github-init` command with CI/CD, security, and project management setup
- **Rich Terminal UI** - Beautiful console output with colors and formatting
- **Claude Code Integration** - Slash commands that work directly in Claude conversations
- **Interactive Workflows** - User-friendly TUI interfaces (menuconfig-style)
- **Project-Specific Installation** - Install per-project without global conflicts
- **Auto-Updates** - Keeps itself current with latest releases

## Installation

### Project-Specific Installation (Recommended)
```bash
# Install to any project directory
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- ~/repos/example

# Update (re-run same command)
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- ~/repos/example
```

### Development Installation
```bash
# For contributing to claude-slash itself
git clone https://github.com/jeremyeder/claude-slash.git
cd claude-slash
uv venv && source venv/bin/activate
uv sync --dev
```

## Usage

### Claude Code Integration (Primary Use)
After installation, use slash commands directly in Claude conversations:

```
/github-init my-new-repo --description "My awesome project"
/menuconfig
/learn
/example --message "Testing the system"
```

### CLI Access
```bash
# From project directory where claude-slash is installed
.claude-slash/bin/claude-slash --help
.claude-slash/bin/claude-slash github-init my-repo

# Or add to PATH temporarily
export PATH=".claude-slash/bin:$PATH"
claude-slash --help
```

## Key Commands

### `/github-init` - Repository Initialization
Complete GitHub repository setup with best practices:

- **Repository Creation** - Creates private GitHub repo with proper configuration
- **CI/CD Workflows** - GitHub Actions for testing, linting, and automated releases
- **Branch Protection** - Enforces code review and status checks
- **GitHub Projects** - Repository-level project boards with outcome tracking
- **Security Setup** - Dependabot, security scanning, and vulnerability management
- **Documentation** - Optional Docusaurus site generation
- **Claude Integration** - Pre-configured Claude Code workflows and permissions

```bash
# Basic usage
/github-init my-new-project

# With custom options (interactive prompts guide you)
/github-init --dry-run  # Preview what will be created
```

### `/menuconfig` - Interactive Configuration
Linux kernel menuconfig-style TUI for managing CLAUDE.md files:

- Navigate hierarchical configuration menus
- Enable/disable features and settings
- Save/load different configuration profiles
- Real-time validation and help text

### `/learn` - Interactive Learning Integration
Continuously refine your global CLAUDE.md with session learnings:

- **Session Analysis**: Analyzes current Claude Code session for insights
- **Interactive Integration**: User-friendly interface for reviewing learnings
- **Smart Suggestions**: Automatically suggests appropriate CLAUDE.md sections
- **Automatic Backup**: Creates backup before making changes
- **Multiple Integration Modes**: Append, insert, or manual integration options
- **Rich UI**: Progress tracking and formatted terminal output

### `/example` - Development Template
Example command for testing and development:

- **Command Discovery Testing** - Verifies automatic command registration
- **Development Template** - Copy/paste template for new commands
- **Rich Formatting Demo** - Shows proper terminal output formatting
- **Error Handling** - Demonstrates standard error handling patterns

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
2. Create a corresponding markdown file in `.claude/commands/`
3. Inherit from `BaseCommand` in the Python file
4. Implement required methods and attributes
5. Commands are automatically discovered and registered

Example Python command (`src/claude_slash/commands/new.py`):
```python
from .base import BaseCommand
import typer

class NewCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "new"

    @property
    def help_text(self) -> str:
        return "Description of the new command"

    def execute(self, **kwargs):
        """Execute the command logic."""
        message = kwargs.get("message", "Hello!")
        self.success(f"New command executed: {message}")

    def create_typer_command(self):
        def command_wrapper(message: str = typer.Option("Hello!", help="Message to display")):
            self.execute(message=message)
        return command_wrapper
```

Example markdown file (`.claude/commands/new.md`):
```markdown
# New Command - Description

Brief description of what the command does.

## Usage
/new --message "Custom message"

## Description
Detailed description of functionality...
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
src/claude_slash/           # Python CLI package
├── main.py                # CLI entry point with command discovery
├── commands/              # CLI command implementations
│   ├── base.py           # Base command class
│   ├── github_init.py    # GitHub repository initialization
│   ├── learn.py          # Interactive learning integration
│   ├── menuconfig.py     # TUI configuration editor
│   ├── example.py        # Development template command
│   └── slash.py          # Slash command utilities
└── ui/                   # User interface components
    ├── console.py        # Console formatting utilities
    ├── formatting.py     # Text formatting helpers
    └── progress.py       # Progress indicators

.claude/commands/          # Claude Code slash commands
├── github_init.py        # /github-init slash command (Python)
├── menuconfig.py         # /menuconfig TUI interface (Python)
├── slash.py              # /slash utilities (Python)
├── learn.md              # /learn knowledge management (Markdown)
├── example.md            # /example development template (Markdown)
└── error-utils.md        # Error handling utilities (Markdown)

install.sh                # Project-specific installer
```

### Key Components

- **Dual Interface**: Both CLI commands and Claude Code slash commands
- **Command Discovery**: Automatic loading and registration of command classes
- **Rich Integration**: Enhanced terminal output with colors and formatting
- **Project Isolation**: Per-project installations with no global conflicts
- **GitHub Integration**: Complete repository lifecycle management
- **Interactive TUIs**: menuconfig-style interfaces for complex workflows
- **Learning Integration**: Session analysis and knowledge management
- **Hybrid Command Format**: Python files for complex logic, markdown for simple commands

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
