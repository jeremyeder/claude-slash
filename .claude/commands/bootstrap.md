# Bootstrap

Initialize an empty directory with complete GitHub repository infrastructure.

## Usage

```
/project:bootstrap [project-name]
```

## Description

The bootstrap command creates a fully configured GitHub repository with modern development practices, including Git initialization, GitHub repository creation, CI/CD workflows, branch protection, project structure, documentation, and licensing. This command is designed to be **idempotent** - it can be run multiple times safely without causing issues.

## Implementation

!# Initialize repository with complete GitHub infrastructure
!set -e
!
!# Color codes for output
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!NC='\033[0m' # No Color
!
!# Get git root safely
!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!
!# Parse arguments
!PROJECT_NAME="${ARGUMENTS:-$(basename "$git_root")}"
!
!echo -e "${BLUE}🚀 Bootstrapping repository: ${PROJECT_NAME}${NC}"
!echo "Directory: $git_root"
!echo
!
!# Function to check if command exists
!command_exists() {
!    command -v "$1" >/dev/null 2>&1
!}
!
!# Function to safely create file if it doesn't exist
!safe_create_file() {
!    local file_path="$1"
!    local content="$2"
!    
!    if [ -f "$file_path" ]; then
!        echo -e "${YELLOW}⚠️  $file_path already exists - skipping${NC}"
!        return 0
!    fi
!    
!    echo "$content" > "$file_path"
!    echo -e "${GREEN}✅ Created $file_path${NC}"
!}
!
!# Function to safely create directory
!safe_create_dir() {
!    local dir_path="$1"
!    
!    if [ -d "$dir_path" ]; then
!        echo -e "${YELLOW}⚠️  Directory $dir_path already exists - skipping${NC}"
!        return 0
!    fi
!    
!    mkdir -p "$dir_path"
!    echo -e "${GREEN}✅ Created directory $dir_path${NC}"
!}
!
!# 1. Git initialization (idempotent)
!echo -e "${BLUE}1. Initializing Git repository...${NC}"
!cd "$git_root"
!
!if [ -d ".git" ]; then
!    echo -e "${YELLOW}⚠️  Git repository already initialized - skipping${NC}"
!else
!    git init
!    echo -e "${GREEN}✅ Git repository initialized${NC}"
!fi
!
!# 2. Create GitHub repository (idempotent)
!echo -e "${BLUE}2. Creating GitHub repository...${NC}"
!
!if ! command_exists gh; then
!    echo -e "${RED}❌ GitHub CLI (gh) not found. Please install it first.${NC}"
!    exit 1
!fi
!
!# Check if remote already exists
!if git remote get-url origin >/dev/null 2>&1; then
!    echo -e "${YELLOW}⚠️  Remote 'origin' already exists - skipping GitHub repo creation${NC}"
!    REPO_URL=$(git remote get-url origin)
!else
!    # Try to create GitHub repo
!    if gh repo create "$PROJECT_NAME" --public --source=. --remote=origin --push 2>/dev/null; then
!        echo -e "${GREEN}✅ GitHub repository created and connected${NC}"
!        REPO_URL="https://github.com/$(gh api user --jq .login)/$PROJECT_NAME"
!    else
!        echo -e "${YELLOW}⚠️  GitHub repository may already exist or creation failed - continuing${NC}"
!        REPO_URL="https://github.com/$(gh api user --jq .login)/$PROJECT_NAME"
!    fi
!fi
!
!# 3. Configure GitHub Actions workflows (idempotent)
!echo -e "${BLUE}3. Setting up GitHub Actions workflows...${NC}"
!
!safe_create_dir ".github/workflows"
!
!# Python and Markdown linting workflow
!safe_create_file ".github/workflows/lint.yml" 'name: Lint and Test
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
!        python-version: [3.8, 3.9, "3.10", "3.11"]
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Set up Python ${{ matrix.python-version }}
!      uses: actions/setup-python@v4
!      with:
!        python-version: ${{ matrix.python-version }}
!    
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort mypy
!        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    
!    - name: Lint with flake8
!      run: |
!        # Stop the build if there are Python syntax errors or undefined names
!        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
!        # Exit-zero treats all errors as warnings
!        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
!    
!    - name: Check code formatting with black
!      run: black --check .
!    
!    - name: Check import sorting with isort
!      run: isort --check-only .
!    
!    - name: Type check with mypy
!      run: mypy . --ignore-missing-imports || true
!
!  markdown-lint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - uses: actions/setup-node@v4
!      with:
!        node-version: 16
!    - run: npm install -g markdownlint-cli
!    - run: markdownlint "**/*.md" --ignore node_modules
!
!  shell-lint:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run ShellCheck
!      uses: ludeeus/action-shellcheck@master
!      with:
!        scandir: '"'"'./'"'"'
!'
!
!# Security scanning workflow
!safe_create_file ".github/workflows/security.yml" 'name: Security Scan
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!  schedule:
!    - cron: '"'"'0 2 * * 1'"'"' # Weekly on Mondays
!
!jobs:
!  security:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!      with:
!        fetch-depth: 0
!    
!    - name: Run GitHub Super Linter
!      uses: github/super-linter@v4
!      env:
!        DEFAULT_BRANCH: main
!        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
!        VALIDATE_ALL_CODEBASE: false
!        VALIDATE_PYTHON_FLAKE8: true
!        VALIDATE_MARKDOWN: true
!        VALIDATE_BASH: true
!'
!
!# 4. Configure branch protection (idempotent)
!echo -e "${BLUE}4. Configuring branch protection...${NC}"
!
!# Only set up branch protection if we have a valid GitHub repo
!if [ -n "$REPO_URL" ] && [[ "$REPO_URL" == https://github.com/* ]]; then
!    REPO_OWNER=$(echo "$REPO_URL" | cut -d'/' -f4)
!    REPO_NAME=$(echo "$REPO_URL" | cut -d'/' -f5)
!    
!    # Check if branch protection already exists
!    if gh api "repos/$REPO_OWNER/$REPO_NAME/branches/main/protection" >/dev/null 2>&1; then
!        echo -e "${YELLOW}⚠️  Branch protection already configured - skipping${NC}"
!    else
!        # Try to set up branch protection
!        if gh api --method PUT "repos/$REPO_OWNER/$REPO_NAME/branches/main/protection" \
!            --field required_status_checks='{"strict":true,"contexts":["lint","markdown-lint","shell-lint"]}' \
!            --field enforce_admins=true \
!            --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
!            --field restrictions=null >/dev/null 2>&1; then
!            echo -e "${GREEN}✅ Branch protection configured${NC}"
!        else
!            echo -e "${YELLOW}⚠️  Branch protection setup failed (may need repository admin rights) - continuing${NC}"
!        fi
!    fi
!else
!    echo -e "${YELLOW}⚠️  No valid GitHub repository URL - skipping branch protection${NC}"
!fi
!
!# 5. Initialize project structure (idempotent)
!echo -e "${BLUE}5. Creating project structure...${NC}"
!
!safe_create_dir "src"
!safe_create_dir "tests"
!safe_create_dir "docs"
!safe_create_dir "scripts"
!
!# Create basic Python project files
!safe_create_file "src/__init__.py" "# $PROJECT_NAME package"
!safe_create_file "tests/__init__.py" "# Tests for $PROJECT_NAME"
!safe_create_file "tests/test_main.py" "# Basic test file
!import unittest
!
!
!class TestMain(unittest.TestCase):
!    def test_placeholder(self):
!        \"\"\"Placeholder test to ensure test suite runs.\"\"\"
!        self.assertTrue(True)
!
!
!if __name__ == '"'"'__main__'"'"':
!    unittest.main()
!"
!
!# 6. Create README.md (idempotent)
!echo -e "${BLUE}6. Creating README.md...${NC}"
!
!safe_create_file "README.md" "# $PROJECT_NAME
!
![![Lint and Test](https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME/actions/workflows/lint.yml/badge.svg)](https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME/actions/workflows/lint.yml)
![![Security Scan](https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME/actions/workflows/security.yml/badge.svg)](https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME/actions/workflows/security.yml)
!
!## Description
!
!A brief description of what this project does and who it's for.
!
!## Installation
!
!\`\`\`bash
!git clone https://github.com/$(gh api user --jq .login 2>/dev/null || echo 'username')/$PROJECT_NAME.git
!cd $PROJECT_NAME
!pip install -r requirements.txt
!\`\`\`
!
!## Usage
!
!Provide examples of how to use your project.
!
!\`\`\`python
!# Example usage
!import $PROJECT_NAME
!\`\`\`
!
!## Development
!
!\`\`\`bash
!# Install development dependencies
!pip install -r requirements-dev.txt
!
!# Run tests
!python -m pytest tests/
!
!# Run linting
!flake8 .
!black .
!isort .
!\`\`\`
!
!## Contributing
!
!Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
!
!## License
!
!This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
!"
!
!# 7. Create MIT LICENSE (idempotent)
!echo -e "${BLUE}7. Creating MIT LICENSE...${NC}"
!
!# Get user info from git config
!USER_NAME=$(git config user.name 2>/dev/null || echo "Your Name")
!CURRENT_YEAR=$(date +%Y)
!
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
!
!# 8. GitHub Apps installation guidance
!echo -e "${BLUE}8. GitHub Apps recommendations...${NC}"
!echo -e "${GREEN}✅ Consider installing these GitHub Apps for enhanced functionality:${NC}"
!echo "   • Dependabot - Automated dependency updates"
!echo "   • CodeQL - Advanced security analysis"  
!echo "   • Renovate - Dependency management"
!echo "   • Codecov - Code coverage reporting"
!echo
!
!# Additional infrastructure files (idempotent)
!echo -e "${BLUE}Creating additional infrastructure files...${NC}"
!
!# .gitignore
!safe_create_file ".gitignore" "# Byte-compiled / optimized / DLL files
!__pycache__/
!*.py[cod]
!*$py.class
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
!# Installer logs
!pip-log.txt
!pip-delete-this-directory.txt
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
!# Jupyter Notebook
!.ipynb_checkpoints
!
!# IPython
!profile_default/
!ipython_config.py
!
!# pyenv
!.python-version
!
!# pipenv
!Pipfile.lock
!
!# poetry
!poetry.lock
!
!# pdm
!.pdm.toml
!.pdm-python
!.pdm-build/
!
!# PEP 582
!__pypackages__/
!
!# Celery
!celerybeat-schedule
!celerybeat.pid
!
!# SageMath parsed files
!*.sage.py
!
!# Environments
!.env
!.venv
!env/
!venv/
!ENV/
!env.bak/
!venv.bak/
!
!# Spyder project settings
!.spyderproject
!.spyproject
!
!# Rope project settings
!.ropeproject
!
!# mkdocs documentation
!/site
!
!# mypy
!.mypy_cache/
!.dmypy.json
!dmypy.json
!
!# Pyre type checker
!.pyre/
!
!# pytype static type analyzer
!.pytype/
!
!# Cython debug symbols
!cython_debug/
!
!# IDE
!.vscode/
!.idea/
!*.swp
!*.swo
!*~
!
!# OS
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
!yarn-error.log*"
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
![*.{js,json}]
!indent_size = 2
!
![*.md]
!trim_trailing_whitespace = false"
!
!# CONTRIBUTING.md
!safe_create_file "CONTRIBUTING.md" "# Contributing to $PROJECT_NAME
!
!Thank you for your interest in contributing to $PROJECT_NAME! We welcome contributions from everyone.
!
!## Development Process
!
!1. Fork the repository
!2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
!3. Make your changes
!4. Add tests for your changes
!5. Run the test suite to ensure everything passes
!6. Commit your changes (\`git commit -m 'Add amazing feature'\`)
!7. Push to the branch (\`git push origin feature/amazing-feature\`)
!8. Open a Pull Request
!
!## Code Style
!
!This project uses:
!- **Black** for Python code formatting
!- **isort** for import sorting
!- **flake8** for linting
!- **mypy** for type checking
!
!Run these tools before submitting:
!
!\`\`\`bash
!black .
!isort .
!flake8 .
!mypy .
!\`\`\`
!
!## Testing
!
!Please add tests for any new functionality:
!
!\`\`\`bash
!python -m pytest tests/
!\`\`\`
!
!## Pull Request Guidelines
!
!- Update the README.md with details of changes to the interface
!- Update the version numbers following [Semantic Versioning](https://semver.org/)
!- Ensure all tests pass and coverage remains high
!- Write clear, concise commit messages
!- Reference any related issues in your PR description
!
!## Code of Conduct
!
!This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. By participating, you are expected to uphold this code.
!
!## Questions?
!
!Feel free to open an issue for any questions or concerns about contributing!"
!
!# requirements.txt files
!safe_create_file "requirements.txt" "# Production dependencies
!# Add your project dependencies here
!"
!
!safe_create_file "requirements-dev.txt" "# Development dependencies
!pytest>=7.0.0
!black>=22.0.0
!isort>=5.10.0
!flake8>=4.0.0
!mypy>=0.950
!coverage>=6.0.0
!pre-commit>=2.17.0
!"
!
!echo
!echo -e "${GREEN}🎉 Bootstrap complete!${NC}"
!echo -e "${BLUE}Repository: $PROJECT_NAME${NC}"
!echo -e "${BLUE}Location: $git_root${NC}"
!
!if [ -n "$REPO_URL" ]; then
!    echo -e "${BLUE}GitHub URL: $REPO_URL${NC}"
!fi
!
!echo
!echo -e "${YELLOW}Next steps:${NC}"
!echo "1. Install development dependencies: pip install -r requirements-dev.txt"
!echo "2. Set up pre-commit hooks: pre-commit install"
!echo "3. Start developing your project!"
!echo "4. Push your initial commit: git add . && git commit -m 'Initial commit' && git push"
!echo
!echo -e "${GREEN}✅ All done! Your repository is ready for development.${NC}"