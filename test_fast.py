#!/usr/bin/env python3
"""Fast unit tests for GitHub Init command - optimized for speed."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from github_init_command import (GitHubInitCommand, GitHubInitOptions,
                                 handle_github_init_command, parse_arguments)


class TestFastGitHubInitOptions(unittest.TestCase):
    """Fast tests for GitHubInitOptions dataclass."""

    def test_default_options(self):
        """Test default option values."""
        options = GitHubInitOptions(repo_name="test-repo")

        self.assertEqual(options.repo_name, "test-repo")
        self.assertIsNone(options.description)
        self.assertTrue(options.private)
        self.assertIsNone(options.license)
        self.assertIsNone(options.gitignore)
        self.assertTrue(options.readme)
        self.assertEqual(options.default_branch, "main")
        self.assertIsNone(options.topics)
        self.assertFalse(options.create_website)

    def test_all_options(self):
        """Test all option combinations."""
        options = GitHubInitOptions(
            repo_name="test",
            description="desc",
            private=False,
            license="MIT",
            gitignore="python",
            readme=False,
            default_branch="dev",
            topics=["a", "b"],
            create_website=True,
        )

        self.assertEqual(options.repo_name, "test")
        self.assertEqual(options.description, "desc")
        self.assertFalse(options.private)
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertFalse(options.readme)
        self.assertEqual(options.default_branch, "dev")
        self.assertEqual(options.topics, ["a", "b"])
        self.assertTrue(options.create_website)


class TestFastArgumentParsing(unittest.TestCase):
    """Fast tests for argument parsing."""

    def test_minimal_args(self):
        """Test minimal argument parsing."""
        options = parse_arguments(["repo"])
        self.assertEqual(options.repo_name, "repo")
        self.assertTrue(options.private)
        self.assertFalse(options.create_website)

    def test_public_flag(self):
        """Test --public flag."""
        options = parse_arguments(["repo", "--public"])
        self.assertFalse(options.private)

    def test_website_flag(self):
        """Test --create-website flag."""
        options = parse_arguments(["repo", "--create-website"])
        self.assertTrue(options.create_website)

    def test_all_flags(self):
        """Test all flags together."""
        options = parse_arguments(
            [
                "repo",
                "--public",
                "--create-website",
                "--license",
                "MIT",
                "--gitignore",
                "python",
                "--desc",
                "test",
                "--topics",
                "a,b",
            ]
        )

        self.assertEqual(options.repo_name, "repo")
        self.assertFalse(options.private)
        self.assertTrue(options.create_website)
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertEqual(options.description, "test")
        self.assertEqual(options.topics, ["a", "b"])


class TestFastWorkflowGeneration(unittest.TestCase):
    """Fast tests for workflow content generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.options = GitHubInitOptions(repo_name="test")
        self.command = GitHubInitCommand(self.options)

    def test_python_workflow_content(self):
        """Test Python CI workflow generation."""
        content = self.command._get_python_ci_workflow()

        self.assertIn("python-version:", content)
        self.assertIn("pip install", content)
        self.assertIn("pytest", content)
        self.assertIn("flake8", content)
        self.assertIn("mypy", content)

    def test_docusaurus_workflow_content(self):
        """Test Docusaurus workflow contains all expected elements."""
        docusaurus_command = GitHubInitCommand(
            GitHubInitOptions(repo_name="test", create_website=True)
        )
        content = docusaurus_command._get_docusaurus_ci_workflow()

        self.assertIn("name: CI", content)
        self.assertIn("node-version: 20", content)
        self.assertIn("npm install", content)
        self.assertIn("npm run build", content)
        self.assertIn("test -d build", content)
        # Should not have cache setting to avoid lock file issues
        self.assertNotIn("cache:", content)

    def test_node_workflow_content(self):
        """Test Node.js CI workflow generation."""
        content = self.command._get_node_ci_workflow()

        self.assertIn("node-version:", content)
        self.assertIn("npm ci", content)
        self.assertIn("npm run", content)

    def test_generic_workflow_content(self):
        """Test generic CI workflow generation."""
        content = self.command._get_generic_ci_workflow()

        self.assertIn("runs-on: ubuntu-latest", content)
        self.assertIn("checkout@v4", content)
        self.assertIn("echo", content)


class TestFastFileCreation(unittest.TestCase):
    """Fast tests for file creation methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.options = GitHubInitOptions(
            repo_name="test-repo",
            description="Test description",
            license="MIT",
            gitignore="python",
        )
        self.command = GitHubInitCommand(self.options)

    @patch("builtins.open", new_callable=mock_open)
    def test_readme_creation(self, mock_file):
        """Test README content generation."""
        self.command._create_readme()

        mock_file.assert_called_once_with("README.md", "w")
        written_content = mock_file().write.call_args[0][0]

        self.assertIn("# test-repo", written_content)
        self.assertIn("Test description", written_content)
        self.assertIn("MIT License", written_content)

    def test_gitignore_templates(self):
        """Test gitignore template selection."""
        # Test Python template
        self.command.options.gitignore = "python"
        self.command._create_gitignore()

        # Test Node template
        self.command.options.gitignore = "node"
        self.command._create_gitignore()

        # Test generic template
        self.command.options.gitignore = "unknown"
        self.command._create_gitignore()

        # Should not raise exceptions
        self.assertTrue(True)

    @patch("builtins.open", new_callable=mock_open)
    def test_license_creation(self, mock_file):
        """Test license file creation."""
        self.command._create_license()

        mock_file.assert_called_once_with("LICENSE", "w")
        written_content = mock_file().write.call_args[0][0]

        self.assertIn("MIT License", written_content)
        self.assertIn("Copyright", written_content)


class TestFastCommandExecution(unittest.TestCase):
    """Fast tests for command execution."""

    @patch("github_init_command.GitHubInitCommand.execute")
    @patch("github_init_command.parse_arguments")
    def test_handle_command_success(self, mock_parse, mock_execute):
        """Test successful command handling."""
        mock_options = GitHubInitOptions(repo_name="test")
        mock_parse.return_value = mock_options

        handle_github_init_command(["test"])

        mock_parse.assert_called_once_with(["test"])
        mock_execute.assert_called_once()

    @patch("github_init_command.GitHubInitCommand.execute")
    @patch("github_init_command.parse_arguments")
    def test_handle_command_error(self, mock_parse, mock_execute):
        """Test command handling with error."""
        mock_options = GitHubInitOptions(repo_name="test")
        mock_parse.return_value = mock_options
        mock_execute.side_effect = Exception("Test error")

        with self.assertRaises(Exception):
            handle_github_init_command(["test"])


class TestFastDocusaurusGeneration(unittest.TestCase):
    """Fast tests for Docusaurus content generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.options = GitHubInitOptions(
            repo_name="test-docs", description="Test docs", create_website=True
        )
        self.command = GitHubInitCommand(self.options)

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_package_json_creation(self, mock_json_dump, mock_file, mock_mkdir):
        """Test package.json creation for Docusaurus."""
        with patch("pathlib.Path.exists", return_value=False):
            self.command._initialize_docusaurus()

        # Verify package.json was created
        mock_json_dump.assert_called()
        package_data = mock_json_dump.call_args[0][0]

        self.assertEqual(package_data["name"], "test-docs")
        self.assertIn("@docusaurus/core", package_data["dependencies"])
        self.assertIn("docusaurus", package_data["scripts"])


if __name__ == "__main__":
    # Run tests with minimal output for speed
    unittest.main(verbosity=1, buffer=True)
