# Update Command

Update claude-slash commands to the latest release from GitHub.

## Usage

```bash
/project:update
```

## Description

This command checks for the latest release of claude-slash on GitHub and updates your installed commands. The update process:

- Checks GitHub releases API for the latest version
- Downloads the latest command files
- Creates a backup of existing commands
- Updates commands in place
- Shows what changed in the new release

## Implementation

!echo "🔄 Checking for claude-slash updates..."

!# GitHub API endpoint for latest release
!REPO_URL="https://api.github.com/repos/jeremyeder/claude-slash/releases/latest"
!DOWNLOAD_URL="https://api.github.com/repos/jeremyeder/claude-slash/tarball"

!# Determine installation location
!if [ -d ".claude/commands" ]; then
!  INSTALL_DIR=".claude/commands"
!  INSTALL_TYPE="project"
!elif [ -d "$HOME/.claude/commands" ]; then
!  INSTALL_DIR="$HOME/.claude/commands"
!  INSTALL_TYPE="global"
!else
!  echo "❌ No claude-slash installation found"
!  echo "Run the installer first: curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash"
!  exit 1
!fi

!echo "📍 Found $INSTALL_TYPE installation at: $INSTALL_DIR"

!# Check for latest release
!echo "🔍 Checking latest release..."
!if ! command -v curl &> /dev/null; then
!  echo "❌ curl is required but not installed"
!  exit 1
!fi

!LATEST_INFO=$(curl -s "$REPO_URL")
!if [ $? -ne 0 ]; then
!  echo "❌ Failed to check for updates (network error)"
!  exit 1
!fi

!LATEST_TAG=$(echo "$LATEST_INFO" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
!RELEASE_NOTES=$(echo "$LATEST_INFO" | grep '"body"' | sed 's/.*"body": *"\([^"]*\)".*/\1/' | sed 's/\\n/\n/g' | head -5)

!if [ -z "$LATEST_TAG" ]; then
!  echo "❌ Could not determine latest version"
!  exit 1
!fi

!echo "📦 Latest release: $LATEST_TAG"

!# Create backup directory
!BACKUP_DIR="$INSTALL_DIR.backup.$(date +%Y%m%d-%H%M%S)"
!echo "💾 Creating backup at: $BACKUP_DIR"
!cp -r "$INSTALL_DIR" "$BACKUP_DIR"

!# Download and extract latest release
!TEMP_DIR=$(mktemp -d)
!echo "⬇️  Downloading latest release..."

!curl -sL "$DOWNLOAD_URL/$LATEST_TAG" | tar -xz -C "$TEMP_DIR" --strip-components=1

!if [ $? -ne 0 ]; then
!  echo "❌ Failed to download release"
!  echo "🔄 Restoring from backup..."
!  rm -rf "$INSTALL_DIR"
!  mv "$BACKUP_DIR" "$INSTALL_DIR"
!  rm -rf "$TEMP_DIR"
!  exit 1
!fi

!# Update commands
!if [ -d "$TEMP_DIR/.claude/commands" ]; then
!  echo "🔄 Updating commands..."
!  
!  # Remove old commands (but keep backups)
!  find "$INSTALL_DIR" -name "*.md" -delete
!  
!  # Copy new commands
!  cp "$TEMP_DIR/.claude/commands/"*.md "$INSTALL_DIR/"
!  
!  echo "✅ Update completed successfully!"
!  echo ""
!  echo "📋 What's new in $LATEST_TAG:"
!  echo "$RELEASE_NOTES"
!  echo ""
!  echo "📁 Backup saved to: $BACKUP_DIR"
!  echo "🗑️  Remove backup with: rm -rf $BACKUP_DIR"
!  
!else
!  echo "❌ Downloaded release doesn't contain command files"
!  echo "🔄 Restoring from backup..."
!  rm -rf "$INSTALL_DIR"
!  mv "$BACKUP_DIR" "$INSTALL_DIR"
!fi

!# Cleanup
!rm -rf "$TEMP_DIR"

!echo ""
!echo "🎉 claude-slash commands updated to $LATEST_TAG"