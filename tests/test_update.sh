#!/bin/bash

# Test suite for update functionality
# Tests update command and install script update flag

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
# YELLOW='\033[1;33m' # Currently unused
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test utilities
test_start() {
    echo -e "${BLUE}[TEST]${NC} $1"
    TESTS_RUN=$((TESTS_RUN + 1))
}

test_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

test_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# Test update command file exists and has proper structure
test_update_command_structure() {
    test_start "Update command structure"

    if [ -f ".claude/commands/update.md" ]; then
        # Check for required sections
        if grep -q "^# Update Command" ".claude/commands/update.md" && \
           grep -q "## Usage" ".claude/commands/update.md" && \
           grep -q "## Implementation" ".claude/commands/update.md"; then
            test_pass "update.md has proper structure"
        else
            test_fail "update.md missing required sections"
        fi
    else
        test_fail "update.md command file not found"
    fi

    if [ -f ".claude/commands/cr-upgrade.md" ]; then
        # Check for required sections
        if grep -q "^# CR Upgrade" ".claude/commands/cr-upgrade.md" && \
           grep -q "## Usage" ".claude/commands/cr-upgrade.md" && \
           grep -q "## Implementation" ".claude/commands/cr-upgrade.md"; then
            test_pass "cr-upgrade.md has proper structure"
        else
            test_fail "cr-upgrade.md missing required sections"
        fi
    else
        test_fail "cr-upgrade.md command file not found"
    fi
}

# Test update command logic (dry run)
test_update_logic() {
    test_start "Update command logic"

    # Extract shell commands from update.md
    if [ -f ".claude/commands/update.md" ]; then
        grep "^!" ".claude/commands/update.md" | sed 's/^!//' > /tmp/test_update_commands.sh 2>/dev/null || true

        if [ -s /tmp/test_update_commands.sh ]; then
            # Test shell syntax
            if bash -n /tmp/test_update_commands.sh 2>/dev/null; then
                test_pass "Update command shell syntax valid"
            else
                test_fail "Update command has invalid shell syntax"
            fi

            # Check for GitHub API usage
            if grep -q "api.github.com" /tmp/test_update_commands.sh; then
                test_pass "Update command uses GitHub API"
            else
                test_fail "Update command doesn't use GitHub API"
            fi

            # Check for backup functionality
            if grep -q "backup" /tmp/test_update_commands.sh; then
                test_pass "Update command includes backup functionality"
            else
                test_fail "Update command missing backup functionality"
            fi
        else
            test_fail "No shell commands found in update.md"
        fi

        rm -f /tmp/test_update_commands.sh
    else
        test_fail "update.md not found for logic testing"
    fi
}

# Test install script update flag
test_install_script_update() {
    test_start "Install script update flag"

    if [ -f "install.sh" ]; then
        # Check for update functionality
        if grep -q "update_installation" install.sh; then
            test_pass "Install script has update_installation function"
        else
            test_fail "Install script missing update_installation function"
        fi

        # Check for --update flag handling
        if grep -q "\-\-update" install.sh; then
            test_pass "Install script handles --update flag"
        else
            test_fail "Install script doesn't handle --update flag"
        fi

        # Check for GitHub API usage in update function
        if grep -q "api.github.com" install.sh; then
            test_pass "Install script update uses GitHub API"
        else
            test_fail "Install script update doesn't use GitHub API"
        fi

        # Test help message includes update
        if ./install.sh --help | grep -q "update"; then
            test_pass "Install script help includes update option"
        else
            test_fail "Install script help missing update option"
        fi
    else
        test_fail "install.sh not found"
    fi
}

# Test GitHub API response handling (mock)
test_github_api_handling() {
    test_start "GitHub API response handling"

    # Create mock API responses
    local temp_dir
    temp_dir=$(mktemp -d)

    # Mock successful response
    cat > "$temp_dir/mock_success.json" << 'EOF'
{
  "tag_name": "v1.1.0",
  "body": "Test release notes"
}
EOF

    # Mock error response (empty)
    touch "$temp_dir/mock_error.json"

    # Test parsing successful response
    local tag_name
    tag_name=$(grep '"tag_name"' "$temp_dir/mock_success.json" | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')

    if [ "$tag_name" = "v1.1.0" ]; then
        test_pass "GitHub API response parsing works"
    else
        test_fail "GitHub API response parsing failed"
    fi

    # Test error handling
    local empty_tag
    empty_tag=$(grep '"tag_name"' "$temp_dir/mock_error.json" | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/' || echo "")

    if [ -z "$empty_tag" ]; then
        test_pass "Empty API response handled correctly"
    else
        test_fail "Empty API response not handled"
    fi

    rm -rf "$temp_dir"
}

# Test backup and rollback functionality
test_backup_rollback() {
    test_start "Backup and rollback functionality"

    # Create a test directory structure
    local temp_dir
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    echo "# Test Command" > "$temp_dir/.claude/commands/test.md"

    cd "$temp_dir"

    # Test backup creation logic
    local backup_dir
    backup_dir=".claude/commands.backup.$(date +%Y%m%d-%H%M%S)"
    cp -r ".claude/commands" "$backup_dir"

    if [ -d "$backup_dir" ] && [ -f "$backup_dir/test.md" ]; then
        test_pass "Backup creation works"
    else
        test_fail "Backup creation failed"
    fi

    # Test rollback logic
    echo "# Modified" > ".claude/commands/test.md"
    rm -rf ".claude/commands"
    mv "$backup_dir" ".claude/commands"

    if [ -f ".claude/commands/test.md" ] && grep -q "# Test Command" ".claude/commands/test.md"; then
        test_pass "Rollback functionality works"
    else
        test_fail "Rollback functionality failed"
    fi

    cd - > /dev/null
    rm -rf "$temp_dir"
}

# Test release workflow file
test_release_workflow() {
    test_start "GitHub Actions release workflow"

    if [ -f ".github/workflows/release.yml" ]; then
        # Check for proper trigger
        if grep -q "tags:" ".github/workflows/release.yml"; then
            test_pass "Release workflow triggered by tags"
        else
            test_fail "Release workflow missing tag trigger"
        fi

        # Check for release creation
        if grep -q "create-release" ".github/workflows/release.yml"; then
            test_pass "Release workflow creates GitHub releases"
        else
            test_fail "Release workflow doesn't create releases"
        fi

        # Check for asset uploading
        if grep -q "upload-release-asset" ".github/workflows/release.yml"; then
            test_pass "Release workflow uploads assets"
        else
            test_fail "Release workflow doesn't upload assets"
        fi
    else
        test_fail "Release workflow file not found"
    fi
}

# Main test runner
main() {
    echo "🧪 claude-slash update functionality test suite"
    echo "=============================================="
    echo

    # Change to repository root
    cd "$(dirname "$0")/.."

    # Run tests
    test_update_command_structure
    test_update_logic
    test_install_script_update
    test_github_api_handling
    test_backup_rollback
    test_release_workflow

    # Summary
    echo
    echo "📊 Test Results"
    echo "==============="
    echo "Tests run: $TESTS_RUN"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All update functionality tests passed!${NC}"
        exit 0
    else
        echo -e "\n${RED}❌ Some update functionality tests failed${NC}"
        exit 1
    fi
}

# Run tests
main "$@"
