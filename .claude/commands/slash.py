"""
Slash command implementation providing help display and update functionality.

This module provides the main slash command that:
- Displays help and available commands (default behavior)
- Updates local claude-slash commands to the latest release
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from ..ui import SpinnerManager, track_operation
from .base import BaseCommand


class SlashCommand(BaseCommand):
    """
    Main slash command providing help display and update functionality.
    """

    @property
    def name(self) -> str:
        """Return the command name."""
        return "slash"

    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return (
            "Display Rich-formatted help with all available commands, or update "
            "to the latest release with progress tracking.\n\n"
            "Examples:\n"
            "  /slash              # Show help with all commands\n"
            "  /slash update       # Update to latest release\n"
            "  claude-slash slash  # Show help (CLI mode)"
        )

    def execute(self, **kwargs: Any) -> None:
        """
        Execute the slash command.

        Args:
            **kwargs: Command arguments passed from Typer
        """
        subcommand = kwargs.get("subcommand")

        if subcommand == "update":
            self._handle_update()
        else:
            self._handle_help()

    def create_typer_command(self):
        """Create a Typer command with custom arguments."""

        def command_wrapper(
            subcommand: Optional[str] = typer.Argument(
                None, help="Subcommand: help (default) or update"
            )
        ) -> None:
            """Show help and available commands or update to latest release."""
            try:
                self.execute(subcommand=subcommand)
            except Exception as e:
                self.console.print(
                    f"[bold red]Error executing {self.name}:[/bold red] {str(e)}"
                )
                raise typer.Exit(1)

        return command_wrapper

    def _handle_help(self) -> None:
        """Handle the help subcommand (default behavior)."""
        self.console.print(
            Panel(
                "[bold blue]📋 Available Claude Slash Commands[/bold blue]",
                style="blue",
            )
        )

        # Get the commands directory
        commands_dir = self._find_commands_directory()
        if not commands_dir:
            self.error(
                "❌ No claude-slash commands found\n"
                "Install commands by downloading and running install.sh from:\n"
                "https://github.com/jeremyeder/claude-slash"
            )
            return

        self.console.print(f"[cyan]Commands installed in: {commands_dir}[/cyan]")
        self.console.print()

        # Create a table for commands
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Command", style="cyan")
        table.add_column("Description")

        # Process all command files
        command_files = list(Path(commands_dir).glob("*.md"))
        if not command_files:
            self.warning("No command files found in commands directory")
            return

        for cmd_file in sorted(command_files):
            filename = cmd_file.stem

            # Skip this help command to avoid recursion
            if filename == "slash":
                continue

            description = self._extract_description(cmd_file)
            usage = self._extract_usage(cmd_file)

            # Format the command name
            if usage:
                cmd_display = usage
            else:
                cmd_display = f"/{filename}"

            # Truncate description if too long
            if len(description) > 60:
                description = description[:57] + "..."

            table.add_row(cmd_display, description)

        self.console.print(table)
        self.console.print()

        # Print tips
        tips_panel = Panel(
            "[yellow]💡 Tips:[/yellow]\n"
            "• Type any command above to use it\n"
            "• Use /learn to extract insights from your current session\n"
            "• Use /slash update to get the latest commands",
            style="yellow",
        )
        self.console.print(tips_panel)

        self.console.print()
        self.console.print(
            "[blue]📖 For more information visit:[/blue] https://github.com/jeremyeder/claude-slash"
        )

    def _handle_update(self) -> None:
        """Handle the update subcommand."""
        self.console.print("🔄 Updating claude-slash commands...")
        self.console.print()

        # Determine installation location
        install_dir, install_type = self._detect_installation()
        if not install_dir:
            self.error(
                "❌ No claude-slash installation found\n"
                "Run the installer first:\n"
                "curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh -o install.sh && bash install.sh"
            )
            return

        self.console.print(f"📍 Found {install_type} installation at: {install_dir}")

        # Check for latest release using gh CLI with spinner
        with SpinnerManager.network_operation(
            "🔍 Checking for latest release..."
        ) as status:
            try:
                result = subprocess.run(
                    ["gh", "api", "repos/jeremyeder/claude-slash/releases/latest"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                latest_info = json.loads(result.stdout)
                latest_tag = latest_info.get("tag_name")

                if not latest_tag:
                    self.error("❌ Could not determine latest version")
                    return

            except subprocess.CalledProcessError:
                self.error(
                    "❌ Failed to check for updates (network error or gh CLI not available)"
                )
                return
            except json.JSONDecodeError:
                self.error("❌ Failed to parse release information")
                return

        self.console.print(f"📦 Latest release: {latest_tag}")

        # Create backup
        backup_dir = f"{install_dir}.backup.{self._get_timestamp()}"
        self.console.print(f"💾 Creating backup at: {backup_dir}")
        try:
            shutil.copytree(install_dir, backup_dir)
        except Exception as e:
            self.error(f"❌ Failed to create backup: {e}")
            return

        # Download and extract latest release using gh CLI with progress tracking
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Download the tarball using gh CLI with spinner
                with SpinnerManager.network_operation(
                    "⬇️ Downloading latest release..."
                ):
                    tarball_path = os.path.join(temp_dir, "claude-slash.tar.gz")
                    subprocess.run(
                        [
                            "gh",
                            "api",
                            f"repos/jeremyeder/claude-slash/tarball/{latest_tag}",
                        ],
                        stdout=open(tarball_path, "wb"),
                        check=True,
                    )

                # Extract the tarball with spinner
                with SpinnerManager.file_operation(
                    "📦 Extracting release..."
                ):
                    subprocess.run(
                        [
                            "tar",
                            "-xz",
                            "-C",
                            temp_dir,
                            "--strip-components=1",
                            "-f",
                            tarball_path,
                        ],
                        check=True,
                    )

                # Update commands with progress
                commands_source = os.path.join(temp_dir, ".claude", "commands")
                if os.path.isdir(commands_source):
                    # Count files for progress tracking
                    old_files = list(Path(install_dir).glob("*.md"))
                    new_files = list(Path(commands_source).glob("*.md"))
                    total_operations = len(old_files) + len(new_files)

                    with track_operation(
                        "🔄 Updating commands...",
                        total=total_operations,
                        operation_type="file",
                    ) as (progress, task):
                        # Remove old commands
                        for md_file in old_files:
                            md_file.unlink()
                            progress.update(task, advance=1)

                        # Copy new commands
                        for md_file in new_files:
                            shutil.copy2(md_file, install_dir)
                            progress.update(task, advance=1)

                    self.console.print("✅ Update completed successfully!")
                    self.console.print(f"📦 Updated to: {latest_tag}")
                    self.console.print(f"📁 Backup saved to: {backup_dir}")
                    self.console.print(f"🗑️  Remove backup with: rm -rf {backup_dir}")
                else:
                    self.error("❌ Downloaded release doesn't contain command files")
                    # Restore from backup
                    self.console.print("🔄 Restoring from backup...")
                    shutil.rmtree(install_dir)
                    shutil.move(backup_dir, install_dir)
                    return

            except subprocess.CalledProcessError as e:
                self.error(f"❌ Failed to download release: {e}")
                # Restore from backup
                self.console.print("🔄 Restoring from backup...")
                shutil.rmtree(install_dir)
                shutil.move(backup_dir, install_dir)
                return
            except Exception as e:
                self.error(f"❌ Failed to update commands: {e}")
                # Restore from backup
                self.console.print("🔄 Restoring from backup...")
                shutil.rmtree(install_dir)
                shutil.move(backup_dir, install_dir)
                return

        self.console.print()
        self.console.print("🎉 claude-slash commands updated successfully!")

    def _find_commands_directory(self) -> Optional[str]:
        """Find the commands directory (project or global)."""
        # Try to get git root first
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            git_root = result.stdout.strip()
            commands_dir = os.path.join(git_root, ".claude", "commands")
            if os.path.isdir(commands_dir):
                return commands_dir
        except subprocess.CalledProcessError:
            pass

        # Fall back to current directory
        commands_dir = os.path.join(os.getcwd(), ".claude", "commands")
        if os.path.isdir(commands_dir):
            return commands_dir

        # Try global installation
        global_dir = os.path.join(os.path.expanduser("~"), ".claude", "commands")
        if os.path.isdir(global_dir):
            return global_dir

        return None

    def _detect_installation(self) -> tuple[Optional[str], str]:
        """
        Detect installation type and location.

        Returns:
            Tuple of (install_dir, install_type) or (None, "") if not found
        """
        # Check project installation
        project_dir = os.path.join(os.getcwd(), ".claude", "commands")
        if os.path.isdir(project_dir):
            return project_dir, "project"

        # Check global installation
        global_dir = os.path.join(os.path.expanduser("~"), ".claude", "commands")
        if os.path.isdir(global_dir):
            return global_dir, "global"

        return None, ""

    def _extract_description(self, file_path: Path) -> str:
        """
        Extract command description from markdown file.

        Args:
            file_path: Path to the markdown command file

        Returns:
            Extracted description or default text
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Try to get the first line after the title that contains descriptive text
            if len(lines) >= 3:
                description = lines[2].strip()
                if description and len(description) >= 10:
                    return description

            # If that's empty or too short, look for the Description section
            in_description = False
            for line in lines:
                line = line.strip()
                if line.startswith("## Description"):
                    in_description = True
                    continue
                if in_description and line.startswith("##"):
                    break
                if in_description and line and not line.startswith("#"):
                    return line[:80]

            # Fallback to a generic description
            return "Custom claude-slash command"

        except Exception:
            return "Custom claude-slash command"

    def _extract_usage(self, file_path: Path) -> str:
        """
        Extract usage from markdown file.

        Args:
            file_path: Path to the markdown command file

        Returns:
            Extracted usage string or empty string
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for usage in code blocks
            lines = content.split("\n")
            in_code_block = False
            for line in lines:
                line = line.strip()
                if line.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block and line.startswith("/"):
                    return line

            return ""

        except Exception:
            return ""

    def _get_timestamp(self) -> str:
        """Get a timestamp string for backup directories."""
        import datetime

        return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
