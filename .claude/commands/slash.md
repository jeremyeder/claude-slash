# Slash Commands

Main claude-slash command with help display and update functionality.

## Usage

```bash
/slash                # Show help and available commands
/slash help           # Show help and available commands
/slash update         # Update commands to latest release
```

## Description

This is the main claude-slash command that provides:

- **Help Mode**: Display all available commands with descriptions and usage examples
- **Update Mode**: Update your local claude-slash commands to the latest release from GitHub

The help mode dynamically scans the `.claude/commands/` directory to provide up-to-date information about installed commands.

## Implementation

!# CLAUDE_OUTPUT_MODE: DIRECT_TERMINAL
!# This command should output directly to terminal without Claude parsing or interpretation
!
!# Parse arguments for subcommand support
!subcommand="${ARGUMENTS%% *}"  # Get first argument
!if [ -z "$subcommand" ]; then
!    subcommand="help"
!fi

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!# Handle update subcommand
!if [ "$subcommand" = "update" ]; then
!    echo "🔄 Updating claude-slash commands..."
!    echo
!
!    # Determine installation location
!    install_dir=""
!    install_type=""
!
!    if [ -d ".claude/commands" ]; then
!        install_dir=".claude/commands"
!        install_type="project"
!    elif [ -d "$HOME/.claude/commands" ]; then
!        install_dir="$HOME/.claude/commands"
!        install_type="global"
!    else
!        echo "❌ No claude-slash installation found"
!        echo "Run the installer first:"
!        echo "curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh -o install.sh && bash install.sh"
!        exit 1
!    fi
!
!    echo "📍 Found $install_type installation at: $install_dir"
!
!    # Check for latest release
!    echo "🔍 Checking latest release..."
!    latest_info=$(curl -s "https://api.github.com/repos/jeremyeder/claude-slash/releases/latest")
!    if [ $? -ne 0 ]; then
!        echo "❌ Failed to check for updates (network error)"
!        exit 1
!    fi
!
!    latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
!
!    if [ -z "$latest_tag" ]; then
!        echo "❌ Could not determine latest version"
!        exit 1
!    fi
!
!    echo "📦 Latest release: $latest_tag"
!
!    # Create backup
!    backup_dir="$install_dir.backup.$(date +%Y%m%d-%H%M%S)"
!    echo "💾 Creating backup at: $backup_dir"
!    cp -r "$install_dir" "$backup_dir"
!
!    # Download and extract latest release
!    temp_dir=$(mktemp -d)
!    echo "⬇️  Downloading latest release..."
!
!    download_url="https://api.github.com/repos/jeremyeder/claude-slash/tarball/$latest_tag"
!    tarball_file="$temp_dir/claude-slash.tar.gz"
!    curl -sL "$download_url" -o "$tarball_file"
!    if [ $? -ne 0 ] || ! tar -xz -C "$temp_dir" --strip-components=1 -f "$tarball_file"; then
!        echo "❌ Failed to download release"
!        echo "🔄 Restoring from backup..."
!        rm -rf "$install_dir"
!        mv "$backup_dir" "$install_dir"
!        rm -rf "$temp_dir"
!        exit 1
!    fi
!
!    # Update commands
!    if [ -d "$temp_dir/.claude/commands" ]; then
!        echo "🔄 Updating commands..."
!
!        # Remove old commands
!        find "$install_dir" -name "*.md" -delete
!
!        # Copy new commands
!        cp "$temp_dir/.claude/commands/"*.md "$install_dir/"
!
!        echo "✅ Update completed successfully!"
!        echo "📦 Updated to: $latest_tag"
!        echo "📁 Backup saved to: $backup_dir"
!        echo "🗑️  Remove backup with: rm -rf $backup_dir"
!
!    else
!        echo "❌ Downloaded release doesn't contain command files"
!        echo "🔄 Restoring from backup..."
!        rm -rf "$install_dir"
!        mv "$backup_dir" "$install_dir"
!    fi
!
!    # Cleanup
!    rm -rf "$temp_dir"
!
!    echo
!    echo "🎉 claude-slash commands updated successfully!"
!    exit 0
!fi

!# Default help mode
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
!echo "• Use /learn to extract insights from your current session"
!echo "• Use /slash update to get the latest commands"
!echo ""
!echo -e "${BLUE}📖 For more information visit:${NC} https://github.com/jeremyeder/claude-slash"
