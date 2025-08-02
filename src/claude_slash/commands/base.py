"""
Base command interface for claude-slash CLI commands.

This module defines the BaseCommand abstract base class that all commands
should inherit from to ensure consistent behavior and type safety.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import typer
from rich.console import Console


class BaseCommand(ABC):
    """
    Abstract base class for all claude-slash commands.
    
    This class provides a common interface for command implementation,
    ensuring type safety and consistent behavior across all commands.
    """
    
    def __init__(self):
        """Initialize the base command with a console for output."""
        self.console = Console()
    
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
        def command_wrapper(**kwargs: Any) -> None:
            """Wrapper function to handle command execution with error handling."""
            try:
                self.execute(**kwargs)
            except Exception as e:
                self.console.print(f"[bold red]Error executing {self.name}:[/bold red] {str(e)}")
                raise typer.Exit(1)
        
        # Set the function name and docstring for better help text
        command_wrapper.__name__ = self.name
        command_wrapper.__doc__ = self.help_text
        
        return command_wrapper
    
    def error(self, message: str) -> None:
        """Print an error message and exit."""
        self.console.print(f"[bold red]Error:[/bold red] {message}")
        raise typer.Exit(1)
    
    def success(self, message: str) -> None:
        """Print a success message."""
        self.console.print(f"[bold green]Success:[/bold green] {message}")
    
    def info(self, message: str) -> None:
        """Print an informational message."""
        self.console.print(f"[bold blue]Info:[/bold blue] {message}")
    
    def warning(self, message: str) -> None:
        """Print a warning message."""
        self.console.print(f"[bold yellow]Warning:[/bold yellow] {message}")