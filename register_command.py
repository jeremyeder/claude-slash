"""Registration for the GitHub Init slash command."""

from typing import Any, Callable, Dict, List

from github_init_command import handle_github_init_command


class SlashCommand:
    """Represents a slash command that can be executed."""

    def __init__(
        self,
        name: str,
        description: str,
        usage: str,
        examples: List[str],
        handler: Callable[[List[str]], None],
    ):
        self.name = name
        self.description = description
        self.usage = usage
        self.examples = examples
        self.handler = handler

    def execute(self, args: List[str]) -> None:
        """Execute the command with given arguments."""
        self.handler(args)

    def get_help(self) -> str:
        """Get formatted help text for the command."""
        return f"""
# {self.name}

{self.description}

## Usage
{self.usage}

## Examples
{chr(10).join(f'  {example}' for example in self.examples)}
"""


# Register the GitHub Init command
github_init_command = SlashCommand(
    name="/github-init",
    description="Initialize and configure a new GitHub repository with best practices",
    usage="/github-init <repo-name> [options]",
    examples=[
        "/github-init my-project",
        "/github-init my-app --public --license=MIT --gitignore=python",
        "/github-init web-app --desc='A new web application' --topics=python,django,api",
        "/github-init private-lib --gitignore=python --license=MIT --branch=develop",
        "/github-init docs-site --create-website --public --desc='Documentation site'",
    ],
    handler=handle_github_init_command,
)


def get_command_help() -> str:
    """Get comprehensive help documentation for the command."""
    return """
# GitHub Init Command

Initialize and configure a new GitHub repository with a single command.
Repositories are created as **private by default** for security.

## Usage
/github-init <repo-name> [options]

## Options
  --desc=<description>    Repository description
  --public               Create a public repository (default: private)
  --license=<type>       Add a license file (MIT, Apache-2.0, GPL-3.0)
  --gitignore=<template> Add .gitignore file (python, node, or general)
  --no-readme            Skip README creation
  --branch=<name>        Default branch name (default: main)
  --topics=<list>        Comma-separated list of repository topics
  --create-website       Initialize a Docusaurus documentation website

## Examples
  # Create a private repository (default)
  /github-init my-private-project
  
  # Create a public repository with MIT license
  /github-init my-oss-project --public --license=MIT
  
  # Python project with gitignore and topics
  /github-init python-api --gitignore=python --topics=api,fastapi,python
  
  # Node.js project with custom branch
  /github-init node-app --public --gitignore=node --branch=develop
  
  # Documentation site with Docusaurus
  /github-init my-docs --create-website --public --desc="Project documentation"

## Requirements
- GitHub CLI (gh) must be installed and authenticated
- Git must be installed and configured
- Python 3.6 or higher
- Node.js 18+ (required when using --create-website)

## Installation
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: gh auth login
3. Configure git with your name and email

## Features
- **CI/CD Ready**: Every repository includes GitHub Actions workflows
- **Language-Specific**: CI templates adapt to your project type (Python, Node.js, etc.)
- **Documentation**: Optional Docusaurus website with automatic deployment
- **PR Previews**: Documentation preview deployments for pull requests
- **Security First**: Private repositories by default

## Security Note
Repositories are created as private by default to prevent accidental
exposure of sensitive code. Use --public flag explicitly for open source projects.
"""


# Command registry for Claude integration
COMMANDS_REGISTRY: Dict[str, SlashCommand] = {"/github-init": github_init_command}


def get_available_commands() -> List[str]:
    """Get list of all available slash commands."""
    return list(COMMANDS_REGISTRY.keys())


def execute_command(command_name: str, args: List[str]) -> None:
    """Execute a slash command by name."""
    if command_name in COMMANDS_REGISTRY:
        COMMANDS_REGISTRY[command_name].execute(args)
    else:
        raise ValueError(f"Unknown command: {command_name}")
