# Learn Command

Continuously refine the global CLAUDE.md file with impactful learnings from the current session.

## Usage

```bash
/project:learn [learning_description]
```

## Description

This command captures important insights, patterns, and learnings from the current Claude Code session and
intelligently integrates them into the global CLAUDE.md file. It focuses on:

- Strategic engineering insights and patterns
- Debugging techniques and troubleshooting approaches
- Development workflow improvements
- Tool usage and configuration learnings
- Process refinements and best practices

The command analyzes the current session context and adds the most impactful learnings to the appropriate
sections of the global CLAUDE.md file, avoiding duplication and ensuring high signal-to-noise ratio.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!claude_md_path="$HOME/.claude/CLAUDE.md"
!timestamp=$(date +"%Y-%m-%d %H:%M:%S")

!echo "Analyzing current session for learnings to integrate into global CLAUDE.md..."

!# Check if global CLAUDE.md exists
!if [ ! -f "$claude_md_path" ]; then
!  echo "Error: Global CLAUDE.md not found at $claude_md_path"
!  echo "Please ensure your global Claude configuration is set up correctly."
!  exit 1
!fi

!# Create a backup of the current CLAUDE.md
!backup_path="$HOME/.claude/CLAUDE.md.backup-$(date +%Y%m%d-%H%M%S)"
!cp "$claude_md_path" "$backup_path"
!echo "Created backup at: $backup_path"

!# Extract learning content from arguments
!learning_content="$ARGUMENTS"

!if [ -z "$learning_content" ]; then
!  echo "Please provide a learning description to add to CLAUDE.md"
!  echo "Usage: /project:learn [learning_description]"
!  exit 1
!fi

!# Create temporary file for the learning entry
!temp_learning="/tmp/claude_learning_$(date +%s).txt"

!cat > "$temp_learning" << LEARNING_EOF

## Session Learning - $timestamp

**Context**: $(basename "$git_root" 2>/dev/null || echo "Current session")

**Learning**: $learning_content

**Application**: This insight should be applied to future similar scenarios to improve efficiency and outcomes.

---

LEARNING_EOF

!echo "Learning captured and ready for integration:"
!echo ""
!cat "$temp_learning"
!echo ""

!# Prompt for integration guidance
!echo "This learning has been formatted for integration into your global CLAUDE.md file."
!echo "To complete the integration, you should:"
!echo ""
!echo "1. Review the learning content above"
!echo "2. Determine the most appropriate section in CLAUDE.md for this insight"
!echo "3. Manually integrate this learning to avoid duplication and ensure proper categorization"
!echo ""
!echo "Suggested integration sections:"
!echo "- Key Operating Principles (for workflow insights)"
!echo "- Pre-Push Linting Workflow (for development process learnings)"
!echo "- Test-Implementation Synchronization (for debugging/testing insights)"
!echo "- Strategic Tools & Methodologies (for strategic insights)"
!echo ""
!echo "Learning content saved temporarily at: $temp_learning"
!echo "Global CLAUDE.md backup created at: $backup_path"

!# Cleanup
!rm -f "$temp_learning"
