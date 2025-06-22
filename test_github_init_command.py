"""Tests for the GitHub Init command."""

import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from github_init_command import (GitHubInitCommand, GitHubInitOptions,
                                 handle_github_init_command, parse_arguments)


class TestGitHubInitOptions(unittest.TestCase):
    """Test GitHubInitOptions dataclass."""

    def test_default_options(self):
        """Test default option values."""
        options = GitHubInitOptions(repo_name="test-repo")

        self.assertEqual(options.repo_name, "test-repo")
        self.assertIsNone(options.description)
        self.assertTrue(options.private)  # Should default to private
        self.assertIsNone(options.license)
        self.assertIsNone(options.gitignore)
        self.assertTrue(options.readme)
        self.assertEqual(options.default_branch, "main")
        self.assertIsNone(options.topics)
        self.assertFalse(options.create_website)

    def test_custom_options(self):
        """Test custom option values."""
        options = GitHubInitOptions(
            repo_name="custom-repo",
            description="My custom repo",
            private=False,
            license="MIT",
            gitignore="python",
            readme=False,
            default_branch="develop",
            topics=["python", "cli"],
            create_website=True,
        )

        self.assertEqual(options.repo_name, "custom-repo")
        self.assertEqual(options.description, "My custom repo")
        self.assertFalse(options.private)
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertFalse(options.readme)
        self.assertEqual(options.default_branch, "develop")
        self.assertEqual(options.topics, ["python", "cli"])
        self.assertTrue(options.create_website)


class TestParseArguments(unittest.TestCase):
    """Test command-line argument parsing."""

    def test_minimal_args(self):
        """Test parsing with minimal arguments."""
        options = parse_arguments(["my-repo"])

        self.assertEqual(options.repo_name, "my-repo")
        self.assertTrue(options.private)  # Should default to private
        self.assertTrue(options.readme)
        self.assertEqual(options.default_branch, "main")
        self.assertFalse(options.create_website)

    def test_public_flag(self):
        """Test --public flag makes repo public."""
        options = parse_arguments(["my-repo", "--public"])
        self.assertFalse(options.private)

    def test_all_arguments(self):
        """Test parsing all available arguments."""
        args = [
            "test-repo",
            "--desc",
            "Test description",
            "--public",
            "--license",
            "MIT",
            "--gitignore",
            "python",
            "--no-readme",
            "--branch",
            "develop",
            "--topics",
            "python,cli,tool",
            "--create-website",
        ]

        options = parse_arguments(args)

        self.assertEqual(options.repo_name, "test-repo")
        self.assertEqual(options.description, "Test description")
        self.assertFalse(options.private)
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertFalse(options.readme)
        self.assertEqual(options.default_branch, "develop")
        self.assertEqual(options.topics, ["python", "cli", "tool"])
        self.assertTrue(options.create_website)


class TestGitHubInitCommand(unittest.TestCase):
    """Test GitHubInitCommand class."""

    def setUp(self):
        """Set up test fixtures."""
        self.options = GitHubInitOptions(
            repo_name="test-repo",
            description="Test repository",
            private=True,
            license="MIT",
            gitignore="python",
            readme=True,
            topics=["python", "test"],
            create_website=False,
        )
        self.command = GitHubInitCommand(self.options)

    @patch("subprocess.run")
    @patch("os.chdir")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_execute_success(self, mock_file, mock_mkdir, mock_chdir, mock_run):
        """Test successful execution of the command."""
        mock_run.return_value = MagicMock(returncode=0)

        self.command.execute()

        # Verify directory creation and navigation
        mock_mkdir.assert_called()  # Called multiple times for repo and .github/workflows
        self.assertEqual(mock_chdir.call_count, 2)  # Enter and exit

        # Verify git init
        mock_run.assert_any_call(["git", "init", "--initial-branch=main"], check=True)

        # Verify file creation
        self.assertTrue(
            any("README.md" in str(call) for call in mock_file.call_args_list)
        )
        self.assertTrue(
            any(".gitignore" in str(call) for call in mock_file.call_args_list)
        )
        self.assertTrue(
            any("LICENSE" in str(call) for call in mock_file.call_args_list)
        )

        # Verify GitHub Actions workflow creation
        self.assertTrue(any("ci.yml" in str(call) for call in mock_file.call_args_list))

        # Verify GitHub repo creation
        mock_run.assert_any_call(
            [
                "gh",
                "repo",
                "create",
                "test-repo",
                "--private",
                "--confirm",
                "--description",
                "Test repository",
            ],
            check=True,
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_create_readme(self, mock_file):
        """Test README creation."""
        self.command._create_readme()

        mock_file.assert_called_once_with("README.md", "w")
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("# test-repo", written_content)
        self.assertIn("Test repository", written_content)
        self.assertIn("MIT License", written_content)

    @patch("builtins.open", new_callable=mock_open)
    def test_create_gitignore_python(self, mock_file):
        """Test Python .gitignore creation."""
        self.command._create_gitignore()

        mock_file.assert_called_once_with(".gitignore", "w")
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("__pycache__/", written_content)
        self.assertIn("venv/", written_content)
        self.assertIn("*.py[cod]", written_content)

    @patch("builtins.open", new_callable=mock_open)
    def test_create_license_mit(self, mock_file):
        """Test MIT license creation."""
        self.command._create_license()

        mock_file.assert_called_once_with("LICENSE", "w")
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("MIT License", written_content)
        self.assertIn("Copyright (c)", written_content)

    @patch("subprocess.run")
    def test_create_github_repo_public(self, mock_run):
        """Test creating a public GitHub repository."""
        self.command.options.private = False

        # Mock the username API call
        mock_user_result = MagicMock()
        mock_user_result.stdout.strip.return_value = "testuser"
        mock_run.side_effect = [
            MagicMock(returncode=0),  # gh repo create
            mock_user_result,  # gh api user
            MagicMock(returncode=0),  # git remote add
        ]

        self.command._create_github_repo()

        expected_calls = [
            call(
                [
                    "gh",
                    "repo",
                    "create",
                    "test-repo",
                    "--public",
                    "--confirm",
                    "--description",
                    "Test repository",
                ],
                check=True,
            ),
            call(
                ["gh", "api", "user", "--jq", ".login"],
                capture_output=True,
                text=True,
                check=True,
            ),
            call(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    "https://github.com/testuser/test-repo.git",
                ],
                check=True,
            ),
        ]
        mock_run.assert_has_calls(expected_calls)

    @patch("subprocess.run")
    def test_configure_repo_with_topics(self, mock_run):
        """Test repository configuration with topics."""
        mock_run.return_value = MagicMock(returncode=0)

        self.command._configure_repo()

        # Should be called once for each topic
        expected_calls = [
            call(["gh", "repo", "edit", "--add-topic", "python"], check=True),
            call(["gh", "repo", "edit", "--add-topic", "test"], check=True),
        ]
        mock_run.assert_has_calls(expected_calls)

    @patch("subprocess.run")
    def test_error_handling(self, mock_run):
        """Test error handling during execution."""
        mock_run.side_effect = Exception("Test error")

        with self.assertRaises(Exception) as context:
            self.command.execute()

        self.assertEqual(str(context.exception), "Test error")

    @patch("subprocess.run")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_workflows(self, mock_file, mock_mkdir, mock_run):
        """Test GitHub Actions workflow creation."""
        mock_run.return_value = MagicMock(returncode=0)

        self.command._create_github_workflows()

        # Verify .github/workflows directory creation
        mock_mkdir.assert_called()

        # Verify CI workflow creation
        self.assertTrue(any("ci.yml" in str(call) for call in mock_file.call_args_list))

    @patch("subprocess.run")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_docusaurus_website(self, mock_file, mock_mkdir, mock_run):
        """Test Docusaurus website initialization."""
        # Create command with website option enabled
        website_options = GitHubInitOptions(repo_name="test-site", create_website=True)
        website_command = GitHubInitCommand(website_options)

        mock_run.return_value = MagicMock(returncode=0)

        website_command._initialize_docusaurus()

        # Verify multiple directories are created
        mock_mkdir.assert_called()

        # Verify Docusaurus files are created
        created_files = [str(call) for call in mock_file.call_args_list]
        self.assertTrue(any("package.json" in file for file in created_files))
        self.assertTrue(any("docusaurus.config.js" in file for file in created_files))
        self.assertTrue(any("sidebars.js" in file for file in created_files))
        self.assertTrue(any("intro.md" in file for file in created_files))

    @patch("subprocess.run")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_docusaurus_workflows_created(self, mock_file, mock_mkdir, mock_run):
        """Test that Docusaurus deployment workflows are created when website is enabled."""
        website_options = GitHubInitOptions(repo_name="test-site", create_website=True)
        website_command = GitHubInitCommand(website_options)

        mock_run.return_value = MagicMock(returncode=0)

        website_command._create_github_workflows()

        # Verify deployment workflows are created
        created_files = [str(call) for call in mock_file.call_args_list]
        self.assertTrue(any("deploy-docusaurus.yml" in file for file in created_files))
        self.assertTrue(any("pr-preview.yml" in file for file in created_files))


class TestHandleGitHubInitCommand(unittest.TestCase):
    """Test the command handler function."""

    @patch("github_init_command.GitHubInitCommand")
    def test_handle_command_success(self, mock_command_class):
        """Test successful command handling."""
        mock_command = MagicMock()
        mock_command_class.return_value = mock_command

        handle_github_init_command(["test-repo", "--public", "--license", "MIT"])

        mock_command_class.assert_called_once()
        mock_command.execute.assert_called_once()

    @patch("github_init_command.GitHubInitCommand")
    def test_handle_command_with_error(self, mock_command_class):
        """Test command handling with execution error."""
        mock_command = MagicMock()
        mock_command.execute.side_effect = Exception("Execution failed")
        mock_command_class.return_value = mock_command

        with self.assertRaises(Exception):
            handle_github_init_command(["test-repo"])


if __name__ == "__main__":
    unittest.main()
