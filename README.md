# GitHub Setup Claude Command

A Python-based slash command for Claude that initializes and configures GitHub repositories with best practices.

## Features

- **Interactive Mode**: User-friendly prompts guide you through repository setup
- **Security First**: Repositories are private by default
- **GitHub Projects**: Repository-level project boards with customizable templates
- **Advanced Automation**: Comprehensive GitHub Actions workflow suite
  - **Auto-versioning**: Semantic versioning based on commit messages
  - **Auto-merge**: Automatic Dependabot PR approval and merging
  - **Auto-release**: Automated releases on tag creation
  - **Claude AI Review**: Optional AI-powered code review (requires API key)
- **CI/CD Ready**: Every repository includes GitHub Actions workflows
- **Language-Specific**: CI templates adapt to your project type (Python, Node.js, etc.)
- **Documentation**: Optional Docusaurus website with automatic deployment
- **PR Previews**: Documentation preview deployments for pull requests
- **Complete Setup**: Creates local repo, initial files, and GitHub remote
- **Customizable**: Support for licenses, gitignore templates, and repo metadata
- **Best Practices**: Follows GitHub Flow and includes proper documentation

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

### Interactive Mode (Recommended)
```bash
# Launch interactive setup (prompts for all options)
./github_init_command.py

# Or force interactive mode
./github_init_command.py --interactive
```

Interactive mode guides you through:
- Repository name
- Description
- Public/private visibility 
- License selection
- Gitignore template
- Topics and settings
- Preview before creation

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
  --create-website \
  --project-template=release \
  --enable-claude-review
```

### Options

#### Basic Options
- `--interactive, -i` - Use interactive mode with prompts
- `--public` - Create a public repository (default: private)
- `--desc=<description>` - Repository description
- `--license=<type>` - Add license file (MIT, Apache-2.0, GPL-3.0)
- `--gitignore=<template>` - Add .gitignore (python, node, general)
- `--branch=<name>` - Default branch name (default: main)
- `--topics=<list>` - Comma-separated repository topics
- `--no-readme` - Skip README creation
- `--create-website` - Initialize a Docusaurus documentation website

#### GitHub Projects
- `--no-project` - Disable GitHub project creation (enabled by default)
- `--project-template=<type>` - Project template: basic, development, release (default: development)

#### Automation Options
- `--no-auto-version` - Disable automatic semantic versioning (enabled by default)
- `--no-auto-merge` - Disable Dependabot auto-merge (enabled by default)
- `--no-auto-release` - Disable automatic releases (enabled by default)
- `--enable-claude-review` - Enable Claude AI code review (requires ANTHROPIC_API_KEY)
- `--no-dependabot` - Disable Dependabot configuration (enabled by default)

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