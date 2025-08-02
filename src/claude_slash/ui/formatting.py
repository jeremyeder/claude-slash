"""
Formatting utilities for consistent Rich output styling.
"""

from typing import List, Dict, Any, Optional, Tuple

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markup import escape

from .console import get_console


def create_status_panel(
    title: str,
    content: str,
    status: str = "info",
    expand: bool = True
) -> Panel:
    """
    Create a status panel with appropriate styling.
    
    Args:
        title: Panel title
        content: Panel content text
        status: Status type (info, success, warning, error)
        expand: Whether panel should expand to full width
        
    Returns:
        Styled Rich Panel
    """
    status_styles = {
        "info": ("blue", "ℹ️"),
        "success": ("green", "✅"), 
        "warning": ("yellow", "⚠️"),
        "error": ("red", "❌"),
    }
    
    style, icon = status_styles.get(status, ("white", ""))
    panel_title = f"{icon} {title}" if icon else title
    
    return Panel(
        content,
        title=panel_title,
        style=style,
        expand=expand
    )


def create_info_table(
    data: List[Tuple[str, str]],
    title: Optional[str] = None,
    show_header: bool = False
) -> Table:
    """
    Create an information table with key-value pairs.
    
    Args:
        data: List of (key, value) tuples
        title: Optional table title
        show_header: Whether to show table headers
        
    Returns:
        Styled Rich Table
    """
    table = Table(show_header=show_header, box=None, title=title)
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    
    for key, value in data:
        table.add_row(key, escape(str(value)))
    
    return table


def format_command_table(
    commands: List[Dict[str, str]],
    title: str = "Available Commands"
) -> Table:
    """
    Create a formatted table for displaying commands.
    
    Args:
        commands: List of command dictionaries with 'name', 'description', etc.
        title: Table title
        
    Returns:
        Styled Rich Table for commands
    """
    table = Table(show_header=True, header_style="bold green", title=title)
    table.add_column("Command", style="cyan", min_width=20)
    table.add_column("Description", style="white")
    
    for cmd in commands:
        name = cmd.get("name", "")
        description = cmd.get("description", "")
        
        # Truncate long descriptions
        if len(description) > 60:
            description = description[:57] + "..."
            
        table.add_row(name, escape(description))
    
    return table


def format_error_message(
    message: str,
    details: Optional[str] = None,
    prefix: str = "Error"
) -> str:
    """
    Format an error message with consistent styling.
    
    Args:
        message: Main error message
        details: Optional detailed error information
        prefix: Error prefix text
        
    Returns:
        Formatted error string with Rich markup
    """
    formatted = f"[bold red]{prefix}:[/bold red] {escape(message)}"
    if details:
        formatted += f"\n[dim red]{escape(details)}[/dim red]"
    return formatted


def format_success_message(
    message: str,
    details: Optional[str] = None,
    prefix: str = "Success"
) -> str:
    """
    Format a success message with consistent styling.
    
    Args:
        message: Main success message
        details: Optional detailed success information
        prefix: Success prefix text
        
    Returns:
        Formatted success string with Rich markup
    """
    formatted = f"[bold green]{prefix}:[/bold green] {escape(message)}"
    if details:
        formatted += f"\n[dim green]{escape(details)}[/dim green]"
    return formatted


def format_warning_message(
    message: str,
    details: Optional[str] = None,
    prefix: str = "Warning"
) -> str:
    """
    Format a warning message with consistent styling.
    
    Args:
        message: Main warning message
        details: Optional detailed warning information
        prefix: Warning prefix text
        
    Returns:
        Formatted warning string with Rich markup
    """
    formatted = f"[bold yellow]{prefix}:[/bold yellow] {escape(message)}"
    if details:
        formatted += f"\n[dim yellow]{escape(details)}[/dim yellow]"
    return formatted


def format_info_message(
    message: str,
    details: Optional[str] = None,
    prefix: str = "Info"
) -> str:
    """
    Format an info message with consistent styling.
    
    Args:
        message: Main info message
        details: Optional detailed information
        prefix: Info prefix text
        
    Returns:
        Formatted info string with Rich markup
    """
    formatted = f"[bold blue]{prefix}:[/bold blue] {escape(message)}"
    if details:
        formatted += f"\n[dim blue]{escape(details)}[/dim blue]"
    return formatted


def create_command_help_panel(
    command_name: str,
    description: str,
    usage: str,
    examples: Optional[List[str]] = None
) -> Panel:
    """
    Create a help panel for a specific command.
    
    Args:
        command_name: Name of the command
        description: Command description
        usage: Usage syntax
        examples: Optional list of usage examples
        
    Returns:
        Rich Panel with formatted help content
    """
    content = f"[bold]{description}[/bold]\n\n"
    content += f"[cyan]Usage:[/cyan]\n{escape(usage)}\n"
    
    if examples:
        content += f"\n[cyan]Examples:[/cyan]\n"
        for i, example in enumerate(examples, 1):
            content += f"{i}. [dim]{escape(example)}[/dim]\n"
    
    return Panel(
        content,
        title=f"📖 Help: {command_name}",
        style="blue",
        expand=False
    )