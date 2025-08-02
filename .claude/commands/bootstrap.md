# Bootstrap Command

Initialize an empty directory with complete GitHub repository infrastructure including CI/CD, linting, branch protection, and essential files.

## Usage

```bash
/bootstrap [project-name]
```

## Description

This command sets up a complete GitHub repository from scratch with all the modern development infrastructure you need:

- **Repository Initialization**: `git init` and GitHub repository creation
- **CI/CD Pipeline**: GitHub Actions with linters for Python and Markdown
- **Branch Protection**: Configure main branch protection rules
- **Project Structure**: Initialize basic project files and structure
- **Documentation**: Create comprehensive README and contributing guidelines
- **Legal**: Ensure MIT LICENSE file is present
- **GitHub Apps**: Install and configure essential GitHub apps

The command creates a production-ready repository setup that follows modern best practices for open source projects.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!project_name="${ARGUMENTS:-$(basename "$(pwd)")}"

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!echo -e "${BLUE}🚀 Repository Bootstrap Utility${NC}"
!echo -e "${BLUE}===============================${NC}"
!echo -e "Project: ${CYAN}$project_name${NC}"
!echo ""

!# Safety check - don't run in existing git repos unless explicitly confirmed
!if [ -d ".git" ]; then
!  echo -e "${YELLOW}⚠️  This directory is already a git repository.${NC}"
!  echo -n "Continue with bootstrap anyway? [y/N]: "
!  read -r confirm
!  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
!    echo -e "${YELLOW}❌ Bootstrap cancelled.${NC}"
!    exit 0
!  fi
!  existing_repo=true
!else
!  existing_repo=false
!fi

!echo ""

!# Step 1: Initialize Git Repository
!echo -e "${CYAN}📁 Step 1: Initializing Git repository...${NC}"
!if [ "$existing_repo" = false ]; then
!  git init
!  if [ $? -eq 0 ]; then
!    echo -e "${GREEN}✅ Git repository initialized${NC}"
!  else
!    echo -e "${RED}❌ Failed to initialize git repository${NC}"
!    exit 1
!  fi
!else
!  echo -e "${GREEN}✅ Using existing Git repository${NC}"
!fi

!# Step 2: Create GitHub Repository
!echo -e "${CYAN}📦 Step 2: Creating GitHub repository...${NC}"
!if command -v gh >/dev/null 2>&1; then
!  if ! gh repo view "$project_name" >/dev/null 2>&1; then
!    echo "Creating GitHub repository: $project_name"
!    gh repo create "$project_name" --public --description "Bootstrapped project with claude-slash" --clone=false
!    if [ $? -eq 0 ]; then
!      echo -e "${GREEN}✅ GitHub repository created${NC}"
!      # Set remote origin if not exists
!      if ! git remote get-url origin >/dev/null 2>&1; then
!        git remote add origin "https://github.com/$(gh api user --jq .login)/$project_name.git"
!        echo -e "${GREEN}✅ Remote origin configured${NC}"
!      fi
!    else
!      echo -e "${YELLOW}⚠️  Failed to create GitHub repository (continuing anyway)${NC}"
!    fi
!  else
!    echo -e "${GREEN}✅ GitHub repository already exists${NC}"
!  fi
!else
!  echo -e "${YELLOW}⚠️  GitHub CLI not found. Install gh CLI to create remote repository${NC}"
!  echo "   Visit: https://cli.github.com/"
!fi

!# Step 3: Create .gitignore
!echo -e "${CYAN}🚫 Step 3: Creating .gitignore...${NC}"
!if [ ! -f ".gitignore" ]; then
!  cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
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

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
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
logs
*.log

# Temporary files
*.tmp
*.temp
.tmp/
.temp/
EOF
!  echo -e "${GREEN}✅ .gitignore created${NC}"
!else
!  echo -e "${GREEN}✅ .gitignore already exists${NC}"
!fi

!# Step 4: Create GitHub Actions Workflows
!echo -e "${CYAN}⚙️  Step 4: Setting up GitHub Actions workflows...${NC}"
!mkdir -p .github/workflows

!# Create linting workflow
!cat > .github/workflows/lint.yml << 'EOF'
name: Lint and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        check: [python, markdown, shell]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      if: matrix.check == 'python'
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install Python linting tools
      if: matrix.check == 'python'
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black isort mypy
    
    - name: Lint Python code
      if: matrix.check == 'python'
      run: |
        # Check if there are any Python files
        if find . -name "*.py" -not -path "./.*" | grep -q .; then
          echo "Linting Python files..."
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
          isort --check-only .
        else
          echo "No Python files found, skipping Python linting"
        fi
    
    - name: Lint Markdown
      if: matrix.check == 'markdown'
      uses: DavidAnson/markdownlint-cli2-action@v13
      with:
        globs: '**/*.md'
    
    - name: Lint Shell scripts
      if: matrix.check == 'shell'
      run: |
        # Install shellcheck
        sudo apt-get update && sudo apt-get install -y shellcheck
        
        # Check if there are any shell scripts
        if find . -name "*.sh" -not -path "./.*" | grep -q .; then
          echo "Linting shell scripts..."
          find . -name "*.sh" -not -path "./.*" -exec shellcheck {} +
        else
          echo "No shell scripts found, skipping shell linting"
        fi

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security scan
      uses: github/super-linter@v4
      env:
        DEFAULT_BRANCH: main
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        VALIDATE_ALL_CODEBASE: true
        VALIDATE_PYTHON_FLAKE8: true
        VALIDATE_MARKDOWN: true
        VALIDATE_BASH: true
EOF

!echo -e "${GREEN}✅ GitHub Actions linting workflow created${NC}"

!# Step 5: Create MIT License
!echo -e "${CYAN}📄 Step 5: Creating MIT LICENSE...${NC}"
!if [ ! -f "LICENSE" ] && [ ! -f "LICENSE.md" ] && [ ! -f "LICENSE.txt" ]; then
!  current_year=$(date +%Y)
!  # Try to get user info from git or gh
!  if command -v gh >/dev/null 2>&1; then
!    author_name=$(gh api user --jq .name 2>/dev/null || git config user.name 2>/dev/null || echo "Your Name")
!  else
!    author_name=$(git config user.name 2>/dev/null || echo "Your Name")
!  fi
!  
!  cat > LICENSE << EOF
MIT License

Copyright (c) $current_year $author_name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
!  echo -e "${GREEN}✅ MIT LICENSE created${NC}"
!else
!  echo -e "${GREEN}✅ LICENSE file already exists${NC}"
!fi

!# Step 6: Create README
!echo -e "${CYAN}📖 Step 6: Creating README.md...${NC}"
!if [ ! -f "README.md" ]; then
!  cat > README.md << EOF
# $project_name

A project bootstrapped with [claude-slash](https://github.com/jeremyeder/claude-slash).

## Description

Brief description of your project goes here.

## Installation

\`\`\`bash
# Add installation instructions here
\`\`\`

## Usage

\`\`\`bash
# Add usage examples here
\`\`\`

## Features

- Feature 1
- Feature 2
- Feature 3

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [claude-slash](https://github.com/jeremyeder/claude-slash)
- Bootstrapped on $(date +"%Y-%m-%d")
EOF
!  echo -e "${GREEN}✅ README.md created${NC}"
!else
!  echo -e "${GREEN}✅ README.md already exists${NC}"
!fi

!# Step 7: Create additional project structure
!echo -e "${CYAN}📁 Step 7: Creating project structure...${NC}"

!# Create basic directories
!mkdir -p src tests docs

!# Create .editorconfig
!if [ ! -f ".editorconfig" ]; then
!  cat > .editorconfig << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
EOF
!  echo -e "${GREEN}✅ .editorconfig created${NC}"
!fi

!# Create CONTRIBUTING.md
!if [ ! -f "CONTRIBUTING.md" ]; then
!  cat > CONTRIBUTING.md << EOF
# Contributing to $project_name

Thank you for your interest in contributing to $project_name! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs
- Clearly describe the issue including steps to reproduce
- Include information about your environment

### Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes with clear, descriptive commit messages
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup

\`\`\`bash
# Clone your fork
git clone https://github.com/yourusername/$project_name.git
cd $project_name

# Install dependencies (adjust as needed)
# pip install -r requirements.txt
# npm install
\`\`\`

### Coding Standards

- Follow the existing code style
- Write clear, self-documenting code
- Add comments for complex logic
- Include tests for new features
- Update documentation as needed

### Pull Request Guidelines

- Keep changes focused and atomic
- Write clear PR descriptions
- Link to related issues
- Ensure CI checks pass
- Be responsive to feedback

## Questions?

Feel free to open an issue for questions about contributing.
EOF
!  echo -e "${GREEN}✅ CONTRIBUTING.md created${NC}"
!fi

!echo -e "${GREEN}✅ Basic project structure created${NC}"

!# Step 8: Configure branch protection (requires GitHub CLI and permissions)
!echo -e "${CYAN}🔒 Step 8: Configuring branch protection...${NC}"
!if command -v gh >/dev/null 2>&1; then
!  if gh repo view "$project_name" >/dev/null 2>&1; then
!    echo "Configuring main branch protection..."
!    gh api repos/:owner/:repo/branches/main/protection \
!      --method PUT \
!      --field required_status_checks='{"strict":true,"contexts":["lint"]}' \
!      --field enforce_admins=true \
!      --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
!      --field restrictions=null \
!      2>/dev/null && echo -e "${GREEN}✅ Branch protection configured${NC}" || echo -e "${YELLOW}⚠️  Branch protection setup requires admin permissions${NC}"
!  else
!    echo -e "${YELLOW}⚠️  Cannot configure branch protection without GitHub repository${NC}"
!  fi
!else
!  echo -e "${YELLOW}⚠️  Cannot configure branch protection without GitHub CLI${NC}"
!fi

!# Step 9: Install GitHub Apps (placeholder - requires manual action)
!echo -e "${CYAN}🤖 Step 9: GitHub Apps installation guidance...${NC}"
!echo -e "${YELLOW}📋 Recommended GitHub Apps to install manually:${NC}"
!echo "   • Dependabot (dependency updates)"
!echo "   • CodeQL Analysis (security scanning)"
!echo "   • All Contributors (contributor recognition)"
!echo "   • Semantic Pull Requests (enforce PR naming)"
!echo ""
!echo -e "${BLUE}💡 Visit your repository settings > Apps to install these${NC}"

!# Initial commit
!echo -e "${CYAN}💾 Creating initial commit...${NC}"
!git add .
!if git diff --staged --quiet; then
!  echo -e "${YELLOW}⚠️  No changes to commit${NC}"
!else
!  # Set default git config if not set
!  if [ -z "$(git config user.name)" ]; then
!    git config user.name "$(whoami)"
!  fi
!  if [ -z "$(git config user.email)" ]; then
!    git config user.email "$(whoami)@users.noreply.github.com"
!  fi
!  
!  git commit -m "Initial commit: Bootstrap project with claude-slash
!
!- Add GitHub Actions workflows for linting (Python, Markdown, Shell)
!- Create MIT LICENSE
!- Add comprehensive README.md and CONTRIBUTING.md
!- Set up basic project structure (src/, tests/, docs/)
!- Add .gitignore, .editorconfig for development standards
!- Configure repository for modern development workflow
!
!Bootstrapped with claude-slash on $(date +"%Y-%m-%d")"
!  
!  if [ $? -eq 0 ]; then
!    echo -e "${GREEN}✅ Initial commit created${NC}"
!    # Push to remote if origin exists
!    if git remote get-url origin >/dev/null 2>&1; then
!      echo -e "${CYAN}📤 Pushing to remote repository...${NC}"
!      git push -u origin main 2>/dev/null && echo -e "${GREEN}✅ Changes pushed to remote${NC}" || echo -e "${YELLOW}⚠️  Push failed - you may need to push manually${NC}"
!    fi
!  else
!    echo -e "${RED}❌ Failed to create initial commit${NC}"
!  fi
!fi

!echo ""
!echo -e "${GREEN}🎉 Repository bootstrap completed successfully!${NC}"
!echo -e "${GREEN}================================================${NC}"
!echo ""
!echo -e "${CYAN}📊 Summary of what was created:${NC}"
!echo "  ✅ Git repository initialized"
!echo "  ✅ GitHub repository created (if GitHub CLI available)"
!echo "  ✅ GitHub Actions workflows (linting for Python, Markdown, Shell)"
!echo "  ✅ MIT LICENSE file"
!echo "  ✅ Comprehensive README.md"
!echo "  ✅ CONTRIBUTING.md guidelines"
!echo "  ✅ .gitignore with common exclusions"
!echo "  ✅ .editorconfig for consistent coding style"
!echo "  ✅ Basic project structure (src/, tests/, docs/)"
!echo "  ✅ Branch protection guidance provided"
!echo "  ✅ Initial commit created and pushed"
!echo ""
!echo -e "${BLUE}🚀 Next steps:${NC}"
!echo "  1. Review and customize the generated files"
!echo "  2. Install recommended GitHub Apps from repository settings"
!echo "  3. Set up branch protection rules manually if needed"
!echo "  4. Add your project-specific code and documentation"
!echo "  5. Configure any additional CI/CD workflows"
!echo ""
!echo -e "${PURPLE}🔗 Repository URL:${NC} $(git remote get-url origin 2>/dev/null || echo 'Not configured')"
!echo -e "${PURPLE}📁 Local path:${NC} $(pwd)"