# Restore (Short Alias)

Shorthand alias for the restore command.

## Usage

```bash
/project:rst [checkpoint_file]
```

This is an alias for `/project:restore`. See the main restore command for full documentation.

## Implementation

!checkpoint_file="$ARGUMENTS"
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!checkpoint_dir="$git_root/.claude/checkpoints"

!# If no checkpoint file specified, find the latest one
!if [ -z "$checkpoint_file" ]; then
!  latest_checkpoint=$(ls -t "$checkpoint_dir"/checkpoint-*.json 2>/dev/null | head -1)
!  if [ -z "$latest_checkpoint" ]; then
!    echo "❌ No checkpoints found in $checkpoint_dir"
!    echo "Create a checkpoint first with: /project:checkpoint"
!    exit 1
!  fi
!  checkpoint_file="$latest_checkpoint"
!  echo "📂 Using latest checkpoint: $(basename "$checkpoint_file")"
!else
!  # Handle relative paths
!  if [ ! -f "$checkpoint_file" ]; then
!    if [ -f "$checkpoint_dir/$checkpoint_file" ]; then
!      checkpoint_file="$checkpoint_dir/$checkpoint_file"
!    elif [ -f "$git_root/$checkpoint_file" ]; then
!      checkpoint_file="$git_root/$checkpoint_file"
!    else
!      echo "❌ Checkpoint file not found: $checkpoint_file"
!      exit 1
!    fi
!  fi
!fi

!echo "🔄 Restoring checkpoint: $(basename "$checkpoint_file")"
!echo ""

!# Validate JSON structure
!if command -v python3 &> /dev/null; then
!  if ! python3 -c "import json; json.load(open('$checkpoint_file'))" 2>/dev/null; then
!    echo "❌ Invalid checkpoint file format"
!    exit 1
!  fi
!fi

!# Extract checkpoint data
!checkpoint_timestamp=$(grep -o '"timestamp":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
!checkpoint_description=$(grep -o '"description":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
!checkpoint_branch=$(grep -o '"current_branch":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
!checkpoint_working_dir=$(grep -o '"working_directory":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
!checkpoint_commit=$(grep -o '"commit_hash":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)

!echo "📋 Checkpoint Information:"
!echo "   Timestamp: $checkpoint_timestamp"
!echo "   Description: $checkpoint_description"
!echo "   Branch: $checkpoint_branch"
!echo "   Working Directory: $checkpoint_working_dir"
!echo "   Commit: ${checkpoint_commit:0:8}"
!echo ""

!# Check current git state
!current_branch=$(git branch --show-current 2>/dev/null || echo "N/A")
!current_commit=$(git rev-parse HEAD 2>/dev/null || echo "N/A")
!git_status=$(git status --porcelain 2>/dev/null || echo "")

!# Safety check - warn about uncommitted changes
!if [ -n "$git_status" ]; then
!  echo "⚠️  WARNING: You have uncommitted changes in the current repository"
!  echo "   Current changes will be preserved, but may conflict with restoration"
!  echo ""
!  git status --short
!  echo ""
!  echo "💡 Consider creating a checkpoint of current state before proceeding"
!  echo "   Run: /project:checkpoint \"Before restore $(date)\""
!  echo ""
!fi

!# Switch to checkpoint branch if different and possible
!if [ "$checkpoint_branch" != "N/A" ] && [ "$checkpoint_branch" != "$current_branch" ]; then
!  if git show-ref --verify --quiet "refs/heads/$checkpoint_branch"; then
!    echo "🔀 Switching to branch: $checkpoint_branch"
!    git checkout "$checkpoint_branch"
!  else
!    echo "⚠️  Branch '$checkpoint_branch' not found in repository"
!    echo "   Staying on current branch: $current_branch"
!  fi
!fi

!# Navigate to checkpoint working directory
!if [ -d "$checkpoint_working_dir" ]; then
!  echo "📂 Navigating to: $checkpoint_working_dir"
!  cd "$checkpoint_working_dir"
!else
!  echo "⚠️  Working directory not found: $checkpoint_working_dir"
!  echo "   Staying in current directory: $(pwd)"
!fi

!echo ""
!echo "✅ Checkpoint restoration complete!"
!echo ""
!echo "🎯 Next Steps:"
!echo "1. Review the current repository state with: git status"
!echo "2. Check for any conflicts or missing files"
!echo "3. Recreate any todos that were active at checkpoint time"
!echo "4. Continue your work from where you left off"
!echo ""
!echo "💭 Checkpoint Context:"
!echo "   Share this checkpoint file with Claude to restore full session context:"
!echo "   cat \"$checkpoint_file\""
