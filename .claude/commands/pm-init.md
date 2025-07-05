# Project Management Init Command

Alias for project:setup - Create comprehensive GitHub project management workflow.

## Usage

```bash
/pm:init [project_type] [sprint_days]
```

## Description

Shorthand alias for `/project:setup`. Creates complete collaborative development workflow including:

- GitHub project board with comprehensive fields for time tracking
- Complete label system and issue templates
- Automated progress reporting and quality gates
- Documentation framework with test coverage requirements

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")

# This is an alias - call the main project-setup command
!source "$(dirname "${BASH_SOURCE[0]}")/project-setup.md"