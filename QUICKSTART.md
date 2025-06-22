# GitHub Setup Claude - Quickstart Guide

Get started with `/github-init` in just 3 minutes! This tool creates professional GitHub repositories with best practices built-in.

## ⚡ Quick Start

### 1. Interactive Mode (Recommended)
Simply run without arguments for a guided setup:

```bash
./github_init_command.py
```

You'll be prompted for:
- Repository name
- Description  
- Public/Private visibility
- License (MIT, Apache-2.0, GPL-3.0)
- Gitignore template (Python, Node.js, general)
- README creation
- Branch name
- Topics
- Documentation website
- Dependabot configuration

### 2. Command Line Mode
For automation or when you know exactly what you want:

```bash
# Basic private repository
./github_init_command.py my-project

# Full-featured public project
./github_init_command.py awesome-app \
  --public \
  --desc="My awesome application" \
  --license=MIT \
  --gitignore=python \
  --topics=api,fastapi,python

# Documentation site
./github_init_command.py project-docs \
  --public \
  --create-website \
  --desc="Project documentation"
```

## 🎯 What You Get

Every repository includes:

### 📁 Repository Structure
- **Local git repository** with proper remote setup
- **Initial commit** with all files
- **Default branch** (main or custom)

### 📄 Essential Files  
- **README.md** with project structure and license info
- **LICENSE** file (if specified)
- **.gitignore** with language-specific rules
- **GitHub Actions workflows** for CI/CD

### 🔧 Automation
- **CI Pipeline** that runs on every PR and push
- **Dependabot** for automatic dependency updates  
- **Code quality** checks (linting, testing, type checking)

### 🌐 Documentation (Optional)
- **Docusaurus website** with modern documentation
- **GitHub Pages deployment** 
- **PR preview deployments** for documentation changes

## 🚀 Common Workflows

### Python Project
```bash
./github_init_command.py python-api \
  --desc="REST API built with FastAPI" \
  --license=MIT \
  --gitignore=python \
  --topics=python,api,fastapi
```

**What you get:**
- Python-optimized .gitignore
- CI with pytest, flake8, mypy
- pip dependency management
- Code coverage reporting

### Node.js Project  
```bash
./github_init_command.py node-app \
  --desc="React application" \
  --license=MIT \
  --gitignore=node \
  --topics=react,typescript,frontend
```

**What you get:**
- Node.js-optimized .gitignore  
- CI with npm ci, build, test
- npm dependency caching
- ESLint and Prettier integration

### Documentation Site
```bash
./github_init_command.py project-docs \
  --public \
  --create-website \
  --desc="Project documentation and guides"
```

**What you get:**
- Complete Docusaurus setup
- GitHub Pages deployment
- PR preview environments
- Professional documentation theme

### Open Source Project
```bash
./github_init_command.py oss-library \
  --public \
  --license=MIT \
  --gitignore=python \
  --topics=library,opensource,python
```

**What you get:**
- MIT license with current year
- Public repository visibility
- Community-ready README template
- Contributor-friendly CI setup

## 📋 All Available Options

| Flag | Description | Default |
|------|-------------|---------|
| `--interactive, -i` | Use interactive guided setup | Auto when no repo name |
| `--public` | Create public repository | Private |
| `--desc="text"` | Repository description | None |
| `--license=TYPE` | Add license (MIT, Apache-2.0, GPL-3.0) | None |
| `--gitignore=LANG` | Language template (python, node, general) | None |
| `--no-readme` | Skip README creation | Create README |
| `--branch=NAME` | Default branch name | main |
| `--topics=list` | Comma-separated topics | None |
| `--create-website` | Initialize Docusaurus docs | Disabled |
| `--no-dependabot` | Disable dependency updates | Enabled |

## 🔧 Prerequisites

Make sure you have these installed:

```bash
# GitHub CLI (required)
brew install gh
# or: https://cli.github.com/

# Authenticate with GitHub
gh auth login

# Git (usually pre-installed)
git --version

# Python 3.6+ (required)
python3 --version

# Node.js 18+ (only for --create-website)
node --version
```

## 🎨 Customization Examples

### Corporate Project
```bash
./github_init_command.py enterprise-app \
  --desc="Internal business application" \
  --license=Apache-2.0 \
  --gitignore=python \
  --topics=enterprise,internal,business \
  --branch=develop
```

### Research Project
```bash
./github_init_command.py research-analysis \
  --public \
  --desc="Data analysis for XYZ research" \
  --license=MIT \
  --gitignore=python \
  --topics=research,data-science,analysis \
  --create-website
```

### Quick Prototype
```bash
./github_init_command.py quick-proto \
  --desc="Rapid prototype for feature X" \
  --gitignore=general \
  --no-dependabot
```

## 🐛 Troubleshooting

### Authentication Issues
```bash
# Check GitHub CLI auth
gh auth status

# Re-authenticate if needed
gh auth login
```

### Permission Issues
```bash
# Check if you can create repos
gh repo create test-permissions --private

# Delete test repo
gh repo delete test-permissions --yes
```

### Node.js Issues (for websites)
```bash
# Check Node.js version (need 18+)
node --version

# Update if needed
nvm install --lts
nvm use --lts
```

## 📚 Next Steps

After creating your repository:

1. **Clone locally** (if created on GitHub):
   ```bash
   gh repo clone your-username/your-repo
   cd your-repo
   ```

2. **Start developing**:
   - Add your code to the repository
   - Push changes to trigger CI
   - Create pull requests for review

3. **Configure settings**:
   - Set up branch protection rules
   - Add collaborators  
   - Configure GitHub Pages (for websites)

4. **Monitor automation**:
   - Check CI runs in Actions tab
   - Review Dependabot PRs
   - Update documentation

## 💡 Pro Tips

- **Use interactive mode** when learning or for complex setups
- **Save common configurations** by creating shell aliases:
  ```bash
  alias gh-python='./github_init_command.py --license=MIT --gitignore=python'
  alias gh-docs='./github_init_command.py --public --create-website'
  ```
- **Review generated CI workflows** to understand what's running
- **Customize Dependabot** schedules in `.github/dependabot.yml`
- **Check Actions tab** after first push to see CI results

Happy coding! 🚀