# claude-slash

Custom slash commands for Claude Code CLI. Save and restore your coding sessions with powerful checkpoint functionality.

## Features

- **📋 `/project:checkpoint`** - Save session state for future restoration
- **🔄 `/project:restore`** - Restore session from checkpoint file  
- **🧠 `/project:learn`** - Extract and integrate learnings into CLAUDE.md
- **⬆️ `/project:update`** - Update commands to latest version
- **🚀 `/project:bootstrap`** - Bootstrap claude-slash installation
- **⚙️ `/project:menuconfig`** - Interactive configuration management

*All commands have shorthand aliases (e.g., `/project:ckpt`, `/project:rst`)*

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

### Session Management
```bash
# Create a checkpoint
/project:checkpoint "Before major refactor"

# Restore from latest checkpoint
/project:restore

# Restore from specific checkpoint
/project:restore checkpoint-2024-07-03-10-30-00.json
```

### Learning Integration
```bash
# Extract session learnings into CLAUDE.md
/project:learn
```

### Updates & Configuration
```bash
# Update to latest version
/project:update

# Interactive configuration
/project:menuconfig
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
| `/project:checkpoint [description]` | `/project:ckpt` | Create a session checkpoint |
| `/project:restore [checkpoint_file]` | `/project:rst` | Restore from checkpoint |
| `/project:learn` | - | Extract session learnings |
| `/project:update` | `/project:cr-upgrade` | Update to latest version |
| `/project:bootstrap` | `/project:cr-bootstrap` | Bootstrap installation |
| `/project:menuconfig` | `/project:mcfg` | Interactive configuration |

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