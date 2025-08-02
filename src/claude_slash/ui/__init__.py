"""
Rich UI utilities for claude-slash CLI commands.

This package provides standardized Rich components and utilities for
consistent terminal output across all claude-slash commands.
"""

from .console import get_console, with_progress, with_spinner
from .formatting import (
    create_status_panel,
    create_info_table,
    format_command_table,
    format_error_message,
    format_success_message,
    format_warning_message,
    format_info_message,
)
from .progress import ProgressManager, SpinnerManager

__all__ = [
    "get_console",
    "with_progress",
    "with_spinner",
    "create_status_panel",
    "create_info_table", 
    "format_command_table",
    "format_error_message",
    "format_success_message",
    "format_warning_message",
    "format_info_message",
    "ProgressManager",
    "SpinnerManager",
]