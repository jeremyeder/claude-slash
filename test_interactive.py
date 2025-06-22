#!/usr/bin/env python3
"""Tests for interactive mode functionality."""

import unittest
from unittest.mock import patch, call
from github_init_command import (
    get_interactive_options,
    parse_arguments,
    GitHubInitOptions,
)


class TestInteractiveMode(unittest.TestCase):
    """Test interactive mode prompts and logic."""

    @patch("builtins.input")
    def test_interactive_minimal_options(self, mock_input):
        """Test interactive mode with minimal user input."""
        # Simulate user input: repo name, empty description, private (default), no license, etc.
        mock_input.side_effect = [
            "my-test-repo",  # repo name
            "",  # description (empty)
            "n",  # public? (n = private)
            "",  # license (empty)
            "",  # gitignore (empty)
            "y",  # create README (yes)
            "",  # default branch (empty = main)
            "",  # topics (empty)
            "n",  # create website (no)
            "y",  # confirm
        ]

        options = get_interactive_options()

        self.assertEqual(options.repo_name, "my-test-repo")
        self.assertIsNone(options.description)
        self.assertTrue(options.private)
        self.assertIsNone(options.license)
        self.assertIsNone(options.gitignore)
        self.assertTrue(options.readme)
        self.assertEqual(options.default_branch, "main")
        self.assertIsNone(options.topics)
        self.assertFalse(options.create_website)

    @patch("builtins.input")
    def test_interactive_full_options(self, mock_input):
        """Test interactive mode with all options specified."""
        mock_input.side_effect = [
            "full-featured-repo",  # repo name
            "A comprehensive test repository",  # description
            "y",  # public? (yes)
            "MIT",  # license
            "python",  # gitignore
            "y",  # create README (yes)
            "develop",  # default branch
            "python,testing,cli",  # topics
            "y",  # create website (yes)
            "y",  # confirm
        ]

        options = get_interactive_options()

        self.assertEqual(options.repo_name, "full-featured-repo")
        self.assertEqual(options.description, "A comprehensive test repository")
        self.assertFalse(options.private)  # public = True means private = False
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertTrue(options.readme)
        self.assertEqual(options.default_branch, "develop")
        self.assertEqual(options.topics, ["python", "testing", "cli"])
        self.assertTrue(options.create_website)

    @patch("builtins.input")
    def test_interactive_invalid_inputs_retry(self, mock_input):
        """Test that invalid inputs prompt for retry."""
        mock_input.side_effect = [
            "",  # empty repo name (invalid)
            "valid-repo",  # valid repo name
            "",  # description
            "maybe",  # invalid public response
            "y",  # valid public response
            "BadLicense",  # invalid license
            "MIT",  # valid license
            "invalid-lang",  # invalid gitignore
            "python",  # valid gitignore
            "maybe",  # invalid readme response
            "n",  # valid readme response
            "develop",  # branch name
            "test,example",  # topics
            "maybe",  # invalid website response
            "n",  # valid website response
            "y",  # confirm
        ]

        options = get_interactive_options()

        self.assertEqual(options.repo_name, "valid-repo")
        self.assertFalse(options.private)
        self.assertEqual(options.license, "MIT")
        self.assertEqual(options.gitignore, "python")
        self.assertFalse(options.readme)
        self.assertEqual(options.topics, ["test", "example"])
        self.assertFalse(options.create_website)

    @patch("builtins.exit")
    @patch("builtins.input")
    def test_interactive_abort_on_no_confirm(self, mock_input, mock_exit):
        """Test that user can abort during confirmation."""
        # Make exit actually raise SystemExit to stop execution
        mock_exit.side_effect = SystemExit(0)

        mock_input.side_effect = [
            "test-repo",  # repo name
            "",  # description
            "",  # private (default)
            "",  # license
            "",  # gitignore
            "",  # readme (default yes)
            "",  # branch (default main)
            "",  # topics
            "",  # website (default no)
            "n",  # do not confirm - should abort
        ]

        with self.assertRaises(SystemExit):
            get_interactive_options()

        mock_exit.assert_called_once_with(0)

    def test_parse_arguments_no_args_triggers_interactive(self):
        """Test that no arguments triggers interactive mode."""
        with patch("github_init_command.get_interactive_options") as mock_interactive:
            mock_interactive.return_value = GitHubInitOptions(repo_name="test")

            parse_arguments([])
            mock_interactive.assert_called_once()

    def test_parse_arguments_interactive_flag_triggers_interactive(self):
        """Test that --interactive flag triggers interactive mode."""
        with patch("github_init_command.get_interactive_options") as mock_interactive:
            mock_interactive.return_value = GitHubInitOptions(repo_name="test")

            parse_arguments(["--interactive"])
            mock_interactive.assert_called_once()

    def test_parse_arguments_with_repo_name_skips_interactive(self):
        """Test that providing repo name skips interactive mode."""
        with patch("github_init_command.get_interactive_options") as mock_interactive:

            options = parse_arguments(["test-repo"])

            mock_interactive.assert_not_called()
            self.assertEqual(options.repo_name, "test-repo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
