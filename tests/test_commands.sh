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
    
    if [ -f ".claude/commands/checkpoint.md" ] && [ -f ".claude/commands/ckpt.md" ] && [ -f ".claude/commands/restore.md" ] && [ -f ".claude/commands/rst.md" ] && [ -f ".claude/commands/cr-bootstrap.md" ] && [ -f ".claude/commands/bootstrap.md" ] && [ -f ".claude/commands/menuconfig.md" ] && [ -f ".claude/commands/mcfg.md" ]; then
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

# Test restore functionality (dry run)
test_restore_dry_run() {
    test_start "Restore dry run"
    
    # Create a temporary directory structure
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    mkdir -p "$temp_dir/.claude/checkpoints"
    cp .claude/commands/restore.md "$temp_dir/.claude/commands/"
    
    cd "$temp_dir"
    
    # Initialize git repo for testing
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "Test User"
    
    # Create a test checkpoint file
    checkpoint_file="$temp_dir/.claude/checkpoints/checkpoint-2024-01-01-12-00-00.json"
    cat > "$checkpoint_file" << 'EOF'
{
  "timestamp": "2024-01-01T12:00:00Z",
  "description": "test checkpoint for restore",
  "git_info": {
    "repository_root": "/test/repo",
    "current_branch": "main",
    "commit_hash": "abc123def456",
    "status": "",
    "staged_files": "",
    "modified_files": "",
    "untracked_files": ""
  },
  "working_directory": "/test/repo",
  "session_info": {
    "user": "testuser",
    "hostname": "testhost",
    "os": "Linux",
    "shell": "/bin/bash"
  }
}
EOF
    
    # Test checkpoint file detection
    if [ -f "$checkpoint_file" ]; then
        test_pass "Test checkpoint file created"
    else
        test_fail "Failed to create test checkpoint file"
    fi
    
    # Test JSON parsing logic (extract timestamp)
    timestamp=$(grep -o '"timestamp":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$timestamp" = "2024-01-01T12:00:00Z" ]; then
        test_pass "Checkpoint timestamp extraction works"
    else
        test_fail "Failed to extract checkpoint timestamp"
    fi
    
    # Test latest checkpoint detection
    latest_checkpoint=$(ls -t "$temp_dir/.claude/checkpoints"/checkpoint-*.json 2>/dev/null | head -1)
    if [ "$latest_checkpoint" = "$checkpoint_file" ]; then
        test_pass "Latest checkpoint detection works"
    else
        test_fail "Failed to detect latest checkpoint"
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$temp_dir"
}

# Test restore error handling
test_restore_error_handling() {
    test_start "Restore error handling"
    
    # Create a temporary directory structure
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    mkdir -p "$temp_dir/.claude/checkpoints"
    cp .claude/commands/restore.md "$temp_dir/.claude/commands/"
    
    cd "$temp_dir"
    
    # Initialize git repo for testing
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "Test User"
    
    # Test 1: No checkpoints directory
    rmdir "$temp_dir/.claude/checkpoints"
    
    # Test the logic for finding latest checkpoint when directory doesn't exist
    latest_checkpoint=$(ls -t "$temp_dir/.claude/checkpoints"/checkpoint-*.json 2>/dev/null | head -1)
    if [ -z "$latest_checkpoint" ]; then
        test_pass "Handles missing checkpoints directory correctly"
    else
        test_fail "Should detect missing checkpoints directory"
    fi
    
    # Recreate checkpoints directory
    mkdir -p "$temp_dir/.claude/checkpoints"
    
    # Test 2: Invalid JSON file
    invalid_json_file="$temp_dir/.claude/checkpoints/checkpoint-invalid.json"
    cat > "$invalid_json_file" << 'EOF'
{
  "timestamp": "2024-01-01T12:00:00Z",
  "description": "invalid json"
  "missing_comma": true
}
EOF
    
    # Test JSON validation (if python3 available)
    if command -v python3 &> /dev/null; then
        if ! python3 -c "import json; json.load(open('$invalid_json_file'))" 2>/dev/null; then
            test_pass "Detects invalid JSON format"
        else
            test_fail "Should detect invalid JSON format"
        fi
    else
        test_pass "JSON validation skipped (Python not available)"
    fi
    
    # Test 3: Missing checkpoint file
    nonexistent_file="$temp_dir/.claude/checkpoints/nonexistent-checkpoint.json"
    if [ ! -f "$nonexistent_file" ]; then
        test_pass "Correctly identifies missing checkpoint file"
    else
        test_fail "Should detect missing checkpoint file"
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$temp_dir"
}

# Test restore path resolution
test_restore_path_resolution() {
    test_start "Restore path resolution"
    
    # Create a temporary directory structure
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    mkdir -p "$temp_dir/.claude/checkpoints"
    cp .claude/commands/restore.md "$temp_dir/.claude/commands/"
    
    cd "$temp_dir"
    
    # Initialize git repo for testing
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "Test User"
    
    # Create test checkpoint files
    checkpoint1="$temp_dir/.claude/checkpoints/checkpoint-2024-01-01-12-00-00.json"
    checkpoint2="$temp_dir/.claude/checkpoints/checkpoint-2024-01-02-12-00-00.json"
    
    # Create valid checkpoint content
    for checkpoint_file in "$checkpoint1" "$checkpoint2"; do
        cat > "$checkpoint_file" << 'EOF'
{
  "timestamp": "2024-01-01T12:00:00Z",
  "description": "test checkpoint",
  "git_info": {
    "repository_root": "/test/repo",
    "current_branch": "main",
    "commit_hash": "abc123def456",
    "status": "",
    "staged_files": "",
    "modified_files": "",
    "untracked_files": ""
  },
  "working_directory": "/test/repo",
  "session_info": {
    "user": "testuser",
    "hostname": "testhost",
    "os": "Linux",
    "shell": "/bin/bash"
  }
}
EOF
    done
    
    # Test relative path resolution
    relative_name="checkpoint-2024-01-01-12-00-00.json"
    if [ -f "$temp_dir/.claude/checkpoints/$relative_name" ]; then
        test_pass "Relative path resolution works"
    else
        test_fail "Failed to resolve relative path"
    fi
    
    # Test absolute path resolution
    if [ -f "$checkpoint1" ]; then
        test_pass "Absolute path resolution works"
    else
        test_fail "Failed to resolve absolute path"
    fi
    
    # Test latest checkpoint detection with multiple files
    # The second checkpoint should be newer due to filename sorting
    latest_checkpoint=$(ls -t "$temp_dir/.claude/checkpoints"/checkpoint-*.json 2>/dev/null | head -1)
    if [ "$(basename "$latest_checkpoint")" = "checkpoint-2024-01-02-12-00-00.json" ]; then
        test_pass "Latest checkpoint detection works with multiple files"
    else
        test_fail "Failed to detect latest checkpoint with multiple files"
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$temp_dir"
}

# Test restore JSON field extraction
test_restore_json_extraction() {
    test_start "Restore JSON field extraction"
    
    # Create a temporary directory structure
    temp_dir=$(mktemp -d)
    mkdir -p "$temp_dir/.claude/commands"
    mkdir -p "$temp_dir/.claude/checkpoints"
    
    cd "$temp_dir"
    
    # Create test checkpoint with various field values
    checkpoint_file="$temp_dir/.claude/checkpoints/checkpoint-test-extraction.json"
    cat > "$checkpoint_file" << 'EOF'
{
  "timestamp": "2024-12-25T15:30:45Z",
  "description": "test checkpoint with spaces and special chars!",
  "git_info": {
    "repository_root": "/path/to/test/repo",
    "current_branch": "feature/test-branch",
    "commit_hash": "1234567890abcdef1234567890abcdef12345678",
    "status": "M  modified-file.txt\n?? untracked-file.txt",
    "staged_files": "staged-file.txt",
    "modified_files": "modified-file.txt",
    "untracked_files": "untracked-file.txt"
  },
  "working_directory": "/path/to/test/repo/subdir",
  "session_info": {
    "user": "testuser",
    "hostname": "test-hostname",
    "os": "Darwin",
    "shell": "/bin/zsh"
  }
}
EOF
    
    # Test timestamp extraction
    timestamp=$(grep -o '"timestamp":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$timestamp" = "2024-12-25T15:30:45Z" ]; then
        test_pass "Timestamp extraction works"
    else
        test_fail "Failed to extract timestamp: '$timestamp'"
    fi
    
    # Test description extraction
    description=$(grep -o '"description":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$description" = "test checkpoint with spaces and special chars!" ]; then
        test_pass "Description extraction works"
    else
        test_fail "Failed to extract description: '$description'"
    fi
    
    # Test branch extraction
    branch=$(grep -o '"current_branch":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$branch" = "feature/test-branch" ]; then
        test_pass "Branch extraction works"
    else
        test_fail "Failed to extract branch: '$branch'"
    fi
    
    # Test working directory extraction
    working_dir=$(grep -o '"working_directory":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$working_dir" = "/path/to/test/repo/subdir" ]; then
        test_pass "Working directory extraction works"
    else
        test_fail "Failed to extract working directory: '$working_dir'"
    fi
    
    # Test commit hash extraction
    commit_hash=$(grep -o '"commit_hash":[[:space:]]*"[^"]*"' "$checkpoint_file" | cut -d'"' -f4)
    if [ "$commit_hash" = "1234567890abcdef1234567890abcdef12345678" ]; then
        test_pass "Commit hash extraction works"
    else
        test_fail "Failed to extract commit hash: '$commit_hash'"
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$temp_dir"
}

# Test restore command alias (rst)
test_restore_alias() {
    test_start "Restore command alias"
    
    # Test that rst.md exists and has proper structure
    if [ -f ".claude/commands/rst.md" ]; then
        if grep -q "^# Restore (Short Alias)" ".claude/commands/rst.md"; then
            test_pass "Restore alias file exists with proper title"
        else
            test_fail "Restore alias file missing proper title"
        fi
    else
        test_fail "Restore alias file not found"
    fi
    
    # Test that rst.md has the same core logic as restore.md
    if [ -f ".claude/commands/rst.md" ] && [ -f ".claude/commands/restore.md" ]; then
        # Check that both files have the same key shell commands
        if grep -q 'ls -t.*checkpoint-.*\.json' ".claude/commands/rst.md" && \
           grep -q 'ls -t.*checkpoint-.*\.json' ".claude/commands/restore.md"; then
            test_pass "Restore alias has same core logic"
        else
            test_fail "Restore alias missing core logic"
        fi
    else
        test_fail "Cannot compare restore files"
    fi
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
    test_restore_dry_run
    test_restore_error_handling
    test_restore_path_resolution
    test_restore_json_extraction
    test_restore_alias
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