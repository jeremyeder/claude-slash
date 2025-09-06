#!/bin/bash
set -e

# claude-slash installer - Anthropic Claude Code compliant extension installer
#
# This installer follows Anthropic's official documentation for Claude Code integration:
# https://docs.anthropic.com/en/docs/claude-code/setup
#
# Prerequisites (automatically checked):
# - Claude Code installed: npm install -g @anthropic-ai/claude-code
# - Node.js 18+ (Claude Code requirement)
# - Python 3.11+ (recommended)
# - Git
# - 4GB+ RAM (recommended)
#
# Usage: install.sh [TARGET_DIRECTORY]
# Example: install.sh ~/repos/example

INSTALLER_VERSION="2.0.0"
GITHUB_REPO="jeremyeder/claude-slash"
GITHUB_API_URL="https://api.github.com/repos/$GITHUB_REPO"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if target directory is provided
if [ $# -eq 0 ]; then
    log_error "Usage: $0 <target_directory>"
    log_info "Example: $0 ~/repos/example"
    exit 1
fi

TARGET_DIR="$1"

# Resolve absolute path
TARGET_DIR=$(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$TARGET_DIR")

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    log_error "Target directory does not exist: $TARGET_DIR"
    exit 1
fi

log_info "Installing claude-slash to: $TARGET_DIR"

# Installation directory
INSTALL_DIR="$TARGET_DIR/.claude-slash"
VENV_DIR="$INSTALL_DIR/venv"
BIN_DIR="$INSTALL_DIR/bin"
COMMANDS_DIR="$TARGET_DIR/.claude/commands"

# Check for required tools
check_dependencies() {
    log_info "Checking dependencies and prerequisites..."

    # Check for official Claude Code installation (PREREQUISITE)
    if command -v claude >/dev/null 2>&1; then
        CLAUDE_VERSION=$(claude --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
        if [ -n "$CLAUDE_VERSION" ]; then
            log_success "Found Claude Code v$CLAUDE_VERSION"
        else
            log_success "Found Claude Code installation"
        fi
    else
        log_error "Claude Code is required but not installed"
        log_info "Please install Claude Code first using one of these methods:"
        log_info "  • npm install -g @anthropic-ai/claude-code"
        log_info "  • curl -fsSL https://claude.ai/install.sh | bash (Linux/macOS)"
        log_info "  • irm https://claude.ai/install.ps1 | iex (Windows PowerShell)"
        log_info ""
        log_info "After installation, run 'claude doctor' to verify setup"
        log_info "Official documentation: https://docs.anthropic.com/en/docs/claude-code/setup"
        exit 1
    fi

    # Check for Node.js 18+ (Claude Code requirement)
    if command -v node >/dev/null 2>&1; then
        NODE_VERSION=$(node -v | sed 's/v//')
        NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)

        if [ "$NODE_MAJOR" -ge 18 ]; then
            log_success "Found Node.js v$NODE_VERSION"
        else
            log_error "Node.js 18+ required for Claude Code, found v$NODE_VERSION"
            log_info "Please upgrade Node.js: https://nodejs.org/"
            exit 1
        fi
    else
        log_error "Node.js is required for Claude Code but not installed"
        log_info "Please install Node.js 18+: https://nodejs.org/"
        exit 1
    fi

    # Check for Python 3.11+ (adjusted to match Claude Code requirements)
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
            PYTHON_CMD="python3"
            log_success "Found Python $PYTHON_VERSION"
        else
            log_error "Python 3.11+ recommended, found $PYTHON_VERSION"
            log_warning "Continuing with Python $PYTHON_VERSION - some features may not work"
            PYTHON_CMD="python3"
        fi
    else
        log_error "Python 3 not found. Please install Python 3.11+"
        exit 1
    fi

    # Check for git
    if ! command -v git >/dev/null 2>&1; then
        log_error "Git is required but not installed"
        exit 1
    fi

    # Check system memory (4GB+ recommended by Anthropic)
    if command -v free >/dev/null 2>&1; then
        # Linux
        TOTAL_MEM_KB=$(free | awk '/^Mem:/ {print $2}')
        TOTAL_MEM_GB=$((TOTAL_MEM_KB / 1024 / 1024))
    elif command -v vm_stat >/dev/null 2>&1; then
        # macOS
        PAGE_SIZE=$(vm_stat | grep "page size" | awk '{print $8}')
        TOTAL_PAGES=$(vm_stat | head -2 | tail -1 | awk '{print $3}' | sed 's/\.//')
        TOTAL_MEM_GB=$(((PAGE_SIZE * TOTAL_PAGES) / 1024 / 1024 / 1024))
    else
        log_warning "Could not determine system memory"
        TOTAL_MEM_GB=0
    fi

    if [ "$TOTAL_MEM_GB" -ge 4 ]; then
        log_success "System memory: ${TOTAL_MEM_GB}GB (meets Claude Code requirements)"
    elif [ "$TOTAL_MEM_GB" -gt 0 ]; then
        log_warning "System memory: ${TOTAL_MEM_GB}GB (Claude Code recommends 4GB+)"
    fi

    # Check for shell compatibility
    if [ -n "$ZSH_VERSION" ]; then
        log_success "Shell: Zsh (compatible with Claude Code)"
    elif [ -n "$BASH_VERSION" ]; then
        log_success "Shell: Bash (compatible with Claude Code)"
    elif [ -n "$FISH_VERSION" ]; then
        log_success "Shell: Fish (compatible with Claude Code)"
    else
        log_warning "Shell: $SHELL (Claude Code works best with Bash, Zsh, or Fish)"
    fi

    log_success "All dependencies satisfied"
}

# Check Claude Code authentication and provide setup guidance
check_claude_authentication() {
    log_info "Checking Claude Code authentication..."

    # Try to get authentication status
    if claude auth status >/dev/null 2>&1; then
        log_success "Claude Code is authenticated and ready"
    else
        log_warning "Claude Code authentication not configured"
        log_info ""
        log_info "Authentication Setup Required:"
        log_info "1. Anthropic Console (recommended for developers):"
        log_info "   • Visit: https://console.anthropic.com"
        log_info "   • Create an account and add billing"
        log_info "   • Run: claude auth login"
        log_info ""
        log_info "2. Claude App (Pro/Max subscription):"
        log_info "   • Subscribe to Claude Pro or Max"
        log_info "   • Run: claude auth login --app"
        log_info ""
        log_info "3. Enterprise (Bedrock/Vertex AI):"
        log_info "   • Configure with your cloud provider"
        log_info "   • Documentation: https://docs.anthropic.com/en/docs/claude-code/deployment"
        log_info ""
        log_warning "claude-slash installation will continue, but Claude Code features require authentication"
        log_info "Run 'claude auth login' after installation to set up authentication"
        log_info ""

        # Ask if user wants to continue
        printf "Continue installation without authentication setup? [y/N]: "
        read -r CONTINUE_RESPONSE
        case $CONTINUE_RESPONSE in
            [Yy]*)
                log_info "Continuing installation..."
                ;;
            *)
                log_info "Installation cancelled. Please run 'claude auth login' first, then retry installation."
                exit 1
                ;;
        esac
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."

    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    mkdir -p "$COMMANDS_DIR"

    log_success "Directories created"
}

# Set up Python virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."

    if [ -d "$VENV_DIR" ]; then
        log_info "Virtual environment exists, updating..."
        # shellcheck source=/dev/null
        source "$VENV_DIR/bin/activate"
    else
        log_info "Creating new virtual environment..."
        "$PYTHON_CMD" -m venv "$VENV_DIR"
        # shellcheck source=/dev/null
        source "$VENV_DIR/bin/activate"
    fi

    # Upgrade pip
    pip install --upgrade pip >/dev/null 2>&1

    log_success "Virtual environment ready"
}

# Install or update claude-slash
install_claude_slash() {
    log_info "Installing/updating claude-slash..."

    # Get latest release info
    LATEST_RELEASE=$(curl -s "$GITHUB_API_URL/releases/latest" | grep -o '"tag_name": "[^"]*"' | cut -d'"' -f4)
    if [ -z "$LATEST_RELEASE" ]; then
        log_warning "Could not fetch latest release, using main branch"
        INSTALL_URL="https://github.com/$GITHUB_REPO/archive/main.zip"
    else
        log_info "Latest release: $LATEST_RELEASE"
        INSTALL_URL="https://github.com/$GITHUB_REPO/archive/$LATEST_RELEASE.zip"
    fi

    # Install from GitHub
    pip install --upgrade "$INSTALL_URL" >/dev/null 2>&1

    log_success "claude-slash installed/updated"
}

# Copy slash commands for Claude Code integration
setup_slash_commands() {
    log_info "Setting up Claude Code slash commands..."

    # Download and extract commands
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    if [ -n "$LATEST_RELEASE" ]; then
        ARCHIVE_URL="https://github.com/$GITHUB_REPO/archive/$LATEST_RELEASE.zip"
    else
        ARCHIVE_URL="https://github.com/$GITHUB_REPO/archive/main.zip"
    fi

    curl -sL "$ARCHIVE_URL" -o claude-slash.zip
    unzip -q claude-slash.zip

    # Find the extracted directory
    EXTRACTED_DIR=$(find . -name "claude-slash-*" -type d | head -1)

    if [ -d "$EXTRACTED_DIR/.claude/commands" ]; then
        # Copy commands to target
        cp -r "$EXTRACTED_DIR/.claude/commands/"* "$COMMANDS_DIR/"
        log_success "Slash commands installed to $COMMANDS_DIR"
    else
        log_warning "Slash commands not found in release"
    fi

    # Cleanup
    cd "$TARGET_DIR"
    rm -rf "$TEMP_DIR"
}

# Create wrapper scripts
create_wrappers() {
    log_info "Creating wrapper scripts..."

    # Create claude-slash wrapper
    cat > "$BIN_DIR/claude-slash" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/../venv"
source "$VENV_DIR/bin/activate"
exec claude-slash "$@"
EOF
    chmod +x "$BIN_DIR/claude-slash"

    log_success "Wrapper scripts created"
}

# Create version tracking
create_version_info() {
    cat > "$INSTALL_DIR/version.json" << EOF
{
    "version": "${LATEST_RELEASE:-main}",
    "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "installer_version": "$INSTALLER_VERSION"
}
EOF
}

# Post-install validation (similar to claude doctor)
validate_installation() {
    log_info "Validating installation..."
    local validation_errors=0

    # Check if claude-slash binary works
    if "$BIN_DIR/claude-slash" --version >/dev/null 2>&1; then
        INSTALLED_VERSION=$("$BIN_DIR/claude-slash" --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
        log_success "claude-slash CLI operational (v${INSTALLED_VERSION:-unknown})"
    else
        log_error "claude-slash CLI not working properly"
        validation_errors=$((validation_errors + 1))
    fi

    # Check if slash commands are installed
    if [ -d "$COMMANDS_DIR" ] && [ "$(find "$COMMANDS_DIR" -maxdepth 1 -type f 2>/dev/null | wc -l)" -gt 0 ]; then
        COMMAND_COUNT=$(find "$COMMANDS_DIR" -maxdepth 1 -name "*.py" -o -name "*.md" 2>/dev/null | wc -l)
        log_success "Slash commands installed: $COMMAND_COUNT files"
    else
        log_error "Slash commands not installed properly"
        validation_errors=$((validation_errors + 1))
    fi

    # Check virtual environment
    if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        log_success "Python virtual environment created"
    else
        log_error "Python virtual environment not created"
        validation_errors=$((validation_errors + 1))
    fi

    # Check Claude Code integration
    if command -v claude >/dev/null 2>&1; then
        log_success "Claude Code integration ready"

        # Check if authentication is working
        if claude auth status >/dev/null 2>&1; then
            log_success "Claude Code authentication configured"
        else
            log_warning "Claude Code authentication not configured (run 'claude auth login')"
        fi
    else
        log_error "Claude Code not found - integration unavailable"
        validation_errors=$((validation_errors + 1))
    fi

    # Check network connectivity
    if curl -s --max-time 5 https://api.anthropic.com >/dev/null 2>&1; then
        log_success "Network connectivity to Anthropic API"
    else
        log_warning "Network connectivity check failed - may affect Claude Code features"
    fi

    # Summary
    if [ $validation_errors -eq 0 ]; then
        log_success "All validation checks passed!"
        return 0
    else
        log_warning "$validation_errors validation issue(s) found - some features may not work"
        return 1
    fi
}

# Print usage instructions
print_usage() {
    log_success "claude-slash installation complete!"
    echo
    log_info "🚀 Getting Started:"
    echo "  1. Authentication (if not done already):"
    echo "     claude auth login"
    echo ""
    echo "  2. Verify installation:"
    echo "     claude doctor                    # Check Claude Code setup"
    echo "     $BIN_DIR/claude-slash --help     # Check claude-slash CLI"
    echo ""
    echo "  3. Start using slash commands in Claude Code:"
    echo "     /slash                          # Show all available commands"
    echo "     /github-init my-repo            # Create repository with best practices"
    echo "     /menuconfig                     # Interactive TUI configuration"
    echo "     /learn                          # Extract session insights"
    echo
    log_info "📁 Installation Details:"
    echo "  • Project directory: $TARGET_DIR"
    echo "  • Installation directory: $INSTALL_DIR"
    echo "  • Commands directory: $COMMANDS_DIR"
    echo
    log_info "💡 Advanced Usage:"
    echo "  • CLI access: $BIN_DIR/claude-slash [command] [options]"
    echo "  • Add to PATH: export PATH=\"$BIN_DIR:\$PATH\""
    echo "  • Update: Re-run this installer script"
    echo "  • Troubleshooting: claude doctor"
    echo
    log_info "📖 Documentation:"
    echo "  • Claude Code: https://docs.anthropic.com/en/docs/claude-code/"
    echo "  • claude-slash: https://github.com/jeremyeder/claude-slash"
    echo
    if ! claude auth status >/dev/null 2>&1; then
        log_warning "⚠️  Authentication Required:"
        echo "  Run 'claude auth login' to set up Claude Code authentication"
        echo "  Visit https://console.anthropic.com to create an account"
    fi
}

# Main installation process
main() {
    log_info "claude-slash installer v$INSTALLER_VERSION"
    log_info "Installing claude-slash extension for Claude Code"
    echo

    check_dependencies
    check_claude_authentication
    create_directories
    setup_venv
    install_claude_slash
    setup_slash_commands
    create_wrappers
    create_version_info

    echo
    log_info "Running post-install validation..."
    validate_installation

    echo
    print_usage
}

# Run main installation
main
