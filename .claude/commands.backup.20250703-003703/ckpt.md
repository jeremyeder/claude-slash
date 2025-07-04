# Checkpoint (Short Alias)

Shorthand alias for the checkpoint command.

## Usage

```bash
/project:ckpt [description]
```

This is an alias for `/project:checkpoint`. See the main checkpoint command for full documentation.

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
