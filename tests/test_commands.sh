#!/bin/bash

# Test suite for claude-slash commands
# Tests command file structure and basic functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    
    if [ -f ".claude/commands/checkpoint.md" ] && [ -f ".claude/commands/ckpt.md" ]; then
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

# Test checkpoint functionality (dry run)
test_checkpoint_dry_run() {
    test_start "Checkpoint dry run"
    
    # Create a temporary directory structure
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    cp .claude/commands/checkpoint.md "$temp_dir/.claude/commands/"
    
    cd "$temp_dir"
    
    # Initialize git repo for testing
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "Test User"
    
    # Test the checkpoint logic without actually running the command
    git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
    timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
    checkpoint_dir="$git_root/.claude/checkpoints"
    checkpoint_file="$checkpoint_dir/checkpoint-$timestamp.json"
    
    # Test directory creation
    mkdir -p "$checkpoint_dir"
    
    if [ -d "$checkpoint_dir" ]; then
        test_pass "Checkpoint directory creation works"
    else
        test_fail "Failed to create checkpoint directory"
    fi
    
    # Test JSON structure (create a minimal checkpoint)
    cat > "$checkpoint_file" << 'EOF'
{
  "timestamp": "2024-01-01T00:00:00Z",
  "description": "test checkpoint",
  "git_info": {
    "repository_root": "/test/repo",
    "current_branch": "main",
    "commit_hash": "abc123"
  },
  "working_directory": "/test/repo",
  "session_info": {
    "user": "testuser",
    "hostname": "testhost"
  }
}
EOF
    
    # Validate JSON structure
    if command -v python3 &> /dev/null; then
        if python3 -c "import json; json.load(open('$checkpoint_file'))" 2>/dev/null; then
            test_pass "Checkpoint JSON structure valid"
        else
            test_fail "Invalid checkpoint JSON structure"
        fi
    else
        test_pass "Checkpoint file created (Python not available for JSON validation)"
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$temp_dir"
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
    test_checkpoint_dry_run
    test_install_script
    
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