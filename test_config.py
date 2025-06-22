#!/usr/bin/env python3
"""Tests for configuration file functionality."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from github_init_command import load_config_defaults, parse_arguments, GitHubInitOptions


class TestConfigurationLoading(unittest.TestCase):
    """Test configuration file loading and validation."""

    @patch('github_init_command.yaml')
    def test_load_config_no_file(self, mock_yaml):
        """Test behavior when config file doesn't exist."""
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=False):
                config = load_config_defaults()
                self.assertEqual(config, {})

    @patch('github_init_command.yaml')
    def test_load_config_no_yaml_module(self, mock_yaml):
        """Test behavior when PyYAML is not installed."""
        with patch('github_init_command.yaml', None):
            with patch('pathlib.Path.home') as mock_home:
                mock_home.return_value = Path('/fake/home')
                with patch('pathlib.Path.exists', return_value=True):
                    config = load_config_defaults()
                    self.assertEqual(config, {})

    @patch('github_init_command.yaml')
    def test_load_valid_config(self, mock_yaml):
        """Test loading valid configuration file."""
        valid_config = {
            'description': 'Default description',
            'private': False,
            'license': 'MIT',
            'gitignore': 'python',
            'readme': True,
            'default_branch': 'develop',
            'topics': ['python', 'cli'],
            'create_website': True,
            'enable_dependabot': False
        }
        
        mock_yaml.safe_load.return_value = valid_config
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', mock_open()):
                    config = load_config_defaults()
                    
                    self.assertEqual(config, valid_config)

    @patch('github_init_command.yaml')
    def test_load_config_with_invalid_keys(self, mock_yaml):
        """Test loading config with invalid keys filters them out."""
        config_with_invalid = {
            'license': 'MIT',
            'invalid_key': 'should_be_filtered',
            'another_invalid': 'also_filtered',
            'gitignore': 'python'
        }
        
        mock_yaml.safe_load.return_value = config_with_invalid
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', mock_open()):
                    config = load_config_defaults()
                    
                    # Should only contain valid keys
                    self.assertEqual(config, {
                        'license': 'MIT',
                        'gitignore': 'python'
                    })

    @patch('github_init_command.yaml')
    def test_load_config_yaml_error(self, mock_yaml):
        """Test handling of YAML parsing errors."""
        mock_yaml.safe_load.side_effect = mock_yaml.YAMLError("Invalid YAML")
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', mock_open()):
                    config = load_config_defaults()
                    self.assertEqual(config, {})


class TestConfigurationIntegration(unittest.TestCase):
    """Test configuration integration with argument parsing."""

    @patch('github_init_command.load_config_defaults')
    def test_cli_with_config_defaults(self, mock_load_config):
        """Test CLI mode uses config defaults when flags not provided."""
        mock_load_config.return_value = {
            'description': 'Config description',
            'license': 'MIT',
            'gitignore': 'python',
            'private': False,
            'topics': ['config', 'test']
        }
        
        options = parse_arguments(['test-repo'])
        
        self.assertEqual(options.repo_name, 'test-repo')
        self.assertEqual(options.description, 'Config description')
        self.assertEqual(options.license, 'MIT')
        self.assertEqual(options.gitignore, 'python')
        self.assertFalse(options.private)
        self.assertEqual(options.topics, ['config', 'test'])

    @patch('github_init_command.load_config_defaults')
    def test_cli_flags_override_config(self, mock_load_config):
        """Test CLI flags override config defaults."""
        mock_load_config.return_value = {
            'description': 'Config description',
            'license': 'MIT',
            'private': False
        }
        
        options = parse_arguments([
            'test-repo', 
            '--desc', 'CLI description',
            '--license', 'Apache-2.0'
        ])
        
        self.assertEqual(options.repo_name, 'test-repo')
        self.assertEqual(options.description, 'CLI description')  # CLI overrides config
        self.assertEqual(options.license, 'Apache-2.0')  # CLI overrides config
        self.assertFalse(options.private)  # From config (no CLI flag)

    @patch('github_init_command.get_interactive_options')
    def test_interactive_mode_loads_config(self, mock_interactive):
        """Test interactive mode loads and uses config defaults."""
        mock_interactive.return_value = GitHubInitOptions(repo_name='test')
        
        # Trigger interactive mode
        parse_arguments([])
        
        # Interactive function should be called
        mock_interactive.assert_called_once()


class TestConfigurationEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    @patch('github_init_command.yaml')
    def test_empty_config_file(self, mock_yaml):
        """Test handling of empty config file."""
        mock_yaml.safe_load.return_value = None
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', mock_open()):
                    config = load_config_defaults()
                    self.assertEqual(config, {})

    @patch('github_init_command.yaml')
    def test_config_file_io_error(self, mock_yaml):
        """Test handling of file I/O errors."""
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', side_effect=IOError("Permission denied")):
                    config = load_config_defaults()
                    self.assertEqual(config, {})

    @patch('github_init_command.yaml')
    def test_config_topics_validation(self, mock_yaml):
        """Test that topics are properly handled as lists."""
        mock_yaml.safe_load.return_value = {
            'topics': ['python', 'cli', 'tool']
        }
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/fake/home')
            with patch('pathlib.Path.exists', return_value=True):
                with patch('builtins.open', mock_open()):
                    config = load_config_defaults()
                    
                    self.assertEqual(config['topics'], ['python', 'cli', 'tool'])
                    self.assertIsInstance(config['topics'], list)


if __name__ == '__main__':
    unittest.main(verbosity=2)