# GitHub Setup Claude - Complete Documentation

Comprehensive guide to using the GitHub repository initialization tool for Claude.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Configuration](#configuration)
- [CI/CD Workflows](#cicd-workflows)
- [Documentation Websites](#documentation-websites)
- [Dependabot Integration](#dependabot-integration)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Overview

The GitHub Setup Claude tool (`/github-init`) automates the creation of professional GitHub repositories with industry best practices built-in. It handles everything from initial git setup to CI/CD pipeline configuration.

### Key Benefits

- **Zero Configuration**: Works out-of-the-box with sensible defaults
- **Security First**: Private repositories by default
- **Best Practices**: Industry-standard CI/CD, dependency management, and documentation
- **Language Awareness**: Adapts workflows and configurations to your project type
- **Interactive & Automated**: Guided setup or scriptable CLI
- **Documentation Ready**: Optional Docusaurus integration with deployment

## Installation

### Prerequisites

1. **GitHub CLI** (required):
   ```bash
   # macOS
   brew install gh
   
   # Windows
   winget install --id GitHub.cli
   
   # Linux
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update && sudo apt install gh
   ```

2. **Authenticate GitHub CLI**:
   ```bash
   gh auth login
   ```

3. **Python 3.6+** (required):
   ```bash
   python3 --version
   ```

4. **Node.js 18+** (optional, for documentation websites):
   ```bash
   node --version
   npm --version
   ```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/github-setup-claude.git
   cd github-setup-claude
   ```

2. Make executable:
   ```bash
   chmod +x github_init_command.py
   ```

3. Test installation:
   ```bash
   ./github_init_command.py --help
   ```

## Basic Usage

### Interactive Mode

Launch guided setup (recommended for new users):

```bash
./github_init_command.py
```

**Interactive prompts include:**
- Repository name (required)
- Description (optional) 
- Visibility (private/public)
- License selection
- Gitignore template
- README creation
- Default branch name
- Repository topics
- Documentation website
- Dependabot configuration

### Command Line Mode

Direct execution with flags (ideal for automation):

```bash
./github_init_command.py REPO_NAME [OPTIONS]
```

**Basic examples:**
```bash
# Minimal private repository
./github_init_command.py my-project

# Public repository with license
./github_init_command.py my-oss-project --public --license=MIT

# Python project with full setup
./github_init_command.py python-api \
  --desc="REST API built with FastAPI" \
  --license=MIT \
  --gitignore=python \
  --topics=api,python,fastapi
```

## Advanced Features

### Repository Visibility

**Default: Private** (security-first approach)

```bash
# Private repository (default)
./github_init_command.py private-project

# Public repository
./github_init_command.py public-project --public
```

### License Integration

Supported licenses with automatic file generation:

```bash
# MIT License
./github_init_command.py project --license=MIT

# Apache 2.0 License  
./github_init_command.py project --license=Apache-2.0

# GPL 3.0 License
./github_init_command.py project --license=GPL-3.0
```

**License features:**
- Automatic current year insertion
- Standard license text
- README license badge and section
- Compliance with OSI standards

### Gitignore Templates

Language-specific ignore patterns:

```bash
# Python projects
./github_init_command.py python-app --gitignore=python

# Node.js projects  
./github_init_command.py node-app --gitignore=node

# General projects
./github_init_command.py generic-app --gitignore=general
```

**Python template includes:**
- `__pycache__/`, `*.pyc`, `*.pyo`
- Virtual environments (`venv/`, `.env`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

**Node.js template includes:**
- `node_modules/`, `npm-debug.log*`
- Environment files (`.env*`)
- Build outputs (`dist/`, `build/`)
- IDE and OS files

### Repository Topics

Improve discoverability with relevant topics:

```bash
./github_init_command.py awesome-lib \
  --topics=python,library,api,opensource,fastapi
```

**Topic benefits:**
- Enhanced GitHub search visibility
- Community discovery
- Ecosystem categorization
- Trend participation

### Branch Configuration

Customize the default branch name:

```bash
# Use 'main' (default)
./github_init_command.py project

# Use 'develop' 
./github_init_command.py project --branch=develop

# Use custom name
./github_init_command.py project --branch=production
```

## Configuration

### Command Line Options

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `--interactive, -i` | Force interactive mode | Auto-detect | `--interactive` |
| `--public` | Create public repository | Private | `--public` |
| `--desc="text"` | Repository description | None | `--desc="My project"` |
| `--license=TYPE` | Add license file | None | `--license=MIT` |
| `--gitignore=LANG` | Language template | None | `--gitignore=python` |
| `--no-readme` | Skip README creation | Create README | `--no-readme` |
| `--branch=NAME` | Default branch name | main | `--branch=develop` |
| `--topics=list` | Comma-separated topics | None | `--topics=api,python` |
| `--create-website` | Initialize Docusaurus | Disabled | `--create-website` |
| `--no-dependabot` | Disable dependency updates | Enabled | `--no-dependabot` |

### Exit Codes

- `0`: Success
- `1`: General error (missing dependencies, invalid arguments)
- `2`: GitHub authentication failure
- `3`: Repository creation failure
- `4`: File system error

## CI/CD Workflows

Every repository includes GitHub Actions workflows optimized for the project type.

### Python Projects

**Workflow: `.github/workflows/ci.yml`**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest mypy
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Lint with flake8
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Type check with mypy
      run: mypy . --ignore-missing-imports
    
    - name: Test with pytest
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

**Features:**
- Multi-version Python testing (3.8-3.11)
- Dependency caching for faster builds
- Code linting with flake8
- Type checking with mypy
- Test coverage with pytest and codecov
- Automatic dependency installation

### Node.js Projects

**Workflow: `.github/workflows/ci.yml`**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Build
      run: npm run build
    
    - name: Test
      run: npm test
```

**Features:**
- Multi-version Node.js testing (16, 18, 20)
- npm dependency caching
- Standard npm script execution
- Build verification
- Test execution

### Generic Projects

**Workflow: `.github/workflows/ci.yml`**

```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup
      run: echo "Setting up project..."
    
    - name: Build
      run: echo "Building project..."
    
    - name: Test  
      run: echo "Running tests..."
```

**Features:**
- Basic workflow structure
- Ready for customization
- Standard trigger events
- Placeholder for project-specific steps

## Documentation Websites

Create professional documentation with Docusaurus integration.

### Enabling Documentation

```bash
./github_init_command.py project-docs \
  --public \
  --create-website \
  --desc="Project documentation"
```

### What's Included

**Docusaurus Setup:**
- Modern React-based documentation
- Responsive design with dark mode
- Search functionality
- Blog capabilities
- Versioning support

**Deployment Pipeline:**
- Automatic GitHub Pages deployment
- PR preview environments
- Custom domain support (configurable)

**File Structure:**
```
docs/
├── intro.md                 # Getting started page
├── tutorial-basics/         # Tutorial section
└── tutorial-extras/        # Advanced tutorials

docusaurus.config.js        # Site configuration
sidebars.js                  # Navigation structure
package.json                 # Dependencies
```

### Deployment Workflow

**Deploy: `.github/workflows/deploy-docusaurus.yml`**

```yaml
name: Deploy Docusaurus to GitHub Pages

on:
  push:
    branches: [main]
    paths: ['docs/**', 'docusaurus.config.js', 'sidebars.js']

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: npm
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build website
      run: npm run build
    
    - name: Setup Pages
      uses: actions/configure-pages@v4
    
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: build
  
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
```

### PR Preview Workflow

**Preview: `.github/workflows/pr-preview.yml`**

Automatically deploys documentation previews for pull requests, allowing reviewers to see changes before merging.

**Features:**
- Automatic preview deployment
- Comment on PR with preview link
- Cleanup after PR closure
- No interference with main site

## Dependabot Integration

Automatic dependency management with Dependabot is enabled by default.

### Configuration

**File: `.github/dependabot.yml`**

```yaml
version: 2
updates:
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  # Python dependencies (if Python project)
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  # npm dependencies (if Node.js project)  
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

### Ecosystem Detection

Dependabot configuration is automatically customized based on:

- **Gitignore template**: Determines primary language
- **Website option**: Adds npm ecosystem
- **File detection**: Scans for `package.json`, `requirements.txt`, etc.

### Benefits

- **Security updates**: Automatic vulnerability patches
- **Version management**: Keep dependencies current
- **Compatibility testing**: CI runs on dependency updates
- **Reduced maintenance**: Less manual dependency tracking

### Disabling Dependabot

```bash
# Disable during creation
./github_init_command.py project --no-dependabot

# Or interactively choose "no" when prompted
```

## Troubleshooting

### Common Issues

#### Authentication Problems

**Issue**: `gh: command not found`
**Solution**: Install GitHub CLI
```bash
# macOS
brew install gh

# Other platforms: https://cli.github.com/
```

**Issue**: `authentication required`
**Solution**: Authenticate with GitHub
```bash
gh auth login
```

**Issue**: `insufficient permissions`
**Solution**: Check token permissions
```bash
gh auth status
gh auth refresh
```

#### Repository Creation Failures

**Issue**: `repository already exists`
**Solution**: Choose a different name or delete existing repository
```bash
gh repo delete username/repo-name
```

**Issue**: `invalid repository name`
**Solution**: Use valid characters (alphanumeric, hyphens, underscores)

**Issue**: `organization repository creation failed`
**Solution**: Ensure you have repository creation permissions in the organization

#### Workflow Failures

**Issue**: Docusaurus build fails
**Solution**: Ensure Node.js 18+ is available
```bash
# Check Node.js version in workflow
cat .github/workflows/deploy-docusaurus.yml
```

**Issue**: Python CI fails
**Solution**: Check Python version compatibility
```bash
# Update Python versions in workflow
vim .github/workflows/ci.yml
```

#### File System Issues

**Issue**: `permission denied`
**Solution**: Check directory permissions
```bash
ls -la
chmod +x github_init_command.py
```

**Issue**: `directory not empty`
**Solution**: Ensure target directory is clean
```bash
rm -rf target-directory
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Add debug output (modify script temporarily)
python3 -u github_init_command.py project --debug
```

### Getting Help

1. **Check prerequisites**: Ensure all dependencies are installed
2. **Verify authentication**: Test GitHub CLI access
3. **Review error messages**: Look for specific error details
4. **Test with minimal options**: Try basic repository creation first
5. **Check GitHub status**: Visit [githubstatus.com](https://githubstatus.com)

### Reporting Issues

When reporting issues, include:

- **Command used**: Full command with all flags
- **Error message**: Complete error output
- **Environment**: OS, Python version, Node.js version
- **GitHub CLI version**: `gh --version`
- **Expected behavior**: What should have happened
- **Actual behavior**: What actually happened

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run the test suite
5. Submit a pull request

### Running Tests

```bash
# Fast unit tests
python -m pytest test_fast.py -v

# Interactive mode tests
python -m pytest test_interactive.py -v

# All tests
python -m pytest --tb=short

# With coverage
python -m pytest --cov=github_init_command --cov-report=html
```

### Code Quality

```bash
# Format code
black github_init_command.py test_*.py

# Sort imports
isort github_init_command.py test_*.py

# Type checking
mypy github_init_command.py --ignore-missing-imports

# Linting
flake8 github_init_command.py test_*.py
```

### Project Structure

```
github-setup-claude/
├── github_init_command.py      # Main implementation
├── register_command.py         # Claude command registration
├── test_fast.py               # Fast unit tests
├── test_interactive.py        # Interactive mode tests
├── test_integration_fast.py   # Integration tests
├── test_github_init_command.py # Comprehensive tests
├── README.md                  # Project overview
├── QUICKSTART.md              # Quick start guide
├── DOCUMENTATION.md           # This file
├── example-usage.md           # Usage examples
├── Makefile                   # Development commands
├── pytest.ini                # Test configuration
├── requirements-test.txt      # Test dependencies
└── .github/
    └── workflows/
        └── test.yml           # CI pipeline
```

### Architecture

The tool follows a modular architecture:

- **`GitHubInitOptions`**: Configuration data class
- **`GitHubInitCommand`**: Main execution logic
- **Interactive mode**: User-guided setup
- **CLI parsing**: Argument processing
- **Template system**: Workflow and file generation
- **GitHub integration**: Repository creation and configuration

### Extending Functionality

**Adding new gitignore templates:**
1. Add template to `_get_gitignore_template()` method
2. Update CLI choices in argument parser
3. Add tests for new template

**Adding new CI workflows:**
1. Create new `_get_language_ci_workflow()` method
2. Update workflow selection logic
3. Add corresponding tests

**Adding new license types:**
1. Extend `_create_license()` method
2. Update CLI choices
3. Add license text and tests

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support, please:
1. Check this documentation
2. Review the troubleshooting section  
3. Search existing issues
4. Create a new issue with detailed information

Happy coding! 🚀