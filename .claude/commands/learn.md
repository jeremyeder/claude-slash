# Learn Command - Interactive Learning Integration

Continuously refine the global CLAUDE.md file with impactful learnings from the current session through an interactive integration interface.

## Usage

Extract and integrate session learnings into CLAUDE.md:

```bash
/learn                    # Start interactive learning session
claude-slash learn        # Learn session (CLI mode)
```

## Description

The Learn command provides an autonomous analysis system for Claude Code sessions that extracts important insights, patterns, and learnings, then provides an interactive interface for integrating them into the global CLAUDE.md file.

### Key Features

- **Session Context Analysis**: Analyzes current Claude Code session for meaningful insights
- **Interactive Integration**: Provides user-friendly interface for reviewing and integrating learnings
- **Smart Section Suggestions**: Suggests appropriate CLAUDE.md sections based on content analysis
- **Automatic Backup**: Creates backup before making any changes
- **Flexible Integration**: Multiple integration modes (append, insert, manual)
- **Rich Terminal Output**: Progress tracking and formatted displays

### Integration Modes

1. **Append Mode**: Add learning to end of selected section
2. **Insert Mode**: Add learning after section header
3. **Manual Mode**: Show content for manual copy/paste integration

### Learning Categories

The system analyzes for patterns in:
- Git workflow improvements
- Testing and debugging insights
- Development best practices
- Strategic decision patterns
- Code quality enhancements
- Process optimization learnings

## Implementation

This command is implemented as a Python class in `src/claude_slash/commands/learn.py` that integrates with the Typer CLI framework and Rich terminal UI library.

### Technical Details

- **Framework**: Python with Typer/Rich
- **UI**: Interactive prompts and formatted displays
- **File Handling**: Safe backup and content management
- **Integration**: Works with both project and global CLAUDE.md files
- **Error Handling**: Comprehensive error handling and user feedback

### Dependencies

- Python 3.13+
- Rich library for terminal formatting
- Typer for CLI argument handling
- Standard library modules (datetime, pathlib, shutil)

## Examples

### Basic Learning Session
```bash
# Start interactive learning extraction
/learn
```

### Expected Workflow
1. Command analyzes current session context
2. Presents extracted learnings for review
3. User confirms integration
4. Backup is created automatically
5. User selects target section in CLAUDE.md
6. Learning is integrated using chosen mode
7. Success confirmation with backup location

## Related Commands

- `/menuconfig` - TUI editor for CLAUDE.md structure
- `/github-init` - Repository initialization with best practices
- Other workflow optimization commands

## Notes

- Requires existing global CLAUDE.md file at `~/.claude/CLAUDE.md`
- Creates timestamped backups before any modifications
- Supports both project-local and global CLAUDE.md files
- Designed for continuous improvement of development practices
