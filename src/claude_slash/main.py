"""
Main entry point for claude-slash CLI application.

This module provides the primary CLI interface using Typer for command-line
argument parsing and Rich for enhanced terminal output. It includes automatic
command discovery from the commands package.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import List, Type

import typer
from rich.console import Console
from rich.panel import Panel

from .commands.base import BaseCommand

app = typer.Typer(
    name="claude-slash",
    help="Custom slash commands for Claude Code CLI",
    add_completion=False,
)
console = Console()


def discover_commands() -> List[Type[BaseCommand]]:
    """
    Discover all command classes in the commands package.
    
    Returns:
        List of BaseCommand subclasses found in the commands package
    """
    commands = []
    commands_package = "claude_slash.commands"
    
    try:
        # Import the commands package
        package = importlib.import_module(commands_package)
        package_path = Path(package.__file__).parent
        
        # Iterate through all modules in the commands package
        for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
            if name == "base":  # Skip the base module
                continue
                
            try:
                # Import the module
                module_name = f"{commands_package}.{name}"
                module = importlib.import_module(module_name)
                
                # Find all classes that inherit from BaseCommand
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (inspect.isclass(item) and 
                        issubclass(item, BaseCommand) and 
                        item is not BaseCommand):
                        commands.append(item)
                        
            except ImportError as e:
                console.print(f"[yellow]Warning: Could not import command module {name}: {e}[/yellow]")
                continue
                
    except ImportError as e:
        console.print(f"[red]Error: Could not import commands package: {e}[/red]")
    
    return commands


def register_commands() -> None:
    """
    Register all discovered commands with the Typer app.
    """
    discovered_commands = discover_commands()
    
    for command_class in discovered_commands:
        try:
            # Instantiate the command
            command_instance = command_class()
            
            # Create the Typer command function
            command_func = command_instance.create_typer_command()
            
            # Register the command with the app
            app.command(name=command_instance.name, help=command_instance.help_text)(command_func)
            
        except Exception as e:
            console.print(f"[red]Error registering command {command_class.__name__}: {e}[/red]")


@app.command()
def version():
    """Show version information."""
    try:
        from . import __version__
        version_str = f"claude-slash v{__version__}"
    except ImportError:
        version_str = "claude-slash (version unknown)"
    
    console.print(
        Panel(
            version_str,
            title="Version",
            style="bold blue",
        )
    )


@app.command()
def checkpoint(name: str = typer.Argument(None, help="Checkpoint name")):
    """Create a session checkpoint."""
    console.print(
        Panel(
            f"Creating checkpoint: {name or 'auto'}",
            title="Checkpoint",
            style="bold green",
        )
    )
    # TODO: Implement checkpoint functionality


@app.command()
def restore(name: str = typer.Argument(None, help="Checkpoint name to restore")):
    """Restore from a session checkpoint."""
    console.print(
        Panel(
            f"Restoring checkpoint: {name or 'latest'}",
            title="Restore",
            style="bold yellow",
        )
    )
    # TODO: Implement restore functionality


# Register discovered commands when the module is imported
register_commands()


if __name__ == "__main__":
    app()