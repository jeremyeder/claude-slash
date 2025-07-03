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
COMMANDS=("checkpoint.md" "ckpt.md")

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
}

# Main installation logic
main() {
    echo "🚀 claude-slash installer"
    echo "=========================="
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
    echo "3. Your checkpoint will be saved for future sessions"
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
        echo "  --global    Install to personal directory (~/.claude/commands/)"
        echo "  --help      Show this help message"
        echo
        echo "Examples:"
        echo "  $0                    # Install to current project"
        echo "  $0 --global          # Install for personal use"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac