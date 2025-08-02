#!/bin/bash

# Test suite for claude-slash commands
# Tests command file structure and basic functionality

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

# Test command file existence
test_command_files_exist() {
    test_start "Command files exist"

    if [ -f ".claude/commands/slash.md" ] && [ -f ".claude/commands/learn.md" ] && [ -f ".claude/commands/cr-bootstrap.md" ] && [ -f ".claude/commands/bootstrap.md" ] && [ -f ".claude/commands/menuconfig.md" ] && [ -f ".claude/commands/mcfg.md" ] && [ -f ".claude/commands/update.md" ] && [ -f ".claude/commands/cr-upgrade.md" ]; then
        test_pass "All command files found"
    else
        test_fail "Missing command files"
    fi
}

# Test command file structure
test_command_structure() {
    test_start "Command file structure"

    for file in .claude/commands/*.md; do
        if [ -f "$file" ]; then
            # Check for required sections
            if grep -q "^# " "$file" && grep -q "## Usage" "$file" && grep -q "## Implementation" "$file"; then
                test_pass "$(basename "$file") has proper structure"
            else
                test_fail "$(basename "$file") missing required sections"
            fi
        fi
    done
}

# Test shell syntax in commands
test_shell_syntax() {
    test_start "Shell syntax validation"

    for file in .claude/commands/*.md; do
        if [ -f "$file" ]; then
            # Extract shell commands (lines starting with !)
            grep "^!" "$file" | sed 's/^!//' > /tmp/test_shell_commands.sh 2>/dev/null || true

            if [ -s /tmp/test_shell_commands.sh ]; then
                if bash -n /tmp/test_shell_commands.sh 2>/dev/null; then
                    test_pass "$(basename "$file") shell syntax valid"
                else
                    test_fail "$(basename "$file") has invalid shell syntax"
                fi
            else
                test_pass "$(basename "$file") has no shell commands to validate"
            fi

            rm -f /tmp/test_shell_commands.sh
        fi
    done
}




# Test install script
test_install_script() {
    test_start "Install script validation"

    if [ -f "install.sh" ]; then
        if [ -x "install.sh" ]; then
            if bash -n install.sh 2>/dev/null; then
                test_pass "Install script syntax valid"
            else
                test_fail "Install script has syntax errors"
            fi
        else
            test_fail "Install script not executable"
        fi
    else
        test_fail "Install script not found"
    fi
}

# Test bootstrap command functionality
test_bootstrap_functionality() {
    test_start "Bootstrap command functionality"

    # Test cr-bootstrap command structure
    if [ -f ".claude/commands/cr-bootstrap.md" ]; then
        if grep -q "Bootstrap claude-slash installation" ".claude/commands/cr-bootstrap.md"; then
            test_pass "cr-bootstrap.md has proper description"
        else
            test_fail "cr-bootstrap.md missing proper description"
        fi

        # Test argument parsing
        if grep -q "for arg in \$ARGUMENTS" ".claude/commands/cr-bootstrap.md"; then
            test_pass "cr-bootstrap.md has argument parsing"
        else
            test_fail "cr-bootstrap.md missing argument parsing"
        fi

        # Test installation options
        if grep -q -- "--global" ".claude/commands/cr-bootstrap.md" && grep -q -- "--force" ".claude/commands/cr-bootstrap.md"; then
            test_pass "cr-bootstrap.md has installation options"
        else
            test_fail "cr-bootstrap.md missing installation options"
        fi
    else
        test_fail "cr-bootstrap.md not found"
    fi
}

# Test bootstrap command alias
test_bootstrap_alias() {
    test_start "Bootstrap command alias"

    if [ -f ".claude/commands/bootstrap.md" ]; then
        if grep -q "This is an alias for the full" ".claude/commands/bootstrap.md"; then
            test_pass "bootstrap.md has proper alias documentation"
        else
            test_fail "bootstrap.md missing alias documentation"
        fi

        # Test that alias has same core functionality
        if grep -q "install_global=false" ".claude/commands/bootstrap.md"; then
            test_pass "bootstrap.md has same core logic"
        else
            test_fail "bootstrap.md missing core logic"
        fi
    else
        test_fail "bootstrap.md not found"
    fi
}

# Test bootstrap command validation
test_bootstrap_validation() {
    test_start "Bootstrap command validation"

    # Test directory creation logic
    if grep -q "mkdir -p.*checkpoints" ".claude/commands/cr-bootstrap.md"; then
        test_pass "cr-bootstrap creates checkpoints directory"
    else
        test_fail "cr-bootstrap missing checkpoints directory creation"
    fi

    # Test GitHub API usage
    if grep -q "api.github.com/repos" ".claude/commands/cr-bootstrap.md"; then
        test_pass "cr-bootstrap uses GitHub API"
    else
        test_fail "cr-bootstrap missing GitHub API usage"
    fi

    # Test validation step
    if grep -q "Validating installation" ".claude/commands/cr-bootstrap.md"; then
        test_pass "cr-bootstrap includes validation step"
    else
        test_fail "cr-bootstrap missing validation step"
    fi
}

# Test menuconfig functionality
test_menuconfig_functionality() {
    test_start "Menuconfig command functionality"

    if [ -f ".claude/commands/menuconfig.md" ]; then
        # Check for menuconfig-specific content
        if grep -q "menuconfig-style" ".claude/commands/menuconfig.md" && \
           grep -q "textual" ".claude/commands/menuconfig.md" && \
           grep -q "claude_menuconfig.py" ".claude/commands/menuconfig.md"; then
            test_pass "Menuconfig command has proper content"
        else
            test_fail "Menuconfig command missing key functionality"
        fi

        # Check if Python script path is referenced correctly
        if grep -q 'claude_menuconfig.py' ".claude/commands/menuconfig.md" && \
           grep -q 'scripts_dir.*claude_menuconfig.py' ".claude/commands/menuconfig.md"; then
            test_pass "Menuconfig references correct Python script path"
        else
            test_fail "Menuconfig missing Python script reference"
        fi

        # Check if the Python script exists
        if [ -f ".claude/scripts/claude_menuconfig.py" ]; then
            test_pass "Menuconfig Python script exists"

            # Test Python syntax if python3 is available
            if command -v python3 &> /dev/null; then
                if python3 -m py_compile .claude/scripts/claude_menuconfig.py 2>/dev/null; then
                    test_pass "Menuconfig Python script syntax is valid"
                else
                    test_fail "Menuconfig Python script has syntax errors"
                fi
            else
                test_pass "Python syntax check skipped (Python not available)"
            fi
        else
            test_fail "Menuconfig Python script missing"
        fi
    else
        test_fail "Menuconfig command file not found"
    fi
}

# Test menuconfig alias
test_menuconfig_alias() {
    test_start "Menuconfig alias functionality"

    if [ -f ".claude/commands/mcfg.md" ] && [ -f ".claude/commands/menuconfig.md" ]; then
        # Check that both files reference the same Python script
        if grep -q "claude_menuconfig.py" ".claude/commands/mcfg.md" && \
           grep -q "claude_menuconfig.py" ".claude/commands/menuconfig.md"; then
            test_pass "Menuconfig alias references same script"
        else
            test_fail "Menuconfig alias missing script reference"
        fi

        # Check that alias has proper description
        if grep -q "Short alias" ".claude/commands/mcfg.md"; then
            test_pass "Menuconfig alias has proper description"
        else
            test_fail "Menuconfig alias missing alias description"
        fi
    else
        test_fail "Cannot compare menuconfig alias files"
    fi
}

# Test slash command functionality
test_slash_command() {
    test_start "Slash command functionality"

    if [ -f ".claude/commands/slash.md" ]; then
        # Check for proper structure
        if grep -q "Display all available custom slash commands" ".claude/commands/slash.md" && \
           grep -q "/slash" ".claude/commands/slash.md" && \
           grep -q "extract_description" ".claude/commands/slash.md"; then
            test_pass "Slash command has proper content and functionality"
        else
            test_fail "Slash command missing key functionality"
        fi

        # Check if it references command scanning
        if grep -q "commands_dir" ".claude/commands/slash.md" && \
           grep -q '\*.md' ".claude/commands/slash.md"; then
            test_pass "Slash command includes dynamic command scanning"
        else
            test_fail "Slash command missing dynamic scanning functionality"
        fi
    else
        test_fail "Slash command file not found"
    fi
}

# Main test runner
main() {
    echo "🧪 claude-slash test suite"
    echo "=========================="
    echo

    # Change to repository root
    cd "$(dirname "$0")/.."

    # Run tests
    test_command_files_exist
    test_command_structure
    test_shell_syntax
    test_slash_command
    test_bootstrap_functionality
    test_bootstrap_alias
    test_bootstrap_validation
    test_install_script
    test_menuconfig_functionality
    test_menuconfig_alias

    # Summary
    echo
    echo "📊 Test Results"
    echo "==============="
    echo "Tests run: $TESTS_RUN"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All tests passed!${NC}"
        exit 0
    else
        echo -e "\n${RED}❌ Some tests failed${NC}"
        exit 1
    fi
}

# Run tests
main "$@"
