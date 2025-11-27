# Bookmark Command - Project-Specific Bookmark Management

Manage project-specific bookmarks for URLs, notes, and code snippets with automatic categorization and persistence.

## Usage

```bash
/bookmark add <text>          # Add a bookmark
/bookmark -a <text>           # Add a bookmark (short form)
/bookmark list                # List all bookmarks
/bookmark -l                  # List all bookmarks (short form)
/bookmark remove <index>      # Remove bookmark by index
/bookmark -r <index>          # Remove bookmark by index (short form)
/bookmark -h                  # Show help
```

## Description

The Bookmark command provides a lightweight, project-specific bookmark management system that automatically categorizes bookmarks into URLs, Notes, and Code Snippets. Bookmarks are stored in `.claude/BOOKMARKS.md` and automatically loaded into every Claude Code session via a reference in `CLAUDE.md`.

### Key Features

- **Auto-categorization**: Automatically sorts bookmarks into URLs, Notes, or Code Snippets based on content
- **Global sequential numbering**: All bookmarks numbered 1, 2, 3... across categories for easy reference
- **Persistent storage**: Bookmarks stored in `.claude/BOOKMARKS.md` and committed to repo
- **Auto-load integration**: Automatically referenced in `CLAUDE.md` for seamless access
- **Automatic renumbering**: When removing bookmarks, remaining ones are renumbered sequentially
- **Team sharing**: Bookmarks committed to repo by default for team collaboration

### Categorization Rules

1. **URLs**: Text starts with `http://`, `https://`, or `www.`
2. **Code Snippets**: Text contains: `pytest`, `npm`, `git`, `python`, `bash`, backticks, pipe `|`, `&&`, `./`
3. **Notes**: Everything else (default category)

### Storage Structure

Bookmarks are stored in `.claude/BOOKMARKS.md` with this structure:

```markdown
# Project Bookmarks

*Last updated: YYYY-MM-DD*

## URLs

1. https://example.com - Description
2. www.example.org

## Notes

3. Remember to check X before Y

## Code Snippets

4. pytest tests/ -v --cov=src
```

## Examples

### Adding Bookmarks

```bash
# Add a URL
/bookmark add https://docs.example.com/api - API documentation

# Add a note
/bookmark -a Remember to use the Xcode simulator

# Add a code snippet
/bookmark add pytest tests/ -v --cov=src
```

### Listing Bookmarks

```bash
/bookmark list
# or
/bookmark -l

# Output:
# 📚 Project Bookmarks (3 total):
#
# URLs (1):
#   1. https://docs.example.com/api - API documentation
#
# Notes (1):
#   2. Remember to use the Xcode simulator
#
# Code Snippets (1):
#   3. pytest tests/ -v --cov=src
```

### Removing Bookmarks

```bash
# Remove bookmark #2
/bookmark remove 2
# or
/bookmark -r 2

# Output:
# ✓ Removed bookmark #2: "Remember to use the Xcode simulator"
# 2 bookmark(s) remaining
```

## Initialization

On first use, the bookmark command automatically:

1. Creates `.claude/` directory if it doesn't exist
2. Creates `.claude/BOOKMARKS.md` with template structure
3. Adds a reference to `CLAUDE.md` (if not already present):

```markdown
## Project Bookmarks
See `.claude/BOOKMARKS.md` for project-specific URLs and notes.
```

This ensures bookmarks are automatically loaded into every Claude Code session.

## Security Notes

- **Do NOT store credentials** directly in bookmarks
- Use references instead: "API key in 1Password"
- Bookmarks are committed to version control by default
- Add `.claude/BOOKMARKS.md` to `.gitignore` if needed for private bookmarks

## Implementation

This command is implemented as a Python class that integrates with the Typer CLI framework.

### Technical Details

- **Framework**: Python with Typer
- **Storage**: Markdown files in `.claude/` directory
- **Auto-loading**: Via `CLAUDE.md` reference
- **Numbering**: Global sequential across all categories
- **Error Handling**: Comprehensive validation and user feedback

### Dependencies

- Python 3.13+
- Typer for CLI argument handling
- Standard library modules (pathlib, re, datetime)

## Related Commands

- `/learn` - Extract learnings from sessions
- `/github-init` - Repository initialization
- Other project management commands

## Notes

- Bookmarks are project-specific (stored in project's `.claude/` directory)
- Global sequential numbering makes removal by index straightforward
- Automatic renumbering prevents gaps in bookmark indices
- First bookmark triggers auto-setup of `CLAUDE.md` reference
- Works seamlessly with both slash command and CLI interfaces
