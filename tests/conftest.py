"""
pytest configuration and fixtures for claude-slash tests.

This module provides fixtures for subprocess mocking, git operations,
and test environment setup.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import Mock

import pytest
from pytest_subprocess import FakeProcess


@pytest.fixture
def temp_git_repo() -> Generator[Path, None, None]:
    """
    Create a temporary git repository for testing.
    
    Yields:
        Path to the temporary git repository
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Initialize git repo
        os.chdir(repo_path)
        os.system("git init")
        os.system("git config user.name 'Test User'")
        os.system("git config user.email 'test@example.com'")
        
        yield repo_path


@pytest.fixture
def mock_git_operations(fp: FakeProcess) -> FakeProcess:
    """
    Mock common git operations using pytest-subprocess.
    
    Args:
        fp: FakeProcess fixture from pytest-subprocess
        
    Returns:
        Configured FakeProcess instance
    """
    # Mock git status
    fp.register_subprocess(
        ["git", "status", "--porcelain"],
        stdout="",
        returncode=0
    )
    
    # Mock git rev-parse --show-toplevel
    fp.register_subprocess(
        ["git", "rev-parse", "--show-toplevel"],
        stdout="/fake/repo/path",
        returncode=0
    )
    
    # Mock git add
    fp.register_subprocess(
        ["git", "add", fp.any()],
        stdout="",
        returncode=0
    )
    
    # Mock git commit
    fp.register_subprocess(
        ["git", "commit", "-m", fp.any()],
        stdout="[main abc1234] Test commit",
        returncode=0
    )
    
    # Mock git log
    fp.register_subprocess(
        ["git", "log", "--oneline", "-10"],
        stdout="abc1234 Test commit\ndef5678 Previous commit",
        returncode=0
    )
    
    return fp


@pytest.fixture
def mock_gh_operations(fp: FakeProcess) -> FakeProcess:
    """
    Mock GitHub CLI operations using pytest-subprocess.
    
    Args:
        fp: FakeProcess fixture from pytest-subprocess
        
    Returns:
        Configured FakeProcess instance
    """
    # Mock gh auth status
    fp.register_subprocess(
        ["gh", "auth", "status"],
        stdout="Logged in to github.com as testuser",
        returncode=0
    )
    
    # Mock gh repo view
    fp.register_subprocess(
        ["gh", "repo", "view", "--json", "name,owner"],
        stdout='{"name":"test-repo","owner":{"login":"testuser"}}',
        returncode=0
    )
    
    return fp


@pytest.fixture
def mock_subprocess_all(mock_git_operations: FakeProcess, mock_gh_operations: FakeProcess) -> FakeProcess:
    """
    Fixture that combines all subprocess mocking.
    
    Args:
        mock_git_operations: Git operations mock
        mock_gh_operations: GitHub CLI operations mock
        
    Returns:
        Combined FakeProcess instance
    """
    return mock_git_operations


@pytest.fixture
def claude_checkpoints_dir(temp_git_repo: Path) -> Path:
    """
    Create .claude/checkpoints directory structure for testing.
    
    Args:
        temp_git_repo: Temporary git repository path
        
    Returns:
        Path to .claude/checkpoints directory
    """
    checkpoints_dir = temp_git_repo / ".claude" / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    return checkpoints_dir


@pytest.fixture
def sample_checkpoint_data() -> dict:
    """
    Provide sample checkpoint data for testing.
    
    Returns:
        Dictionary with sample checkpoint data
    """
    return {
        "timestamp": "2024-01-01T12:00:00Z",
        "git_hash": "abc1234567890",
        "branch": "main",
        "files_changed": ["file1.py", "file2.py"],
        "message": "Test checkpoint"
    }


@pytest.fixture(autouse=True)
def reset_working_directory():
    """
    Automatically reset working directory after each test.
    """
    original_cwd = os.getcwd()
    yield
    os.chdir(original_cwd)


@pytest.fixture
def console_mock() -> Mock:
    """
    Mock the Rich console for testing output.
    
    Returns:
        Mock console object
    """
    return Mock()