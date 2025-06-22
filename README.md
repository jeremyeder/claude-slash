# GitHub Setup Claude Command

A Python-based slash command for Claude that initializes and configures GitHub repositories with best practices.

## Features

- **Security First**: Repositories are private by default
- **CI/CD Ready**: Every repository includes GitHub Actions workflows
- **Language-Specific**: CI templates adapt to your project type (Python, Node.js, etc.)
- **Documentation**: Optional Docusaurus website with automatic deployment
- **PR Previews**: Documentation preview deployments for pull requests
- **Complete Setup**: Creates local repo, initial files, and GitHub remote
- **Customizable**: Support for licenses, gitignore templates, and repo metadata
- **Best Practices**: Follows GitHub conventions and includes proper documentation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/github-setup-claude.git
cd github-setup-claude
```

2. Ensure prerequisites are installed:
- Python 3.6+
- GitHub CLI (`gh`)
- Git
- Node.js 18+ (only required for `--create-website` option)

3. Make the script executable:
```bash
chmod +x github_init_command.py
```

## Usage

### Basic Usage
```bash
# Create a private repository (default)
./github_init_command.py my-new-project

# Create a public repository
./github_init_command.py my-oss-project --public

# Create a documentation site
./github_init_command.py my-docs --create-website --public
```

### Advanced Options
```bash
./github_init_command.py my-app \
  --public \
  --desc="My awesome application" \
  --license=MIT \
  --gitignore=python \
  --topics=python,api,fastapi \
  --branch=develop \
  --create-website
```

### Options

- `--public` - Create a public repository (default: private)
- `--desc=<description>` - Repository description
- `--license=<type>` - Add license file (MIT, Apache-2.0, GPL-3.0)
- `--gitignore=<template>` - Add .gitignore (python, node, general)
- `--branch=<name>` - Default branch name (default: main)
- `--topics=<list>` - Comma-separated repository topics
- `--no-readme` - Skip README creation
- `--create-website` - Initialize a Docusaurus documentation website

## Claude Integration

This command is designed to be used as a slash command in Claude:

1. Register the command with Claude's system
2. Use as `/github-init <repo-name> [options]`
3. Claude will execute the Python script with the provided arguments

## Testing

Run the test suite:
```bash
python -m unittest test_github_init_command.py
```

## Project Structure

- `github_init_command.py` - Main command implementation
- `register_command.py` - Command registration for Claude
- `test_github_init_command.py` - Comprehensive test suite
- `example-usage.md` - Detailed usage examples

## License

This project is open source and available under the MIT License.