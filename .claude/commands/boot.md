# Boot Command

Initialize empty directories with complete GitHub repository infrastructure including git, GitHub repo creation, linting workflows, branch protection, project structure, documentation, and automated dependency management.

## Usage

```bash
/boot [project-name]
```

## Description

The `/boot` command provides a comprehensive solution for setting up new projects with modern best practices and complete GitHub infrastructure. It creates a production-ready repository with all essential components:

**Core Infrastructure:**
- Git repository initialization with safety checks
- GitHub remote repository creation via GitHub CLI
- Branch protection rules for main branch
- Multi-language linting workflows (Python, Markdown, Shell)
- Security scanning and automated dependency management

**Project Structure:**
- Standard directory layout (src/, tests/, docs/)
- Comprehensive .gitignore for multiple languages
- MIT LICENSE with auto-attribution
- Professional README template
- Contribution guidelines and coding standards

**Developer Experience:**
- EditorConfig for consistent coding style
- Dependabot configuration for automated updates
- GitHub Actions CI/CD pipelines
- Security scanning workflows

The command is **fully idempotent** - safe to run multiple times without overwriting existing files.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!echo -e "${BLUE}🚀 Bootstrap - Complete Repository Setup${NC}"
!echo -e "${BLUE}=======================================${NC}"
!echo ""

!# Parse project name from arguments
!PROJECT_NAME="${ARGUMENTS%% *}"
!if [ -z "$PROJECT_NAME" ]; then
!  PROJECT_NAME=$(basename "$(pwd)")
!fi

!echo -e "${CYAN}📁 Initializing project: ${YELLOW}$PROJECT_NAME${NC}"
!echo ""

!# Safe file creation function
!safe_create_file() {
!  local file_path="$1"
!  local content="$2"
!  
!  if [ -f "$file_path" ]; then
!    echo -e "${YELLOW}⚠️  Skipped: $file_path (already exists)${NC}"
!    return 1
!  else
!    echo "$content" > "$file_path"
!    echo -e "${GREEN}✅ Created: $file_path${NC}"
!    return 0
!  fi
!}

!# Safe directory creation function
!safe_create_dir() {
!  local dir_path="$1"
!  
!  if [ -d "$dir_path" ]; then
!    echo -e "${YELLOW}⚠️  Skipped: $dir_path/ (already exists)${NC}"
!    return 1
!  else
!    mkdir -p "$dir_path"
!    echo -e "${GREEN}✅ Created: $dir_path/${NC}"
!    return 0
!  fi
!}

!# Step 1: Git initialization
!echo -e "${BLUE}🔧 Step 1: Git Repository Initialization${NC}"
!if [ -d ".git" ]; then
!  echo -e "${YELLOW}⚠️  Skipped: Git repository already initialized${NC}"
!else
!  git init
!  echo -e "${GREEN}✅ Initialized Git repository${NC}"
!fi
!echo ""

!# Step 2: Project structure
!echo -e "${BLUE}📂 Step 2: Project Structure Creation${NC}"
!safe_create_dir "src"
!safe_create_dir "tests"
!safe_create_dir "docs"
!safe_create_dir ".github/workflows"

!# Create basic Python files if src was created
!if [ -d "src" ] && [ ! -f "src/__init__.py" ]; then
!  safe_create_file "src/__init__.py" ""
!  safe_create_file "src/main.py" "#!/usr/bin/env python3
!\"\"\"
!$PROJECT_NAME - Main application module.
!\"\"\"

!def main():
!    \"\"\"Main entry point for the application.\"\"\"
!    print(\"Hello from $PROJECT_NAME!\")

!if __name__ == \"__main__\":
!    main()
!"
!fi

!# Create basic test file
!if [ -d "tests" ] && [ ! -f "tests/test_main.py" ]; then
!  safe_create_file "tests/__init__.py" ""
!  safe_create_file "tests/test_main.py" "#!/usr/bin/env python3
!\"\"\"
!Tests for $PROJECT_NAME main module.
!\"\"\"

!import unittest
!import sys
!import os

!# Add src directory to path for imports
!sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

!try:
!    from main import main
!except ImportError:
!    main = None

!class TestMain(unittest.TestCase):
!    \"\"\"Test cases for main functionality.\"\"\"
!    
!    def test_main_exists(self):
!        \"\"\"Test that main function exists.\"\"\"
!        self.assertIsNotNone(main, \"main function should be defined\")

!if __name__ == '__main__':
!    unittest.main()
!"
!fi
!echo ""

!# Step 3: Configuration files
!echo -e "${BLUE}⚙️  Step 3: Configuration Files${NC}"

!# .gitignore
!safe_create_file ".gitignore" "# Byte-compiled / optimized / DLL files
!__pycache__/
!*.py[cod]
!*\$py.class

!# C extensions
!*.so

!# Distribution / packaging
!.Python
!build/
!develop-eggs/
!dist/
!downloads/
!eggs/
!.eggs/
!lib/
!lib64/
!parts/
!sdist/
!var/
!wheels/
!share/python-wheels/
!*.egg-info/
!.installed.cfg
!*.egg
!MANIFEST

!# PyInstaller
!*.manifest
!*.spec

!# Installer logs
!pip-log.txt
!pip-delete-this-directory.txt

!# Unit test / coverage reports
!htmlcov/
!.tox/
!.nox/
!.coverage
!.coverage.*
!.cache
!nosetests.xml
!coverage.xml
!*.cover
!*.py,cover
!.hypothesis/
!.pytest_cache/
!cover/

!# Virtual environments
!.env
!.venv
!env/
!venv/
!ENV/
!env.bak/
!venv.bak/

!# IDEs
!.vscode/
!.idea/
!*.swp
!*.swo
!*~

!# OS files
!.DS_Store
!.DS_Store?
!._*
!.Spotlight-V100
!.Trashes
!ehthumbs.db
!Thumbs.db

!# Node.js
!node_modules/
!npm-debug.log*
!yarn-debug.log*
!yarn-error.log*

!# Logs
!logs
!*.log

!# Runtime data
!pids
!*.pid
!*.seed
!*.pid.lock

!# Temporary folders
!tmp/
!temp/
!"

!# .editorconfig
!safe_create_file ".editorconfig" "root = true

![*]
!charset = utf-8
!end_of_line = lf
!insert_final_newline = true
!trim_trailing_whitespace = true
!indent_style = space
!indent_size = 4

![*.{yml,yaml}]
!indent_size = 2

![*.{json,js,ts}]
!indent_size = 2

![*.{md,markdown}]
!trim_trailing_whitespace = false

![Makefile]
!indent_style = tab
!"

!# Python requirements files
!safe_create_file "requirements.txt" "# Production dependencies
!# Add your project dependencies here
!# Example:
!# requests>=2.25.0
!# numpy>=1.20.0
!"

!safe_create_file "requirements-dev.txt" "# Development dependencies
!-r requirements.txt

!# Testing
!pytest>=6.0.0
!pytest-cov>=2.10.0

!# Code quality
!flake8>=3.8.0
!black>=21.0.0
!isort>=5.0.0

!# Documentation
!sphinx>=4.0.0
!"
!echo ""

!# Step 4: Documentation
!echo -e "${BLUE}📖 Step 4: Documentation${NC}"

!# Get git user info for attribution
!GIT_USER_NAME=$(git config user.name 2>/dev/null || echo "Your Name")
!GIT_USER_EMAIL=$(git config user.email 2>/dev/null || echo "your.email@example.com")
!CURRENT_YEAR=$(date +%Y)

!# README.md
!safe_create_file "README.md" "# $PROJECT_NAME

!Brief description of what $PROJECT_NAME does.

!## Features

!- 🚀 Modern Python project structure
!- 🔍 Comprehensive testing setup
!- 📋 Code quality tools (flake8, black, isort)
!- 🔒 Security scanning workflows
!- 🤖 Automated dependency management with Dependabot
!- 📚 Documentation ready

!## Installation

!\`\`\`bash
!# Clone the repository
!git clone https://github.com/YOUR_USERNAME/$PROJECT_NAME.git
!cd $PROJECT_NAME

!# Create virtual environment
!python -m venv venv
!source venv/bin/activate  # On Windows: venv\\Scripts\\activate

!# Install dependencies
!pip install -r requirements.txt
!\`\`\`

!## Usage

!\`\`\`bash
!# Run the main application
!python src/main.py

!# Run tests
!python -m pytest tests/

!# Run with coverage
!python -m pytest tests/ --cov=src
!\`\`\`

!## Development

!\`\`\`bash
!# Install development dependencies
!pip install -r requirements-dev.txt

!# Run code formatting
!black src/ tests/
!isort src/ tests/

!# Run linting
!flake8 src/ tests/

!# Run all quality checks
!black --check src/ tests/
!isort --check-only src/ tests/
!flake8 src/ tests/
!pytest tests/ --cov=src
!\`\`\`

!## Contributing

!Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

!## License

!This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

!## Author

!$GIT_USER_NAME <$GIT_USER_EMAIL>
!"

!# CONTRIBUTING.md
!safe_create_file "CONTRIBUTING.md" "# Contributing to $PROJECT_NAME

!Thank you for your interest in contributing to $PROJECT_NAME! This document provides guidelines and instructions for contributing.

!## Code of Conduct

!This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

!## How to Contribute

!### Reporting Bugs

!Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

!- A clear and descriptive title
!- Steps to reproduce the behavior
!- Expected vs actual behavior
!- Environment details (OS, Python version, etc.)

!### Suggesting Enhancements

!Enhancement suggestions are welcome! Please provide:

!- A clear and descriptive title
!- A detailed description of the proposed functionality
!- Examples of how the enhancement would be used

!### Pull Requests

!1. Fork the repository
!2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
!3. Make your changes
!4. Add tests for your changes
!5. Ensure all tests pass
!6. Run code quality checks
!7. Commit your changes (\`git commit -m 'Add amazing feature'\`)
!8. Push to your branch (\`git push origin feature/amazing-feature\`)
!9. Open a Pull Request

!## Development Setup

!\`\`\`bash
!# Clone your fork
!git clone https://github.com/YOUR_USERNAME/$PROJECT_NAME.git
!cd $PROJECT_NAME

!# Create virtual environment
!python -m venv venv
!source venv/bin/activate

!# Install development dependencies
!pip install -r requirements-dev.txt
!\`\`\`

!## Code Style

!This project uses:

!- **Black** for code formatting
!- **isort** for import sorting
!- **flake8** for linting
!- **pytest** for testing

!Run quality checks before submitting:

!\`\`\`bash
!# Format code
!black src/ tests/
!isort src/ tests/

!# Check formatting and linting
!black --check src/ tests/
!isort --check-only src/ tests/
!flake8 src/ tests/

!# Run tests with coverage
!pytest tests/ --cov=src --cov-report=html
!\`\`\`

!## Testing

!- Write tests for new functionality
!- Ensure all tests pass before submitting
!- Maintain or improve code coverage
!- Use descriptive test names and docstrings

!## Documentation

!- Update README.md for user-facing changes
!- Add docstrings to new functions and classes
!- Update this CONTRIBUTING.md if the development process changes

!Thank you for contributing!
!"

!# MIT LICENSE
!safe_create_file "LICENSE" "MIT License

!Copyright (c) $CURRENT_YEAR $GIT_USER_NAME

!Permission is hereby granted, free of charge, to any person obtaining a copy
!of this software and associated documentation files (the \"Software\"), to deal
!in the Software without restriction, including without limitation the rights
!to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
!copies of the Software, and to permit persons to whom the Software is
!furnished to do so, subject to the following conditions:

!The above copyright notice and this permission notice shall be included in all
!copies or substantial portions of the Software.

!THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
!IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
!FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
!AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
!LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
!OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
!SOFTWARE.
!"
!echo ""

!# Step 5: GitHub Actions workflows
!echo -e "${BLUE}🔄 Step 5: GitHub Actions Workflows${NC}"

!# Linting workflow
!safe_create_file ".github/workflows/lint.yml" "name: Code Quality

!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]

!jobs:
!  python-lint:
!    runs-on: ubuntu-latest
!    name: Python Linting
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Set up Python
!      uses: actions/setup-python@v4
!      with:
!        python-version: '3.9'
!    
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    
!    - name: Run Black (Code Formatting)
!      run: black --check --diff src/ tests/
!    
!    - name: Run isort (Import Sorting)
!      run: isort --check-only --diff src/ tests/
!    
!    - name: Run flake8 (Linting)
!      run: flake8 src/ tests/

!  markdown-lint:
!    runs-on: ubuntu-latest
!    name: Markdown Linting
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Run markdownlint
!      uses: articulate/actions-markdownlint@v1
!      with:
!        config: .markdownlint.json
!        files: '*.md'

!  shell-lint:
!    runs-on: ubuntu-latest
!    name: Shell Script Linting
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Run ShellCheck
!      uses: ludeeus/action-shellcheck@master
!      with:
!        scandir: './scripts'
!        severity: warning
!"

!# Security scanning workflow
!safe_create_file ".github/workflows/security.yml" "name: Security Scanning

!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!  schedule:
!    - cron: '0 6 * * 1'  # Weekly on Mondays

!jobs:
!  security-scan:
!    runs-on: ubuntu-latest
!    name: Security Analysis
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Run Super-Linter
!      uses: super-linter/super-linter@v5
!      env:
!        DEFAULT_BRANCH: main
!        GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
!        VALIDATE_PYTHON_FLAKE8: true
!        VALIDATE_PYTHON_BLACK: true
!        VALIDATE_MARKDOWN: true
!        VALIDATE_YAML: true
!        VALIDATE_JSON: true
!        VALIDATE_BASH: true
!        VALIDATE_DOCKERFILE: true
!"

!# Testing workflow
!safe_create_file ".github/workflows/test.yml" "name: Tests

!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]

!jobs:
!  test:
!    runs-on: ubuntu-latest
!    strategy:
!      matrix:
!        python-version: [\"3.8\", \"3.9\", \"3.10\", \"3.11\"]
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Set up Python \${{ matrix.python-version }}
!      uses: actions/setup-python@v4
!      with:
!        python-version: \${{ matrix.python-version }}
!    
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    
!    - name: Run tests with pytest
!      run: |
!        pytest tests/ --cov=src --cov-report=xml --cov-report=html
!    
!    - name: Upload coverage to Codecov
!      uses: codecov/codecov-action@v3
!      if: matrix.python-version == '3.9'
!      with:
!        file: ./coverage.xml
!        fail_ci_if_error: false
!"
!echo ""

!# Step 6: Dependabot configuration
!echo -e "${BLUE}🤖 Step 6: Dependabot Configuration${NC}"

!safe_create_file ".github/dependabot.yml" "version: 2
!updates:
!  # Python dependencies
!  - package-ecosystem: \"pip\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 10
!    reviewers:
!      - \"$GIT_USER_NAME\"
!    assignees:
!      - \"$GIT_USER_NAME\"
!    commit-message:
!      prefix: \"deps\"
!      prefix-development: \"deps-dev\"
!    labels:
!      - \"dependencies\"
!      - \"python\"

!  # GitHub Actions
!  - package-ecosystem: \"github-actions\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 5
!    reviewers:
!      - \"$GIT_USER_NAME\"
!    assignees:
!      - \"$GIT_USER_NAME\"
!    commit-message:
!      prefix: \"ci\"
!    labels:
!      - \"dependencies\"
!      - \"github-actions\"

!  # Docker (if Dockerfile exists)
!  - package-ecosystem: \"docker\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 5
!    reviewers:
!      - \"$GIT_USER_NAME\"
!    assignees:
!      - \"$GIT_USER_NAME\"
!    commit-message:
!      prefix: \"docker\"
!    labels:
!      - \"dependencies\"
!      - \"docker\"

!  # NPM (if package.json exists)
!  - package-ecosystem: \"npm\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 10
!    reviewers:
!      - \"$GIT_USER_NAME\"
!    assignees:
!      - \"$GIT_USER_NAME\"
!    commit-message:
!      prefix: \"deps\"
!      prefix-development: \"deps-dev\"
!    labels:
!      - \"dependencies\"
!      - \"javascript\"
!"

!# Markdown linting config
!safe_create_file ".markdownlint.json" "{
!  \"MD013\": {
!    \"line_length\": 120,
!    \"code_blocks\": false,
!    \"tables\": false
!  },
!  \"MD033\": false,
!  \"MD041\": false
!}
!"
!echo ""

!# Step 7: GitHub repository creation
!echo -e "${BLUE}🐙 Step 7: GitHub Repository Setup${NC}"

!# Check if GitHub CLI is available
!if ! command -v gh &> /dev/null; then
!  echo -e "${YELLOW}⚠️  GitHub CLI not found. Skipping remote repository creation.${NC}"
!  echo -e "${CYAN}📖 To create GitHub repository manually:${NC}"
!  echo "1. Install GitHub CLI: https://cli.github.com/"
!  echo "2. Run: gh auth login"
!  echo "3. Run: gh repo create $PROJECT_NAME --public --source=. --push"
!else
!  # Check if already has remote
!  if git remote get-url origin &> /dev/null; then
!    echo -e "${YELLOW}⚠️  Git remote 'origin' already exists. Skipping repository creation.${NC}"
!  else
!    echo -e "${CYAN}Creating GitHub repository: $PROJECT_NAME${NC}"
!    
!    # Create repository
!    if gh repo create "$PROJECT_NAME" --public --source=. --remote=origin 2>/dev/null; then
!      echo -e "${GREEN}✅ GitHub repository created successfully${NC}"
!      
!      # Initial commit and push
!      git add .
!      git commit -m "Initial commit: Bootstrap project with complete infrastructure

!- Git repository initialization
!- Complete project structure (src/, tests/, docs/)
!- Python application template with tests
!- Comprehensive configuration (.gitignore, .editorconfig, requirements)
!- Professional documentation (README, CONTRIBUTING, LICENSE)
!- GitHub Actions workflows (linting, testing, security)
!- Dependabot configuration for automated updates
!- MIT license with proper attribution

!Generated with claude-slash bootstrap command"
!      
!      if git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null; then
!        echo -e "${GREEN}✅ Initial commit pushed to GitHub${NC}"
!      else
!        echo -e "${YELLOW}⚠️  Failed to push initial commit. Push manually later.${NC}"
!      fi
!    else
!      echo -e "${YELLOW}⚠️  Failed to create GitHub repository. Create manually if needed.${NC}"
!    fi
!  fi
!fi
!echo ""

!# Step 8: Branch protection
!echo -e "${BLUE}🛡️  Step 8: Branch Protection${NC}"

!if command -v gh &> /dev/null && git remote get-url origin &> /dev/null; then
!  # Get the default branch name
!  default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
!  
!  echo -e "${CYAN}Setting up branch protection for: $default_branch${NC}"
!  
!  # Enable branch protection
!  if gh api "repos/:owner/:repo/branches/$default_branch/protection" \
!    --method PUT \
!    --field required_status_checks='{"strict":true,"contexts":["Python Linting","Markdown Linting","Shell Script Linting","Security Analysis"]}' \
!    --field enforce_admins=true \
!    --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
!    --field restrictions=null 2>/dev/null; then
!    echo -e "${GREEN}✅ Branch protection enabled for $default_branch${NC}"
!  else
!    echo -e "${YELLOW}⚠️  Could not set up branch protection. Configure manually in GitHub settings.${NC}"
!  fi
!else
!  echo -e "${YELLOW}⚠️  GitHub CLI not available or no remote. Configure branch protection manually.${NC}"
!fi
!echo ""

!# Step 9: GitHub Apps recommendations
!echo -e "${BLUE}📱 Step 9: Recommended GitHub Apps${NC}"
!echo -e "${CYAN}Consider installing these GitHub Apps for enhanced functionality:${NC}"
!echo ""
!echo -e "${PURPLE}🔒 Security:${NC}"
!echo "• Dependabot (automated dependency updates) - Already configured!"
!echo "• CodeQL (security analysis) - Enable in Security tab"
!echo "• Snyk (vulnerability scanning)"
!echo ""
!echo -e "${PURPLE}📊 Code Quality:${NC}"
!echo "• Codecov (code coverage reporting) - Already configured!"
!echo "• SonarCloud (code quality analysis)"
!echo "• DeepCode (AI-powered code analysis)"
!echo ""
!echo -e "${PURPLE}🤖 Automation:${NC}"
!echo "• Renovate (advanced dependency management)"
!echo "• Mergify (automated PR merging)"
!echo "• Semantic Release (automated versioning)"
!echo ""

!# Final summary
!echo -e "${GREEN}🎉 Bootstrap Complete!${NC}"
!echo -e "${GREEN}===================${NC}"
!echo ""
!echo -e "${CYAN}📁 Project: ${YELLOW}$PROJECT_NAME${NC}"
!echo -e "${CYAN}📂 Structure: ${GREEN}src/, tests/, docs/, .github/${NC}"
!echo -e "${CYAN}📋 Documentation: ${GREEN}README.md, CONTRIBUTING.md, LICENSE${NC}"
!echo -e "${CYAN}⚙️  Configuration: ${GREEN}.gitignore, .editorconfig, requirements.txt${NC}"
!echo -e "${CYAN}🔄 Workflows: ${GREEN}Linting, Testing, Security Scanning${NC}"
!echo -e "${CYAN}🤖 Automation: ${GREEN}Dependabot configured${NC}"
!echo ""
!echo -e "${BLUE}Next steps:${NC}"
!echo "1. Review and customize the generated files"
!echo "2. Install dependencies: ${CYAN}pip install -r requirements-dev.txt${NC}"
!echo "3. Run tests: ${CYAN}pytest tests/${NC}"
!echo "4. Start coding in ${CYAN}src/main.py${NC}"
!echo "5. Configure GitHub Apps for enhanced functionality"
!echo ""
!echo -e "${GREEN}Happy coding! 🚀${NC}"