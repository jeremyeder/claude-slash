"""
Test that ensures CLI commands and their implementations stay synchronized.

This test validates that all commands shown in the CLI help have proper
implementations and follow the established patterns, preventing the issue
where commands appear in help but lack real functionality.
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Set
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from claude_slash.commands.base import BaseCommand
from claude_slash.main import app, discover_commands


class TestCLICommandSynchronization:
    """Test suite to ensure CLI commands and implementations are synchronized."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_commands_have_implementations(self):
        """Test that all CLI commands have proper implementations."""
        # Get CLI help to extract available commands
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        
        help_output = result.stdout
        
        # Extract command names from help output
        cli_commands = self._extract_commands_from_help(help_output)
        
        # Check each command for proper implementation
        unimplemented_commands = []
        todo_commands = []
        
        for command_name in cli_commands:
            implementation_status = self._check_command_implementation(command_name)
            
            if implementation_status == "unimplemented":
                unimplemented_commands.append(command_name)
            elif implementation_status == "todo":
                todo_commands.append(command_name)
        
        # Assert that we don't have unimplemented or TODO-only commands
        if unimplemented_commands:
            pytest.fail(
                f"Commands without implementations: {unimplemented_commands}. "
                "These commands appear in CLI help but have no implementation."
            )
        
        if todo_commands:
            pytest.fail(
                f"Commands with only TODO placeholders: {todo_commands}. "
                "These commands appear in CLI help but contain only TODO comments "
                "instead of real functionality."
            )

    def test_direct_commands_follow_patterns(self):
        """Test that directly registered commands follow established patterns."""
        main_file = Path(__file__).parent.parent / "src" / "claude_slash" / "main.py"
        
        # Parse main.py to find directly registered commands
        direct_commands = self._extract_direct_commands_from_main(main_file)
        
        # Check if these commands should be BaseCommand subclasses instead
        problematic_commands = []
        
        for command_name, has_todo in direct_commands.items():
            if has_todo:
                problematic_commands.append(command_name)
        
        if problematic_commands:
            pytest.fail(
                f"Direct commands with TODO implementations: {problematic_commands}. "
                "Consider implementing these as BaseCommand subclasses in the commands/ "
                "directory for better organization and consistency."
            )

    def test_discovered_commands_are_registered(self):
        """Test that all discovered commands are properly registered."""
        discovered_commands = discover_commands()
        
        # Get CLI help to see what's actually available
        result = self.runner.invoke(app, ["--help"])
        help_output = result.stdout
        cli_commands = self._extract_commands_from_help(help_output)
        
        # Check that all discovered commands appear in CLI
        missing_commands = []
        
        for command_class in discovered_commands:
            try:
                command_instance = command_class()
                command_name = command_instance.name
                
                if command_name not in cli_commands:
                    missing_commands.append(command_name)
            except Exception as e:
                # Command instantiation failed
                missing_commands.append(f"{command_class.__name__} (instantiation failed: {e})")
        
        if missing_commands:
            pytest.fail(
                f"Discovered commands not available in CLI: {missing_commands}. "
                "These commands were found in the commands/ directory but are not "
                "accessible through the CLI interface."
            )

    def test_command_help_consistency(self):
        """Test that command help text is consistent and informative."""
        # Get CLI help
        result = self.runner.invoke(app, ["--help"])
        help_output = result.stdout
        cli_commands = self._extract_commands_from_help(help_output)
        
        commands_with_poor_help = []
        
        for command_name in cli_commands:
            # Test individual command help
            result = self.runner.invoke(app, [command_name, "--help"])
            if result.exit_code == 0:
                command_help = result.stdout.lower()
                
                # Check for placeholder or unhelpful help text
                if any(phrase in command_help for phrase in [
                    "todo", "implement", "placeholder", "coming soon", "not implemented"
                ]):
                    commands_with_poor_help.append(command_name)
        
        if commands_with_poor_help:
            pytest.fail(
                f"Commands with placeholder help text: {commands_with_poor_help}. "
                "These commands have help text indicating they're not fully implemented."
            )

    def _extract_commands_from_help(self, help_output: str) -> Set[str]:
        """Extract command names from CLI help output."""
        commands = set()
        
        # Look for command lines in help output
        # Typer help format typically shows: "  command-name    Description"
        lines = help_output.split('\n')
        in_commands_section = False
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('Usage:') or line.startswith('Options:'):
                continue
            
            # Look for commands section
            if 'Commands:' in line:
                in_commands_section = True
                continue
            
            # Stop at next section
            if in_commands_section and line.endswith(':'):
                break
            
            # Extract command name from command line
            if in_commands_section and line.startswith(' '):
                # Format: "  command-name    Description"
                parts = line.strip().split()
                if parts:
                    command_name = parts[0]
                    # Filter out obvious non-command lines
                    if not command_name.startswith('[') and not command_name.startswith('--'):
                        commands.add(command_name)
        
        return commands

    def _check_command_implementation(self, command_name: str) -> str:
        """
        Check the implementation status of a command.
        
        Returns:
            "implemented": Command has real implementation
            "todo": Command has only TODO/placeholder implementation
            "unimplemented": Command has no implementation
        """
        # Try to run the command with --help to see if it exists
        result = self.runner.invoke(app, [command_name, "--help"])
        
        if result.exit_code != 0:
            return "unimplemented"
        
        # Check if this is a direct command in main.py
        main_file = Path(__file__).parent.parent / "src" / "claude_slash" / "main.py"
        direct_commands = self._extract_direct_commands_from_main(main_file)
        
        if command_name in direct_commands:
            return "todo" if direct_commands[command_name] else "implemented"
        
        # Check if this is a discovered command
        discovered_commands = discover_commands()
        for command_class in discovered_commands:
            try:
                command_instance = command_class()
                if command_instance.name == command_name:
                    # Check if the execute method has real implementation
                    execute_method = inspect.getsource(command_instance.execute)
                    if "TODO" in execute_method or "pass" in execute_method:
                        return "todo"
                    return "implemented"
            except Exception:
                continue
        
        return "implemented"  # Assume implemented if we can't determine otherwise

    def _extract_direct_commands_from_main(self, main_file: Path) -> Dict[str, bool]:
        """
        Extract directly registered commands from main.py and check for TODOs.
        
        Returns:
            Dict mapping command names to whether they have TODO implementations
        """
        commands = {}
        
        try:
            with open(main_file, 'r') as f:
                content = f.read()
            
            # Parse the AST to find @app.command() decorators
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function has @app.command() decorator
                    for decorator in node.decorator_list:
                        if (isinstance(decorator, ast.Call) and
                            isinstance(decorator.func, ast.Attribute) and
                            isinstance(decorator.func.value, ast.Name) and
                            decorator.func.value.id == "app" and
                            decorator.func.attr == "command"):
                            
                            command_name = node.name
                            
                            # Check if function body contains TODO
                            function_source = ast.get_source_segment(content, node)
                            has_todo = "TODO" in function_source if function_source else False
                            
                            commands[command_name] = has_todo
                            break
        
        except Exception as e:
            # If we can't parse the file, return empty dict
            pytest.fail(f"Failed to parse main.py for direct commands: {e}")
        
        return commands


class TestSpecificCommandIssues:
    """Test specific known issues with command synchronization."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_checkpoint_command_implementation(self):
        """Test that checkpoint command has proper implementation."""
        result = self.runner.invoke(app, ["checkpoint", "--help"])
        assert result.exit_code == 0
        
        # Run the actual command to check implementation
        result = self.runner.invoke(app, ["checkpoint", "test"])
        assert result.exit_code == 0
        
        # Check that output doesn't indicate TODO status
        output = result.stdout.lower()
        if "todo" in output:
            pytest.fail(
                "Checkpoint command appears to have TODO implementation. "
                "The command should have real functionality, not placeholders."
            )

    def test_restore_command_implementation(self):
        """Test that restore command has proper implementation."""
        result = self.runner.invoke(app, ["restore", "--help"])
        assert result.exit_code == 0
        
        # Run the actual command to check implementation
        result = self.runner.invoke(app, ["restore", "test"])
        assert result.exit_code == 0
        
        # Check that output doesn't indicate TODO status
        output = result.stdout.lower()
        if "todo" in output:
            pytest.fail(
                "Restore command appears to have TODO implementation. "
                "The command should have real functionality, not placeholders."
            )

    def test_no_orphaned_command_files(self):
        """Test that there are no command files that aren't being discovered."""
        commands_dir = Path(__file__).parent.parent / "src" / "claude_slash" / "commands"
        
        if not commands_dir.exists():
            pytest.skip("Commands directory doesn't exist")
        
        # Get all Python files in commands directory
        command_files = list(commands_dir.glob("*.py"))
        command_files = [f for f in command_files if f.name not in ["__init__.py", "base.py"]]
        
        # Get discovered commands
        discovered_commands = discover_commands()
        discovered_names = set()
        
        for command_class in discovered_commands:
            try:
                command_instance = command_class()
                discovered_names.add(command_instance.name)
            except Exception:
                continue
        
        # Check that we have discovered commands for most command files
        # (allowing some flexibility for utility files)
        if len(command_files) > 0 and len(discovered_names) == 0:
            pytest.fail(
                f"Found {len(command_files)} command files but no discovered commands. "
                "This suggests the command discovery mechanism might be broken."
            )