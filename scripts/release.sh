#!/bin/bash

# Full release script for claude-slash
# Handles the complete release process including version bumping, testing, and deployment

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
    echo "Release types:"
    echo "  major   Major release (1.0.0 -> 2.0.0) - breaking changes"
    echo "  minor   Minor release (1.0.0 -> 1.1.0) - new features"  
    echo "  patch   Patch release (1.0.0 -> 1.0.1) - bug fixes"
    echo
    echo "Options:"
    echo "  --skip-tests    Skip running tests before release"
    echo "  --dry-run       Show what would be done without making changes"
    echo "  --help          Show this help message"
    echo
    echo "Examples:"
    echo "  $0 patch        # Create a patch release"
    echo "  $0 minor        # Create a minor release with new features"
    echo "  $0 major        # Create a major release with breaking changes"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    
    # Check if we're on main branch
    local current_branch
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        print_error "Must be on main branch for release (currently on: $current_branch)"
        exit 1
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "You have uncommitted changes. Please commit or stash them first."
        exit 1
    fi
    
    # Check if origin is up to date
    git fetch origin
    local local_commit remote_commit
    local_commit=$(git rev-parse HEAD)
    remote_commit=$(git rev-parse origin/main)
    
    if [ "$local_commit" != "$remote_commit" ]; then
        print_error "Local main branch is not up to date with origin/main"
        print_status "Run: git pull origin main"
        exit 1
    fi
    
    # Check for required tools
    local missing_tools=()
    
    if ! command -v curl &> /dev/null; then
        missing_tools+=("curl")
    fi
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Check if test directory exists
    if [ ! -d "tests" ]; then
        print_warning "No tests directory found, skipping tests"
        return
    fi
    
    # Run all test scripts
    local test_failed=false
    for test_file in tests/*.sh; do
        if [ -f "$test_file" ]; then
            print_status "Running $(basename "$test_file")..."
            if ! bash "$test_file"; then
                print_error "Test failed: $test_file"
                test_failed=true
            fi
        fi
    done
    
    if [ "$test_failed" = true ]; then
        print_error "Some tests failed. Fix them before releasing."
        exit 1
    fi
    
    print_success "All tests passed"
}

# Run linting
run_linting() {
    print_status "Running linting checks..."
    
    # Check markdown files if markdownlint is available
    if command -v markdownlint &> /dev/null; then
        print_status "Linting markdown files..."
        if ! markdownlint --config .markdownlint.json ./*.md .claude/commands/*.md 2>/dev/null; then
            print_warning "Markdown linting issues found"
        fi
    fi
    
    # Check shell scripts if shellcheck is available
    if command -v shellcheck &> /dev/null; then
        print_status "Linting shell scripts..."
        
        # Lint main scripts
        if ! shellcheck install.sh scripts/*.sh; then
            print_error "Shell script linting failed"
            exit 1
        fi
        
        # Lint test scripts
        if [ -d "tests" ]; then
            find tests -name "*.sh" -exec shellcheck {} \;
        fi
        
        print_success "Shell script linting passed"
    else
        print_warning "shellcheck not found, skipping shell script linting"
    fi
}

# Generate changelog
generate_changelog() {
    local new_version="$1"
    
    print_status "Generating changelog for $new_version..."
    
    # Get commits since last tag
    local last_tag
    last_tag=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
    
    local changelog_file="CHANGELOG-$new_version.md"
    
    if [ -n "$last_tag" ]; then
        print_status "Generating changelog since $last_tag..."
        git log --pretty=format:"- %s" "$last_tag"..HEAD > "$changelog_file"
    else
        print_status "Generating changelog for initial release..."
        git log --pretty=format:"- %s" > "$changelog_file"
    fi
    
    print_success "Changelog generated: $changelog_file"
}

# Main function
main() {
    local release_type=""
    local skip_tests=false
    local dry_run=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            major|minor|patch)
                if [ -n "$release_type" ]; then
                    print_error "Multiple release types specified"
                    exit 1
                fi
                release_type="$1"
                shift
                ;;
            --skip-tests)
                skip_tests=true
                shift
                ;;
            --dry-run)
                dry_run=true
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
    if [ -z "$release_type" ]; then
        print_error "Release type required (major, minor, or patch)"
        show_usage
        exit 1
    fi
    
    echo "🚀 claude-slash Release Process"
    echo "==============================="
    echo
    
    # Get current version for preview
    local current_version
    current_version=$(git tag --sort=-version:refname | head -1 2>/dev/null || echo "v0.0.0")
    
    # Calculate new version using bump script logic
    local new_version
    local major minor patch
    read -r major minor patch <<< "$(echo "${current_version#v}" | tr '.' ' ')"
    
    case "$release_type" in
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
    esac
    
    new_version="v$major.$minor.$patch"
    
    print_status "Current version: $current_version"
    print_status "New version: $new_version"
    print_status "Release type: $release_type"
    echo
    
    if [ "$dry_run" = true ]; then
        print_warning "DRY RUN - No changes will be made"
        print_status "Would perform full release process for $new_version"
        exit 0
    fi
    
    # Confirm the release
    echo "This will perform a complete release process:"
    echo "  • Check prerequisites and environment"
    echo "  • Run linting checks"
    if [ "$skip_tests" != true ]; then
        echo "  • Run test suite"
    fi
    echo "  • Bump version to $new_version"
    echo "  • Generate changelog"
    echo "  • Create and push git tag"
    echo "  • Trigger GitHub Actions release"
    echo
    read -p "Continue with $release_type release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Release cancelled"
        exit 0
    fi
    
    # Execute release steps
    echo
    print_status "🔍 Step 1: Checking prerequisites..."
    check_prerequisites
    
    echo
    print_status "🧹 Step 2: Running linting checks..."
    run_linting
    
    if [ "$skip_tests" != true ]; then
        echo
        print_status "🧪 Step 3: Running tests..."
        run_tests
    else
        print_warning "⚠️  Step 3: Skipping tests (--skip-tests specified)"
    fi
    
    echo
    print_status "📝 Step 4: Generating changelog..."
    generate_changelog "$new_version"
    
    echo
    print_status "🔖 Step 5: Bumping version and creating tag..."
    if ! ./scripts/bump-version.sh "$release_type" --push; then
        print_error "Version bump failed"
        exit 1
    fi
    
    echo
    print_success "🎉 Release $new_version completed successfully!"
    echo
    print_status "Next steps:"
    echo "  • GitHub Actions will automatically create the release"
    echo "  • Release assets will be built and uploaded"
    echo "  • Users can update with: curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash -s -- --update"
    echo
    print_status "Monitor the release at:"
    echo "  https://github.com/jeremyeder/claude-slash/actions"
    echo "  https://github.com/jeremyeder/claude-slash/releases"
    
    # Clean up changelog file
    rm -f "CHANGELOG-$new_version.md"
}

# Run main function with all arguments
main "$@"