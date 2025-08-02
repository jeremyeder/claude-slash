# claude-slash

Custom slash commands for Claude Code CLI. Save and restore your coding sessions, extract learnings, and enhance your development workflow with powerful slash commands.

## Features

- **🎯 `/slash`** - Display all available commands with descriptions
- **🎓 `/learn`** - Interactive learning and development workflow
- **📋 `/bootstrap`** - Bootstrap claude-slash installation
- **⚙️ `/menuconfig`** - Interactive configuration interface
- **🔄 `/update`** - Update commands to latest release

*All commands have shorthand aliases (e.g., `/cr-bootstrap`, `/mcfg`)*

## Installation

### One-Line Install (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash
```

### Global Installation (All Projects)
```bash
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- --global
```

## Usage

### Getting Started

After installation, use the `/slash` command to see all available commands:

```bash
# Display all available commands
/slash
```

### Learn Command

The `/learn` command provides an interactive learning and development workflow:

```bash
# Start interactive learning session
/learn
```

### Bootstrap Command

Bootstrap a new claude-slash installation:

```bash
# Bootstrap installation
/bootstrap

# Bootstrap with options
/bootstrap --global --force
```

## Command Reference

| Command | Alias | Description |
|---------|--------|--------------|
| `/slash` | - | Display all available commands |
| `/learn` | - | Interactive learning workflow |
| `/bootstrap` | `/cr-bootstrap` | Bootstrap installation |
| `/menuconfig` | `/mcfg` | Interactive configuration |
| `/update` | `/cr-upgrade` | Update to latest release |

## How It Works

Claude Code slash commands are markdown files stored in `.claude/commands/` that contain:
- Command documentation
- Shell script implementations using `!` prefix
- Dynamic argument handling with `$ARGUMENTS`

## Contributing

1. Fork this repository
2. Create a new command file in `.claude/commands/`
3. Follow the existing command format
4. Add documentation and examples
5. Run linting and tests locally
6. Submit a pull request

### Local Development

```bash
# Set up pre-commit hooks (automated quality checks - RECOMMENDED)
./install.sh --hooks

# Alternative manual setup:
pip install pre-commit
pre-commit install

# Run linting manually
npm run lint

# Run tests
npm test

# Run both linting and tests
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
# Update via install script
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
- [x] Interactive learning workflow
- [x] Comprehensive test suite with 28+ test cases
- [x] Bootstrap installation system
- [x] Interactive configuration interface
- [ ] Project templates and scaffolding
- [ ] Git workflow helpers
- [ ] Development environment setup commands
- [ ] Integration with popular tools (Docker, Kubernetes, etc.)

---

*Made with ❤️ for the Claude Code community*
