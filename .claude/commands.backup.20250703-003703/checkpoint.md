# Checkpoint Command

Create a checkpoint of the current Claude Code session state for restoration in future sessions.

## Usage

```bash
/project:checkpoint [description]
```

## Description

This command captures the current session state including:

- Git repository status and branch information
- Current todo list state
- Working directory context
- Session metadata

The checkpoint is saved to the git repository's `.claude/checkpoints/` directory with a timestamp.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
!checkpoint_dir="$git_root/.claude/checkpoints"
!checkpoint_file="$checkpoint_dir/checkpoint-$timestamp.json"

!mkdir -p "$checkpoint_dir"

!echo "Creating checkpoint at $checkpoint_file..."

!cat > "$checkpoint_file" << 'CHECKPOINT_EOF'
{
  "timestamp": "$(date -Iseconds)",
  "description": "$ARGUMENTS",
  "git_info": {
    "repository_root": "$(git rev-parse --show-toplevel 2>/dev/null || echo 'Not in git repo')",
    "current_branch": "$(git branch --show-current 2>/dev/null || echo 'N/A')",
    "commit_hash": "$(git rev-parse HEAD 2>/dev/null || echo 'N/A')",
    "status": "$(git status --porcelain 2>/dev/null || echo 'N/A')",
    "staged_files": "$(git diff --cached --name-only 2>/dev/null || echo 'N/A')",
    "modified_files": "$(git diff --name-only 2>/dev/null || echo 'N/A')",
    "untracked_files": "$(git ls-files --others --exclude-standard 2>/dev/null || echo 'N/A')"
  },
  "working_directory": "$(pwd)",
  "session_info": {
    "user": "$(whoami)",
    "hostname": "$(hostname)",
    "os": "$(uname -s)",
    "shell": "$SHELL"
  }
}
CHECKPOINT_EOF

!echo "Checkpoint created successfully!"
!echo "Location: $checkpoint_file"
!echo ""
!echo "To restore this checkpoint in a new Claude session:"
!echo "1. Navigate to: $git_root"
!if [ -f "$git_root/.git/config" ]; then
  !echo "2. Ensure you're on branch: $(git branch --show-current 2>/dev/null)"
  !if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    !echo "3. Note: Repository has uncommitted changes - review before restoring"
  !fi
!fi
!echo "4. Share the checkpoint file contents with Claude to restore context"

## Todo List Capture

Since Claude Code doesn't provide direct access to todo list state via shell commands,
include this instruction in your checkpoint restoration:

**Current Todo List State:**
*When restoring this checkpoint, ask Claude to read the todo list from the checkpoint
file if it was captured, or recreate the relevant todos based on the project state
at checkpoint time.*

## Notes

- Checkpoints are stored within the git repository for project-specific context
- Each checkpoint includes a timestamp for easy identification
- Git information is captured even if not in a git repository
- Todo list state should be manually communicated when restoring checkpoints
