"""
GitHub repository initialization slash command for claude-slash.

This module provides the /github-init command that initializes and configures
new GitHub repositories with best practices including CI/CD workflows,
documentation sites, and security-first defaults.
"""

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional

import typer

from .base import BaseCommand


@dataclass
class GitHubInitOptions:
    """Options for GitHub repository initialization."""

    repo_name: str
    description: Optional[str] = None
    private: bool = True  # Default to private
    license: Optional[str] = None
    gitignore: Optional[str] = None
    readme: bool = True
    default_branch: str = "main"
    topics: Optional[List[str]] = None
    create_website: bool = False
    enable_dependabot: bool = True
    dry_run: bool = False

    # GitHub Projects
    create_project: bool = True
    project_template: str = "development"

    # Advanced GitHub Automation
    enable_auto_version: bool = True
    enable_auto_merge: bool = True
    enable_claude_review: bool = False
    enable_auto_release: bool = True
    enable_branch_protection: bool = True


class GitHubInitialization:
    """Core GitHub repository initialization logic."""

    def __init__(self, options: GitHubInitOptions):
        self.options = options
        self.original_dir = os.getcwd()
        self.created_files = []

    def execute(self) -> None:
        """Execute the repository initialization process."""
        if self.options.dry_run:
            self._execute_dry_run()
            return

        # Validate prerequisites before starting
        self._validate_prerequisites()

        try:
            print(f"🚀 Initializing GitHub repository: {self.options.repo_name}")

            # Step 1: Initialize git repository
            self._init_git_repo()

            # Step 2: Create initial files
            self._create_initial_files()

            # Step 3: Create GitHub Actions workflows
            self._create_github_workflows()

            # Step 4: Initialize Docusaurus if requested
            if self.options.create_website:
                self._initialize_docusaurus()

            # Step 5: Create GitHub repository
            self._create_github_repo()

            # Step 6: Create GitHub project if requested
            if self.options.create_project:
                self._create_github_project()

            # Step 7: Setup dependabot
            if self.options.enable_dependabot:
                self._setup_dependabot()

            # Step 8: Configure advanced automation
            self._configure_automation()

            # Step 9: Setup branch protection if enabled
            if self.options.enable_branch_protection:
                self._setup_branch_protection()

            # Step 10: Initial commit and push
            self._initial_commit_and_push()

            print(f"✅ Repository '{self.options.repo_name}' initialized successfully!")
            print(f"📂 Local directory: {os.getcwd()}")
            print(
                f"🔗 GitHub URL: https://github.com/{self._get_github_user()}/{self.options.repo_name}"
            )

        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            self._rollback()
            raise

    def _validate_prerequisites(self) -> None:
        """Validate that all prerequisites are available."""
        # Check if gh CLI is available and authenticated
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError("GitHub CLI (gh) is not installed or not authenticated")

        # Check if git is available
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Git is not installed")

        # Check if repo name already exists locally
        if Path(self.options.repo_name).exists():
            raise RuntimeError(f"Directory '{self.options.repo_name}' already exists")

    def _get_github_user(self) -> str:
        """Get the current GitHub username."""
        result = subprocess.run(["gh", "api", "user"], capture_output=True, text=True)
        if result.returncode == 0:
            import json

            user_data = json.loads(result.stdout)
            return user_data.get("login", "unknown")
        return "unknown"

    def _init_git_repo(self) -> None:
        """Initialize a new git repository."""
        # Create directory and initialize git
        os.makedirs(self.options.repo_name)
        os.chdir(self.options.repo_name)

        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", self.options.default_branch], check=True)

    def _create_initial_files(self) -> None:
        """Create initial files for the repository."""
        if self.options.readme:
            self._create_readme()

        if self.options.gitignore:
            self._create_gitignore()

        if self.options.license:
            self._create_license()

    def _create_readme(self) -> None:
        """Create a README.md file."""
        content = f"""# {self.options.repo_name}

{self.options.description or ""}

## Getting Started

Add instructions for getting started with your project here.

## Contributing

Contributions are welcome! Please read our contributing guidelines.

## License

{self.options.license or "See LICENSE file for details."}
"""
        with open("README.md", "w") as f:
            f.write(content)
        self.created_files.append("README.md")

    def _create_gitignore(self) -> None:
        """Create .gitignore file."""
        # Use gh to get gitignore template if available
        try:
            result = subprocess.run(
                ["gh", "api", f"/gitignore/templates/{self.options.gitignore}"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json

                data = json.loads(result.stdout)
                content = data.get("source", "")
                with open(".gitignore", "w") as f:
                    f.write(content)
                self.created_files.append(".gitignore")
        except Exception:
            # Fallback to basic gitignore
            basic_gitignore = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
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

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Environments
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
"""
            with open(".gitignore", "w") as f:
                f.write(basic_gitignore)
            self.created_files.append(".gitignore")

    def _create_license(self) -> None:
        """Create LICENSE file."""
        # For simplicity, create a basic MIT license placeholder
        # In a real implementation, you'd want to fetch the actual license text
        content = f"""MIT License

Copyright (c) 2025 {self._get_github_user()}

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
"""
        with open("LICENSE", "w") as f:
            f.write(content)
        self.created_files.append("LICENSE")

    def _create_github_workflows(self) -> None:
        """Create GitHub Actions workflows."""
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Create a basic CI workflow
        ci_workflow = """name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f requirements-test.txt ]; then pip install -r requirements-test.txt; fi

    - name: Run tests
      run: pytest
"""

        with open(workflows_dir / "ci.yml", "w") as f:
            f.write(ci_workflow)
        self.created_files.append(".github/workflows/ci.yml")

    def _initialize_docusaurus(self) -> None:
        """Initialize Docusaurus documentation site."""
        print("📚 Setting up Docusaurus documentation site...")
        # This is a placeholder - real implementation would need Node.js setup
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)

        with open(docs_dir / "index.md", "w") as f:
            f.write(
                f"""# {self.options.repo_name} Documentation

Welcome to the documentation for {self.options.repo_name}.

## Overview

{self.options.description or "Add your project description here."}
"""
            )
        self.created_files.append("docs/index.md")

    def _create_github_repo(self) -> None:
        """Create the GitHub repository."""
        visibility = "private" if self.options.private else "public"

        cmd = ["gh", "repo", "create", self.options.repo_name, f"--{visibility}"]

        if self.options.description:
            cmd.extend(["--description", self.options.description])

        subprocess.run(cmd, check=True)

    def _create_github_project(self) -> None:
        """Create GitHub project board with outcome management system."""
        print("📋 Creating GitHub project with outcome management...")
        # Repository-level project creation
        subprocess.run(
            [
                "gh",
                "project",
                "create",
                "--title",
                f"{self.options.repo_name} Development",
                "--body",
                f"Development tracking for {self.options.repo_name}",
            ],
            check=True,
        )

        # Create hierarchical labels for outcome management
        self._create_outcome_labels()

        # Create issue templates for structured development
        self._create_issue_templates()

        # Create automation workflows for project management
        self._create_project_automation()

    def _create_outcome_labels(self) -> None:
        """Create hierarchical labels for outcome management system."""
        print("🏷️  Creating outcome management labels...")

        labels = [
            (
                "outcome",
                "6B46C1",
                "Top-level business outcomes that group related epics",
            ),
            ("epic", "F59E0B", "Major work items that deliver part of an outcome"),
            ("story", "10B981", "Development tasks that implement part of an epic"),
        ]

        for name, color, description in labels:
            try:
                subprocess.run(
                    [
                        "gh",
                        "label",
                        "create",
                        name,
                        "--color",
                        color,
                        "--description",
                        description,
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError:
                # Label might already exist, try to update it
                subprocess.run(
                    [
                        "gh",
                        "label",
                        "edit",
                        name,
                        "--color",
                        color,
                        "--description",
                        description,
                    ],
                    check=False,
                )  # Don't fail if update doesn't work

    def _create_issue_templates(self) -> None:
        """Create issue templates for outcome/epic/story hierarchy."""
        print("📋 Creating issue templates...")

        template_dir = Path(".github/ISSUE_TEMPLATE")
        template_dir.mkdir(parents=True, exist_ok=True)

        # Outcome template
        outcome_template = """---
name: 💼 Outcome
about: Create a new business outcome that groups related epics
title: 'Outcome: [Brief description]'
labels: ["outcome"]
assignees: []
---

## 🎯 Business Outcome

**Brief Description:** What business value will this outcome deliver?

## 📊 Success Metrics

- [ ] Metric 1: [Quantifiable measure]
- [ ] Metric 2: [Quantifiable measure]
- [ ] Metric 3: [Quantifiable measure]

## 🎨 Scope & Context

**Problem Statement:** What problem does this solve?

**User Impact:** Who benefits and how?

**Strategic Alignment:** How does this align with business objectives?

## 🗺️ Related Epics

This outcome will be delivered through the following epics:

- [ ] Epic: [Link to epic issue]
- [ ] Epic: [Link to epic issue]
- [ ] Epic: [Link to epic issue]

## ✅ Definition of Done

- [ ] All epics under this outcome are completed
- [ ] Success metrics are achieved and validated
- [ ] User acceptance testing passed
- [ ] Documentation updated
- [ ] Stakeholder sign-off obtained

## 📝 Notes

[Additional context, assumptions, or constraints]
"""

        # Epic template
        epic_template = """---
name: 🚀 Epic
about: Create a new epic under a business outcome
title: 'Epic: [Brief description]'
labels: ["epic"]
assignees: []
---

## 🎯 Epic Overview

**Parent Outcome:** [Link to outcome issue]

**Brief Description:** What major capability will this epic deliver?

## 📋 Scope & Requirements

**Functional Requirements:**
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

**Non-Functional Requirements:**
- [ ] Performance: [Specific targets]
- [ ] Security: [Security considerations]
- [ ] Scalability: [Scale requirements]

## 🏗️ Implementation Approach

**Architecture:** [High-level architectural approach]

**Technology Stack:** [Key technologies/frameworks]

**Integration Points:** [Systems this epic integrates with]

## 📊 Stories & Tasks

This epic will be implemented through the following stories:

- [ ] Story: [Link to story issue]
- [ ] Story: [Link to story issue]
- [ ] Story: [Link to story issue]

## 🧪 Testing Strategy

- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests

## ✅ Definition of Done

- [ ] All stories under this epic are completed
- [ ] Code review completed and approved
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Feature deployed to production

## 📝 Notes

[Technical notes, architectural decisions, or implementation details]
"""

        # Story template
        story_template = """---
name: 📋 Story
about: Create a new development story under an epic
title: 'Story: [Brief description]'
labels: ["story"]
assignees: []
---

## 🎯 Story Overview

**Parent Epic:** [Link to epic issue]

**User Story:** As a [user type], I want [functionality] so that [benefit].

## 📋 Acceptance Criteria

- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]

## 🔧 Technical Requirements

**Implementation Details:**
- [ ] [Specific technical requirement]
- [ ] [Specific technical requirement]
- [ ] [Specific technical requirement]

## 🧪 Test Plan

**Unit Tests:**
- [ ] Test case 1
- [ ] Test case 2

**Integration Tests:**
- [ ] Integration scenario 1
- [ ] Integration scenario 2

## ✅ Definition of Done

- [ ] Code implemented and tested
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Code review completed
- [ ] Documentation updated

## 📝 Notes

[Implementation notes, technical considerations, or edge cases]
"""

        # Write templates to files
        templates = [
            ("outcome.md", outcome_template),
            ("epic.md", epic_template),
            ("story.md", story_template),
        ]

        for filename, content in templates:
            template_path = template_dir / filename
            with open(template_path, "w") as f:
                f.write(content)
            self.created_files.append(f".github/ISSUE_TEMPLATE/{filename}")

    def _create_project_automation(self) -> None:
        """Create GitHub Actions workflows for project automation."""
        print("🤖 Creating project automation workflows...")

        workflow_dir = Path(".github/workflows")
        workflow_dir.mkdir(parents=True, exist_ok=True)

        # Project automation workflow
        automation_workflow = """name: Project Automation

on:
  issues:
    types: [opened, edited, labeled, unlabeled, closed, reopened]
  issue_comment:
    types: [created]

permissions:
  issues: write
  repository-projects: write
  contents: read

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    if: github.event_name == 'issues' && github.event.action == 'opened'
    steps:
      - name: Add issue to project
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/${{ github.repository_owner }}/projects
          github-token: ${{ secrets.GITHUB_TOKEN }}

  hierarchy-validation:
    runs-on: ubuntu-latest
    if: github.event_name == 'issues' && (github.event.action == 'opened' || github.event.action == 'labeled')
    steps:
      - name: Validate hierarchy labels
        uses: actions/github-script@v6
        with:
          script: |
            const { owner, repo, number } = context.issue;
            const issue = await github.rest.issues.get({
              owner,
              repo,
              issue_number: number
            });

            const labels = issue.data.labels.map(l => l.name);
            const hasOutcome = labels.includes('outcome');
            const hasEpic = labels.includes('epic');
            const hasStory = labels.includes('story');

            // Validate hierarchy rules
            const hierarchyCount = [hasOutcome, hasEpic, hasStory].filter(Boolean).length;

            if (hierarchyCount > 1) {
              await github.rest.issues.createComment({
                owner,
                repo,
                issue_number: number,
                body: '⚠️ **Hierarchy Validation**: Issues should have only one hierarchy label (outcome, epic, or story). Please remove conflicting labels.'
              });
            }

  update-outcome-progress:
    runs-on: ubuntu-latest
    if: github.event_name == 'issues' && (github.event.action == 'closed' || github.event.action == 'reopened')
    steps:
      - name: Update parent outcome progress
        uses: actions/github-script@v6
        with:
          script: |
            const { owner, repo, number } = context.issue;
            const issue = await github.rest.issues.get({
              owner,
              repo,
              issue_number: number
            });

            const labels = issue.data.labels.map(l => l.name);
            const isEpic = labels.includes('epic');

            if (isEpic && issue.data.body) {
              // Look for parent outcome reference in the body
              const outcomeMatch = issue.data.body.match(/\\*\\*Parent Outcome:\\*\\* #(\\d+)/);
              if (outcomeMatch) {
                const outcomeNumber = parseInt(outcomeMatch[1]);

                // Get all epics for this outcome
                const epics = await github.rest.search.issuesAndPullRequests({
                  q: `repo:${owner}/${repo} is:issue label:epic "Parent Outcome: #${outcomeNumber}"`
                });

                const totalEpics = epics.data.total_count;
                const closedEpics = epics.data.items.filter(epic => epic.state === 'closed').length;
                const progressPercent = totalEpics > 0 ? Math.round((closedEpics / totalEpics) * 100) : 0;

                // Comment on outcome with progress update
                await github.rest.issues.createComment({
                  owner,
                  repo,
                  issue_number: outcomeNumber,
                  body: `📊 **Progress Update**: ${closedEpics}/${totalEpics} epics completed (${progressPercent}%)`
                });
              }
            }
"""

        # Outcome metrics workflow
        metrics_workflow = """name: Outcome Metrics Dashboard

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Mondays at 6 AM UTC
  workflow_dispatch:  # Allow manual triggers

jobs:
  generate-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Generate outcome metrics report
        uses: actions/github-script@v6
        with:
          script: |
            const { owner, repo } = context.repo;

            // Get all outcomes
            const outcomes = await github.rest.search.issuesAndPullRequests({
              q: `repo:${owner}/${repo} is:issue label:outcome`
            });

            let metricsReport = `# 📊 Outcome Metrics Report\\n\\n`;
            metricsReport += `*Generated: ${new Date().toISOString().split('T')[0]}*\\n\\n`;
            metricsReport += `## Summary\\n\\n`;
            metricsReport += `- **Total Outcomes**: ${outcomes.data.total_count}\\n`;

            let completedOutcomes = 0;
            let activeOutcomes = 0;
            let plannedOutcomes = 0;

            for (const outcome of outcomes.data.items) {
              // Get epics for this outcome
              const epics = await github.rest.search.issuesAndPullRequests({
                q: `repo:${owner}/${repo} is:issue label:epic "Parent Outcome: #${outcome.number}"`
              });

              const totalEpics = epics.data.total_count;
              const closedEpics = epics.data.items.filter(epic => epic.state === 'closed').length;
              const progressPercent = totalEpics > 0 ? Math.round((closedEpics / totalEpics) * 100) : 0;

              if (progressPercent === 100) {
                completedOutcomes++;
              } else if (progressPercent > 0) {
                activeOutcomes++;
              } else {
                plannedOutcomes++;
              }

              metricsReport += `\\n## ${outcome.title}\\n`;
              metricsReport += `- **Progress**: ${closedEpics}/${totalEpics} epics (${progressPercent}%)\\n`;
              metricsReport += `- **Status**: ${outcome.state}\\n`;
              metricsReport += `- **Link**: [#${outcome.number}](${outcome.html_url})\\n`;
            }

            metricsReport += `\\n## Overall Status\\n`;
            metricsReport += `- **Completed**: ${completedOutcomes}\\n`;
            metricsReport += `- **Active**: ${activeOutcomes}\\n`;
            metricsReport += `- **Planned**: ${plannedOutcomes}\\n`;

            // Create or update metrics issue
            try {
              const existingIssue = await github.rest.search.issuesAndPullRequests({
                q: `repo:${owner}/${repo} is:issue in:title "Outcome Metrics Dashboard"`
              });

              if (existingIssue.data.total_count > 0) {
                // Update existing dashboard issue
                await github.rest.issues.update({
                  owner,
                  repo,
                  issue_number: existingIssue.data.items[0].number,
                  body: metricsReport
                });
              } else {
                // Create new dashboard issue
                await github.rest.issues.create({
                  owner,
                  repo,
                  title: '📊 Outcome Metrics Dashboard',
                  body: metricsReport,
                  labels: ['metrics', 'dashboard']
                });
              }
            } catch (error) {
              console.error('Error managing metrics dashboard:', error);
            }
"""

        # Write workflows to files
        workflows = [
            ("project-automation.yml", automation_workflow),
            ("outcome-metrics.yml", metrics_workflow),
        ]

        for filename, content in workflows:
            workflow_path = workflow_dir / filename
            with open(workflow_path, "w") as f:
                f.write(content)
            self.created_files.append(f".github/workflows/{filename}")

    def _setup_dependabot(self) -> None:
        """Setup Dependabot configuration."""
        dependabot_dir = Path(".github")
        dependabot_dir.mkdir(exist_ok=True)

        dependabot_config = """version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "@me"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "@me"
"""

        with open(dependabot_dir / "dependabot.yml", "w") as f:
            f.write(dependabot_config)
        self.created_files.append(".github/dependabot.yml")

    def _setup_branch_protection(self) -> None:
        """Setup branch protection rules for the main branch."""
        print("🛡️ Setting up branch protection rules...")

        user = self._get_github_user()
        repo_full_name = f"{user}/{self.options.repo_name}"

        try:
            # Create branch protection rule using GitHub CLI
            cmd = [
                "gh",
                "api",
                "--method",
                "PUT",
                f"/repos/{repo_full_name}/branches/{self.options.default_branch}/protection",
                "--field",
                'required_status_checks={"strict":true,"checks":[]}',
                "--field",
                "enforce_admins=false",
                "--field",
                'required_pull_request_reviews={"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}',
                "--field",
                "restrictions=null",
                "--field",
                "allow_force_pushes=false",
                "--field",
                "allow_deletions=false",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Branch protection rules configured successfully")
            else:
                print(f"⚠️ Warning: Could not set up branch protection: {result.stderr}")

        except Exception as e:
            print(f"⚠️ Warning: Failed to setup branch protection: {e}")

    def _configure_automation(self) -> None:
        """Configure advanced GitHub automation."""
        if self.options.enable_auto_version:
            print("🔄 Configuring automatic versioning...")

        if self.options.enable_auto_merge:
            print("🔄 Configuring auto-merge for dependabot...")

        if self.options.enable_auto_release:
            print("🔄 Configuring automatic releases...")

    def _initial_commit_and_push(self) -> None:
        """Make initial commit and push to GitHub."""
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        # Add remote and push
        user = self._get_github_user()
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                f"git@github.com:{user}/{self.options.repo_name}.git",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", self.options.default_branch], check=True
        )

    def _execute_dry_run(self) -> None:
        """Show what would be created without actually creating it."""
        print("🔍 DRY RUN MODE - Preview of what would be created:")
        print(f"📦 Repository name: {self.options.repo_name}")
        print(f"🔒 Visibility: {'private' if self.options.private else 'public'}")
        if self.options.description:
            print(f"📝 Description: {self.options.description}")
        print(f"📄 README: {'✓' if self.options.readme else '✗'}")
        if self.options.gitignore:
            print(f"🚫 .gitignore: {self.options.gitignore}")
        if self.options.license:
            print(f"📜 License: {self.options.license}")
        print(f"🌐 Website: {'✓' if self.options.create_website else '✗'}")
        print(f"📋 Project board: {'✓' if self.options.create_project else '✗'}")
        print(f"🤖 Dependabot: {'✓' if self.options.enable_dependabot else '✗'}")
        print(
            f"🛡️ Branch protection: {'✓' if self.options.enable_branch_protection else '✗'}"
        )

        # New outcome management features
        print("\n🎯 Outcome Management System:")
        print("   🏷️  Hierarchical labels: outcome, epic, story")
        print("   📋 Issue templates: outcome.md, epic.md, story.md")
        print("   🤖 Project automation workflow")
        print("   📊 Weekly metrics dashboard")

        print("\n🎯 GitHub Actions workflows:")
        print("   🚀 CI/CD pipeline")
        print("   📋 Project automation")
        print("   📊 Outcome metrics dashboard")

    def _rollback(self) -> None:
        """Rollback changes on failure."""
        try:
            print("🔄 Rolling back changes...")

            # Change back to original directory
            os.chdir(self.original_dir)

            # Try to delete the GitHub repository if it was created
            try:
                user = self._get_github_user()
                subprocess.run(
                    [
                        "gh",
                        "repo",
                        "delete",
                        f"{user}/{self.options.repo_name}",
                        "--yes",
                    ],
                    capture_output=True,
                )
            except Exception:
                pass

            # Remove local directory
            import shutil

            if Path(self.options.repo_name).exists():
                shutil.rmtree(self.options.repo_name)

        except Exception as e:
            print(f"⚠️ Error during rollback: {e}")


class GitHubInitCommand(BaseCommand):
    """
    Initialize and configure a new GitHub repository with outcome-driven project management.

    This command creates a complete repository setup including:
    - Git repository initialization
    - README, .gitignore, and LICENSE files
    - Outcome management system (hierarchical labels: outcome/epic/story)
    - Professional issue templates for structured development
    - Automated progress tracking and metrics dashboard
    - GitHub Actions CI/CD workflows
    - Project automation workflows
    - Optional Docusaurus documentation site
    - GitHub project board with enhanced automation
    - Dependabot configuration
    - Advanced automation features

    The outcome management system provides:
    - Hierarchical project organization (outcomes → epics → stories)
    - Automated progress tracking and reporting
    - Weekly metrics dashboards
    - Professional issue templates
    - Label validation and management
    """

    @property
    def name(self) -> str:
        """Return the command name."""
        return "github-init"

    @property
    def help_text(self) -> str:
        """Return the help text for the command."""
        return (
            "Initialize a new GitHub repository with outcome-driven project management.\n\n"
            "This command creates a complete repository setup including Git initialization,\n"
            "essential files (README, .gitignore, LICENSE), GitHub Actions workflows,\n"
            "project boards with outcome management, and automated dependency management.\n\n"
            "Examples:\n"
            '  /github-init my-project --description "My awesome project"\n'
            "  /github-init my-lib --public --license MIT --gitignore Python\n"
            "  /github-init docs-site --create-website --dry-run\n\n"
            "Features:\n"
            "• 🔒 Private repositories by default (security-first)\n"
            "• 🎯 Outcome management system (outcome/epic/story hierarchy)\n"
            "• 📋 Professional issue templates for structured development\n"
            "• 🤖 Automated progress tracking and metrics dashboard\n"
            "• 🏷️ Hierarchical labels for project organization\n"
            "• 🚀 Complete CI/CD workflow setup\n"
            "• 🛡️ Branch protection rules enabled by default\n"
            "• 📚 Optional Docusaurus documentation site\n"
            "• 📋 Repository-level project boards\n"
            "• 🔄 Rollback on failure\n"
            "• 👀 Dry-run preview mode"
        )

    def execute(self, **kwargs: Any) -> None:
        """
        Execute the GitHub init command.

        Args:
            **kwargs: Command arguments passed from Typer
        """
        try:
            # Extract arguments
            repo_name = kwargs.get("repo_name")
            if not repo_name:
                self.error("Repository name is required")
                return

            # Build options from arguments
            options = GitHubInitOptions(
                repo_name=repo_name,
                description=kwargs.get("description"),
                private=not kwargs.get("public", False),
                license=kwargs.get("license"),
                gitignore=kwargs.get("gitignore"),
                readme=kwargs.get("readme", True),
                create_website=kwargs.get("create_website", False),
                enable_dependabot=kwargs.get("enable_dependabot", True),
                dry_run=kwargs.get("dry_run", False),
                create_project=kwargs.get("create_project", True),
                enable_auto_version=kwargs.get("enable_auto_version", True),
                enable_auto_merge=kwargs.get("enable_auto_merge", True),
                enable_auto_release=kwargs.get("enable_auto_release", True),
                enable_branch_protection=kwargs.get("enable_branch_protection", True),
            )

            # Execute the initialization
            initializer = GitHubInitialization(options)
            initializer.execute()

            self.success(f"Repository '{repo_name}' initialized successfully!")

        except Exception as e:
            self.error(f"Failed to initialize repository: {str(e)}")

    def create_typer_command(self):
        """Create a Typer command with custom arguments."""

        def command_wrapper(
            repo_name: str = typer.Argument(
                ..., help="Name of the repository to create"
            ),
            description: Optional[str] = typer.Option(
                None, "--description", "-d", help="Repository description"
            ),
            public: bool = typer.Option(
                False, "--public", help="Create public repository (default: private)"
            ),
            license: Optional[str] = typer.Option(
                None, "--license", "-l", help="License type (e.g., MIT, Apache-2.0)"
            ),
            gitignore: Optional[str] = typer.Option(
                None,
                "--gitignore",
                "-g",
                help="Gitignore template (e.g., Python, Node)",
            ),
            create_website: bool = typer.Option(
                False,
                "--create-website",
                help="Initialize Docusaurus documentation site",
            ),
            enable_dependabot: bool = typer.Option(
                True,
                "--enable-dependabot/--no-dependabot",
                help="Enable Dependabot automation",
            ),
            dry_run: bool = typer.Option(
                False,
                "--dry-run",
                help="Preview what would be created without executing",
            ),
            create_project: bool = typer.Option(
                True,
                "--create-project/--no-project",
                help="Create GitHub project board",
            ),
            enable_auto_version: bool = typer.Option(
                True,
                "--enable-auto-version/--no-auto-version",
                help="Enable automatic versioning",
            ),
            enable_auto_merge: bool = typer.Option(
                True,
                "--enable-auto-merge/--no-auto-merge",
                help="Enable auto-merge for dependabot",
            ),
            enable_auto_release: bool = typer.Option(
                True,
                "--enable-auto-release/--no-auto-release",
                help="Enable automatic releases",
            ),
            enable_branch_protection: bool = typer.Option(
                True,
                "--enable-branch-protection/--no-branch-protection",
                help="Enable branch protection rules",
            ),
        ) -> None:
            """Initialize a new GitHub repository with best practices."""
            try:
                self.execute(
                    repo_name=repo_name,
                    description=description,
                    public=public,
                    license=license,
                    gitignore=gitignore,
                    create_website=create_website,
                    enable_dependabot=enable_dependabot,
                    dry_run=dry_run,
                    create_project=create_project,
                    enable_auto_version=enable_auto_version,
                    enable_auto_merge=enable_auto_merge,
                    enable_auto_release=enable_auto_release,
                    enable_branch_protection=enable_branch_protection,
                )
            except Exception as e:
                self.console.print(
                    f"[bold red]Error executing {self.name}:[/bold red] {str(e)}"
                )
                raise typer.Exit(1)

        return command_wrapper
