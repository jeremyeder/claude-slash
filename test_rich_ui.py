#!/usr/bin/env python3
"""
Test script for Rich UI enhancements.

This script demonstrates the new Rich UI features added to claude-slash commands.
"""

import sys
import time
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from claude_slash.ui import (
    get_console,
    with_progress,
    with_spinner,
    create_status_panel,
    create_info_table,
    format_command_table,
    ProgressManager,
    SpinnerManager,
    track_operation,
    simulate_progress,
)


def test_spinners():
    """Test spinner functionality."""
    console = get_console()
    console.print("[bold blue]Testing Spinners...[/bold blue]")
    
    # Test network spinner
    with SpinnerManager.network_operation("Checking network connection...") as status:
        time.sleep(2)
        status.update("Downloading data...")
        time.sleep(1)
    
    # Test file spinner
    with SpinnerManager.file_operation("Processing files...") as status:
        time.sleep(1.5)
    
    # Test git spinner
    with SpinnerManager.git_operation("Running git operations...") as status:
        time.sleep(1)
    
    console.print("✅ Spinners test completed")
    console.print()


def test_progress_bars():
    """Test progress bar functionality."""
    console = get_console()
    console.print("[bold blue]Testing Progress Bars...[/bold blue]")
    
    # Test simple progress
    simulate_progress("Simple operation", total=50, delay=0.02)
    
    # Test file operation progress
    with track_operation("File operations", total=25, operation_type="file") as (progress, task):
        for i in range(25):
            time.sleep(0.03)
            progress.update(task, advance=1)
    
    console.print("✅ Progress bars test completed")
    console.print()


def test_panels_and_tables():
    """Test panels and tables."""
    console = get_console()
    console.print("[bold blue]Testing Panels and Tables...[/bold blue]")
    
    # Test status panels
    info_panel = create_status_panel(
        "Information",
        "This is an informational message with some details.",
        status="info"
    )
    console.print(info_panel)
    
    success_panel = create_status_panel(
        "Success",
        "Operation completed successfully!",
        status="success"
    )
    console.print(success_panel)
    
    warning_panel = create_status_panel(
        "Warning",
        "This is a warning message that you should pay attention to.",
        status="warning"
    )
    console.print(warning_panel)
    
    # Test info table
    info_data = [
        ("Project", "claude-slash"),
        ("Version", "1.2.1"),
        ("Python", sys.version.split()[0]),
        ("Rich UI", "Enhanced ✨"),
    ]
    info_table = create_info_table(info_data, title="Project Information")
    console.print(info_table)
    
    # Test command table
    commands = [
        {"name": "/slash", "description": "Show help and available commands"},
        {"name": "/learn", "description": "Extract insights from current session"},
        {"name": "/menuconfig", "description": "Interactive configuration menu"},
    ]
    cmd_table = format_command_table(commands, title="Available Commands")
    console.print(cmd_table)
    
    console.print("✅ Panels and tables test completed")
    console.print()


def test_formatting():
    """Test message formatting utilities."""
    from claude_slash.ui.formatting import (
        format_error_message,
        format_success_message,
        format_warning_message,
        format_info_message,
    )
    
    console = get_console()
    console.print("[bold blue]Testing Message Formatting...[/bold blue]")
    
    # Test different message types
    console.print(format_error_message("This is an error", "Additional error details"))
    console.print(format_success_message("Operation successful", "All files processed"))
    console.print(format_warning_message("Potential issue detected", "Please review settings"))
    console.print(format_info_message("Information available", "Check the documentation"))
    
    console.print("✅ Message formatting test completed")
    console.print()


def main():
    """Run all tests."""
    console = get_console()
    
    console.print("[bold green]🎨 Rich UI Enhancement Test Suite[/bold green]")
    console.rule("Starting Tests", style="green")
    console.print()
    
    try:
        test_spinners()
        test_progress_bars()
        test_panels_and_tables()
        test_formatting()
        
        console.rule("All Tests Completed", style="green")
        console.print("[bold green]🎉 All Rich UI features are working correctly![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Test failed:[/bold red] {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())