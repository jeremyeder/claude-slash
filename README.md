# claude-slash

Custom slash commands for Claude Code CLI. This repository provides a collection of useful slash commands that extend Claude Code's functionality.

## Features

- **📋 `/project:checkpoint`** - Save session state for future restoration
- **⚡ `/project:ckpt`** - Shorthand alias for checkpoint command
- **🔄 `/project:restore`** - Restore session from checkpoint file
- **⬆️ `/project:rst`** - Shorthand alias for restore command

## Quick Install

### Option 1: One-Line Install (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/jeremyeder/claude-slash.git

# Copy commands to your project
cp -r claude-slash/.claude/commands .claude/

# Clean up
rm -rf claude-slash
```

### Option 3: Git Subtree (Tracks Updates)
```bash
git subtree add --prefix=.claude/commands https://github.com/jeremyeder/claude-slash.git main --squash
```

To update later:
```bash
git subtree pull --prefix=.claude/commands https://github.com/jeremyeder/claude-slash.git main --squash
```

### Option 4: Global Personal Installation
```bash
# For personal use across all projects
mkdir -p ~/.claude/commands
cp -r claude-slash/.claude/commands/* ~/.claude/commands/
```

## Usage

### Checkpoint Command

Create a checkpoint of your current Claude Code session:

```bash
# Create a checkpoint with description
/project:checkpoint "Before major refactor"

# Create a quick checkpoint
/project:ckpt "Quick save"
```

### Restore Command

Restore a Claude Code session from a previously created checkpoint:

```bash
# Restore from latest checkpoint
/project:restore

# Restore from specific checkpoint file
/project:restore checkpoint-2024-07-03-10-30-00.json

# Shorthand version
/project:rst
```

#### What Gets Saved

- **Git Information**: Current branch, commit hash, status
- **File Changes**: Staged, modified, and untracked files
- **Working Directory**: Current path and context
- **Session Metadata**: Timestamp, user, system info

#### Checkpoint Storage

Checkpoints are stored in your git repository at:
```
{git-repo-root}/.claude/checkpoints/checkpoint-YYYY-MM-DD-HH-MM-SS.json
```

#### Restoring a Checkpoint

**Automated Restoration** (Recommended):
```bash
# Restore latest checkpoint automatically
/project:restore

# Restore specific checkpoint
/project:restore checkpoint-2024-07-03-10-30-00.json
```

**Manual Restoration** (Alternative):
1. Share the checkpoint JSON file with Claude in a new session
2. Claude will help restore the context and working state
3. Navigate to the correct directory and git branch as indicated

## Command Reference

| Command | Alias | Description |
|---------|--------|-------------|
| `/project:checkpoint [description]` | `/project:ckpt` | Create a session checkpoint |
| `/project:restore [checkpoint_file]` | `/project:rst` | Restore from checkpoint (latest if no file specified) |

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
# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# Run linting
npm install -g markdownlint-cli
markdownlint --config .markdownlint.json *.md .claude/commands/*.md

# Install shellcheck (varies by OS)
# macOS: brew install shellcheck
# Ubuntu: sudo apt-get install shellcheck

# Run tests
./tests/test_commands.sh

# Test update functionality
./tests/test_update.sh
```

### Command Development Guidelines

- Use descriptive names and provide aliases for common commands
- Include comprehensive documentation with usage examples
- Test commands thoroughly before submitting
- Ensure security best practices (no hardcoded paths, safe shell operations)

## Security

- Commands are executed in your local environment
- No external network calls without explicit user consent
- All checkpoint data stays local to your git repository
- Review command implementations before installation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/jeremyeder/claude-slash/issues)
- **Documentation**: [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- **Community**: Share your custom commands!

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

- [x] Session checkpoint and restoration
- [x] Automated restore command with checkpoint file override
- [x] Comprehensive test suite with 28+ test cases
- [x] Safety checks and git integration
- [ ] Project templates and scaffolding
- [ ] Git workflow helpers
- [ ] Development environment setup commands
- [ ] Integration with popular tools (Docker, Kubernetes, etc.)

---

*Made with ❤️ for the Claude Code community*