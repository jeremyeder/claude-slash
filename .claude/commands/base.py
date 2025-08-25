"""
Base command interface for claude-slash CLI commands.

This module defines the BaseCommand abstract base class that all commands
should inherit from to ensure consistent behavior and type safety.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

import typer

from ..ui import (
    format_error_message,
    format_info_message,
    format_success_message,
    format_warning_message,
    get_console,
)


class BaseCommand(ABC):
    """
    Abstract base class for all claude-slash commands.

    This class provides a common interface for command implementation,
    ensuring type safety and consistent behavior across all commands.
    """

    def __init__(self):
        """Initialize the base command with a shared console for output."""
        self.console = get_console()

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the command name for registration."""
        pass

    @property
    @abstractmethod
    def help_text(self) -> str:
        """Return the help text for the command."""
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> None:
        """
        Execute the command with the given arguments.

        Args:
            **kwargs: Command arguments passed from Typer
        """
        pass

    def create_typer_command(self):
        """
        Create a Typer command function for this command.

        This method should be overridden by subclasses that need
        custom argument parsing or command structure.

        Returns:
            A callable function that can be registered with Typer
        """

        def command_wrapper(**kwargs) -> None:
            """Wrapper function to handle command execution."""
            try:
                self.execute(**kwargs)
            except Exception as e:
                self.console.print(
                    f"[bold red]Error executing {self.name}:[/bold red] " f"{str(e)}"
                )
                raise typer.Exit(1)

        # Set the function name and docstring for better help text
        command_wrapper.__name__ = self.name
        command_wrapper.__doc__ = self.help_text

        return command_wrapper

    def error(self, message: str, details: Optional[str] = None) -> None:
        """Print an error message and exit."""
        self.console.print(format_error_message(message, details))
        raise typer.Exit(1)

    def success(self, message: str, details: Optional[str] = None) -> None:
        """Print a success message."""
        self.console.print(format_success_message(message, details))

    def info(self, message: str, details: Optional[str] = None) -> None:
        """Print an informational message."""
        self.console.print(format_info_message(message, details))

    def warning(self, message: str, details: Optional[str] = None) -> None:
        """Print a warning message."""
        self.console.print(format_warning_message(message, details))
