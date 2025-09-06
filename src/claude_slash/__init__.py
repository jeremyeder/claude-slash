"""
claude-slash: Python CLI with custom slash commands for Claude Code

This package provides a modern Python CLI with Rich terminal UI for Claude
Code, featuring session management, interactive learning workflows, and hybrid
command support (both Python and legacy shell commands).

Key Features:
- Rich-formatted terminal output with progress bars and interactive elements
- Interactive learning and configuration interfaces
- Hybrid architecture supporting both Python and shell-based commands
- Comprehensive CLI with automatic command discovery

Usage:
    # As a standalone CLI
    claude-slash slash          # Show all commands
    claude-slash learn          # Interactive learning
    claude-slash menuconfig     # Configuration interface

    # Within Claude Code environment
    /slash                      # Show help
    /learn                      # Learning workflow
    /menuconfig                 # Configuration
"""

__version__ = "1.5.0"
__author__ = "Jeremy Eder"
__email__ = "jeremyeder@users.noreply.github.com"

from .main import app

__all__ = ["app"]
