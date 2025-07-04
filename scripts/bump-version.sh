#!/bin/bash

# Version bumping script for claude-slash
# Handles semantic versioning with git tags

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Show usage information
show_usage() {
    echo "Usage: $0 [major|minor|patch] [options]"
    echo
    echo "Bump version types:"
    echo "  major   Bump major version (1.0.0 -> 2.0.0)"
    echo "  minor   Bump minor version (1.0.0 -> 1.1.0)"  
    echo "  patch   Bump patch version (1.0.0 -> 1.0.1)"
    echo
    echo "Options:"
    echo "  --dry-run    Show what would be done without making changes"
    echo "  --push       Push the new tag to origin after creation"
    echo "  --yes        Skip confirmation prompts (non-interactive)"
    echo "  --help       Show this help message"
    echo
    echo "Examples:"
    echo "  $0 patch              # Bump patch version locally"
    echo "  $0 minor --push       # Bump minor version and push to trigger release"
    echo "  $0 major --dry-run    # Preview major version bump"
}

# Get current version from git tags
get_current_version() {
    local current_tag
    current_tag=$(git tag --sort=-version:refname | head -1 2>/dev/null || echo "")
    
    if [ -z "$current_tag" ]; then
        echo "v0.0.0"
        return
    fi
    
    echo "$current_tag"
}

# Parse version into components
parse_version() {
    local version="$1"
    # Remove 'v' prefix if present
    version="${version#v}"
    
    local major minor patch
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    patch=$(echo "$version" | cut -d. -f3)
    
    echo "$major $minor $patch"
}

# Bump version based on type
bump_version() {
    local bump_type="$1"
    local current_version="$2"
    
    read -r major minor patch <<< "$(parse_version "$current_version")"
    
    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            print_error "Invalid bump type: $bump_type"
            return 1
            ;;
    esac
    
    echo "v$major.$minor.$patch"
}

# Update VERSION file
update_version_file() {
    local new_version="$1"
    # Remove 'v' prefix for VERSION file
    echo "${new_version#v}" > VERSION
    print_status "Updated VERSION file to ${new_version#v}"
}

# Update install script version
update_install_script() {
    local new_version="$1"
    local version_no_v="${new_version#v}"
    
    if [ -f "install.sh" ]; then
        sed -i.bak "s/INSTALLER_VERSION=\"[^\"]*\"/INSTALLER_VERSION=\"$version_no_v\"/" install.sh
        rm -f install.sh.bak
        print_status "Updated install.sh version to $version_no_v"
    fi
}

# Main function
main() {
    local bump_type=""
    local dry_run=false
    local push_tag=false
    local auto_yes=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            major|minor|patch)
                if [ -n "$bump_type" ]; then
                    print_error "Multiple bump types specified"
                    exit 1
                fi
                bump_type="$1"
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --push)
                push_tag=true
                shift
                ;;
            --yes|-y)
                auto_yes=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate arguments
    if [ -z "$bump_type" ]; then
        print_error "Bump type required (major, minor, or patch)"
        show_usage
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes"
        if [ "$auto_yes" != true ]; then
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_status "Aborted"
                exit 0
            fi
        else
            print_status "Auto-confirmed: Continuing with uncommitted changes"
        fi
    fi
    
    # Get current version
    local current_version
    current_version=$(get_current_version)
    print_status "Current version: $current_version"
    
    # Calculate new version
    local new_version
    new_version=$(bump_version "$bump_type" "$current_version")
    print_status "New version: $new_version"
    
    if [ "$dry_run" = true ]; then
        print_warning "DRY RUN - No changes will be made"
        print_status "Would update VERSION file to: ${new_version#v}"
        print_status "Would update install.sh version to: ${new_version#v}"
        print_status "Would create git tag: $new_version"
        if [ "$push_tag" = true ]; then
            print_status "Would push tag to origin"
        fi
        exit 0
    fi
    
    # Confirm the changes
    echo
    print_status "This will:"
    echo "  • Update VERSION file to ${new_version#v}"
    echo "  • Update install.sh version to ${new_version#v}"
    echo "  • Create git tag $new_version"
    if [ "$push_tag" = true ]; then
        echo "  • Push tag to origin (triggering release)"
    fi
    echo
    
    if [ "$auto_yes" != true ]; then
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Aborted"
            exit 0
        fi
    else
        print_status "Auto-confirmed: Proceeding with version bump"
    fi
    
    # Make the changes
    print_status "Bumping version from $current_version to $new_version..."
    
    # Update files
    update_version_file "$new_version"
    update_install_script "$new_version"
    
    # Commit changes
    git add VERSION install.sh
    git commit -m "Bump version to $new_version

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    
    # Create tag
    git tag "$new_version"
    print_success "Created tag $new_version"
    
    # Push if requested
    if [ "$push_tag" = true ]; then
        print_status "Pushing tag to origin..."
        git push origin main
        git push origin "$new_version"
        print_success "Tag pushed to origin - release will be triggered automatically"
    else
        print_status "Tag created locally. Push with: git push origin $new_version"
    fi
    
    print_success "Version bumped successfully!"
}

# Run main function with all arguments
main "$@"