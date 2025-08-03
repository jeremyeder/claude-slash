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

!# Get git root for sourcing error utilities
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!error_utils_path="$git_root/.claude/commands/error-utils.md"

!# Source error handling utilities if available
!if [ -f "$error_utils_path" ]; then
!    # Extract and execute the shell functions from error-utils.md
!    grep "^!" "$error_utils_path" | sed 's/^!//' | while IFS= read -r line; do
!        eval "$line"
!    done
!    # Source the functions by executing them in current shell
!    eval "$(grep "^!" "$error_utils_path" | sed 's/^!//')"
!else
!    # Fallback color definitions if error-utils.md not available
!    RED='\033[0;31m'
!    GREEN='\033[0;32m'
!    YELLOW='\033[1;33m'
!    BLUE='\033[0;34m'
!    PURPLE='\033[0;35m'
!    CYAN='\033[0;36m'
!    NC='\033[0m' # No Color
!    
!    # Fallback error functions
!    error_exit() { echo -e "${RED}❌ Error: $1${NC}" >&2; exit "${2:-1}"; }
!    success() { echo -e "${GREEN}✅ $1${NC}"; }
!    warning() { echo -e "${YELLOW}⚠️  Warning: $1${NC}" >&2; }
!    info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
!    safe_curl() { 
!        local url="$1" output_file="$2" max_retries="${3:-3}" retry_count=0
!        while [ $retry_count -lt $max_retries ]; do
!            if [ -n "$output_file" ]; then
!                curl -sSL "$url" -o "$output_file" 2>/dev/null && return 0
!            else
!                curl -sSL "$url" 2>/dev/null && return 0
!            fi
!            retry_count=$((retry_count + 1))
!            [ $retry_count -lt $max_retries ] && sleep 2
!        done
!        error_exit "Network request failed after $max_retries attempts. Check your internet connection."
!    }
!fi

!# Parse arguments for subcommand support
!subcommand="${ARGUMENTS%% *}"  # Get first argument
!if [ -z "$subcommand" ]; then
!    subcommand="help"
!fi

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
!        error_exit "No claude-slash installation found. Run the installer first:
!curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh -o install.sh && bash install.sh"
!    fi
!
!    echo "📍 Found $install_type installation at: $install_dir"
!
!    # Check for latest release
!    info "Checking latest release..."
!    latest_info=$(safe_curl "https://api.github.com/repos/jeremyeder/claude-slash/releases/latest")
!
!    latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
!
!    if [ -z "$latest_tag" ]; then
!        error_exit "Could not determine latest version from GitHub API response"
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
!    
!    if ! safe_curl "$download_url" "$tarball_file" || ! tar -xz -C "$temp_dir" --strip-components=1 -f "$tarball_file"; then
!        error_msg "Failed to download or extract release"
!        info "Restoring from backup..."
!        rm -rf "$install_dir"
!        mv "$backup_dir" "$install_dir"
!        rm -rf "$temp_dir"
!        error_exit "Update failed, restored from backup"
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
!        success "Update completed successfully!"
!        info "Updated to: $latest_tag"
!        info "Backup saved to: $backup_dir"
!        info "Remove backup with: rm -rf $backup_dir"
!
!    else
!        error_msg "Downloaded release doesn't contain command files"
!        info "Restoring from backup..."
!        rm -rf "$install_dir"
!        mv "$backup_dir" "$install_dir"
!        error_exit "Update failed, restored from backup"
!    fi
!
!    # Cleanup
!    rm -rf "$temp_dir"
!
!    echo
!    success "claude-slash commands updated successfully!"
!    exit 0
!fi

!# Default help mode
!echo -e "${BLUE}📋 Available Claude Slash Commands${NC}"
!echo -e "${BLUE}=================================${NC}"
!echo ""

!# Get the commands directory (git_root already set above)
!commands_dir="$git_root/.claude/commands"

!# Check if commands directory exists
!if [ ! -d "$commands_dir" ]; then
!  commands_dir="$HOME/.claude/commands"
!  if [ ! -d "$commands_dir" ]; then
!    error_exit "No claude-slash commands found. Install commands by downloading and running install.sh from:
!https://github.com/jeremyeder/claude-slash"
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
