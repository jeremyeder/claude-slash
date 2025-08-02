# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **claude-slash** project that provides custom slash commands for the Claude Code CLI. The project extends Claude Code functionality with a streamlined set of core commands focused on command discovery, learning workflows, and configuration management.

### Architecture

- **Language**: Bash shell scripting with Node.js tooling
- **Command Format**: Markdown files with embedded shell scripts (using `!` prefix)
- **Command Storage**: `.claude/commands/` directory contains command implementations
- **Target Runtime**: Claude Code CLI environment
- **Update System**: Integrated GitHub release-based update mechanism

### Key Components

- **Commands**: Located in `.claude/commands/` - streamlined core set
  - `slash.md` - Main command with help display and update functionality
  - `learn.md` - Interactive learning and development workflow
  - `menuconfig.md` - Interactive configuration interface
- **Scripts**: Build and release automation in `scripts/`
- **Tests**: Focused test suite in `tests/`
- **CI/CD**: GitHub Actions workflows in `.github/workflows/`

## Development Commands

### Testing and Validation
```bash
# Run all tests
npm test

# Run linting (markdown + shell)
npm run lint

# Run both lint and test
npm run validate

# Run specific test file
./tests/test_commands.sh
./tests/test_update.sh
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
# Install markdown linting
npm install

# Install shellcheck (varies by OS)
# macOS: brew install shellcheck
# Ubuntu: sudo apt-get install shellcheck

# Run local development commands
markdownlint --config .markdownlint.json *.md .claude/commands/*.md
shellcheck install.sh scripts/*.sh
```

## Command Development Guidelines

### File Structure
All commands must follow this markdown structure:
```markdown
# Command Name

Brief description of what the command does.

## Usage
```
/project:command-name [arguments]
```

## Description
Detailed description of the command functionality.

## Implementation

!# Shell commands here (prefixed with !)
!echo "Hello, world!"
```

### Shell Script Requirements
- Use `git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")` for repository root
- Access user arguments via `$ARGUMENTS` variable
- Include error handling with `set -e` where appropriate
- Quote variables properly to handle paths with spaces
- Store outputs in git repository when possible (`.claude/` directory)

### Command Naming
- Use descriptive names (no specific prefix requirement after restructuring)
- Main `/slash` command provides discovery and update functionality
- Commands integrate subcommand functionality internally (e.g., `/slash update`)

### Security Requirements
- Never include dangerous operations (`rm -rf`, `sudo`, etc.)
- No hardcoded paths or sensitive information
- All operations should be safe and reversible
- Review shell command implications before implementation

## Testing Requirements

### Test Coverage
- Command file existence and structure validation
- Shell syntax validation for all embedded scripts
- Functional testing with temporary environments
- Error handling validation
- JSON structure validation for data files

### Test Development
- Add tests to `tests/test_commands.sh` for new commands
- Create dry-run tests that don't modify the actual environment
- Test both success and failure scenarios
- Validate command aliases work identically to full commands

## Git Workflow

### Commit Standards
- Use present tense commit messages
- Include detailed descriptions for complex changes
- Always squash commits before merging
- Sign commits with personal git signature

### Release Process
- Version bumping updates `VERSION` file and `install.sh`
- Git tags trigger automated releases via GitHub Actions
- Releases include changelog generation and asset packaging
- Use semantic versioning (major.minor.patch)

### Tagging Releases
```bash
# Create and push tag (triggers CI release)
git tag v1.2.0
git push origin v1.2.0
```

## Architecture Notes

### Command Discovery and Updates
- `/slash` command dynamically scans `.claude/commands/` directory for available commands
- Integrated update system downloads latest commands from GitHub releases
- Backup and restore functionality for safe updates
- Color-coded terminal output for better user experience

### Command Execution
- Commands are executed in user's local environment
- No external network calls without explicit user consent
- All operations are git-repository-aware
- Error messages provide clear guidance for resolution

### Integration Points
- Claude Code CLI slash command system
- Git repository integration for state tracking
- Node.js ecosystem for development tooling
- GitHub Actions for CI/CD automation

## Project Standards

### Code Quality
- Focused test coverage for core command structure
- Markdown and shell script linting via markdownlint and shellcheck
- Security scanning in CI pipeline
- Documentation requirements for all commands

### User Experience
- Clear command documentation with examples
- Comprehensive error handling and user feedback
- Both interactive and non-interactive modes
- Consistent command structure and behavior

## Memories

- NEVER include `/project:` in new slash commands
