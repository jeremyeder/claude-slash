"""
Console utilities for consistent Rich output across claude-slash commands.

This module provides a shared Rich console instance and utility functions
for progress tracking and spinner operations. All commands should use the
shared console instance to ensure consistent formatting and behavior.

Functions:
- get_console(): Get the shared Rich console instance
- with_progress(): Context manager for progress bar operations
- with_spinner(): Context manager for spinner operations

Usage:
    console = get_console()
    console.print("Hello, world!")
    
    with with_progress("Processing...") as progress:
        # Long running operation
        pass
"""

import time
from contextlib import contextmanager
from typing import Any, Generator, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.status import Status


# Global console instance for consistent output
_console: Optional[Console] = None


def get_console() -> Console:
    """
    Get a shared Console instance for consistent output formatting.
    
    Returns:
        Shared Rich Console instance
    """
    global _console
    if _console is None:
        _console = Console()
    return _console


@contextmanager
def with_progress(
    description: str = "Working...",
    show_percentage: bool = True,
    show_time: bool = True
) -> Generator[Progress, None, None]:
    """
    Context manager for Rich progress bars.
    
    Args:
        description: Description text for the progress bar
        show_percentage: Whether to show percentage completion
        show_time: Whether to show elapsed time
        
    Yields:
        Progress instance for tracking operations
        
    Example:
        with with_progress("Downloading files...") as progress:
            task = progress.add_task("Download", total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.01)
    """
    columns = [
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ]
    
    if show_percentage:
        columns.extend([
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ])
    
    if show_time:
        columns.append(TimeElapsedColumn())
    
    with Progress(*columns, console=get_console()) as progress:
        yield progress


@contextmanager
def with_spinner(
    text: str = "Working...",
    spinner: str = "dots"
) -> Generator[Status, None, None]:
    """
    Context manager for Rich spinner status indicators.
    
    Args:
        text: Status text to display with spinner
        spinner: Spinner style (dots, line, arc, etc.)
        
    Yields:
        Status instance for updating spinner text
        
    Example:
        with with_spinner("Checking for updates...") as status:
            # Do some work
            status.update("Downloading...")
            time.sleep(2)
            status.update("Installing...")
            time.sleep(1)
    """
    with get_console().status(text, spinner=spinner) as status:
        yield status


def print_with_style(
    message: str,
    style: str = "white",
    prefix: Optional[str] = None
) -> None:
    """
    Print a message with Rich styling.
    
    Args:
        message: Message to print
        style: Rich style string (e.g., "bold red", "cyan")
        prefix: Optional prefix to add before message
    """
    console = get_console()
    if prefix:
        console.print(f"[{style}]{prefix}[/{style}] {message}")
    else:
        console.print(f"[{style}]{message}[/{style}]")


def clear_screen() -> None:
    """Clear the terminal screen."""
    get_console().clear()


def print_rule(title: str = "", style: str = "white") -> None:
    """
    Print a horizontal rule with optional title.
    
    Args:
        title: Optional title text for the rule
        style: Rich style for the rule
    """
    get_console().rule(title, style=style)