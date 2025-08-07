# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based slash command for Claude that initializes and configures GitHub repositories with best practices. The tool creates complete repository setups including CI/CD workflows, documentation sites, and follows security-first principles (private by default).

## Architecture

### Core Components

- **`github_init_command.py`** - Main command implementation with `GitHubInitCommand` class
- **`register_command.py`** - Command registration system with `SlashCommand` class for Claude integration
- **Interactive Mode** - User-friendly prompts for all configuration options via `--interactive`
- **Dry Run Mode** - Preview mode (`--dry-run`) that shows what will be created without execution
- **Rollback System** - Automatic cleanup on failure, including GitHub repo deletion

### Key Classes

- `GitHubInitOptions` - Dataclass containing all configuration parameters
- `GitHubInitCommand` - Main orchestrator that executes the initialization process
- `SlashCommand` - Registration wrapper for Claude slash command integration

## Development Commands

### Testing
```bash
# Run all tests (< 1 minute)
make test

# Run only fast unit tests (< 5 seconds)
make test-fast

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Quick syntax and import validation
make check

# Full CI validation
make ci-full
```

### Code Quality
```bash
# Run all linters
make lint

# Format code
make format

# Install test dependencies
make install-deps

# Clean test artifacts
make clean
```

### Manual Testing
```bash
# Interactive mode (recommended for testing)
./github_init_command.py --interactive

# Dry run mode (safe preview)
./github_init_command.py my-test-repo --dry-run

# Basic repository creation
./github_init_command.py my-test-repo --public --desc="Test repository"
```

## Prerequisites & Dependencies

- **Python 3.11+** (required)
- **GitHub CLI (`gh`)** (required, must be authenticated)
- **Git** (required)
- **Node.js 18+** (only for `--create-website` option)

Install test dependencies: `pip install -r requirements-test.txt`

## Test Strategy

- **Fast tests** (`test_fast.py`) - Unit tests under 5 seconds using mocks
- **Integration tests** (`test_integration_fast.py`) - Faster integration tests with GitHub API mocks
- **Full integration** (`test_github_init_command.py`) - Complete workflow tests
- **Markers**: `@pytest.mark.fast`, `@pytest.mark.slow`, `@pytest.mark.network`

## Key Features to Understand

### Security First
- Repositories are **private by default**
- Only creates public repos when explicitly requested with `--public`
- Validates GitHub API access before making changes

### Rollback System
- Automatically cleans up on failure
- Deletes both local directory and GitHub repository if creation fails
- Preserves original working directory

### Interactive Mode
- Prompts for all configuration options
- Shows preview before creation
- Validates prerequisites upfront

### GitHub Actions Integration
- Automatically creates appropriate CI/CD workflows based on project type
- Supports Python, Node.js, and other language templates
- Includes test, lint, and fast-feedback workflows

### Documentation Website Support
- Optional Docusaurus integration (`--create-website`)
- Automatic deployment to GitHub Pages
- PR preview deployments

## Error Handling Patterns

- **Prerequisite validation** before any changes
- **Rollback on failure** with detailed error messages
- **Subprocess error handling** with meaningful user feedback
- **Progress indicators** (emoji-based status messages)

## Code Conventions

- Uses **dataclasses** for configuration (`GitHubInitOptions`)
- **Subprocess calls** with proper error handling and validation
- **Path objects** from `pathlib` for file operations
- **Type hints** throughout for better maintainability
- **Docstrings** in Google style format

## CI/CD Workflows

The project includes multiple workflow tiers:
- **fast-test** (1 minute timeout) - Syntax validation and fastest unit tests
- **lint** (2 minutes timeout) - Code quality checks
- **test** (5 minutes timeout) - Full test suite with coverage

## Common Development Patterns

When working with this codebase:
1. Always run `make check` before committing
2. Use `--dry-run` mode to test changes safely
3. Integration tests should use mocks to avoid creating real repositories
4. Follow the existing error handling patterns with rollback
5. Add new features to the `GitHubInitOptions` dataclass first
6. Test both interactive and non-interactive modes for new features