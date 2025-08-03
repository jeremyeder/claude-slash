"""
Command modules for claude-slash CLI.

This package contains all command implementations that can be automatically
discovered and registered with the CLI application.
"""

from .base import BaseCommand

__all__ = ["BaseCommand"]
