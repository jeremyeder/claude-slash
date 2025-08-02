# Boot

Initialize an empty directory with complete GitHub repository infrastructure including git, GitHub repo creation, linting workflows, branch protection, project structure, documentation, and dependency management.

## Usage

```bash
/project:boot [project-name]
```

## Description

The boot command sets up a complete modern development environment in an empty directory, including all the essential GitHub repository infrastructure. This command is fully idempotent and can be run multiple times safely.

This is a shorthand alias for the `/project:bootstrap` command.

**Core Features:**
1. Git repository initialization
2. GitHub repository creation (requires GitHub CLI)
3. GitHub Actions workflows with Python, Markdown, and Shell linting
4. Branch protection configuration
5. Project structure initialization (src/, tests/, docs/)
6. README.md generation with comprehensive template
7. MIT LICENSE file with current year and user info
8. Dependabot configuration for automated dependency updates

**Additional Infrastructure:**
- .gitignore with comprehensive exclusions
- .editorconfig for consistent coding style
- CONTRIBUTING.md with contribution guidelines
- Security scanning workflows
- Python dependency files (requirements.txt, requirements-dev.txt)

## Implementation

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color
!
!# Get project name from arguments or use current directory name
!project_name="$ARGUMENTS"
!if [ -z "$project_name" ]; then
!    project_name=$(basename "$(pwd)")
!fi
!
!echo -e "${BLUE}🚀 Bootstrapping project: $project_name${NC}"
!echo
!
!# Helper functions for idempotent operations
!safe_create_file() {
!    local file="$1"
!    local content="$2"
!    if [ -f "$file" ]; then
!        echo -e "${YELLOW}⚠️  $file already exists, skipping${NC}"
!        return 1
!    else
!        echo "$content" > "$file"
!        echo -e "${GREEN}✅ Created $file${NC}"
!        return 0
!    fi
!}
!
!safe_create_dir() {
!    local dir="$1"
!    if [ -d "$dir" ]; then
!        echo -e "${YELLOW}⚠️  Directory $dir already exists, skipping${NC}"
!        return 1
!    else
!        mkdir -p "$dir"
!        echo -e "${GREEN}✅ Created directory $dir${NC}"
!        return 0
!    fi
!}
!
!# 1. Git repository initialization
!echo -e "${BLUE}1. Initializing Git repository...${NC}"
!if [ -d ".git" ]; then
!    echo -e "${YELLOW}⚠️  Git repository already initialized${NC}"
!else
!    git init
!    echo -e "${GREEN}✅ Git repository initialized${NC}"
!fi
!echo
!
!# 2. Create GitHub repository
!echo -e "${BLUE}2. Creating GitHub repository...${NC}"
!if command -v gh >/dev/null 2>&1; then
!    # Check if remote already exists
!    if git remote get-url origin >/dev/null 2>&1; then
!        echo -e "${YELLOW}⚠️  GitHub remote already configured${NC}"
!    else
!        if gh repo create "$project_name" --public --confirm; then
!            echo -e "${GREEN}✅ GitHub repository created and remote configured${NC}"
!        else
!            echo -e "${YELLOW}⚠️  GitHub repository creation failed or already exists${NC}"
!        fi
!    fi
!else
!    echo -e "${YELLOW}⚠️  GitHub CLI not found. Install gh to create repositories automatically${NC}"
!    echo "   Install: https://cli.github.com/"
!fi
!echo
!
!# 3. Configure GitHub Actions workflows
!echo -e "${BLUE}3. Creating GitHub Actions workflows...${NC}"
!safe_create_dir ".github/workflows"
!
!# Linting workflow
!safe_create_file ".github/workflows/lint.yml" "name: Lint Code
!
!on:
!  push:
!    branches: [ main, develop ]
!  pull_request:
!    branches: [ main, develop ]
!
!jobs:
!  lint-python:
!    runs-on: ubuntu-latest
!    if: contains(github.event.head_commit.message, '.py') || contains(github.event.pull_request.changed_files, '.py')
!    steps:
!    - uses: actions/checkout@v4
!    - name: Set up Python
!      uses: actions/setup-python@v4
!      with:
!        python-version: '3.x'
!    - name: Install dependencies
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort
!        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
!    - name: Lint with flake8
!      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
!    - name: Check formatting with black
!      run: black --check .
!    - name: Check imports with isort
!      run: isort --check-only .
!
!  lint-markdown:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Lint Markdown
!      uses: DavidAnson/markdownlint-cli2-action@v13
!      with:
!        globs: '**/*.md'
!
!  lint-shell:
!    runs-on: ubuntu-latest
!    if: contains(github.event.head_commit.message, '.sh') || contains(github.event.pull_request.changed_files, '.sh')
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run shellcheck
!      uses: ludeeus/action-shellcheck@master"
!
!# Security scanning workflow
!safe_create_file ".github/workflows/security.yml" "name: Security Scanning
!
!on:
!  push:
!    branches: [ main ]
!  pull_request:
!    branches: [ main ]
!  schedule:
!    - cron: '0 0 * * 0'  # Weekly on Sunday
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
!        GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
!        VALIDATE_ALL_CODEBASE: false"
!
!echo
!
!# 4. Configure branch protection
!echo -e "${BLUE}4. Configuring branch protection...${NC}"
!if command -v gh >/dev/null 2>&1 && git remote get-url origin >/dev/null 2>&1; then
!    if gh api repos/:owner/:repo/branches/main/protection >/dev/null 2>&1; then
!        echo -e "${YELLOW}⚠️  Branch protection already configured${NC}"
!    else
!        if gh api repos/:owner/:repo/branches/main/protection -X PUT \
!            --field required_status_checks='{"strict":true,"contexts":["lint-python","lint-markdown","lint-shell"]}' \
!            --field enforce_admins=true \
!            --field required_pull_request_reviews='{"required_approving_review_count":1}' \
!            --field restrictions=null 2>/dev/null; then
!            echo -e "${GREEN}✅ Branch protection configured${NC}"
!        else
!            echo -e "${YELLOW}⚠️  Branch protection configuration failed (may require admin permissions)${NC}"
!        fi
!    fi
!else
!    echo -e "${YELLOW}⚠️  GitHub CLI not configured or no remote repository${NC}"
!fi
!echo
!
!# 5. Initialize project structure
!echo -e "${BLUE}5. Creating project structure...${NC}"
!safe_create_dir "src"
!safe_create_dir "tests"
!safe_create_dir "docs"
!
!# Create basic Python files
!safe_create_file "src/__init__.py" ""
!safe_create_file "tests/__init__.py" ""
!safe_create_file "tests/test_example.py" "\"\"\"
!Example test file.
!\"\"\"
!
!def test_example():
!    \"\"\"Example test function.\"\"\"
!    assert True"
!
!# Python dependency files
!safe_create_file "requirements.txt" "# Production dependencies
!# Add your project dependencies here"
!
!safe_create_file "requirements-dev.txt" "# Development dependencies
!pytest>=7.0.0
!flake8>=5.0.0
!black>=22.0.0
!isort>=5.0.0"
!
!echo
!
!# 6. Create README
!echo -e "${BLUE}6. Creating README.md...${NC}"
!user_name=$(git config user.name || echo "Your Name")
!user_email=$(git config user.email || echo "you@example.com")
!
!safe_create_file "README.md" "# $project_name
!
!A modern Python project with comprehensive development infrastructure.
!
!## Features
!
!- 🐍 Python project structure with src/ layout
!- 🧪 Test framework with pytest
!- 🔍 Code quality tools (flake8, black, isort)
!- 🛡️ Security scanning with GitHub Actions
!- 📝 Markdown linting
!- 🔧 Shell script validation
!- 🤖 Automated dependency updates with Dependabot
!- 📋 Comprehensive documentation
!
!## Quick Start
!
!\`\`\`bash
!# Clone the repository
!git clone https://github.com/YOUR_USERNAME/$project_name.git
!cd $project_name
!
!# Install dependencies
!pip install -r requirements.txt
!pip install -r requirements-dev.txt
!
!# Run tests
!pytest
!
!# Format code
!black .
!isort .
!
!# Lint code
!flake8 .
!\`\`\`
!
!## Project Structure
!
!\`\`\`
!$project_name/
!├── src/                    # Source code
!├── tests/                  # Test files
!├── docs/                   # Documentation
!├── .github/workflows/      # GitHub Actions
!├── requirements.txt        # Production dependencies
!├── requirements-dev.txt    # Development dependencies
!├── README.md              # This file
!├── LICENSE                # MIT License
!├── CONTRIBUTING.md        # Contribution guidelines
!└── .gitignore            # Git ignore patterns
!\`\`\`
!
!## Development
!
!This project follows modern Python development practices:
!
!- **Code Formatting**: Black for consistent code style
!- **Import Sorting**: isort for organized imports
!- **Linting**: flake8 for code quality checks
!- **Testing**: pytest for unit and integration tests
!- **CI/CD**: GitHub Actions for automated testing and deployment
!
!## Contributing
!
!Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
!
!## License
!
!This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
!
!## Author
!
!$user_name <$user_email>"
!
!echo
!
!# 7. Create MIT LICENSE
!echo -e "${BLUE}7. Creating MIT LICENSE...${NC}"
!current_year=$(date +%Y)
!user_name=$(git config user.name || echo "Your Name")
!
!safe_create_file "LICENSE" "MIT License
!
!Copyright (c) $current_year $user_name
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
!echo
!
!# 8. Create Dependabot configuration
!echo -e "${BLUE}8. Creating Dependabot configuration...${NC}"
!safe_create_dir ".github"
!
!safe_create_file ".github/dependabot.yml" "version: 2
!updates:
!  # Python dependencies
!  - package-ecosystem: \"pip\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 10
!    commit-message:
!      prefix: \"deps\"
!      prefix-development: \"deps-dev\"
!    labels:
!      - \"dependencies\"
!      - \"python\"
!    assignees:
!      - \"$user_name\"
!
!  # GitHub Actions
!  - package-ecosystem: \"github-actions\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 5
!    commit-message:
!      prefix: \"ci\"
!    labels:
!      - \"dependencies\"
!      - \"github-actions\"
!    assignees:
!      - \"$user_name\"
!
!  # Docker (if Dockerfile exists)
!  - package-ecosystem: \"docker\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 5
!    commit-message:
!      prefix: \"docker\"
!    labels:
!      - \"dependencies\"
!      - \"docker\"
!    assignees:
!      - \"$user_name\"
!
!  # NPM (if package.json exists)
!  - package-ecosystem: \"npm\"
!    directory: \"/\"
!    schedule:
!      interval: \"weekly\"
!      day: \"monday\"
!    open-pull-requests-limit: 10
!    commit-message:
!      prefix: \"deps\"
!      prefix-development: \"deps-dev\"
!    labels:
!      - \"dependencies\"
!      - \"javascript\"
!    assignees:
!      - \"$user_name\""
!
!echo
!
!# Additional infrastructure files
!echo -e "${BLUE}9. Creating additional infrastructure files...${NC}"
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
!pip-wheel-metadata/
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
!
!# Translations
!*.mo
!*.pot
!
!# Django stuff:
!*.log
!local_settings.py
!db.sqlite3
!db.sqlite3-journal
!
!# Flask stuff:
!instance/
!.webassets-cache
!
!# Scrapy stuff:
!.scrapy
!
!# Sphinx documentation
!docs/_build/
!
!# PyBuilder
!target/
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
!# PEP 582
!__pypackages__/
!
!# Celery stuff
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
!# IDE files
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
!yarn-error.log*"
!
!# .editorconfig
!safe_create_file ".editorconfig" "root = true
!
![*]
!charset = utf-8
!end_of_line = lf
!insert_final_newline = true
!trim_trailing_whitespace = true
!indent_style = space
!indent_size = 4
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
!safe_create_file "CONTRIBUTING.md" "# Contributing to $project_name
!
!Thank you for your interest in contributing to $project_name! This document provides guidelines and information about contributing to this project.
!
!## Code of Conduct
!
!By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to the project maintainers.
!
!## How to Contribute
!
!### Reporting Bugs
!
!Before creating bug reports, please check the existing issues to avoid duplicates. When you are creating a bug report, please include as many details as possible:
!
!- Use a clear and descriptive title
!- Describe the exact steps which reproduce the problem
!- Provide specific examples to demonstrate the steps
!- Describe the behavior you observed after following the steps
!- Explain which behavior you expected to see instead and why
!- Include screenshots if applicable
!
!### Suggesting Enhancements
!
!Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:
!
!- Use a clear and descriptive title
!- Provide a step-by-step description of the suggested enhancement
!- Provide specific examples to demonstrate the steps
!- Describe the current behavior and explain which behavior you expected to see instead
!- Explain why this enhancement would be useful
!
!### Pull Requests
!
!- Fill in the required template
!- Do not include issue numbers in the PR title
!- Follow the Python styleguide
!- Include thoughtfully-worded, well-structured tests
!- Document new code based on the Documentation Styleguide
!- End all files with a newline
!
!## Development Process
!
!1. Fork the repository
!2. Create a new branch from main: \`git checkout -b feature/your-feature-name\`
!3. Make your changes
!4. Add tests for your changes
!5. Run the test suite: \`pytest\`
!6. Run linting: \`flake8 .\`
!7. Format code: \`black .\` and \`isort .\`
!8. Commit your changes: \`git commit -m 'Add some feature'\`
!9. Push to the branch: \`git push origin feature/your-feature-name\`
!10. Submit a pull request
!
!## Style Guidelines
!
!### Python Style Guide
!
!- Follow PEP 8
!- Use Black for code formatting
!- Use isort for import sorting
!- Write docstrings for all public functions and classes
!- Use type hints where appropriate
!
!### Git Commit Messages
!
!- Use the present tense (\"Add feature\" not \"Added feature\")
!- Use the imperative mood (\"Move cursor to...\" not \"Moves cursor to...\")
!- Limit the first line to 72 characters or less
!- Reference issues and pull requests liberally after the first line
!
!## Testing
!
!- Write tests for new functionality
!- Ensure all tests pass before submitting a PR
!- Maintain or improve code coverage
!- Use descriptive test names
!
!## Documentation
!
!- Update README.md if needed
!- Add docstrings to new functions and classes
!- Update any relevant documentation files
!- Include code examples in docstrings when helpful
!
!Thank you for contributing!"
!
!echo
!
!# GitHub Apps guidance
!echo -e "${BLUE}10. GitHub Apps recommendations...${NC}"
!echo -e "${GREEN}✅ Repository infrastructure complete!${NC}"
!echo
!echo -e "${PURPLE}🤖 Recommended GitHub Apps to install:${NC}"
!echo "• CodeQL Analysis - Security vulnerability scanning"
!echo "• Dependabot - Automated dependency updates (already configured)"
!echo "• GitHub Advanced Security - Enhanced security features"
!echo "• Codecov - Code coverage reporting"
!echo "• Renovate - Alternative dependency management"
!echo
!echo -e "${CYAN}📝 Next Steps:${NC}"
!echo "1. Review and customize the generated files"
!echo "2. Install recommended GitHub Apps"
!echo "3. Configure any additional integrations"
!echo "4. Start developing your project!"
!echo
!echo -e "${GREEN}🎉 Bootstrap completed successfully!${NC}"
!echo -e "${BLUE}Project: $project_name${NC}"