#!/usr/bin/env python3
"""GitHub repository initialization slash command."""

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None


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
    enable_dependabot: bool = True  # Default to enabled
    dry_run: bool = False  # Preview mode without execution


class GitHubInitCommand:
    """Initialize and configure a new GitHub repository."""

    def __init__(self, options: GitHubInitOptions):
        self.options = options
        self.original_dir = os.getcwd()
        self.created_files = []
        self.created_dirs = []
        self.github_repo_created = False

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

            # Step 6: Configure repository settings
            self._configure_repo()

            # Step 7: Initial commit and push
            self._commit_and_push()

            print(f"✅ Successfully initialized repository: {self.options.repo_name}")
        except Exception as e:
            print(f"❌ Error initializing repository: {e}")
            print("🔄 Rolling back changes...")
            self._rollback_changes()
            raise
        finally:
            os.chdir(self.original_dir)

    def _execute_dry_run(self) -> None:
        """Preview what would be created without actually executing."""
        print("🔍 DRY RUN MODE - Preview of repository initialization")
        print("=" * 60)
        print(f"📁 Repository: {self.options.repo_name}")
        print(f"📄 Description: {self.options.description or 'None'}")
        print(f"🔒 Visibility: {'Private' if self.options.private else 'Public'}")
        print(f"📋 License: {self.options.license or 'None'}")
        print(f"🗂️  Gitignore: {self.options.gitignore or 'None'}")
        print(f"📖 README: {'Yes' if self.options.readme else 'No'}")
        print(f"🌿 Default branch: {self.options.default_branch}")
        print(f"🏷️  Topics: {', '.join(self.options.topics) if self.options.topics else 'None'}")
        print(f"🌐 Website: {'Yes' if self.options.create_website else 'No'}")
        print(f"🤖 Dependabot: {'Yes' if self.options.enable_dependabot else 'No'}")
        
        print("\n📝 Files that would be created:")
        files_to_create = []
        
        # Git repository
        files_to_create.append(f"  📁 {self.options.repo_name}/.git/ (git repository)")
        
        # README
        if self.options.readme:
            files_to_create.append(f"  📄 {self.options.repo_name}/README.md")
        
        # License
        if self.options.license:
            files_to_create.append(f"  📄 {self.options.repo_name}/LICENSE ({self.options.license})")
        
        # Gitignore
        if self.options.gitignore:
            files_to_create.append(f"  📄 {self.options.repo_name}/.gitignore ({self.options.gitignore} template)")
        
        # GitHub workflows
        files_to_create.append(f"  📄 {self.options.repo_name}/.github/workflows/ci.yml")
        
        # Docusaurus files
        if self.options.create_website:
            files_to_create.extend([
                f"  📄 {self.options.repo_name}/package.json",
                f"  📄 {self.options.repo_name}/docusaurus.config.js",
                f"  📄 {self.options.repo_name}/sidebars.js",
                f"  📁 {self.options.repo_name}/docs/",
                f"  📄 {self.options.repo_name}/docs/intro.md",
                f"  📄 {self.options.repo_name}/.github/workflows/deploy-docusaurus.yml",
                f"  📄 {self.options.repo_name}/.github/workflows/pr-preview.yml"
            ])
        
        # Dependabot
        if self.options.enable_dependabot:
            files_to_create.append(f"  📄 {self.options.repo_name}/.github/dependabot.yml")
        
        for file_item in files_to_create:
            print(file_item)
        
        print("\n⚡ Actions that would be performed:")
        actions = [
            f"  1. Create local directory: {self.options.repo_name}/",
            f"  2. Initialize git repository with branch: {self.options.default_branch}",
            f"  3. Create {len([f for f in files_to_create if '📄' in f])} files",
            f"  4. Create GitHub repository ({'private' if self.options.private else 'public'})",
        ]
        
        if self.options.topics:
            actions.append(f"  5. Add topics: {', '.join(self.options.topics)}")
        
        actions.extend([
            f"  6. Configure git remote origin",
            f"  7. Create initial commit with all files",
            f"  8. Push to GitHub ({self.options.default_branch} branch)"
        ])
        
        for action in actions:
            print(action)
        
        print("\n" + "=" * 60)
        print("💡 This was a preview only. No files were created or modified.")
        print("💡 Remove --dry-run flag to actually create the repository.")

    def _validate_prerequisites(self) -> None:
        """Validate required tools and authentication."""
        print("🔍 Validating prerequisites...")
        
        # Check if git is available
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
            print(f"✅ Git is available: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("❌ Git is not installed or not available in PATH. Please install Git first.")
        
        # Check if GitHub CLI is available
        try:
            result = subprocess.run(["gh", "--version"], capture_output=True, text=True, check=True)
            version_line = result.stdout.split('\n')[0]
            print(f"✅ GitHub CLI is available: {version_line}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("❌ GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/")
        
        # Check GitHub CLI authentication
        try:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=True)
            print("✅ GitHub CLI is authenticated")
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.lower()
            if "not logged into" in error_output or "not authenticated" in error_output:
                raise RuntimeError("❌ GitHub CLI is not authenticated. Please run 'gh auth login' first.")
            else:
                raise RuntimeError(f"❌ GitHub CLI authentication check failed: {e.stderr}")
        
        # Check repository creation permissions
        try:
            result = subprocess.run(
                ["gh", "api", "user"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print("✅ GitHub API access confirmed")
        except subprocess.CalledProcessError:
            raise RuntimeError("❌ Cannot access GitHub API. Check your authentication and permissions.")
        
        # Check for Node.js if website creation is requested
        if self.options.create_website:
            try:
                result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
                version = result.stdout.strip()
                major_version = int(version.lstrip('v').split('.')[0])
                if major_version < 18:
                    raise RuntimeError(f"❌ Node.js version {version} is too old. Docusaurus requires Node.js 18+")
                print(f"✅ Node.js is available: {version}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError("❌ Node.js is not installed. Required for --create-website option.")
            except ValueError:
                print("⚠️  Could not parse Node.js version, but it seems to be installed")

    def _rollback_changes(self) -> None:
        """Rollback any changes made during failed initialization."""
        try:
            # Delete GitHub repository if it was created
            if self.github_repo_created:
                try:
                    print(f"🗑️  Deleting GitHub repository: {self.options.repo_name}")
                    subprocess.run(
                        ["gh", "repo", "delete", self.options.repo_name, "--yes"],
                        capture_output=True,
                        check=True
                    )
                    print("✅ GitHub repository deleted")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Could not delete GitHub repository: {e}")

            # Delete local directory if it was created
            repo_path = Path(self.options.repo_name)
            if repo_path.exists():
                try:
                    print(f"🗑️  Deleting local directory: {repo_path}")
                    import shutil
                    shutil.rmtree(repo_path)
                    print("✅ Local directory deleted")
                except Exception as e:
                    print(f"⚠️  Could not delete local directory: {e}")

        except Exception as e:
            print(f"⚠️  Error during rollback: {e}")

    def _init_git_repo(self) -> None:
        """Initialize local git repository."""
        print("📁 Initializing local git repository...")

        repo_path = Path(self.options.repo_name)
        repo_path.mkdir(parents=True, exist_ok=True)

        os.chdir(self.options.repo_name)
        subprocess.run(
            ["git", "init", f"--initial-branch={self.options.default_branch}"],
            check=True,
        )

    def _create_initial_files(self) -> None:
        """Create initial repository files."""
        print("📄 Creating initial files...")

        if self.options.readme:
            self._create_readme()

        if self.options.gitignore:
            self._create_gitignore()

        if self.options.license:
            self._create_license()

    def _create_readme(self) -> None:
        """Create README.md file."""
        readme_content = f"""# {self.options.repo_name}

{self.options.description or 'A new GitHub repository'}

## Getting Started

This repository was initialized using the Claude GitHub Init command.

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/{self.options.repo_name}.git

# Navigate to the project directory
cd {self.options.repo_name}
```

## License

{f'This project is licensed under the {self.options.license} License.' if self.options.license else 'This project is not yet licensed.'}
"""

        with open("README.md", "w") as f:
            f.write(readme_content)

    def _create_gitignore(self) -> None:
        """Create .gitignore file based on template."""
        gitignore_templates: Dict[str, str] = {
            "python": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
ENV/
.venv
.env

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
.pytest_cache/

# IDE
.idea/
.vscode/
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
Thumbs.db""",
            "node": """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Build outputs
dist/
build/
*.log
.cache
.parcel-cache

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
coverage/
.nyc_output/

# Misc
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db""",
            "general": """# OS files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Environment files
.env
.env.local

# Temporary files
*.tmp
*.temp
tmp/
temp/""",
            "rust": """# Generated by Cargo
/target/
**/*.rs.bk

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log

# Environment files
.env

# Lock file (optional to ignore)
# Cargo.lock""",
            "go": """# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool, specifically when used with LiteIDE
*.out

# Dependency directories (remove the comment below to include it)
# vendor/

# Go workspace file
go.work

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log

# Environment files
.env""",
            "java": """# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files #
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# virtual machine crash logs, see http://www.java.com/en/download/help/error_hotspot.xml
hs_err_pid*
replay_pid*

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle
build/
gradle-app.setting
!gradle-wrapper.jar
!gradle-wrapper.properties

# IDE files
.vscode/
.idea/
*.iws
*.iml
*.ipr
.settings/
.project
.classpath

# OS files
.DS_Store
Thumbs.db

# Environment files
.env""",
            "csharp": """# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/

# Visual Studio files
*.user
*.userosscache
*.sln.docstates
*.suo
*.vsp
*.vspx
*.sap

# User-specific files (MonoDevelop/Xamarin Studio)
*.userprefs

# Build results
[Dd]ebug/
[Rr]elease/
x64/
x86/
build/
bld/
[Bb]in/
[Oo]bj/

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# NUnit
*.VisualState.xml
TestResult.xml

# .NET Core
project.lock.json
project.fragment.lock.json
artifacts/

# IDE files
.vscode/
.vs/
.idea/

# OS files
.DS_Store
Thumbs.db

# Package files
*.nupkg
*.snupkg

# Environment files
.env""",
        }

        template = gitignore_templates.get(
            self.options.gitignore or "general", gitignore_templates["general"]
        )

        with open(".gitignore", "w") as f:
            f.write(template)

    def _create_github_workflows(self) -> None:
        """Create GitHub Actions workflows."""
        print("🔧 Creating GitHub Actions workflows...")

        # Create .github/workflows directory
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Create basic CI workflow
        self._create_ci_workflow()

        # Create Docusaurus deployment workflow if website is enabled
        if self.options.create_website:
            self._create_docusaurus_deploy_workflow()
            self._create_pr_preview_workflow()

        # Create dependabot configuration if enabled
        if self.options.enable_dependabot:
            self._create_dependabot_config()

    def _create_ci_workflow(self) -> None:
        """Create basic CI workflow based on project type."""
        # Determine workflow content based on gitignore/language and website option
        if self.options.create_website:
            ci_content = self._get_docusaurus_ci_workflow()
        elif self.options.gitignore == "python":
            ci_content = self._get_python_ci_workflow()
        elif self.options.gitignore == "node":
            ci_content = self._get_node_ci_workflow()
        elif self.options.gitignore == "rust":
            ci_content = self._get_rust_ci_workflow()
        elif self.options.gitignore == "go":
            ci_content = self._get_go_ci_workflow()
        elif self.options.gitignore == "java":
            ci_content = self._get_java_ci_workflow()
        elif self.options.gitignore == "csharp":
            ci_content = self._get_csharp_ci_workflow()
        else:
            ci_content = self._get_generic_ci_workflow()

        with open(".github/workflows/ci.yml", "w") as f:
            f.write(ci_content)

    def _get_python_ci_workflow(self) -> str:
        """Get Python-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        # Uncomment and modify as needed:
        # pip install -r requirements.txt
        # pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        # pip install flake8
        # flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        echo "Add linting steps here"
    
    - name: Type check with mypy
      run: |
        # pip install mypy
        # mypy .
        echo "Add type checking steps here"
    
    - name: Test with pytest
      run: |
        # pip install pytest pytest-cov
        # pytest --cov=./ --cov-report=xml
        echo "Add test steps here"
    
    - name: Upload coverage reports
      if: matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
"""

    def _get_node_ci_workflow(self) -> str:
        """Get Node.js-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: |
        # npm run lint
        echo "Add linting steps here"
    
    - name: Type check
      run: |
        # npm run typecheck
        echo "Add type checking steps here"
    
    - name: Test
      run: |
        # npm test -- --coverage
        echo "Add test steps here"
    
    - name: Build
      run: |
        # npm run build
        echo "Add build steps here"
    
    - name: Upload coverage reports
      if: matrix.node-version == '20.x'
      uses: codecov/codecov-action@v3
      with:
        fail_ci_if_error: false
"""

    def _get_generic_ci_workflow(self) -> str:
        """Get generic CI workflow template."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup
      run: |
        echo "Add setup steps here"
    
    - name: Install dependencies
      run: |
        echo "Add dependency installation here"
    
    - name: Lint
      run: |
        echo "Add linting steps here"
    
    - name: Test
      run: |
        echo "Add test steps here"
    
    - name: Build
      run: |
        echo "Add build steps here"
"""

    def _get_docusaurus_ci_workflow(self) -> str:
        """Get Docusaurus-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: 20
    
    - name: Install dependencies
      run: npm install
    
    - name: Build website
      run: npm run build
    
    - name: Test build artifacts
      run: |
        test -d build
        echo "Build directory created successfully"
    
    # Optional: Add more checks here
    # - name: Run tests
    #   run: npm test
    
    # - name: Lint
    #   run: npm run lint
"""

    def _get_rust_ci_workflow(self) -> str:
        """Get Rust-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        rust: [stable, beta, nightly]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Rust
      uses: dtolnay/rust-toolchain@stable
      with:
        toolchain: ${{ matrix.rust }}
        components: rustfmt, clippy
    
    - name: Cache cargo dependencies
      uses: actions/cache@v3
      with:
        path: |
          ~/.cargo/bin/
          ~/.cargo/registry/index/
          ~/.cargo/registry/cache/
          ~/.cargo/git/db/
          target/
        key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
        restore-keys: |
          ${{ runner.os }}-cargo-
    
    - name: Check formatting
      run: cargo fmt --all -- --check
    
    - name: Lint with clippy
      run: cargo clippy --all-targets --all-features -- -D warnings
    
    - name: Run tests
      run: cargo test --all-features
    
    - name: Build
      run: cargo build --release --all-features
"""

    def _get_go_ci_workflow(self) -> str:
        """Get Go-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: ['1.20', '1.21', '1.22']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Go
      uses: actions/setup-go@v5
      with:
        go-version: ${{ matrix.go-version }}
    
    - name: Cache Go modules
      uses: actions/cache@v3
      with:
        path: |
          ~/.cache/go-build
          ~/go/pkg/mod
        key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
        restore-keys: |
          ${{ runner.os }}-go-
    
    - name: Download dependencies
      run: go mod download
    
    - name: Verify dependencies
      run: go mod verify
    
    - name: Format check
      run: |
        if [ "$(gofmt -s -l . | wc -l)" -gt 0 ]; then
          echo "Code is not formatted. Please run 'go fmt ./...'"
          gofmt -s -l .
          exit 1
        fi
    
    - name: Lint
      uses: golangci/golangci-lint-action@v3
      with:
        version: latest
    
    - name: Run tests
      run: go test -race -coverprofile=coverage.out -covermode=atomic ./...
    
    - name: Build
      run: go build -v ./...
"""

    def _get_java_ci_workflow(self) -> str:
        """Get Java-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java-version: ['11', '17', '21']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up JDK ${{ matrix.java-version }}
      uses: actions/setup-java@v4
      with:
        java-version: ${{ matrix.java-version }}
        distribution: 'temurin'
    
    - name: Cache Maven dependencies
      uses: actions/cache@v3
      with:
        path: ~/.m2
        key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-m2-
    
    - name: Validate Maven wrapper
      run: |
        if [ -f mvnw ]; then
          chmod +x mvnw
          ./mvnw validate
        fi
    
    - name: Compile
      run: |
        if [ -f mvnw ]; then
          ./mvnw clean compile
        else
          mvn clean compile
        fi
    
    - name: Run tests
      run: |
        if [ -f mvnw ]; then
          ./mvnw test
        else
          mvn test
        fi
    
    - name: Package
      run: |
        if [ -f mvnw ]; then
          ./mvnw package -DskipTests
        else
          mvn package -DskipTests
        fi
    
    - name: Upload test reports
      uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: test-reports-${{ matrix.java-version }}
        path: target/surefire-reports/
"""

    def _get_csharp_ci_workflow(self) -> str:
        """Get C#/.NET-specific CI workflow."""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: ['6.0.x', '7.0.x', '8.0.x']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{ matrix.dotnet-version }}
    
    - name: Cache NuGet packages
      uses: actions/cache@v3
      with:
        path: ~/.nuget/packages
        key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj', '**/*.props') }}
        restore-keys: |
          ${{ runner.os }}-nuget-
    
    - name: Restore dependencies
      run: dotnet restore
    
    - name: Build
      run: dotnet build --no-restore --configuration Release
    
    - name: Run tests
      run: dotnet test --no-build --configuration Release --verbosity normal --collect:"XPlat Code Coverage"
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      if: matrix.dotnet-version == '8.0.x'
      with:
        file: '**/coverage.cobertura.xml'
        fail_ci_if_error: false
"""

    def _create_docusaurus_deploy_workflow(self) -> None:
        """Create Docusaurus deployment workflow."""
        deploy_content = """name: Deploy Docusaurus to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
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
          path: ./build
          
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
"""

        with open(".github/workflows/deploy-docusaurus.yml", "w") as f:
            f.write(deploy_content)

    def _create_pr_preview_workflow(self) -> None:
        """Create PR preview deployment workflow."""
        preview_content = """name: Deploy PR Preview

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  pull-requests: write
  contents: read

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build website
        run: npm run build
        env:
          DOCUSAURUS_BASE_URL: /pr-preview/pr-${{ github.event.pull_request.number }}/
          
      - name: Deploy preview
        uses: rossjrw/pr-preview-action@v1
        with:
          source-dir: ./build/
          preview-branch: gh-pages
          umbrella-dir: pr-preview
          action: deploy
          
      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const url = `https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/pr-preview/pr-${{ github.event.pull_request.number }}/`;
            const comment = `### 📖 Documentation Preview
            
            The documentation preview for this PR is available at:
            ${url}
            
            This preview will be updated automatically when the PR is updated.`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
"""

        with open(".github/workflows/pr-preview.yml", "w") as f:
            f.write(preview_content)

    def _create_dependabot_config(self) -> None:
        """Create dependabot configuration for automatic dependency updates."""
        print("🔧 Creating dependabot configuration...")

        # Determine package ecosystems based on project type
        ecosystems = []
        
        # Always include GitHub Actions
        ecosystems.append({
            "package-ecosystem": "github-actions",
            "directory": "/",
            "schedule": {"interval": "weekly"},
            "open-pull-requests-limit": 5
        })
        
        # Add ecosystems based on gitignore/project type
        if self.options.gitignore == "python" or self.options.create_website:
            if self.options.gitignore == "python":
                ecosystems.append({
                    "package-ecosystem": "pip",
                    "directory": "/",
                    "schedule": {"interval": "weekly"},
                    "open-pull-requests-limit": 5
                })
            
            if self.options.create_website:
                ecosystems.append({
                    "package-ecosystem": "npm",
                    "directory": "/",
                    "schedule": {"interval": "weekly"},
                    "open-pull-requests-limit": 5
                })
        
        elif self.options.gitignore == "node":
            ecosystems.append({
                "package-ecosystem": "npm",
                "directory": "/",
                "schedule": {"interval": "weekly"},
                "open-pull-requests-limit": 5
            })
        
        # If no specific gitignore, try to detect from files or use generic
        if not self.options.gitignore:
            # Check for common files to determine ecosystem
            if Path("package.json").exists() or Path("package-lock.json").exists():
                ecosystems.append({
                    "package-ecosystem": "npm",
                    "directory": "/",
                    "schedule": {"interval": "weekly"},
                    "open-pull-requests-limit": 5
                })
            if (Path("requirements.txt").exists() or Path("pyproject.toml").exists() or 
                Path("setup.py").exists() or Path("Pipfile").exists()):
                ecosystems.append({
                    "package-ecosystem": "pip",
                    "directory": "/",
                    "schedule": {"interval": "weekly"},
                    "open-pull-requests-limit": 5
                })

        dependabot_config = f"""version: 2
updates:"""
        
        for ecosystem in ecosystems:
            dependabot_config += f"""
  - package-ecosystem: "{ecosystem['package-ecosystem']}"
    directory: "{ecosystem['directory']}"
    schedule:
      interval: "{ecosystem['schedule']['interval']}"
    open-pull-requests-limit: {ecosystem['open-pull-requests-limit']}"""

        # Create .github directory if it doesn't exist
        github_dir = Path(".github")
        github_dir.mkdir(exist_ok=True)
        
        with open(".github/dependabot.yml", "w") as f:
            f.write(dependabot_config)

    def _create_license(self) -> None:
        """Create LICENSE file."""
        if self.options.license and self.options.license.upper() == "MIT":
            from datetime import datetime

            mit_license = f"""MIT License

Copyright (c) {datetime.now().year} [Your Name]

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
SOFTWARE."""

            with open("LICENSE", "w") as f:
                f.write(mit_license)

    def _initialize_docusaurus(self) -> None:
        """Initialize Docusaurus project."""
        print("🌐 Initializing Docusaurus website...")

        try:
            # Create package.json if it doesn't exist
            if not Path("package.json").exists():
                package_json = {
                    "name": self.options.repo_name,
                    "version": "0.0.0",
                    "private": True,
                    "scripts": {
                        "docusaurus": "docusaurus",
                        "start": "docusaurus start",
                        "build": "docusaurus build",
                        "swizzle": "docusaurus swizzle",
                        "deploy": "docusaurus deploy",
                        "clear": "docusaurus clear",
                        "serve": "docusaurus serve",
                        "write-translations": "docusaurus write-translations",
                        "write-heading-ids": "docusaurus write-heading-ids",
                    },
                    "dependencies": {
                        "@docusaurus/core": "^3.0.0",
                        "@docusaurus/preset-classic": "^3.0.0",
                        "@mdx-js/react": "^3.0.0",
                        "clsx": "^2.0.0",
                        "prism-react-renderer": "^2.1.0",
                        "react": "^18.0.0",
                        "react-dom": "^18.0.0",
                    },
                    "devDependencies": {
                        "@docusaurus/module-type-aliases": "^3.0.0",
                        "@docusaurus/types": "^3.0.0",
                    },
                    "browserslist": {
                        "production": [">0.5%", "not dead", "not op_mini all"],
                        "development": [
                            "last 3 chrome version",
                            "last 3 firefox version",
                            "last 5 safari version",
                        ],
                    },
                    "engines": {"node": ">=18.0"},
                }

                import json

                with open("package.json", "w") as f:
                    json.dump(package_json, f, indent=2)

            # Create docusaurus.config.js
            docusaurus_config = f"""// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {{themes as prismThemes}} from 'prism-react-renderer';

/** @type {{import('@docusaurus/types').Config}} */
const config = {{
  title: '{self.options.repo_name}',
  tagline: '{self.options.description or "Documentation for " + self.options.repo_name}',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://{"{username}"}.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/{self.options.repo_name}/',

  // GitHub pages deployment config.
  organizationName: '{"{username}"}', // Usually your GitHub org/user name.
  projectName: '{self.options.repo_name}', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {{
    defaultLocale: 'en',
    locales: ['en'],
  }},

  presets: [
    [
      'classic',
      /** @type {{import('@docusaurus/preset-classic').Options}} */
      ({{
        docs: {{
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          editUrl:
            'https://github.com/{"{username}"}/{self.options.repo_name}/tree/main/',
        }},
        blog: {{
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/{"{username}"}/{self.options.repo_name}/tree/main/',
        }},
        theme: {{
          customCss: './src/css/custom.css',
        }},
      }}),
    ],
  ],

  themeConfig:
    /** @type {{import('@docusaurus/preset-classic').ThemeConfig}} */
    ({{
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {{
        title: '{self.options.repo_name}',
        logo: {{
          alt: '{self.options.repo_name} Logo',
          src: 'img/logo.svg',
        }},
        items: [
          {{
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tutorial',
          }},
          {{to: '/blog', label: 'Blog', position: 'left'}},
          {{
            href: 'https://github.com/{"{username}"}/{self.options.repo_name}',
            label: 'GitHub',
            position: 'right',
          }},
        ],
      }},
      footer: {{
        style: 'dark',
        links: [
          {{
            title: 'Docs',
            items: [
              {{
                label: 'Tutorial',
                to: '/docs/intro',
              }},
            ],
          }},
          {{
            title: 'Community',
            items: [
              {{
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              }},
              {{
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              }},
              {{
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              }},
            ],
          }},
          {{
            title: 'More',
            items: [
              {{
                label: 'Blog',
                to: '/blog',
              }},
              {{
                label: 'GitHub',
                href: 'https://github.com/{"{username}"}/{self.options.repo_name}',
              }},
            ],
          }},
        ],
        copyright: `Copyright © ${{new Date().getFullYear()}} {self.options.repo_name}. Built with Docusaurus.`,
      }},
      prism: {{
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      }},
    }}),
}};

export default config;
"""

            with open("docusaurus.config.js", "w") as f:
                f.write(docusaurus_config)

            # Create sidebars.js
            sidebars_content = """/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
"""

            with open("sidebars.js", "w") as f:
                f.write(sidebars_content)

            # Create docs directory with intro page
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)

            intro_content = f"""---
sidebar_position: 1
---

# Tutorial Intro

Let's discover **{self.options.repo_name} in less than 5 minutes**.

## Getting Started

Get started by **creating a new site**.

Or **try Docusaurus immediately** with **[docusaurus.new](https://docusaurus.new)**.

### What you'll need

- [Node.js](https://nodejs.org/en/download/) version 18.0 or above:
  - When installing Node.js, you are recommended to check all checkboxes related to dependencies.

## Generate a new site

Generate a new Docusaurus site using the **classic template**.

The classic template will automatically be added to your project after you run the command:

```bash
npm init docusaurus@latest my-website classic
```

You can type this command into Command Prompt, Powershell, Terminal, or any other integrated terminal of your code editor.

The command also installs all necessary dependencies you need to run Docusaurus.

## Start your site

Run the development server:

```bash
cd my-website
npm run start
```

The `cd` command changes the directory you're working with. In order to work with your newly created Docusaurus site, you'll need to navigate the terminal there.

The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.

Open `docs/intro.md` (this page) and edit some lines: the site **reloads automatically** and displays your changes.
"""

            with open("docs/intro.md", "w") as f:
                f.write(intro_content)

            # Create src directory structure
            src_dir = Path("src")
            src_dir.mkdir(exist_ok=True)

            # Create CSS directory
            css_dir = src_dir / "css"
            css_dir.mkdir(exist_ok=True)

            custom_css = """/**
 * Any CSS included here will be global. The classic template
 * bundles Infima by default. Infima is a CSS framework designed to
 * work well for content-centric websites.
 */

/* You can override the default Infima variables here. */
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

/* For readability concerns, you should choose a lighter palette in dark mode. */
[data-theme='dark'] {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: #21af90;
  --ifm-color-primary-darker: #1fa588;
  --ifm-color-primary-darkest: #1a8870;
  --ifm-color-primary-light: #29d5b0;
  --ifm-color-primary-lighter: #32d8b4;
  --ifm-color-primary-lightest: #4fddbf;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}
"""

            with open(css_dir / "custom.css", "w") as f:
                f.write(custom_css)

            # Create pages directory
            pages_dir = src_dir / "pages"
            pages_dir.mkdir(exist_ok=True)

            # Create index page
            index_content = """import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Docusaurus Tutorial - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
"""

            with open(pages_dir / "index.js", "w") as f:
                f.write(index_content)

            # Create index.module.css
            index_css = """.heroBanner {
  padding: 4rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

@media screen and (max-width: 996px) {
  .heroBanner {
    padding: 2rem;
  }
}

.buttons {
  display: flex;
  align-items: center;
  justify-content: center;
}
"""

            with open(pages_dir / "index.module.css", "w") as f:
                f.write(index_css)

            # Create components directory
            components_dir = src_dir / "components"
            components_dir.mkdir(exist_ok=True)

            # Create HomepageFeatures component
            features_dir = components_dir / "HomepageFeatures"
            features_dir.mkdir(exist_ok=True)

            features_content = """import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Easy to Use',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Docusaurus was designed from the ground up to be easily installed and
        used to get your website up and running quickly.
      </>
    ),
  },
  {
    title: 'Focus on What Matters',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Docusaurus lets you focus on your docs, and we&apos;ll do the chores. Go
        ahead and move your docs into the <code>docs</code> directory.
      </>
    ),
  },
  {
    title: 'Powered by React',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Extend or customize your website layout by reusing React. Docusaurus can
        be extended while reusing the same header and footer.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
"""

            with open(features_dir / "index.js", "w") as f:
                f.write(features_content)

            features_css = """.features {
  display: flex;
  align-items: center;
  padding: 2rem 0;
  width: 100%;
}

.featureSvg {
  height: 200px;
  width: 200px;
}
"""

            with open(features_dir / "styles.module.css", "w") as f:
                f.write(features_css)

            # Create static directories
            static_dir = Path("static")
            static_dir.mkdir(exist_ok=True)

            img_dir = static_dir / "img"
            img_dir.mkdir(exist_ok=True)

            # Create .gitignore for Docusaurus
            docusaurus_gitignore = """# Dependencies
/node_modules

# Production
/build

# Generated files
.docusaurus
.cache-loader

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""

            # Append to existing .gitignore or create new one
            existing_gitignore = ""
            if Path(".gitignore").exists():
                with open(".gitignore", "r") as f:
                    existing_gitignore = f.read()

            if "node_modules" not in existing_gitignore:
                with open(".gitignore", "a") as f:
                    f.write("\n# Docusaurus\n" + docusaurus_gitignore)

            print("✅ Docusaurus initialized successfully!")
            print("📝 Remember to:")
            print("   1. Replace {username} placeholders in docusaurus.config.js")
            print("   2. Run 'npm install' to install dependencies")
            print("   3. Run 'npm start' to preview the site locally")

        except Exception as e:
            print(f"⚠️  Error initializing Docusaurus: {e}")
            raise

    def _create_github_repo(self) -> None:
        """Create GitHub repository using gh CLI."""
        print("🌐 Creating GitHub repository...")

        visibility = "--public" if not self.options.private else "--private"
        cmd = ["gh", "repo", "create", self.options.repo_name, visibility, "--confirm"]

        if self.options.description:
            cmd.extend(["--description", self.options.description])

        try:
            subprocess.run(cmd, check=True)
            self.github_repo_created = True  # Track that repo was created
            # Get current GitHub user
            result = subprocess.run(
                ["gh", "api", "user", "--jq", ".login"],
                capture_output=True,
                text=True,
                check=True,
            )
            username = result.stdout.strip()
            # Set up git remote
            remote_url = f"https://github.com/{username}/{self.options.repo_name}.git"
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
            print(f"✅ Repository created and remote configured: {remote_url}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Could not create remote repository or set up remote: {e}")
            print("You may need to set up the remote manually.")

    def _configure_repo(self) -> None:
        """Configure repository settings."""
        print("⚙️  Configuring repository...")

        if self.options.topics:
            try:
                for topic in self.options.topics:
                    subprocess.run(
                        ["gh", "repo", "edit", "--add-topic", topic], check=True
                    )
                print(f"✅ Added topics: {', '.join(self.options.topics)}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Could not add topics to repository: {e}")

    def _commit_and_push(self) -> None:
        """Create initial commit and push to remote."""
        print("📤 Creating initial commit and pushing...")

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        try:
            subprocess.run(
                ["git", "push", "-u", "origin", self.options.default_branch], check=True
            )
        except subprocess.CalledProcessError:
            print(
                "⚠️  Could not push to remote. You may need to set up the remote manually."
            )


def load_config_defaults() -> Dict[str, any]:
    """Load default configuration from ~/.github-init.yaml"""
    config_path = Path.home() / ".github-init.yaml"
    
    if not config_path.exists():
        return {}
    
    if yaml is None:
        print("⚠️  Warning: PyYAML not installed. Install with 'pip install PyYAML' to use config files.")
        return {}
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
        
        # Validate configuration keys
        valid_keys = {
            'description', 'private', 'license', 'gitignore', 'readme', 
            'default_branch', 'topics', 'create_website', 'enable_dependabot'
        }
        
        # Filter out invalid keys and warn
        filtered_config = {}
        for key, value in config.items():
            if key in valid_keys:
                filtered_config[key] = value
            else:
                print(f"⚠️  Warning: Unknown config key '{key}' in ~/.github-init.yaml")
        
        return filtered_config
        
    except Exception as e:
        # Handle both YAML errors and file I/O errors
        error_name = type(e).__name__
        if yaml and hasattr(yaml, 'YAMLError') and error_name == 'YAMLError':
            print(f"⚠️  Warning: Error parsing ~/.github-init.yaml: {e}")
        else:
            print(f"⚠️  Warning: Error reading ~/.github-init.yaml: {e}")
        return {}


def get_interactive_options() -> GitHubInitOptions:
    """Get repository options through interactive prompts."""
    print("🔧 Interactive GitHub Repository Setup")
    print("=" * 40)
    
    # Load configuration defaults
    config = load_config_defaults()
    if config:
        print(f"📁 Loaded defaults from ~/.github-init.yaml")
        print("=" * 40)

    # Repository name (required)
    while True:
        repo_name = input("Repository name: ").strip()
        if repo_name:
            break
        print("Repository name is required.")

    # Description (optional)
    default_desc = config.get('description', '')
    desc_prompt = f"Description (optional{', default: ' + default_desc if default_desc else ''}): "
    description_input = input(desc_prompt).strip()
    description: Optional[str] = description_input if description_input else (default_desc if default_desc else None)

    # Public/private
    default_private = config.get('private', True)
    visibility_default = "y/N" if default_private else "Y/n"
    while True:
        visibility = input(f"Make repository public? ({visibility_default}): ").strip().lower()
        if visibility in ["", "n", "no"]:
            private = True
            break
        elif visibility in ["y", "yes"]:
            private = False
            break
        print("Please enter 'y' for yes or 'n' for no.")
    
    # Apply default if no input provided
    if not visibility:
        private = default_private

    # License
    default_license = config.get('license', '')
    print("\nAvailable licenses: MIT, Apache-2.0, GPL-3.0")
    license_prompt = f"License (optional{', default: ' + default_license if default_license else ''}): "
    license_choice: Optional[str] = None
    while True:
        license_input = input(license_prompt).strip()
        if not license_input or license_input in ["MIT", "Apache-2.0", "GPL-3.0"]:
            license_choice = license_input if license_input else (default_license if default_license else None)
            break
        print("Please enter a valid license: MIT, Apache-2.0, GPL-3.0, or leave empty.")

    # Gitignore template
    default_gitignore = config.get('gitignore', '')
    print("\nAvailable gitignore templates: python, node, rust, go, java, csharp, general")
    gitignore_prompt = f"Gitignore template (optional{', default: ' + default_gitignore if default_gitignore else ''}): "
    gitignore: Optional[str] = None
    while True:
        gitignore_input = input(gitignore_prompt).strip()
        if not gitignore_input or gitignore_input in ["python", "node", "rust", "go", "java", "csharp", "general"]:
            gitignore = gitignore_input if gitignore_input else (default_gitignore if default_gitignore else None)
            break
        print("Please enter a valid template: python, node, rust, go, java, csharp, general, or leave empty.")

    # README
    default_readme = config.get('readme', True)
    readme_default = "Y/n" if default_readme else "y/N"
    while True:
        create_readme = input(f"Create README.md? ({readme_default}): ").strip().lower()
        if create_readme in ["", "y", "yes"]:
            readme = True
            break
        elif create_readme in ["n", "no"]:
            readme = False
            break
        print("Please enter 'y' for yes or 'n' for no.")
    
    # Apply default if no input provided
    if not create_readme:
        readme = default_readme

    # Default branch
    config_branch = config.get('default_branch', 'main')
    branch_prompt = f"Default branch name ({config_branch}): "
    default_branch = input(branch_prompt).strip()
    default_branch = default_branch if default_branch else config_branch

    # Topics
    default_topics = config.get('topics', [])
    topics_default = ', '.join(default_topics) if default_topics else ''
    topics_prompt = f"Topics (comma-separated{', default: ' + topics_default if topics_default else ''}): "
    topics_input = input(topics_prompt).strip()
    if topics_input:
        topics = [t.strip() for t in topics_input.split(",") if t.strip()]
    else:
        topics = default_topics if default_topics else None

    # Website creation
    default_website = config.get('create_website', False)
    website_default = "Y/n" if default_website else "y/N"
    while True:
        create_website = (
            input(f"Create Docusaurus documentation website? ({website_default}): ").strip().lower()
        )
        if create_website in ["", "n", "no"]:
            website = False
            break
        elif create_website in ["y", "yes"]:
            website = True
            break
        print("Please enter 'y' for yes or 'n' for no.")
    
    # Apply default if no input provided
    if not create_website:
        website = default_website

    # Dependabot configuration
    default_dependabot = config.get('enable_dependabot', True)
    dependabot_default = "Y/n" if default_dependabot else "y/N"
    while True:
        enable_dependabot = (
            input(f"Enable dependabot for dependency updates? ({dependabot_default}): ").strip().lower()
        )
        if enable_dependabot in ["", "y", "yes"]:
            dependabot = True
            break
        elif enable_dependabot in ["n", "no"]:
            dependabot = False
            break
        print("Please enter 'y' for yes or 'n' for no.")
    
    # Apply default if no input provided
    if not enable_dependabot:
        dependabot = default_dependabot

    options = GitHubInitOptions(
        repo_name=repo_name,
        description=description,
        private=private,
        license=license_choice,
        gitignore=gitignore,
        readme=readme,
        default_branch=default_branch,
        topics=topics,
        create_website=website,
        enable_dependabot=dependabot,
        dry_run=False,  # Interactive mode doesn't use dry-run
    )

    # Show preview
    print("\n" + "=" * 40)
    print("📋 Repository Configuration Preview")
    print("=" * 40)
    print(f"Name: {options.repo_name}")
    print(f"Description: {options.description or 'None'}")
    print(f"Visibility: {'Private' if options.private else 'Public'}")
    print(f"License: {options.license or 'None'}")
    print(f"Gitignore: {options.gitignore or 'None'}")
    print(f"README: {'Yes' if options.readme else 'No'}")
    print(f"Default branch: {options.default_branch}")
    print(f"Topics: {', '.join(options.topics) if options.topics else 'None'}")
    print(f"Website: {'Yes' if options.create_website else 'No'}")
    print(f"Dependabot: {'Yes' if options.enable_dependabot else 'No'}")

    # Confirm
    while True:
        confirm = input("\nProceed with this configuration? (Y/n): ").strip().lower()
        if confirm in ["", "y", "yes"]:
            return options
        elif confirm in ["n", "no"]:
            print("Aborting repository creation.")
            exit(0)
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def parse_arguments(args: List[str]) -> GitHubInitOptions:
    """Parse command arguments into GitHubInitOptions."""
    parser = argparse.ArgumentParser(
        prog="/github-init",
        description="Initialize and configure a new GitHub repository",
    )

    parser.add_argument("repo_name", nargs="?", help="Name of the repository to create")
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Use interactive mode with prompts",
    )
    parser.add_argument(
        "--desc", "--description", dest="description", help="Repository description"
    )
    parser.add_argument(
        "--public",
        action="store_true",
        help="Create a public repository (default: private)",
    )
    parser.add_argument(
        "--license", choices=["MIT", "Apache-2.0", "GPL-3.0"], help="Add a license file"
    )
    parser.add_argument(
        "--gitignore",
        choices=["python", "node", "rust", "go", "java", "csharp", "general"],
        help="Add .gitignore file with template",
    )
    parser.add_argument(
        "--no-readme",
        dest="readme",
        action="store_false",
        default=True,
        help="Skip README creation",
    )
    parser.add_argument(
        "--branch",
        dest="default_branch",
        default="main",
        help="Default branch name (default: main)",
    )
    parser.add_argument("--topics", help="Comma-separated list of repository topics")
    parser.add_argument(
        "--create-website",
        action="store_true",
        help="Initialize a Docusaurus documentation website",
    )
    parser.add_argument(
        "--no-dependabot",
        action="store_true",
        help="Disable dependabot configuration (enabled by default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without executing (dry run mode)",
    )

    parsed = parser.parse_args(args)

    # Use interactive mode if no repo_name provided or --interactive flag used
    if not parsed.repo_name or parsed.interactive:
        return get_interactive_options()

    # Load config defaults for CLI mode too
    config = load_config_defaults()

    return GitHubInitOptions(
        repo_name=parsed.repo_name,
        description=parsed.description or config.get('description'),
        private=not parsed.public if parsed.public else config.get('private', True),
        license=parsed.license or config.get('license'),
        gitignore=parsed.gitignore or config.get('gitignore'),
        readme=parsed.readme if hasattr(parsed, 'readme') else config.get('readme', True),
        default_branch=parsed.default_branch or config.get('default_branch', 'main'),
        topics=parsed.topics.split(",") if parsed.topics else config.get('topics'),
        create_website=parsed.create_website or config.get('create_website', False),
        enable_dependabot=not parsed.no_dependabot if parsed.no_dependabot else config.get('enable_dependabot', True),
        dry_run=parsed.dry_run,
    )


def handle_github_init_command(args: List[str]) -> None:
    """Handle the /github-init slash command."""
    try:
        options = parse_arguments(args)
        command = GitHubInitCommand(options)
        command.execute()
    except SystemExit:
        # argparse calls sys.exit() on error, we want to handle it gracefully
        pass
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    import sys

    handle_github_init_command(sys.argv[1:])
