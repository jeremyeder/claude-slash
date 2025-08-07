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
        self.assertTrue(options.enable_dependabot)  # Default enabled
        
        # Test new automation defaults
        self.assertTrue(options.create_project)  # Default enabled
        self.assertEqual(options.project_template, "development")  # Default template
        self.assertTrue(options.enable_auto_version)  # Default enabled
        self.assertTrue(options.enable_auto_merge)  # Default enabled
        self.assertTrue(options.enable_auto_release)  # Default enabled
        self.assertFalse(options.enable_claude_review)  # Default disabled

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
            enable_dependabot=False,
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
        self.assertFalse(options.enable_dependabot)


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

    def test_project_flags(self):
        """Test GitHub project-related flags."""
        # Test --no-project flag
        options = parse_arguments(["repo", "--no-project"])
        self.assertFalse(options.create_project)
        
        # Test --project-template flag
        options = parse_arguments(["repo", "--project-template", "basic"])
        self.assertEqual(options.project_template, "basic")
        
        # Test default project template
        options = parse_arguments(["repo"])
        self.assertEqual(options.project_template, "development")

    def test_automation_flags(self):
        """Test advanced automation flags."""
        # Test --no-auto-version flag
        options = parse_arguments(["repo", "--no-auto-version"])
        self.assertFalse(options.enable_auto_version)
        
        # Test --no-auto-merge flag
        options = parse_arguments(["repo", "--no-auto-merge"])
        self.assertFalse(options.enable_auto_merge)
        
        # Test --enable-claude-review flag
        options = parse_arguments(["repo", "--enable-claude-review"])
        self.assertTrue(options.enable_claude_review)
        
        # Test --no-auto-release flag
        options = parse_arguments(["repo", "--no-auto-release"])
        self.assertFalse(options.enable_auto_release)

    def test_automation_defaults(self):
        """Test that automation features are enabled by default."""
        options = parse_arguments(["repo"])
        self.assertTrue(options.create_project)
        self.assertTrue(options.enable_auto_version)
        self.assertTrue(options.enable_auto_merge)
        self.assertTrue(options.enable_auto_release)
        self.assertFalse(options.enable_claude_review)  # Disabled by default

    def test_no_dependabot_flag(self):
        """Test --no-dependabot flag."""
        options = parse_arguments(["repo", "--no-dependabot"])
        self.assertFalse(options.enable_dependabot)

    def test_dependabot_default_enabled(self):
        """Test dependabot is enabled by default."""
        options = parse_arguments(["repo"])
        self.assertTrue(options.enable_dependabot)

    def test_dry_run_flag(self):
        """Test --dry-run flag."""
        options = parse_arguments(["repo", "--dry-run"])
        self.assertTrue(options.dry_run)

    def test_dry_run_default_disabled(self):
        """Test dry-run is disabled by default."""
        options = parse_arguments(["repo"])
        self.assertFalse(options.dry_run)

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

    def test_dependabot_config_content(self):
        """Test dependabot configuration generation."""
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test", 
            gitignore="python",
            enable_dependabot=True
        ))
        
        with patch("pathlib.Path.mkdir"), patch("builtins.open", mock_open()) as mock_file:
            command._create_dependabot_config()
        
        mock_file.assert_called_with(".github/dependabot.yml", "w")
        written_content = mock_file().write.call_args[0][0]
        
        self.assertIn("version: 2", written_content)
        self.assertIn("github-actions", written_content)
        self.assertIn("pip", written_content)
        self.assertIn("weekly", written_content)

    def test_dry_run_execution(self):
        """Test dry-run mode executes preview without side effects."""
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test-dry",
            dry_run=True,
            license="MIT",
            gitignore="python"
        ))
        
        # Should not raise any exceptions and not create files
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            with patch("builtins.open", mock_open()) as mock_file:
                command.execute()
                
                # No actual file operations should occur in dry-run
                mock_mkdir.assert_not_called()
                mock_file.assert_not_called()

    def test_rust_workflow_content(self):
        """Test Rust CI workflow generation."""
        content = self.command._get_rust_ci_workflow()

        self.assertIn("dtolnay/rust-toolchain", content)
        self.assertIn("cargo fmt", content)
        self.assertIn("cargo clippy", content)
        self.assertIn("cargo test", content)
        self.assertIn("cargo build", content)
        self.assertIn("rustfmt, clippy", content)

    def test_go_workflow_content(self):
        """Test Go CI workflow generation."""
        content = self.command._get_go_ci_workflow()

        self.assertIn("actions/setup-go", content)
        self.assertIn("go mod download", content)
        self.assertIn("gofmt", content)
        self.assertIn("golangci-lint", content)
        self.assertIn("go test", content)
        self.assertIn("go build", content)

    def test_java_workflow_content(self):
        """Test Java CI workflow generation."""
        content = self.command._get_java_ci_workflow()

        self.assertIn("actions/setup-java", content)
        self.assertIn("temurin", content)
        self.assertIn("mvnw", content)
        self.assertIn("mvn", content)
        self.assertIn("surefire-reports", content)

    def test_csharp_workflow_content(self):
        """Test C#/.NET CI workflow generation."""
        content = self.command._get_csharp_ci_workflow()

        self.assertIn("actions/setup-dotnet", content)
        self.assertIn("dotnet restore", content)
        self.assertIn("dotnet build", content)
        self.assertIn("dotnet test", content)
        self.assertIn("codecov", content)

    def test_auto_version_workflow_content(self):
        """Test auto-version workflow generation."""
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test", enable_auto_version=True
        ))
        
        with patch("builtins.open", mock_open()) as mock_file:
            command._create_auto_version_workflow()
            
            # Verify workflow file is created
            mock_file.assert_called_with(".github/workflows/auto-version.yml", "w")
            
            # Get the written content
            written_content = mock_file().write.call_args[0][0]
            self.assertIn("name: Auto Version", written_content)
            self.assertIn("version increment", written_content.lower())
            self.assertIn("workflow_dispatch", written_content)

    def test_automerge_workflow_content(self):
        """Test automerge workflow generation.""" 
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test", enable_auto_merge=True
        ))
        
        with patch("builtins.open", mock_open()) as mock_file:
            command._create_automerge_workflow()
            
            # Verify workflow file is created
            mock_file.assert_called_with(".github/workflows/automerge.yml", "w")
            
            # Get the written content
            written_content = mock_file().write.call_args[0][0]
            self.assertIn("name: Dependabot Auto-Merge", written_content)
            self.assertIn("dependabot[bot]", written_content)
            self.assertIn("gh pr review --approve", written_content)

    def test_release_workflow_content(self):
        """Test release workflow generation."""
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test", enable_auto_release=True
        ))
        
        with patch("builtins.open", mock_open()) as mock_file:
            command._create_release_workflow()
            
            # Verify workflow file is created
            mock_file.assert_called_with(".github/workflows/release.yml", "w")
            
            # Get the written content
            written_content = mock_file().write.call_args[0][0]
            self.assertIn("name: Release", written_content)
            self.assertIn("tags:", written_content)
            self.assertIn("v*.*.*", written_content)

    def test_claude_review_workflows_content(self):
        """Test Claude AI review workflow generation."""
        command = GitHubInitCommand(GitHubInitOptions(
            repo_name="test", enable_claude_review=True
        ))
        
        with patch("builtins.open", mock_open()) as mock_file:
            command._create_claude_review_workflows()
            
            # Verify both workflow files are created
            expected_calls = [
                ".github/workflows/claude-code-review.yml",
                ".github/workflows/claude.yml"
            ]
            
            actual_calls = [call[0][0] for call in mock_file.call_args_list]
            for expected_call in expected_calls:
                self.assertIn(expected_call, actual_calls)


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
