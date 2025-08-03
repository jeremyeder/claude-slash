# Error Handling Utilities

Common error handling functions for claude-slash commands.

## Usage

This file contains reusable shell functions that should be sourced by other commands:

```bash
# Source error utilities
source .claude/commands/error-utils.md

# Use error functions
error_exit "Something went wrong"
success "Operation completed"
warning "This is a warning"
```

## Description

Provides standardized error handling, messaging, and tool validation functions for consistent user experience across all claude-slash commands.

## Implementation

!# Color definitions for consistent UI
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!# Standardized message functions
!error_exit() {
!    local message="$1"
!    local exit_code="${2:-1}"
!    echo -e "${RED}❌ Error: $message${NC}" >&2
!    exit "$exit_code"
!}

!error_msg() {
!    local message="$1"
!    echo -e "${RED}❌ Error: $message${NC}" >&2
!}

!warning() {
!    local message="$1"
!    echo -e "${YELLOW}⚠️  Warning: $message${NC}" >&2
!}

!success() {
!    local message="$1"
!    echo -e "${GREEN}✅ $message${NC}"
!}

!info() {
!    local message="$1"
!    echo -e "${BLUE}ℹ️  $message${NC}"
!}

!# Tool validation functions
!check_git() {
!    if ! command -v git >/dev/null 2>&1; then
!        error_exit "Git is not installed. Please install Git and try again.
!
!Installation instructions:
!  • macOS: brew install git
!  • Ubuntu/Debian: sudo apt-get install git
!  • Windows: Download from https://git-scm.com/download/win"
!    fi
!
!    # Check if we're in a git repository when needed
!    if [ "$1" = "--require-repo" ] && ! git rev-parse --show-toplevel >/dev/null 2>&1; then
!        error_exit "Not in a Git repository. Please run this command from within a Git repository."
!    fi
!}

!check_gh_cli() {
!    if ! command -v gh >/dev/null 2>&1; then
!        error_exit "GitHub CLI (gh) is not installed. Please install it and try again.
!
!Installation instructions:
!  • macOS: brew install gh
!  • Ubuntu/Debian: Follow instructions at https://cli.github.com/manual/installation
!  • Windows: Download from https://cli.github.com/manual/installation"
!    fi
!
!    # Check if user is authenticated when needed
!    if [ "$1" = "--require-auth" ] && ! gh auth status >/dev/null 2>&1; then
!        error_exit "GitHub CLI is not authenticated. Please run 'gh auth login' first."
!    fi
!}

!check_curl() {
!    if ! command -v curl >/dev/null 2>&1; then
!        error_exit "curl is not installed. Please install curl and try again.
!
!Installation instructions:
!  • macOS: curl is usually pre-installed
!  • Ubuntu/Debian: sudo apt-get install curl
!  • Windows: Download from https://curl.se/windows/"
!    fi
!}

!# Network operation wrapper with retry and user-friendly error handling
!safe_curl() {
!    local url="$1"
!    local output_file="$2"
!    local max_retries="${3:-3}"
!    local retry_count=0
!
!    while [ $retry_count -lt $max_retries ]; do
!        if [ -n "$output_file" ]; then
!            if curl -sSL "$url" -o "$output_file" 2>/dev/null; then
!                return 0
!            fi
!        else
!            if curl -sSL "$url" 2>/dev/null; then
!                return 0
!            fi
!        fi
!
!        retry_count=$((retry_count + 1))
!        if [ $retry_count -lt $max_retries ]; then
!            warning "Network request failed, retrying... ($retry_count/$max_retries)"
!            sleep 2
!        fi
!    done
!
!    error_exit "Network request failed after $max_retries attempts.
!
!Troubleshooting:
!  • Check your internet connection
!  • Verify the URL is accessible: $url
!  • Check if you're behind a corporate firewall
!  • Try again in a few minutes"
!}

!# File operation error handling
!safe_create_file() {
!    local file_path="$1"
!    local content="$2"
!    local overwrite="${3:-false}"
!    
!    # Check if file exists and overwrite is not allowed
!    if [ -f "$file_path" ] && [ "$overwrite" != "true" ]; then
!        warning "$file_path already exists, skipping"
!        return 1
!    fi
!    
!    # Try to create the file
!    if ! echo "$content" > "$file_path" 2>/dev/null; then
!        error_exit "Failed to create file: $file_path
!
!Possible causes:
!  • Permission denied - check directory permissions
!  • Disk full - check available disk space
!  • Invalid path - verify directory exists"
!    fi
!    
!    success "Created $file_path"
!    return 0
!}

!safe_create_dir() {
!    local dir_path="$1"
!    
!    if [ -d "$dir_path" ]; then
!        warning "Directory $dir_path already exists, skipping"
!        return 1
!    fi
!    
!    if ! mkdir -p "$dir_path" 2>/dev/null; then
!        error_exit "Failed to create directory: $dir_path
!
!Possible causes:
!  • Permission denied - check parent directory permissions
!  • Invalid path - verify parent directories exist
!  • Disk full - check available disk space"
!    fi
!    
!    success "Created directory $dir_path"
!    return 0
!}

!# Git operation error handling
!safe_git() {
!    local git_command="$*"
!    local error_output
!    
!    # Capture both stdout and stderr
!    if ! error_output=$(git $git_command 2>&1); then
!        local error_msg="Git command failed: git $git_command"
!        
!        # Provide specific help based on common git errors
!        case "$error_output" in
!            *"not a git repository"*)
!                error_msg="$error_msg
!
!Not in a Git repository. Please run this command from within a Git repository."
!                ;;
!            *"nothing to commit"*)
!                warning "Nothing to commit, working tree clean"
!                return 0
!                ;;
!            *"fatal: remote origin already exists"*)
!                warning "Remote 'origin' already exists"
!                return 0
!                ;;
!            *"Permission denied"*)
!                error_msg="$error_msg
!
!Permission denied. Please check your SSH keys or use HTTPS authentication."
!                ;;
!            *)
!                error_msg="$error_msg
!
!Git error: $error_output"
!                ;;
!        esac
!        
!        error_exit "$error_msg"
!    fi
!    
!    # Return the output for commands that need it
!    echo "$error_output"
!}