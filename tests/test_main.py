"""
Tests for the main CLI application.

This module tests the core CLI functionality including command discovery,
registration, and execution using mocked subprocess calls.
"""

import importlib
from pathlib import Path
from typing import List, Type
from unittest.mock import Mock, patch

import pytest
import typer
from pytest_subprocess import FakeProcess
from typer.testing import CliRunner

from claude_slash.commands.base import BaseCommand
from claude_slash.main import app, discover_commands, register_commands


class TestCommandDiscovery:
    """Test command discovery functionality."""
    
    def test_discover_commands_returns_list(self):
        """Test that discover_commands returns a list."""
        commands = discover_commands()
        assert isinstance(commands, list)
    
    def test_discover_commands_excludes_base(self):
        """Test that BaseCommand itself is not included in discovered commands."""
        commands = discover_commands()
        assert BaseCommand not in commands
    
    def test_discover_commands_finds_subclasses(self):
        """Test that discover_commands finds BaseCommand subclasses."""
        commands = discover_commands()
        
        # All discovered commands should be subclasses of BaseCommand
        for command_class in commands:
            assert issubclass(command_class, BaseCommand)
            assert command_class is not BaseCommand


class TestCliApplication:
    """Test the main CLI application."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_app_is_typer_instance(self):
        """Test that app is a Typer instance."""
        assert isinstance(app, typer.Typer)
    
    def test_version_command_exists(self):
        """Test that version command is available."""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "claude-slash" in result.stdout
    
    def test_checkpoint_command_exists(self):
        """Test that checkpoint command is available."""
        result = self.runner.invoke(app, ["checkpoint", "test"])
        assert result.exit_code == 0
        assert "Creating checkpoint" in result.stdout
    
    def test_restore_command_exists(self):
        """Test that restore command is available."""
        result = self.runner.invoke(app, ["restore", "test"])
        assert result.exit_code == 0
        assert "Restoring checkpoint" in result.stdout
    
    def test_help_command_works(self):
        """Test that help command works."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Custom slash commands for Claude Code CLI" in result.stdout


class TestSubprocessMocking:
    """Test subprocess mocking functionality."""
    
    def test_git_status_mock(self, mock_subprocess_all: FakeProcess):
        """Test that git status can be mocked."""
        import subprocess
        
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert result.stdout == ""
    
    def test_git_rev_parse_mock(self, mock_subprocess_all: FakeProcess):
        """Test that git rev-parse can be mocked."""
        import subprocess
        
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert result.stdout == "/fake/repo/path"
    
    def test_gh_auth_status_mock(self, mock_subprocess_all: FakeProcess):
        """Test that gh auth status can be mocked."""
        import subprocess
        
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Logged in to github.com" in result.stdout


class TestFixtures:
    """Test pytest fixtures."""
    
    def test_temp_git_repo_fixture(self, temp_git_repo: Path):
        """Test that temp_git_repo fixture creates a valid git repo."""
        assert temp_git_repo.exists()
        assert temp_git_repo.is_dir()
        assert (temp_git_repo / ".git").exists()
    
    def test_claude_checkpoints_dir_fixture(self, claude_checkpoints_dir: Path):
        """Test that claude_checkpoints_dir fixture creates the directory."""
        assert claude_checkpoints_dir.exists()
        assert claude_checkpoints_dir.is_dir()
        assert claude_checkpoints_dir.name == "checkpoints"
        assert claude_checkpoints_dir.parent.name == ".claude"
    
    def test_sample_checkpoint_data_fixture(self, sample_checkpoint_data: dict):
        """Test that sample_checkpoint_data fixture provides valid data."""
        assert "timestamp" in sample_checkpoint_data
        assert "git_hash" in sample_checkpoint_data
        assert "branch" in sample_checkpoint_data
        assert "files_changed" in sample_checkpoint_data
        assert "message" in sample_checkpoint_data
    
    def test_console_mock_fixture(self, console_mock: Mock):
        """Test that console_mock fixture provides a Mock object."""
        assert isinstance(console_mock, Mock)


class TestErrorHandling:
    """Test error handling in command discovery and registration."""
    
    def test_discover_commands_handles_import_error(self):
        """Test that discover_commands handles import errors gracefully."""
        with patch('importlib.import_module') as mock_import:
            mock_import.side_effect = ImportError("Test error")
            
            commands = discover_commands()
            # Should return empty list when package can't be imported
            assert isinstance(commands, list)
    
    @patch('claude_slash.main.console')
    def test_register_commands_handles_exceptions(self, mock_console):
        """Test that register_commands handles exceptions during registration."""
        # Create a mock command class that raises an exception
        class BrokenCommand(BaseCommand):
            name = "broken"
            help_text = "A broken command"
            
            def create_typer_command(self):
                raise ValueError("Broken command")
        
        with patch('claude_slash.main.discover_commands') as mock_discover:
            mock_discover.return_value = [BrokenCommand]
            
            # Should not raise an exception
            register_commands()
            
            # Should print error message
            mock_console.print.assert_called()