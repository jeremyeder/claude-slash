# Bootstrap

Initialize an empty directory with complete GitHub repository infrastructure.

## Usage

```
/bootstrap [project-name]
```

## Description

Creates a complete modern repository setup with all the essential infrastructure for GitHub-based development projects.

## Implementation

!# Get the git repository root directory
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!
!# Set default project name if not provided
!PROJECT_NAME=${ARGUMENTS:-"test-repo"}
!
!# Color codes for output
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!NC='\033[0m' # No Color
!
!# Helper functions
!safe_create_file() {
!    local file_path="$1"
!    local content="$2"
!    if [[ -f "$file_path" ]]; then
!        echo -e "${YELLOW}⚠️  Skipping $file_path (already exists)${NC}"
!        return 1
!    else
!        echo "$content" > "$file_path"
!        echo -e "${GREEN}✅ Created $file_path${NC}"
!        return 0
!    fi
!}
!
!safe_create_dir() {
!    local dir_path="$1"
!    if [[ -d "$dir_path" ]]; then
!        echo -e "${YELLOW}⚠️  Skipping $dir_path (already exists)${NC}"
!        return 1
!    else
!        mkdir -p "$dir_path"
!        echo -e "${GREEN}✅ Created directory $dir_path${NC}"
!        return 0
!    fi
!}
!
!echo -e "${BLUE}🚀 Bootstrapping repository: $PROJECT_NAME${NC}"
!echo
!
!# Step 1: Git initialization
!echo -e "${BLUE}1. Initializing Git repository...${NC}"
!if [[ -d ".git" ]]; then
!    echo -e "${YELLOW}⚠️  Git repository already initialized${NC}"
!else
!    git init
!    echo -e "${GREEN}✅ Git repository initialized${NC}"
!fi
!echo
!
!# Step 2: Create GitHub repository
!echo -e "${BLUE}2. Creating GitHub repository...${NC}"
!if command -v gh >/dev/null 2>&1; then
!    # Check if remote already exists
!    if git remote get-url origin >/dev/null 2>&1; then
!        echo -e "${YELLOW}⚠️  GitHub remote already configured${NC}"
!    else
!        if gh repo create "$PROJECT_NAME" --public --confirm 2>/dev/null; then
!            git remote add origin "https://github.com/$(gh api user --jq .login)/$PROJECT_NAME.git"
!            echo -e "${GREEN}✅ GitHub repository created and remote configured${NC}"
!        else
!            echo -e "${RED}❌ Failed to create GitHub repository (may already exist)${NC}"
!        fi
!    fi
!else
!    echo -e "${RED}❌ GitHub CLI (gh) not found. Please install it first.${NC}"
!fi
!echo
!
!# Step 3: Create project structure
!echo -e "${BLUE}3. Creating project structure...${NC}"
!safe_create_dir "src"
!safe_create_dir "tests"
!safe_create_dir "docs"
!safe_create_dir ".github/workflows"
!echo
!
!# Step 4: Create GitHub Actions workflows
!echo -e "${BLUE}4. Creating GitHub Actions workflows...${NC}"
!
!# Python linting workflow
!safe_create_file ".github/workflows/python-lint.yml" "name: Python Lint
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  lint:
!    runs-on: ubuntu-latest
!    strategy:
!      matrix:
!        python-version: [3.8, 3.9, '3.10', '3.11']
!
!    steps:
!    - uses: actions/checkout@v4
!    - name: Set up Python \${{ matrix.python-version }}
!      uses: actions/setup-python@v4
!      with:
!        python-version: \${{ matrix.python-version }}
!    
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort
!        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    
!    - name: Lint with flake8
!      run: |
!        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
!        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
!    
!    - name: Check formatting with black
!      run: black --check .
!    
!    - name: Check import sorting with isort
!      run: isort --check-only ."
!
!# Markdown linting workflow
!safe_create_file ".github/workflows/markdown-lint.yml" "name: Markdown Lint
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  markdownlint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run markdownlint
!      uses: articulate/actions-markdownlint@v1
!      with:
!        config: .markdownlint.json
!        files: '*.md'
!        ignore: node_modules"
!
!# Shell script linting workflow
!safe_create_file ".github/workflows/shell-lint.yml" "name: Shell Lint
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  shellcheck:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run ShellCheck
!      uses: ludeeus/action-shellcheck@master
!      with:
!        scandir: './scripts'
!        format: gcc
!        severity: warning"
!
!# Security scanning workflow
!safe_create_file ".github/workflows/security-scan.yml" "name: Security Scan
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  security:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run Super Linter
!      uses: github/super-linter/slim@v4
!      env:
!        DEFAULT_BRANCH: main
!        GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"
!
!echo
!
!# Step 5: Configure branch protection
!echo -e "${BLUE}5. Configuring branch protection...${NC}"
!if command -v gh >/dev/null 2>&1 && git remote get-url origin >/dev/null 2>&1; then
!    # Try to set up branch protection (may fail if repo is new)
!    if gh api repos/:owner/:repo/branches/main/protection \
!        --method PUT \
!        --field required_status_checks='{"strict":true,"contexts":["lint"]}' \
!        --field enforce_admins=true \
!        --field required_pull_request_reviews='{"required_approving_review_count":1}' \
!        --field restrictions=null 2>/dev/null; then
!        echo -e "${GREEN}✅ Branch protection configured${NC}"
!    else
!        echo -e "${YELLOW}⚠️  Branch protection setup failed (normal for new repos)${NC}"
!    fi
!else
!    echo -e "${YELLOW}⚠️  Skipping branch protection (GitHub CLI or remote not configured)${NC}"
!fi
!echo
!
!# Step 6: Create README
!echo -e "${BLUE}6. Creating README...${NC}"
!USER_NAME=$(git config user.name || echo "Your Name")
!USER_EMAIL=$(git config user.email || echo "your.email@example.com")
!CURRENT_YEAR=$(date +%Y)
!
!safe_create_file "README.md" "# $PROJECT_NAME
!
!A modern Python project with comprehensive GitHub infrastructure.
!
!## Features
!
!- 🐍 Python project structure
!- 🧪 Testing framework setup
!- 📚 Documentation structure
!- 🚀 GitHub Actions CI/CD
!- 🔍 Code quality tools (linting, formatting)
!- 🔒 Security scanning
!- 🤖 Dependabot dependency updates
!- 📋 Branch protection rules
!
!## Getting Started
!
!### Prerequisites
!
!- Python 3.8+
!- pip
!
!### Installation
!
!1. Clone the repository:
!   \`\`\`bash
!   git clone https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME.git
!   cd $PROJECT_NAME
!   \`\`\`
!
!2. Install dependencies:
!   \`\`\`bash
!   pip install -r requirements.txt
!   pip install -r requirements-dev.txt  # For development
!   \`\`\`
!
!### Usage
!
!Add your usage instructions here.
!
!## Development
!
!### Running Tests
!
!\`\`\`bash
!python -m pytest tests/
!\`\`\`
!
!### Code Quality
!
!\`\`\`bash
!# Format code
!black .
!
!# Sort imports
!isort .
!
!# Lint code
!flake8 .
!\`\`\`
!
!## Contributing
!
!Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
!
!## License
!
!This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
!
!## Acknowledgments
!
!- Built with modern Python development best practices
!- Automated with GitHub Actions
!- Dependencies managed with Dependabot"
!
!echo
!
!# Step 7: Create MIT LICENSE
!echo -e "${BLUE}7. Creating MIT LICENSE...${NC}"
!safe_create_file "LICENSE" "MIT License
!
!Copyright (c) $CURRENT_YEAR $USER_NAME
!
!Permission is hereby granted, free of charge, to any person obtaining a copy
!of this software and associated documentation files (the \"Software\"), to deal
!in the Software without restriction, including without limitation the rights
!to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
!copies of the Software, and to permit persons to whom the Software is
!furnished to do so, subject to the following conditions:
!
!The above copyright notice and this permission notice shall be included in all
!copies or substantial portions of the Software.
!
!THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
!IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
!FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
!AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
!LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
!OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
!SOFTWARE."
!echo
!
!# Step 8: Create Dependabot configuration
!echo -e "${BLUE}8. Creating Dependabot configuration...${NC}"
!safe_create_dir ".github"
!safe_create_file ".github/dependabot.yml" "version: 2
!updates:
!  # Python dependencies
!  - package-ecosystem: \"pip\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    labels:
!      - \"dependencies\"
!      - \"python\"
!    reviewers:
!      - \"$USER_NAME\"
!    commit-message:
!      prefix: \"deps\"
!      include: \"scope\"
!    open-pull-requests-limit: 10
!
!  # GitHub Actions
!  - package-ecosystem: \"github-actions\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    labels:
!      - \"dependencies\"
!      - \"github-actions\"
!    reviewers:
!      - \"$USER_NAME\"
!    commit-message:
!      prefix: \"ci\"
!      include: \"scope\"
!    open-pull-requests-limit: 5
!
!  # Docker (if Dockerfile exists)
!  - package-ecosystem: \"docker\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    labels:
!      - \"dependencies\"
!      - \"docker\"
!    reviewers:
!      - \"$USER_NAME\"
!    commit-message:
!      prefix: \"docker\"
!      include: \"scope\"
!    open-pull-requests-limit: 5
!
!  # NPM (if package.json exists)
!  - package-ecosystem: \"npm\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    labels:
!      - \"dependencies\"
!      - \"npm\"
!    reviewers:
!      - \"$USER_NAME\"
!    commit-message:
!      prefix: \"deps\"
!      include: \"scope\"
!    open-pull-requests-limit: 10"
!echo
!
!# Additional infrastructure files
!echo -e "${BLUE}Creating additional infrastructure files...${NC}"
!
!# .gitignore
!safe_create_file ".gitignore" "# Byte-compiled / optimized / DLL files
!__pycache__/
!*.py[cod]
!*\$py.class
!
!# C extensions
!*.so
!
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
!
!# PyInstaller
!*.manifest
!*.spec
!
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
!
!# Virtual environments
!.env
!.venv
!env/
!venv/
!ENV/
!env.bak/
!venv.bak/
!
!# IDEs
!.vscode/
!.idea/
!*.swp
!*.swo
!*~
!
!# OS generated files
!.DS_Store
!.DS_Store?
!._*
!.Spotlight-V100
!.Trashes
!ehthumbs.db
!Thumbs.db
!
!# Node.js
!node_modules/
!npm-debug.log*
!yarn-debug.log*
!yarn-error.log*
!
!# Logs
!*.log
!logs/
!
!# Runtime data
!pids
!*.pid
!*.seed
!*.pid.lock
!
!# Optional npm cache directory
!.npm
!
!# Optional eslint cache
!.eslintcache"
!
!# .editorconfig
!safe_create_file ".editorconfig" "root = true
!
![*]
!charset = utf-8
!end_of_line = lf
!indent_style = space
!indent_size = 4
!insert_final_newline = true
!trim_trailing_whitespace = true
!
![*.{yml,yaml}]
!indent_size = 2
!
![*.md]
!trim_trailing_whitespace = false
!
![Makefile]
!indent_style = tab"
!
!# CONTRIBUTING.md
!safe_create_file "CONTRIBUTING.md" "# Contributing to $PROJECT_NAME
!
!Thank you for your interest in contributing to $PROJECT_NAME! We welcome contributions from everyone.
!
!## Getting Started
!
!1. Fork the repository
!2. Clone your fork: \`git clone https://github.com/YOUR_USERNAME/$PROJECT_NAME.git\`
!3. Create a branch: \`git checkout -b feature/your-feature-name\`
!4. Make your changes
!5. Run tests and linting
!6. Commit your changes: \`git commit -m 'Add some feature'\`
!7. Push to the branch: \`git push origin feature/your-feature-name\`
!8. Create a Pull Request
!
!## Development Setup
!
!1. Install dependencies:
!   \`\`\`bash
!   pip install -r requirements.txt
!   pip install -r requirements-dev.txt
!   \`\`\`
!
!2. Run tests:
!   \`\`\`bash
!   python -m pytest tests/
!   \`\`\`
!
!3. Run linting:
!   \`\`\`bash
!   flake8 .
!   black --check .
!   isort --check-only .
!   \`\`\`
!
!## Code Style
!
!- We use [Black](https://black.readthedocs.io/) for code formatting
!- We use [isort](https://pycqa.github.io/isort/) for import sorting
!- We use [flake8](https://flake8.pycqa.org/) for linting
!- Follow PEP 8 style guidelines
!
!## Pull Request Process
!
!1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
!2. Update the README.md with details of changes to the interface, if applicable
!3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
!4. Your Pull Request will be merged once you have the sign-off of at least one other developer
!
!## Code of Conduct
!
!This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.
!
!## Questions?
!
!Feel free to open an issue for any questions or concerns."
!
!# Python requirements files
!safe_create_file "requirements.txt" "# Add your production dependencies here
!# Example:
!# requests>=2.25.1
!# numpy>=1.21.0"
!
!safe_create_file "requirements-dev.txt" "# Development dependencies
!pytest>=6.0.0
!black>=21.0.0
!isort>=5.9.0
!flake8>=3.9.0
!coverage>=5.5"
!
!# .markdownlint.json
!safe_create_file ".markdownlint.json" "{
!  \"default\": true,
!  \"MD013\": {
!    \"line_length\": 120
!  },
!  \"MD033\": false,
!  \"MD041\": false
!}"
!
!# Create basic Python files
!safe_create_file "src/__init__.py" ""
!safe_create_file "src/main.py" "\"\"\"
!Main module for $PROJECT_NAME.
!\"\"\"
!
!
!def main():
!    \"\"\"Main entry point of the application.\"\"\"
!    print(\"Hello, $PROJECT_NAME!\")
!
!
!if __name__ == \"__main__\":
!    main()"
!
!safe_create_file "tests/__init__.py" ""
!safe_create_file "tests/test_main.py" "\"\"\"
!Tests for the main module.
!\"\"\"
!import pytest
!from src.main import main
!
!
!def test_main(capsys):
!    \"\"\"Test the main function.\"\"\"
!    main()
!    captured = capsys.readouterr()
!    assert \"Hello, $PROJECT_NAME!\" in captured.out"
!
!echo
!echo -e "${BLUE}GitHub Apps Installation Recommendations:${NC}"
!echo -e "${GREEN}Consider installing these GitHub Apps for enhanced functionality:${NC}"
!echo "• Dependabot (automated dependency updates)"
!echo "• CodeQL (security analysis)"
!echo "• GitHub Advanced Security (if available)"
!echo "• Renovate (alternative to Dependabot)"
!echo
!echo -e "${GREEN}🎉 Repository bootstrap complete!${NC}"
!echo -e "${BLUE}Project: $PROJECT_NAME${NC}"
!echo -e "${BLUE}Next steps:${NC}"
!echo "1. Review and customize the generated files"
!echo "2. Install GitHub Apps as needed"
!echo "3. Push your first commit to activate workflows"
!echo "4. Configure branch protection rules if needed"
!echo