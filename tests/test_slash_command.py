"""Tests for the slash command functionality."""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import typer

from claude_slash.commands.slash import SlashCommand


class TestSlashCommand:
    """Test the slash command implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.slash_cmd = SlashCommand()

    def test_command_properties(self):
        """Test basic command properties."""
        assert self.slash_cmd.name == "slash"
        assert "help" in self.slash_cmd.help_text.lower()
        assert "update" in self.slash_cmd.help_text.lower()

    def test_help_functionality(self, tmp_path):
        """Test help display functionality."""
        # Create mock commands directory structure
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)

        # Create a mock command file
        test_cmd = commands_dir / "test.md"
        test_cmd.write_text(
            """# Test Command

Test command description.

## Usage

```bash
/test
```

## Description

This is a test command for testing purposes.

## Implementation

!echo "test"
"""
        )

        with patch.object(
            self.slash_cmd, "_find_commands_directory", return_value=str(commands_dir)
        ):
            # Should not raise an exception
            self.slash_cmd._handle_help()

    def test_extract_description(self, tmp_path):
        """Test description extraction from markdown files."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """# Test Command

This is the description.

## Usage
"""
        )

        description = self.slash_cmd._extract_description(test_file)
        assert description == "This is the description."

    def test_extract_usage(self, tmp_path):
        """Test usage extraction from markdown files."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """# Test Command

Description here.

## Usage

```bash
/test-command [args]
```
"""
        )

        usage = self.slash_cmd._extract_usage(test_file)
        assert usage == "/test-command [args]"

    def test_detect_installation_project(self, tmp_path):
        """Test installation detection for project-level installation."""
        # Create project-level commands directory
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)

        with patch("os.getcwd", return_value=str(tmp_path)):
            install_dir, install_type = self.slash_cmd._detect_installation()
            assert install_dir == str(commands_dir)
            assert install_type == "project"

    def test_detect_installation_global(self, tmp_path):
        """Test installation detection for global installation."""
        # Create global-level commands directory
        global_dir = tmp_path / "home" / ".claude" / "commands"
        global_dir.mkdir(parents=True)

        with patch("os.getcwd", return_value=str(tmp_path / "workdir")):
            with patch("os.path.expanduser", return_value=str(tmp_path / "home")):
                install_dir, install_type = self.slash_cmd._detect_installation()
                assert install_dir == str(global_dir)
                assert install_type == "global"

    def test_find_commands_directory_with_git(self, tmp_path):
        """Test commands directory finding with git repository."""
        git_root = tmp_path / "repo"
        commands_dir = git_root / ".claude" / "commands"
        commands_dir.mkdir(parents=True)

        mock_result = Mock()
        mock_result.stdout.strip.return_value = str(git_root)

        with patch("subprocess.run", return_value=mock_result) as mock_subprocess:
            result = self.slash_cmd._find_commands_directory()
            mock_subprocess.assert_called_once()
            assert result == str(commands_dir)

    @patch("subprocess.run")
    def test_update_functionality_success(self, mock_subprocess, tmp_path):
        """Test successful update functionality."""
        # Mock successful gh CLI calls
        mock_release_info = {
            "tag_name": "v1.2.0",
            "tarball_url": "https://example.com/tarball",
        }

        def subprocess_side_effect(cmd, **kwargs):
            mock_result = Mock()
            mock_result.returncode = 0

            if "releases/latest" in str(cmd):
                mock_result.stdout = json.dumps(mock_release_info)
            elif "tarball" in str(cmd):
                # Mock successful tarball download
                pass
            elif cmd[0] == "tar":
                # Mock successful tar extraction
                pass

            return mock_result

        mock_subprocess.side_effect = subprocess_side_effect

        # Create mock installation
        install_dir = tmp_path / ".claude" / "commands"
        install_dir.mkdir(parents=True)
        (install_dir / "old.md").write_text("old command")

        # Create mock source directory structure for the update
        with tempfile.TemporaryDirectory() as temp_dir:
            source_commands = Path(temp_dir) / ".claude" / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "new.md").write_text("new command")

            with patch.object(
                self.slash_cmd,
                "_detect_installation",
                return_value=(str(install_dir), "project"),
            ):
                with patch("tempfile.TemporaryDirectory") as mock_tempdir:
                    mock_tempdir.return_value.__enter__.return_value = temp_dir

                    # Should not raise an exception
                    self.slash_cmd._handle_update()

    @patch("subprocess.run")
    def test_update_network_error(self, mock_subprocess):
        """Test update handling when network request fails."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, ["gh"])

        install_dir = "/fake/dir"
        with patch.object(
            self.slash_cmd,
            "_detect_installation",
            return_value=(install_dir, "project"),
        ):
            with pytest.raises((SystemExit, typer.Exit)):
                self.slash_cmd._handle_update()

    def test_get_timestamp(self):
        """Test timestamp generation."""
        timestamp = self.slash_cmd._get_timestamp()
        assert len(timestamp) == 15  # YYYYMMDD-HHMMSS format
        assert "-" in timestamp

    def test_execute_help_default(self):
        """Test execute method with default (help) behavior."""
        with patch.object(self.slash_cmd, "_handle_help") as mock_help:
            self.slash_cmd.execute()
            mock_help.assert_called_once()

    def test_execute_update_subcommand(self):
        """Test execute method with update subcommand."""
        with patch.object(self.slash_cmd, "_handle_update") as mock_update:
            self.slash_cmd.execute(subcommand="update")
            mock_update.assert_called_once()

    def test_create_typer_command(self):
        """Test Typer command creation."""
        command_func = self.slash_cmd.create_typer_command()
        assert callable(command_func)

        # Test that it doesn't raise an exception with help
        with patch.object(self.slash_cmd, "_handle_help"):
            command_func()

        # Test with update subcommand
        with patch.object(self.slash_cmd, "_handle_update"):
            command_func("update")
