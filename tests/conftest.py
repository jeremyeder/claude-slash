"""Pytest configuration and fixtures for claude-slash tests."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from pytest_subprocess import FakeProcess


@pytest.fixture
def temp_git_repo() -> Generator[Path, None, None]:
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)

        # Initialize git repo
        os.chdir(repo_path)
        os.system("git init")
        os.system("git config user.name 'Test User'")
        os.system("git config user.email 'test@example.com'")

        # Create basic file structure
        (repo_path / ".claude").mkdir()

        yield repo_path


@pytest.fixture
def mock_git_operations(fp: FakeProcess) -> FakeProcess:
    """Mock common git operations."""
    # Mock git rev-parse --show-toplevel
    fp.register_subprocess(
        ["git", "rev-parse", "--show-toplevel"], stdout="/tmp/test-repo"
    )

    # Mock git status
    fp.register_subprocess(
        ["git", "status", "--porcelain"], stdout=" M file1.py\n?? file2.py"
    )

    # Mock git add
    fp.register_subprocess(["git", "add", "."], returncode=0)

    # Mock git commit
    fp.register_subprocess(
        ["git", "commit", "-m", fp.any()],
        returncode=0,
        stdout="[main abc1234] Test commit",
    )

    # Mock git log
    fp.register_subprocess(
        ["git", "log", "--oneline", "-10"],
        stdout="abc1234 Test commit\ndef5678 Previous commit",
    )

    return fp


@pytest.fixture
def mock_gh_operations(fp: FakeProcess) -> FakeProcess:
    """Mock GitHub CLI operations."""
    # Mock gh auth status
    fp.register_subprocess(
        ["gh", "auth", "status"],
        returncode=0,
        stdout="✓ Logged in to github.com as testuser",
    )

    # Mock gh repo view
    fp.register_subprocess(
        ["gh", "repo", "view", "--json", "name,owner"],
        stdout='{"name": "test-repo", "owner": {"login": "testuser"}}',
    )

    return fp




@pytest.fixture
def mock_subprocess_calls(fp: FakeProcess) -> FakeProcess:
    """Mock all subprocess calls for comprehensive testing."""
    # Combine git and gh mocks
    fp.register_subprocess(
        ["git", "rev-parse", "--show-toplevel"], stdout="/tmp/test-repo"
    )

    fp.register_subprocess(
        ["git", "status", "--porcelain"], stdout=" M file1.py\n?? file2.py"
    )

    fp.register_subprocess(["git", "add", "."], returncode=0)

    fp.register_subprocess(["git", "commit", "-m", fp.any()], returncode=0)

    fp.register_subprocess(["gh", "auth", "status"], returncode=0)

    return fp
