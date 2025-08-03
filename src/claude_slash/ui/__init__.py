"""
Rich UI utilities for claude-slash CLI commands.

This package provides standardized Rich components and utilities for
consistent terminal output across all claude-slash commands. It includes
progress bars, spinners, panels, tables, and formatting utilities for
creating beautiful and consistent CLI experiences.

Key Components:
- Console management with shared Rich console instance
- Progress bars for downloads, file operations, and general tasks
- Spinner managers for long-running operations
- Formatted panels and tables for structured output
- Error, success, warning, and info message formatting
- Context managers for progress tracking and spinner operations

Usage:
    from claude_slash.ui import get_console, ProgressManager, format_success_message

    console = get_console()
    console.print(format_success_message("Operation completed"))

    with ProgressManager.file_operation("Processing files...") as progress:
        # Long running operation
        pass
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
from .progress import ProgressManager, SpinnerManager, track_operation

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
    "track_operation",
]
