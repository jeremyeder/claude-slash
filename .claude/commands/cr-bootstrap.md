# CR Bootstrap (cr-bootstrap)

Bootstrap claude-slash installation with interactive setup and configuration.

## Usage

```bash
/project:cr-bootstrap [--global] [--force] [--yes]
```

## Description

This command provides an interactive bootstrap process for setting up claude-slash commands. It:

- Detects the current environment (project vs global)
- Downloads and installs the latest claude-slash commands
- Sets up the proper directory structure
- Configures basic settings and preferences
- Validates the installation

## Options

- `--global` - Install globally in ~/.claude/commands
- `--force` - Force reinstallation even if already installed
- `--yes` - Skip interactive prompts and use defaults

## Implementation

!echo "🚀 claude-slash bootstrap"
!echo

!# Parse arguments
!install_global=false
!force_install=false
!skip_prompts=false

!for arg in $ARGUMENTS; do
!    case $arg in
!        --global)
!            install_global=true
!            ;;
!        --force)
!            force_install=true
!            ;;
!        --yes)
!            skip_prompts=true
!            ;;
!        *)
!            echo "❌ Unknown option: $arg"
!            echo "Usage: /project:cr-bootstrap [--global] [--force] [--yes]"
!            exit 1
!            ;;
!    esac
!done

!# Determine installation target
!if [ "$install_global" = true ]; then
!    install_dir="$HOME/.claude/commands"
!    install_type="global"
!else
!    install_dir=".claude/commands"
!    install_type="project"
!fi

!echo "🎯 Target: $install_type installation"
!echo "📁 Directory: $install_dir"

!# Check if already installed
!if [ -d "$install_dir" ] && [ "$force_install" = false ]; then
!    if [ "$skip_prompts" = false ]; then
!        echo
!        echo "⚠️  claude-slash is already installed in $install_dir"
!        echo -n "Do you want to reinstall? (y/N): "
!        read -r response
!        if [[ ! "$response" =~ ^[Yy]$ ]]; then
!            echo "❌ Installation cancelled"
!            exit 0
!        fi
!    else
!        echo "⚠️  claude-slash already installed (use --force to reinstall)"
!        exit 0
!    fi
!fi

!# Create directory structure
!echo
!echo "📁 Creating directory structure..."
!mkdir -p "$install_dir"
!
!# Create checkpoints directory
!if [ "$install_type" = "project" ]; then
!    mkdir -p ".claude/checkpoints"
!    echo "✅ Created checkpoints directory"
!fi

!# Download latest release info
!echo
!echo "🔍 Checking latest release..."
!if ! latest_info=$(curl -s "<https://api.github.com/repos/jeremyeder/claude-slash/releases/latest>"); then
!    echo "❌ Failed to check latest release (network error)"
!    exit 1
!fi

!latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
!if [ -z "$latest_tag" ]; then
!    echo "❌ Could not determine latest version"
!    exit 1
!fi

!echo "📦 Latest release: $latest_tag"

!# Download and install commands
!echo
!echo "⬇️  Downloading commands..."
!temp_dir=$(mktemp -d)

!download_url="<https://api.github.com/repos/jeremyeder/claude-slash/tarball/$latest_tag>"
!if ! curl -sL "$download_url" | tar -xz -C "$temp_dir" --strip-components=1; then
!    echo "❌ Failed to download release"
!    rm -rf "$temp_dir"
!    exit 1
!fi

!# Install commands
!if [ -d "$temp_dir/.claude/commands" ]; then
!    echo "📋 Installing commands..."
!    cp "$temp_dir/.claude/commands/"*.md "$install_dir/"
!    echo "✅ Commands installed successfully"
!else
!    echo "❌ Downloaded release doesn't contain command files"
!    rm -rf "$temp_dir"
!    exit 1
!fi

!# Cleanup
!rm -rf "$temp_dir"

!# Check for GitHub Actions integration (if in git repo)
!if git rev-parse --git-dir > /dev/null 2>&1; then
!    echo
!    echo "🔍 Checking GitHub Actions integration..."
!    if [ ! -f ".github/workflows/ci.yml" ] && [ ! -f ".github/workflows/main.yml" ] && [ ! -d ".github/workflows" ]; then
!        echo "⚠️  Warning: This appears to be a GitHub repository without GitHub Actions integration."
!        echo "   Consider setting up GitHub Actions for automated testing and deployment."
!        echo "   See: <https://docs.github.com/en/actions/quickstart>"
!    else
!        echo "✅ GitHub Actions integration detected"
!    fi
!fi

!# Validate installation
!echo
!echo "🔍 Validating installation..."
!command_count=$(find "$install_dir" -name "*.md" | wc -l)
!echo "📋 Found $command_count command files"

!if [ "$command_count" -eq 0 ]; then
!    echo "❌ No commands found after installation"
!    exit 1
!fi

!# Setup pre-commit hooks (if in git repo)
!if git rev-parse --git-dir > /dev/null 2>&1; then
!    echo
!    echo "🪝 Setting up pre-commit hooks..."
!
!    # Check if pre-commit is installed
!    if command -v pre-commit > /dev/null 2>&1; then
!        # Check if .pre-commit-config.yaml exists
!        if [ -f ".pre-commit-config.yaml" ]; then
!            echo "📋 Installing pre-commit hooks..."
!            if pre-commit install; then
!                echo "✅ Pre-commit hooks installed successfully"
!            else
!                echo "⚠️  Warning: Failed to install pre-commit hooks"
!            fi
!        else
!            echo "⚠️  No .pre-commit-config.yaml found - skipping pre-commit setup"
!        fi
!    else
!        echo "⚠️  pre-commit not installed - skipping hook setup"
!        echo "   Install with: pip install pre-commit (or brew install pre-commit)"
!    fi
!fi

!# Show available commands
!echo
!echo "🎉 Bootstrap completed successfully!"
!echo
!echo "📋 Available commands:"
!find "$install_dir" -name "*.md" -exec basename {} .md \; | sort | while read -r cmd; do
!    echo "  • /project:$cmd"
!done

!echo
!echo "🎯 Next steps:"
!echo "1. Try creating a checkpoint: /project:checkpoint"
!echo "2. View all commands with: ls $install_dir"
!echo "3. Update anytime with: /project:update"

!if [ "$install_type" = "project" ]; then
!    echo
!    echo "💡 Tips:"
!    echo "- Checkpoints are saved in .claude/checkpoints/"
!    echo "- Add .claude/ to your .gitignore if desired"
!    echo "- Use /project:restore to restore from checkpoints"
!fi

## Notes

- Bootstrap automatically installs the latest stable release
- Creates necessary directory structure for session management
- Validates the installation before completing
- Provides helpful next steps and usage tips
- Supports both project-local and global installations
