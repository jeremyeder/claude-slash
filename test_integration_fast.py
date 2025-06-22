#!/usr/bin/env python3
"""Fast integration tests with all external dependencies mocked."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from github_init_command import GitHubInitCommand, GitHubInitOptions


class TestFastIntegration(unittest.TestCase):
    """Fast integration tests with comprehensive mocking."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)

    @patch("subprocess.run")
    @patch("os.chdir")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_full_repo_creation_private(
        self, mock_file, mock_exists, mock_mkdir, mock_chdir, mock_run
    ):
        """Test complete private repository creation flow."""
        # Setup mocks
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)

        options = GitHubInitOptions(
            repo_name="test-private-repo",
            description="A test private repository",
            private=True,
            license="MIT",
            gitignore="python",
            readme=True,
            topics=["test", "python"],
        )

        command = GitHubInitCommand(options)
        command.execute()

        # Verify directory operations
        mock_mkdir.assert_called()
        mock_chdir.assert_called()

        # Verify git operations
        git_calls = [call for call in mock_run.call_args_list if "git" in str(call)]
        self.assertTrue(any("'git', 'init'" in str(call) for call in git_calls))
        self.assertTrue(any("'git', 'add'" in str(call) for call in git_calls))
        self.assertTrue(any("'git', 'commit'" in str(call) for call in git_calls))

        # Verify GitHub repo creation
        gh_calls = [call for call in mock_run.call_args_list if "gh" in str(call)]
        self.assertTrue(any("--private" in str(call) for call in gh_calls))

        # Verify file creation
        file_calls = [str(call) for call in mock_file.call_args_list]
        self.assertTrue(any("README.md" in call for call in file_calls))
        self.assertTrue(any(".gitignore" in call for call in file_calls))
        self.assertTrue(any("LICENSE" in call for call in file_calls))
        self.assertTrue(any("ci.yml" in call for call in file_calls))

    @patch("subprocess.run")
    @patch("os.chdir")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_full_repo_with_website(
        self, mock_json, mock_file, mock_exists, mock_mkdir, mock_chdir, mock_run
    ):
        """Test complete repository creation with Docusaurus website."""
        # Setup mocks
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)

        options = GitHubInitOptions(
            repo_name="test-docs-repo",
            description="A test documentation repository",
            private=False,  # Public for docs
            license="MIT",
            gitignore="node",
            readme=True,
            create_website=True,
            topics=["docs", "docusaurus"],
        )

        command = GitHubInitCommand(options)
        command.execute()

        # Verify Docusaurus files were created
        file_calls = [str(call) for call in mock_file.call_args_list]
        self.assertTrue(any("package.json" in call for call in file_calls))
        self.assertTrue(any("docusaurus.config.js" in call for call in file_calls))
        self.assertTrue(any("sidebars.js" in call for call in file_calls))
        self.assertTrue(any("intro.md" in call for call in file_calls))

        # Verify Docusaurus workflows were created
        self.assertTrue(any("deploy-docusaurus.yml" in call for call in file_calls))
        self.assertTrue(any("pr-preview.yml" in call for call in file_calls))

        # Verify GitHub repo creation as public
        gh_calls = [call for call in mock_run.call_args_list if "gh" in str(call)]
        self.assertTrue(any("--public" in str(call) for call in gh_calls))

        # Verify package.json was written
        mock_json.assert_called()

    @patch("subprocess.run")
    @patch("os.chdir")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_minimal_repo_creation(
        self, mock_file, mock_exists, mock_mkdir, mock_chdir, mock_run
    ):
        """Test minimal repository creation with defaults."""
        # Setup mocks
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)

        options = GitHubInitOptions(repo_name="minimal-repo")
        command = GitHubInitCommand(options)
        command.execute()

        # Verify minimal setup
        self.assertTrue(mock_mkdir.called)
        self.assertTrue(mock_chdir.called)
        self.assertTrue(mock_run.called)

        # Should create CI workflow even for minimal repo
        file_calls = [str(call) for call in mock_file.call_args_list]
        self.assertTrue(any("ci.yml" in call for call in file_calls))

        # Should create README by default
        self.assertTrue(any("README.md" in call for call in file_calls))

    @patch("subprocess.run")
    def test_error_handling_subprocess_failure(self, mock_run):
        """Test error handling when subprocess commands fail."""
        mock_run.side_effect = Exception("Command failed")

        options = GitHubInitOptions(repo_name="error-repo")
        command = GitHubInitCommand(options)

        with self.assertRaises(Exception) as context:
            command.execute()

        self.assertIn("Command failed", str(context.exception))

    @patch("subprocess.run")
    @patch("os.chdir")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("builtins.open")
    def test_file_creation_error_handling(
        self, mock_file, mock_exists, mock_mkdir, mock_chdir, mock_run
    ):
        """Test error handling when file creation fails."""
        # Setup mocks
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)
        mock_file.side_effect = IOError("Cannot write file")

        options = GitHubInitOptions(repo_name="file-error-repo")
        command = GitHubInitCommand(options)

        with self.assertRaises(Exception):
            command.execute()


class TestFastWorkflowContent(unittest.TestCase):
    """Test workflow content generation without file I/O."""

    def setUp(self):
        """Set up test fixtures."""
        self.command = GitHubInitCommand(GitHubInitOptions(repo_name="test"))

    def test_python_workflow_comprehensive(self):
        """Test Python workflow contains all expected elements."""
        content = self.command._get_python_ci_workflow()

        # Check essential CI elements
        essential_elements = [
            "name: CI",
            "on:",
            "pull_request:",
            "push:",
            "jobs:",
            "runs-on: ubuntu-latest",
            "actions/checkout@v4",
            "actions/setup-python@v4",
            "python-version:",
            "pip install",
            "Cache pip dependencies",
            "flake8",
            "mypy",
            "pytest",
            "codecov",
        ]

        for element in essential_elements:
            self.assertIn(element, content, f"Missing element: {element}")

    def test_node_workflow_comprehensive(self):
        """Test Node.js workflow contains all expected elements."""
        content = self.command._get_node_ci_workflow()

        essential_elements = [
            "name: CI",
            "node-version:",
            "actions/setup-node@v4",
            "npm ci",
            "cache:",
            "npm run",
        ]

        for element in essential_elements:
            self.assertIn(element, content, f"Missing element: {element}")

    def test_docusaurus_deploy_workflow(self):
        """Test Docusaurus deployment workflow content."""
        command = GitHubInitCommand(
            GitHubInitOptions(repo_name="test", create_website=True)
        )

        with patch("builtins.open", mock_open()) as mock_file:
            command._create_docusaurus_deploy_workflow()

        # Verify file was created
        mock_file.assert_called_with(".github/workflows/deploy-docusaurus.yml", "w")

        # Get the written content
        written_content = mock_file().write.call_args[0][0]

        essential_elements = [
            "Deploy Docusaurus to GitHub Pages",
            "pages: write",
            "npm ci",
            "npm run build",
            "actions/deploy-pages@v4",
        ]

        for element in essential_elements:
            self.assertIn(element, written_content, f"Missing element: {element}")


if __name__ == "__main__":
    # Run with minimal output for speed
    unittest.main(verbosity=1, buffer=True, failfast=True)
