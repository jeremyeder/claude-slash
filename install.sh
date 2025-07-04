#!/bin/bash

# claude-slash installer
# Installs Claude Code slash commands for checkpoint functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub repository details
REPO_URL="https://raw.githubusercontent.com/jeremyeder/claude-slash/main"
API_URL="https://api.github.com/repos/jeremyeder/claude-slash"
COMMANDS=("checkpoint.md" "ckpt.md" "update.md" "up.md")
INSTALLER_VERSION="1.1.0"

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a git repository
check_git_repo() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Install commands to project directory
install_project() {
    print_status "Installing commands for current project..."
    
    # Create commands directory
    mkdir -p .claude/commands
    
    # Download each command file
    for cmd in "${COMMANDS[@]}"; do
        print_status "Downloading $cmd..."
        if curl -sSL "$REPO_URL/.claude/commands/$cmd" -o ".claude/commands/$cmd"; then
            print_success "Downloaded $cmd"
        else
            print_error "Failed to download $cmd"
            exit 1
        fi
    done
    
    print_success "Commands installed to .claude/commands/"
    print_status "Available commands:"
    echo "  • /project:checkpoint [description] - Create a session checkpoint"
    echo "  • /project:ckpt [description] - Shorthand alias"
    echo "  • /project:update - Update commands to latest release"
    echo "  • /project:up - Shorthand alias for update"
}

# Update existing installation
update_installation() {
    print_status "🔄 Updating claude-slash commands..."
    
    # Determine installation location
    local install_dir=""
    local install_type=""
    
    if [ -d ".claude/commands" ]; then
        install_dir=".claude/commands"
        install_type="project"
    elif [ -d "$HOME/.claude/commands" ]; then
        install_dir="$HOME/.claude/commands"
        install_type="global"
    else
        print_error "No claude-slash installation found"
        print_status "Run the installer first: $0"
        exit 1
    fi
    
    print_status "Found $install_type installation at: $install_dir"
    
    # Check for latest release
    print_status "🔍 Checking latest release..."
    local latest_info
    if ! latest_info=$(curl -s "$API_URL/releases/latest"); then
        print_error "Failed to check for updates (network error)"
        exit 1
    fi
    
    local latest_tag
    latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
    
    if [ -z "$latest_tag" ]; then
        print_error "Could not determine latest version"
        exit 1
    fi
    
    print_status "📦 Latest release: $latest_tag"
    
    # Create backup
    local backup_dir
    backup_dir="$install_dir.backup.$(date +%Y%m%d-%H%M%S)"
    print_status "💾 Creating backup at: $backup_dir"
    cp -r "$install_dir" "$backup_dir"
    
    # Download and extract latest release
    local temp_dir
    temp_dir=$(mktemp -d)
    print_status "⬇️  Downloading latest release..."
    
    if ! curl -sL "$API_URL/tarball/$latest_tag" | tar -xz -C "$temp_dir" --strip-components=1; then
        print_error "Failed to download release"
        print_status "🔄 Restoring from backup..."
        rm -rf "$install_dir"
        mv "$backup_dir" "$install_dir"
        rm -rf "$temp_dir"
        exit 1
    fi
    
    # Update commands
    if [ -d "$temp_dir/.claude/commands" ]; then
        print_status "🔄 Updating commands..."
        
        # Remove old commands
        find "$install_dir" -name "*.md" -delete
        
        # Copy new commands
        cp "$temp_dir/.claude/commands/"*.md "$install_dir/"
        
        print_success "✅ Update completed successfully!"
        print_status "📦 Updated to: $latest_tag"
        print_status "📁 Backup saved to: $backup_dir"
        print_status "🗑️  Remove backup with: rm -rf $backup_dir"
        
    else
        print_error "Downloaded release doesn't contain command files"
        print_status "🔄 Restoring from backup..."
        rm -rf "$install_dir"
        mv "$backup_dir" "$install_dir"
    fi
    
    # Cleanup
    rm -rf "$temp_dir"
}

# Install commands to user directory
install_user() {
    print_status "Installing commands for personal use..."
    
    # Create user commands directory
    mkdir -p ~/.claude/commands
    
    # Download each command file
    for cmd in "${COMMANDS[@]}"; do
        print_status "Downloading $cmd..."
        if curl -sSL "$REPO_URL/.claude/commands/$cmd" -o "$HOME/.claude/commands/$cmd"; then
            print_success "Downloaded $cmd"
        else
            print_error "Failed to download $cmd"
            exit 1
        fi
    done
    
    print_success "Commands installed to ~/.claude/commands/"
    print_status "Available commands:"
    echo "  • /user:checkpoint [description] - Create a session checkpoint"
    echo "  • /user:ckpt [description] - Shorthand alias"
    echo "  • /user:update - Update commands to latest release"
    echo "  • /user:up - Shorthand alias for update"
}

# Show version information
show_version() {
    echo "claude-slash installer v$INSTALLER_VERSION"
    
    # Get latest release version from GitHub
    print_status "Checking latest release version..."
    local latest_info
    if latest_info=$(curl -s "$API_URL/releases/latest" 2>/dev/null) && [ -n "$latest_info" ]; then
        local latest_tag
        latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
        if [ -n "$latest_tag" ]; then
            echo "Latest release: $latest_tag"
        else
            echo "Latest release: Unable to determine"
        fi
    else
        echo "Latest release: Unable to check (network error)"
    fi
}

# Main installation logic
main() {
    echo "🚀 claude-slash installer v$INSTALLER_VERSION"
    echo "============================================="
    echo
    
    # Check for required tools
    if ! command -v curl &> /dev/null; then
        print_error "curl is required but not installed. Please install curl first."
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "git is required but not installed. Please install git first."
        exit 1
    fi
    
    # Determine installation type
    if check_git_repo; then
        print_status "Git repository detected"
        
        # Check for --global flag
        if [[ "$1" == "--global" ]]; then
            install_user
        else
            print_status "Installing to current project (use --global for personal installation)"
            install_project
        fi
    else
        print_warning "Not in a git repository"
        print_status "Installing to personal directory (~/.claude/commands/)"
        install_user
    fi
    
    echo
    print_success "Installation complete!"
    echo
    print_status "Next steps:"
    echo "1. Open Claude Code CLI in your project"
    echo "2. Try: /project:checkpoint \"Test checkpoint\""
    echo "3. Update anytime with: /project:update"
    echo
    print_status "For more information, visit:"
    echo "https://github.com/jeremyeder/claude-slash"
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --version   Show version information"
        echo "  --update    Update existing installation to latest release"
        echo "  --global    Install to personal directory (~/.claude/commands/)"
        echo "  --help      Show this help message"
        echo
        echo "Examples:"
        echo "  $0                    # Install to current project"
        echo "  $0 --global          # Install for personal use"
        echo "  $0 --update          # Update existing installation"
        echo "  $0 --version         # Show version information"
        exit 0
        ;;
    --version|-v)
        show_version
        exit 0
        ;;
    --update)
        update_installation
        ;;
    *)
        main "$@"
        ;;
esac