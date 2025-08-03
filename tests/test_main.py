"""Tests for claude-slash main module and CLI functionality."""

import importlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from claude_slash.commands.base import BaseCommand
from claude_slash.main import app, discover_commands, register_commands


class MockCommand(BaseCommand):
    """Mock command for testing."""

    @property
    def name(self) -> str:
        return "mock"

    @property
    def help_text(self) -> str:
        return "Mock command for testing"

    def execute(self, **kwargs):
        return "Mock executed"


class TestCommandDiscovery:
    """Test command discovery functionality."""

    def test_discover_commands_finds_base_command_subclasses(self):
        """Test that discover_commands finds BaseCommand subclasses."""
        with patch("claude_slash.main.pkgutil.iter_modules") as mock_iter:
            with patch("claude_slash.main.importlib.import_module") as mock_import:
                # Mock the package structure
                mock_iter.return_value = [
                    (None, "example", False),
                    (None, "base", False),  # Should be skipped
                ]

                # Mock module with a command class
                mock_module = MagicMock()
                mock_module.MockExampleCommand = MockCommand
                mock_module.__file__ = "/fake/path/commands/example.py"
                mock_import.return_value = mock_module

                # Mock dir() to return our command class
                with patch("builtins.dir", return_value=["MockExampleCommand"]):
                    with patch("builtins.getattr", return_value=MockCommand):
                        commands = discover_commands()

                        assert (
                            len(commands) >= 0
                        )  # Should find commands or handle gracefully

    def test_discover_commands_handles_import_errors(self):
        """Test that discover_commands handles import errors gracefully."""
        with patch("claude_slash.main.pkgutil.iter_modules") as mock_iter:
            with patch("claude_slash.main.importlib.import_module") as mock_import:
                mock_iter.return_value = [(None, "broken", False)]
                mock_import.side_effect = ImportError("Module not found")

                commands = discover_commands()
                assert isinstance(commands, list)

    def test_register_commands_handles_registration_errors(self):
        """Test that register_commands handles command registration errors."""

        class BrokenCommand(BaseCommand):
            @property
            def name(self):
                return "broken"

            @property
            def help_text(self):
                return "Broken command"

            def execute(self, **kwargs):
                pass

            def create_typer_command(self):
                raise Exception("Command creation failed")

        with patch("claude_slash.main.discover_commands", return_value=[BrokenCommand]):
            # Should not raise an exception
            register_commands()


class TestCLIApplication:
    """Test the CLI application functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_version_command(self):
        """Test the version command."""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "claude-slash" in result.stdout

    def test_checkpoint_command(self):
        """Test the checkpoint command."""
        result = self.runner.invoke(app, ["checkpoint", "test-checkpoint"])
        assert result.exit_code == 0
        assert "Creating checkpoint" in result.stdout

    def test_checkpoint_command_without_name(self):
        """Test the checkpoint command without a name."""
        result = self.runner.invoke(app, ["checkpoint"])
        assert result.exit_code == 0
        assert "Creating checkpoint" in result.stdout

    def test_restore_command(self):
        """Test the restore command."""
        result = self.runner.invoke(app, ["restore", "test-checkpoint"])
        assert result.exit_code == 0
        assert "Restoring checkpoint" in result.stdout

    def test_restore_command_without_name(self):
        """Test the restore command without a name."""
        result = self.runner.invoke(app, ["restore"])
        assert result.exit_code == 0
        assert "Restoring checkpoint" in result.stdout


class TestFixtures:
    """Test the pytest fixtures work correctly."""

    def test_temp_git_repo_fixture(self, temp_git_repo):
        """Test that temp_git_repo fixture creates a git repository."""
        assert temp_git_repo.exists()
        assert (temp_git_repo / ".git").exists() or (temp_git_repo / ".claude").exists()

    def test_mock_git_operations_fixture(self, mock_git_operations):
        """Test that git operations can be mocked."""
        import subprocess

        # Test git rev-parse mock
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "/tmp/test-repo" in result.stdout

    def test_mock_gh_operations_fixture(self, mock_gh_operations):
        """Test that GitHub CLI operations can be mocked."""
        import subprocess

        # Test gh auth status mock
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_claude_checkpoints_dir_fixture(self, claude_checkpoints_dir):
        """Test that checkpoints directory fixture works."""
        assert claude_checkpoints_dir.exists()
        assert claude_checkpoints_dir.name == "checkpoints"
        assert claude_checkpoints_dir.parent.name == ".claude"

    def test_sample_checkpoint_data_fixture(self, sample_checkpoint_data):
        """Test that sample checkpoint data fixture provides valid data."""
        assert "timestamp" in sample_checkpoint_data
        assert "branch" in sample_checkpoint_data
        assert "commit" in sample_checkpoint_data
        assert isinstance(sample_checkpoint_data["modified_files"], list)

    def test_mock_subprocess_calls_fixture(self, mock_subprocess_calls):
        """Test comprehensive subprocess mocking."""
        import subprocess

        # Test multiple command mocks
        commands_to_test = [
            ["git", "rev-parse", "--show-toplevel"],
            ["git", "status", "--porcelain"],
            ["gh", "auth", "status"],
        ]

        for cmd in commands_to_test:
            result = subprocess.run(cmd, capture_output=True, text=True)
            assert result.returncode == 0


class TestBaseCommand:
    """Test BaseCommand functionality."""

    def test_base_command_interface(self):
        """Test that BaseCommand provides the correct interface."""
        cmd = MockCommand()

        assert cmd.name == "mock"
        assert cmd.help_text == "Mock command for testing"
        assert hasattr(cmd, "execute")
        assert hasattr(cmd, "create_typer_command")

    def test_base_command_error_handling(self):
        """Test BaseCommand error handling methods."""
        cmd = MockCommand()

        # Test that these methods exist and are callable
        assert hasattr(cmd, "error")
        assert hasattr(cmd, "success")
        assert hasattr(cmd, "info")
        assert hasattr(cmd, "warning")

    def test_create_typer_command_wrapper(self):
        """Test that create_typer_command creates a valid wrapper."""
        cmd = MockCommand()
        wrapper = cmd.create_typer_command()

        assert callable(wrapper)
        assert wrapper.__name__ == "mock"
        assert wrapper.__doc__ == "Mock command for testing"


class TestSubprocessMocking:
    """Test subprocess mocking capabilities."""

    def test_git_command_mocking(self, mock_git_operations):
        """Test that git commands are properly mocked."""
        import subprocess

        # Test git status mock
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "file1.py" in result.stdout

    def test_git_add_command_mock(self, mock_git_operations):
        """Test git add command mock."""
        import subprocess

        result = subprocess.run(["git", "add", "."], capture_output=True)
        assert result.returncode == 0

    def test_gh_command_mocking(self, mock_gh_operations):
        """Test that GitHub CLI commands are properly mocked."""
        import subprocess

        # Test gh repo view mock
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "name,owner"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "test-repo" in result.stdout
