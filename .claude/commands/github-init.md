# GitHub Repository Initialization - Complete Setup with Outcome Management

Initialize and configure a new GitHub repository with outcome-driven project management system.

## Usage
```
/github-init my-project --description "My awesome project"
/github-init my-lib --public --license MIT --gitignore Python
/github-init docs-site --create-website --dry-run
```

## Description

This command creates a complete repository setup with best practices including:

### Core Features
- **🔒 Security-First**: Private repositories by default
- **🎯 Outcome Management**: Hierarchical project organization (outcomes → epics → stories)
- **📋 Professional Templates**: Structured issue templates for development
- **🤖 Automated Tracking**: Progress tracking and metrics dashboard
- **🚀 CI/CD Ready**: Complete GitHub Actions workflow setup
- **🛡️ Branch Protection**: Automatic branch protection rules

### Outcome Management System
The repository includes a sophisticated three-tier project management system:

- **Outcomes** (💼): Top-level business objectives with success metrics
- **Epics** (🚀): Major work items that deliver parts of outcomes
- **Stories** (📋): Development tasks that implement parts of epics

### Advanced Automation
- **🏷️ Hierarchical Labels**: Automatic label creation and validation
- **📊 Metrics Dashboard**: Weekly automated progress reporting
- **🔄 Project Automation**: GitHub Actions workflows for project management
- **🤖 Claude Integration**: Optional Claude GitHub App installation
- **📚 Documentation**: Optional Docusaurus documentation site

### Arguments
- `repo_name` (required): Name of the repository to create
- `--description, -d`: Repository description
- `--public`: Create public repository (default: private)
- `--license, -l`: License type (e.g., MIT, Apache-2.0)
- `--gitignore, -g`: Gitignore template (e.g., Python, Node)
- `--create-website`: Initialize Docusaurus documentation site
- `--enable-dependabot/--no-dependabot`: Enable Dependabot automation (default: enabled)
- `--dry-run`: Preview what would be created without executing
- `--create-project/--no-project`: Create GitHub project board (default: enabled)
- `--enable-branch-protection/--no-branch-protection`: Enable branch protection (default: enabled)
- `--install-claude-app/--no-claude-app`: Install Claude GitHub App (default: enabled)

## Examples

### Basic Private Repository
```bash
/github-init my-app --description "My application"
```

### Public Python Library
```bash
/github-init python-lib --public --license MIT --gitignore Python
```

### Documentation Site
```bash
/github-init docs --create-website --public
```

### Preview Mode
```bash
/github-init test-repo --dry-run --description "Test repository"
```

## What Gets Created

### Repository Structure
```
my-project/
├── README.md              # Generated with project info
├── LICENSE                # MIT license (if specified)
├── .gitignore             # Language-specific ignores
├── .github/
│   ├── workflows/
│   │   ├── ci.yml         # CI/CD pipeline
│   │   ├── project-automation.yml  # Project management
│   │   └── outcome-metrics.yml     # Weekly metrics
│   ├── ISSUE_TEMPLATE/
│   │   ├── outcome.md     # Business outcome template
│   │   ├── epic.md        # Epic template
│   │   └── story.md       # Story template
│   └── dependabot.yml     # Dependency automation
└── docs/                  # Documentation (if enabled)
    └── index.md
```

### GitHub Configuration
- Repository created on GitHub
- Repository-level project board with automation
- Branch protection rules configured
- Hierarchical labels (outcome/epic/story)
- Claude GitHub App installed (if enabled)

## Prerequisites
- GitHub CLI (`gh`) installed and authenticated
- Git installed and configured
- Internet connection for GitHub API access

## Rollback Protection
If initialization fails:
- Automatic rollback of all changes
- GitHub repository deletion (if created)
- Local directory cleanup
- Error reporting with recovery instructions

## Tips
- Use `--dry-run` first to preview what will be created
- Default to private repositories for security
- Enable branch protection for collaborative projects
- Use descriptive commit messages in the generated templates
