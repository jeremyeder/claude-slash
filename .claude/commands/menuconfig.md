# CLAUDE.md Menuconfig - Interactive Configuration Editor

Interactive text-based configuration interface for CLAUDE.md files, inspired by Linux kernel menuconfig.

## Usage
```
/menuconfig                    # Edit project/global CLAUDE.md
/menuconfig custom.md          # Edit specific file
/menuconfig /path/to/file.md   # Edit specific file with full path
```

## Description

A Terminal User Interface (TUI) editor that provides a Linux kernel menuconfig-style interface for managing CLAUDE.md files. Navigate hierarchical sections, toggle them enabled/disabled, and edit configuration files interactively.

### Features
- **🐧 Linux Kernel Style**: Familiar menuconfig interface with keyboard shortcuts
- **🗂️ Hierarchical Navigation**: Browse sections as a tree structure
- **⚡ Real-time Editing**: Toggle sections on/off with immediate visual feedback
- **🔍 Search Functionality**: Find sections quickly with built-in search
- **💾 Automatic Backup**: Creates backups before making changes
- **📱 Responsive Design**: Terminal-friendly interface that works everywhere

### Interface Elements
- `[*]` - Section enabled (will be included in output)
- `[ ]` - Section disabled (will be excluded from output)
- `-->` - Section has subsections (expandable)

### Keyboard Controls

#### Navigation
- `↑/↓` or `j/k` - Navigate up/down through sections
- `←/→` or `h/l` - Collapse/expand sections
- `Enter` - Expand/collapse current section
- `Home/End` - Jump to first/last item

#### Actions
- `Space` - Toggle section enabled/disabled
- `s` - Save configuration to file
- `/` - Search sections by name
- `?` - Show help screen with all shortcuts
- `q` or `Escape` - Exit (prompts to save if modified)

### File Selection Logic
When no file is specified, the command automatically selects:
1. **Project CLAUDE.md**: `./CLAUDE.md` (if in git repository)
2. **Global CLAUDE.md**: `~/.claude/CLAUDE.md` (fallback)
3. **Error**: If neither exists, shows helpful error message

### Safe Editing
- **Backup Creation**: Original file backed up as `.md.menuconfig.bak`
- **Modification Tracking**: Status bar shows if file has unsaved changes
- **Exit Confirmation**: Prompts to save when exiting with changes
- **Error Recovery**: Graceful error handling with helpful messages

## Examples

### Edit Project Configuration
```bash
/menuconfig
# Automatically finds and edits project CLAUDE.md or global fallback
```

### Edit Specific File
```bash
/menuconfig my-config.md
# Opens specified markdown file in menuconfig interface
```

### Edit with Full Path
```bash
/menuconfig /Users/username/projects/config.md
# Opens file at absolute path
```

## Interface Walkthrough

### Main Screen
```
┌─ CLAUDE.md Configuration ────────────────────────┐
│ [*] Core Operating Philosophy          -->       │
│ [*]   Dynamic Framework Selection                │
│ [ ]   Strategic Analysis Framework               │
│ [*] Team Topologies                   -->        │
│ [*]   Stream-Aligned Teams                       │
│ [ ]   Platform Teams                             │
│ [*] Key Operating Principles                     │
└───────────────────────────────────────────────────┘
File: ./CLAUDE.md | 15 sections loaded | Space=toggle, s=save, ?=help
```

### Status Bar Information
- **File Path**: Shows which CLAUDE.md file is being edited
- **Modification Status**: `[MODIFIED]` indicator for unsaved changes
- **Section Count**: Total number of sections loaded
- **Quick Help**: Essential keyboard shortcuts

### Search Interface
Press `/` to open search:
```
┌─ Search sections: ────────────┐
│ Enter search term...          │
│ [Search] [Cancel]             │
└───────────────────────────────┘
```

### Help Screen
Press `?` for complete keyboard reference:
```
┌─ CLAUDE.md Menuconfig Help ──────────────────────┐
│ Navigation:                                       │
│   ↑/↓, j/k    Navigate sections                  │
│   →/←, l/h    Expand/collapse                    │
│   Space       Toggle enabled/disabled            │
│   s           Save configuration                 │
│   /           Search sections                    │
│   ?           Show help                          │
│   q, Escape   Exit                              │
└───────────────────────────────────────────────────┘
```

## Technical Details

### File Structure Support
- Supports any depth of markdown headers (`#`, `##`, `###`, etc.)
- Preserves section hierarchy and relationships
- Handles nested content blocks and code sections
- Maintains original formatting for enabled sections

### Content Processing
- **Header Recognition**: Parses `#` through `######` headers
- **Code Block Safety**: Ignores headers inside code blocks
- **Content Preservation**: Maintains exact formatting of section content
- **Hierarchical Structure**: Parent-child relationships preserved

### Error Handling
- **Missing Files**: Clear error messages with search paths
- **Parse Errors**: Graceful handling of malformed markdown
- **Permission Issues**: Helpful messages for access problems
- **Recovery Options**: Backup restoration in case of errors

## Tips
- Use search (`/`) to quickly find sections in large files
- Toggle parent sections to enable/disable entire hierarchies
- Save frequently (`s`) when making many changes
- Check the status bar for unsaved modifications
- Use `--help` flag with CLI for additional options
