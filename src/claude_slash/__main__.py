"""
Entry point for running claude-slash as a module with python -m claude_slash.

This eliminates the RuntimeWarning about module import behavior.
"""

from .main import app

if __name__ == "__main__":
    app()
