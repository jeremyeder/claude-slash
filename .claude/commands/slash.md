# Slash Commands Help

Display all available custom slash commands with descriptions and usage.

## Usage

```bash
/slash
```

## Description

This command displays a comprehensive list of all available claude-slash commands with their descriptions and usage examples. It dynamically scans the `.claude/commands/` directory to provide up-to-date information about installed commands.

## Implementation

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!echo -e "${BLUE}📋 Available Claude Slash Commands${NC}"
!echo -e "${BLUE}=================================${NC}"
!echo ""

!# Get the commands directory
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!commands_dir="$git_root/.claude/commands"

!# Check if commands directory exists
!if [ ! -d "$commands_dir" ]; then
!  commands_dir="$HOME/.claude/commands"
!  if [ ! -d "$commands_dir" ]; then
!    echo -e "${RED}❌ No claude-slash commands found${NC}"
!    echo "Install commands by downloading and running install.sh from:"
!    echo "https://github.com/jeremyeder/claude-slash"
!    exit 1
!  fi
!fi

!echo -e "${CYAN}Commands installed in: $commands_dir${NC}"
!echo ""

!# Function to extract command description from markdown file
!extract_description() {
!  local file="$1"
!  local description=""
!
!  # Try to get the first line after the title that contains descriptive text
!  description=$(sed -n '3p' "$file" | sed 's/^[[:space:]]*//')
!
!  # If that's empty or too short, look for the Description section
!  if [ -z "$description" ] || [ ${#description} -lt 10 ]; then
!    description=$(sed -n '/^## Description/,/^##/p' "$file" | sed -n '2p' | sed 's/^[[:space:]]*//' | head -c 80)
!  fi
!
!  # Fallback to a generic description if still empty
!  if [ -z "$description" ]; then
!    description="Custom claude-slash command"
!  fi
!
!  echo "$description"
!}

!# Function to extract usage from markdown file
!extract_usage() {
!  local file="$1"
!  local usage=""
!
!  # Look for usage in code blocks
!  usage=$(sed -n '/^```bash/,/^```/p' "$file" | sed -n '2p' | sed 's/^[[:space:]]*//')
!
!  # If not found, try without bash specifier
!  if [ -z "$usage" ]; then
!    usage=$(sed -n '/^```/,/^```/p' "$file" | sed -n '2p' | sed 's/^[[:space:]]*//')
!  fi
!
!  echo "$usage"
!}

!# Process all command files
!echo -e "${GREEN}Command${NC} | ${GREEN}Description${NC}"
!echo "---------|------------"
!
!for cmd_file in "$commands_dir"/*.md; do
!  if [ -f "$cmd_file" ]; then
!    filename=$(basename "$cmd_file" .md)
!
!    # Skip this help command to avoid recursion
!    if [ "$filename" = "slash" ]; then
!      continue
!    fi
!
!    description=$(extract_description "$cmd_file")
!    usage=$(extract_usage "$cmd_file")
!
!    # Format the command name
!    if [ -n "$usage" ]; then
!      cmd_display="$usage"
!    else
!      cmd_display="/$filename"
!    fi
!
!    # Truncate description if too long
!    if [ ${#description} -gt 60 ]; then
!      description="${description:0:57}..."
!    fi
!
!    echo -e "${CYAN}$cmd_display${NC} | $description"
!  fi
!done

!echo ""
!echo -e "${YELLOW}💡 Tips:${NC}"
!echo "• Type any command above to use it"
!echo "• Most commands have shorthand aliases (e.g., /ckpt for /checkpoint)"
!echo "• Use /learn to extract insights from your current session"
!echo "• Use /update to get the latest commands"
!echo ""
!echo -e "${BLUE}📖 For more information visit:${NC} https://github.com/jeremyeder/claude-slash"
