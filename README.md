# claude-slash

A powerful Python CLI with custom slash commands for Claude Code. Enhance your development workflow with session management, interactive learning, and rich terminal UI experiences.

## Features

- **🎯 `/slash`** - Display all available commands with Rich-formatted help
- **🔄 `/slash update`** - Update commands to latest release with progress tracking
- **🎓 `/learn`** - Interactive learning and development workflow
- **⚙️ `/menuconfig`** - Interactive configuration interface with TUI
- **🐍 Python CLI** - Modern Python implementation with Rich terminal UI
- **📦 Hybrid Commands** - Support for both Python commands and legacy shell scripts

## Installation

### Python Installation (Recommended)

#### From Source
```bash
# Clone the repository
git clone https://github.com/jeremyeder/claude-slash.git
cd claude-slash

# Install with pip (Python 3.13+ required)
pip install .

# Or install in development mode
pip install -e .
```

#### From PyPI (Future)
```bash
# Once published to PyPI
pip install claude-slash
```

### Legacy Shell Installation

#### One-Line Install
```bash
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash
```

#### Global Installation (All Projects)
```bash
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- --global
```

## Usage

### Python CLI Usage

After Python installation, you can use claude-slash in multiple ways:

```bash
# Run as a CLI application
claude-slash slash          # Show all commands
claude-slash learn          # Start learning session
claude-slash menuconfig     # Interactive configuration

# Check version
claude-slash version
```

### Claude Code Integration

For use within Claude Code CLI environment:

```bash
# Display all available commands with Rich formatting
/slash

# Start interactive learning session
/learn

# Interactive configuration interface
/menuconfig

# Update to latest release
/slash update
```

### Command Examples

#### Learning Command
```bash
# Interactive learning workflow
/learn
```

#### Configuration
```bash
# Launch interactive configuration TUI
/menuconfig
```

#### Help and Updates
```bash
# Show help with Rich formatting
/slash

# Update commands with progress tracking
/slash update
```

## Command Reference

| Command | Description | Type |
|---------|-------------|------|
| `/slash` | Display help with Rich formatting | Python |
| `/slash update` | Update to latest release with progress | Python |
| `/learn` | Interactive learning workflow | Python |
| `/menuconfig` | Interactive configuration interface (TUI) | Python |
| `checkpoint` | Create session checkpoints | Python |
| `restore` | Restore from session checkpoints | Python |

### Command Types
- **Python Commands**: Modern Rich-formatted CLI commands with progress bars, tables, and interactive elements
- **Legacy Shell Commands**: Markdown-based commands with embedded shell scripts (`.claude/commands/*.md`)

## How It Works

### Hybrid Architecture

Claude-slash uses a hybrid architecture supporting both modern Python commands and legacy shell commands:

#### Python Commands
- Located in `src/claude_slash/commands/`
- Use Rich for beautiful terminal output
- Provide progress bars, interactive elements, and formatted help
- Type-safe with full Python tooling support

#### Legacy Shell Commands
- Stored as markdown files in `.claude/commands/`
- Contain embedded shell scripts using `!` prefix
- Support dynamic argument handling with `$ARGUMENTS`
- Maintained for backward compatibility

### Command Discovery
The CLI automatically discovers and registers all available commands from both sources, providing a unified interface for all functionality.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

### Quick Start

1. Fork this repository
2. Clone and set up development environment:
   ```bash
   git clone https://github.com/your-username/claude-slash.git
   cd claude-slash
   pip install -e ".[dev]"  # Install with development dependencies
   ```
3. Choose your contribution type:
   - **Python Commands**: Create new files in `src/claude_slash/commands/`
   - **Legacy Commands**: Create markdown files in `.claude/commands/`
4. Follow existing patterns and add comprehensive tests
5. Run quality checks and submit a pull request

### Local Development

#### Python Development
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run Python tests
pytest

# Run Python linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/

# Run all Python quality checks
pytest && black --check src/ tests/ && isort --check src/ tests/ && flake8 src/ tests/ && mypy src/
```

#### Legacy Development
```bash
# Set up pre-commit hooks for shell scripts
./install.sh --hooks

# Run legacy shell tests
npm test

# Run markdown/shell linting
npm run lint

# Run both legacy linting and tests
npm run validate
```

### Pre-commit Hooks

Pre-commit hooks automatically run quality checks before each commit to prevent CI failures:

- **Markdown linting** - Ensures consistent markdown formatting
- **Shell script validation** - Checks shell syntax with shellcheck
- **File quality checks** - Removes trailing whitespace, ensures proper file endings

**Setup**: Run `./install.sh --hooks` to automatically install and configure pre-commit hooks.

**Manual execution**: `pre-commit run --all-files`

**Skip once**: `git commit --no-verify` (use sparingly)

### Command Development Guidelines

#### Python Commands (Recommended)
- Inherit from `BaseCommand` class for consistent behavior
- Use Rich for all terminal output (panels, tables, progress bars)
- Include comprehensive docstrings with examples
- Implement proper error handling with user-friendly messages
- Add type hints for all methods and properties

#### Legacy Shell Commands
- Use descriptive names and provide aliases for common commands
- Include comprehensive documentation with usage examples
- Test commands thoroughly before submitting
- Ensure security best practices (no hardcoded paths, safe shell operations)

## Security

- Commands are executed in your local environment
- No external network calls without explicit user consent
- All data stays local to your git repository
- Review command implementations before installation

## Support

- **Issues**: [GitHub Issues](https://github.com/jeremyeder/claude-slash/issues)
- **Documentation**: [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands)

MIT License - see [LICENSE](LICENSE) file for details.

## Updating Commands

### Automatic Updates

Keep your commands current with the latest features:

```bash
# Update via slash command
/slash update

# Or update via install script
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- --update
```

### Release Process

New releases are automatically created when tags are pushed:

```bash
# Create and push a new release tag
git tag v1.1.0
git push origin v1.1.0
```

This triggers GitHub Actions to:
- Create a GitHub release with changelog
- Package command files as downloadable assets
- Make the release available for updates

## Roadmap

- [x] Dynamic command discovery with `/slash`
- [x] Integrated update system with `/slash update`
- [x] Interactive learning workflow
- [x] Comprehensive test suite with 28+ test cases
- [x] Interactive configuration interface
- [ ] Project templates and scaffolding
- [ ] Git workflow helpers
- [ ] Development environment setup commands
- [ ] Integration with popular tools (Docker, Kubernetes, etc.)

---

*Made with ❤️ for the Claude Code community*
<!-- CI trigger -->
