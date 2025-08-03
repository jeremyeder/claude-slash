"""
Example command implementation to demonstrate the command discovery system.

This module provides a simple example command that can be automatically
discovered and registered with the CLI application.
"""

from typing import Any

import typer

from .base import BaseCommand


class ExampleCommand(BaseCommand):
    """
    Example command for testing the command discovery system.
    """

    @property
    def name(self) -> str:
        """Return the command name."""
        return "example"

    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return (
            "Example command to test command discovery system with Rich formatting.\n\n"
            "Examples:\n"
            "  /example                           # Default hello message\n"
            '  /example --message "Custom text"   # Custom message\n'
            "  claude-slash example               # CLI mode\n\n"
            "This command demonstrates:\n"
            "• BaseCommand inheritance\n"
            "• Custom argument handling\n"
            "• Rich-formatted success messages"
        )

    def execute(self, **kwargs: Any) -> None:
        """
        Execute the example command.

        Args:
            **kwargs: Command arguments passed from Typer
        """
        message = kwargs.get("message", "Hello, World!")
        self.success(f"Example command executed with message: {message}")

    def create_typer_command(self):
        """Create a Typer command with custom arguments."""

        def command_wrapper(
            message: str = typer.Option("Hello, World!", help="Message to display")
        ) -> None:
            """Example command to test command discovery system."""
            try:
                self.execute(message=message)
            except Exception as e:
                self.console.print(
                    f"[bold red]Error executing {self.name}:[/bold red] {str(e)}"
                )
                raise typer.Exit(1)

        return command_wrapper
