# Update Command

Update claude-slash commands to the latest release from GitHub.

## Usage

```bash
/project:update
```

## Description

This command updates your local claude-slash commands to the latest release version from GitHub. It:

- Checks for the latest release on GitHub
- Creates a backup of existing commands
- Downloads and installs new command files
- Preserves your existing configuration

The update process is safe and includes automatic rollback if anything goes wrong.

## Implementation

!echo "🔄 Updating claude-slash commands..."
!echo

!# Determine installation location
!install_dir=""
!install_type=""

!if [ -d ".claude/commands" ]; then
!    install_dir=".claude/commands"
!    install_type="project"
!elif [ -d "$HOME/.claude/commands" ]; then
!    install_dir="$HOME/.claude/commands"
!    install_type="global"
!else
!    echo "❌ No claude-slash installation found"
!    echo "Run the installer first:"
!    echo "curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh -o install.sh && bash install.sh"
!    exit 1
!fi

!echo "📍 Found $install_type installation at: $install_dir"

!# Check for latest release
!echo "🔍 Checking latest release..."
!latest_info=$(curl -s "https://api.github.com/repos/jeremyeder/claude-slash/releases/latest")
!if [ $? -ne 0 ]; then
!    echo "❌ Failed to check for updates (network error)"
!    exit 1
!fi

!latest_tag=$(echo "$latest_info" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')

!if [ -z "$latest_tag" ]; then
!    echo "❌ Could not determine latest version"
!    exit 1
!fi

!echo "📦 Latest release: $latest_tag"

!# Create backup
!backup_dir="$install_dir.backup.$(date +%Y%m%d-%H%M%S)"
!echo "💾 Creating backup at: $backup_dir"
!cp -r "$install_dir" "$backup_dir"

!# Download and extract latest release
!temp_dir=$(mktemp -d)
!echo "⬇️  Downloading latest release..."

!download_url="https://api.github.com/repos/jeremyeder/claude-slash/tarball/$latest_tag"
!tarball_file="$temp_dir/claude-slash.tar.gz"
!curl -sL "$download_url" -o "$tarball_file"
!if [ $? -ne 0 ] || ! tar -xz -C "$temp_dir" --strip-components=1 -f "$tarball_file"; then
!    echo "❌ Failed to download release"
!    echo "🔄 Restoring from backup..."
!    rm -rf "$install_dir"
!    mv "$backup_dir" "$install_dir"
!    rm -rf "$temp_dir"
!    exit 1
!fi

!# Update commands
!if [ -d "$temp_dir/.claude/commands" ]; then
!    echo "🔄 Updating commands..."
!
!    # Remove old commands
!    find "$install_dir" -name "*.md" -delete
!
!    # Copy new commands
!    cp "$temp_dir/.claude/commands/"*.md "$install_dir/"
!
!    echo "✅ Update completed successfully!"
!    echo "📦 Updated to: $latest_tag"
!    echo "📁 Backup saved to: $backup_dir"
!    echo "🗑️  Remove backup with: rm -rf $backup_dir"
!
!else
!    echo "❌ Downloaded release doesn't contain command files"
!    echo "🔄 Restoring from backup..."
!    rm -rf "$install_dir"
!    mv "$backup_dir" "$install_dir"
!fi

!# Cleanup
!rm -rf "$temp_dir"

!echo
!echo "🎉 claude-slash commands updated successfully!"
!echo
!echo "Available commands:"
!echo "  • /project:checkpoint - Create session checkpoints"
!echo "  • /project:ckpt - Shorthand for checkpoint"
!echo "  • /project:restore - Restore from checkpoint"
!echo "  • /project:rst - Shorthand for restore"
!echo "  • /project:update - Update to latest release"
!echo "  • /project:up - Shorthand for update"

## Notes

- The update process creates automatic backups for safety
- If the update fails, your previous installation is automatically restored
- Updates preserve your local project configuration
- The command works for both project-specific and global installations
