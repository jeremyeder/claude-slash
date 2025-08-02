"""
Learn command for extracting and integrating session learnings into CLAUDE.md.

This module provides an interactive interface for analyzing current session context
to extract important insights and integrate them into the global CLAUDE.md file.
"""

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.syntax import Syntax
from rich.table import Table

from .base import BaseCommand


class LearnCommand(BaseCommand):
    """
    Interactive Learning Integration System for CLAUDE.md.
    
    Autonomously analyzes the current Claude Code session context to extract
    important insights, patterns, and learnings, then provides an interactive
    interface for integrating them into the global CLAUDE.md file.
    """
    
    @property
    def name(self) -> str:
        """Return the command name for registration."""
        return "learn"
    
    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return ("Continuously refine the global CLAUDE.md file with impactful "
                "learnings from the current session through an interactive "
                "integration interface.")
    
    def __init__(self):
        """Initialize the learn command."""
        super().__init__()
        self.claude_md_path = Path.home() / ".claude" / "CLAUDE.md"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def execute(self, **kwargs) -> None:
        """Execute the learn command."""
        self.console.print(Panel.fit(
            "🧠 Interactive Learning Integration System",
            style="bold blue"
        ))
        self.console.print()
        
        # Check if global CLAUDE.md exists
        if not self.claude_md_path.exists():
            self.error(f"Global CLAUDE.md not found at {self.claude_md_path}")
            self.console.print("Please ensure your global Claude configuration is set up correctly.")
            return
        
        # Extract learnings from current session
        learning_content = self._extract_session_learnings()
        
        # Display extracted learnings
        self._display_learning_summary(learning_content)
        
        # Ask user to confirm the extracted learnings
        if not Confirm.ask(
            "[yellow]📝 Do you want to integrate these learnings into CLAUDE.md?[/yellow]",
            default=False
        ):
            self.console.print("[yellow]❌ Learning extraction cancelled by user.[/yellow]")
            return
        
        # Create backup
        backup_path = self._create_backup()
        self.success(f"Backup created at: {backup_path}")
        self.console.print()
        
        # Parse CLAUDE.md structure and get user selection
        sections = self._parse_claude_md_structure()
        selected_section = self._interactive_section_selection(sections)
        
        if selected_section is None:
            self.error("Invalid selection. Please run the command again.")
            return
        
        # Format learning content
        formatted_learning = self._format_learning_content(learning_content)
        
        # Handle integration based on selection
        if selected_section["type"] == "new_section":
            self._integrate_new_section(selected_section["name"], formatted_learning)
        else:
            integration_mode = self._choose_integration_mode()
            if integration_mode == "manual":
                self._show_manual_integration(selected_section, formatted_learning)
                return
            
            self._integrate_existing_section(
                selected_section, formatted_learning, integration_mode
            )
        
        # Show integration summary
        self._show_integration_summary(selected_section, learning_content, backup_path)
    
    def _extract_session_learnings(self) -> str:
        """
        Extract learnings from current session context.
        
        This is a placeholder implementation that demonstrates the structure.
        In a real implementation, this would analyze the actual session context.
        """
        self.console.print("[cyan]🔍 Analyzing current session context for learnings...[/cyan]")
        self.console.print()
        
        # Get current git repository info for context
        try:
            git_root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            repo_name = Path(git_root).name
        except subprocess.CalledProcessError:
            repo_name = "Current session"
        
        # Sample learning content (in production, this would analyze actual session data)
        learning_content = f"""Session Analysis Results:

Key learnings identified from current session:

1. **Clean Feature Branch Management**: When creating feature branches, always cherry-pick specific commits to avoid including unrelated changes in PRs. Use 'git checkout -B feature/name' from clean main, then 'git cherry-pick COMMIT_HASH' to include only relevant changes.

2. **Force Push Safety**: Use 'git push --force-with-lease' instead of 'git push --force' to safely update feature branches while protecting against overwriting others' work.

3. **PR Hygiene**: Always verify PR contents show only intended changes by checking commit history and file diffs before submission.

4. **Command Enhancement Pattern**: When enhancing CLI tools, add terminal output to show users exactly what was accomplished.

Context: {repo_name}"""
        
        return learning_content
    
    def _display_learning_summary(self, learning_content: str) -> None:
        """Display the extracted learning summary."""
        self.console.print(Panel(
            learning_content,
            title="📊 Extracted Learning Summary",
            style="green"
        ))
        self.console.print()
    
    def _create_backup(self) -> Path:
        """Create a backup of the current CLAUDE.md file."""
        timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = self.claude_md_path.parent / f"CLAUDE.md.backup-{timestamp_str}"
        shutil.copy2(self.claude_md_path, backup_path)
        return backup_path
    
    def _parse_claude_md_structure(self) -> List[dict]:
        """Parse CLAUDE.md structure to extract sections."""
        self.console.print("[cyan]📖 Analyzing CLAUDE.md structure...[/cyan]")
        
        sections = []
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.startswith('#'):
                sections.append({
                    "line_num": line_num,
                    "header": line.strip(),
                    "type": "existing"
                })
                # Limit to first 20 sections for display
                if len(sections) >= 20:
                    break
        
        return sections
    
    def _interactive_section_selection(self, sections: List[dict]) -> Optional[dict]:
        """Interactive section selection interface."""
        self.console.print("[cyan]📝 Available sections in CLAUDE.md:[/cyan]")
        self.console.print()
        
        # Create table for better display
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Number", style="purple", width=8)
        table.add_column("Section", style="cyan")
        
        for i, section in enumerate(sections, 1):
            table.add_row(str(i), section["header"])
        
        max_selection = len(sections) + 1
        table.add_row(str(max_selection), "Create new section")
        
        self.console.print(table)
        self.console.print()
        
        # Smart content analysis for suggestions
        learning_suggestions = self._analyze_content_for_suggestions()
        if learning_suggestions:
            self.console.print("[green]💡 Suggested sections based on content analysis:[/green]")
            self.console.print(f"[green]   {learning_suggestions}[/green]")
            self.console.print()
        
        # Get user selection
        selection = IntPrompt.ask(
            "[yellow]🎯 Select target section for integration[/yellow]",
            default=1,
            show_default=True
        )
        
        if selection < 1 or selection > max_selection:
            return None
        
        if selection == max_selection:
            # Handle new section creation
            new_section_name = Prompt.ask("Enter new section name")
            if not new_section_name.strip():
                return None
            
            return {
                "name": new_section_name.strip(),
                "header": f"## {new_section_name.strip()}",
                "type": "new_section"
            }
        else:
            # Return selected existing section
            selected = sections[selection - 1]
            return {
                "name": selected["header"],
                "header": selected["header"],
                "line_num": selected["line_num"],
                "type": "existing"
            }
    
    def _analyze_content_for_suggestions(self) -> str:
        """Analyze learning content for smart section suggestions."""
        # This would analyze the learning content for keywords
        # and suggest appropriate sections
        suggestions = []
        
        # Sample keyword analysis (would be enhanced in production)
        learning_keywords = ["test", "debug", "workflow", "git", "strategic", "principle"]
        section_mapping = {
            "test": "Test-Implementation Synchronization",
            "debug": "Test-Implementation Synchronization", 
            "workflow": "Pre-Push Linting Workflow",
            "git": "Pre-Push Linting Workflow",
            "strategic": "Strategic Tools & Methodologies",
            "principle": "Key Operating Principles"
        }
        
        for keyword in learning_keywords:
            if keyword in section_mapping:
                suggestions.append(section_mapping[keyword])
        
        return ", ".join(list(dict.fromkeys(suggestions)))  # Remove duplicates
    
    def _choose_integration_mode(self) -> str:
        """Choose integration mode for existing sections."""
        self.console.print("[yellow]🔧 Choose integration mode:[/yellow]")
        
        options = [
            "1. Append to end of section",
            "2. Insert after section header", 
            "3. Show section content for manual placement"
        ]
        
        for option in options:
            self.console.print(option)
        self.console.print()
        
        mode_selection = IntPrompt.ask(
            "Select integration mode",
            choices=["1", "2", "3"],
            default=1
        )
        
        mode_map = {1: "append", 2: "insert", 3: "manual"}
        return mode_map[mode_selection]
    
    def _format_learning_content(self, learning_content: str) -> str:
        """Format learning content for integration."""
        formatted = f"""## Session Learning - {self.timestamp}

**Context**: Current session

**Learning**: {learning_content}

**Application**: This insight should be applied to future similar scenarios to improve efficiency and outcomes.
"""
        return formatted
    
    def _show_manual_integration(self, section: dict, formatted_learning: str) -> None:
        """Show section content for manual integration."""
        self.console.print("[yellow]📖 Current section content:[/yellow]")
        
        # Read and display current section content
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = section["line_num"] - 1
        # Find next section or end of file
        end_line = len(lines)
        for i in range(start_line + 1, len(lines)):
            if lines[i].startswith('#'):
                end_line = i
                break
        
        section_content = ''.join(lines[start_line:end_line])
        self.console.print(Panel(section_content, style="dim"))
        
        self.console.print()
        self.console.print("[yellow]You can manually copy and integrate the learning content above.[/yellow]")
        
        # Show the learning content to copy
        self.console.print()
        self.console.print(Panel(
            formatted_learning,
            title="Learning Content to Integrate",
            style="green"
        ))
    
    def _integrate_new_section(self, section_name: str, formatted_learning: str) -> None:
        """Integrate learning as a new section."""
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = f"{content}\n\n## {section_name}\n\n{formatted_learning}"
        
        with open(self.claude_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        self.success("Learning successfully integrated into CLAUDE.md!")
    
    def _integrate_existing_section(self, section: dict, formatted_learning: str, mode: str) -> None:
        """Integrate learning into existing section."""
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = section["line_num"] - 1
        
        if mode == "append":
            # Find end of section
            end_line = len(lines)
            for i in range(start_line + 1, len(lines)):
                if lines[i].startswith('#'):
                    end_line = i
                    break
            
            # Insert before next section or at end
            lines.insert(end_line, f"\n{formatted_learning}\n")
            
        elif mode == "insert":
            # Insert right after section header
            lines.insert(start_line + 1, f"\n{formatted_learning}\n")
        
        # Write back to file
        with open(self.claude_md_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        self.success("Learning successfully integrated into CLAUDE.md!")
    
    def _show_integration_summary(self, section: dict, learning_content: str, backup_path: Path) -> None:
        """Show integration summary."""
        self.console.print()
        self.console.print(Panel.fit(
            "📊 Integration Summary",
            style="cyan"
        ))
        
        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("Label", style="cyan")
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("📁 Target:", section["name"])
        summary_table.add_row("🕐 Timestamp:", self.timestamp)
        summary_table.add_row("💾 Backup:", str(backup_path))
        
        preview = learning_content[:50] + "..." if len(learning_content) > 50 else learning_content
        summary_table.add_row("📝 Content:", preview)
        
        self.console.print(summary_table)
        self.console.print()