# Slash Command Help and Update System

Display Rich-formatted help with all available commands, or update to the latest release with progress tracking.

## Usage
```
/slash              # Show help with all commands
/slash update       # Update to latest release
/slash help         # Explicit help (same as no arguments)
```

## Description

The main slash command provides two core functions: displaying comprehensive help information about all available commands, and updating the claude-slash system to the latest release.

### Help Display (Default)
When run without arguments or with `help`, this command:
- **📋 Command Discovery**: Automatically finds all installed commands
- **📊 Rich Formatting**: Beautiful table display with command descriptions
- **💡 Usage Examples**: Shows proper command syntax and examples
- **🔍 Smart Descriptions**: Extracts descriptions from command files
- **📁 Installation Info**: Shows where commands are installed

### Update System
The `update` subcommand provides:
- **🔄 Latest Release Detection**: Uses GitHub API to find newest version
- **📦 Progress Tracking**: Visual progress bars for download and installation
- **💾 Automatic Backup**: Creates timestamped backups before updating
- **🔁 Rollback Protection**: Automatic restoration if update fails
- **✅ Verification**: Confirms successful installation

## Arguments
- No arguments or `help`: Display help information (default behavior)
- `update`: Update claude-slash commands to latest GitHub release

## Examples

### Show Help
```bash
/slash
# Displays table of all available commands with descriptions
```

### Update Commands
```bash
/slash update
# Downloads and installs latest release with progress tracking
```

### Explicit Help
```bash
/slash help
# Same as running /slash with no arguments
```

## Help Display Features

### Command Table
Shows all available commands in a formatted table:
```
┌─ Available Claude Slash Commands ────────────────────┐
│ Command              │ Description                   │
├──────────────────────┼───────────────────────────────┤
│ /learn               │ Interactive learning system   │
│ /github-init my-repo │ Repository initialization     │
│ /menuconfig          │ TUI configuration editor      │
└──────────────────────┴───────────────────────────────┘
```

### Installation Detection
Automatically detects and reports command installation location:
- **Project Installation**: `.claude/commands/` in current git repository
- **Global Installation**: `~/.claude/commands/` in home directory
- **Installation Status**: Reports if no commands are found

### Smart Description Extraction
For each command file, extracts:
1. **Primary Description**: First substantial content line
2. **Usage Examples**: From code blocks in documentation
3. **Fallback Text**: Generic description if parsing fails
4. **Truncation**: Limits description length for table formatting

## Update System Features

### Update Process Installation Detection
Automatically detects installation type and location:
```bash
📍 Found project installation at: /path/to/project/.claude/commands
📍 Found global installation at: ~/.claude/commands
```

### Release Management
- **GitHub API Integration**: Uses `gh` CLI for reliable release detection
- **Version Tracking**: Shows current and available versions
- **Release Notes**: Links to GitHub release information

### Safe Update Process
1. **Backup Creation**: `{install_dir}.backup.{timestamp}`
2. **Download**: Uses GitHub API to fetch latest release tarball
3. **Verification**: Confirms download integrity and structure
4. **Installation**: Replaces old commands with new versions
5. **Cleanup**: Provides instructions for removing backups

### Progress Tracking
Visual feedback for all operations:
- **🔍 Checking**: Network operation to find latest release
- **⬇️ Downloading**: Release tarball download with spinner
- **📦 Extracting**: Archive extraction progress
- **🔄 Updating**: File-by-file replacement with progress bar

### Error Recovery
If update fails at any stage:
- **Automatic Rollback**: Restores from backup immediately
- **Error Reporting**: Clear messages about what went wrong
- **Recovery Instructions**: Guidance for manual recovery
- **Backup Preservation**: Keeps backup for manual investigation

## Prerequisites

### For Help Display
- Commands installed in `.claude/commands/` directory
- Readable markdown files with proper structure

### For Updates
- **GitHub CLI**: `gh` command must be installed and authenticated
- **Internet Access**: Required for GitHub API and download
- **File Permissions**: Write access to installation directory
- **Archive Tools**: `tar` command for extraction

## Installation Locations

### Project Installation
```
project-root/
└── .claude/
    └── commands/
        ├── learn.md
        ├── github-init.md
        └── menuconfig.md
```

### Global Installation
```
~/.claude/
└── commands/
    ├── learn.md
    ├── github-init.md
    └── menuconfig.md
```

## Troubleshooting

### No Commands Found
```bash
❌ No claude-slash commands found
Install commands by downloading and running install.sh from:
https://github.com/jeremyeder/claude-slash
```

**Solution**: Run the installer script to set up commands.

### Update Failed
```bash
❌ Failed to download release: network error
🔄 Restoring from backup...
```

**Solution**: Check internet connection and GitHub CLI authentication.

### Permission Denied
```bash
❌ Failed to create backup: Permission denied
```

**Solution**: Ensure write permissions to installation directory.

## Tips
- Run `/slash` regularly to discover new commands
- Use `/slash update` to stay current with latest features
- Check backup directory after updates for rollback if needed
- Commands work in both project and global installation modes
