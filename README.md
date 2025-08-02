# claude-slash

Custom slash commands for Claude Code CLI. Save and restore your coding sessions, extract learnings, and enhance your development workflow with powerful slash commands.

## Features

- **📋 `/slash`** - Display all available commands with descriptions
- **💾 `/checkpoint`** - Save session state for future restoration
- **🔄 `/restore`** - Restore session from checkpoint file  
- **🧠 `/learn`** - Extract and integrate learnings into CLAUDE.md
- **⬆️ `/update`** - Update commands to latest version
- **🚀 `/bootstrap`** - Bootstrap claude-slash installation
- **⚙️ `/menuconfig`** - Interactive configuration management

*All commands have shorthand aliases (e.g., `/ckpt`, `/rst`)*

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

### Command Discovery

Get help and see all available commands:

```bash
# Display all available commands
/slash
```

### Session Management
```bash
# Create a checkpoint
/checkpoint "Before major refactor"

# Restore from latest checkpoint
/restore

# Restore from specific checkpoint
/restore checkpoint-2024-07-03-10-30-00.json
```

### Learning Integration
```bash
# Extract session learnings into CLAUDE.md
/learn
```

### Updates & Configuration
```bash
# Update to latest version
/update

# Interactive configuration
/menuconfig
```

## What Gets Saved

Checkpoints capture your complete development context:
- **Git state**: branch, commit hash, staged/modified files
- **Working directory**: current path and file structure
- **Session metadata**: timestamp, user, system info

Checkpoints are stored in `.claude/checkpoints/` within your git repository.

## Command Reference

| Command | Alias | Description |
|---------|-------|-------------|
| `/slash` | - | Display all available commands with descriptions |
| `/checkpoint [description]` | `/ckpt` | Create a session checkpoint |
| `/restore [checkpoint_file]` | `/rst` | Restore from checkpoint |
| `/learn` | - | Extract session learnings |
| `/update` | `/cr-upgrade` | Update to latest version |
| `/bootstrap` | `/cr-bootstrap` | Bootstrap installation |
| `/menuconfig` | `/mcfg` | Interactive configuration |

## Updates

```bash
# Update existing installation
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- --update
```

## Contributing

1. Fork this repository
2. Create a new command file in `.claude/commands/`
3. Follow existing command format
4. Test your changes
5. Submit a pull request

### Development Setup
```bash
# Set up quality checks
./install.sh --hooks

# Run tests
npm test
```

## Security

- Commands execute in your local environment only
- No external network calls without explicit consent
- All data stays local to your git repository
- Review command implementations before installation

## Support

- **Issues**: [GitHub Issues](https://github.com/jeremyeder/claude-slash/issues)
- **Documentation**: [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

*Made with ❤️ for the Claude Code community*