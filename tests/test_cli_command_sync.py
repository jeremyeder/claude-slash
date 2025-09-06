"""
Test to ensure CLI commands and slash commands stay synchronized.

This test validates that:
1. All Python command classes are properly discoverable and implemented
2. Slash commands in .claude/commands/ correspond to actual implementations
3. No placeholder or TODO implementations exist in the CLI
4. Command discovery system works correctly
"""

import ast
import os
import importlib.util
from pathlib import Path
from typing import List, Set, Dict
import pytest
from typer.testing import CliRunner

from claude_slash.main import app, discover_commands
from claude_slash.commands.base import BaseCommand


class TestCLICommandSync:
    """Test synchronization between CLI and slash commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.project_root = Path(__file__).parent.parent

    def get_python_command_classes(self) -> Dict[str, Path]:
        """Get all Python command classes from src/claude_slash/commands/."""
        commands_dir = self.project_root / "src" / "claude_slash" / "commands"
        command_files = {}
        
        for file_path in commands_dir.glob("*.py"):
            if file_path.name in ["__init__.py", "base.py"]:
                continue
            command_files[file_path.stem] = file_path
            
        return command_files

    def get_slash_command_files(self) -> Dict[str, Path]:
        """Get all slash command files from .claude/commands/."""
        slash_dir = self.project_root / ".claude" / "commands"
        slash_files = {}
        
        for file_path in slash_dir.glob("*"):
            if file_path.name in ["__init__.py", "base.py", "error-utils.md"]:
                continue
            if file_path.suffix in [".py", ".md"]:
                # Remove extension and normalize name
                name = file_path.stem.replace("-", "_")
                slash_files[name] = file_path
                
        return slash_files

    def get_discovered_commands(self) -> List[str]:
        """Get commands discovered by the CLI discovery system."""
        commands = discover_commands()
        return [cmd().__class__.__name__.lower().replace("command", "") for cmd in commands]

    def get_cli_help_commands(self) -> Set[str]:
        """Extract available commands from CLI help output."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        
        commands = set()
        in_commands_section = False
        
        for line in result.stdout.split("\n"):
            line = line.strip()
            if "Commands:" in line:
                in_commands_section = True
                continue
            elif in_commands_section and line and not line.startswith(" "):
                break
            elif in_commands_section and line.startswith("  "):
                # Extract command name (first word after spaces)
                parts = line.split()
                if parts:
                    commands.add(parts[0])
                    
        return commands

    def has_todo_implementation(self, file_path: Path) -> bool:
        """Check if a Python file has TODO/placeholder implementations."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for common TODO patterns
            todo_patterns = [
                "# TODO",
                "# FIXME",
                "TODO:",
                "FIXME:",
                "raise NotImplementedError",
                "pass  # TODO",
                "pass # TODO",
            ]
            
            for pattern in todo_patterns:
                if pattern.lower() in content.lower():
                    return True
                    
            # Parse AST to find function bodies with only pass statements
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if (len(node.body) == 1 and 
                            isinstance(node.body[0], ast.Pass)):
                            return True
                            
            except SyntaxError:
                # If we can't parse it, assume it's not a TODO
                pass
                
        except (IOError, UnicodeDecodeError):
            # If we can't read the file, assume it's not a TODO
            pass
            
        return False

    def validate_command_class(self, file_path: Path) -> bool:
        """Validate that a Python file contains a proper BaseCommand subclass."""
        try:
            spec = importlib.util.spec_from_file_location("test_module", file_path)
            if spec is None or spec.loader is None:
                return False
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for BaseCommand subclasses
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseCommand) and 
                    attr is not BaseCommand):
                    # Found a valid command class
                    instance = attr()
                    # Validate required properties exist and work
                    if hasattr(instance, 'name') and hasattr(instance, 'help_text'):
                        return True
                        
        except Exception:
            return False
            
        return False

    def test_no_todo_implementations(self):
        """Test that no command files have TODO/placeholder implementations."""
        python_commands = self.get_python_command_classes()
        todo_commands = []
        
        for name, file_path in python_commands.items():
            if self.has_todo_implementation(file_path):
                todo_commands.append(f"{name} ({file_path})")
                
        if todo_commands:
            pytest.fail(
                f"Found commands with TODO/placeholder implementations:\n" +
                "\n".join(f"  - {cmd}" for cmd in todo_commands) +
                "\n\nThese commands should either be properly implemented or removed."
            )

    def test_python_commands_are_valid(self):
        """Test that all Python command files contain valid BaseCommand subclasses."""
        python_commands = self.get_python_command_classes()
        invalid_commands = []
        
        for name, file_path in python_commands.items():
            if not self.validate_command_class(file_path):
                invalid_commands.append(f"{name} ({file_path})")
                
        if invalid_commands:
            pytest.fail(
                f"Found invalid command class files:\n" +
                "\n".join(f"  - {cmd}" for cmd in invalid_commands) +
                "\n\nThese files should contain proper BaseCommand subclasses."
            )

    def test_command_discovery_works(self):
        """Test that command discovery finds expected commands."""
        python_commands = self.get_python_command_classes()
        discovered_commands = self.get_discovered_commands()
        
        # All valid Python commands should be discoverable
        for name in python_commands.keys():
            # Some flexibility in naming conventions
            found = any(
                name in discovered or discovered in name or
                name.replace("_", "") in discovered.replace("_", "")
                for discovered in discovered_commands
            )
            
            if not found and self.validate_command_class(python_commands[name]):
                pytest.fail(
                    f"Command '{name}' has a valid implementation but is not discoverable. "
                    f"Discovered commands: {discovered_commands}"
                )

    def test_slash_commands_have_implementations(self):
        """Test that slash commands correspond to actual implementations."""
        slash_commands = self.get_slash_command_files()
        python_commands = self.get_python_command_classes()
        
        missing_implementations = []
        
        for name, slash_file in slash_commands.items():
            # Skip markdown-only commands (they're self-contained)
            if slash_file.suffix == ".md":
                continue
                
            # Python slash commands should have corresponding implementations
            if slash_file.suffix == ".py":
                if name not in python_commands:
                    missing_implementations.append(f"{name} (slash: {slash_file})")
                elif not self.validate_command_class(python_commands[name]):
                    missing_implementations.append(f"{name} (invalid implementation: {python_commands[name]})")
                    
        if missing_implementations:
            pytest.fail(
                f"Found slash commands without proper implementations:\n" +
                "\n".join(f"  - {cmd}" for cmd in missing_implementations) +
                "\n\nEach Python slash command should have a corresponding BaseCommand implementation."
            )

    def test_cli_commands_match_implementations(self):
        """Test that CLI help output matches available implementations."""
        cli_commands = self.get_cli_help_commands()
        python_commands = self.get_python_command_classes()
        
        # Filter out built-in commands like 'version'
        builtin_commands = {"version"}
        cli_commands = cli_commands - builtin_commands
        
        unimplemented_commands = []
        
        for cli_cmd in cli_commands:
            # Look for matching implementation
            found = False
            for py_name, py_path in python_commands.items():
                if (cli_cmd in py_name or py_name in cli_cmd or 
                    cli_cmd.replace("-", "_") == py_name or
                    py_name.replace("_", "-") == cli_cmd):
                    if self.validate_command_class(py_path):
                        found = True
                        break
                        
            if not found:
                unimplemented_commands.append(cli_cmd)
                
        if unimplemented_commands:
            pytest.fail(
                f"Found CLI commands without proper implementations:\n" +
                "\n".join(f"  - {cmd}" for cmd in unimplemented_commands) +
                f"\n\nAvailable implementations: {list(python_commands.keys())}" +
                "\n\nEach CLI command should have a corresponding BaseCommand implementation."
            )

    def test_synchronization_overview(self):
        """Provide an overview of command synchronization status."""
        python_commands = self.get_python_command_classes()
        slash_commands = self.get_slash_command_files()
        cli_commands = self.get_cli_help_commands()
        discovered_commands = self.get_discovered_commands()
        
        # This test always passes but provides useful information
        print(f"\n=== Command Synchronization Overview ===")
        print(f"Python command files: {len(python_commands)}")
        print(f"Slash command files: {len(slash_commands)}")
        print(f"CLI help commands: {len(cli_commands)}")
        print(f"Discovered commands: {len(discovered_commands)}")
        
        print(f"\nPython commands: {list(python_commands.keys())}")
        print(f"Slash commands: {list(slash_commands.keys())}")
        print(f"CLI commands: {list(cli_commands)}")
        print(f"Discovered: {discovered_commands}")
        
        # Check for potential issues
        issues = []
        
        # Commands in slash but not in python
        for slash_name in slash_commands:
            if slash_commands[slash_name].suffix == ".py" and slash_name not in python_commands:
                issues.append(f"Slash command '{slash_name}' has no Python implementation")
        
        # Python commands not discoverable
        for py_name in python_commands:
            if self.validate_command_class(python_commands[py_name]):
                found = any(py_name in disc or disc in py_name for disc in discovered_commands)
                if not found:
                    issues.append(f"Python command '{py_name}' is not discoverable")
        
        if issues:
            print(f"\nPotential issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"\nNo synchronization issues detected!")