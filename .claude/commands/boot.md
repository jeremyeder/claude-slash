# Bootstrap Command (Short Alias)

Initialize an empty directory with complete GitHub repository infrastructure including dependency management.

## Usage

```bash
/boot [project-name]
```

## Description

This command sets up a complete GitHub repository from scratch with modern development infrastructure:

1. **Git initialization** - Repository setup with safety checks
2. **GitHub repository creation** - Remote repository via GitHub CLI
3. **GitHub Actions** - Blocking linters for Python, Markdown, and Shell
4. **Branch protection** - Main branch protection rules
5. **Project structure** - Standard directory layout
6. **Documentation** - README.md with project template
7. **MIT License** - Auto-generated with user information
8. **GitHub Apps** - Installation recommendations
9. **Dependabot** - Automated dependency updates

Additional infrastructure includes comprehensive `.gitignore`, `.editorconfig`, security scanning, and contribution guidelines.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!project_name="${ARGUMENTS:-$(basename "$(pwd)")}"

!# Color definitions
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m'

!echo -e "${BLUE}🚀 Bootstrap Repository Infrastructure${NC}"
!echo -e "${BLUE}====================================${NC}"
!echo -e "${CYAN}Project: ${project_name}${NC}"
!echo ""

!# 1. Git initialization (idempotent)
!echo -e "${CYAN}📁 1. Initializing Git repository...${NC}"
!if [ ! -d ".git" ]; then
!  git init
!  echo -e "${GREEN}   ✅ Git repository initialized${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  Git repository already exists${NC}"
!fi

!# 2. Create GitHub repository (idempotent check)
!echo -e "${CYAN}🌐 2. Creating GitHub repository...${NC}"
!if gh repo view >/dev/null 2>&1; then
!  echo -e "${YELLOW}   ⚠️  GitHub repository already exists${NC}"
!else
!  if command -v gh >/dev/null 2>&1; then
!    gh repo create "$project_name" --public --source=. --remote=origin --push || {
!      echo -e "${YELLOW}   ⚠️  Could not create GitHub repo (may already exist or auth issue)${NC}"
!    }
!    echo -e "${GREEN}   ✅ GitHub repository created${NC}"
!  else
!    echo -e "${YELLOW}   ⚠️  GitHub CLI not found. Install 'gh' to create remote repository${NC}"
!  fi
!fi

!# 3. Create .github directory structure (idempotent)
!echo -e "${CYAN}⚙️  3. Setting up GitHub Actions workflows...${NC}"
!mkdir -p .github/workflows

!# Python, Markdown, Shell linting workflow (idempotent)
!if [ ! -f ".github/workflows/lint.yml" ]; then
!cat > .github/workflows/lint.yml << 'EOF'
!name: Lint and Test
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
!        lint-type: [python, markdown, shell]
!    
!    steps:
!    - uses: actions/checkout@v4
!    
!    - name: Python Linting
!      if: matrix.lint-type == 'python'
!      run: |
!        python -m pip install --upgrade pip
!        pip install flake8 black isort
!        # Find Python files and run linters
!        if find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | head -1 | grep -q .; then
!          echo "Running Python linters..."
!          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
!          black --check --diff .
!          isort --check-only --diff .
!        else
!          echo "No Python files found, skipping Python linting"
!        fi
!    
!    - name: Markdown Linting
!      if: matrix.lint-type == 'markdown'
!      uses: DavidAnson/markdownlint-cli2-action@v16
!      with:
!        globs: '**/*.md'
!    
!    - name: Shell Linting
!      if: matrix.lint-type == 'shell'
!      run: |
!        # Install shellcheck
!        sudo apt-get update && sudo apt-get install -y shellcheck
!        # Find shell scripts and run shellcheck
!        if find . -name "*.sh" -o -name "*.bash" | head -1 | grep -q .; then
!          echo "Running shellcheck..."
!          find . -name "*.sh" -o -name "*.bash" | xargs shellcheck
!        else
!          echo "No shell scripts found, skipping shell linting"
!        fi
!
!  security:
!    runs-on: ubuntu-latest
!    steps:
!    - uses: actions/checkout@v4
!    - name: Run Super-Linter
!      uses: super-linter/super-linter@v5
!      env:
!        DEFAULT_BRANCH: main
!        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
!        VALIDATE_ALL_CODEBASE: false
!        VALIDATE_DOCKERFILE_HADOLINT: false
!        VALIDATE_JSCPD: false
!EOF
!  echo -e "${GREEN}   ✅ Linting workflow created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  Linting workflow already exists${NC}"
!fi

!# 4. Branch protection (requires GitHub CLI and proper permissions)
!echo -e "${CYAN}🛡️  4. Configuring branch protection...${NC}"
!if command -v gh >/dev/null 2>&1; then
!  if gh repo view >/dev/null 2>&1; then
!    gh api repos/:owner/:repo/branches/main/protection \
!      --method PUT \
!      --field required_status_checks='{"strict":true,"contexts":["lint"]}' \
!      --field enforce_admins=true \
!      --field required_pull_request_reviews='{"required_approving_review_count":1}' \
!      --field restrictions=null \
!      >/dev/null 2>&1 && {
!      echo -e "${GREEN}   ✅ Branch protection configured${NC}"
!    } || {
!      echo -e "${YELLOW}   ⚠️  Could not configure branch protection (may need admin permissions)${NC}"
!    }
!  else
!    echo -e "${YELLOW}   ⚠️  No GitHub repository found${NC}"
!  fi
!else
!  echo -e "${YELLOW}   ⚠️  GitHub CLI not available for branch protection${NC}"
!fi

!# 5. Project structure initialization (idempotent)
!echo -e "${CYAN}📂 5. Initializing project structure...${NC}"
!mkdir -p src tests docs
!
!# Create basic Python project structure if needed
!if [ ! -f "src/__init__.py" ]; then
!  touch src/__init__.py
!  echo -e "${GREEN}   ✅ Python source structure created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  Source structure already exists${NC}"
!fi
!
!if [ ! -f "tests/__init__.py" ]; then
!  touch tests/__init__.py
!  cat > tests/test_example.py << 'EOF'
!"""Example test file."""
!
!def test_example():
!    """Example test function."""
!    assert True
!EOF
!  echo -e "${GREEN}   ✅ Test structure created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  Test structure already exists${NC}"
!fi

!# 6. Create README.md (idempotent)
!echo -e "${CYAN}📖 6. Creating README...${NC}"
!if [ ! -f "README.md" ]; then
!cat > README.md << EOF
!# ${project_name}
!
!A modern Python project with comprehensive development infrastructure.
!
!## Features
!
!- 🐍 Python project structure
!- 🧪 Testing framework ready
!- 🔍 Comprehensive linting (Python, Markdown, Shell)
!- 🛡️ Security scanning
!- 🤖 Automated dependency updates with Dependabot
!- 📝 Documentation structure
!- ⚙️ GitHub Actions CI/CD
!- 🔒 Branch protection rules
!
!## Getting Started
!
!### Prerequisites
!
!- Python 3.8+
!- pip or poetry for dependency management
!
!### Installation
!
!\`\`\`bash
!git clone https://github.com/\$(gh api user --jq .login)/${project_name}.git
!cd ${project_name}
!pip install -r requirements.txt  # or: poetry install
!\`\`\`
!
!### Development
!
!\`\`\`bash
!# Install development dependencies
!pip install -r requirements-dev.txt
!
!# Run tests
!python -m pytest tests/
!
!# Run linting
!flake8 src/ tests/
!black src/ tests/
!isort src/ tests/
!\`\`\`
!
!## Project Structure
!
!\`\`\`
!${project_name}/
!├── src/              # Source code
!├── tests/            # Test files
!├── docs/             # Documentation
!├── .github/          # GitHub Actions workflows
!├── README.md         # This file
!├── LICENSE           # MIT License
!└── requirements.txt  # Python dependencies
!\`\`\`
!
!## Contributing
!
!Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
!
!## License
!
!This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
!EOF
!  echo -e "${GREEN}   ✅ README.md created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  README.md already exists${NC}"
!fi

!# 7. Create MIT LICENSE (idempotent)
!echo -e "${CYAN}📄 7. Creating MIT LICENSE...${NC}"
!if [ ! -f "LICENSE" ]; then
!  user_name=$(git config user.name || echo "Your Name")
!  current_year=$(date +%Y)
!cat > LICENSE << EOF
!MIT License
!
!Copyright (c) ${current_year} ${user_name}
!
!Permission is hereby granted, free of charge, to any person obtaining a copy
!of this software and associated documentation files (the "Software"), to deal
!in the Software without restriction, including without limitation the rights
!to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
!copies of the Software, and to permit persons to whom the Software is
!furnished to do so, subject to the following conditions:
!
!The above copyright notice and this permission notice shall be included in all
!copies or substantial portions of the Software.
!
!THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
!IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
!FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
!AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
!LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
!OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
!SOFTWARE.
!EOF
!  echo -e "${GREEN}   ✅ MIT LICENSE created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  LICENSE already exists${NC}"
!fi

!# 8. GitHub Apps recommendations
!echo -e "${CYAN}📱 8. GitHub Apps recommendations...${NC}"
!echo -e "${BLUE}   Recommended GitHub Apps to install:${NC}"
!echo -e "${BLUE}   • Dependabot (automated dependency updates) - Built-in${NC}"
!echo -e "${BLUE}   • CodeQL (security analysis) - Available in Security tab${NC}"
!echo -e "${BLUE}   • Renovate (alternative to Dependabot) - github.com/apps/renovate${NC}"
!echo -e "${GREEN}   ✅ GitHub Apps guidance provided${NC}"

!# 9. Create Dependabot configuration (idempotent)
!echo -e "${CYAN}🤖 9. Setting up Dependabot configuration...${NC}"
!if [ ! -f ".github/dependabot.yml" ]; then
!cat > .github/dependabot.yml << 'EOF'
!version: 2
!updates:
!  # Python dependency updates
!  - package-ecosystem: "pip"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 10
!    reviewers:
!      - "@me"
!    assignees:
!      - "@me"
!    commit-message:
!      prefix: "deps"
!      prefix-development: "deps-dev"
!    labels:
!      - "dependencies"
!      - "python"
!
!  # GitHub Actions updates
!  - package-ecosystem: "github-actions"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 5
!    reviewers:
!      - "@me"
!    assignees:
!      - "@me"
!    commit-message:
!      prefix: "ci"
!    labels:
!      - "dependencies"
!      - "github-actions"
!
!  # Docker updates (if Dockerfile exists)
!  - package-ecosystem: "docker"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"  
!      time: "09:00"
!    open-pull-requests-limit: 5
!    reviewers:
!      - "@me"
!    assignees:
!      - "@me"
!    commit-message:
!      prefix: "docker"
!    labels:
!      - "dependencies"
!      - "docker"
!
!  # NPM updates (if package.json exists)
!  - package-ecosystem: "npm"
!    directory: "/"
!    schedule:
!      interval: "weekly"
!      day: "monday"
!      time: "09:00"
!    open-pull-requests-limit: 10
!    reviewers:
!      - "@me"
!    assignees:
!      - "@me"
!    commit-message:
!      prefix: "deps"
!      prefix-development: "deps-dev"
!    labels:
!      - "dependencies"
!      - "javascript"
!EOF
!  echo -e "${GREEN}   ✅ Dependabot configuration created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  Dependabot configuration already exists${NC}"
!fi

!# Additional infrastructure files (idempotent)
!echo -e "${CYAN}🔧 Additional infrastructure setup...${NC}"

!# .gitignore (idempotent)
!if [ ! -f ".gitignore" ]; then
!cat > .gitignore << 'EOF'
!# Byte-compiled / optimized / DLL files
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
!# OS
!.DS_Store
!.DS_Store?
!._*
!.Spotlight-V100
!.Trashes
!ehthumbs.db
!Thumbs.db
!
!# Project specific
!.env.local
!.env.production
!.env.test
!config/local.json
!
!# Node.js (if applicable)
!node_modules/
!npm-debug.log*
!yarn-debug.log*
!yarn-error.log*
!EOF
!  echo -e "${GREEN}   ✅ .gitignore created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  .gitignore already exists${NC}"
!fi

!# .editorconfig (idempotent)
!if [ ! -f ".editorconfig" ]; then
!cat > .editorconfig << 'EOF'
!root = true
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
![*.{js,json,ts}]
!indent_size = 2
!
![*.md]
!trim_trailing_whitespace = false
!EOF
!  echo -e "${GREEN}   ✅ .editorconfig created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  .editorconfig already exists${NC}"
!fi

!# CONTRIBUTING.md (idempotent)
!if [ ! -f "CONTRIBUTING.md" ]; then
!cat > CONTRIBUTING.md << EOF
!# Contributing to ${project_name}
!
!We love your input! We want to make contributing to this project as easy and transparent as possible.
!
!## Development Process
!
!1. Fork the repo and create your branch from \`main\`
!2. Make your changes
!3. Ensure tests pass
!4. Ensure linting passes
!5. Submit a pull request
!
!## Pull Request Process
!
!1. Update the README.md with details of changes if applicable
!2. Update the version numbers if applicable
!3. The PR will be merged once you have the sign-off of maintainers
!
!## Any contributions you make will be under the MIT Software License
!
!When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.
!
!## Report bugs using GitHub issues
!
!We use GitHub issues to track public bugs. Report a bug by [opening a new issue](../../issues/new).
!
!## License
!
!By contributing, you agree that your contributions will be licensed under its MIT License.
!EOF
!  echo -e "${GREEN}   ✅ CONTRIBUTING.md created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  CONTRIBUTING.md already exists${NC}"
!fi

!# Create basic requirements files (idempotent)
!if [ ! -f "requirements.txt" ]; then
!  touch requirements.txt
!  echo -e "${GREEN}   ✅ requirements.txt created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  requirements.txt already exists${NC}"
!fi

!if [ ! -f "requirements-dev.txt" ]; then
!cat > requirements-dev.txt << 'EOF'
!# Development dependencies
!pytest>=7.0.0
!pytest-cov>=4.0.0
!flake8>=5.0.0
!black>=22.0.0
!isort>=5.10.0
!mypy>=1.0.0
!EOF
!  echo -e "${GREEN}   ✅ requirements-dev.txt created${NC}"
!else
!  echo -e "${YELLOW}   ⚠️  requirements-dev.txt already exists${NC}"
!fi

!echo ""
!echo -e "${GREEN}🎉 Bootstrap complete! Repository infrastructure ready.${NC}"
!echo ""
!echo -e "${CYAN}📊 Summary:${NC}"
!echo -e "${CYAN}===========${NC}"
!echo -e "✅ Git repository initialized"
!echo -e "✅ GitHub repository created (if possible)"
!echo -e "✅ GitHub Actions linting workflows"
!echo -e "✅ Branch protection configured (if possible)"
!echo -e "✅ Project structure (src/, tests/, docs/)"
!echo -e "✅ README.md with project template"
!echo -e "✅ MIT LICENSE with your information"
!echo -e "✅ GitHub Apps recommendations"
!echo -e "✅ Dependabot automated dependency updates"
!echo -e "✅ .gitignore with comprehensive exclusions"
!echo -e "✅ .editorconfig for consistent style"
!echo -e "✅ CONTRIBUTING.md guidelines"
!echo -e "✅ Python requirements files"
!echo ""
!echo -e "${BLUE}🚀 Next Steps:${NC}"
!echo -e "• Add your Python dependencies to requirements.txt"
!echo -e "• Start coding in the src/ directory"
!echo -e "• Write tests in the tests/ directory"
!echo -e "• Configure Dependabot reviewers/assignees in .github/dependabot.yml"
!echo -e "• Enable branch protection and required status checks in GitHub"
!echo -e "• Install recommended GitHub Apps for enhanced security"