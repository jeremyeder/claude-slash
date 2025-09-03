#!/bin/bash
set -e

# claude-slash installer - handles both installation and updates
# Usage: install.sh [TARGET_DIRECTORY]
# Example: install.sh ~/repos/example

INSTALLER_VERSION="1.7.0"
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
    log_info "Checking dependencies..."

    # Check for Python 3.13+
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
            PYTHON_CMD="python3"
            log_success "Found Python $PYTHON_VERSION"
        else
            log_error "Python 3.13+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python 3 not found. Please install Python 3.13+"
        exit 1
    fi

    # Check for git
    if ! command -v git >/dev/null 2>&1; then
        log_error "Git is required but not installed"
        exit 1
    fi

    log_success "All dependencies satisfied"
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

# Print usage instructions
print_usage() {
    log_success "claude-slash installation complete!"
    echo
    log_info "Usage:"
    echo "  • CLI access: $BIN_DIR/claude-slash --help"
    echo "  • Claude Code: Use /github-init and other slash commands in Claude conversations"
    echo "  • Update: Re-run this installer script"
    echo
    log_info "Project directory: $TARGET_DIR"
    log_info "Installation directory: $INSTALL_DIR"
    echo
    log_info "To add CLI to PATH (optional):"
    echo "  export PATH=\"$BIN_DIR:\$PATH\""
}

# Main installation process
main() {
    log_info "claude-slash installer v$INSTALLER_VERSION"
    echo

    check_dependencies
    create_directories
    setup_venv
    install_claude_slash
    setup_slash_commands
    create_wrappers
    create_version_info

    echo
    print_usage
}

# Run main installation
main
