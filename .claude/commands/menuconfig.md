# CLAUDE.md Configuration Tool

Interactive menuconfig-style editor for CLAUDE.md files with Linux kernel menuconfig look and feel.

## Usage
```
/menuconfig [file]
```

## Description
Provides a text-based user interface similar to Linux kernel menuconfig for managing CLAUDE.md file sections. Navigate with arrow keys, toggle sections with space, search with '/', and save with 'S'.

Features:
- TreeView navigation of CLAUDE.md sections
- Enable/disable sections with visual indicators
- Linux kernel menuconfig-style interface
- Search functionality
- Backup and restore capabilities
- Support for both project and global CLAUDE.md files

## Implementation

!#!/bin/bash
!
!# CLAUDE.md menuconfig-style editor
!set -e
!
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!scripts_dir="$git_root/.claude/scripts"
!
!# Determine target CLAUDE.md file
!if [[ -n "$ARGUMENTS" ]]; then
!    claude_file="$ARGUMENTS"
!else
!    # Default to project CLAUDE.md, fallback to global
!    if [[ -f "$git_root/CLAUDE.md" ]]; then
!        claude_file="$git_root/CLAUDE.md"
!    else
!        claude_file="$HOME/.claude/CLAUDE.md"
!    fi
!fi
!
!# Ensure the target file exists
!if [[ ! -f "$claude_file" ]]; then
!    echo "Error: CLAUDE.md file not found at: $claude_file"
!    echo "Available options:"
!    [[ -f "$git_root/CLAUDE.md" ]] && echo "  - Project: $git_root/CLAUDE.md"
!    [[ -f "$HOME/.claude/CLAUDE.md" ]] && echo "  - Global: $HOME/.claude/CLAUDE.md"
!    exit 1
!fi
!
!# Ensure scripts directory exists
!mkdir -p "$scripts_dir"
!
!# Check if Python script exists, create if needed
!python_script="$scripts_dir/claude_menuconfig.py"
!if [[ ! -f "$python_script" ]]; then
!    echo "Creating CLAUDE.md menuconfig script..."
!    # Script will be created by the implementation
!fi
!
!# Ensure required Python packages are available using uv
!venv_dir=".venv"
!
!# Check if uv is available, fallback to pip
!if command -v uv >/dev/null 2>&1; then
!    # Use uv for fast dependency management
!    if [[ ! -d "$venv_dir" ]]; then
!        echo "Creating Python virtual environment for menuconfig with uv..."
!        uv venv "$venv_dir"
!    fi
!
!    # Check if textual is installed
!    if ! "$venv_dir/bin/python" -c "import textual" 2>/dev/null; then
!        echo "Installing textual using uv..."
!        uv pip install --python "$venv_dir/bin/python" textual
!    fi
!
!    python_exe="$venv_dir/bin/python"
!else
!    # Fallback to traditional pip
!    if [[ ! -d "$venv_dir" ]]; then
!        echo "Creating Python virtual environment for menuconfig..."
!        python3 -m venv "$venv_dir"
!    fi
!
!    source "$venv_dir/bin/activate"
!
!    if ! python -c "import textual" 2>/dev/null; then
!        echo "Installing textual using pip..."
!        pip install textual
!    fi
!
!    python_exe="python"
!fi
!
!# Run the menuconfig interface
!echo "Starting CLAUDE.md menuconfig for: $claude_file"
!"$python_exe" "$python_script" "$claude_file"
