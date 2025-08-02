# Bootstrap Command

Initialize an empty directory with complete GitHub repository infrastructure, including git setup, GitHub repo creation, CI/CD workflows, branch protection, project structure, documentation, and automated dependency management.

## Usage

```bash
/bootstrap [project-name]
```

## Description

The bootstrap command provides a comprehensive repository initialization solution that sets up a complete modern development environment. It handles all the essential infrastructure components needed for a professional GitHub repository.

### Core Features

1. **Git initialization** - Creates local repository with safety checks
2. **GitHub repository creation** - Sets up remote repository using GitHub CLI
3. **GitHub Actions workflows** - Configures linting pipelines for Python, Markdown, and Shell scripts
4. **Branch protection** - Implements main branch protection rules with required status checks
5. **Project structure** - Creates standard directory layout (src/, tests/, docs/)
6. **Documentation** - Generates comprehensive README and contribution guidelines
7. **MIT License** - Auto-generates license with current year and user information
8. **Dependabot** - Configures automated dependency updates for multiple ecosystems

### Additional Infrastructure

- Comprehensive .gitignore for Python, Node.js, and development environments
- EditorConfig for consistent coding standards
- Security scanning workflows
- Development dependency templates

The command is **fully idempotent** - safe to run multiple times without overwriting existing files.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!project_name="$ARGUMENTS"

!# Color definitions
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m'

!# Helper functions for safe file creation
!safe_create_file() {
!  local file_path="$1"
!  local content="$2"
!  
!  if [ -f "$file_path" ]; then
!    echo -e "${YELLOW}⚠️  $file_path already exists, skipping${NC}"
!    return 1
!  else
!    echo "$content" > "$file_path"
!    echo -e "${GREEN}✅ Created $file_path${NC}"
!    return 0
!  fi
!}

!safe_create_dir() {
!  local dir_path="$1"
!  
!  if [ -d "$dir_path" ]; then
!    echo -e "${YELLOW}⚠️  Directory $dir_path already exists, skipping${NC}"
!    return 1
!  else
!    mkdir -p "$dir_path"
!    echo -e "${GREEN}✅ Created directory $dir_path${NC}"
!    return 0
!  fi
!}

!echo -e "${BLUE}🚀 Repository Bootstrap Initialization${NC}"
!echo -e "${BLUE}====================================${NC}"
!echo ""

!# Use project name or default to current directory name
!if [ -z "$project_name" ]; then
!  project_name=$(basename "$(pwd)")
!fi

!echo -e "${CYAN}📁 Project: $project_name${NC}"
!echo ""

!# 1. Git initialization
!echo -e "${BLUE}1. Initializing Git repository...${NC}"
!if [ -d ".git" ]; then
!  echo -e "${YELLOW}⚠️  Git repository already exists, skipping git init${NC}"
!else
!  git init
!  echo -e "${GREEN}✅ Git repository initialized${NC}"
!fi
!echo ""

!# 2. Create GitHub repository
!echo -e "${BLUE}2. Creating GitHub repository...${NC}"
!if command -v gh >/dev/null 2>&1; then
!  # Check if remote already exists
!  if git remote get-url origin >/dev/null 2>&1; then
!    echo -e "${YELLOW}⚠️  Git remote 'origin' already exists, skipping GitHub repo creation${NC}"
!  else
!    if gh repo create "$project_name" --public --source=. --remote=origin --push 2>/dev/null; then
!      echo -e "${GREEN}✅ GitHub repository created and connected${NC}"
!    else
!      echo -e "${YELLOW}⚠️  GitHub repository may already exist or creation failed${NC}"
!    fi
!  fi
!else
!  echo -e "${RED}❌ GitHub CLI (gh) not found. Please install it for repository creation.${NC}"
!  echo -e "${BLUE}💡 Install: https://cli.github.com/manual/installation${NC}"
!fi
!echo ""

!# 3. Configure GitHub Actions workflows
!echo -e "${BLUE}3. Setting up GitHub Actions workflows...${NC}"
!safe_create_dir ".github/workflows"

!# Linting workflow
!lint_workflow='.github/workflows/lint.yml'
!safe_create_file "$lint_workflow" 'name: Lint
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  python-lint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Set up Python
!      uses: actions/setup-python@v4
!      with:
!        python-version: "3.x"
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    - name: Lint with flake8
!      run: |
!        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
!        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
!    - name: Check formatting with black
!      run: black --check .
!    - name: Check import sorting with isort
!      run: isort --check-only .
!
!  markdown-lint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Lint Markdown files
!      uses: DavidAnson/markdownlint-cli2-action@v13
!      with:
!        globs: "**/*.md"
!
!  shell-lint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run ShellCheck
!      uses: ludeeus/action-shellcheck@master
!      with:
!        scandir: "./scripts"
!        severity: warning'

!# Security scanning workflow  
!security_workflow='.github/workflows/security.yml'
!safe_create_file "$security_workflow" 'name: Security Scan
!
!on:
!  push:
!    branches: [ main ]
!  pull_request:
!    branches: [ main ]
!  schedule:
!    - cron: "0 2 * * 1"  # Weekly on Mondays
!
!jobs:
!  security:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run Super Linter
!      uses: github/super-linter@v4
!      env:
!        DEFAULT_BRANCH: main
!        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
!        VALIDATE_ALL_CODEBASE: false'

!echo ""

!# 4. Configure branch protection
!echo -e "${BLUE}4. Configuring branch protection...${NC}"
!if command -v gh >/dev/null 2>&1; then
!  if gh api repos/:owner/:repo/branches/main/protection >/dev/null 2>&1; then
!    echo -e "${YELLOW}⚠️  Branch protection already configured, skipping${NC}"
!  else
!    if gh api repos/:owner/:repo/branches/main/protection \
!      --method PUT \
!      --field required_status_checks='{"strict":true,"contexts":["python-lint","markdown-lint","shell-lint"]}' \
!      --field enforce_admins=true \
!      --field required_pull_request_reviews='{"required_approving_review_count":1}' \
!      --field restrictions=null >/dev/null 2>&1; then
!      echo -e "${GREEN}✅ Branch protection configured${NC}"
!    else
!      echo -e "${YELLOW}⚠️  Branch protection setup failed (may require admin permissions)${NC}"
!    fi
!  fi
!else
!  echo -e "${YELLOW}⚠️  GitHub CLI not available, skipping branch protection${NC}"
!fi
!echo ""

!# 5. Initialize project structure
!echo -e "${BLUE}5. Creating project structure...${NC}"
!safe_create_dir "src"
!safe_create_dir "tests"
!safe_create_dir "docs"
!safe_create_dir "scripts"

!# Create initial Python files
!safe_create_file "src/__init__.py" "# $project_name package"
!safe_create_file "src/main.py" "#!/usr/bin/env python3
\"\"\"
Main module for $project_name.
\"\"\"

def main():
    \"\"\"Main entry point.\"\"\"
    print(\"Hello from $project_name!\")

if __name__ == \"__main__\":
    main()"

!safe_create_file "tests/__init__.py" ""
!safe_create_file "tests/test_main.py" "#!/usr/bin/env python3
\"\"\"
Tests for main module.
\"\"\"
import unittest
from src.main import main

class TestMain(unittest.TestCase):
    \"\"\"Test cases for main module.\"\"\"
    
    def test_main_runs(self):
        \"\"\"Test that main function runs without error.\"\"\"
        try:
            main()
        except Exception as e:
            self.fail(f\"main() raised {e} unexpectedly!\")

if __name__ == \"__main__\":
    unittest.main()"

!echo ""

!# 6. Create README
!echo -e "${BLUE}6. Generating README.md...${NC}"
!readme_content="# $project_name

A modern Python project with comprehensive CI/CD and development infrastructure.

## Features

- 🐍 Python-based project structure
- 🔧 Automated linting and formatting (flake8, black, isort)
- 📝 Markdown linting
- 🛡️ Security scanning
- 🤖 Dependabot dependency updates
- ✅ Branch protection with required status checks
- 📚 Comprehensive documentation

## Quick Start

\`\`\`bash
# Clone the repository
git clone https://github.com/\$(git config user.name)/$project_name.git
cd $project_name

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
python src/main.py

# Run tests
python -m pytest tests/
\`\`\`

## Development

### Prerequisites

- Python 3.7+
- pip

### Setup

\`\`\`bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 .
black --check .
isort --check-only .

# Run tests
python -m pytest tests/ -v
\`\`\`

### Project Structure

\`\`\`
$project_name/
├── src/                 # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── scripts/             # Build and utility scripts
├── .github/workflows/   # CI/CD workflows
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── README.md           # This file
└── LICENSE             # MIT License
\`\`\`

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with modern Python development best practices
- Automated CI/CD pipeline with GitHub Actions  
- Dependabot for automated dependency management"

!safe_create_file "README.md" "$readme_content"
!echo ""

!# 7. Create MIT LICENSE
!echo -e "${BLUE}7. Creating MIT LICENSE...${NC}"
!current_year=$(date +%Y)
!git_user_name=$(git config user.name 2>/dev/null || echo "Your Name")
!git_user_email=$(git config user.email 2>/dev/null || echo "your.email@example.com")

!license_content="MIT License

Copyright (c) $current_year $git_user_name <$git_user_email>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."

!safe_create_file "LICENSE" "$license_content"
!echo ""

!# 8. Configure Dependabot
!echo -e "${BLUE}8. Setting up Dependabot configuration...${NC}"
!dependabot_config='.github/dependabot.yml'
!safe_create_file "$dependabot_config" 'version: 2
!updates:
!  # Python dependencies
!  - package-ecosystem: "pip"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 10
!    labels:
!      - "dependencies"
!      - "python"
!    commit-message:
!      prefix: "deps"
!      prefix-development: "dev-deps"
!      include: "scope"
!
!  # GitHub Actions
!  - package-ecosystem: "github-actions"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 5
!    labels:
!      - "dependencies"
!      - "github-actions"
!    commit-message:
!      prefix: "ci"
!      include: "scope"
!
!  # Docker (if Dockerfile exists)
!  - package-ecosystem: "docker"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 5
!    labels:
!      - "dependencies"
!      - "docker"
!    commit-message:
!      prefix: "docker"
!      include: "scope"
!
!  # NPM (if package.json exists)
!  - package-ecosystem: "npm"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 10
!    labels:
!      - "dependencies"
!      - "javascript"
!    commit-message:
!      prefix: "deps"
!      prefix-development: "dev-deps"
!      include: "scope"'

!echo ""

!# Additional infrastructure files
!echo -e "${BLUE}9. Creating additional infrastructure files...${NC}"

!# .gitignore
!gitignore_content="# Python
__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Temporary folders
tmp/
temp/"

!safe_create_file ".gitignore" "$gitignore_content"

!# .editorconfig
!editorconfig_content="root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.{yml,yaml}]
indent_size = 2

[*.{json,js,ts}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false"

!safe_create_file ".editorconfig" "$editorconfig_content"

!# CONTRIBUTING.md
!contributing_content="# Contributing to $project_name

We love your input! We want to make contributing to $project_name as easy and transparent as possible.

## Development Process

1. Fork the repo and create your branch from \`main\`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Update the version numbers in any examples files and the README.md to the new version
3. The PR will be merged once you have the sign-off of at least one maintainer

## Development Setup

\`\`\`bash
# Clone your fork
git clone https://github.com/yourusername/$project_name.git
cd $project_name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 .
black --check .
isort --check-only .
\`\`\`

## Code Style

We use several tools to maintain code quality:

- **flake8** for linting
- **black** for code formatting  
- **isort** for import sorting
- **pytest** for testing

Please ensure your code passes all checks before submitting a PR.

## Any contributions you make will be under the MIT Software License

When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using Github's [issue tracker](https://github.com/\$(git config user.name)/$project_name/issues)

We use GitHub issues to track public bugs. Report a bug by opening a new issue.

## License

By contributing, you agree that your contributions will be licensed under its MIT License."

!safe_create_file "CONTRIBUTING.md" "$contributing_content"

!# Python requirements files
!safe_create_file "requirements.txt" "# Production dependencies
# Add your project dependencies here"

!safe_create_file "requirements-dev.txt" "# Development dependencies
flake8>=5.0.0
black>=22.0.0
isort>=5.10.0
pytest>=7.0.0
pytest-cov>=4.0.0"

!echo ""

!# GitHub Apps guidance
!echo -e "${BLUE}10. GitHub Apps recommendations...${NC}"
!echo -e "${CYAN}📱 Recommended GitHub Apps for enhanced functionality:${NC}"
!echo -e "${CYAN}   • Dependabot (enabled via dependabot.yml)${NC}"
!echo -e "${CYAN}   • CodeQL (security analysis)${NC}"
!echo -e "${CYAN}   • Super Linter (comprehensive linting)${NC}"
!echo -e "${CYAN}   • Codecov (code coverage reporting)${NC}"
!echo ""
!echo -e "${BLUE}💡 To install GitHub Apps:${NC}"
!echo -e "${BLUE}   1. Go to your repository settings${NC}"
!echo -e "${BLUE}   2. Navigate to 'Integrations & services'${NC}"
!echo -e "${BLUE}   3. Browse and install recommended apps${NC}"
!echo ""

!# Final summary
!echo -e "${GREEN}🎉 Bootstrap Complete!${NC}"
!echo -e "${GREEN}====================${NC}"
!echo ""
!echo -e "${CYAN}📋 Summary of what was created:${NC}"
!echo -e "${CYAN}  • Git repository initialized${NC}"
!echo -e "${CYAN}  • GitHub repository created (if gh CLI available)${NC}"
!echo -e "${CYAN}  • GitHub Actions workflows (lint.yml, security.yml)${NC}"
!echo -e "${CYAN}  • Branch protection configured${NC}"
!echo -e "${CYAN}  • Project structure (src/, tests/, docs/, scripts/)${NC}"
!echo -e "${CYAN}  • README.md with comprehensive documentation${NC}"
!echo -e "${CYAN}  • MIT LICENSE with your information${NC}"
!echo -e "${CYAN}  • Dependabot configuration for automated updates${NC}"
!echo -e "${CYAN}  • .gitignore, .editorconfig, CONTRIBUTING.md${NC}"
!echo -e "${CYAN}  • Python requirements files and sample code${NC}"
!echo ""
!echo -e "${GREEN}✨ Your repository is ready for development!${NC}"
!echo ""
!echo -e "${BLUE}Next steps:${NC}"
!echo -e "${BLUE}  1. Add your project dependencies to requirements.txt${NC}"
!echo -e "${BLUE}  2. Start developing in the src/ directory${NC}"
!echo -e "${BLUE}  3. Write tests in the tests/ directory${NC}"
!echo -e "${BLUE}  4. Commit and push your initial code${NC}"
!echo ""