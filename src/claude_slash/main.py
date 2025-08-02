"""
Main entry point for claude-slash CLI application.

This module provides the primary CLI interface using Typer for command-line
argument parsing and Rich for enhanced terminal output.
"""

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="claude-slash",
    help="Custom slash commands for Claude Code CLI",
    add_completion=False,
)
console = Console()


@app.command()
def version():
    """Show version information."""
    from . import __version__
    
    console.print(
        Panel(
            f"claude-slash v{__version__}",
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


if __name__ == "__main__":
    app()