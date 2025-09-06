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

### `/github-init` - Complete Repository Initialization
Enterprise-grade GitHub repository setup with outcome-driven project management:

**Core Features:**
- **🔒 Security-First**: Private repositories by default with branch protection
- **🎯 Outcome Management**: Three-tier project hierarchy (outcomes → epics → stories)
- **📋 Professional Templates**: Structured issue templates for systematic development
- **🤖 Automated Tracking**: Weekly metrics dashboard and progress reporting
- **🚀 CI/CD Ready**: Complete GitHub Actions workflow setup
- **🛡️ Security Hardening**: Dependabot, vulnerability scanning, and compliance

**Advanced Automation:**
- Repository-level project boards with automation workflows
- Hierarchical label system with validation rules
- Claude GitHub App integration for AI-powered code reviews
- Optional Docusaurus documentation site generation
- Automatic dependency management and security updates

```bash
# Basic usage - creates private repo with full automation
/github-init my-new-project --description "My awesome project"

# Public library with specific settings
/github-init python-lib --public --license MIT --gitignore Python

# Preview mode to see what will be created
/github-init test-repo --dry-run --description "Test repository"

# Full feature set with documentation
/github-init docs-project --create-website --public
```

### `/menuconfig` - Interactive TUI Configuration Editor
Linux kernel menuconfig-style interface for managing CLAUDE.md files:

**Interface Features:**
- **🐧 Familiar Navigation**: Linux kernel menuconfig-inspired keyboard shortcuts
- **🗂️ Hierarchical Editing**: Tree view of markdown sections with toggle controls
- **💾 Safe Editing**: Automatic backups and modification tracking
- **🔍 Smart Search**: Find sections quickly with built-in search functionality
- **📱 Terminal Friendly**: Works in any terminal environment

**Editing Capabilities:**
- Toggle sections enabled/disabled with visual feedback (`[*]` / `[ ]`)
- Navigate with vim-style keys (`j/k`, `h/l`) or arrows
- Real-time status bar with file info and modification indicators
- Automatic file detection (project → global CLAUDE.md)

```bash
/menuconfig                    # Edit project/global CLAUDE.md
/menuconfig custom.md          # Edit specific file
```

### `/learn` - Interactive Learning Integration
Continuously improve your CLAUDE.md with session insights:

**Learning Extraction:**
- **📝 Session Analysis**: Captures meaningful insights from Claude Code conversations
- **🤖 Smart Integration**: Suggests appropriate CLAUDE.md sections for learnings
- **💭 Interactive Review**: User-friendly interface for reviewing and editing insights
- **📊 Progress Tracking**: Visual feedback during learning extraction process

**Integration Features:**
- **🔄 Multiple Modes**: Append to existing sections or create new ones
- **💾 Safe Operations**: Automatic backup creation before modifications
- **📋 Rich Formatting**: Maintains proper markdown structure and formatting
- **⚡ Quick Access**: Works with both project and global CLAUDE.md files

```bash
/learn                         # Interactive session analysis and integration
```

### `/slash` - Help System and Updater
Comprehensive help display and automatic update system:

**Help Features:**
- **📋 Command Discovery**: Automatically finds and lists all installed commands
- **📊 Rich Display**: Beautiful table format with descriptions and usage examples
- **🔍 Smart Descriptions**: Extracts documentation from command files
- **📁 Installation Info**: Shows command installation location and status

**Update System:**
- **🔄 GitHub Integration**: Fetches latest releases using GitHub API
- **📦 Progress Tracking**: Visual progress bars for download and installation
- **💾 Safe Updates**: Automatic backup creation with rollback protection
- **✅ Verification**: Confirms successful installation and provides recovery options

```bash
/slash                         # Show help with all commands
/slash update                  # Update to latest release
```

### `/example` - Development Template
Reference implementation for command development:

- **🏗️ Architecture Demo**: Shows proper BaseCommand inheritance patterns
- **📝 Documentation**: Comprehensive inline documentation and examples
- **🎨 Rich Formatting**: Demonstrates proper terminal output styling
- **⚠️ Error Handling**: Standard error handling and user feedback patterns

```bash
/example --message "Testing the command system"
```

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

The project uses a **dual command system** supporting both Python and Markdown implementations:

#### Python Commands (Complex Logic)
1. Create Python file in `src/claude_slash/commands/` inheriting from `BaseCommand`
2. Create corresponding markdown documentation in `.claude/commands/`
3. Commands are automatically discovered and registered in both CLI and slash modes

#### Markdown Commands (Simple Documentation)
1. Create standalone markdown file in `.claude/commands/`
2. Used directly by Claude Code for simple commands and utilities

#### Command Development Example

**Python Implementation** (`src/claude_slash/commands/new.py`):
```python
from .base import BaseCommand
import typer
from typing import Any

class NewCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "new"

    @property
    def help_text(self) -> str:
        return "Description of the new command with usage examples"

    def execute(self, **kwargs: Any) -> None:
        """Execute the command logic."""
        message = kwargs.get("message", "Hello!")
        self.success(f"New command executed: {message}")

    def create_typer_command(self):
        def command_wrapper(
            message: str = typer.Option("Hello!", help="Message to display")
        ) -> None:
            self.execute(message=message)
        return command_wrapper
```

**Markdown Documentation** (`.claude/commands/new.md`):
```markdown
# New Command - Brief Description

Detailed description of what the command does and why it's useful.

## Usage
```
/new --message "Custom message"
/new --help
```

## Description
Comprehensive documentation including:
- Feature overview with benefits
- All command-line arguments and options
- Multiple usage examples
- Prerequisites and troubleshooting tips
- Integration with other commands

## Arguments
- `--message`: Message to display (default: "Hello!")

## Examples
```bash
/new --message "Testing the new command"
/new                              # Uses default message
```
```

#### Command Requirements
- **Type Hints**: All public methods must include proper type annotations
- **Error Handling**: Use `self.error()`, `self.warning()`, `self.success()` for consistent messaging
- **Rich Output**: Use `self.console` for formatted terminal output
- **Documentation**: Both Python docstrings and markdown files required
- **Testing**: Add tests in `tests/` directory for new commands

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
├── github_init.py        # /github-init repository setup (Python)
├── menuconfig.py         # /menuconfig TUI interface (Python)
├── slash.py              # /slash help and updater (Python)
├── learn.py              # /learn session analysis (Python)
├── github-init.md        # /github-init documentation (Markdown)
├── menuconfig.md         # /menuconfig documentation (Markdown)
├── slash.md              # /slash documentation (Markdown)
├── learn.md              # /learn documentation (Markdown)
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
