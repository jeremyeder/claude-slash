"""
claude-slash: Custom slash commands for Claude Code CLI

This package provides session management capabilities for Claude Code,
specifically checkpoint and restore features.
"""

__version__ = "1.2.1"
__author__ = "Jeremy Eder"
__email__ = "jeremyeder@users.noreply.github.com"

from .main import app

__all__ = ["app"]