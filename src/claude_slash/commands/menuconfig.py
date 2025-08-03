#!/usr/bin/env python3
"""
CLAUDE.md Menuconfig Command

Interactive text-based configuration interface for CLAUDE.md files,
inspired by Linux kernel menuconfig. Integrated with the new Typer-based CLI framework.
"""

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

import typer
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Static,
    Tree,
)

from .base import BaseCommand


@dataclass
class Section:
    """Represents a section in CLAUDE.md"""

    level: int  # 1 for #, 2 for ##, 3 for ###
    title: str
    line_start: int
    line_end: int
    enabled: bool = True
    children: List["Section"] = field(default_factory=list)
    parent: Optional["Section"] = None
    content_lines: List[str] = field(default_factory=list)

    def __hash__(self):
        """Make Section hashable by using immutable attributes"""
        return hash((self.level, self.title, self.line_start))

    def __eq__(self, other):
        """Define equality for sections"""
        if not isinstance(other, Section):
            return False
        return (
            self.level == other.level
            and self.title == other.title
            and self.line_start == other.line_start
        )

    @property
    def full_title(self) -> str:
        prefix = "#" * self.level
        return f"{prefix} {self.title}"

    @property
    def indent_level(self) -> int:
        return max(0, self.level - 1)


class CLAUDEParser:
    """Parse CLAUDE.md files into hierarchical sections"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lines = []
        self.sections = []

    def parse(self) -> List[Section]:
        """Parse the CLAUDE.md file and return sections"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as f:
            self.lines = f.readlines()

        self.sections = []
        current_sections = []  # Stack to track hierarchy
        in_code_block = False

        for i, line in enumerate(self.lines):
            # Track code blocks to avoid parsing headers inside them
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Skip headers inside code blocks
            if in_code_block:
                continue

            header_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                # Close any sections at same or higher level
                while current_sections and current_sections[-1].level >= level:
                    section = current_sections.pop()
                    section.line_end = i - 1

                # Create new section
                section = Section(
                    level=level,
                    title=title,
                    line_start=i,
                    line_end=len(self.lines) - 1,  # Will be updated when section ends
                )

                # Set parent relationship
                if current_sections:
                    section.parent = current_sections[-1]
                    current_sections[-1].children.append(section)
                else:
                    self.sections.append(section)

                current_sections.append(section)

        # Close remaining sections
        for section in current_sections:
            section.line_end = len(self.lines) - 1

        # Extract content for each section
        self._extract_content()

        return self.sections

    def _extract_content(self):
        """Extract content lines for each section"""
        all_sections = self._flatten_sections(self.sections)

        for section in all_sections:
            start = section.line_start
            end = section.line_end + 1

            # Find the actual content end (next section start)
            for other in all_sections:
                if other.line_start > start and other.line_start < end:
                    end = other.line_start
                    break

            section.content_lines = self.lines[start:end]
            section.line_end = end - 1

    def _flatten_sections(self, sections: List[Section]) -> List[Section]:
        """Flatten nested sections into a single list"""
        result = []
        for section in sections:
            result.append(section)
            result.extend(self._flatten_sections(section.children))
        return result


class HelpScreen(ModalScreen):
    """Help screen showing keyboard shortcuts"""

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("q", "close", "Close"),
    ]

    def compose(self) -> ComposeResult:
        help_text = """
┌─ CLAUDE.md Menuconfig Help ─────────────────────────────────────────┐
│                                                                     │
│ Navigation:                                                         │
│   ↑/↓, j/k       Navigate through sections                         │
│   →/←, l/h       Expand/collapse sections                          │
│   Enter          Expand/collapse sections                          │
│   Home/End       Go to first/last item                             │
│                                                                     │
│ Actions:                                                            │
│   Space          Toggle section enabled/disabled                   │
│   s              Save configuration                                 │
│   /              Search sections                                    │
│   ?              Show this help                                     │
│   q, Escape      Exit (prompts to save if modified)                │
│                                                                     │
│ Section States:                                                     │
│   [*]            Section enabled (will be included)                │
│   [ ]            Section disabled (will be excluded)               │
│   --->           Section has subsections                           │
│                                                                     │
│ Features:                                                           │
│   • Hierarchical section management                                │
│   • Automatic backup creation                                      │
│   • Search functionality                                           │
│   • Linux kernel menuconfig-inspired interface                    │
│                                                                     │
│ Press Escape or 'q' to close this help screen.                     │
└─────────────────────────────────────────────────────────────────────┘
        """

        yield Container(Static(help_text, id="help-text"), id="help-container")

    def action_close(self) -> None:
        self.dismiss()


class SearchScreen(ModalScreen):
    """Search screen for finding sections"""

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("enter", "search", "Search"),
    ]

    def __init__(self, sections: List[Section]):
        super().__init__()
        self.sections = sections

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Search sections:", id="search-label"),
            Input(placeholder="Enter search term...", id="search-input"),
            Horizontal(
                Button("Search", variant="primary", id="search-btn"),
                Button("Cancel", variant="default", id="cancel-btn"),
                id="search-buttons",
            ),
            id="search-container",
        )

    def on_mount(self) -> None:
        self.query_one("#search-input").focus()

    def action_close(self) -> None:
        self.dismiss(None)

    def action_search(self) -> None:
        search_term = self.query_one("#search-input").value.lower()
        if search_term:
            # Find matching sections
            matches = []
            all_sections = self._flatten_sections(self.sections)
            for section in all_sections:
                if search_term in section.title.lower():
                    matches.append(section)
            self.dismiss(matches)
        else:
            self.dismiss(None)

    @on(Button.Pressed, "#search-btn")
    def on_search_button(self) -> None:
        self.action_search()

    @on(Button.Pressed, "#cancel-btn")
    def on_cancel_button(self) -> None:
        self.action_close()

    def _flatten_sections(self, sections: List[Section]) -> List[Section]:
        """Flatten nested sections into a single list"""
        result = []
        for section in sections:
            result.append(section)
            result.extend(self._flatten_sections(section.children))
        return result


class MenuconfigTree(Tree):
    """Custom tree widget for menuconfig interface"""

    class SectionToggled(Message):
        """Message sent when a section is toggled"""

        def __init__(self, section: Section) -> None:
            self.section = section
            super().__init__()

    def __init__(self, sections: List[Section], **kwargs):
        super().__init__("CLAUDE.md Configuration", **kwargs)
        self.sections = sections
        self.section_nodes = {}  # Map section to tree node
        self._build_tree()

    def _build_tree(self):
        """Build the tree from sections"""

        def add_section(section: Section, parent_node):
            state_char = "*" if section.enabled else " "
            subsection_indicator = " --->" if section.children else ""

            label = f"[{state_char}] {section.title}{subsection_indicator}"
            node = parent_node.add(label, data=section)
            self.section_nodes[section] = node

            # Add children
            for child in section.children:
                add_section(child, node)

        # Add root sections
        for section in self.sections:
            add_section(section, self.root)

        # Expand root
        self.root.expand()

    def update_section_label(self, section: Section):
        """Update the label for a section after toggle"""
        if section in self.section_nodes:
            node = self.section_nodes[section]
            state_char = "*" if section.enabled else " "
            subsection_indicator = " --->" if section.children else ""
            node.label = f"[{state_char}] {section.title}{subsection_indicator}"

    def action_toggle_section(self) -> None:
        """Toggle the currently selected section"""
        if self.cursor_node and self.cursor_node.data:
            section = self.cursor_node.data
            section.enabled = not section.enabled
            self.update_section_label(section)
            self.post_message(self.SectionToggled(section))


class MenuconfigApp(App):
    """Main menuconfig application"""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        height: 100%;
    }

    #tree-container {
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }

    #status-bar {
        height: 3;
        background: $primary;
        color: $text;
        padding: 1;
    }

    MenuconfigTree {
        height: 1fr;
    }

    #help-container {
        align: center middle;
        width: 80;
        height: 30;
        background: $surface;
        border: solid $primary;
    }

    #help-text {
        color: $text;
        margin: 1;
    }

    #search-container {
        align: center middle;
        width: 60;
        height: 10;
        background: $surface;
        border: solid $primary;
        padding: 1;
    }

    #search-label {
        margin-bottom: 1;
    }

    #search-input {
        margin-bottom: 1;
    }

    #search-buttons {
        align: center middle;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("s", "save", "Save"),
        Binding("d", "debug_msg", "Debug"),
        Binding("question_mark", "help", "Help", key_display="?"),
        Binding("slash", "search", "Search", key_display="/"),
        Binding("space", "toggle", "Toggle"),
    ]

    modified = reactive(False)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = Path(file_path)
        self.parser = CLAUDEParser(file_path)
        self.sections = []
        self.original_content = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("CLAUDE.md Menuconfig - Loading...", id="loading-message"),
            id="main-container",
        )
        yield Container(
            Static(self._get_status_text(), id="status-text"), id="status-bar"
        )
        yield Footer()

    async def on_mount(self) -> None:
        """Load and parse the CLAUDE.md file"""
        try:
            # Read original content for backup
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.original_content = f.read()

            # Parse sections
            self.sections = self.parser.parse()

            # Replace loading message with tree
            main_container = self.query_one("#main-container")
            main_container.remove_children()

            if self.sections:
                tree = MenuconfigTree(self.sections, id="config-tree")
                tree_container = Container(tree, id="tree-container")
                main_container.mount(tree_container)
            else:
                main_container.mount(
                    Static("No sections found in CLAUDE.md file", id="no-sections")
                )

            self._update_status()

        except Exception as e:
            self.exit(f"Error loading {self.file_path}: {e}")

    def _get_status_text(self) -> str:
        """Get status bar text"""
        modified_text = " [MODIFIED]" if self.modified else ""
        sections_text = (
            f" | {len(self.sections)} sections loaded"
            if hasattr(self, "sections")
            else ""
        )
        return f"File: {self.file_path}{modified_text}{sections_text} | Use arrow keys to navigate, Space to toggle, 's' to save, '?' for help"

    def _update_status(self) -> None:
        """Update status bar"""
        try:
            status = self.query_one("#status-text", Static)
            status.update(self._get_status_text())
        except Exception:
            # Status bar might not exist yet during startup
            pass

    def action_toggle(self) -> None:
        """Toggle current section"""
        tree = self.query_one("#config-tree", MenuconfigTree)
        tree.action_toggle_section()

    def action_help(self) -> None:
        """Show help screen"""
        self.push_screen(HelpScreen())

    def action_search(self) -> None:
        """Show search screen"""

        def handle_search_result(matches):
            if matches:
                # Focus on first match
                tree = self.query_one("#config-tree", MenuconfigTree)
                first_match = matches[0]
                if first_match in tree.section_nodes:
                    tree.select_node(tree.section_nodes[first_match])

        self.push_screen(SearchScreen(self.sections), handle_search_result)

    def action_save(self) -> None:
        """Save configuration to file"""
        try:
            self._save_configuration()
            self.modified = False
            self._update_status()
            self.notify("Configuration saved successfully!")
        except Exception as e:
            self.notify(f"Error saving: {e}", severity="error")

    def action_debug_msg(self) -> None:
        """Debug message"""
        print("Debug: 'd' key pressed - app is running!")

    def action_quit(self) -> None:
        """Quit application"""
        if self.modified:
            # TODO: Add confirmation dialog
            pass
        self.exit()

    def on_menuconfig_tree_section_toggled(
        self, message: MenuconfigTree.SectionToggled
    ) -> None:
        """Handle section toggle"""
        self.modified = True
        self._update_status()

    def _save_configuration(self) -> None:
        """Save the current configuration to CLAUDE.md"""
        # Create backup
        backup_path = self.file_path.with_suffix(".md.menuconfig.bak")
        shutil.copy2(self.file_path, backup_path)

        # Generate new content
        new_content = self._generate_content()

        # Write to file
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    def _generate_content(self) -> str:
        """Generate CLAUDE.md content based on enabled sections"""
        lines = []

        def add_section(section: Section, content_lines: List[str]):
            if section.enabled:
                # Add section header
                lines.append(section.full_title + "\n")

                # Add section content (excluding the header line and subsequent headers)
                for i, line in enumerate(section.content_lines[1:], 1):
                    # Skip if this line is a header that starts another section
                    if re.match(r"^#{1,6}\s+", line.strip()):
                        continue
                    lines.append(line)

                # Add enabled children
                for child in section.children:
                    add_section(child, content_lines)

        # Process all root sections
        for section in self.sections:
            add_section(section, self.parser.lines)

        return "".join(lines)


class MenuconfigCommand(BaseCommand):
    """
    Interactive text-based configuration interface for CLAUDE.md files,
    inspired by Linux kernel menuconfig.
    """

    @property
    def name(self) -> str:
        """Return the command name."""
        return "menuconfig"

    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return (
            "Interactive menuconfig-style TUI editor for CLAUDE.md files with "
            "Linux kernel menuconfig look and feel.\n\n"
            "Examples:\n"
            "  /menuconfig                        # Edit project/global CLAUDE.md\n"
            "  /menuconfig custom.md              # Edit specific file\n"
            "  claude-slash menuconfig            # CLI mode\n\n"
            "Features:\n"
            "• Linux kernel menuconfig-inspired interface\n"
            "• Navigate sections with keyboard shortcuts\n"
            "• Toggle sections enabled/disabled\n"
            "• Real-time preview and editing"
        )

    def execute(self, **kwargs: Any) -> None:
        """
        Execute the menuconfig command.

        Args:
            **kwargs: Command arguments passed from Typer
        """
        file_path = kwargs.get("file")

        # Determine target CLAUDE.md file
        if file_path:
            claude_file = Path(file_path)
        else:
            # Default to project CLAUDE.md, fallback to global
            git_root = self._get_git_root()
            project_file = git_root / "CLAUDE.md"
            global_file = Path.home() / ".claude" / "CLAUDE.md"

            if project_file.exists():
                claude_file = project_file
            elif global_file.exists():
                claude_file = global_file
            else:
                self.error(
                    f"CLAUDE.md file not found. Checked:\n  - Project: {project_file}\n  - Global: {global_file}"
                )
                return

        # Ensure the target file exists
        if not claude_file.exists():
            self.error(f"CLAUDE.md file not found at: {claude_file}")
            return

        self.info(f"Starting CLAUDE.md menuconfig for: {claude_file}")

        # Run the menuconfig interface
        app = MenuconfigApp(str(claude_file))
        app.run()

    def create_typer_command(self):
        """Create a Typer command with custom arguments."""

        def command_wrapper(
            file: Optional[str] = typer.Argument(
                None,
                help="Path to CLAUDE.md file (defaults to project or global CLAUDE.md)",
            )
        ) -> None:
            """Interactive menuconfig-style editor for CLAUDE.md files with Linux kernel menuconfig look and feel."""
            try:
                self.execute(file=file)
            except Exception as e:
                self.console.print(
                    f"[bold red]Error executing {self.name}:[/bold red] {str(e)}"
                )
                raise typer.Exit(1)

        return command_wrapper

    def _get_git_root(self) -> Path:
        """Get the git repository root, or current directory if not in a git repo."""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            return Path(result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return Path.cwd()
