"""
Bookmark command for managing project-specific bookmarks.

This module provides a lightweight bookmark management system that automatically
categorizes bookmarks into URLs, Notes, and Code Snippets, with persistent storage
in .claude/BOOKMARKS.md.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from base import BaseCommand
from rich.panel import Panel


class BookmarkCommand(BaseCommand):
    """
    Bookmark Management System for Claude Code projects.

    Manages project-specific bookmarks with automatic categorization,
    global sequential numbering, and persistent storage.
    """

    @property
    def name(self) -> str:
        """Return the command name for registration."""
        return "bookmark"

    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return (
            "Manage project-specific bookmarks with automatic categorization.\n\n"
            "Usage:\n"
            "  /bookmark add <text>      # Add a bookmark\n"
            "  /bookmark -a <text>       # Add a bookmark (short form)\n"
            "  /bookmark list            # List all bookmarks\n"
            "  /bookmark -l              # List all bookmarks (short form)\n"
            "  /bookmark remove <index>  # Remove bookmark by index\n"
            "  /bookmark -r <index>      # Remove bookmark by index (short form)\n"
            "  /bookmark -h              # Show this help\n\n"
            "Features:\n"
            "• Auto-categorization (URLs, Notes, Code Snippets)\n"
            "• Global sequential numbering\n"
            "• Persistent storage in .claude/BOOKMARKS.md\n"
            "• Automatic renumbering on removal"
        )

    def __init__(self):
        """Initialize the bookmark command."""
        super().__init__()
        self.bookmarks_dir = Path.cwd() / ".claude"
        self.bookmarks_file = self.bookmarks_dir / "BOOKMARKS.md"
        self.claude_md_file = Path.cwd() / "CLAUDE.md"

    def execute(self, args: Optional[str] = None, **kwargs) -> None:
        """
        Execute the bookmark command with the given arguments.

        Args:
            args: Command line arguments as a string
            **kwargs: Additional keyword arguments
        """
        # Parse arguments
        if not args or args in ["-h", "--help"]:
            self._show_help()
            return

        parts = args.split(maxsplit=1)
        operation = parts[0]

        # Determine operation
        if operation in ["add", "-a"]:
            if len(parts) < 2:
                self.error("Specify text to bookmark: /bookmark add <text>")
                return
            self._add_bookmark(parts[1])
        elif operation in ["list", "-l"]:
            self._list_bookmarks()
        elif operation in ["remove", "-r"]:
            if len(parts) < 2:
                self.error("Specify index to remove: /bookmark -r <number>")
                return
            try:
                index = int(parts[1])
                self._remove_bookmark(index)
            except ValueError:
                self.error("Invalid index. Use: /bookmark -r <number>")
        else:
            self.error(
                f"Unknown operation: {operation}\n"
                "Use: /bookmark add|list|remove or -a|-l|-r\n\n"
                "Run '/bookmark -h' for help"
            )

    def _show_help(self) -> None:
        """Display help information."""
        help_text = """[bold]📚 Bookmark Management[/bold]

[yellow]USAGE:[/yellow]
  /bookmark add <text>          Add a bookmark
  /bookmark -a <text>           Add a bookmark (short form)
  /bookmark list                List all bookmarks
  /bookmark -l                  List all bookmarks (short form)
  /bookmark remove <index>      Remove bookmark by index
  /bookmark -r <index>          Remove bookmark by index (short form)
  /bookmark -h                  Show this help

[yellow]EXAMPLES:[/yellow]
  /bookmark add https://docs.example.com/api - API docs
  /bookmark -a Remember to use the Xcode simulator
  /bookmark add pytest tests/ -v --cov=src
  /bookmark list
  /bookmark -l
  /bookmark remove 5
  /bookmark -r 3

[yellow]STORAGE:[/yellow]
  Bookmarks are stored in .claude/BOOKMARKS.md
  Auto-loaded via reference in CLAUDE.md
  Committed to repo by default for team sharing

[yellow]CATEGORIES:[/yellow]
  URLs, Notes, and Code Snippets are auto-detected"""

        self.console.print(Panel(help_text, expand=False))

    def _categorize_bookmark(self, text: str) -> str:
        """
        Categorize a bookmark based on its content.

        Args:
            text: The bookmark text

        Returns:
            Category name: "URLs", "Notes", or "Code Snippets"
        """
        # Check for URLs
        if text.startswith(("http://", "https://", "www.")):
            return "URLs"

        # Check for code snippets
        code_patterns = ["pytest", "npm", "git", "python", "bash", "`", "|", "&&", "./"]
        if any(pattern in text for pattern in code_patterns):
            return "Code Snippets"

        # Default to Notes
        return "Notes"

    def _initialize_bookmarks(self) -> None:
        """Initialize the bookmarks system if needed."""
        # Create .claude directory if it doesn't exist
        self.bookmarks_dir.mkdir(exist_ok=True)

        # Create BOOKMARKS.md if it doesn't exist
        if not self.bookmarks_file.exists():
            today = datetime.now().strftime("%Y-%m-%d")
            template = f"""# Project Bookmarks

*Last updated: {today}*

## URLs

## Notes

## Code Snippets
"""
            self.bookmarks_file.write_text(template)

        # Add reference to CLAUDE.md if it doesn't exist
        if self.claude_md_file.exists():
            claude_content = self.claude_md_file.read_text()
            if (
                "BOOKMARKS" not in claude_content
                and ".claude/BOOKMARKS.md" not in claude_content
            ):
                reference = """

## Project Bookmarks
See `.claude/BOOKMARKS.md` for project-specific URLs and notes.
"""
                self.claude_md_file.write_text(claude_content + reference)
        else:
            # Create CLAUDE.md with bookmark reference
            today = datetime.now().strftime("%Y-%m-%d")
            template = f"""# Project Configuration

*Created: {today}*

## Project Bookmarks
See `.claude/BOOKMARKS.md` for project-specific URLs and notes.
"""
            self.claude_md_file.write_text(template)

    def _parse_bookmarks(self) -> Tuple[dict, int]:
        """
        Parse existing bookmarks from the file.

        Returns:
            Tuple of (bookmarks_dict, max_index)
        """
        if not self.bookmarks_file.exists():
            return {}, 0

        content = self.bookmarks_file.read_text()
        bookmarks = {"URLs": [], "Notes": [], "Code Snippets": []}
        current_category = None
        max_index = 0

        for line in content.split("\n"):
            # Check for category headers
            if line.startswith("## "):
                category = line[3:].strip()
                if category in bookmarks:
                    current_category = category
                continue

            # Parse bookmark lines
            if current_category and line.strip():
                match = re.match(r"^(\d+)\.\s+(.+)$", line.strip())
                if match:
                    index = int(match.group(1))
                    text = match.group(2)
                    bookmarks[current_category].append((index, text))
                    max_index = max(max_index, index)

        return bookmarks, max_index

    def _add_bookmark(self, text: str) -> None:
        """
        Add a new bookmark.

        Args:
            text: The bookmark text
        """
        # Initialize if needed
        self._initialize_bookmarks()

        # Determine category
        category = self._categorize_bookmark(text)

        # Parse existing bookmarks
        bookmarks, max_index = self._parse_bookmarks()

        # Calculate new index
        new_index = max_index + 1

        # Add to category
        bookmarks[category].append((new_index, text))

        # Write updated bookmarks
        self._write_bookmarks(bookmarks)

        # Show success message
        self.success(f"Added bookmark #{new_index} to {category} category")

        # Show security tip on first bookmark
        if new_index == 1:
            self.info(
                "💡 Tip: Avoid storing credentials directly. "
                "Use references like 'API key in 1Password'"
            )

    def _list_bookmarks(self) -> None:
        """List all bookmarks."""
        if not self.bookmarks_file.exists():
            self.console.print("No bookmarks yet. Add one with: /bookmark <text>")
            return

        bookmarks, _ = self._parse_bookmarks()

        # Count total bookmarks
        total = sum(len(items) for items in bookmarks.values())

        if total == 0:
            self.console.print("No bookmarks yet. Add one with: /bookmark <text>")
            return

        # Display bookmarks
        self.console.print(f"\n[bold]📚 Project Bookmarks[/bold] ({total} total):\n")

        for category in ["URLs", "Notes", "Code Snippets"]:
            items = bookmarks[category]
            self.console.print(f"[yellow]{category}[/yellow] ({len(items)}):")
            if items:
                for index, text in items:
                    self.console.print(f"  {index}. {text}")
            else:
                self.console.print("  [dim](none)[/dim]")
            self.console.print()

    def _remove_bookmark(self, index: int) -> None:
        """
        Remove a bookmark by index.

        Args:
            index: The bookmark index to remove
        """
        if not self.bookmarks_file.exists():
            self.error("No bookmarks to remove")
            return

        if index <= 0:
            self.error("Invalid index. Use: /bookmark -r <number>")
            return

        # Parse existing bookmarks
        bookmarks, _ = self._parse_bookmarks()

        # Find and remove the bookmark
        removed_text = None
        for category in bookmarks:
            for i, (idx, text) in enumerate(bookmarks[category]):
                if idx == index:
                    removed_text = text
                    bookmarks[category].pop(i)
                    break
            if removed_text:
                break

        if not removed_text:
            self.error(
                f"Bookmark #{index} not found. " "Use /bookmark -l to see all bookmarks"
            )
            return

        # Renumber all bookmarks sequentially
        renumbered = {"URLs": [], "Notes": [], "Code Snippets": []}
        new_index = 1
        for category in ["URLs", "Notes", "Code Snippets"]:
            for _, text in bookmarks[category]:
                renumbered[category].append((new_index, text))
                new_index += 1

        # Write updated bookmarks
        self._write_bookmarks(renumbered)

        # Calculate remaining count
        remaining = sum(len(items) for items in renumbered.values())

        # Show success message
        self.success(f'Removed bookmark #{index}: "{removed_text}"')
        self.console.print(f"{remaining} bookmark(s) remaining")

    def _write_bookmarks(self, bookmarks: dict) -> None:
        """
        Write bookmarks to the file.

        Args:
            bookmarks: Dictionary of categorized bookmarks
        """
        today = datetime.now().strftime("%Y-%m-%d")
        lines = [
            "# Project Bookmarks",
            "",
            f"*Last updated: {today}*",
            "",
        ]

        for category in ["URLs", "Notes", "Code Snippets"]:
            lines.append(f"## {category}")
            lines.append("")
            for index, text in bookmarks[category]:
                lines.append(f"{index}. {text}")
            lines.append("")

        self.bookmarks_file.write_text("\n".join(lines))


# Command instance for registration
command = BookmarkCommand()
